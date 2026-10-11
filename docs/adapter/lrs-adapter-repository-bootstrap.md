# lrs-adapter repository bootstrap

Target repository: `ftreppo/lrs-adapter`

Recommended visibility: **Public**

Recommended license: **Apache-2.0**

Recommended description:

> Portable, provider-neutral LRS/dyslexia learning-material adapter with assessment safeguards, PolicyPack interface, tests and documentation.

## Initial repository layout

```text
lrs-adapter/
├── README.md
├── LICENSE
├── VERSION
├── CHANGELOG.md
├── adapter/
│   └── LRS_ADAPTER_GENERIC_v0.1.md
├── specifications/
│   ├── contract-v0.1.md
│   └── PolicyPack.schema.json
├── fixtures/
│   └── policy-pack.synthetic.json
└── tests/
    └── test_generic_adapter_contract.py
```

## Migration source

Only the GENERIC artifacts are copied.

Do **not** copy:
- DSM school-stage rules;
- DSM 2015 source material;
- DSM-LRS project state;
- private Google Drive locators;
- Personal Prompt / protected-core state;
- DSM-specific branding/authority rules.

## Post-creation gate

After repository creation:
1. copy the generic artifacts;
2. run/read back conformance tests;
3. verify forbidden-dependency scan;
4. make `lrs-adapter` canonical for generic Adapter artifacts;
5. change DSM-LRS from owner of the generic files to consumer/integrator.
