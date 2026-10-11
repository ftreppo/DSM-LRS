# DSM-LRS developer quickstart

Technical maintainer documentation; English is canonical for this file.

## Requirements

- Git
- Python 3.12+
- public access to:
  - https://github.com/ftreppo/DSM-LRS
  - https://github.com/ftreppo/lrs-adapter

## DSM-LRS checkout and tests

```bash
git clone https://github.com/ftreppo/DSM-LRS.git
cd DSM-LRS
python -m pip install -r requirements-dev.txt

cd auth-mvp/v0.3-public.1
pytest -q
cd ../..

pytest -q pipelines/world-news/test_world_news_weekly_pipeline_v0_1.py
pytest -q tests/test_library_provider_contract.py
```

Expected baselines:
- Auth MVP: 16 tests;
- World News: 9 tests;
- Library provider contract: 6 tests.

All test data is synthetic/fictitious.

## Generic Adapter

The generic Adapter is not maintained in this repository.

Canonical repository:
https://github.com/ftreppo/lrs-adapter

DSM-LRS pins the standalone baseline through:
`integrations/lrs-adapter/consumer.json`.

## Public site

Public site source is under `site/`.

Live site:
https://ftreppo.github.io/DSM-LRS/

## Privacy

Never add real student, diagnostic, PDP/Förderplan, clinical, correspondence, credential or private-Library data to the public repositories.
