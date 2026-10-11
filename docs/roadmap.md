# DSM-LRS — GitHub / Drive Separation Roadmap v0.1

**Status:** ACTIVE — Phase 2 complete; Gate G2 PASS  
**Date:** 2026-10-11  
**Owner:** DSM-LRS project  
**Coordination:** MindMap / REGIA only; MindMap does not own or execute the DSM-LRS product.  
**Current source:** DSM-LRS project and pilot public surface on Google Drive.  
**Target:** DSM-LRS remains independently distributable; GitHub becomes the public/versioned product surface, Google Drive remains the Library, and the generic LRS Adapter is extracted only after its standalone contract is verified.

## Architectural target

```text
MindMap / REGIA
    |
    | coordinates / tracks
    v
DSM-LRS  ----------------------> Google Drive Library
public GitHub repo                - general dyslexia/LRS sources
- project documentation           - learning guidelines
- public product/code             - DSM reference material
- GitHub Pages                    - personalized/protected material
- DSM integration
    |
    | optional dependency after extraction
    v
LRS Adapter
independent public repo
- generic adapter engine
- generic contracts
- tests/examples
- no dependency on DSM-LRS, MindMap, Notion or Franco's infrastructure
```

## Canonical-source rule

- **DSM-LRS GitHub:** public product, code, public specifications, tests, public documentation, website/GitHub Pages and release history.
- **Google Drive Library:** source/reference documents used by DSM-LRS, including general dyslexia/LRS material, learning guidelines and protected/personalized documents.
- **LRS Adapter GitHub (future):** generic reusable adapter only, after extraction gate passes.
- **MindMap:** coordination, roadmap visibility and cross-project dependencies only. It must never become a runtime dependency of DSM-LRS or LRS Adapter.

No file should have two competing canonical homes.

---

# Phase 0 — Bootstrap the public destination

| ID | Task | Result | Verification / gate | Depends on |
|---|---|---|---|---|
| DL-00 | ✅ Freeze a baseline of the current DSM-LRS structure | Existing Drive project, pilot page, key contracts and current state are identified before migration | Baseline list can be reproduced from Drive; no content has been moved/deleted | — |
| DL-01 | ✅ **Create public GitHub repository `DSM-LRS`** | Public destination exists under the selected GitHub account | Repository opens in an unauthenticated browser; default branch exists | DL-00 |
| DL-02 | ✅ Set minimal repository governance | README, visibility statement, contribution posture and explicit license decision placeholder | README explains scope; no sensitive/student material present; license status is explicit (selected or pending) | DL-01 |
| DL-03 | ✅ Promote this roadmap into `DSM-LRS` | Project roadmap becomes canonical in the DSM-LRS repository | Roadmap in DSM-LRS matches the MindMap staging version; MindMap changes to reference/link role | DL-01, DL-02 |
| DL-04 | ✅ Register DSM-LRS as external coordinated workstream in MindMap | REGIA can see current phase, blockers and next task without owning the product | MindMap entry explicitly says external/independent; repo link recorded | DL-03 |

**Gate G0 — Public destination ready: ✅ PASS.** DL-00–DL-04 completed; product migration still waits for Phase 1 classification.

---

# Phase 1 — Inventory and classify the existing DSM-LRS

| ID | Task | Result | Verification / gate | Depends on |
|---|---|---|---|---|
| DL-10 | ✅ Inventory current Drive project | File/folder inventory of DSM-LRS including pilot public surface, Adapter, contracts, tasks/state and reference material | Every relevant item has an ID/path and current role | G0 |
| DL-11 | ✅ Classify each item | Each item marked **PRODUCT / LIBRARY-GENERAL / LIBRARY-PROTECTED / OPERATIONAL-STATE / LEGACY** | No unclassified item on the migration critical path | DL-10 |
| DL-12 | ✅ Identify the existing pilot-page implementation | Source files/configuration for the pilot public page are located and understood | Can state exactly what must move to GitHub Pages and what stays in Drive | DL-10 |
| DL-13 | ✅ Define canonical-home map | One destination per information type | Conflict check finds no file intended to remain canonical in both Drive and GitHub | DL-11, DL-12 |

