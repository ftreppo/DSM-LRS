# World News pipeline

Current public/product baseline for the DSM-LRS `LRS News Worldwide` flow.

Included:
- architecture
- JSON schema
- candidate public-source allowlist
- deterministic staging/dedup/export pipeline
- repository-portable synthetic regression tests

## Test portability

The original project test depended on hard-coded `/mnt/data` paths and historical snapshot fixtures.

The public test `test_world_news_weekly_pipeline_v0_1.py` now:
- uses repository-relative schema loading;
- constructs synthetic accepted/stale baselines in the test itself;
- preserves DOI → canonical URL → source/title/date dedup ordering;
- verifies DRAFT-first behavior and human/admin approval boundary;
- verifies private-key rejection and prior-run deduplication;
- requires no private Drive content or historical publication snapshot.

Verification: **9/9 tests PASS**. The GitHub blob read-back matches the verified local test artifact exactly.

Operational drafts, approval queues and accepted publication snapshots remain on Google Drive; they are runtime/content state, not source code.
