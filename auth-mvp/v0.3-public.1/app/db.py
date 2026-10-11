from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from .security import hash_password

SCHEMA = r"""
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS accounts (
    account_id TEXT PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    display_name TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    primary_role TEXT NOT NULL,
    linked_teacher_id TEXT,
    linked_student_id TEXT,
    status TEXT NOT NULL DEFAULT 'ACTIVE'
);
CREATE TABLE IF NOT EXISTS account_roles (
    username TEXT NOT NULL,
    role_code TEXT NOT NULL,
    PRIMARY KEY (username, role_code),
    FOREIGN KEY (username) REFERENCES accounts(username) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS role_permissions (
    role_code TEXT NOT NULL,
    resource_code TEXT NOT NULL,
    action TEXT NOT NULL,
    scope_rule TEXT NOT NULL,
    allowed INTEGER NOT NULL,
    PRIMARY KEY(role_code, resource_code, action)
);
CREATE TABLE IF NOT EXISTS teachers (
    teacher_id TEXT PRIMARY KEY,
    display_name TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS teacher_assignments (
    assignment_id TEXT PRIMARY KEY,
    teacher_id TEXT NOT NULL,
    school_year TEXT NOT NULL,
    class_id TEXT NOT NULL,
    subject_id TEXT NOT NULL,
    assignment_role TEXT NOT NULL,
    valid_from TEXT NOT NULL,
    valid_until TEXT NOT NULL,
    status TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS students (
    student_id TEXT PRIMARY KEY,
    display_name TEXT NOT NULL,
    active INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS enrollments (
    enrollment_id TEXT PRIMARY KEY,
    student_id TEXT NOT NULL,
    class_id TEXT NOT NULL,
    school_year TEXT NOT NULL,
    status TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS profiles (
    profile_id TEXT PRIMARY KEY,
    student_id TEXT NOT NULL,
    school_year TEXT NOT NULL,
    version REAL NOT NULL,
    status TEXT NOT NULL,
    approved_at TEXT,
    approved_by TEXT,
    supersedes_profile_id TEXT,
    review_reason TEXT
);
CREATE TABLE IF NOT EXISTS rules (
    rule_id TEXT PRIMARY KEY,
    profile_id TEXT NOT NULL,
    category TEXT NOT NULL,
    subject_scope TEXT NOT NULL,
    condition_code TEXT NOT NULL,
    action_code TEXT NOT NULL,
    value TEXT NOT NULL,
    rule_status TEXT NOT NULL,
    priority INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS learning_profile_domains (
    learning_profile_id TEXT PRIMARY KEY,
    student_id TEXT NOT NULL,
    school_year TEXT NOT NULL,
    domain_code TEXT NOT NULL,
    status TEXT NOT NULL,
    impact_level INTEGER,
    profile_version REAL NOT NULL,
    valid_until TEXT
);
CREATE TABLE IF NOT EXISTS parent_contacts (
    contact_id TEXT PRIMARY KEY,
    student_id TEXT NOT NULL,
    contact_name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT,
    active INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS support_registry (
    support_id TEXT PRIMARY KEY,
    student_id TEXT NOT NULL,
    school_year TEXT NOT NULL,
    support_status TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS class_report_versions (
    report_id TEXT PRIMARY KEY,
    class_id TEXT NOT NULL,
    school_year TEXT NOT NULL,
    version TEXT NOT NULL,
    generated_at TEXT NOT NULL,
    status TEXT NOT NULL,
    supersedes_report_id TEXT,
    change_reason TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS review_cycles (
    cycle_id TEXT PRIMARY KEY,
    school_year TEXT NOT NULL,
    semester TEXT NOT NULL,
    label TEXT NOT NULL,
    status TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS teacher_observations (
    observation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    cycle_id TEXT NOT NULL,
    teacher_id TEXT NOT NULL,
    student_id TEXT NOT NULL,
    class_id TEXT NOT NULL,
    subject_id TEXT NOT NULL,
    domain_code TEXT NOT NULL,
    current_impact_level INTEGER NOT NULL,
    q1_change_observed TEXT NOT NULL,
    q2_change_direction TEXT,
    suggested_impact_level INTEGER,
    evidence_note TEXT,
    submitted_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS semester_summary (
    summary_id TEXT PRIMARY KEY,
    cycle_id TEXT NOT NULL,
    student_id TEXT NOT NULL,
    domain_code TEXT NOT NULL,
    current_impact_level INTEGER NOT NULL,
    observation_count INTEGER NOT NULL,
    no_change_count INTEGER NOT NULL,
    change_yes_count INTEGER NOT NULL,
    insufficient_evidence_count INTEGER NOT NULL,
    improved_count INTEGER NOT NULL,
    more_impact_count INTEGER NOT NULL,
    lrs_review_decision TEXT,
    approved_impact_level INTEGER,
    approved_by TEXT,
    approved_at TEXT,
    notes TEXT
);
CREATE TABLE IF NOT EXISTS operator_drafts (
    draft_id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_by TEXT NOT NULL,
    student_id TEXT,
    source_text TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'DRAFT',
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS audit_log (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    occurred_at TEXT NOT NULL,
    username TEXT,
    event_type TEXT NOT NULL,
    resource TEXT,
    outcome TEXT NOT NULL,
    detail TEXT
);
"""

