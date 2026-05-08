# JAG-R020 Journey API Reference

Base path: `/api/journey`

## POST /api/journey/create

Creates a journey session from an itinerary.

Payload:

```json
{
  "session_id": "jag-journey-demo",
  "itinerary": {},
  "persona": "family",
  "pace": "normal"
}
```

## POST /api/journey/persona

Switches persona.

```json
{
  "session_id": "jag-journey-demo",
  "persona": "couple"
}
```

## POST /api/journey/pace

Switches pace.

```json
{
  "session_id": "jag-journey-demo",
  "pace": "slow"
}
```

## POST /api/journey/remove-stop

Removes a stop.

```json
{
  "session_id": "jag-journey-demo",
  "stop_title": "伏见稻荷大社"
}
```

## POST /api/journey/replace-stop

Replaces a stop.

```json
{
  "session_id": "jag-journey-demo",
  "stop_title": "祗园",
  "replacement_title": "金阁寺"
}
```

## POST /api/journey/regenerate

Regenerates the route using a template prompt.

```json
{
  "session_id": "jag-journey-demo",
  "prompt": "更轻松一点"
}
```

## GET /api/journey/{session_id}

Returns current journey state.

## Editable Response

```json
{
  "journey_state": {},
  "editable_itinerary": {},
  "interaction_history": [],
  "analytics": {
    "journey_session_id": "jag-journey-demo",
    "interaction_count": 5,
    "regeneration_count": 1,
    "persona_changes": 1,
    "pace_changes": 1
  },
  "replay": {}
}
```

## Interaction Flow

Frontend controls call the Journey API, receive an editable response, and then refresh itinerary UI from backend state.
