# JAG-R021 Journey Persistence API

Base path: `/api/journey`

## POST /api/journey/save

Saves the current active journey session.

```json
{
  "session_id": "r021-storage-session",
  "title": "京都情侣半日保存路线",
  "user_id": null
}
```

## GET /api/journey/saved

Lists saved journeys.

Response data:

```json
[
  {
    "journey_id": "...",
    "session_id": "...",
    "title": "京都情侣半日保存路线",
    "city": "京都",
    "persona": "couple",
    "pace": "normal",
    "updated_at": "..."
  }
]
```

## GET /api/journey/saved/{journey_id}

Restores a saved journey into its active session.

Response data:

```json
{
  "saved_journey": {},
  "restored_session_id": "r021-storage-session",
  "analytics": {
    "journey_restored": true
  },
  "replay": {
    "journey_restored": true
  }
}
```

## DELETE /api/journey/saved/{journey_id}

Deletes a saved journey from the saved list.

```json
{
  "deleted": true,
  "journey_id": "..."
}
```

## Response Contract

Saved journeys include:

- journey_id
- session_id
- future user_id
- title
- city
- persona
- pace
- editable_itinerary
- interaction_history
- analytics
- replay
- created_at
- updated_at
- status

## Boundary

This is a persistence protocol only. It does not use real database storage.
