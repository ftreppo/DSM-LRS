# DSM-LRS migration residuals v0.1

**Date:** 2026-10-11  
**Status:** Phase 2 closed — these items are explicit holds, private state, or historical evidence and do not compete with the GitHub product canon.

## Completed migration items

### World News tests
✅ Repository-portable synthetic test suite is now in `pipelines/world-news/test_world_news_weekly_pipeline_v0_1.py`.

- no `/mnt/data` dependency;
- no private/historical Drive fixtures required;
- repository-relative schema loading;
- **9/9 PASS**;
- GitHub blob read-back exactly matches the verified local artifact.

### Auth MVP / protected pilot
✅ DL-21A review and DL-21B publication hardening are complete.

Public-safe derivative:
`auth-mvp/v0.3-public.1/`

Verification:
- **16/16 regression tests PASS**;
- fail-closed configuration check PASS;
- fresh empty-database demo startup PASS;
- local configured login PASS;
- generated runtime database excluded;
- public contamination scan PASS.

This remains **LOCAL DEMO / FICTITIOUS DATA ONLY / NOT FOR PRODUCTION**.

## Explicit non-migration / hold classes

### 90_CODEX
This area mixes project state, decisions, verification evidence, experiments and historical work.

**Decision:** no bulk migration. Current reusable product code/specifications were migrated selectively. `TASKS.md`, `PROJECT_STATE.md`, `DECISIONS.md`, checkpoints and private evidence remain operational/private state, not public product canon.

### Dashboard derived DSM-rule/source data
Some structured rule/source data is technically versionable, but C13 source freshness remains unresolved.

**Decision:** HOLD. Do not publish it as current official DSM policy until the source-freshness review passes.

### Legacy Adapter releases
v2.2–v2.5 historical release packages remain Drive evidence.

**Decision:** retain as historical evidence for now. The current public baseline is Adapter core v2.5 with release metadata/traceability v2.5.1. Historical packages do not compete with the current GitHub canon.

### External review material
Reviewer workspaces, feedback and review correspondence remain private by default.

**Decision:** not product canon. Only a deliberately approved public review/demo artifact may be copied later.

## Content that remains canonically on Google Drive

- general LRS/dyslexia reference documents;
- DSM source/reference documents;
- learning guidelines and source corpus;
- personalized/protected documents;
- correspondence;
- operational drafts, approval queues and publication snapshots;
- private migration and review evidence.

## Canonical-source status

Google Drive `00_START_HERE` records that:
- GitHub is canonical for code/specifications/tests/product documentation/site source;
- Drive remains canonical for Library/protected/operational content;
- old Drive product copies are provenance/archive evidence;
- no historical file was deleted.

## Next

**DL-30 — GitHub Pages preparation/deployment for the existing migrated pilot source.**
