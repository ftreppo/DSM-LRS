# DSM-LRS migration residuals v0.1

**Date:** 2026-10-11  
**Status:** DL-21 remains in progress.

## Open product candidates

### World News tests
The existing test script is not portable yet because it uses hard-coded `/mnt/data` fixture paths and expects fixture files that are not in the repository.

**Required before migration:** package synthetic/public fixtures and change the test to repository-relative paths.

### Auth MVP / protected pilot
DL-21A security/publication review is complete: **REVIEW / HOLD BEFORE PUBLIC SOURCE MIGRATION**. The v0.3 package still passes 16/16 tests and contains no real credentials, but it includes a known development secret fallback, a shared demo password, and a generated SQLite demo database.

**Required before migration:** DL-21B publication hardening — fail-closed secret configuration, explicit local-demo boundary, generated DB exclusion, repository guardrails, then regression + fresh-start verification. No live protected deployment is implied.

### 90_CODEX
This area mixes current product code/specifications with task state, decisions, evidence, experiments and history.

**Rule:** migrate current reusable product code/specifications selectively; keep `TASKS.md`, `PROJECT_STATE.md`, `DECISIONS.md`, checkpoints and private operational evidence outside the public repository unless deliberately sanitized.

### Dashboard derived data
Some structured DSM-rule/source files are candidates for versioned product data, but the current 2015 DSM guideline freshness gate remains unresolved.

**Rule:** do not present derived 2015 rule data as current official policy until the C13 freshness review is completed.

### Legacy Adapter releases
v2.2–v2.5 historical packages remain Drive evidence.

**Decision pending:** whether to expose them as GitHub release history or retain only v2.5.1/current public baseline.

### External review material
Reviewer workspaces and feedback stay private by default. Only deliberately approved public demo/review artifacts may move.

## Non-product content that remains on Drive

- general LRS/dyslexia reference documents;
- DSM source/reference documents;
- personalized/protected material;
- correspondence;
- operational drafts/approval queues/publication snapshots;
- private migration evidence.

## Next bounded task

**DL-21B — prepare a public-safe Auth MVP derivative** without changing the authorization contract; then rerun security scan, regression tests and local-start verification.
