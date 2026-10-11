#!/usr/bin/env bash
set -euo pipefail
export DSM_LRS_DEMO_MODE=1
: "${DSM_LRS_DEMO_PASSWORD:?Set DSM_LRS_DEMO_PASSWORD to a local demo password first}"
if [[ -z "${DSM_LRS_SECRET_KEY:-}" ]]; then
  export DSM_LRS_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(48))')"
fi
python -m uvicorn app.main:create_app --factory --host 127.0.0.1 --port 8800
