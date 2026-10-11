# DSM-LRS — Drive migration inventory & classification v0.1

**Date:** 2026-10-11  
**Status:** Phase 1 complete — Gate G1 PASS  
**Scope:** migration-relevant content in the existing DSM-LRS Google Drive project. Protected content is classified but not copied or exposed here.

## Classification vocabulary

- **PRODUCT** — versioned software, specifications, schemas, tests, public documentation or site source. Target: GitHub.
- **LIBRARY-GENERAL** — source/reference documents and learning/LRS guidance. Target: Google Drive Library.
- **LIBRARY-PROTECTED** — personalized, correspondence, profiles or other protected material. Target: protected Google Drive Library.
- **OPERATIONAL-STATE** — internal task/project/review state. Remains private unless a deliberately sanitized public projection is created.
- **LEGACY** — superseded versions, backup bundles, temp material or historical releases not needed as current source.

## Area map

| Existing Drive area | Classification | Canonical target | Migration rule |
|---|---|---|---|
| Root `00_START_HERE`, current project protocol | OPERATIONAL-STATE | Private project coordination | Keep as migration provenance; do not publish raw private links |
| Root old protocol + `Backup/` | LEGACY | Drive archive | Do not migrate as current product |
| `01_DSM_DOKUMENTE` | LIBRARY-GENERAL | Google Drive Library | DSM guidelines, regulations, presentations and reference PDFs remain in Drive |
| `02_WHATSAPP_INBOX_PRIVAT` | LIBRARY-PROTECTED | Protected Drive | Never publish; correspondence ingestion stays private |
| `03_DASHBOARD_DATA` | MIXED | GitHub + Drive | Static public schemas/rules/config may move to GitHub; weekly drafts/queues/publication state remain operational data |
| `04_LRS_AI_ADAPTER` | MIXED | GitHub + Drive archive | Current DSM Adapter source/spec/tests move to DSM-LRS first; older releases/test packs become legacy; generic extraction is deferred until G5 |
| `05_DASHBOARD_PUBLIC` | PRODUCT | GitHub / GitHub Pages | Pilot public site source moves to the repository |
| `06_OPERATIONAL_PROFILES_PRIVAT` | MIXED | GitHub + protected Drive | Generic contracts/templates/synthetic fixtures may move after scan; real operational profiles always remain protected |
| `07_AUTH_MVP` | PRODUCT-CANDIDATE | GitHub after security scan | Move code/specs only after secret/privacy scan; deployment evidence can remain archived |
| `08_EXTERNAL_REVIEW` | OPERATIONAL-STATE / PROTECTED | Drive | External review material remains private by default; only deliberately public demo assets may be copied after review |
| `09_SOURCE_LIBRARY` | MIXED | GitHub + Drive Library | Technical registries, schemas, tests and under-the-hood prototype are PRODUCT; actual reference corpus remains Drive Library |
| `90_CODEX` | MIXED | GitHub + private state + archive | Code/spec/tests move selectively; TASKS/PROJECT_STATE/DECISIONS remain private state unless sanitized; temp/archive remain legacy |

## Pilot public page — verified implementation

The existing pilot public surface is a dependency-free static site built from:

- `index.html`
- `styles.css`
- `data.js`
- `app.js`
- README

Verification on 2026-10-11 found:

- synthetic/demo data only;
- no Google Drive fetch;
- no authentication;
- no tracker or analytics script;
- no external font;
- no cookie;
- no secret;
- no private Drive link in the preview source;
- DE / IT / EN user interface;
- accessibility features including skip link, focus styles and reduced-motion handling.

This source is the seed for the official DSM-LRS GitHub Pages surface; it should be evolved rather than replaced by a second unrelated website.

## Adapter boundary

For Phase 2, the **current DSM-specific Adapter stays inside `DSM-LRS`** as product material.

Do not create `lrs-adapter` yet. The generic Adapter becomes a separate repository only after:

1. a standalone input/output/configuration contract exists;
2. all DSM-specific dependencies are isolated behind explicit configuration/interfaces;
3. a clean synthetic test runs without DSM-LRS project state, MindMap, Notion or private Drive access.

## Canonical-home decisions

1. **Software/specifications/tests/public site → GitHub.**
2. **General LRS/DSM learning/reference documents → Google Drive Library.**
3. **Personalized/protected documents and correspondence → protected Drive.**
4. **Internal operational state → private coordination surface, not public by default.**
5. **Historical bundles/backups → legacy archive, not competing canon.**
6. **Technical Source-Library machinery → GitHub; actual Library corpus → Drive.**

## Gate G1 result

**PASS.**

All migration-critical areas now have a destination class. Areas marked MIXED have explicit item-level rules, and protected/operational content is excluded from automatic public migration.

## Next

**DL-20 — create the initial public repository structure**, then migrate only the first bounded PRODUCT batch with read-back verification.
