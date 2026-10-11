# Community Adapter Lab

## Purpose

The Community Adapter Lab turns real-world, public-safe Adapter use into structured evidence for improving the LRS Adapter.

It is **not** a direct-edit channel for the core Adapter and it is **not** a place for student records.

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
│ REVIEWED EXAMPLE    │ IMPROVEMENT CANDIDATE  │
│ examples/community/ │ improvement register    │
└─────────────────────┴────────────────────────┘
      ↓
EVIDENCE ACROSS MULTIPLE CASES
      ↓
PROPOSED ADAPTER CHANGE
      ↓
TEST / VERIFICATION / RELEASE GATE
```

## Submission entry point

Use the GitHub Issue Form:

**Submit an Adapter Example / Beispiel einreichen / Invia un esempio**

The issue is public. The form contains a mandatory privacy and sharing-rights gate.

## Submission fields

A useful submission contains:
- Adapter version;
- language;
- STUDY / HOMEWORK / ASSESSMENT;
- subject;
- broad school stage/class if useful and non-identifying;
- objective;
- assessed competence for ASSESSMENT;
- anonymized/synthetic original material;
- Adapter output;
- what worked;
- what should improve;
- optional unexpected behavior.

## Privacy and rights boundary

Never submit:
- student names or identifiers;
- email addresses or phone numbers;
- signatures;
- diagnoses or clinical reports;
- PDP/Förderplan documents;
- private correspondence;
- private Drive links;
- credentials/tokens;
- copyrighted/confidential school material unless the submitter has the right to share it.

When in doubt, create a synthetic minimal example that reproduces the behavior.

## Review classifications

A reviewed submission can receive one or more analytical classifications:

- `GOOD_EXAMPLE`
- `ADAPTER_WEAKNESS`
- `AMBIGUOUS`
- `ASSESSMENT_SAFETY`
- `LAYOUT`
- `LANGUAGE`
- `OCR_UNREADABLE`
- `SUBJECT_TERMINOLOGY`
- `POLICY_CONTEXT`
- `NEW_USE_CASE`
- `NO_CHANGE_NEEDED`

These are analytical classifications, not endorsements.

## Promotion rule

A raw GitHub issue never becomes a canonical example automatically.

Promotion to `examples/community/reviewed/` requires:
1. privacy/rights check PASS;
2. reproduction or sufficient review;
3. public-safe anonymization;
4. reviewer note;
5. explicit status;
6. contributor permission where required.

## Improvement rule

A single case can create an improvement candidate, but normally does not change the Adapter core by itself.

Repeated patterns across submissions should be aggregated in the Improvement Register.

Example:

```text
7 submissions
→ same OCR behavior
→ ADAPTER_WEAKNESS
→ candidate: strengthen [UNREADABLE / CHECK]
→ regression tests
→ contract review
→ release decision
```

## Relationship to lrs-adapter

During DSM-LRS bootstrap this Lab lives in `DSM-LRS`.

After the standalone `lrs-adapter` repository is created and made canonical for the generic Adapter, the generic Community Adapter Lab should move there. DSM-LRS may retain DSM-specific case studies or integrations.
