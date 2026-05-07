$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$BackendDir = Join-Path $ProjectRoot "backend"
$VenvPython = Join-Path $BackendDir ".venv\Scripts\python.exe"

Set-Location $BackendDir
if (Test-Path $VenvPython) {
  & $VenvPython -m uvicorn app.main:app --reload
}
else {
  python -m uvicorn app.main:app --reload
}