**Gate G1 — Classification complete: ✅ PASS.** Migration-critical areas are classified; protected/operational material is excluded from automatic publication.

---

# Phase 2 — Bootstrap DSM-LRS on GitHub

| ID | Task | Result | Verification / gate | Depends on |
|---|---|---|---|---|
| DL-20 | ✅ Create repository structure | Minimal folders for docs, specifications, tests/examples, site and DSM integration | Repository tree matches agreed architecture and contains no private data | G1 |
| DL-21 | ✅ Migrate public/versionable project material | Public code/specifications/contracts move from Drive staging to GitHub | File-by-file comparison or hash/content check where practical | DL-20 |
| DL-22 | ✅ Preserve provenance | Migrated items reference their former Drive source/version when useful | Random sample can be traced back to origin | DL-21 |
| DL-23 | ✅ Remove obsolete duplicate canon | Drive copies that are no longer canonical are clearly marked archive/reference, not silently deleted | No ambiguous “current” copy remains in Drive | DL-21 |
| DL-24 | ✅ Add release/change discipline | Changelog/release convention and version identifiers defined | One test change can be traced from commit to published version | DL-21 |

**Gate G2 — GitHub product canon established: ✅ PASS.** Current public/product material is canonical on GitHub; Drive `00_START_HERE` explicitly marks remaining product copies as provenance/archive evidence while Drive remains canonical for Library/protected/operational content. Version `0.1.0-alpha.1`, `CHANGELOG.md` and `docs/versioning.md` establish change discipline.

---

# Phase 3 — Convert the pilot page into the official GitHub Page

| ID | Task | Result | Verification / gate | Depends on |
|---|---|---|---|---|
| DL-30 | Port the existing pilot public page | GitHub Pages version reproduces the useful pilot content | Content comparison against pilot; no broken essential sections | G2 |
| DL-31 | Define the public information architecture | Home / What is DSM-LRS / How it works / User Manual / Help / GitHub | Navigation works on desktop and mobile | DL-30 |
| DL-32 | Add Welcome | New visitor can understand purpose, audience and first action | 30-second comprehension test with no project background | DL-31 |
| DL-33 | Add Help | Common actions, limitations, troubleshooting and privacy boundary documented | At least five representative tasks can be resolved from Help | DL-31 |
| DL-34 | Add User Manual | End-to-end user-facing guide separate from developer documentation | Fresh-user walkthrough reaches first successful use without internal MindMap knowledge | DL-31 |
| DL-35 | Public/no-account verification | Page and public repository work without GitHub login | Test in signed-out/incognito browser; links and downloads resolve | DL-30–DL-34 |

**Gate G3 — Public UX ready:** DSM-LRS has one public entry point that does not require a GitHub account for reading.

---

# Phase 4 — Formalize Google Drive as the Library

| ID | Task | Result | Verification / gate | Depends on |
|---|---|---|---|---|
| DL-40 | Define Library taxonomy | Separate general references, DSM-specific sources and protected/personalized material | Folder/content sample maps unambiguously to one class | G1 |
| DL-41 | Separate public references from protected content | Privacy boundary is explicit and enforceable | Protected examples are not reachable from public GitHub/Page | DL-40 |
| DL-42 | Define Library interface/contract | DSM-LRS refers to Library content through stable identifiers/configuration, not hard-coded personal paths where avoidable | Test configuration can point to another Library root/provider | DL-40 |
| DL-43 | Document source provenance and update rules | General dyslexia/LRS guidance can be updated independently from software releases | Updating a Library document does not require a DSM-LRS code release unless contract changes | DL-42 |
| DL-44 | Failure-mode test | Product behaves predictably when Library content is unavailable or access is denied | No leakage, silent fallback or accidental publication | DL-41, DL-42 |

**Gate G4 — Library boundary verified:** Drive is knowledge/content storage, not a hidden code dependency or public hosting substitute.

---

# Phase 5 — Decide and extract the standalone LRS Adapter

> **Do not create the standalone Adapter repository merely because separation sounds desirable. First prove the boundary.**