ACCOUNTS = [
    ("ACC-0001", "member01", "Member Demo 01", "MEMBER", None, None, []),
    ("ACC-0002", "student01", "Student Demo 01", "STUDENT", None, "STU-0001", []),
    ("ACC-0003", "teacher01", "Subject Teacher Demo 01", "SUBJECT_TEACHER", "TCH-0003", None, []),
    ("ACC-0004", "classteacher01", "Class Teacher Demo 01", "CLASS_TEACHER", "TCH-0001", None, ["SUBJECT_TEACHER"]),
    ("ACC-0005", "operator01", "Operator Demo 01", "OPERATOR", None, None, []),
    ("ACC-0006", "lrsadmin01", "LRS Admin Demo 01", "LRS_ADMIN", None, None, []),
    ("ACC-0007", "dsm01", "DSM Coordinator Demo 01", "DSM_COORDINATOR", None, None, []),
    ("ACC-0008", "admin01", "System Admin Demo 01", "SYSTEM_ADMIN", None, None, []),
]

PERMISSIONS = [
    ("MEMBER", "MEMBER_HOME", "READ", "GENERAL_INTERNAL"),
    ("STUDENT", "OWN_PROFILE", "READ", "OWN_STUDENT_ONLY"),
    ("SUBJECT_TEACHER", "MY_CLASSES", "READ", "ACTIVE_ASSIGNMENTS_ONLY"),
    ("SUBJECT_TEACHER", "CLASS_SUBJECT_PROFILE", "READ", "ACTIVE_ASSIGNMENTS_ONLY"),
    ("SUBJECT_TEACHER", "SEMESTER_REVIEW", "SUBMIT", "ACTIVE_ASSIGNMENTS_ONLY"),
    ("SUBJECT_TEACHER", "TEACHER_NOTIFICATIONS", "READ", "SELF"),
    ("CLASS_TEACHER", "CLASS_HOME", "READ", "ASSIGNED_CLASS_ONLY"),
    ("CLASS_TEACHER", "CLASS_MASTER_REPORT", "READ", "ASSIGNED_CLASS_ONLY"),
    ("CLASS_TEACHER", "PARENT_CONTACTS", "READ", "ASSIGNED_CLASS_ONLY"),
    ("CLASS_TEACHER", "SEMESTER_REVIEW", "SUBMIT", "ASSIGNED_CLASS_ONLY"),
    ("OPERATOR", "OPERATOR_CONSOLE", "READ_WRITE", "OPERATIONAL_WORKFLOW"),
    ("OPERATOR", "INGESTION_QUEUE", "CREATE_EDIT", "OPERATIONAL_WORKFLOW"),
    ("OPERATOR", "AI_DRAFT_RULES", "EDIT_DRAFT", "OPERATIONAL_WORKFLOW"),
    ("OPERATOR", "REVIEW_QUEUE", "PREPARE", "OPERATIONAL_WORKFLOW"),
    ("OPERATOR", "EXPORT_QUEUE", "REQUEST", "APPROVED_DATA_ONLY"),
    ("LRS_ADMIN", "LRS_ADMIN_HOME", "READ", "SCHOOL_WIDE_LRS"),
    ("LRS_ADMIN", "PROFILES", "READ_APPROVE", "SCHOOL_WIDE_LRS"),
    ("LRS_ADMIN", "LEARNING_PROFILE_DOMAINS", "READ_APPROVE", "SCHOOL_WIDE_LRS"),
    ("LRS_ADMIN", "SEMESTER_SUMMARY", "READ_APPROVE", "SCHOOL_WIDE_LRS"),
    ("LRS_ADMIN", "CLASS_MASTER_REPORT", "READ", "SCHOOL_WIDE_LRS"),
    ("LRS_ADMIN", "PARENT_CONTACTS", "READ", "SCHOOL_WIDE_LRS"),
    ("LRS_ADMIN", "REPORT_HISTORY", "READ", "SCHOOL_WIDE_LRS"),
    ("DSM_COORDINATOR", "DSM_OVERVIEW", "READ", "SCHOOL_WIDE_READ_ONLY"),
    ("DSM_COORDINATOR", "CURRENT_APPROVED_PROFILES", "READ", "SCHOOL_WIDE_READ_ONLY"),
    ("DSM_COORDINATOR", "CLASS_MASTER_REPORT", "READ", "SCHOOL_WIDE_READ_ONLY"),
    ("DSM_COORDINATOR", "PARENT_CONTACTS", "READ", "SCHOOL_WIDE_READ_ONLY"),
    ("DSM_COORDINATOR", "SEMESTER_SUMMARY", "READ", "SCHOOL_WIDE_READ_ONLY"),
    ("SYSTEM_ADMIN", "SYSTEM_ADMIN_HOME", "READ", "SYSTEM_CONFIGURATION"),
    ("SYSTEM_ADMIN", "AUTH_TEST_ACCOUNTS", "MANAGE", "SYSTEM_CONFIGURATION"),
    ("SYSTEM_ADMIN", "ACCESS_ROLES", "MANAGE", "SYSTEM_CONFIGURATION"),
    ("SYSTEM_ADMIN", "ROLE_PERMISSIONS", "MANAGE", "SYSTEM_CONFIGURATION"),
    ("SYSTEM_ADMIN", "TEACHER_ASSIGNMENTS", "MANAGE", "SYSTEM_CONFIGURATION"),
    ("SYSTEM_ADMIN", "AUDIT_LOG", "READ", "SYSTEM_CONFIGURATION"),
    ("SYSTEM_ADMIN", "SYSTEM_CONFIG", "MANAGE", "SYSTEM_CONFIGURATION"),
]

