# JAG-R019 Journey Interaction Architecture

## Goal

R019 upgrades the travel flow from a static personalized itinerary into an editable journey prototype.

```text
AI itinerary
-> journey state
-> user interaction
-> edited itinerary
-> replay + analytics
```

## Editable Itinerary

The backend defines:

- `EditableItinerary`
- `EditableStop`
- `JourneyState`
- `JourneyInteraction`

The current implementation stores journey state in memory only.

## Supported Interactions

- persona_switch
- pace_switch
- stop_remove
- stop_replace
- journey_regenerate

## Session State

`journey_session_store.py` keeps:

- session_id
- current itinerary
- persona
- pace
- edited stops
- interaction history

This is intentionally not persistent. No PostgreSQL, Redis, account system, or real user memory is connected.

## Frontend Flow

`ItineraryFlowView.tsx` provides lightweight controls:

- persona switcher
- pace switcher
- remove stop
- replace stop
- regenerate route

The frontend interaction is local mock state in this round.

## Future AI Co-Planning

Future rounds can send interactions to backend APIs, persist journey state, and let AI rewrite route narrative after each edit.

## Future Persistent Memory

Future memory should store explicit traveler choices only. Do not infer sensitive traits or over-personalize from one query.
