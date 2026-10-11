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

For the currently registered DSM 2015 guideline, source freshness remains REVIEW before claims of current official DSM-rule compliance.

## Protected material

Protected/personalized material:
- is never published merely because a public schema/template exists;
- is accessed only within an authorized workflow;
- does not become less protected when a synthetic public example exists.

## Failure handling

Provider errors and missing sources must preserve the resolution state defined in the Library Provider Contract. No silent authority substitution is allowed.
