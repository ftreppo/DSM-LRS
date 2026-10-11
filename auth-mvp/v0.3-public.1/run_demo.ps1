$env:PYTHONPATH = $PSScriptRoot
$env:DSM_LRS_DEMO_MODE = "1"
if (-not $env:DSM_LRS_DEMO_PASSWORD) { throw "Set DSM_LRS_DEMO_PASSWORD to a local demo password first" }
if (-not $env:DSM_LRS_SECRET_KEY) {
  $env:DSM_LRS_SECRET_KEY = python -c "import secrets; print(secrets.token_urlsafe(48))"
}
python -m uvicorn app.main:create_app --factory --host 127.0.0.1 --port 8800
