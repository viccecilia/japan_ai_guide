# Dev Server Guide

## Backend Port Policy

JAG-R008 standardizes the backend validation port as `8010`.

Port `8000` may still be occupied by an old FastAPI process from earlier rounds. Do not treat `8000` as the only source of truth for validation in this phase.

## Start Backend

```powershell
cd C:\PycharmProjects\pythonProject01\Japan Guide\japan_ai_guide
python scripts\dev_backend.py --port 8010
```

Equivalent manual command:

```powershell
cd C:\PycharmProjects\pythonProject01\Japan Guide\japan_ai_guide\backend
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8010
```

## Inspect A Port

```powershell
cd C:\PycharmProjects\pythonProject01\Japan Guide\japan_ai_guide
python scripts\kill_backend_port.py --port 8010
```

This only prints PID information. It does not kill anything by default.

## Stop A Confirmed Backend PID

Only after confirming the PID belongs to the local dev backend:

```powershell
python scripts\kill_backend_port.py --port 8010 --kill
```

Manual Windows commands:

```powershell
netstat -ano | Select-String ":8010"
taskkill /PID <PID> /F
```

## Frontend

```powershell
cd C:\PycharmProjects\pythonProject01\Japan Guide\japan_ai_guide\frontend
npm run dev
```

If frontend needs to call `8010`, set:

```powershell
$env:NEXT_PUBLIC_API_BASE_URL="http://127.0.0.1:8010"
npm run dev
```
