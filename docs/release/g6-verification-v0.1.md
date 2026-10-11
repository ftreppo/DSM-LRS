# G6 release verification — architecture baseline v0.1

**Date:** 2026-10-12  
**Target baseline:** `0.1.0-alpha.1`

## DL-60 — Cross-repository architecture check

**PASS**

Canonical ownership:

| Domain | Canonical home |
|---|---|
| DSM-LRS product, DSM integration, public site, Auth MVP, World News | `ftreppo/DSM-LRS` |
| Generic LRS Adapter, generic contract, PolicyPack, generic Community Adapter Lab | `ftreppo/lrs-adapter` |
| LRS/DSA/DSM reference documents and protected/personalized material | Google Drive Library |
| Cross-project coordination | MindMap / REGIA only |

Dependency direction:

`DSM-LRS → lrs-adapter`

The reverse dependency is prohibited and the standalone Adapter scan reports zero forbidden DSM-LRS/MindMap/Notion/Drive runtime dependencies.

Former generic copies in DSM-LRS are explicitly marked NON-CANONICAL / extraction evidence.

## DL-61 — Privacy / publication scan

**PASS for current public trees**

Checked both public repositories for:
- Google Drive direct URLs;
- Gmail addresses;
- GitHub-token patterns;
- Google API-key patterns;
- private-key material;
- exposed real email addresses in reviewed key surfaces.

Findings:
- no GitHub token pattern;
- no Google API key;
- no Gmail address;
- no private key;
- no private Drive URL in canonical product surfaces;
- DSM-LRS contains `@example.invalid` only in the explicitly synthetic Auth MVP seed;
- occurrences of `drive.google.com` / `BEGIN PRIVATE KEY` in DSM-LRS search results are defensive test/scan strings, not credentials or links to private material.

Public site remains static and contains no protected Library access.

## DL-62 — Fresh-user public test

**PASS**

- GitHub Pages deployed successfully;
- live site: https://ftreppo.github.io/DSM-LRS/;
- signed-out/private-browser access verified by user;
- Home, User Manual, Help, Community and DE/IT/EN language switching verified.

## DL-63 — Fresh-developer test

**PASS**

### lrs-adapter

Standalone GitHub Actions:
- workflow: `Standalone conformance`;
- run #1;
- result: SUCCESS;
- fresh checkout;
- test dependency install;
- standalone tests PASS;
- forbidden dependency scan PASS.

### DSM-LRS

GitHub Actions:
- workflow: `DSM-LRS public verification`;
- run #1;
- result: SUCCESS;
- Auth MVP: **16 passed**;
- World News: **9 passed**;
- Library provider contract: **6 passed**;
- canonical Adapter consumer pointer: PASS.

Total DSM-LRS regression checks in the public CI run: **31 passed**.

## DL-64 — Library integration/failure test

**PASS at contract boundary**

The provider-neutral Library contract verifies:
- AVAILABLE positive case;
- missing root → UNAVAILABLE;
- missing source → NOT_FOUND;
- permission failure → ACCESS_DENIED;
- non-authority workflow may continue without source;
- authority-required UNVERIFIED source fails closed.

Result in public CI: **6 passed**.

No provider error silently substitutes a different authority/source class.

## DL-65 — Canonical-source conflict audit

**PASS — zero unresolved active canon conflicts**

Resolved:
- generic Adapter canonical in `ftreppo/lrs-adapter`;
- DSM-LRS pins `0.1.0-alpha.1` through `integrations/lrs-adapter/consumer.json`;
- DSM-LRS generic-prototype/spec/test copies marked archive/reference/non-canonical;
- generic Community Adapter Lab canonical in `lrs-adapter`;
- DSM-LRS Community submission path retained only for DSM-specific cases/integrations;
- Drive product copies are archive/provenance; Drive remains canonical for Library/protected/operational material.

## Known limitation not hidden by this baseline

Adapter C13 remains **REVIEW**:
the project has not yet proven that the registered DSM guideline from 2015 is the latest/current official DSM source.

Therefore this architecture baseline must **not** be described as proof of compliance with current official DSM rules.

## G6 decision

**G6 PASS for an architecture/public-project baseline**, with C13 recorded as an explicit source-freshness limitation.

DL-66 may tag the first public architecture baseline.
