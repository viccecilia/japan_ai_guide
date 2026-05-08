# Analytics Architecture

JAG-R015 adds an in-memory growth analytics foundation.

## Event Flow

```text
query submitted
  -> intent detected
  -> main card impression
  -> related card impressions
  -> section views
  -> suggested prompt clicks / external jumps in future
```

## Query Flow

Each `/api/chat/query` response includes:

- `metadata.analytics`
- `metadata.governance`
- `metadata.attribution`

## Tracking Flow

Current events are stored in an in-memory list through `analytics_service.py`.

Tracked event types:

- `query_submitted`
- `card_impression`
- `card_click`
- `section_view`
- `prompt_click`
- `external_jump`
- `conversation_continue`

## Query Journey

`conversation_journey_builder.py` records:

- query sequence
- intent evolution
- recommendation path

## Future PostgreSQL

Move event storage from memory to an append-only events table. Recommended keys:

- `session_id`
- `event_type`
- `timestamp`
- `intent`
- `card_slug`
- `section_type`

## Future Redis

Redis can store short-lived session state, active journey, and event counters.

## Future BI Dashboard

BI can aggregate:

- popular queries
- intent conversion
- suggested prompt clicks
- card CTR
- section engagement
- external jump funnel
