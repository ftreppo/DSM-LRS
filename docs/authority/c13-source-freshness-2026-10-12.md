# C13 — Official-source freshness verification

**Date:** 2026-10-12  
**Status:** **UPDATE_REQUIRED / MANUAL DSM VERSION CHECK**

## Question

Is the DSM guideline adopted on 12.02.2015 still sufficient as the current official authority basis for DSM-LRS, including assessment and graduation-related use?

## Evidence

### DSM public surface

The current Deutsche Schule Mailand website still publishes the page:

`Lese-Rechtschreib-Störung und spezifische Lernstörungen`

The page states that DSM support is based on the BLASchA decision of 17.03.2010 and Italian DM 5669/2011, and links to:

`Richtlinien der DSM zum Umgang mit Lese-, Rechtschreib- bzw. Rechenstörungen`

The linked document currently requires DSM login, so its present protected version/revision date cannot be verified from the public web.

Public page:
https://www.dsmailand.it/de/gymnasium/lrs-und-lernstoerungen

Protected target observed:
`component/edocman/?id=253&task=document.viewDoc`

### DSM-LRS Library

The project Library contains the DSM document:

`DSM_LRS_Richtlinien_DE_approvate_2015-02-12.pdf`

Title:
`Umgang mit Lese-, Rechtschreib- bzw. Rechenstörungen`

Project metadata records adoption by the Schulleitungskomitee on **12.02.2015**.

No newer DSM-local guideline copy was found in the targeted Drive searches performed on 2026-10-12.

### Current German Auslandsschule authority

The current Kultusministerkonferenz Auslandsschulen page lists materially newer authority sources:

1. **Empfehlungen zur Förderung von Schülerinnen und Schülern mit besonderen Schwierigkeiten beim Lesen und Rechtschreiben sowie beim Rechnen an den Deutschen Schulen im Ausland**
   - original BLASchA decision: 17.03.2010
   - current published version: **25.04.2025**

2. **Richtlinie für den abschlussbezogenen Nachteilsausgleich**
   - BLASchA decision: **11.12.2024**
   - includes specific provisions for reading/spelling impairments.

3. **DIA-PO** and **Rili DIA-PO**
   - current version listed by KMK: **27.11.2025**

Official KMK source:
https://www.kmk.org/downloads-dokumente/beschluesse-und-veroeffentlichungen/bildung-/-schule/auslandsschulen.html

## C13 conclusion

The 2015 DSM guideline may still be a valid **DSM-local policy document**, but it is **not sufficient by itself as proof of current authority freshness**.

At minimum, current operation must account for the newer BLASchA/KMK sources above.

Therefore:

`official_source_freshness = UPDATE_REQUIRED`

and not:

`CURRENT_CONFIRMED`

## Runtime consequence

Until the protected DSM guideline version is checked and DSM-local alignment is confirmed:

- STUDY/HOMEWORK accessibility transformations that do not grant an accommodation remain governed by the generic Adapter contract and authorized context.
- ASSESSMENT / GRADED / graduation-related adaptation that depends on an accommodation entitlement must **fail closed** unless a current authorized PolicyPack / individual arrangement explicitly supplies the permitted measure.
- The Adapter must not infer entitlement from the 2015 guideline.
- The Adapter must not use older DSM wording to override newer BLASchA/KMK rules.
- An authority conflict or uncertainty remains `ZU KLÄREN`.

## Manual closure condition

C13 can close only after both are verified:

1. **DSM protected-document check**
   - login to the DSM protected area;
   - open the guideline linked from the current LRS page;
   - record title, revision/version date, approval authority and whether it is still the 12.02.2015 text or a newer revision.

2. **DSM alignment check**
   - confirm with the responsible DSM authority/LRS coordination that the local guideline currently in force has been reconciled with:
     - BLASchA LRS recommendations i.d.F. 25.04.2025;
     - BLASchA abschlussbezogener Nachteilsausgleich 11.12.2024;
     - current DIA-PO/Rili DIA-PO where applicable.

## Project rule

Until C13 closes, DSM-LRS may describe the 2015 document only as:

**registered DSM-local working source (2015), current protected-page linkage observed, freshness/alignment not yet confirmed.**

It must not be described as the latest applicable official rule.
