# Versioning and change discipline

DSM-LRS uses a lightweight Semantic Versioning convention for the public/product repository.

## Version format

`MAJOR.MINOR.PATCH[-PRERELEASE]`

During migration/bootstrap, prerelease versions such as `0.1.0-alpha.1` are expected.

- **MAJOR** — incompatible public contract/product changes after 1.0.
- **MINOR** — backward-compatible product capabilities or public contracts.
- **PATCH** — backward-compatible fixes, metadata corrections or test/documentation changes.
- **PRERELEASE** — architecture/migration baselines not yet declared operational release.

## Canonical version markers

- `VERSION` — current repository baseline version.
- `CHANGELOG.md` — human-readable public change history.
- Git commits — immutable implementation/change evidence.
- future GitHub tags/releases — release markers once the publication workflow is enabled.

## Change rule

Every material product change should have:
1. a Git commit;
2. a changelog entry in the next baseline/release;
3. tests or verification evidence where applicable;
4. an explicit note if the change affects privacy, authority, source freshness or operational-release gates.

Operational Drive state and Library-document updates do not require a software version bump unless they change a public/product contract.

## Current baseline

`0.1.0-alpha.1` — GitHub migration/product-canon baseline dated 2026-10-11.

Example trace:
- World News test portability: commit `db00b9f14aa38ab0f95ead788bb7cd1c3107d082`
- included in `0.1.0-alpha.1`
- verification: 9/9 portable synthetic tests PASS.

This proves the minimal commit → verification → version trace required by DL-24.
