import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import world_news_weekly_pipeline_v0_1 as p

ROOT = Path(__file__).resolve().parent
SCHEMA = json.loads((ROOT / "WORLD_NEWS.schema.json").read_text(encoding="utf-8"))


def variant(title, summary, lang="en", *, approved=False, ai=False):
    status = "APPROVED" if approved else ("DRAFT" if ai else "INGESTED")
    provenance = {
        "kind": "AI_TRANSLATION_SUMMARY" if ai else "ORIGINAL_METADATA",
        "source_language": lang,
    }
    if approved:
        provenance.update({"approved_by": "SYNTHETIC_TEST_ACTOR", "approved_at": "2026-09-20T10:00:00Z"})
    return {"title": title, "summary": summary, "status": status, "provenance": provenance}


def raw(source_id, source_name, country, url, title, date, identity=None, cats=None, lang="en"):
    return {
        "source": {"id": source_id, "name": source_name, "kind": "test_or_public_source"},
        "source_url": url,
        "canonical_url": url,
        "content_identity": identity or {"kind": "canonical_url", "value": url},
        "source_country": country,
        "publication_date": date,
        "original_language": lang,
        "source_terminology": ["dyslexia"],
        "categories": cats or ["DYSLEXIA_LRS"],
        "original_title": title,
        "original_excerpt": None,
        "content": {
            lang: variant(title, "Source-provided public-safe synthetic summary.", lang),
            "de": variant("DE draft", "AI draft", lang, ai=True) if lang != "de" else variant(title, "Original", lang),
        },
        "provenance": {"discovery_method": "deterministic_html"},
        "version": 1,
    }


def public_world(record_id, source_id, source_name, country, url, title, date, *, identity=None, cats=None, lang="en", terms=None):
    return {
        "id": record_id,
        "record_type": "external_news",
        "zone": "PUBLIC",
        "audiences": ["PUBLIC"],
        "original_language": lang,
        "approval_status": "APPROVED",
        "publication_status": "PUBLISHED",
        "source": {"id": source_id, "name": source_name, "country": country},
        "source_url": url,
        "canonical_url": url,
        "content_identity": identity or {"kind": "canonical_url", "value": url},
        "source_country": country,
        "publication_date": date,
        "source_terminology": terms or ["dyslexia"],
        "categories": cats or ["DYSLEXIA_LRS"],
        "original_title": title,
        "provenance": {
            "discovery_method": "deterministic_html",
            "metadata_hash": "sha256:" + "0" * 64,
            "approved_by": "SYNTHETIC_TEST_ACTOR",
            "approved_at": "2026-09-20T10:00:00Z",
        },
        "content": {lang: variant(title, "Approved synthetic baseline summary.", lang, approved=True)},
    }


def non_news(record_id):
    return {
        "id": record_id,
        "record_type": "public_info",
        "zone": "PUBLIC",
        "approval_status": "APPROVED",
        "publication_status": "PUBLISHED",
        "title": f"Synthetic non-news {record_id}",
    }


NATURE = public_world(
    "worldnews_nature_synthetic",
    "nature_scientific_reports",
    "Scientific Reports / Nature",
    "IT",
    "https://www.nature.com/articles/synthetic-dyslexia-rhythm",
    "Synthetic rhythm study baseline",
    "2026-09-15",
    identity={"kind": "doi", "value": "10.1038/SYNTHETIC-DOI-001"},
    cats=["DYSLEXIA_LRS", "RESEARCH"],
)
AID = public_world(
    "worldnews_aid_synthetic",
    "aid_it",
    "Associazione Italiana Dislessia",
    "IT",
    "https://www.aiditalia.org/news/synthetic-public-test",
    "Synthetic AID baseline",
    "2026-09-07",
    cats=["DYSLEXIA_LRS", "DYSCALCULIA", "DYSGRAPHIA_WRITING", "DYSORTHOGRAPHY_SPELLING"],
    lang="it",
    terms=["DSA", "dislessia", "disgrafia", "disortografia", "discalculia"],
)
BVL = public_world(
    "worldnews_bvl_synthetic",
    "bvl_de",
    "Bundesverband Legasthenie und Dyskalkulie e.V.",
    "DE",
    "https://www.bvl-legasthenie.de/synthetic-aktionstag.html",
    "Synthetic Aktionstag baseline",
    "2026-09-30",
    cats=["DYSLEXIA_LRS", "DYSCALCULIA", "SCHOOL_ACCOMMODATIONS"],
    lang="de",
    terms=["Legasthenie", "Dyskalkulie"],
)
NON_NEWS = [non_news("public_info_1"), non_news("public_info_2"), non_news("public_info_3")]
ACCEPTED = {"schema_version": "1.0", "records": NON_NEWS + [NATURE, AID, BVL]}
STALE = {"schema_version": "1.0", "records": NON_NEWS + [NATURE]}


