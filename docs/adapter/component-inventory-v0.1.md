# Adapter component inventory — generic vs DSM-specific v0.1

**Date:** 2026-10-11  
**Task:** DL-50  
**Source baseline:** DSM-specific Adapter core v2.5 / release traceability v2.5.1.

## GENERIC components

These can belong to a standalone LRS Adapter without DSM-LRS runtime state:

1. startup/onboarding and Help;
2. explicit use-case mode: STUDY / HOMEWORK / ASSESSMENT;
3. rule that use-case mode is not the same as adaptation/output mode;
4. select the smallest sufficient compatible intervention;
5. no diagnosis inference and no diagnosis-based automatic mode selection;
6. functional learning/access profile as optional working context;
7. reading vs comprehension distinction;
8. observation → measure mapping only when authority/status supports it;
9. content-fidelity checks;
10. original-faithful / reading-optimized / learning-version output families;
11. assessment adaptation with assessed-competence gate;
12. assessment equivalence checking and no-answer-hints safeguard;
13. subject terminology preservation;
14. photo / scan / PDF uncertainty handling;
15. typography and layout principles;
16. optional TTS where compatible with the task/assessment;
17. print-ready A4 output conventions;
18. privacy minimization;
19. explicit unresolved/clarification status;
20. portable use as an AI working instruction.

## DSM-SPECIFIC components

These remain in DSM-LRS or a DSM policy pack:

1. DSM branding and DSM-specific project description;
2. DSM school-stage gate;
3. DSM-specific stage rules for Grundschule / classes 5–12;
4. registered DSM 2015 guideline and its source-freshness state;
5. DSM-specific authority/role wording;
6. current project terminology such as APPROVED Personal Prompt where it refers to DSM-LRS protected-core authority;
7. DSM-LRS Orchestrator naming where it refers to the DSM-LRS architecture;
8. creator/project-specific INFO content;
9. DSM-specific operational measure provenance and school approval semantics;
10. any real DSM or student-specific configuration/data.

## EXTRACT / RENAME

| DSM-LRS term | Generic contract term |
|---|---|
| APPROVED Personal Prompt | authorized policy context |
| Orchestrator | adaptation selector |
| DSM school-stage gate | optional PolicyPack stage/assessment gate |
| DSM operational measure register | authorized measures |
| BESTÄTIGT | CONFIRMED |
| REGELKONFORM MÖGLICH | POSSIBLE_IF_CONFIRMED |
| NICHT ANWENDEN | DO_NOT_APPLY |
| ZU KLÄREN | TO_CLARIFY |
| MANUELLE PRÜFUNG ERFORDERLICH | HUMAN_REVIEW_REQUIRED |

## Boundary rule

The generic Adapter may **consume** an optional PolicyPack supplied by DSM-LRS or another school/context, but it must not know how that PolicyPack was stored, approved or generated.

DSM-LRS may depend on the generic Adapter. The generic Adapter must not depend on DSM-LRS.
