$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$FrontendDir = Join-Path $ProjectRoot "frontend"
$BackendDir = Join-Path $ProjectRoot "backend"
$VenvPython = Join-Path $BackendDir ".venv\Scripts\python.exe"

Write-Host "Checking frontend manifest..."
if (-not (Test-Path (Join-Path $FrontendDir "package.json"))) {
  throw "Missing frontend/package.json"
}

if (Test-Path (Join-Path $FrontendDir "node_modules")) {
  Push-Location $FrontendDir
  try {
    npm.cmd run check
  }
  finally {
    Pop-Location
  }
}
else {
  Write-Host "Skipping npm check because frontend/node_modules does not exist. Run npm install first."
}

Write-Host "Checking backend FastAPI app import..."
Push-Location $BackendDir
try {
  if (Test-Path $VenvPython) {
    & $VenvPython -B -c "from app.main import app; print(app.title)"
  }
  else {
    python -B -c "from app.main import app; print(app.title)"
  }
}
finally {
  Pop-Location
}

Write-Host "Round 0 checks completed."
