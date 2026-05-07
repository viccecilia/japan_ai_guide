# Japan AI Guide Technical Blueprint

This document records the intended technical direction for Round 0. It is a blueprint, not a production architecture.

## Round 0 Goal

Create a minimal runnable foundation:

- Frontend: Next.js, React, Tailwind CSS
- Backend: FastAPI
- Scripts: local development and basic checks
- Docs: product blueprint, HTML reference, and technical direction

No real business capability is implemented in Round 0.

## Frontend Direction

Recommended stack:

| Area | Technology |
| --- | --- |
| Framework | Next.js |
| UI runtime | React |
| Styling | Tailwind CSS |
| Animation, later | Framer Motion |
| Maps, later | Google Maps or Mapbox |

Round 0 frontend responsibilities:

- Render the product name and core single-page layout.
- Provide a non-functional AI input placeholder.
- Provide quick question button placeholders.
- Provide left-side history and language switch placeholders.
- Avoid calling backend or AI services.

## Backend Direction

Recommended stack:

| Area | Technology |
| --- | --- |
| API | FastAPI |
| Database, later | PostgreSQL |
| Cache/queue, later | Redis |
| Vector search, later | pgvector |
| File storage, later | S3 or Cloudflare R2 |

Round 0 backend responsibilities:

- Expose a FastAPI app.
- Provide `GET /health`.
- Keep database, cache, AI provider, auth, and storage out of scope.

## AI Direction

Potential future components:

| Area | Candidate |
| --- | --- |
| Chat and guide generation | GPT or DeepSeek |
| Translation | GPT |
| TTS | OpenAI Voice or ElevenLabs |
| Retrieval | RAG |
| Embeddings | text-embedding model |

Round 0 does not call any AI provider.

## Data And Runtime Directories

- `data/`: local seed data, mock data, or future import files.
- `runtime/`: local runtime output such as logs, temporary files, or generated artifacts.

These directories are intentionally empty in Round 0 except for placeholder files.

## Development Defaults

- Frontend local port: `3000`
- Backend local port: `8000`
- Backend health endpoint: `/health`
- Preferred shell: PowerShell on Windows
