# DSM-LRS Library Provider Contract v0.1

## Purpose

DSM-LRS keeps the **product** independent from the storage location of its knowledge/document Library.

The product asks for a logical Library class or source identifier. A provider implementation resolves that request. The current operational provider is Google Drive, but the public product contract must not require Google Drive paths or private folder IDs.

## Logical Library classes

| Logical class | Meaning | Current operational home |
|---|---|---|
| `GENERAL_DSM` | DSM documents, regulations, presentations and DSM-specific reference material | Google Drive Library |
| `GENERAL_LRS` | General LRS/DSA guidance, learning guidelines and source corpus | Google Drive Library |
| `PROTECTED_PERSONALIZED` | Authorized personalized/protected documents and operational profiles | Protected Google Drive area |

The following are **not** Library classes:
- intake/inbox content before review;
- TASKS / PROJECT_STATE / DECISIONS;
- approval queues and publication snapshots;
- source-code schemas/tests already canonical on GitHub.

## Configuration boundary

A consumer uses logical root names. Provider-specific locators live in configuration outside the public source tree.

Example consumer request:

`GENERAL_LRS / source:reading-accessibility-guideline`

The consumer must not need to know whether the provider is:
- Google Drive;
- a local folder;
- another future provider.

See `LibraryProviderConfig.schema.json`.

## Resolution states

Every lookup returns one explicit state:

- `AVAILABLE`
- `NOT_FOUND`
- `ACCESS_DENIED`
- `UNAVAILABLE`
- `UNVERIFIED`

A non-AVAILABLE state never silently resolves to another authority/source class.

## Fail-closed rules

1. Missing or inaccessible protected content must not be replaced by a public/general document as if it were the personalized authority.
2. Missing DSM authority material must not be replaced by general LRS guidance as if it were DSM policy.
3. `UNVERIFIED` source freshness must remain visible and non-authorizing.
4. Public pages and public tools must continue to function without protected-Library access when their workflow does not require it.
5. Errors must not expose private locator values, file IDs or access tokens.

## Portability rule

Changing the provider changes configuration, not the consumer contract.

The current Google Drive implementation is therefore an **operational provider**, not a mandatory dependency of DSM-LRS or of the future standalone LRS Adapter.
