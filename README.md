# DSM-LRS

**DSM-LRS** is an open project for LRS support at the Deutsche Schule Mailand / Scuola Germanica di Milano.

**Deutsch:** Offenes Projekt zur LRS-Unterstützung an der Deutschen Schule Mailand: adaptive Lernmaterialien, dokumentierte Regeln, Benutzerhilfen und portable Werkzeuge.

**Italiano:** Progetto aperto per il supporto LRS alla Scuola Germanica di Milano: materiali didattici adattivi, regole documentate, guide utente e strumenti portabili.

## Status

**Public/product canon established — baseline `0.1.0-alpha.1`.**

GitHub is canonical for versioned product code, specifications, tests, public documentation and site source. Google Drive remains canonical for the LRS/DSM document Library, protected/personalized material and operational state.

The next workstream is the official GitHub Pages entry point, based on the existing migrated static pilot in `site/`.

## Architecture boundary

- **GitHub:** public product, code, specifications, tests, documentation, release history and GitHub Pages.
- **Google Drive:** general LRS/dyslexia reference library, DSM reference material, and protected/personalized documents.
- **LRS Adapter:** standalone extraction gate passed; a separate public `lrs-adapter` repository is the next canonical home for the generic Adapter.
- **MindMap / REGIA:** coordination only; never a runtime dependency of DSM-LRS.

See [the project roadmap](docs/roadmap.md), [changelog](CHANGELOG.md), and [versioning convention](docs/versioning.md).

## Privacy

Do **not** commit student data, diagnoses, PDPs, clinical reports, names, grades, signatures, student numbers or other protected/personalized information to this public repository.

Examples and tests must use synthetic or otherwise non-sensitive data.

## Contributions

### Community Adapter Lab

**Deutsch:** [Adapter-Beispiel einreichen](https://github.com/ftreppo/DSM-LRS/issues/new?template=adapter-example.yml) — öffentlich, anonymisiert, keine persönlichen oder geschützten Daten. Eine rohe Submission wird erst nach Review zu einem kuratierten Beispiel oder Verbesserungskandidaten.

**Italiano:** [Invia un esempio dell'Adapter](https://github.com/ftreppo/DSM-LRS/issues/new?template=adapter-example.yml) — pubblico, anonimizzato, senza dati personali o protetti. Una submission grezza diventa un esempio curato o un candidato di miglioramento solo dopo revisione.

**English:** [Submit an Adapter Example](https://github.com/ftreppo/DSM-LRS/issues/new?template=adapter-example.yml) — public, anonymized, and free of personal/protected data. A raw submission becomes a curated example or improvement candidate only after review.

See [Community Adapter Lab](docs/community/COMMUNITY_ADAPTER_LAB.md) and [CONTRIBUTING.md](CONTRIBUTING.md).

Code/documentation contributions should stay within the public/product scope and must not include protected or personal data.

## License

Licensed under the [Apache License 2.0](LICENSE).
