# Changelog

All notable public/product changes to DSM-LRS are recorded here.

## Unreleased

### Standalone lrs-adapter extraction complete
- created public `ftreppo/lrs-adapter` repository with Apache-2.0;
- migrated generic Adapter instruction, contract, PolicyPack schema, synthetic fixture and tests;
- installed independent standalone CI;
- standalone CI run #1: **SUCCESS**;
- forbidden-dependency scan: PASS;
- DSM-LRS now pins `lrs-adapter 0.1.0-alpha.1` through `integrations/lrs-adapter/`;
- former generic prototype copies in DSM-LRS are provenance-only and non-canonical;
- generic Community Adapter Lab moved to `lrs-adapter`.

### Community Adapter Lab
- added structured public GitHub Issue Form for anonymized Adapter examples;
- added mandatory privacy/sharing-rights gate and contributor permission;
- added Community Adapter Lab review model and maintainer checklist;
- added reviewed-example staging under `examples/community/reviewed/`;
- added Adapter Improvement Register;
- added public Community Adapter Example JSON Schema;
- added multilingual public-site CTA for submissions;
- raw issues remain non-canonical until review/promotion;
- public Community pages now follow **German → Italian → English**; maintainer/configuration artifacts may remain English-only.


### Public site
- converted the static pilot into the official public project landing-page source;
- added DE / IT / EN Welcome and architecture explanation;
- added multilingual User Manual;
- added multilingual Help & troubleshooting;
- added privacy and authority/source-freshness boundaries;
- added GitHub Pages workflow publishing only `site/`;
- completed static syntax/i18n/privacy scans.

**GitHub Pages:** deployed successfully and verified signed-out; DL-35 / G3 PASS.

### Generic Adapter extraction
- classified Adapter components into GENERIC vs DSM-SPECIFIC;
- defined the standalone generic Adapter contract and provider-neutral PolicyPack;
- added generic portable prototype and synthetic PolicyPack fixture;
- dependency audit: zero mandatory DSM-LRS/MindMap/Notion/Drive dependencies;
- standalone contract/conformance checks: **8/8 PASS**;
- Gate G5 PASS: separate `lrs-adapter` repository may now be created.

### Library architecture
- formalized the Google Drive Library taxonomy without moving existing folders;
- added provider-neutral Library contract and configuration schema;
- added Google Drive and local provider examples with no private locator values;
- added Library source-governance rules;
- added fail-closed Library reference tests: **6/6 PASS**.

Versioning follows the project convention in [docs/versioning.md](docs/versioning.md).

## 0.1.0-alpha.1 — 2026-10-11

**Architecture migration baseline.**

### Added
- public DSM-LRS repository architecture and migration roadmap;
- technical Source Library schemas;
- DSM-specific Adapter core v2.5 and public-safe v2.5.1 traceability;
- static public pilot source under `site/`;
- Parent Prompt QUICK v0.2 in DE / IT / EN;
- World News architecture, schema, source allowlist, deterministic pipeline and portable synthetic regression tests;
- generic protected-core specifications;
- Auth MVP `v0.3-public.1` for public source review and local fictitious testing.

### Verification
- Auth MVP public-safe derivative: 16/16 regression tests PASS plus fail-closed and fresh-start checks.
- World News portable suite: 9/9 PASS.
- GitHub read-back performed on migrated batches.
- Google Drive `00_START_HERE` now declares GitHub canonical for product/code/specifications while Drive remains canonical for the document/protected Library.

### Trace example
The World News test portability change is represented by commit `db00b9f14aa38ab0f95ead788bb7cd1c3107d082` and is included in this `0.1.0-alpha.1` baseline.

### Known gates
- Adapter C13 source-freshness remains REVIEW before any current-official-DSM-rule compliance claim.
- GitHub Pages deployment/public no-account verification is not yet complete.
- Real identities, real protected data and protected deployment remain outside this baseline.
