# Contributing to DSM-LRS

DSM-LRS is an open project with a strict privacy boundary.

## Community Adapter Lab

### Deutsch

Wenn du ein reales Adapter-Ergebnis beitragen möchtest, ohne Code zu ändern, verwende das strukturierte GitHub-Formular:

**[Adapter-Beispiel einreichen](https://github.com/ftreppo/DSM-LRS/issues/new?template=adapter-example.yml)**

Die Submission ist öffentlich.

Vor dem Einreichen:
- personenbezogene Daten und Schülerdaten entfernen;
- keine Diagnosen, klinischen Berichte oder PDP/Förderplan-Dokumente hochladen;
- keine privaten Drive-Links, Zugangsdaten oder private Korrespondenz einfügen;
- nur Material teilen, das du weitergeben darfst;
- bei urheberrechtlich geschütztem oder vertraulichem Material ein kurzes synthetisches/anonymisiertes Äquivalent verwenden.

Rohe Submissions werden zuerst geprüft. Sie werden nicht automatisch zu kanonischen Beispielen oder Adapter-Regeln.

Öffentliche Community-Seite: [Community Adapter Lab](docs/community/COMMUNITY_ADAPTER_LAB.md)

### Italiano

Se vuoi contribuire con un risultato reale dell'Adapter senza modificare il codice, usa il modulo GitHub strutturato:

**[Invia un esempio dell'Adapter](https://github.com/ftreppo/DSM-LRS/issues/new?template=adapter-example.yml)**

La submission è pubblica.

Prima dell'invio:
- rimuovi dati personali e dati dello studente;
- non caricare diagnosi, referti clinici o documenti PDP/Förderplan;
- non inserire link Drive privati, credenziali o corrispondenza privata;
- condividi solo materiale che hai il diritto di condividere;
- se il materiale è protetto da copyright o riservato, usa un breve equivalente sintetico/anonimizzato.

Le submission grezze vengono prima revisionate. Non diventano automaticamente esempi canonici o regole dell'Adapter.

Pagina pubblica Community: [Community Adapter Lab](docs/community/COMMUNITY_ADAPTER_LAB.md)

### English

If you want to contribute a real-world Adapter result without changing code, use the structured GitHub form:

**[Submit an Adapter Example](https://github.com/ftreppo/DSM-LRS/issues/new?template=adapter-example.yml)**

The submission is public.

Before submitting:
- remove personal and student information;
- do not upload diagnoses, clinical reports, or PDP/Förderplan documents;
- do not include private Drive links, credentials, or private correspondence;
- share only material you have the right to share;
- when material is copyrighted or confidential, use a short synthetic/anonymized equivalent.

Raw submissions are reviewed first. They do not automatically become canonical examples or Adapter rules.

Public Community page: [Community Adapter Lab](docs/community/COMMUNITY_ADAPTER_LAB.md)

## Maintainer / technical contribution notes

The following technical/project-maintainer sections remain in English by design.

### Code / documentation scope

Contributions may cover public product code, specifications, documentation, tests, synthetic examples and the public website.

### Privacy boundary

Never submit student data, diagnoses, PDPs, clinical reports, names, grades, signatures, student numbers, access tokens, private Google Drive links or other protected/personalized material.

Use synthetic data for examples and tests.

### Internal review resources

- [Review Checklist](docs/community/REVIEW_CHECKLIST.md)
- [Improvement Register](docs/community/IMPROVEMENT_REGISTER.md)

### Architecture

Keep DSM-LRS independent from MindMap, Notion and personal infrastructure.

The generic Adapter has passed its standalone extraction gate and will move to the separate `lrs-adapter` repository once that repository is created. Generic Adapter community submissions should eventually follow the generic Adapter there; DSM-LRS may retain DSM-specific integrations and case studies.

Before substantial structural changes, check [docs/roadmap.md](docs/roadmap.md).
