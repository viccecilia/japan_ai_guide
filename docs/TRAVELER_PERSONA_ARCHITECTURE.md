# JAG-R018 Traveler Persona Architecture

## Goal

R018 adds a traveler persona layer on top of the itinerary flow.

```text
query
-> persona detector
-> intent router
-> recommendation orchestrator
-> persona-aware itinerary builder
-> personalized travel flow
```

## Supported Persona Types

- first_time
- family
- couple
- elder
- foodie
- culture
- shopping
- anime
- solo

## Pace System

The pace engine supports:

- slow: fewer stops, more rest, lower walking tolerance
- normal: balanced route density
- dense: more stops, tighter timing

## Personalization Boundary

R018 uses deterministic heuristic rules only. It does not use real AI, user accounts, persistent memory, maps, PostgreSQL, Redis, or commercial ranking.

## Metadata

Response analytics now includes:

```json
{
  "persona": "family",
  "pace": "slow",
  "journey_style": "family_light"
}
```

Replay also includes persona evolution so operators can see how the user's journey changes over a conversation.

## Future Memory Integration

Future rounds can persist traveler preferences per session or user account, but public UI should always let users correct assumptions.

## Future AI Adaptation

Future AI can refine persona detection and itinerary writing, but it must not over-personalize or infer sensitive traits.
