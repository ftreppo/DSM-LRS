# Generic LRS Adapter contract v0.1

## Goal

Define a portable LRS/dyslexia adaptation instruction that can be used independently from DSM-LRS, MindMap, Notion, Google Drive or any specific school.

## Required work-item inputs

For every task:
- `material` or source content;
- `subject_or_activity`;
- `objective`;
- `use_case`: `STUDY | HOMEWORK | ASSESSMENT`.

For `ASSESSMENT` additionally:
- `assessed_competence`;
- applicable restrictions/conditions if known.

Optional:
- authorized `policy_context` / PolicyPack;
- functional observations relevant to access;
- output/file preference.

## Assessment gate

If `use_case = ASSESSMENT` and `assessed_competence` is absent, stop before adaptation.

Do not infer the assessed competence merely from diagnosis, subject or document appearance.

## Adaptation selection

The use-case does not directly select an output mode.

Select the **smallest sufficient compatible** intervention from:
- `ORIGINAL_FAITHFUL`
- `READING_OPTIMIZED`
- `LEARNING_VERSION`
- `ASSESSMENT_ADAPTATION`

The selected intervention must remain compatible with:
- the objective;
- assessed competence where relevant;
- confirmed measures/restrictions;
- explicit source/task constraints.

## Authority / PolicyPack

The Adapter accepts a provider-neutral PolicyPack.

Measure status:
- `CONFIRMED`
- `POSSIBLE_IF_CONFIRMED`
- `DO_NOT_APPLY`
- `TO_CLARIFY`

Only `CONFIRMED` measures are executable by default.

`POSSIBLE_IF_CONFIRMED` does not authorize execution.
`TO_CLARIFY` fails closed for authority-dependent changes.

## Fidelity

Preserve:
- questions;
- facts and numbers;
- subject terminology;
- conditions and requirements;
- learning objective;
- intellectual/subject difficulty;
- required answer;
- points and assessment criteria unless an authorized policy explicitly requires otherwise.

Do not solve exercises or add answer-relevant hints.

If source content cannot be read reliably, mark it `[UNREADABLE / CHECK]` instead of guessing.

## Privacy

Do not request raw diagnoses, full clinical records, anamnesis, full PDP/Förderplan or unnecessary identifiers for ordinary use.

Use only the minimum authorized context needed for the adaptation.

## Output contract

Ordinary work:
1. adapted material;
2. short applied-changes log;
3. unresolved items, if any.

Assessment work:
1. student-facing adapted material;
2. task/subtask equivalence check;
3. measures/status log;
4. `PASS | REVIEW | FAIL`;
5. separate `HUMAN_REVIEW_REQUIRED` flag when a human decision is needed.

## Portability

The Adapter must function:
- with no PolicyPack for generic STUDY/HOMEWORK work that does not require an authority-specific measure;
- with a local/synthetic PolicyPack;
- with a PolicyPack supplied by another product.

Storage, identity, school governance and Library provider are outside this contract.
