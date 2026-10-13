# C13 — Official-source freshness verification

**Date:** 2026-10-12  
**Status:** **CURRENT DSM LOCAL VERSION CONFIRMED BY RICHARD / ALIGNMENT UPDATE REQUIRED**

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

On 2026-10-13 Franco reported that Richard Keiner confirmed that the 12.02.2015 DSM guideline is **still the DSM-local document currently in force**.

This closes the former uncertainty about which local DSM guideline is operative.

However, local validity and external-authority alignment are separate questions. The document predates the current BLASchA/KMK 2024/2025 framework and therefore still requires an alignment review.

Therefore:

`dsm_local_version = CURRENT_CONFIRMED_BY_RICHARD`

`external_authority_alignment = UPDATE_REQUIRED`

The preferred update strategy is documented in [C13 — DSM 2015 guideline: update now or wait for Länder legislation?](c13-update-vs-wait-assessment-2026-10-13.md): **addendum now / full rewrite later**.

## Runtime consequence

Until the protected DSM guideline version is checked and DSM-local alignment is confirmed:

- STUDY/HOMEWORK accessibility transformations that do not grant an accommodation remain governed by the generic Adapter contract and authorized context.
- ASSESSMENT / GRADED / graduation-related adaptation that depends on an accommodation entitlement must **fail closed** unless a current authorized PolicyPack / individual arrangement explicitly supplies the permitted measure.
- The Adapter must not infer entitlement from the 2015 guideline.
- The Adapter must not use older DSM wording to override newer BLASchA/KMK rules.
- An authority conflict or uncertainty remains `ZU KLÄREN`.

## Manual closure condition

The DSM-local version check is now closed by the 2026-10-13 Richard confirmation.

C13 can fully close after the remaining **alignment/update decision** is completed:

- reconcile the still-operative 12.02.2015 local guideline with:
  - BLASchA LRS recommendations i.d.F. 25.04.2025;
  - BLASchA abschlussbezogener Nachteilsausgleich 11.12.2024;
  - current DIA-PO/Rili DIA-PO where applicable;
- decide and approve the DSM-local update form (recommended: bounded Addendum first, full rewrite later).

## Project rule

Until C13 fully closes, DSM-LRS may describe the 2015 document as:

**current DSM-local guideline confirmed in force by Richard Keiner on 2026-10-13; alignment with newer BLASchA/KMK 2024/2025 authority remains under update review.**

It must not be used to override newer or more specific BLASchA/KMK examination rules.
