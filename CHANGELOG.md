# Changelog

All notable public/product changes to DSM-LRS are recorded here.

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
