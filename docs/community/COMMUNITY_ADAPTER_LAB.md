# Community Adapter Lab

---

# Deutsch

## Zweck

Das **Community Adapter Lab** sammelt anonymisierte, öffentlich teilbare Beispiele aus der realen Nutzung des Adapters. Ziel ist, wiederkehrende Stärken, Schwächen und Verbesserungskandidaten systematisch zu erkennen.

Es ist **kein direkter Änderungsweg für den Adapter-Kern** und **kein Ort für Schülerdaten oder andere geschützte Informationen**.

## Ablauf

```text
ÖFFENTLICHE SUBMISSION
        ↓
DATENSCHUTZ- / RECHTE-PRÜFUNG
        ↓
TECHNISCHE & PÄDAGOGISCHE REVIEW
        ↓
KLASSIFIKATION
        ↓
┌─────────────────────┬────────────────────────┐
│ GEPRÜFTES BEISPIEL  │ VERBESSERUNGSKANDIDAT │
│ examples/community/ │ Improvement Register   │
└─────────────────────┴────────────────────────┘
        ↓
EVIDENZ ÜBER MEHRERE FÄLLE
        ↓
VORGESCHLAGENE ADAPTER-ÄNDERUNG
        ↓
TEST / VERIFIKATION / RELEASE-GATE
```

## Beispiel einreichen

Verwende das öffentliche GitHub-Formular:

