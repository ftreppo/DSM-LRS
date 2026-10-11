# LRS Adapter — generic prototype

Portable, provider-neutral working instruction for adapting learning material for LRS/dyslexia-related access needs.

## Current prototype

Version: `0.1.0-alpha.1`

Core instruction:
- `LRS_ADAPTER_GENERIC_v0.1.md`

Contract:
- `../../specifications/adapter-generic/contract-v0.1.md`

Policy interface:
- `../../specifications/adapter-generic/PolicyPack.schema.json`

Synthetic fixture:
- `fixtures/policy-pack.synthetic.json`

Conformance test:
- `../../tests/test_generic_adapter_contract.py`

## Independence

The generic Adapter:
- does not require a specific school;
- does not require DSM-LRS;
- does not require MindMap or Notion;
- does not require Google Drive;
- does not require a specific identity/storage provider.

An integrating product may supply an optional provider-neutral PolicyPack.

## Status

Gate G5 standalone proof: **PASS**.

This directory is the staging source for the future public `lrs-adapter` repository.
