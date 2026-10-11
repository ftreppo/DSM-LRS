# DSM-LRS Library source governance v0.1

## Canonical split

- **GitHub:** product/code/specifications/tests/public documentation/site source.
- **Google Drive Library:** source/reference documents and protected/personalized material.
- **Operational state:** separate from both product canon and Library authority.

## Source record

A Library source should carry, where applicable:
- stable project source ID;
- title / author or organization;
- source class;
- publication/version date;
- original locator in private provider configuration;
- verification date;
- authority/evidence status;
- supersession status;
- copyright/storage note.

Technical source-record schemas are versioned on GitHub; the document bytes/corpus remain in Drive when that is their canonical home.

## Updates

A Library document can be added, replaced or re-verified without requiring a DSM-LRS software release **unless** the change modifies:
- a public data contract;
- a rule interpretation encoded in product behavior;
- an Adapter contract;
- authority/privacy semantics.

If one of those changes, update the corresponding GitHub specification/code and changelog.

## Source freshness

A document being present in the Library does not prove that it is current.

Use explicit states such as:
- CURRENT / verified;
- REFERENCE_ONLY;
- SUPERSEDED;
- REVIEW_REQUIRED / UNVERIFIED.

For the registered DSM 2015 guideline, C13 is now **UPDATE_REQUIRED / MANUAL DSM VERSION CHECK**. Current official BLASchA/KMK sources include materially newer 2024/2025 revisions. The 2015 DSM document may remain a DSM-local working source, but it cannot by itself establish current authority freshness. See `docs/authority/c13-source-freshness-2026-10-12.md`.

## Protected material

Protected/personalized material:
- is never published merely because a public schema/template exists;
- is accessed only within an authorized workflow;
- does not become less protected when a synthetic public example exists.

## Failure handling

Provider errors and missing sources must preserve the resolution state defined in the Library Provider Contract. No silent authority substitution is allowed.
