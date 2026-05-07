# Japan AI Guide

Japan AI Guide is a ChatGPT-style AI guide platform for travel in Japan.

Round 0 only establishes the project skeleton. It does not implement real AI calls, maps, database storage, authentication, itinerary persistence, booking, or production deployment.

## Product Direction

The first product surface is a simple single-page guide:

- Logo and product identity
- AI question input
- Quick question buttons
- Left-side history placeholder
- Language switch placeholder
- AI answer card area in later rounds

The long-term goal is to let travelers ask natural questions about Japan and receive explanations, routes, food suggestions, nearby spots, hotels, and itinerary actions.

## Project Structure

```text
japan_ai_guide/
├─ README.md
├─ docs/
│  ├─ product-blueprint.md
│  ├─ html-reference.html
│  └─ technical-blueprint.md
├─ frontend/
├─ backend/
├─ data/
├─ runtime/
└─ scripts/
```

## Attachment Archive

The source project materials have been archived in `docs/`:

- `docs/product-blueprint.md`: product background and blueprint from `Japan-Guide.md`
- `docs/html-reference.html`: HTML UI reference from `Japan-Guide.html`
- `docs/technical-blueprint.md`: Round 0 technical direction

## Frontend Quick Start

```powershell
cd japan_ai_guide\frontend
npm install
npm run dev
```

Default local URL:

```text
http://localhost:3000
```

## Backend Quick Start

```powershell
cd japan_ai_guide\backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Health check:

```text
GET http://localhost:8000/health
```

Expected response:

```json
{ "status": "ok", "service": "japan-ai-guide" }
```

## Scripts

From the project root:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\dev_frontend.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\dev_backend.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\check.ps1
```

## Round 0 Scope

In scope:

- Project directory skeleton
- README, product archive, and technical blueprint
- Minimal runnable frontend entry
- Minimal runnable backend entry
- Local development scripts

Out of scope:

- Real AI provider integration
- Database, Redis, pgvector, or object storage setup
- Map provider integration
- TTS/audio generation
- User accounts, saved itineraries, booking, or payments
- Deployment pipeline

## Next Rounds

Recommended next steps:

1. Round 1: stabilize the frontend chat-style UI from the HTML sample.
2. Round 2: add mock AI answer cards and local demo data.
3. Round 3: connect backend API contracts.
4. Round 4: introduce AI provider and route generation.
5. Round 5: add persistence, maps, and itinerary actions.
