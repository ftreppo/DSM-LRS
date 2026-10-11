DSM-LRS — MVP-0 DATA CONTRACT v0.1 — FROZEN FOR PROTOTYPE


Date: 2026-09-16
Status: FROZEN FOR MVP-0 PROTOTYPE ONLY
Scope: fictitious-data prototype; not production governance.


PURPOSE
This document freezes the first stable data contract for the DSM-LRS operational prototype so interface work can begin without changing table semantics ad hoc.


CORE INVARIANTS
1. Database is the source of truth; generated documents are derivatives.
2. AI may propose but may not commit.
3. Human approval is required for any official operational-profile or impact-level change.
4. Significant changes create new versions; previous versions are superseded, not overwritten.
5. Student identity is stable; class membership is an annual enrollment.
6. Subject is a rule scope/filter, not part of student identity.
7. Raw PDP/clinical source material remains outside the operational database.
8. Parent contacts and restricted support status are separate from operational rule tables.
9. Teacher authorization derives from active role + class/subject assignment, not email alone.
10. Uncertainty is explicit and never encoded as a midpoint.


STANDARD LEARNING-PROFILE DOMAINS
READING — Lettura / Dislessia
SPELLING — Ortografia / Disortografia
WRITING — Scrittura / Grafomotricità
MATHEMATICS — Calcolo / Discalculia


OPERATIONAL-IMPACT SCALE
1 = low operational impact — ●○○○
2 = relevant operational impact — ●●○○
3 = high operational impact — ●●●○
4 = very high / strongly relevant operational impact — ●●●●


States outside the scale:
ABSENT / NOT_APPLICABLE
INSUFFICIENT_EVIDENCE
PENDING_REVIEW


SEMESTER REVIEW CONTRACT
Question 1: Compared with the last approved assessment, is there a meaningful change?
Allowed: NO_CHANGE | YES | INSUFFICIENT_EVIDENCE


Question 2: only if Question 1 = YES.
Allowed: IMPROVED | MORE_IMPACT


Optional teacher follow-up: suggested level 1–4 + evidence note.
Teacher observation never changes the official level automatically.


CORE TABLES
STUDENTS
- student_id
- display_name
- active
- created_at
- notes


CLASSES
- class_id
- school_year
- class_name
- level
- active
- notes


ENROLLMENTS
- enrollment_id
- student_id
- class_id
- school_year
- valid_from
- valid_to
- status


SUBJECTS
- subject_id
- multilingual labels
- subject_group
- active


TEACHERS
- teacher_id
- display_name
- institutional_email
- active
- role
- notes


TEACHER_ASSIGNMENTS
- assignment_id
- teacher_id
- school_year
- class_id
- subject_id
- assignment_role
- valid_from
- valid_until
- status


PARENT_CONTACTS
- contact_id
- student_id
- contact_name
- relationship
- email
- phone
- preferred_contact
- active


SUPPORT_REGISTRY
- support_id
- student_id
- school_year
- support_status
- valid_from
- valid_until
- source_reference
- review_due
- notes


LEARNING_PROFILE_DOMAINS
- learning_profile_id
- student_id
- school_year
- domain_code
- status
- impact_level
- source_reference
- approved_by
- approved_at
- valid_from
- valid_until
- profile_version
- notes


PROFILES
- profile_id
- student_id
- school_year
- version
- status
- source_pdp_date
- created_at
- approved_at
- approved_by
- valid_from
- valid_until
- supersedes_profile_id
- review_reason
- notes


RULES
- rule_id
- profile_id
- category
- subject_scope
- condition_code
- action_code
- value
- rule_status
- priority
- source_reference
- human_note


APPROVALS
- approval_id
- profile_id
- approver_name
- approver_role
- approval_date
- decision
- comment


REVIEW_CYCLES
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


TEACHER_OBSERVATIONS
- observation_id
- cycle_id
- teacher_id
- student_id
- class_id
- subject_id
- domain_code
- current_impact_level
- q1_change_observed
- q2_change_direction
- suggested_impact_level
- evidence_note
- submitted_at
- status
- human_note
- validation_flag


SEMESTER_SUMMARY
- summary_id
- cycle_id
- student_id
- domain_code
- current_impact_level
- observation_count
- no_change_count
- change_yes_count
- insufficient_evidence_count
- improved_count
- more_impact_count
- suggested_levels_summary
- conflict_flag
- lrs_review_decision
- approved_impact_level
- approved_by
- approved_at
- notes


CLASS_REPORT_VERSIONS
- report_id
- class_id
- school_year
- version
- generated_at
- valid_from
- status
- supersedes_report_id
- change_reason
- notes


CHANGELOG
Every significant profile/domain/report change must write an immutable audit entry.


GENERATED OUTPUT CONTRACTS
A. Personal Operational Profile
B. Class + Subject Operational Profile
C. Class Master Report
D. Semester LRS Review Summary


CLASS MASTER REPORT
Restricted to class teacher / authorized LRS staff by default.
Contains:
- complete class roster;
- parent/guardian contact details;
- minimal support status;
- four-domain visual learning profile;
- current operational profile status/version;
- approval metadata;
- report version/change reason.


CLASS + SUBJECT PROFILE
For subject teachers.
Contains only authorized students and operational rules relevant to ALL + selected subject/group.
Does not include parent contacts by default.


VERSIONING RULE
When an approved domain/profile datum changes:
old domain/profile record → SUPERSEDED
new record/version → APPROVED or CONFIRMED
Class Master Report current version → SUPERSEDED
new Class Master Report version → CURRENT
CHANGELOG entry required.


MVP-0 VALIDATION COMPLETED
- Natural-language ingestion → AI draft → human review → approved profile: PASS
- Generated personal profile: PASS
- Generated class+subject profile: PASS
- Generated Class Master Report: PASS
- Multi-teacher semester review: PASS
- Human-approved impact change 3→2: PASS
- Previous domain/profile/report superseded: PASS
- New domain/profile/report versions created: PASS


NEXT BOUNDARY
The data contract may now be used to design an authenticated teacher/operator interface with fictitious data. Production authentication, real-data access, sharing and school governance remain outside this freeze and require explicit authorization.


TEST / PROTOTYPE CONTRACT — NOT A PRODUCTION POLICY DOCUMENT.