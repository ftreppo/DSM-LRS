#!/usr/bin/env python3
"""DSM-LRS T111 weekly World News pipeline v0.1.

PUBLIC-only deterministic staging/dedup/approval/export mechanics.
Discovery is supplied as a candidate batch (e.g. by the scheduled ChatGPT task).
This module never performs approval or publication by itself.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import unicodedata
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from jsonschema import Draft202012Validator, FormatChecker

TRACKING_PARAMS = {
    "fbclid", "gclid", "dclid", "mc_cid", "mc_eid", "mkt_tok", "ref", "ref_src"
}
PROHIBITED_PRIVATE_KEYS = {
    "student_name", "student_id", "student_email", "member_email", "member_id",
    "diagnosis", "diagnostic_report", "clinical_data", "health_data", "pdp",
    "foerderplan", "förderplan", "whatsapp_message", "whatsapp_chat", "private_note",
    "private_data", "raw_pdp", "raw_diagnosis"
}
SECRET_PATTERNS = [
    re.compile(r"(?i)(api[_-]?key|secret|password|bearer\s+[A-Za-z0-9._~+/-]{12,})"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")
]
VALID_RESULTS = {"NEW", "DUPLICATE_SKIPPED", "UPDATED_EXISTING", "REJECTED"}
STABLE_ID_KINDS = {"doi", "pmid", "publisher_id"}


def canonical_json_bytes(obj: Any) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha256_obj(obj: Any) -> str:
    return sha256_bytes(canonical_json_bytes(obj))


def read_json(path: str | Path) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: str | Path, obj: Any) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, sort_keys=False)
        f.write("\n")


def normalize_text(value: str) -> str:
    text = unicodedata.normalize("NFKC", value or "").casefold().strip()
    text = re.sub(r"[^\w\s]", " ", text, flags=re.UNICODE)
    return re.sub(r"\s+", " ", text).strip()


def normalize_identity(kind: str, value: str) -> str:
    k = (kind or "").casefold().strip()
    v = unicodedata.normalize("NFKC", value or "").strip()
    if k == "doi":
        v = re.sub(r"(?i)^https?://(?:dx\.)?doi\.org/", "", v)
        v = re.sub(r"(?i)^doi:\s*", "", v).strip().casefold()
    elif k in {"pmid", "publisher_id"}:
        v = v.casefold()
    elif k == "canonical_url":
        v = canonicalize_url(v)
    return v


def canonicalize_url(url: str) -> str:
    parts = urlsplit((url or "").strip())
    if parts.scheme.casefold() != "https" or not parts.netloc:
        return (url or "").strip()
    scheme = "https"
    host = parts.netloc.casefold()
    if host.endswith(":443"):
        host = host[:-4]
    path = re.sub(r"/{2,}", "/", parts.path or "/")
    if path != "/":
        path = path.rstrip("/")
    kept = []
    for k, v in parse_qsl(parts.query, keep_blank_values=True):
        lk = k.casefold()
        if lk.startswith("utm_") or lk in TRACKING_PARAMS:
            continue
        kept.append((k, v))
    query = urlencode(sorted(kept))
    return urlunsplit((scheme, host, path, query, ""))


def get_records(dataset: Any) -> List[Dict[str, Any]]:
    if isinstance(dataset, dict) and isinstance(dataset.get("records"), list):
        return dataset["records"]
    if isinstance(dataset, list):
        return dataset
    raise ValueError("dataset must be a list or object containing records[]")


def is_world_news(r: Dict[str, Any]) -> bool:
    return r.get("record_type") == "external_news"


def source_key(r: Dict[str, Any]) -> str:
    s = r.get("source") or {}
    return normalize_text(str(s.get("id") or s.get("name") or ""))


def fallback_key(r: Dict[str, Any]) -> Optional[str]:
    src = source_key(r)
    title = normalize_text(str(r.get("original_title") or ""))
    date = str(r.get("publication_date") or "")
    if src and title and date:
        return f"{src}|{title}|{date}"
    return None


def identity_key(r: Dict[str, Any]) -> Optional[Tuple[str, str]]:
    ci = r.get("content_identity") or {}
    k = str(ci.get("kind") or "").casefold()
    v = str(ci.get("value") or "")
    if k in STABLE_ID_KINDS and v:
        return (k, normalize_identity(k, v))
    return None


def canonical_url_key(r: Dict[str, Any]) -> Optional[str]:
    u = str(r.get("canonical_url") or "")
    if not u:
        ci = r.get("content_identity") or {}
        if str(ci.get("kind") or "").casefold() == "canonical_url":
            u = str(ci.get("value") or "")
    if not u:
        return None
    c = canonicalize_url(u)
    return c if c.startswith("https://") else None


def source_fingerprint(r: Dict[str, Any]) -> str:
    """Fingerprint only externally observable/source metadata, not AI text/state."""
    s = r.get("source") or {}
    obj = {
        "source_id": s.get("id"),
        "source_name": s.get("name"),
        "canonical_url": canonical_url_key(r),
        "source_country": r.get("source_country"),
        "publication_date": r.get("publication_date"),
        "original_language": r.get("original_language"),
        "source_terminology": sorted(r.get("source_terminology") or []),
        "categories": sorted(r.get("categories") or []),
        "original_title": r.get("original_title"),
        "original_excerpt": r.get("original_excerpt"),
    }
    return sha256_obj(obj)


@dataclass
class Match:
    record: Dict[str, Any]
    rule: str


class DedupIndex:
    def __init__(self, records: Iterable[Dict[str, Any]]):
        self.by_identity: Dict[Tuple[str, str], Dict[str, Any]] = {}
        self.by_url: Dict[str, Dict[str, Any]] = {}
        self.by_fallback: Dict[str, Dict[str, Any]] = {}
        for r in records:
            if not is_world_news(r):
                continue
            ik = identity_key(r)
            uk = canonical_url_key(r)
            fk = fallback_key(r)
            if ik:
                self.by_identity.setdefault(ik, r)
            if uk:
                self.by_url.setdefault(uk, r)
            if fk:
                self.by_fallback.setdefault(fk, r)

    def match(self, r: Dict[str, Any]) -> Optional[Match]:
        ik = identity_key(r)
        if ik and ik in self.by_identity:
            return Match(self.by_identity[ik], "DOI_OR_STABLE_ID")
        uk = canonical_url_key(r)
        if uk and uk in self.by_url:
            return Match(self.by_url[uk], "CANONICAL_URL")
        fk = fallback_key(r)
        if fk and fk in self.by_fallback:
            return Match(self.by_fallback[fk], "SOURCE_NORMALIZED_TITLE_DATE")
        return None


def recursive_private_scan(obj: Any, path: str = "$") -> List[str]:
    issues: List[str] = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            nk = unicodedata.normalize("NFKC", str(k)).casefold().replace("-", "_")
            if nk in PROHIBITED_PRIVATE_KEYS:
                issues.append(f"prohibited_key:{path}.{k}")
            issues.extend(recursive_private_scan(v, f"{path}.{k}"))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            issues.extend(recursive_private_scan(v, f"{path}[{i}]"))
    elif isinstance(obj, str):
        for rx in SECRET_PATTERNS:
            if rx.search(obj):
                issues.append(f"secret_pattern:{path}")
    return issues


def prepare_candidate(raw: Dict[str, Any], run_timestamp: str) -> Dict[str, Any]:
    c = copy.deepcopy(raw)
    c["schema_version"] = "1.0"
    c["record_type"] = "external_news"
    c["canonical_url"] = canonicalize_url(str(c.get("canonical_url") or c.get("source_url") or ""))
    c["source_url"] = canonicalize_url(str(c.get("source_url") or c.get("canonical_url") or ""))
    ci = c.get("content_identity") or {}
    kind = str(ci.get("kind") or "canonical_url").casefold()
    value = str(ci.get("value") or c["canonical_url"])
    c["content_identity"] = {"kind": kind, "value": normalize_identity(kind, value)}
    seed = f"{kind}:{c['content_identity']['value']}" if c["content_identity"]["value"] else (fallback_key(c) or c["canonical_url"])
    c["id"] = "worldnews_" + hashlib.sha256(seed.encode("utf-8")).hexdigest()[:20]
    c["approval_status"] = "DRAFT"
    c["publication_status"] = "UNPUBLISHED"
    c["version"] = max(1, int(c.get("version") or 1))
    c["fetched_at"] = c.get("fetched_at") or run_timestamp

    # Candidate output is always DRAFT-first. Original source metadata may stay INGESTED;
    # all generated variants must remain DRAFT.
    for lang, variant in (c.get("content") or {}).items():
        prov = variant.get("provenance") or {}
        if prov.get("kind") == "AI_TRANSLATION_SUMMARY":
            variant["status"] = "DRAFT"
            prov.pop("approved_by", None)
            prov.pop("approved_at", None)
        elif variant.get("status") not in {"INGESTED", "DRAFT"}:
            variant["status"] = "DRAFT"
            prov.pop("approved_by", None)
            prov.pop("approved_at", None)
        variant["provenance"] = prov

    prov = c.setdefault("provenance", {})
    prov.setdefault("discovery_method", "deterministic_html")
    meta = copy.deepcopy(c)
    meta.pop("provenance", None)
    meta.pop("fetched_at", None)
    meta.pop("approval_status", None)
    meta.pop("publication_status", None)
    prov["metadata_hash"] = "sha256:" + sha256_obj(meta)
    return c


def validate_candidate(c: Dict[str, Any], schema: Dict[str, Any], *, test_mode: bool = False) -> List[str]:
    issues = recursive_private_scan(c)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    for e in sorted(validator.iter_errors(c), key=lambda x: list(x.absolute_path)):
        p = ".".join(str(x) for x in e.absolute_path)
        issues.append(f"schema:{p}:{e.message}")
    if c.get("approval_status") != "DRAFT" or c.get("publication_status") != "UNPUBLISHED":
        issues.append("candidate_not_draft_unpublished")
    if not str(c.get("canonical_url") or "").startswith("https://"):
        issues.append("canonical_url_not_https")
    # `example.org` is accepted only for deterministic dry-run fixtures.
    if "example.org" in str(c.get("canonical_url") or "") and not test_mode:
        issues.append("test_fixture_url_in_production")
    return issues


def build_prior_records(prior_drafts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for draft in prior_drafts:
        out.extend(draft.get("candidate_records") or [])
    return out


def process_weekly(
    *,
    accepted_baseline: Dict[str, Any],
    stale_baseline: Dict[str, Any],
    candidates: List[Dict[str, Any]],
    schema: Dict[str, Any],
    run_date: str,
    run_timestamp: str,
    search_window: Dict[str, str],
    prior_drafts: Optional[List[Dict[str, Any]]] = None,
    baseline_refs: Optional[Dict[str, str]] = None,
    test_mode: bool = False,
) -> Dict[str, Any]:
    accepted_records = get_records(accepted_baseline)
    stale_records = get_records(stale_baseline)
    prior_records = build_prior_records(prior_drafts or [])
    baseline_index = DedupIndex(accepted_records)
    prior_index = DedupIndex(prior_records)

    accepted_non_news = [r for r in accepted_records if not is_world_news(r)]
    stale_non_news = [r for r in stale_records if not is_world_news(r)]
    non_news_preserved = accepted_non_news == stale_non_news

    results = []
    candidate_records = []
    approval_queue = []
    counts = {k: 0 for k in ["NEW", "DUPLICATE_SKIPPED", "UPDATED_EXISTING", "REJECTED"]}

    for i, raw in enumerate(candidates, start=1):
        prepared = prepare_candidate(raw, run_timestamp)
        issues = validate_candidate(prepared, schema, test_mode=test_mode)
        if issues:
            result = {
                "candidate_index": i,
                "result": "REJECTED",
                "candidate_id": prepared.get("id"),
                "reason_codes": issues,
                "canonical_url": prepared.get("canonical_url"),
                "original_title": prepared.get("original_title"),
            }
            results.append(result)
            counts["REJECTED"] += 1
            continue

        prior_match = prior_index.match(prepared)
        if prior_match:
            results.append({
                "candidate_index": i,
                "result": "DUPLICATE_SKIPPED",
                "candidate_id": prepared["id"],
                "match_rule": f"PRIOR_RUN:{prior_match.rule}",
                "matched_id": prior_match.record.get("id"),
                "canonical_url": prepared["canonical_url"],
                "original_title": prepared["original_title"],
            })
            counts["DUPLICATE_SKIPPED"] += 1
            continue

        match = baseline_index.match(prepared)
        if match:
            same_source = source_fingerprint(prepared) == source_fingerprint(match.record)
            label = "DUPLICATE_SKIPPED" if same_source else "UPDATED_EXISTING"
            results.append({
                "candidate_index": i,
                "result": label,
                "candidate_id": prepared["id"],
                "match_rule": match.rule,
                "matched_id": match.record.get("id"),
                "canonical_url": prepared["canonical_url"],
                "original_title": prepared["original_title"],
            })
            counts[label] += 1
            if label == "UPDATED_EXISTING":
                prepared["version"] = int(match.record.get("version") or 1) + 1
                prepared.setdefault("provenance", {})["update_of"] = match.record.get("id")
                candidate_records.append(prepared)
                approval_queue.append(approval_item(prepared, label, match.record.get("id")))
            continue

        results.append({
            "candidate_index": i,
            "result": "NEW",
            "candidate_id": prepared["id"],
            "canonical_url": prepared["canonical_url"],
            "original_title": prepared["original_title"],
        })
        counts["NEW"] += 1
        candidate_records.append(prepared)
        approval_queue.append(approval_item(prepared, "NEW", None))

    baseline = {
        "accepted_record_count": len(accepted_records),
        "accepted_world_news_count": sum(is_world_news(r) for r in accepted_records),
        "accepted_non_world_news_count": len(accepted_non_news),
        "accepted_snapshot_sha256": sha256_obj(accepted_baseline),
        "stale_record_count": len(stale_records),
        "stale_world_news_count": sum(is_world_news(r) for r in stale_records),
        "stale_snapshot_sha256": sha256_obj(stale_baseline),
        "stale_missing_published_records": sorted({r.get("id") for r in accepted_records} - {r.get("id") for r in stale_records}),
        "non_world_news_semantically_identical": non_news_preserved,
        "dedup_authority": "ACCEPTED_PUBLISHED_BASELINE",
        "refs": baseline_refs or {},
    }

    draft = {
        "schema_version": "1.0",
        "artifact_type": "WORLD_NEWS_WEEKLY_DRAFT",
        "artifact_name": f"WORLD_NEWS_WEEKLY_DRAFT_{run_date}",
        "run_date": run_date,
        "run_timestamp": run_timestamp,
        "data_boundary": "PUBLIC_ONLY",
        "publication_behavior": "DRAFT_STAGING_ONLY_NO_AUTO_PUBLICATION",
        "search_window": search_window,
        "baseline": baseline,
        "prior_run_count": len(prior_drafts or []),
        "result_counts": counts,
        "dedup_order": ["DOI_OR_STABLE_ID", "CANONICAL_URL", "SOURCE_NORMALIZED_TITLE_DATE"],
        "results": results,
        "candidate_records": candidate_records,
        "approval_queue": approval_queue,
        "invariants": {
            "ai_cannot_auto_approve": all(r.get("approval_status") == "DRAFT" for r in candidate_records),
            "all_candidates_unpublished": all(r.get("publication_status") == "UNPUBLISHED" for r in candidate_records),
            "non_world_news_preserved_against_stale_baseline": non_news_preserved,
            "accepted_baseline_prevents_stale_duplicate_publication": len(accepted_records) > len(stale_records),
        },
    }
    draft["artifact_sha256"] = sha256_obj({k:v for k,v in draft.items() if k != "artifact_sha256"})
    return draft


def approval_item(c: Dict[str, Any], result: str, matched_id: Optional[str]) -> Dict[str, Any]:
    return {
        "candidate_id": c["id"],
        "result": result,
        "matched_id": matched_id,
        "source": c["source"],
        "canonical_url": c["canonical_url"],
        "content_identity": c["content_identity"],
        "publication_date": c["publication_date"],
        "original_language": c["original_language"],
        "original_title": c["original_title"],
        "source_country": c["source_country"],
        "source_terminology": c["source_terminology"],
        "categories": c["categories"],
        "review_required": [
            "source_and_canonical_link", "factual_summary", "source_terminology",
            "country_jurisdiction", "categories", "publication_date", "original_language",
            "per_language_variant"
        ],
        "decision": "PENDING_HUMAN_ADMIN",
    }


def validate_approval(decision: Dict[str, Any]) -> List[str]:
    issues=[]
    if decision.get("actor_type") not in {"HUMAN", "ADMIN"}:
        issues.append("actor_type_must_be_HUMAN_or_ADMIN")
    by=str(decision.get("approved_by") or "")
    if not by or re.match(r"(?i)^ai(?:$|[-_ ])", by):
        issues.append("approved_by_must_be_human_admin_identity")
    if decision.get("decision") not in {"APPROVED", "REJECTED"}:
        issues.append("invalid_decision")
    if not isinstance(decision.get("language_decisions"), dict):
        issues.append("language_decisions_required")
    return issues


def project_candidate_to_public(c: Dict[str, Any], decision: Dict[str, Any]) -> Dict[str, Any]:
    if validate_approval(decision):
        raise ValueError("invalid approval: " + ";".join(validate_approval(decision)))
    if decision["decision"] != "APPROVED":
        raise ValueError("candidate is not approved")
    content={}
    for lang, d in decision["language_decisions"].items():
        if d != "APPROVED":
            continue
        if lang not in c.get("content", {}):
            continue
        v=copy.deepcopy(c["content"][lang])
        v["status"]="APPROVED"
        v.setdefault("provenance", {})["approved_by"]=decision["approved_by"]
        v["provenance"]["approved_at"]=decision["approved_at"]
        content[lang]=v
    if c["original_language"] not in content:
        raise ValueError("approved export must include an approved original-language variant")
    return {
        "id": c["id"],
        "record_type": "external_news",
        "zone": "PUBLIC",
        "audiences": ["PUBLIC"],
        "original_language": c["original_language"],
        "approval_status": "APPROVED",
        "publication_status": "PUBLISHED",
        "source": {
            "id": c["source"]["id"],
            "name": c["source"]["name"],
            "country": c["source_country"],
        },
        "source_url": c["source_url"],
        "canonical_url": c["canonical_url"],
        "content_identity": copy.deepcopy(c["content_identity"]),
        "source_country": c["source_country"],
        "publication_date": c["publication_date"],
        "source_terminology": copy.deepcopy(c["source_terminology"]),
        "categories": copy.deepcopy(c["categories"]),
        "original_title": c["original_title"],
        "provenance": {
            "discovery_method": c["provenance"]["discovery_method"],
            "metadata_hash": c["provenance"]["metadata_hash"],
            "approved_by": decision["approved_by"],
            "approved_at": decision["approved_at"],
        },
        "content": content,
    }


def merge_approved(
    *, accepted_baseline: Dict[str, Any], draft: Dict[str, Any], approvals: Dict[str, Any]
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    base_records = copy.deepcopy(get_records(accepted_baseline))
    non_news_before = [r for r in base_records if not is_world_news(r)]
    by_id = {r.get("id"): i for i, r in enumerate(base_records)}
    approval_by_id = {d["candidate_id"]: d for d in approvals.get("decisions", [])}
    applied=[]
    skipped=[]
    for c in draft.get("candidate_records", []):
        d=approval_by_id.get(c["id"])
        if not d:
            skipped.append({"candidate_id":c["id"],"reason":"NO_HUMAN_ADMIN_DECISION"})
            continue
        issues=validate_approval(d)
        if issues:
            skipped.append({"candidate_id":c["id"],"reason":"INVALID_APPROVAL","issues":issues})
            continue
        if d["decision"] != "APPROVED":
            skipped.append({"candidate_id":c["id"],"reason":"REJECTED_BY_HUMAN_ADMIN"})
            continue
        pub=project_candidate_to_public(c,d)
        update_of=(c.get("provenance") or {}).get("update_of")
        target_id=update_of or c["id"]
        if update_of and update_of in by_id:
            # Preserve the existing public ID on a reviewed update; publication state changes only here,
            # after explicit HUMAN/ADMIN approval.
            pub["id"]=update_of
            base_records[by_id[update_of]]=pub
            applied.append({"candidate_id":c["id"],"action":"UPDATED_EXISTING","public_id":update_of})
        elif c["id"] not in by_id:
            base_records.append(pub)
            by_id[c["id"]]=len(base_records)-1
            applied.append({"candidate_id":c["id"],"action":"ADDED_NEW","public_id":c["id"]})
        else:
            skipped.append({"candidate_id":c["id"],"reason":"PUBLIC_ID_ALREADY_EXISTS"})

    non_news_after=[r for r in base_records if not is_world_news(r)]
    out={"schema_version":accepted_baseline.get("schema_version","1.0"),"records":base_records}
    report={
        "applied":applied,
        "skipped":skipped,
        "record_count":len(base_records),
        "world_news_count":sum(is_world_news(r) for r in base_records),
        "non_world_news_count":len(non_news_after),
        "non_world_news_unchanged":non_news_before==non_news_after,
        "privacy_issues":recursive_private_scan(out),
    }
    report["snapshot_sha256"]=sha256_obj(out)
    return out, report


def validate_public_dataset(dataset: Dict[str, Any]) -> List[str]:
    issues=recursive_private_scan(dataset)
    ids=set()
    for idx,r in enumerate(get_records(dataset)):
        rid=r.get("id")
        if not rid or rid in ids:
            issues.append(f"duplicate_or_missing_id:{idx}:{rid}")
        ids.add(rid)
        if r.get("zone") not in {None,"PUBLIC"}:
            issues.append(f"non_public_zone:{rid}")
        if r.get("approval_status") != "APPROVED" or r.get("publication_status") != "PUBLISHED":
            issues.append(f"not_approved_published:{rid}")
        if is_world_news(r):
            if not str(r.get("canonical_url") or "").startswith("https://"):
                issues.append(f"worldnews_https:{rid}")
            s=r.get("source") or {}
            if not s.get("name") or not (r.get("source_country") or s.get("country")):
                issues.append(f"worldnews_source_display:{rid}")
            if not r.get("publication_date") or not r.get("original_language") or not r.get("source_terminology"):
                issues.append(f"worldnews_display_metadata:{rid}")
            for lang,v in (r.get("content") or {}).items():
                if v.get("status") != "APPROVED":
                    issues.append(f"unapproved_public_variant:{rid}:{lang}")
    return issues


def main() -> None:
    ap=argparse.ArgumentParser()
    sub=ap.add_subparsers(dest="cmd",required=True)
    p=sub.add_parser("stage")
    p.add_argument("--accepted",required=True); p.add_argument("--stale",required=True)
    p.add_argument("--candidates",required=True); p.add_argument("--schema",required=True)
    p.add_argument("--run-date",required=True); p.add_argument("--run-timestamp",required=True)
    p.add_argument("--search-from",required=True); p.add_argument("--search-to",required=True)
    p.add_argument("--prior",action="append",default=[]); p.add_argument("--output",required=True)
    p.add_argument("--test-mode",action="store_true")
    e=sub.add_parser("export")
    e.add_argument("--accepted",required=True); e.add_argument("--draft",required=True)
    e.add_argument("--approvals",required=True); e.add_argument("--output",required=True); e.add_argument("--report",required=True)
    v=sub.add_parser("validate-public"); v.add_argument("--input",required=True)
    args=ap.parse_args()
    if args.cmd=="stage":
        prior=[read_json(x) for x in args.prior]
        draft=process_weekly(accepted_baseline=read_json(args.accepted),stale_baseline=read_json(args.stale),candidates=read_json(args.candidates)["candidates"],schema=read_json(args.schema),run_date=args.run_date,run_timestamp=args.run_timestamp,search_window={"from":args.search_from,"to":args.search_to},prior_drafts=prior,test_mode=args.test_mode)
        write_json(args.output,draft)
    elif args.cmd=="export":
        out,report=merge_approved(accepted_baseline=read_json(args.accepted),draft=read_json(args.draft),approvals=read_json(args.approvals))
        report["validation_issues"]=validate_public_dataset(out)
        write_json(args.output,out); write_json(args.report,report)
    else:
        issues=validate_public_dataset(read_json(args.input))
        print(json.dumps({"status":"PASS" if not issues else "FAIL","issues":issues},ensure_ascii=False,indent=2))
        raise SystemExit(0 if not issues else 1)

if __name__=="__main__":
    main()
