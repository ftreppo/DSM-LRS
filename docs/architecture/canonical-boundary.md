# Canonical architecture boundary

## DSM-LRS

Canonical for:
- DSM-specific product/integration;
- public DSM-LRS site;
- Auth MVP;
- World News pipeline;
- DSM-specific policies/specifications;
- Library provider interface;
- DSM-LRS release history.

## lrs-adapter

Canonical for:
- generic portable LRS Adapter;
- standalone Adapter contract;
- provider-neutral PolicyPack schema;
- generic Adapter tests/fixtures;
- generic Community Adapter Lab;
- generic Adapter improvement/release history.

## Google Drive Library

Canonical for:
- DSM source/reference documents;
- general LRS/DSA reference corpus;
- teaching/learning guidelines;
- protected/personalized documents;
- private operational/library material.

## MindMap / REGIA

Coordination only.

No runtime dependency from DSM-LRS or lrs-adapter.

## Dependency graph

```text
MindMap / REGIA
      |
      | coordination only
      v
DSM-LRS  ----------------------> Google Drive Library
  |
  | pinned generic dependency
  v
lrs-adapter
```

The generic Adapter does not know DSM-LRS.
DSM-LRS may know and consume the generic Adapter.