**[Adapter-Beispiel einreichen](https://github.com/ftreppo/DSM-LRS/issues/new?template=adapter-example.yml)**

Das Issue ist öffentlich. Das Formular enthält verpflichtende Datenschutz- und Rechte-Bestätigungen.

## Was eine gute Submission enthält

- Adapter-Version;
- Sprache;
- STUDY / HOMEWORK / ASSESSMENT;
- Fach;
- optional grobe Schulstufe/Klasse ohne Identifizierung;
- Ziel;
- bei ASSESSMENT die geprüfte Kompetenz;
- anonymisiertes oder synthetisches Originalmaterial;
- Adapter-Ergebnis;
- was gut funktioniert hat;
- was verbessert werden sollte;
- optional unerwartetes Verhalten.

## Datenschutz und Rechte

Nie einreichen:
- Namen oder Identifikatoren von Schüler:innen;
- E-Mail-Adressen oder Telefonnummern;
- Unterschriften;
- Diagnosen oder klinische Berichte;
- PDP/Förderplan-Dokumente;
- private Korrespondenz;
- private Drive-Links;
- Zugangsdaten oder Tokens;
- urheberrechtlich geschütztes/vertrauliches Material ohne Weitergaberecht.

Im Zweifel ein kurzes synthetisches Minimalbeispiel erstellen, das das Verhalten reproduziert.

## Nach der Einreichung

Eine rohe GitHub-Submission wird **nie automatisch** zu einer kanonischen Adapter-Regel oder zu einem geprüften Beispiel.

Mögliche analytische Klassifikationen:
`GOOD_EXAMPLE`, `ADAPTER_WEAKNESS`, `AMBIGUOUS`, `ASSESSMENT_SAFETY`, `LAYOUT`, `LANGUAGE`, `OCR_UNREADABLE`, `SUBJECT_TERMINOLOGY`, `POLICY_CONTEXT`, `NEW_USE_CASE`, `NO_CHANGE_NEEDED`.

Eine Promotion nach `examples/community/reviewed/` erfolgt nur nach Datenschutz-/Rechteprüfung, ausreichender Review, öffentlicher Anonymisierung und entsprechender Erlaubnis.

## Verbesserungen

Ein einzelner Fall kann eine Prüfung auslösen. Kleinere Präferenzen sollten normalerweise durch wiederholte Evidenz gestützt werden. Ein schwerwiegender Fall im Bereich `ASSESSMENT_SAFETY` kann sofortige Review rechtfertigen.

---

# Italiano

## Scopo

Il **Community Adapter Lab** raccoglie esempi anonimizzati e condivisibili pubblicamente dall'uso reale dell'Adapter. Lo scopo è individuare in modo sistematico punti di forza, debolezze ricorrenti e candidati di miglioramento.

Non è **un canale di modifica diretta del core dell'Adapter** e non è **un luogo per dati di studenti o altre informazioni protette**.

## Flusso

```text
SUBMISSION PUBBLICA
        ↓
CONTROLLO PRIVACY / DIRITTI
        ↓
REVISIONE TECNICA & PEDAGOGICA
        ↓
CLASSIFICAZIONE
        ↓
┌─────────────────────┬────────────────────────┐
│ ESEMPIO REVISIONATO │ CANDIDATO MIGLIORAMENTO│
│ examples/community/ │ Improvement Register   │
└─────────────────────┴────────────────────────┘
        ↓
EVIDENZA SU PIÙ CASI
        ↓
PROPOSTA DI MODIFICA ADAPTER
        ↓
TEST / VERIFICA / RELEASE GATE
```

## Inviare un esempio

Usa il modulo pubblico GitHub:

**[Invia un esempio dell'Adapter](https://github.com/ftreppo/DSM-LRS/issues/new?template=adapter-example.yml)**

La Issue è pubblica. Il modulo contiene conferme obbligatorie su privacy e diritto di condivisione.

## Cosa dovrebbe contenere una buona submission

- versione dell'Adapter;
- lingua;
- STUDY / HOMEWORK / ASSESSMENT;
- materia;
- livello/classe generale opzionale, senza identificare lo studente;
- obiettivo;
- per ASSESSMENT, competenza valutata;
- materiale originale anonimizzato o sintetico;
- risultato dell'Adapter;
- cosa ha funzionato;
- cosa potrebbe migliorare;
- eventuale comportamento inatteso.

## Privacy e diritti

Non inviare mai:
- nomi o identificativi di studenti;
- email o numeri di telefono;
- firme;
- diagnosi o referti clinici;
- documenti PDP/Förderplan;
- corrispondenza privata;
- link Drive privati;
- credenziali o token;
- materiale protetto da copyright o riservato senza diritto di condivisione.

In caso di dubbio, crea un breve esempio sintetico minimo che riproduca il comportamento.

## Dopo l'invio

Una submission grezza su GitHub **non diventa mai automaticamente** una regola canonica dell'Adapter o un esempio revisionato.

Classificazioni analitiche possibili:
`GOOD_EXAMPLE`, `ADAPTER_WEAKNESS`, `AMBIGUOUS`, `ASSESSMENT_SAFETY`, `LAYOUT`, `LANGUAGE`, `OCR_UNREADABLE`, `SUBJECT_TERMINOLOGY`, `POLICY_CONTEXT`, `NEW_USE_CASE`, `NO_CHANGE_NEEDED`.

La promozione in `examples/community/reviewed/` avviene solo dopo controllo privacy/diritti, revisione sufficiente, anonimizzazione pubblica e autorizzazione appropriata.

## Miglioramenti

Un singolo caso può aprire una review. Le preferenze minori dovrebbero normalmente essere sostenute da evidenza ripetuta. Un caso grave classificato `ASSESSMENT_SAFETY` può giustificare una revisione immediata.

---

# English

## Purpose

The **Community Adapter Lab** collects anonymized, public-safe examples from real Adapter use. Its purpose is to identify recurring strengths, weaknesses, and improvement candidates systematically.

It is **not a direct-edit channel for the Adapter core** and **not a place for student or other protected data**.

## Flow

```text
PUBLIC SUBMISSION
        ↓
PRIVACY / RIGHTS CHECK
        ↓
TECHNICAL & PEDAGOGICAL REVIEW
        ↓
CLASSIFICATION
        ↓
┌─────────────────────┬────────────────────────┐
│ REVIEWED EXAMPLE    │ IMPROVEMENT CANDIDATE │
│ examples/community/ │ Improvement Register   │
└─────────────────────┴────────────────────────┘
        ↓
EVIDENCE ACROSS MULTIPLE CASES
        ↓
PROPOSED ADAPTER CHANGE
        ↓
TEST / VERIFICATION / RELEASE GATE
```

## Submit an example

Use the public GitHub form:

**[Submit an Adapter Example](https://github.com/ftreppo/DSM-LRS/issues/new?template=adapter-example.yml)**

The issue is public. The form contains mandatory privacy and sharing-rights confirmations.

## What a useful submission contains

- Adapter version;
- language;
- STUDY / HOMEWORK / ASSESSMENT;
- subject;
- optional broad school stage/class without identifying a learner;
- objective;
- assessed competence for ASSESSMENT;
- anonymized or synthetic original material;
- Adapter output;
- what worked;
- what could improve;
- optional unexpected behavior.

## Privacy and rights

Never submit:
- student names or identifiers;
- email addresses or phone numbers;
- signatures;
- diagnoses or clinical reports;
- PDP/Förderplan documents;
- private correspondence;
- private Drive links;
- credentials or tokens;
- copyrighted/confidential material without the right to share it.

When in doubt, create a short synthetic minimal example that reproduces the behavior.

## After submission

A raw GitHub submission **never automatically becomes** a canonical Adapter rule or reviewed example.

Possible analytical classifications:
`GOOD_EXAMPLE`, `ADAPTER_WEAKNESS`, `AMBIGUOUS`, `ASSESSMENT_SAFETY`, `LAYOUT`, `LANGUAGE`, `OCR_UNREADABLE`, `SUBJECT_TERMINOLOGY`, `POLICY_CONTEXT`, `NEW_USE_CASE`, `NO_CHANGE_NEEDED`.

Promotion to `examples/community/reviewed/` happens only after privacy/rights review, sufficient review, public-safe anonymization, and appropriate permission.

## Improvements

A single case can trigger review. Minor preferences should normally be supported by repeated evidence. A serious `ASSESSMENT_SAFETY` case may justify immediate review.
