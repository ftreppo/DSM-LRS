# DSM-LRS Authenticated MVP v0.3-public.1

**EXPERIMENTAL · LOCAL DEMO · FICTITIOUS DATA ONLY · NOT FOR PRODUCTION**

Public-safe derivative of the DSM-LRS Auth MVP v0.3. It preserves the tested server-side authorization model while separating local-demo configuration and generated runtime state from reusable source code.

## Security/publication hardening

Compared with the original local prototype:

- no fallback session secret is embedded; `DSM_LRS_SECRET_KEY` is required;
- fictitious seed data is created only when `DSM_LRS_DEMO_MODE=1`;
- the demo password is supplied through `DSM_LRS_DEMO_PASSWORD`;
- the login form does not prefill a password;
- generated SQLite databases are excluded from version control;
- the application is run as a Uvicorn factory and the demo scripts bind to `127.0.0.1`;
- `.env`, SQLite and runtime artifacts are ignored by Git.

These changes do not broaden authorization or data access.

## What the prototype demonstrates

- signed cookie session;
- PBKDF2 password hashes for local fictitious accounts;
- deny-by-default role/permission matrix;
- class/subject scoping from teacher assignments;
- student self-scope;
- system-admin separation from student-content access;
- server-side filtering of approved profiles/rules;
- Class Master Report access checks;
- Semester Review flow;
- operator DRAFT creation without approval rights;
- audit log for login, access-denied and selected write actions;
- CSRF token on state-changing forms;
- assignment validity dates;
- atomic LRS review/version transition.

## Demo personas

The seed contains fictitious personas such as Member, Student, Subject Teacher, Class Teacher, Operator, LRS Admin, DSM Coordinator and System Admin. No real identities or student data are included.

## Run locally

Create a local demo password and start the loopback-only demo:

```bash
export DSM_LRS_DEMO_PASSWORD='choose-your-local-demo-password'
./run_demo.sh
```

The script sets `DSM_LRS_DEMO_MODE=1` and generates an ephemeral session secret if `DSM_LRS_SECRET_KEY` is not already defined. The SQLite database is created locally under `data/` and is ignored by Git.

For HTTPS or any non-local environment, do **not** use this demo configuration. This repository does not authorize a real protected deployment.

## Tests

```bash
pytest -q
```

The regression suite verifies 16 authorization/versioning scenarios, including the rule that technical system administration does not automatically grant access to student content.

## Important limits

Before any real-data or operational use, identity, hosting, session policy, audit retention, authorization governance, privacy and source freshness must pass their separate project gates. This derivative is source for review and local synthetic testing only.