TEACHERS = [
    ("TCH-0001", "Eva Müller"),
    ("TCH-0002", "Marco Bianchi"),
    ("TCH-0003", "Laura Smith"),
    ("TCH-0004", "Jonas Weber"),
    ("TCH-0005", "Sophie Keller"),
    ("TCH-0006", "Luca Romano"),
]

ASSIGNMENTS = [
    ("TAS-0001","TCH-0001","2026-27","CLS-2026-7A","ALL","CLASS_TEACHER","2026-09-01","2027-08-31","ACTIVE"),
    ("TAS-0002","TCH-0001","2026-27","CLS-2026-7A","GERMAN","SUBJECT_TEACHER","2026-09-01","2027-08-31","ACTIVE"),
    ("TAS-0003","TCH-0002","2026-27","CLS-2026-7B","ALL","CLASS_TEACHER","2026-09-01","2027-08-31","ACTIVE"),
    ("TAS-0004","TCH-0002","2026-27","CLS-2026-7B","ITALIAN","SUBJECT_TEACHER","2026-09-01","2027-08-31","ACTIVE"),
    ("TAS-0005","TCH-0003","2026-27","CLS-2026-7A","MATHEMATICS","SUBJECT_TEACHER","2026-09-01","2027-08-31","ACTIVE"),
    ("TAS-0006","TCH-0003","2026-27","CLS-2026-7B","MATHEMATICS","SUBJECT_TEACHER","2026-09-01","2027-08-31","ACTIVE"),
    ("TAS-0007","TCH-0004","2026-27","CLS-2026-7A","ENGLISH","SUBJECT_TEACHER","2026-09-01","2027-08-31","ACTIVE"),
    ("TAS-0008","TCH-0004","2026-27","CLS-2026-7B","ENGLISH","SUBJECT_TEACHER","2026-09-01","2027-08-31","ACTIVE"),
    ("TAS-0009","TCH-0005","2026-27","CLS-2026-7A","SCIENCE","SUBJECT_TEACHER","2026-09-01","2027-08-31","ACTIVE"),
    ("TAS-0010","TCH-0005","2026-27","CLS-2026-7B","SCIENCE","SUBJECT_TEACHER","2026-09-01","2027-08-31","ACTIVE"),
    ("TAS-0011","TCH-0006","2026-27","CLS-2026-7A","HISTORY","SUBJECT_TEACHER","2026-09-01","2027-08-31","ACTIVE"),
    ("TAS-0012","TCH-0006","2026-27","CLS-2026-7B","HISTORY","SUBJECT_TEACHER","2026-09-01","2027-08-31","ACTIVE"),
]

