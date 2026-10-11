# Auth MVP v0.3-public.1 — verification

**Date:** 2026-10-11  
**Task:** DL-21B  
**Result:** **PASS FOR PUBLIC SOURCE / LOCAL SYNTHETIC TESTING**

## Derivative boundary

Prepared from the tested Drive artifact DSM-LRS Auth MVP v0.3.

Publication/runtime hardening only:
- explicit demo-mode gate;
- externally supplied session secret;
- configurable demo password;
- no password prefill;
- generated SQLite state excluded;
- repository ignore rules;
- Uvicorn factory startup bound to loopback by the supplied demo scripts.

The authorization and versioning modules were compared against the v0.3 source and remained unchanged.

## Verification

Pre-publication workspace:
- Python compile: PASS
- regression suite: **16/16 PASS**
- fail-closed startup without session secret: PASS
- fresh empty-database demo startup with explicit configuration: PASS
- configured demo login: PASS
- generated runtime-state exclusion: PASS
- private-key/API-key/Drive-link scan: PASS
- non-example email scan: PASS

Post-publication GitHub read-back:
- all public-source files fetched from GitHub;
- blob identities match the verified local derivative, with only non-semantic transfer differences documented (final newline / removed test comment);
- no generated database was intentionally committed.

## Scope

This PASS means **public-source and local synthetic-demo suitability only**.

It does not authorize:
- real identities;
- real student/member data;
- protected deployment;
- production authentication;
- operational school use.
