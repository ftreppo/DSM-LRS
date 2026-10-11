# LRS News Worldwide — data and ingestion architecture

Status: design complete; not deployed. Zone: PUBLIC only.

## Separation and terminology
- External news is stored/rendered as `external_news`, never `OFFICIAL_DSM`, DSM guidance, or internal knowledge.
- The UI labels the module and every item as external; source, country, publication date, and original link remain visible.
- Preserve the source-country term verbatim (for example LRS, DSA, dyslexia, Legasthenie, Rechtschreibstörung, Rechenstörung, specific learning disorder). Category mapping aids discovery but never claims diagnostic or legal equivalence.
- No DSM, member, user, WhatsApp, or student data enters this pipeline.

## Record model
```json
{
  "schema_version": "1.0",
  "id": "worldnews_sha256-prefix",
  "record_type": "external_news",
  "source": {"id": "aid_it", "name": "Associazione Italiana Dislessia", "kind": "association"},
  "source_url": "https://example.org/article",
  "canonical_url": "https://example.org/article",
  "content_identity": {"kind": "canonical_url", "value": "https://example.org/article"},
  "source_country": "IT",
  "publication_date": "2026-09-07",
  "original_language": "it",
  "source_terminology": ["DSA", "dislessia"],
  "categories": ["DYSLEXIA_LRS", "SCHOOL_ACCOMMODATIONS"],
  "original_title": "Source title exactly as published",
  "original_excerpt": null,
  "content": {
    "it": {"title": "Source title exactly as published", "summary": null, "status": "INGESTED", "provenance": {"kind": "ORIGINAL_METADATA"}},
    "de": {"title": "...", "summary": "...", "status": "DRAFT", "provenance": {"kind": "AI_TRANSLATION_SUMMARY", "source_language": "it", "model": "...", "created_at": "..."}},
    "en": {"title": "...", "summary": "...", "status": "DRAFT", "provenance": {"kind": "AI_TRANSLATION_SUMMARY", "source_language": "it", "model": "...", "created_at": "..."}}
  },
  "provenance": {"discovery_method": "rss", "feed_url": "https://example.org/feed", "metadata_hash": "sha256:..."},
  "fetched_at": "2026-09-15T00:00:00Z",
  "approval_status": "DRAFT",
  "publication_status": "UNPUBLISHED",
  "version": 1
}
```

Enums:
- categories: `DYSLEXIA_LRS`, `DYSCALCULIA`, `DYSORTHOGRAPHY_SPELLING`, `DYSGRAPHIA_WRITING`, `ASSISTIVE_TECH_AI`, `RESEARCH`, `SCHOOL_ACCOMMODATIONS`, `POLICY_LEGISLATION`.
- approval: `DRAFT`, `APPROVED`, `REJECTED`.
- publication: `UNPUBLISHED`, `PUBLISHED`, `RETRACTED`.

An approved original-language variant may publish without translations. Each AI summary/translation requires its own ADMIN approval. Rendering falls back to the approved original and labels its language.

## Deterministic ingestion
1. Load enabled sources from the allowlisted registry.
2. Fetch RSS/Atom with conditional requests (`ETag`, `Last-Modified`); otherwise use a source-specific deterministic listing parser after terms/robots review.
3. Extract source-provided title, URL, date, language, country, and identifiers. Do not synthesize missing facts.
4. Canonicalize URL by resolving redirects and removing allowlisted tracking parameters; prefer DOI/publisher ID when present.
5. Deduplicate on content identity, then canonical URL, then source-scoped normalized title/date hash. Never use AI for deduplication.
6. Apply deterministic relevance rules and category hints. Non-matches are logged by reason code without AI use.
7. Create or update an `INGESTED`/`DRAFT`, `UNPUBLISHED` record. Only new relevant items may enter the optional AI queue.
8. AI returns schema-constrained category suggestions, 1–2 line summaries, and requested translations with provenance. It cannot approve or publish.
9. ADMIN reviews source link, terminology, categories, summaries, and each language variant. Publication export includes only approved content.
10. Generate a public-safe immutable JSON snapshot for the dashboard; keep internal fetch logs/checkpoints outside public assets.

## Runtime and state
- Provider-neutral scheduled serverless job, enabled only after confirming its free quota and Drive access model. Codex is not the runner.
- File state in Drive: source registry, feed checkpoints, item records, AI queue/results, validation report, and public snapshot; no database.
- One run at a time through a lease/checkpoint file; idempotent record IDs and optimistic versions make retries safe.
- Bounded frequency (initially daily), request timeouts, response-size limits, per-host rate limits, and no broad web crawling.
- Secrets belong in the selected platform secret store, never Drive or public output. Any Drive permission grant is a separate blocked action.

## Dashboard contract
- Home widget shows 4–6 newest published items: category, country/source, date, title, 1–2 line approved summary when available, and original link.
- Filters: All, Dyslexia, Dyscalculia, AI & Tools, Research. Other categories remain addressable in the full module.
- Sort by publication date, then fetched time; clearly mark original-language fallback.
- External-link treatment and visible disclaimer: external information, not DSM policy or guidance.

## Validation gates
- Allowlisted source and HTTPS canonical URL.
- Valid country, ISO date, original language, category, provenance, and stable identity.
- `record_type=external_news`; no `OFFICIAL_DSM`; no private identifiers or DSM/member fields.
- AI content cannot be `APPROVED` without ADMIN approval metadata.
- Public export requires `approval_status=APPROVED` and `publication_status=PUBLISHED`; unapproved translations are omitted.
