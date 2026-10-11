# Private traceability boundary

Two original machine-readable v2.5.1 files contain internal Google Drive identifiers:

- `DSM_LRS_ADAPTER_RELEASE_METADATA_v2.5.1.json`
- `T107_RELEASE_MANIFEST_v0.1.json`

They are not copied verbatim to this public repository. Sanitized public derivatives are provided as:

- `release-metadata.public.json`
- `release-manifest.public.json`

`T107_CONFORMANCE_RESULTS_v0.1.json` does not contain those private storage identifiers and is published with its full conformance content.

Public migration rule:
- publish product semantics and non-sensitive release documentation;
- keep private storage identifiers in private migration/audit evidence;
- replace private locators with public repository references when public traceability is needed.
