# Travel Memory Architecture

## Purpose

JAG-R026 introduces a lightweight travel memory layer for Japan AI Guide. The goal is to let the companion remember a user's travel rhythm and route style across the current runtime, then use that memory to influence itinerary generation, adaptive suggestions, replay, and analytics.

This round remains in-memory only. It does not add real accounts, PostgreSQL, Redis, or persistent user identity.

## Core Flow

```text
query / journey interaction
↓
persona detection
↓
preference learning
↓
travel memory store
↓
memory snapshot
↓
memory-aware itinerary and adaptation
↓
replay + analytics
```

## Schemas

`backend/app/schemas/travel_memory.py` defines:

- `TravelMemory`: session-scoped memory record.
- `PreferenceMemory`: current learned preference state.
- `JourneyPreference`: a single preference signal.
- `MemorySnapshot`: user-facing summary plus current preference state.
- `PreferenceEvolution`: history of preference changes.

## Memory Store

`backend/app/services/travel_memory_store.py` provides:

- `save_memory()`
- `load_memory()`
- `update_memory()`
- `get_memory_snapshot()`

The current implementation uses an in-memory dictionary keyed by `session_id`. Restarting the backend clears memory, which is acceptable for this protocol round.

## Preference Learning

`backend/app/services/preference_learning_engine.py` learns from:

- pace signals such as slow, relaxed, less walking, elder-friendly.
- style signals such as culture, temple, shrine, history, food.
- persona signals from the detected traveler type.
- context signals such as high fatigue or overload.

The learning layer updates:

- `preferred_pace`
- `preferred_persona`
- `preferred_journey_style`
- `walking_tolerance`
- `crowd_tolerance`
- `fatigue_preference`
- preference evolution history

## Memory-Aware Generation

`itinerary_builder.py` now accepts a memory snapshot. When memory says the traveler prefers slow or culture routes, generated travel flow titles, summaries, route type, and style lean in that direction.

`adaptive_journey_engine.py` now accepts memory and can add preference-aware suggestions, for example reducing popular stop density when crowd tolerance is low.

## Replay And Analytics

Response metadata now includes:

```json
{
  "travel_memory": {},
  "analytics": {
    "memory_updates": 3,
    "preference_changes": 4,
    "memory_based_regenerations": 1
  },
  "replay": {
    "preference_evolution": [],
    "memory_adaptation": {}
  }
}
```

These fields are for debug/operator use and future BI. Public UI should only show the companion-style summary, not raw counters or preference internals.

## Future Persistence

The current store can later be replaced by:

- PostgreSQL for durable user memory.
- Redis for hot session memory.
- account sync for authenticated users.
- consent and memory controls for user-managed preference reset.

The existing service boundary is intended to keep builders and UI stable when storage changes.
