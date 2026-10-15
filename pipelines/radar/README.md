# DSM-LRS Radar

Status: **DESIGN ONLY / NOT ENABLED**.

This directory defines the DSM-LRS project profile for the provider-neutral REGIA Signal Radar.

It does not replace `pipelines/world-news`.

Separation:

~~~text
shared source intake
      ↓
DSM-LRS Radar Finding
      ↓
project impact / workflow review

independent path:
      ↓
LRS News Worldwide
      ↓
ADMIN approval / public publication
~~~

The radar reuses the existing public-safe World News source registry where appropriate:

- `../world-news/WORLD_NEWS_SOURCES.json`

No scheduler, n8n workflow, unattended execution or automatic DSM-LRS policy update is enabled by this directory.