def fixture_candidates():
    d1 = raw(
        "nature_scientific_reports", "Scientific Reports / Nature", "IT",
        "https://www.nature.com/articles/synthetic-dyslexia-rhythm?utm_source=x",
        "Temporary title", "2026-09-15",
        {"kind": "doi", "value": "https://doi.org/10.1038/SYNTHETIC-DOI-001"},
        ["DYSLEXIA_LRS", "RESEARCH"],
    )
    d1["original_title"] = NATURE["original_title"]
    d1["source_country"] = NATURE["source_country"]
    d1["source"] = {"id": NATURE["source"]["id"], "name": NATURE["source"]["name"], "kind": "scientific_journal"}
    d1["source_terminology"] = NATURE["source_terminology"]
    d1["categories"] = NATURE["categories"]
    d1["original_language"] = NATURE["original_language"]

    d2 = raw(
        "aid_it", "Associazione Italiana Dislessia", "IT",
        "https://www.aiditalia.org/news/synthetic-public-test?utm_campaign=x",
        AID["original_title"], "2026-09-07", None,
        ["DYSLEXIA_LRS", "DYSCALCULIA", "DYSGRAPHIA_WRITING", "DYSORTHOGRAPHY_SPELLING"], "it",
    )
    d2["source"]["kind"] = "recognized_association"
    d2["source_terminology"] = AID["source_terminology"]

    d3 = raw(
        "bvl_de", "Bundesverband Legasthenie und Dyskalkulie e.V.", "DE",
        BVL["canonical_url"], "Synthetic Aktionstag updated title", "2026-09-30", None,
        ["DYSLEXIA_LRS", "DYSCALCULIA", "SCHOOL_ACCOMMODATIONS"], "de",
    )
    d3["source"]["kind"] = "recognized_association"
    d3["source_terminology"] = BVL["source_terminology"]

    d4 = raw(
        "portable_fixture", "Portable Public Test Fixture", "GB",
        "https://example.org/world-news-portable/new", "Portable new public item", "2026-09-21", None,
        ["DYSLEXIA_LRS", "RESEARCH"], "en",
    )
    d4["source"]["kind"] = "test_fixture"

    d5 = raw(
        "portable_fixture", "Portable Rejected Fixture", "GB",
        "http://example.org/world-news-portable/rejected", "Rejected fixture", "2026-09-21", None,
        ["DYSLEXIA_LRS"], "en",
    )
    d5["source"]["kind"] = "test_fixture"
    return [d1, d2, d3, d4, d5]


def process(candidates, prior_drafts=None):
    return p.process_weekly(
        accepted_baseline=ACCEPTED,
        stale_baseline=STALE,
        candidates=candidates,
        schema=SCHEMA,
        run_date="2026-09-21",
        run_timestamp="2026-09-21T12:00:00Z",
        search_window={"from": "2026-09-14", "to": "2026-09-21"},
        prior_drafts=prior_drafts,
        test_mode=True,
    )


