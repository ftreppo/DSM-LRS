# DSM-specific Adapter

This directory is the current public home of the **DSM-specific** LRS Adapter while the generic/portable boundary is being defined and tested.

## Current migrated baseline

- Adapter core: **v2.5**
- Release package metadata: **v2.5.1**
- Release type: metadata / provenance / traceability only
- Behavior change from core v2.5: **NO**
- Privacy-boundary change: **NO**
- Authority change: **NO**
- Official-source freshness: **REVIEW REQUIRED BEFORE REAL OPERATIONAL USE**

Core files live in [core/](core/). Release notes and public traceability live in [releases/v2.5.1/](releases/v2.5.1/).

## Extraction boundary

This is **not** yet the future generic `lrs-adapter` repository.

A standalone repository will be created only after Gate G5 demonstrates that the generic Adapter:

1. has a standalone input/output/configuration contract;
2. isolates DSM-specific rules behind explicit configuration or interfaces;
3. runs against synthetic fixtures without DSM-LRS project state;
4. has no mandatory dependency on MindMap, Notion or private Google Drive content.

## Authority status

The Adapter is a project tool and not an official DSM document. The v2.5.1 traceability snapshot does not prove that the registered 2015 DSM guideline is the latest applicable official source. No current-official-rule compliance claim should be made until that freshness check passes.

## Public repository rule

Only public-safe product material belongs here. Private or personalized source material stays outside this repository.