| ID | Task | Result | Verification / gate | Depends on |
|---|---|---|---|---|
| DL-50 | Inventory Adapter-specific components | Generic engine separated conceptually from DSM rules/integration | Component map marks GENERIC vs DSM-SPECIFIC | G2 |
| DL-51 | Define the Adapter standalone contract | Inputs, outputs, configuration, error model and extension points specified | Contract can be understood without reading DSM-LRS or MindMap docs | DL-50 |
| DL-52 | Dependency audit | Identify every dependency on DSM-LRS, Google Drive, MindMap, Notion, user-specific paths and private infrastructure | Generic Adapter has zero mandatory dependency on MindMap/Notion/personal infrastructure; remaining DSM dependency is via explicit interface/config | DL-51 |
| DL-53 | Standalone proof inside DSM-LRS tree | Adapter runs against fixtures/mock profile and generic library data | Clean test passes without DSM project state or private Drive access | DL-52 |
| DL-54 | **Create public `lrs-adapter` repository only after G5 passes** | Independent repository exists | Public visibility and clean initial history verified | DL-53 |
| DL-55 | Migrate generic Adapter code/contracts/tests | `lrs-adapter` becomes canonical for generic Adapter | Tests pass in new repo; no DSM-specific secrets/configuration copied | DL-54 |
| DL-56 | Reconnect DSM-LRS as consumer | DSM-LRS consumes Adapter through versioned dependency/interface | DSM-LRS test suite passes against pinned Adapter version | DL-55 |
| DL-57 | Independent portability test | Third party can use Adapter without DSM-LRS | Fresh clone/install/use from README succeeds with synthetic data | DL-55 |

**Gate G5 — Adapter extraction gate:** DL-51–DL-53 must pass before creating `lrs-adapter`.

---

# Phase 6 — Integration, verification and release

| ID | Task | Result | Verification / gate | Depends on |
|---|---|---|---|---|
| DL-60 | Cross-repository architecture check | DSM-LRS, LRS Adapter and Drive Library have non-overlapping ownership | Dependency diagram and canonical-home audit pass | G4, G5 |
| DL-61 | Privacy/publication scan | No student, diagnostic, PDP or protected Library content is in public Git history/site | Repository history + site output reviewed; synthetic examples only | DL-60 |
| DL-62 | Fresh-user public test | Non-technical visitor understands project and can access manual/resources | Test without GitHub account | DL-35, DL-60 |
| DL-63 | Fresh-developer test | Developer can clone/build/test DSM-LRS and Adapter from public instructions | Clean environment smoke test | DL-56 |
| DL-64 | Library integration test | Authorized Library access works; unauthorized/unavailable access fails safely | Positive + negative access cases documented | DL-44, DL-56 |
| DL-65 | Canonical-source conflict audit | No active document/code/state has two authoritative homes | Audit returns zero unresolved conflicts | DL-60–DL-64 |
| DL-66 | Tag first public architecture baseline | DSM-LRS public baseline released with known status and limitations | Release/tag, changelog and public page agree on version | DL-65 |

**Gate G6 — Release ready:** publication only after privacy, portability, fresh-user and canonical-source checks pass.

---

# Critical path

`DL-00 → DL-01 → DL-02 → DL-03 → DL-10 → DL-11 → DL-13 → DL-20 → DL-21 → DL-30 → DL-35 → DL-40 → DL-42 → DL-50 → DL-51 → DL-52 → DL-53 → DL-54 → DL-55 → DL-56 → DL-60 → DL-61 → DL-65 → DL-66`

## Immediate next action

**DL-30 — Prepare the existing pilot source as the official GitHub Pages site.**

Phase 2 is complete. The current public/product baseline is migrated and versioned as `0.1.0-alpha.1`; World News tests are repository-portable (9/9 PASS), Auth MVP `v0.3-public.1` is verified for public source/local synthetic testing (16/16 PASS), provenance is recorded, and Drive explicitly defers product canon to GitHub. Next is Phase 3: convert the already migrated `site/` pilot source into the official GitHub Pages entry point.

## Explicit non-goals

- Do not merge DSM-LRS into MindMap.
- Do not make MindMap a runtime dependency.
- Do not put personalized/protected Library content into public GitHub.
- Do not duplicate the Library into GitHub merely for convenience.
- Do not create `lrs-adapter` before its independence is demonstrated.
- Do not delete the current Drive project during migration; archive/mark provenance first.
