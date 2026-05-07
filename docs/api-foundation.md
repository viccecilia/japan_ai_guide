# JAG-R002 API Foundation

This document describes the first mock API contract for Japan AI Guide.

## Startup

```powershell
cd backend
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Local URL:

```text
http://127.0.0.1:8000
```

## Response Shape

Mock business APIs return a unified response envelope:

```json
{
  "ok": true,
  "data": {},
  "error": null,
  "meta": {
    "mock": true
  }
}
```

Errors use the same structure:

```json
{
  "ok": false,
  "data": null,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed."
  },
  "meta": {
    "path": "/api/chat/query"
  }
}
```

`/health` intentionally keeps the simple health-check response:

```json
{
  "status": "ok",
  "service": "japan-ai-guide"
}
```

## API List

| Method | Path | Purpose | Mock |
| --- | --- | --- | --- |
| GET | `/health` | Health check | No |
| POST | `/api/chat/query` | Return a mock AnswerCard for a user question | Yes |
| POST | `/api/spots/search` | Return mock spot search results | Yes |
| GET | `/api/history/list` | Return mock conversation history | Yes |
| GET | `/api/language/list` | Return supported language options | Yes |

## Mock Business Boundary

JAG-R002 does not connect:

- Real AI provider
- Database
- Search index
- Map provider
- TTS/audio service
- User account or session persistence

The current backend only stabilizes API shape and route organization for later frontend integration.