STUDENT_NAMES = [
    ("STU-0001","Anna Beispiel"),("STU-0002","Luca Esempio"),("STU-0003","Sofia Muster"),
    ("STU-0004","Marco Demo"),("STU-0005","Emilia Testa"),("STU-0006","Jonas Probe"),
    ("STU-0007","Matteo Finto"),("STU-0008","Lea Beispiel"),("STU-0009","David Muster"),
    ("STU-0010","Giulia Demo"),("STU-0011","Noah Esempio"),("STU-0012","Clara Test"),
]

DOMAIN_LEVELS = {
    "STU-0001": {"READING":2,"SPELLING":2,"WRITING":2,"MATHEMATICS":None},
    "STU-0002": {"READING":1,"SPELLING":1,"WRITING":1,"MATHEMATICS":3},
    "STU-0003": {"READING":2,"SPELLING":3,"WRITING":2,"MATHEMATICS":1},
    "STU-0004": {"READING":2,"SPELLING":2,"WRITING":3,"MATHEMATICS":2},
    "STU-0005": {"READING":4,"SPELLING":3,"WRITING":3,"MATHEMATICS":None},
    "STU-0006": {"READING":1,"SPELLING":2,"WRITING":1,"MATHEMATICS":2},
    "STU-0007": {"READING":None,"SPELLING":None,"WRITING":2,"MATHEMATICS":4},
    "STU-0008": {"READING":2,"SPELLING":2,"WRITING":3,"MATHEMATICS":1},
    "STU-0009": {"READING":3,"SPELLING":4,"WRITING":3,"MATHEMATICS":None},
    "STU-0010": {"READING":1,"SPELLING":1,"WRITING":2,"MATHEMATICS":2},
    "STU-0011": {"READING":2,"SPELLING":3,"WRITING":4,"MATHEMATICS":1},
    "STU-0012": {"READING":None,"SPELLING":None,"WRITING":None,"MATHEMATICS":None},
}


