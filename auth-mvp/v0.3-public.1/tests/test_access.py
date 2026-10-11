from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture()
def client(tmp_path: Path):
    app = create_app({
        "DB_PATH": str(tmp_path / "test.sqlite3"),
        "SECRET_KEY": "test-secret",
        "SECURE_COOKIE": False,
        "DEMO_MODE": True,
        "DEMO_PASSWORD": "test-demo-password",
        "RESET_DB": True,
    })
    return TestClient(app)


def login(client, username):
    page = client.get("/login")
    assert page.status_code == 200
    marker = 'name="csrf" value="'
    text = page.text
    token = text.split(marker,1)[1].split('"',1)[0]
    r = client.post("/login", data={"username":username,"password":"test-demo-password","csrf":token}, follow_redirects=False)
    assert r.status_code == 303


def test_unauthenticated_redirects(client):
    r=client.get("/dashboard",follow_redirects=False)
    assert r.status_code == 303 and r.headers["location"].startswith("/login")


def test_student_can_only_view_self(client):
    login(client,"student01")
    assert client.get("/student/STU-0001").status_code == 200
    assert client.get("/student/STU-0002").status_code == 403


def test_member_cannot_view_master(client):
    login(client,"member01")
    assert client.get("/member/resources").status_code == 200
    assert client.get("/class/CLS-2026-7A/master").status_code == 403


def test_subject_teacher_scope(client):
    login(client,"teacher01")
    assert client.get("/class/CLS-2026-7A/subject/MATHEMATICS").status_code == 200
    assert client.get("/class/CLS-2026-7B/subject/MATHEMATICS").status_code == 200
    assert client.get("/class/CLS-2026-7A/subject/GERMAN").status_code == 403
    assert client.get("/class/CLS-2026-7A/master").status_code == 403


def test_subject_profile_excludes_draft_students(client):
    login(client,"teacher01")
    page=client.get("/class/CLS-2026-7A/subject/MATHEMATICS")
    assert "Marco Demo" not in page.text
    assert "Luca Esempio" in page.text


def test_class_teacher_scope(client):
    login(client,"classteacher01")
    assert client.get("/class/CLS-2026-7A/master").status_code == 200
    assert client.get("/class/CLS-2026-7B/master").status_code == 403
    assert client.get("/class/CLS-2026-7A/subject/GERMAN").status_code == 200
    assert client.get("/class/CLS-2026-7A/subject/MATHEMATICS").status_code == 403


def test_operator_can_create_draft_but_not_approve(client):
    login(client,"operator01")
    page=client.get("/operator/drafts")
    assert page.status_code == 200
    token=page.text.split('name="csrf" value="',1)[1].split('"',1)[0]
    r=client.post("/operator/drafts",data={"csrf":token,"student_id":"STU-0002","source_text":"TEST: extra time mentioned without percentage."},follow_redirects=False)
    assert r.status_code == 303
    assert client.get("/lrs/reviews").status_code == 403


def test_lrs_admin_schoolwide(client):
    login(client,"lrsadmin01")
    assert client.get("/lrs/reviews").status_code == 200
    assert client.get("/class/CLS-2026-7A/master").status_code == 200
    assert client.get("/class/CLS-2026-7B/master").status_code == 200


def test_dsm_is_read_only_schoolwide(client):
    login(client,"dsm01")
    assert client.get("/dsm/overview").status_code == 200
    assert client.get("/class/CLS-2026-7A/master").status_code == 200
    assert client.get("/lrs/reviews").status_code == 403
    assert client.get("/operator/drafts").status_code == 403


def test_system_admin_is_not_student_data_admin(client):
    login(client,"admin01")
    assert client.get("/admin/accounts").status_code == 200
    assert client.get("/class/CLS-2026-7A/master").status_code == 403
    assert client.get("/student/STU-0001").status_code == 403


def test_teacher_semester_review_validation(client):
    login(client,"teacher01")
    page=client.get("/semester-review/CLS-2026-7A/MATHEMATICS")
    assert page.status_code == 200
    token=page.text.split('name="csrf" value="',1)[1].split('"',1)[0]
    good=client.post("/semester-review/CLS-2026-7A/MATHEMATICS",data={
        "csrf":token,"student_id":"STU-0002","domain_code":"MATHEMATICS","current_impact_level":"3",
        "q1":"YES","q2":"IMPROVED","suggested_level":"2","evidence_note":"TEST only"
    })
    assert good.status_code == 200
    bad=client.post("/semester-review/CLS-2026-7A/MATHEMATICS",data={
        "csrf":token,"student_id":"STU-0002","domain_code":"MATHEMATICS","current_impact_level":"3",
        "q1":"NO_CHANGE","q2":"IMPROVED","suggested_level":"","evidence_note":""
    })
    assert bad.status_code == 400


