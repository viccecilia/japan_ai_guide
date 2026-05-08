# JAG-R020 Stateful Journey Architecture

## Goal

R020 moves itinerary editing from frontend-only local state into a backend Journey Session system.

```text
frontend interaction
-> FastAPI Journey API
-> in-memory journey session
-> editable itinerary response
-> replay
-> analytics
-> updated frontend itinerary
```

## Journey Session

The backend stores each journey by `session_id`.

Current fields:

- current itinerary
- current persona
- current pace
- active stops
- removed stops
- replaced stops
- interaction history

The store is in-memory only. It is intentionally not PostgreSQL or Redis in this round.

## Editable Itinerary API

All mutation endpoints return:

```json
{
  "journey_state": {},
  "editable_itinerary": {},
  "interaction_history": [],
  "analytics": {},
  "replay": {}
}
```

## Replay Evolution

Replay now includes journey interactions in addition to query sequence and persona evolution.

## Future Persistent Memory

Future rounds can persist explicit user edits into PostgreSQL and optionally cache active sessions in Redis.

## Future Account Sync

When a real account system exists, journeys can be saved under a user profile. R020 does not create accounts.

## Current Boundary

No real AI, map API, PostgreSQL, Redis, payment, hotel booking, DaDa dispatch, ads, or user account system is connected.