def test_baseline_reconciliation_counts_and_non_news():
    b = process([])["baseline"]
    assert (b["accepted_record_count"], b["accepted_world_news_count"]) == (6, 3)
    assert (b["stale_record_count"], b["stale_world_news_count"]) == (4, 1)
    assert len(b["stale_missing_published_records"]) == 2
    assert b["non_world_news_semantically_identical"] is True


def test_dedup_order_identity_then_url_then_fallback():
    idx = p.DedupIndex(ACCEPTED["records"])
    c = dict(NATURE); c["canonical_url"] = "https://example.org/different"; c["source_url"] = c["canonical_url"]
    assert idx.match(c).rule == "DOI_OR_STABLE_ID"
    c = dict(AID); c["content_identity"] = {"kind": "canonical_url", "value": AID["canonical_url"]}; c["canonical_url"] += "?utm_source=test"
    assert idx.match(c).rule == "CANONICAL_URL"
    c = dict(AID); c.pop("canonical_url", None); c.pop("source_url", None); c.pop("content_identity", None)
    assert idx.match(c).rule == "SOURCE_NORMALIZED_TITLE_DATE"


def test_candidate_outputs_always_draft_and_ai_not_approved():
    c = p.prepare_candidate(fixture_candidates()[3], "2026-09-21T12:00:00Z")
    assert c["approval_status"] == "DRAFT" and c["publication_status"] == "UNPUBLISHED"
    assert c["content"]["de"]["status"] == "DRAFT"
    assert "approved_by" not in c["content"]["de"]["provenance"]
    assert p.validate_candidate(c, SCHEMA, test_mode=True) == []


def test_ai_actor_cannot_approve():
    issues = p.validate_approval({"candidate_id":"x","actor_type":"AI","approved_by":"AI","decision":"APPROVED","approved_at":"2026-09-21T12:00:00Z","language_decisions":{"en":"APPROVED"}})
    assert issues


def test_draft_excluded_without_human_approval_and_non_news_preserved():
    d = process([fixture_candidates()[3]])
    out, report = p.merge_approved(accepted_baseline=ACCEPTED, draft=d, approvals={"decisions": []})
    assert report["record_count"] == 6 and report["world_news_count"] == 3
    assert report["non_world_news_unchanged"] is True
    assert not p.validate_public_dataset(out)


def test_human_approved_fixture_can_enter_dry_run_public_export():
    d = process([fixture_candidates()[3]])
    c = d["candidate_records"][0]
    approval = {"candidate_id":c["id"],"actor_type":"HUMAN","approved_by":"PORTABLE_TEST_ACTOR","decision":"APPROVED","approved_at":"2026-09-21T12:10:00Z","language_decisions":{"en":"APPROVED","de":"REJECTED"}}
    out, report = p.merge_approved(accepted_baseline=ACCEPTED, draft=d, approvals={"decisions": [approval]})
    assert report["record_count"] == 7 and report["world_news_count"] == 4
    assert report["non_world_news_unchanged"] is True
    assert not p.validate_public_dataset(out)
    pub = next(r for r in out["records"] if r["id"] == c["id"])
    assert set(pub["content"]) == {"en"}


def test_prior_run_blocks_repeat_new_candidate():
    first = process([fixture_candidates()[3]])
    second = process([fixture_candidates()[3]], prior_drafts=[first])
    assert second["result_counts"]["NEW"] == 0
    assert second["result_counts"]["DUPLICATE_SKIPPED"] == 1
    assert second["candidate_records"] == []


def test_private_key_rejected():
    c = fixture_candidates()[3]
    c["student_name"] = "Should not be here"
    prepared = p.prepare_candidate(c, "2026-09-21T12:00:00Z")
    assert any("prohibited_key" in x for x in p.validate_candidate(prepared, SCHEMA, test_mode=True))


def test_full_dry_run_result_classification():
    d = process(fixture_candidates())
    assert d["result_counts"] == {"NEW":1,"DUPLICATE_SKIPPED":2,"UPDATED_EXISTING":1,"REJECTED":1}
    assert len(d["approval_queue"]) == 2
