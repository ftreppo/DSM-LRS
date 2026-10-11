# DSM-LRS Operational Profile System — Evolution v0.7
**Date:** 2026-09-16

## New component: semester teacher review cycle

Before report-card / grade conferences, the system should open a structured LRS review cycle so teachers can report whether the current visual learning-profile indicators still reflect the student's observed school functioning.

The purpose is not to rediagnose the student. It is to collect classroom evidence from several teachers and make changes, if appropriate, through a controlled human review.

## Teacher experience

For each assigned student/domain, the teacher sees:

- current domain;
- current operational impact level (0–4);
- visual dot indicator;
- current approved operational rules relevant to the teacher's subject.

The teacher then selects one of:

- `UNCHANGED` — current indicator still fits;
- `IMPROVED` — observed impact appears lower;
- `MORE_SUPPORT_NEEDED` — observed impact appears higher / current support may be insufficient;
- `NOT_OBSERVED` — teacher has not had enough opportunity to assess this domain;
- `UNSURE` — teacher cannot make a reliable judgment.

The teacher may optionally suggest a new impact level and add a short evidence note.

Example:

Student: Anna Beispiel
Domain: Reading
Current: 3 / 4

Teacher assessment: IMPROVED
Suggested level: 2 / 4
Comment: "Reads longer instructions more independently than at the beginning of the semester."

This is a teacher observation, not an automatic profile change.

## Review timing

Recommended cycle:

1. Review campaign opens 1–3 weeks before the semester / grade conference.
2. Assigned teachers receive a portal notification and optionally an email reminder.
3. Teachers submit observations by a defined deadline.
4. The system consolidates all teacher feedback by student and domain.
5. LRS responsible / authorized reviewer receives a semester summary.
6. Reviewer decides:
   - KEEP CURRENT LEVEL
   - CHANGE LEVEL
   - NEEDS DISCUSSION
   - NEEDS NEW / UPDATED SOURCE DOCUMENT
7. Only an approved reviewer decision changes the official learning-profile indicator.
8. Any approved change creates a new operational profile version and, where relevant, a new Class Master Report version.

## Multi-teacher aggregation

Teacher feedback should not be averaged mechanically.

Example:

Reading current level: 3

- German teacher: IMPROVED → suggests 2
- English teacher: UNCHANGED → 3
- History teacher: IMPROVED → 2
- Mathematics teacher: NOT_OBSERVED

The system should show the pattern and flag disagreement, but the LRS reviewer makes the final decision.

AI may summarize observations, for example:

"Two teachers report reduced reading-support needs, one reports no meaningful change, one did not observe the domain."

AI must not decide the new level.

## Prototype data model

### REVIEW_CYCLES
- cycle_id
- school_year
- semester
- label
- opens_at
- teacher_deadline
- conference_date
- status
- created_by
- notes

### TEACHER_OBSERVATIONS
- observation_id
- cycle_id
- teacher_id
- student_id
- class_id
- subject_id
- domain_code
- current_impact_level
- teacher_assessment
- proposed_impact_level
- evidence_note
- submitted_at
- status
- human_note

### SEMESTER_SUMMARY
- summary_id
- cycle_id
- student_id
- domain_code
- current_impact_level
- observation_count
- unchanged_count
- improved_count
- more_support_count
- uncertain_count
- conflict_flag
- lrs_review_decision
- approved_impact_level
- approved_by
- approved_at
- notes

## Relationship to visual dots

The visual dot strip remains a quick teacher reminder.

Teacher observations may suggest changing a dot level, but:

**Teacher observation → proposal / evidence**

not:

**Teacher observation → automatic dot change**

Only the designated LRS responsible / authorized reviewer can approve the updated official level.

## Versioning

An approved change to a learning-profile domain or impact level must:

1. create a new learning-profile/profile version;
2. record who approved it and when;
3. supersede the previous version;
4. trigger a new Class Master Report version;
5. optionally notify authorized teachers that a new version is available.

Historical teacher observations remain linked to the review cycle and are not overwritten.

## Portal concept

Before the semester conference, teachers see:

### "LRS Semester Review"

7A — 4 reviews pending

Anna Beispiel — Reading
Current: 3 ●●●○
[Unchanged] [Improved] [More support needed] [Not observed] [Unsure]

Luca Esempio — Mathematics
Current: 3 ●●●○
[Unchanged] [Improved] [More support needed] [Not observed] [Unsure]

The form should take seconds per student unless the teacher wants to add a note.

## New decisions

- OP-035: Run structured teacher review cycles before semester / grade conferences.
- OP-036: Teacher observations may propose a change but never alter official indicators automatically.
- OP-037: Consolidate multi-teacher observations by student and domain for LRS review.
- OP-038: Approved semester changes trigger new operational-profile and Class Master Report versions.
- OP-039: Do not mechanically average teacher observations; disagreement is information to review.
- OP-040: AI may summarize teacher observations but may not decide the official impact level.
- OP-041: Keep historical review-cycle observations as immutable evidence.

## Roadmap

- P0 DONE — Adapter ON HOLD.
- P1 DONE — normalized operational data model.
- P2 IN VALIDATION — AI-assisted ingestion.
- P3A PROTOTYPE — personal operational profile.
- P3B PROTOTYPE — class + subject profile.
- P3C IN DESIGN — Class Master Report + versioning.
- P3D IN DESIGN — teacher registry / access model.
- P3E IN DESIGN — visual learning-profile indicators.
- P3F NOW — semester teacher review cycle.
- P4 FUTURE — private PDP → operational profile workflow.
- P5 FUTURE — governed internal pilot.
- P6 FUTURE — DSM-managed authenticated portal/API.

## Codex policy

No Codex is needed for this design and spreadsheet prototype.

Codex becomes useful later for:
- authenticated review forms;
- automatic teacher assignment filtering;
- review reminders;
- conflict summaries;
- deterministic version generation;
- portal notifications and audit logging.