def connect(path: str | Path) -> sqlite3.Connection:
    conn = sqlite3.connect(str(path), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


@contextmanager
def connection(path: str | Path) -> Iterator[sqlite3.Connection]:
    conn = connect(path)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def initialize(path: str | Path, reset: bool = False, *, seed_demo: bool = False, demo_password: str | None = None) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if reset and path.exists():
        path.unlink()
    with connection(path) as conn:
        conn.executescript(SCHEMA)
        existing = conn.execute("SELECT COUNT(*) FROM accounts").fetchone()[0]
        if existing:
            return
        if not seed_demo:
            raise RuntimeError("Empty database: explicit DSM_LRS_DEMO_MODE=1 is required to seed fictitious demo data")
        if not demo_password:
            raise RuntimeError("DSM_LRS_DEMO_PASSWORD is required when demo seeding is enabled")
        pwd = hash_password(demo_password)
        for aid, username, name, primary, teacher, student, extra in ACCOUNTS:
            conn.execute(
                "INSERT INTO accounts VALUES (?,?,?,?,?,?,?,?)",
                (aid, username, name, pwd, primary, teacher, student, "ACTIVE"),
            )
            conn.execute("INSERT INTO account_roles VALUES (?,?)", (username, primary))
            for role in extra:
                conn.execute("INSERT INTO account_roles VALUES (?,?)", (username, role))
        conn.executemany(
            "INSERT INTO role_permissions VALUES (?,?,?,?,1)", PERMISSIONS
        )
        conn.executemany("INSERT INTO teachers VALUES (?,?)", TEACHERS)
        conn.executemany(
            "INSERT INTO teacher_assignments VALUES (?,?,?,?,?,?,?,?,?)", ASSIGNMENTS
        )
        for sid, name in STUDENT_NAMES:
            conn.execute("INSERT INTO students VALUES (?,?,1)", (sid, name))
            class_id = "CLS-2026-7A" if int(sid[-2:]) <= 6 else "CLS-2026-7B"
            conn.execute(
                "INSERT INTO enrollments VALUES (?,?,?,?,?)",
                (f"ENR-{sid[-4:]}", sid, class_id, "2026-27", "ACTIVE"),
            )
            conn.execute(
                "INSERT INTO parent_contacts VALUES (?,?,?,?,?,1)",
                (f"CON-{sid[-4:]}", sid, f"Parent of {name}", f"parent{int(sid[-2:]):02d}@example.invalid", "TEST-NOT-REAL"),
            )
            support = "NONE" if sid == "STU-0012" else ("PENDING_REVIEW" if sid == "STU-0004" else "CURRENT")
            conn.execute(
                "INSERT INTO support_registry VALUES (?,?,?,?)",
                (f"SUP-{sid[-4:]}", sid, "2026-27", support),
            )
            for domain, level in DOMAIN_LEVELS[sid].items():
                status = "NOT_APPLICABLE" if level is None else ("PENDING_REVIEW" if sid == "STU-0004" else "CONFIRMED")
                conn.execute(
                    "INSERT INTO learning_profile_domains VALUES (?,?,?,?,?,?,?,?)",
                    (f"LPD-{sid[-4:]}-{domain}", sid, "2026-27", domain, status, level, 1.0, "2027-08-31"),
                )
        profiles = [
            ("PROF-0001-2026-2","STU-0001",2,"APPROVED","2027-01-22","LRS Responsible TEST","PROF-0001-2026-1","SEMESTER_REVIEW_S1"),
            ("PROF-0002-2026-1","STU-0002",1,"APPROVED","2026-09-13","Teacher B",None,"INITIAL"),
            ("PROF-0003-2026-1","STU-0003",1,"APPROVED","2026-09-14","Teacher A",None,"INITIAL"),
            ("PROF-0004-2026-1","STU-0004",0.9,"DRAFT",None,None,None,"INITIAL"),
            ("PROF-0005-2026-1","STU-0005",1,"APPROVED","2026-09-16","LRS Responsible TEST",None,"INITIAL_AI_ASSISTED_TEST"),
        ]
        for pid,sid,ver,status,aat,aby,sup,reason in profiles:
            conn.execute(
                "INSERT INTO profiles VALUES (?,?,?,?,?,?,?,?,?)",
                (pid,sid,"2026-27",ver,status,aat,aby,sup,reason),
            )
        rules = [
            ("R-0050","PROF-0001-2026-2","LAYOUT","ALL","ALWAYS","SEGMENT_INSTRUCTIONS","TRUE","APPROVED",10),
            ("R-0051","PROF-0001-2026-2","LAYOUT","ALL","ALWAYS","INCREASE_SPACING","TRUE","APPROVED",20),
            ("R-0052","PROF-0001-2026-2","ACCESS","ALL","READING_NOT_ASSESSED","TTS","ALLOWED","APPROVED",30),
            ("R-0053","PROF-0001-2026-2","ACCESS","ENGLISH","READING_ASSESSED","TTS","NOT_ALLOWED","APPROVED",40),
            ("R-0010","PROF-0002-2026-1","ACCESS","MATHEMATICS","WORD_PROBLEM","READ_ALOUD","ALLOWED","APPROVED",10),
            ("R-0011","PROF-0002-2026-1","ACCESS","MATHEMATICS","AID_ALLOWED","FORMULA_SHEET","ALLOWED","APPROVED",20),
            ("R-0012","PROF-0002-2026-1","ASSESSMENT","ALL","WRITTEN_TEST","EXTRA_TIME_PERCENT","30","APPROVED",30),
            ("R-0020","PROF-0003-2026-1","LAYOUT","ALL","ALWAYS","CLEAR_VISUAL_HIERARCHY","TRUE","APPROVED",10),
            ("R-0021","PROF-0003-2026-1","ASSESSMENT","LANGUAGES","SPELLING_NOT_TARGET","SPELLING_EVALUATION","SUSPEND","APPROVED",20),
            ("R-0022","PROF-0003-2026-1","ACCESS","ALL","ALWAYS","COMPUTER","ALLOWED","APPROVED",30),
            ("R-0030","PROF-0004-2026-1","LAYOUT","ALL","ALWAYS","SEGMENT_INSTRUCTIONS","TRUE","DRAFT",10),
            ("R-0040","PROF-0005-2026-1","LAYOUT","ALL","ALWAYS","SEGMENT_INSTRUCTIONS","TRUE","APPROVED",10),
            ("R-0041","PROF-0005-2026-1","LAYOUT","ALL","ALWAYS","INCREASE_SPACING","TRUE","APPROVED",20),
            ("R-0042","PROF-0005-2026-1","ASSESSMENT","ALL","WRITTEN_TEST","EXTRA_TIME_PERCENT","30","APPROVED",30),
            ("R-0043","PROF-0005-2026-1","ACCESS","ALL","WRITTEN_PRODUCTION","COMPUTER","ALLOWED","APPROVED",40),
        ]
        conn.executemany("INSERT INTO rules VALUES (?,?,?,?,?,?,?,?,?)", rules)
        conn.executemany(
            "INSERT INTO class_report_versions VALUES (?,?,?,?,?,?,?,?)",
            [
                ("CRV-7A-0003","CLS-2026-7A","2026-27","0.3-test","2027-01-22","CURRENT","CRV-7A-0002","SEMESTER_REVIEW_STU-0001_READING_3_TO_2"),
                ("CRV-7B-0001","CLS-2026-7B","2026-27","0.1-test","2026-09-16","CURRENT",None,"INITIAL_TEST_BASELINE"),
            ],
        )
        conn.execute(
            "INSERT INTO review_cycles VALUES (?,?,?,?,?)",
            ("RC-2026-S1","2026-27","S1","TEST — Semester 1 LRS review before grade conference","COMPLETED"),
        )
        conn.execute(
            "INSERT INTO semester_summary VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            ("SUM-S1-0001","RC-2026-S1","STU-0001","READING",3,4,1,2,1,2,0,"CHANGE_LEVEL",2,"LRS Responsible TEST","2027-01-22","Two improved, one no change, one insufficient evidence. TEST DATA ONLY."),
        )
        conn.execute(
            "INSERT INTO semester_summary VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            ("SUM-S1-0002","RC-2026-S1","STU-0002","MATHEMATICS",3,3,1,2,0,2,0,None,None,None,None,"Pending fictitious LRS decision; two teachers suggest reduced impact. TEST DATA ONLY."),
        )
