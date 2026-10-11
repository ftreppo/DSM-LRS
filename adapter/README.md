# DSM-specific Adapter

DSM-LRS now consumes the **generic** Adapter from the independent public repository:

**https://github.com/ftreppo/lrs-adapter**

Pinned generic baseline: `0.1.0-alpha.1`.

## Canonical split

### lrs-adapter — canonical generic layer

The standalone repository owns:
- generic portable Adapter instruction;
- generic input/output/assessment contract;
- provider-neutral PolicyPack schema;
- generic fixtures and conformance tests;
- generic Community Adapter Lab.

### DSM-LRS — DSM-specific layer

This repository remains responsible for:
- DSM-specific school-stage rules and integration;
- DSM-specific authority/governance semantics;
- DSM source/reference material;
- protected/personalized context;
- DSM-LRS public product and documentation.

## Existing DSM-specific baseline

The DSM-specific historical/current project baseline remains:

- Adapter core: **v2.5**
- Release package metadata: **v2.5.1**
- Behavior change from core v2.5: **NO**
- Privacy-boundary change: **NO**
- Authority change: **NO**
- Official-source freshness: **REVIEW REQUIRED BEFORE REAL OPERATIONAL USE**

Core DSM-specific files remain in [core/](core/). Release notes and public traceability remain in [releases/v2.5.1/](releases/v2.5.1/).

## Generic extraction provenance

The former `generic-prototype/` area is retained only as extraction/provenance evidence. It is **not canonical** after DL-56.

Canonical generic source:
https://github.com/ftreppo/lrs-adapter

DSM-LRS consumer declaration:
[../integrations/lrs-adapter/README.md](../integrations/lrs-adapter/README.md)

## Authority status

Neither the generic Adapter nor DSM-LRS is an official DSM rulebook. The v2.5.1 DSM traceability snapshot does not prove that the registered 2015 DSM guideline is the latest applicable official source. No current-official-rule compliance claim should be made until that freshness check passes.
