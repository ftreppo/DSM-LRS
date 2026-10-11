from __future__ import annotations

import sqlite3
from datetime import date
from typing import Optional

from .security import User


def load_user(conn: sqlite3.Connection, username: str) -> User | None:
    row = conn.execute(
        "SELECT username, display_name, primary_role, linked_teacher_id, linked_student_id FROM accounts WHERE username=? AND status='ACTIVE'",
        (username,),
    ).fetchone()
    if not row:
        return None
    roles = tuple(
        r[0] for r in conn.execute("SELECT role_code FROM account_roles WHERE username=? ORDER BY role_code", (username,)).fetchall()
    )
    return User(
        username=row["username"],
        display_name=row["display_name"],
        primary_role=row["primary_role"],
        roles=roles,
        linked_teacher_id=row["linked_teacher_id"],
        linked_student_id=row["linked_student_id"],
    )


def _matching_permissions(conn: sqlite3.Connection, user: User, resource: str, action: str):
    marks = ",".join("?" for _ in user.roles)
    sql = f"SELECT role_code, scope_rule FROM role_permissions WHERE role_code IN ({marks}) AND resource_code=? AND action=? AND allowed=1"
    return conn.execute(sql, (*user.roles, resource, action)).fetchall()


def _teacher_has_subject_assignment(conn, teacher_id: str | None, class_id: str | None, subject_id: str | None) -> bool:
    if not teacher_id or not class_id or not subject_id:
        return False
    today = date.today().isoformat()
    return conn.execute(
        """SELECT 1 FROM teacher_assignments
           WHERE teacher_id=? AND class_id=? AND subject_id=? AND status='ACTIVE'
           AND valid_from<=? AND valid_until>=? LIMIT 1""",
        (teacher_id, class_id, subject_id, today, today),
    ).fetchone() is not None


def _teacher_has_class_assignment(conn, teacher_id: str | None, class_id: str | None) -> bool:
    if not teacher_id or not class_id:
        return False
    today = date.today().isoformat()
    return conn.execute(
        """SELECT 1 FROM teacher_assignments
           WHERE teacher_id=? AND class_id=? AND assignment_role='CLASS_TEACHER' AND status='ACTIVE'
           AND valid_from<=? AND valid_until>=? LIMIT 1""",
        (teacher_id, class_id, today, today),
    ).fetchone() is not None


def authorize(
    conn: sqlite3.Connection,
    user: User,
    resource: str,
    action: str,
    *,
    class_id: Optional[str] = None,
    subject_id: Optional[str] = None,
    student_id: Optional[str] = None,
) -> bool:
    for perm in _matching_permissions(conn, user, resource, action):
        scope = perm["scope_rule"]
        if scope in {"GENERAL_INTERNAL", "OPERATIONAL_WORKFLOW", "APPROVED_DATA_ONLY", "SCHOOL_WIDE_LRS", "SCHOOL_WIDE_READ_ONLY", "SYSTEM_CONFIGURATION", "SELF"}:
            return True
        if scope == "OWN_STUDENT_ONLY" and student_id and user.linked_student_id == student_id:
            return True
        if scope == "ACTIVE_ASSIGNMENTS_ONLY" and _teacher_has_subject_assignment(conn, user.linked_teacher_id, class_id, subject_id):
            return True
        if scope == "ASSIGNED_CLASS_ONLY" and _teacher_has_class_assignment(conn, user.linked_teacher_id, class_id):
            return True
    return False
