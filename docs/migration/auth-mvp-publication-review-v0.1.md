# Auth MVP v0.3 — public-code security review v0.1

**Date:** 2026-10-11  
**Task:** DL-21A  
**Result:** **REVIEW / HOLD BEFORE PUBLIC SOURCE MIGRATION**

## Reviewed artifact

DSM-LRS Auth MVP v0.3.

Declared upstream status: **TESTED · FICTITIOUS DATA ONLY · NOT DEPLOYED**.

## Verification performed

- package extracted and source tree inspected;
- scan for real credentials, private keys, API keys, Google Drive URLs, personal email addresses and project hostnames;
- local automated test suite executed;
- result: **16/16 tests PASS**.

## Positive findings

- no real Google Drive access is embedded;
- no real API key/private key was found;
- synthetic identities/data are visibly marked as demo/test;
- generated contact addresses use the non-real `example.invalid` domain;
- run scripts bind to `127.0.0.1`;
- the package includes CSRF handling, signed session middleware and password hashing;
- the health endpoint is explicitly fictitious-data-only.

## Publication blockers / hardening required

### 1. Development secret fallback

The application currently falls back to:

`DEV-ONLY-CHANGE-ME`

when `DSM_LRS_SECRET_KEY` is absent.

For a public repository, the reusable source should fail closed outside an explicit development mode rather than silently accept a known fallback secret.

### 2. Shared demo password

The synthetic prototype intentionally seeds a shared password `demo` and pre-fills it in the demo login UI.

This is acceptable for a local fixture, but it must be unmistakably separated from any deployable configuration.

### 3. Seed SQLite database

The ZIP contains a generated `data/dsm_lrs_demo.sqlite3` database.

The public repository should not version the generated database. Synthetic data should be created deterministically from source/fixtures during local setup or tests.

### 4. Public repository guardrails

Before source migration, add:
- explicit EXPERIMENTAL / LOCAL DEMO / NOT FOR PRODUCTION notice;
- `.gitignore` for `.env`, SQLite databases and runtime files;
- explicit secure configuration requirements;
- repository-relative test/setup flow.

## Gate decision

**Do not migrate the Auth MVP source verbatim yet.**

The source may become public after a bounded publication-hardening patch that preserves authorization behavior while removing deployment footguns and generated runtime state.

## Next

**DL-21B — prepare a public-safe Auth MVP derivative**, then run:
1. security pattern scan;
2. 16-test regression suite;
3. fresh-clone/local-start smoke test;
4. read-back from GitHub.

The original Drive ZIP remains immutable migration evidence.