def test_teacher_cannot_submit_for_unassigned_subject(client):
    login(client,"teacher01")
    assert client.get("/semester-review/CLS-2026-7A/GERMAN").status_code == 403


def test_health_is_public_but_contains_no_data(client):
    r=client.get("/health")
    assert r.status_code==200
    assert r.json()=={"ok":True,"mode":"fictitious-data-only"}


def test_expired_assignment_is_denied(client):
    import sqlite3
    login(client,"teacher01")
    path=client.app.state.config["DB_PATH"]
    conn=sqlite3.connect(path)
    conn.execute("UPDATE teacher_assignments SET valid_until='2026-09-15' WHERE assignment_id='TAS-0005'")
    conn.commit(); conn.close()
    assert client.get("/class/CLS-2026-7A/subject/MATHEMATICS").status_code == 403


def test_lrs_change_level_creates_version_chain(client):
    import sqlite3
    login(client,"lrsadmin01")
    page=client.get("/lrs/reviews")
    token=page.text.split('name="csrf" value="',1)[1].split('"',1)[0]
    r=client.post("/lrs/reviews/SUM-S1-0002/decision",data={"csrf":token,"decision":"CHANGE_LEVEL","approved_level":"2"},follow_redirects=False)
    assert r.status_code == 303
    path=client.app.state.config["DB_PATH"]
    conn=sqlite3.connect(path); conn.row_factory=sqlite3.Row
    summary=conn.execute("SELECT * FROM semester_summary WHERE summary_id='SUM-S1-0002'").fetchone()
    assert summary["lrs_review_decision"] == "CHANGE_LEVEL" and summary["approved_impact_level"] == 2
    old_domain=conn.execute("SELECT status FROM learning_profile_domains WHERE learning_profile_id='LPD-0002-MATHEMATICS'").fetchone()
    new_domain=conn.execute("SELECT * FROM learning_profile_domains WHERE learning_profile_id='LPD-0002-MATHEMATICS-v2'").fetchone()
    assert old_domain["status"] == "SUPERSEDED"
    assert new_domain["status"] == "CONFIRMED" and new_domain["impact_level"] == 2 and int(new_domain["profile_version"]) == 2
    old_profile=conn.execute("SELECT status FROM profiles WHERE profile_id='PROF-0002-2026-1'").fetchone()
    new_profile=conn.execute("SELECT * FROM profiles WHERE profile_id='PROF-0002-2026-2'").fetchone()
    assert old_profile["status"] == "SUPERSEDED" and new_profile["status"] == "APPROVED"
    copied=conn.execute("SELECT COUNT(*) FROM rules WHERE profile_id='PROF-0002-2026-2' AND rule_status='APPROVED'").fetchone()[0]
    assert copied == 3
    old_report=conn.execute("SELECT status FROM class_report_versions WHERE report_id='CRV-7A-0003'").fetchone()
    new_report=conn.execute("SELECT * FROM class_report_versions WHERE report_id='CRV-7A-0004'").fetchone()
    assert old_report["status"] == "SUPERSEDED"
    assert new_report["status"] == "CURRENT" and new_report["supersedes_report_id"] == "CRV-7A-0003"
    event=conn.execute("SELECT event_type,outcome FROM audit_log WHERE event_type='LRS_DECISION' ORDER BY event_id DESC LIMIT 1").fetchone()
    assert event["outcome"] == "ALLOW"
    conn.close()


def test_lrs_keep_current_does_not_create_versions(client):
    import sqlite3
    login(client,"lrsadmin01")
    page=client.get("/lrs/reviews")
    token=page.text.split('name="csrf" value="',1)[1].split('"',1)[0]
    r=client.post("/lrs/reviews/SUM-S1-0002/decision",data={"csrf":token,"decision":"KEEP_CURRENT","approved_level":""},follow_redirects=False)
    assert r.status_code == 303
    path=client.app.state.config["DB_PATH"]
    conn=sqlite3.connect(path); conn.row_factory=sqlite3.Row
    summary=conn.execute("SELECT * FROM semester_summary WHERE summary_id='SUM-S1-0002'").fetchone()
    assert summary["lrs_review_decision"] == "KEEP_CURRENT" and summary["approved_impact_level"] == 3
    assert conn.execute("SELECT COUNT(*) FROM profiles WHERE student_id='STU-0002'").fetchone()[0] == 1
    assert conn.execute("SELECT COUNT(*) FROM class_report_versions WHERE class_id='CLS-2026-7A'").fetchone()[0] == 1
    conn.close()
