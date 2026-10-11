# Publication notes — v0.3-public.1

This derivative was prepared from the tested DSM-LRS Auth MVP v0.3 for public source review.

Changes are limited to publication/runtime hardening:
- explicit demo-mode gate;
- required externally supplied session secret;
- configurable local demo password;
- no password prefill;
- generated SQLite state removed from source control;
- repository ignore rules;
- Uvicorn factory startup on loopback.

The role/permission matrix, assignment scoping, student self-scope, LRS review/versioning logic and protected-resource authorization rules are unchanged.

Original v0.3 remains immutable Drive evidence.
