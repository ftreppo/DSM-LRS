from __future__ import annotations

import re
import sqlite3
from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class VersionResult:
    summary_id: str
    decision: str
    domain_id: str | None = None
    profile_id: str | None = None
    report_id: str | None = None


def _next_report_version(current: str) -> str:
    m = re.match(r"^(\d+)\.(\d+)(.*)$", current)
    if not m:
        return current + ".1"
    major, minor, suffix = int(m.group(1)), int(m.group(2)), m.group(3)
    return f"{major}.{minor + 1}{suffix}"


def _next_report_id(conn: sqlite3.Connection, class_id: str) -> str:
    short = class_id.split("-")[-1]
    rows = conn.execute("SELECT report_id FROM class_report_versions WHERE class_id=?", (class_id,)).fetchall()
    highest = 0
    for row in rows:
        m = re.search(r"-(\d+)$", row["report_id"])
        if m:
            highest = max(highest, int(m.group(1)))
    return f"CRV-{short}-{highest + 1:04d}"


def apply_lrs_decision(
    conn: sqlite3.Connection,
    *,
    summary_id: str,
    decision: str,
    approved_level: int | None,
    approved_by: str,
    approved_at: str,
    audit_username: str,
) -> VersionResult:
    """Apply one human LRS decision atomically on an open semester summary.

    CHANGE_LEVEL creates a new domain version, operational profile version, copied
    approved rules, and Class Master Report version. KEEP_CURRENT records the
    human decision without changing versioned records.
    """
    summary = conn.execute("SELECT * FROM semester_summary WHERE summary_id=?", (summary_id,)).fetchone()
    if not summary:
        raise ValueError("Unknown semester summary")
    if summary["lrs_review_decision"]:
        raise ValueError("Semester summary already decided")
    if decision not in {"KEEP_CURRENT", "CHANGE_LEVEL"}:
        raise ValueError("Unsupported LRS decision")

    current_level = int(summary["current_impact_level"])
    if decision == "KEEP_CURRENT":
        conn.execute(
            """UPDATE semester_summary SET lrs_review_decision=?, approved_impact_level=?, approved_by=?, approved_at=?
               WHERE summary_id=?""",
            (decision, current_level, approved_by, approved_at, summary_id),
        )
        conn.execute(
            "INSERT INTO audit_log(occurred_at,username,event_type,resource,outcome,detail) VALUES (?,?,?,?,?,?)",
            (approved_at, audit_username, "LRS_DECISION", "SEMESTER_SUMMARY", "ALLOW", f"{summary_id}: KEEP_CURRENT {current_level}"),
        )
        return VersionResult(summary_id=summary_id, decision=decision)

    if approved_level not in {1, 2, 3, 4}:
        raise ValueError("Approved level must be 1–4")
    if approved_level == current_level:
        raise ValueError("Use KEEP_CURRENT when the approved level is unchanged")

    student_id = summary["student_id"]
    domain_code = summary["domain_code"]
    cycle_id = summary["cycle_id"]

    domain = conn.execute(
        """SELECT * FROM learning_profile_domains
           WHERE student_id=? AND domain_code=? AND status='CONFIRMED'
           ORDER BY profile_version DESC LIMIT 1""",
        (student_id, domain_code),
    ).fetchone()
    if not domain:
        raise ValueError("No current confirmed domain record")

    new_domain_version = int(float(domain["profile_version"])) + 1
    new_domain_id = f"LPD-{student_id.split('-')[-1]}-{domain_code}-v{new_domain_version}"
    conn.execute("UPDATE learning_profile_domains SET status='SUPERSEDED' WHERE learning_profile_id=?", (domain["learning_profile_id"],))
    conn.execute(
        """INSERT INTO learning_profile_domains
           (learning_profile_id,student_id,school_year,domain_code,status,impact_level,profile_version,valid_until)
           VALUES (?,?,?,?,?,?,?,?)""",
        (new_domain_id, student_id, domain["school_year"], domain_code, "CONFIRMED", approved_level, new_domain_version, domain["valid_until"]),
    )

    profile = conn.execute(
        "SELECT * FROM profiles WHERE student_id=? AND status='APPROVED' ORDER BY version DESC LIMIT 1",
        (student_id,),
    ).fetchone()
    if not profile:
        raise ValueError("No current approved operational profile")
    new_profile_version = int(float(profile["version"])) + 1
    new_profile_id = f"PROF-{student_id.split('-')[-1]}-2026-{new_profile_version}"
    conn.execute("UPDATE profiles SET status='SUPERSEDED' WHERE profile_id=?", (profile["profile_id"],))
    conn.execute(
        """INSERT INTO profiles(profile_id,student_id,school_year,version,status,approved_at,approved_by,supersedes_profile_id,review_reason)
           VALUES (?,?,?,?,?,?,?,?,?)""",
        (new_profile_id, student_id, profile["school_year"], new_profile_version, "APPROVED", approved_at, approved_by, profile["profile_id"], f"SEMESTER_REVIEW_{cycle_id}"),
    )
    old_rules = conn.execute(
        "SELECT * FROM rules WHERE profile_id=? AND rule_status='APPROVED' ORDER BY priority,rule_id",
        (profile["profile_id"],),
    ).fetchall()
    for idx, rule in enumerate(old_rules, 1):
        conn.execute(
            """INSERT INTO rules(rule_id,profile_id,category,subject_scope,condition_code,action_code,value,rule_status,priority)
               VALUES (?,?,?,?,?,?,?,?,?)""",
            (f"RV{new_profile_version}-{student_id.split('-')[-1]}-{idx:02d}", new_profile_id, rule["category"], rule["subject_scope"], rule["condition_code"], rule["action_code"], rule["value"], "APPROVED", rule["priority"]),
        )

    enrollment = conn.execute(
        "SELECT class_id FROM enrollments WHERE student_id=? AND school_year=? AND status='ACTIVE' LIMIT 1",
        (student_id, profile["school_year"]),
    ).fetchone()
    if not enrollment:
        raise ValueError("No active enrollment for student")
    class_id = enrollment["class_id"]
    report = conn.execute(
        "SELECT * FROM class_report_versions WHERE class_id=? AND status='CURRENT' ORDER BY report_id DESC LIMIT 1",
        (class_id,),
    ).fetchone()
    if not report:
        raise ValueError("No current Class Master Report")
    new_report_id = _next_report_id(conn, class_id)
    new_report_version = _next_report_version(report["version"])
    conn.execute("UPDATE class_report_versions SET status='SUPERSEDED' WHERE report_id=?", (report["report_id"],))
    conn.execute(
        """INSERT INTO class_report_versions(report_id,class_id,school_year,version,generated_at,status,supersedes_report_id,change_reason)
           VALUES (?,?,?,?,?,?,?,?)""",
        (new_report_id, class_id, report["school_year"], new_report_version, approved_at, "CURRENT", report["report_id"], f"SEMESTER_REVIEW_{student_id}_{domain_code}_{current_level}_TO_{approved_level}"),
    )

    conn.execute(
        """UPDATE semester_summary SET lrs_review_decision=?, approved_impact_level=?, approved_by=?, approved_at=?
           WHERE summary_id=?""",
        (decision, approved_level, approved_by, approved_at, summary_id),
    )
    conn.execute(
        "INSERT INTO audit_log(occurred_at,username,event_type,resource,outcome,detail) VALUES (?,?,?,?,?,?)",
        (approved_at, audit_username, "LRS_DECISION", "SEMESTER_SUMMARY", "ALLOW", f"{summary_id}: {current_level}->{approved_level}; {new_domain_id}; {new_profile_id}; {new_report_id}"),
    )
    return VersionResult(
        summary_id=summary_id,
        decision=decision,
        domain_id=new_domain_id,
        profile_id=new_profile_id,
        report_id=new_report_id,
    )
