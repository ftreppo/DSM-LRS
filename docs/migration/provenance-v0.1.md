# DSM-LRS migration provenance v0.1

**Date:** 2026-10-11  
**Purpose:** preserve source/version provenance without exposing private Google Drive identifiers.

## Batch 1 — technical Source Library contracts

Previous project area: `01_WORKING / 09_SOURCE_LIBRARY / 00_REGISTRY`  
Public target: `specifications/source-library/`

Migrated:
- `SourceRecord.schema.json`
- `RuleRecord.schema.json`
- `SourceRuleMapping.schema.json`
- `ReleaseDependency.schema.json`
- `ObservationRecord.schema.json`

The actual reference corpus remains in the Google Drive Library.

## Batch 2 — Adapter v2.5 / release v2.5.1

Previous project area: `01_WORKING / 04_LRS_AI_ADAPTER`  
Public targets: `adapter/core/` and `adapter/releases/v2.5.1/`

Core migrated:
- `LRS_ADAPTER_DSM_v2.5.md`
- `DSM_LRS_ADAPTER_PORTABLE_v2.5.md`
- `DSM_LRS_ADAPTER_GEMINI_v2.5.txt`
- `DSM_LRS_OPERATIONAL_MEASURE_REGISTER_TEMPLATE_v2.5.json`
- `DSM_LRS_ASSESSMENT_EQUIVALENCE_MATRIX_TEMPLATE_v2.5.md`

Release documentation migrated:
- README
- CHANGELOG
- SOURCES
- T107 conformance results

The original release metadata and release manifest contain private storage identifiers; the public repository therefore contains sanitized derivatives rather than verbatim copies.

## Batch 3 — public pilot site

Previous project area: `01_WORKING / 05_DASHBOARD_PUBLIC`  
Public target: `site/`

Migrated:
- `index.html`
- `styles.css`
- `data.js`
- `app.js`
- `README.md`

The pilot remains synthetic/demo-only. GitHub Pages deployment is intentionally deferred to the later public-site phase.

## Provenance rule

Public repository files may identify the previous project area and version, but should not expose private Drive IDs or access URLs. Private item-level Drive provenance remains in the private migration audit.


## Batch 4 — Parent Prompt QUICK v0.2

Previous project area: `01_WORKING / 04_LRS_AI_ADAPTER`  
Public target: `resources/parent-prompt/v0.2/`

Migrated:
- multilingual source
- German version
- Italian version
- English version
- public README

This is the generic/non-personalized parent resource. Personalized prompts remain outside the public repository.

## Batch 5 — World News pipeline

Previous project areas: `01_WORKING / 90_CODEX` and `03_DASHBOARD_DATA`  
Public target: `pipelines/world-news/`

Migrated:
- architecture
- JSON schema
- candidate public-source allowlist
- deterministic weekly pipeline
- migration-boundary README

Not migrated yet: the current test script, because it depends on hard-coded local fixture paths and fixture files not yet present in the public repository. Operational drafts, approval queues and accepted-publication snapshots remain Drive state.

## Batch 6 — protected-core generic contracts

Previous project area: `01_WORKING / 06_OPERATIONAL_PROFILES_PRIVAT`  
Public target: `specifications/protected-core/`

Migrated:
- frozen MVP0 data contract
- current system-evolution specification v0.7
- generic AI ingestion template
- boundary README

Only generic contracts/specifications moved. Personalized/operational records remain in protected Drive storage.
