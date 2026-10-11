# DSM-LRS Adapter release v2.5.1

Status: **metadata-only release / PUBLIC SAFE / FICTITIOUS ONLY**.

## Version model
- `adapter_core_version = 2.5`
- `release_version = 2.5.1`
- `behavior_change = NO`
- `pedagogical_rule_change = NO`
- `privacy_boundary_change = NO`
- `authority_change = NO`

Release v2.5.1 resolves D038 gate C12 by binding the unchanged Adapter core 2.5 to `ADAPTER_CONFORMANCE_MANIFEST_v1.0`, canonical D038, and the T106 source-state snapshot dated 2026-09-20.

## Core files
The files in `core/` are byte-identical copies of the verified v2.5 release artifacts. Their filenames retain `v2.5` intentionally because their semantic/behavioral core version remains 2.5:
- `LRS_ADAPTER_DSM_v2.5.md`
- `DSM_LRS_ADAPTER_PORTABLE_v2.5.md`
- `DSM_LRS_ADAPTER_GEMINI_v2.5.txt`
- `DSM_LRS_OPERATIONAL_MEASURE_REGISTER_TEMPLATE_v2.5.json`
- `DSM_LRS_ASSESSMENT_EQUIVALENCE_MATRIX_TEMPLATE_v2.5.md`

No v2.5 file is overwritten or silently patched.

## Traceability files
- `DSM_LRS_ADAPTER_RELEASE_METADATA_v2.5.1.json`
- `DSM_LRS_ADAPTER_v2.5.1_SOURCES.md`
- `DSM_LRS_ADAPTER_v2.5.1_CHANGELOG.md`
- `T107_RELEASE_MANIFEST_v0.1.json`
- `T107_CONFORMANCE_RESULTS_v0.1.json`
- `T107_ADAPTER_V2_5_1_RELEASE_TRACEABILITY_VERIFICATION_v0.1.md`

## C13 boundary
`official_source_freshness = REVIEW_REQUIRED_BEFORE_REAL_OPERATIONAL_USE`.
The 2026-09-20 source-state date is a traceability snapshot, not proof that the 2015 DSM guideline is the latest applicable official DSM/examination source.
