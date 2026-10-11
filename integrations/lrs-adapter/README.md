# DSM-LRS → lrs-adapter integration

## Canonical dependency

DSM-LRS consumes the generic Adapter from:

**https://github.com/ftreppo/lrs-adapter**

Pinned baseline:

`0.1.0-alpha.1`

Canonical generic artifacts:
- `adapter/LRS_ADAPTER_GENERIC_v0.1.md`
- `specifications/contract-v0.1.md`
- `specifications/PolicyPack.schema.json`
- `fixtures/policy-pack.synthetic.json`
- `tests/test_generic_adapter_contract.py`

## Dependency direction

```text
DSM-LRS  ──►  lrs-adapter
```

The generic Adapter must not depend on DSM-LRS.

## DSM-specific responsibility

DSM-LRS remains responsible for:
- DSM-specific school-stage rules;
- DSM-specific authority/governance semantics;
- DSM source/reference material;
- protected/personalized operational context;
- DSM-LRS integration and presentation.

Those concerns are supplied to the generic Adapter through explicit DSM-LRS policy/integration context; they do not become part of the generic Adapter repository.

## Current transition note

The former `adapter/generic-prototype/` and `specifications/adapter-generic/` copies in DSM-LRS are retained only as extraction/provenance evidence. They are **not canonical** after DL-56.

For generic Adapter changes, use `ftreppo/lrs-adapter`.
