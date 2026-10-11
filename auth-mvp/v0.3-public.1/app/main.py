from __future__ import annotations

import os
import secrets
import sqlite3
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from .authz import authorize, load_user
from .db import connect, initialize
from .security import User, verify_password
from .versioning import apply_lrs_decision

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(BASE_DIR / "templates"))


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def create_app(test_config: dict[str, Any] | None = None) -> FastAPI:
    app = FastAPI(title="DSM-LRS Auth MVP", docs_url=None, redoc_url=None)
    config = {
        "DB_PATH": os.getenv("DSM_LRS_DB_PATH", str(BASE_DIR.parent / "data" / "dsm_lrs_demo.sqlite3")),
        "SECRET_KEY": os.getenv("DSM_LRS_SECRET_KEY"),
        "SECURE_COOKIE": os.getenv("DSM_LRS_SECURE_COOKIE", "0") == "1",
        "DEMO_MODE": os.getenv("DSM_LRS_DEMO_MODE", "0") == "1",
        "DEMO_PASSWORD": os.getenv("DSM_LRS_DEMO_PASSWORD"),
        "RESET_DB": False,
    }
    if test_config:
        config.update(test_config)
    if not config.get("SECRET_KEY"):
        raise RuntimeError("DSM_LRS_SECRET_KEY is required; no fallback secret is provided")
    app.state.config = config
    initialize(
        config["DB_PATH"],
        reset=bool(config.get("RESET_DB")),
        seed_demo=bool(config.get("DEMO_MODE")),
        demo_password=config.get("DEMO_PASSWORD"),
    )
    app.add_middleware(
        SessionMiddleware,
        secret_key=config["SECRET_KEY"],
        https_only=bool(config["SECURE_COOKIE"]),
        same_site="lax",
        session_cookie="dsm_lrs_session",
        max_age=60 * 60 * 8,
    )
    app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

    def db() -> sqlite3.Connection:
        return connect(app.state.config["DB_PATH"])

    def audit(username: str | None, event_type: str, resource: str | None, outcome: str, detail: str = "") -> None:
        conn = db()
        try:
            conn.execute(
                "INSERT INTO audit_log(occurred_at,username,event_type,resource,outcome,detail) VALUES (?,?,?,?,?,?)",
                (now_iso(), username, event_type, resource, outcome, detail),
            )
            conn.commit()
        finally:
            conn.close()

    def csrf_token(request: Request) -> str:
        token = request.session.get("csrf")
        if not token:
            token = secrets.token_urlsafe(24)
            request.session["csrf"] = token
        return token

    def check_csrf(request: Request, submitted: str) -> None:
        expected = request.session.get("csrf")
        if not expected or not secrets.compare_digest(expected, submitted):
            raise HTTPException(status_code=400, detail="Invalid CSRF token")

    def current_user(request: Request) -> User | None:
        username = request.session.get("username")
        if not username:
            return None
        conn = db()
        try:
            return load_user(conn, username)
        finally:
            conn.close()

    def require_user(request: Request) -> User:
        user = current_user(request)
        if not user:
            raise HTTPException(status_code=401, detail="Authentication required")
        return user

    def require_permission(request: Request, resource: str, action: str, **scope: Any) -> User:
        user = require_user(request)
        conn = db()
        try:
            ok = authorize(conn, user, resource, action, **scope)
        finally:
            conn.close()
        if not ok:
            audit(user.username, "ACCESS_DENIED", resource, "DENY", str(scope))
            raise HTTPException(status_code=403, detail="Not authorized")
        return user

    def render(request: Request, template: str, **ctx: Any):
        ctx.setdefault("request", request)
        ctx.setdefault("user", current_user(request))
        ctx.setdefault("csrf_token", csrf_token(request))
        return TEMPLATES.TemplateResponse(request=request, name=template, context=ctx)

    @app.exception_handler(401)
    async def unauthorized_handler(request: Request, exc: HTTPException):
        return RedirectResponse(url=f"/login?next={request.url.path}", status_code=303)

    @app.exception_handler(403)
    async def forbidden_handler(request: Request, exc: HTTPException):
        response = render(request, "forbidden.html", message="Questa persona demo non è autorizzata a questa vista.")
        response.status_code = 403
        return response

    @app.get("/", response_class=HTMLResponse)
    def root(request: Request):
        return RedirectResponse("/dashboard" if current_user(request) else "/login", status_code=303)

    @app.get("/login", response_class=HTMLResponse)
    def login_form(request: Request):
        if current_user(request):
            return RedirectResponse("/dashboard", status_code=303)
        conn = db()
        try:
            accounts = conn.execute("SELECT username,display_name,primary_role FROM accounts WHERE status='ACTIVE' ORDER BY account_id").fetchall()
        finally:
            conn.close()
        return render(request, "login.html", accounts=accounts)

    @app.post("/login")
    def login(request: Request, username: str = Form(...), password: str = Form(...), csrf: str = Form(...)):
        check_csrf(request, csrf)
        conn = db()
        try:
            row = conn.execute("SELECT username,password_hash,status FROM accounts WHERE username=?", (username.strip(),)).fetchone()
        finally:
            conn.close()
        if not row or row["status"] != "ACTIVE" or not verify_password(password, row["password_hash"]):
            audit(username.strip() or None, "LOGIN", None, "DENY", "Invalid credentials")
            response = render(request, "login.html", accounts=[], error="Credenziali demo non valide.")
            response.status_code = 401
            return response
        request.session.clear()
        request.session["username"] = row["username"]
        request.session["csrf"] = secrets.token_urlsafe(24)
        audit(row["username"], "LOGIN", None, "ALLOW")
        return RedirectResponse("/dashboard", status_code=303)

    @app.post("/logout")
    def logout(request: Request, csrf: str = Form(...)):
        check_csrf(request, csrf)
        username = request.session.get("username")
        request.session.clear()
        audit(username, "LOGOUT", None, "ALLOW")
        return RedirectResponse("/login", status_code=303)

    @app.get("/dashboard", response_class=HTMLResponse)
    def dashboard(request: Request):
        user = require_user(request)
        conn = db()
        try:
            counts = {
                "students": conn.execute("SELECT COUNT(*) FROM students WHERE active=1").fetchone()[0],
                "classes": conn.execute("SELECT COUNT(DISTINCT class_id) FROM enrollments WHERE status='ACTIVE'").fetchone()[0],
                "accounts": conn.execute("SELECT COUNT(*) FROM accounts WHERE status='ACTIVE'").fetchone()[0],
            }
            assignments = []
            if user.linked_teacher_id:
                today = date.today().isoformat()
                assignments = conn.execute(
                    """SELECT class_id,subject_id,assignment_role FROM teacher_assignments
                       WHERE teacher_id=? AND status='ACTIVE' AND valid_from<=? AND valid_until>=?
                       ORDER BY class_id,subject_id""",
                    (user.linked_teacher_id, today, today),
                ).fetchall()
        finally:
            conn.close()
        return render(request, "dashboard.html", counts=counts, assignments=assignments)

    @app.get("/member/resources", response_class=HTMLResponse)
    def member_resources(request: Request):
        user = require_permission(request, "MEMBER_HOME", "READ")
        return render(request, "simple.html", title="Area Member", subtitle="Risorse interne generali senza dati studente.", rows=[("Linee guida LRS","READ"),("FAQ progetto","READ"),("Class Master Report","DENY")])

    @app.get("/student/{student_id}", response_class=HTMLResponse)
    def student_profile(request: Request, student_id: str):
        user = require_permission(request, "OWN_PROFILE", "READ", student_id=student_id)
        conn = db()
        try:
            student = conn.execute("SELECT * FROM students WHERE student_id=?", (student_id,)).fetchone()
            profile = conn.execute(
                "SELECT * FROM profiles WHERE student_id=? AND status='APPROVED' ORDER BY version DESC LIMIT 1", (student_id,)
            ).fetchone()
            domains = conn.execute(
                "SELECT domain_code,status,impact_level FROM learning_profile_domains WHERE student_id=? AND status IN ('CONFIRMED','NOT_APPLICABLE') ORDER BY domain_code", (student_id,)
            ).fetchall()
            rules = []
            if profile:
                rules = conn.execute("SELECT * FROM rules WHERE profile_id=? AND rule_status='APPROVED' ORDER BY priority", (profile["profile_id"],)).fetchall()
        finally:
            conn.close()
        if not student:
            raise HTTPException(404)
        return render(request, "student.html", student=student, profile=profile, domains=domains, rules=rules)

    @app.get("/class/{class_id}/subject/{subject_id}", response_class=HTMLResponse)
    def class_subject(request: Request, class_id: str, subject_id: str):
        user = require_permission(request, "CLASS_SUBJECT_PROFILE", "READ", class_id=class_id, subject_id=subject_id)
        conn = db()
        try:
            rows = conn.execute(
                """SELECT s.student_id,s.display_name,p.profile_id,p.version
                   FROM enrollments e JOIN students s ON s.student_id=e.student_id
                   JOIN profiles p ON p.student_id=s.student_id AND p.status='APPROVED'
                   WHERE e.class_id=? AND e.status='ACTIVE'
                   ORDER BY s.display_name""", (class_id,)
            ).fetchall()
            output=[]
            for row in rows:
                rules = conn.execute(
                    """SELECT action_code,value,condition_code,subject_scope FROM rules
                       WHERE profile_id=? AND rule_status='APPROVED'
                       AND (subject_scope='ALL' OR subject_scope=?) ORDER BY priority""",
                    (row["profile_id"],subject_id),
                ).fetchall()
                if rules:
                    output.append((row,rules))
        finally:
            conn.close()
        return render(request, "class_subject.html", class_id=class_id, subject_id=subject_id, output=output)

    @app.get("/class/{class_id}/master", response_class=HTMLResponse)
    def class_master(request: Request, class_id: str):
        user = require_permission(request, "CLASS_MASTER_REPORT", "READ", class_id=class_id)
        conn = db()
        try:
            report = conn.execute("SELECT * FROM class_report_versions WHERE class_id=? AND status='CURRENT'", (class_id,)).fetchone()
            students = conn.execute(
                """SELECT s.student_id,s.display_name,pc.email,pc.phone,sr.support_status
                   FROM enrollments e JOIN students s ON s.student_id=e.student_id
                   LEFT JOIN parent_contacts pc ON pc.student_id=s.student_id AND pc.active=1
                   LEFT JOIN support_registry sr ON sr.student_id=s.student_id AND sr.school_year=e.school_year
                   WHERE e.class_id=? AND e.status='ACTIVE' ORDER BY s.display_name""", (class_id,)
            ).fetchall()
            bundle=[]
            for s in students:
                domains=conn.execute(
                    "SELECT domain_code,status,impact_level FROM learning_profile_domains WHERE student_id=? AND status IN ('CONFIRMED','NOT_APPLICABLE','PENDING_REVIEW') ORDER BY domain_code",(s["student_id"],)
                ).fetchall()
                profile=conn.execute("SELECT profile_id,version,status FROM profiles WHERE student_id=? ORDER BY version DESC LIMIT 1",(s["student_id"],)).fetchone()
                bundle.append((s,domains,profile))
        finally:
            conn.close()
        return render(request, "class_master.html", class_id=class_id, report=report, bundle=bundle)

    @app.get("/semester-review/{class_id}/{subject_id}", response_class=HTMLResponse)
    def semester_review_form(request: Request, class_id: str, subject_id: str):
        user = require_permission(request, "SEMESTER_REVIEW", "SUBMIT", class_id=class_id, subject_id=subject_id)
        conn = db()
        try:
            students = conn.execute(
                "SELECT s.student_id,s.display_name FROM enrollments e JOIN students s ON s.student_id=e.student_id WHERE e.class_id=? AND e.status='ACTIVE' ORDER BY s.display_name",(class_id,)
            ).fetchall()
        finally:
            conn.close()
        return render(request,"semester_review.html",class_id=class_id,subject_id=subject_id,students=students,success=None)

    @app.post("/semester-review/{class_id}/{subject_id}", response_class=HTMLResponse)
    def semester_review_submit(
        request: Request,
        class_id: str,
        subject_id: str,
        student_id: str = Form(...),
        domain_code: str = Form(...),
        current_impact_level: int = Form(...),
        q1: str = Form(...),
        q2: str = Form(""),
        suggested_level: str = Form(""),
        evidence_note: str = Form(""),
        csrf: str = Form(...),
    ):
        check_csrf(request, csrf)
        user = require_permission(request, "SEMESTER_REVIEW", "SUBMIT", class_id=class_id, subject_id=subject_id)
        if q1 not in {"NO_CHANGE","YES","INSUFFICIENT_EVIDENCE"}:
            raise HTTPException(400,"Invalid Q1")
        if q1 == "YES" and q2 not in {"IMPROVED","MORE_IMPACT"}:
            raise HTTPException(400,"Q2 required when Q1=YES")
        if q1 != "YES" and q2:
            raise HTTPException(400,"Q2 must be blank unless Q1=YES")
        level = int(suggested_level) if suggested_level else None
        if level is not None and level not in {1,2,3,4}:
            raise HTTPException(400,"Suggested level must be 1–4")
        conn=db()
        try:
            enrolled=conn.execute("SELECT 1 FROM enrollments WHERE student_id=? AND class_id=? AND status='ACTIVE'",(student_id,class_id)).fetchone()
            if not enrolled:
                raise HTTPException(400,"Student not in assigned class")
            conn.execute(
                """INSERT INTO teacher_observations(cycle_id,teacher_id,student_id,class_id,subject_id,domain_code,current_impact_level,q1_change_observed,q2_change_direction,suggested_impact_level,evidence_note,submitted_at)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                ("RC-2026-S1",user.linked_teacher_id,student_id,class_id,subject_id,domain_code,current_impact_level,q1,q2 or None,level,evidence_note,now_iso()),
            )
            conn.commit()
            students=conn.execute("SELECT s.student_id,s.display_name FROM enrollments e JOIN students s ON s.student_id=e.student_id WHERE e.class_id=? AND e.status='ACTIVE' ORDER BY s.display_name",(class_id,)).fetchall()
        finally:
            conn.close()
        audit(user.username,"SEMESTER_REVIEW_SUBMIT","SEMESTER_REVIEW","ALLOW",f"{student_id}/{domain_code}/{q1}/{q2}")
        return render(request,"semester_review.html",class_id=class_id,subject_id=subject_id,students=students,success="Osservazione salvata come evidenza; nessun livello ufficiale è stato modificato.")

    @app.get("/operator/drafts", response_class=HTMLResponse)
    def operator_drafts(request: Request):
        user = require_permission(request,"OPERATOR_CONSOLE","READ_WRITE")
        conn=db()
        try:
            drafts=conn.execute("SELECT * FROM operator_drafts ORDER BY draft_id DESC").fetchall()
        finally: conn.close()
        return render(request,"operator.html",drafts=drafts)

    @app.post("/operator/drafts")
    def operator_create_draft(request: Request, student_id: str = Form(""), source_text: str = Form(...), csrf: str = Form(...)):
        check_csrf(request,csrf)
        user=require_permission(request,"INGESTION_QUEUE","CREATE_EDIT")
        conn=db()
        try:
            conn.execute("INSERT INTO operator_drafts(created_by,student_id,source_text,status,created_at) VALUES (?,?,?,?,?)",(user.username,student_id or None,source_text,"DRAFT",now_iso()))
            conn.commit()
        finally: conn.close()
        audit(user.username,"CREATE_DRAFT","INGESTION_QUEUE","ALLOW")
        return RedirectResponse("/operator/drafts",status_code=303)

    @app.get("/lrs/reviews", response_class=HTMLResponse)
    def lrs_reviews(request: Request):
        user=require_permission(request,"SEMESTER_SUMMARY","READ_APPROVE")
        conn=db()
        try:
            summaries=conn.execute("""SELECT ss.*,s.display_name FROM semester_summary ss JOIN students s ON s.student_id=ss.student_id ORDER BY summary_id""").fetchall()
        finally: conn.close()
        return render(request,"lrs.html",summaries=summaries)

    @app.post("/lrs/reviews/{summary_id}/decision")
    def lrs_decision(
        request: Request,
        summary_id: str,
        decision: str = Form(...),
        approved_level: str = Form(""),
        csrf: str = Form(...),
    ):
        check_csrf(request, csrf)
        user = require_permission(request, "SEMESTER_SUMMARY", "READ_APPROVE")
        level = int(approved_level) if approved_level else None
        conn = db()
        try:
            try:
                apply_lrs_decision(
                    conn,
                    summary_id=summary_id,
                    decision=decision,
                    approved_level=level,
                    approved_by=user.display_name,
                    approved_at=now_iso(),
                    audit_username=user.username,
                )
                conn.commit()
            except ValueError as exc:
                conn.rollback()
                raise HTTPException(status_code=400, detail=str(exc))
        finally:
            conn.close()
        return RedirectResponse("/lrs/reviews", status_code=303)

    @app.get("/dsm/overview", response_class=HTMLResponse)
    def dsm_overview(request: Request):
        user=require_permission(request,"DSM_OVERVIEW","READ")
        conn=db()
        try:
            rows=conn.execute("""SELECT e.class_id,COUNT(*) AS students,SUM(CASE WHEN sr.support_status='CURRENT' THEN 1 ELSE 0 END) AS current_support
                FROM enrollments e LEFT JOIN support_registry sr ON sr.student_id=e.student_id AND sr.school_year=e.school_year
                WHERE e.status='ACTIVE' GROUP BY e.class_id ORDER BY e.class_id""").fetchall()
        finally: conn.close()
        return render(request,"dsm.html",rows=rows)

    @app.get("/admin/accounts", response_class=HTMLResponse)
    def admin_accounts(request: Request):
        user=require_permission(request,"AUTH_TEST_ACCOUNTS","MANAGE")
        conn=db()
        try:
            accounts=conn.execute("SELECT account_id,username,display_name,primary_role,linked_teacher_id,linked_student_id,status FROM accounts ORDER BY account_id").fetchall()
            audit_rows=conn.execute("SELECT occurred_at,username,event_type,resource,outcome FROM audit_log ORDER BY event_id DESC LIMIT 25").fetchall()
        finally: conn.close()
        return render(request,"admin.html",accounts=accounts,audit_rows=audit_rows)

    @app.get("/health")
    def health():
        return {"ok":True,"mode":"fictitious-data-only"}

    return app
