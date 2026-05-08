# JAG-R016 Operator Console Blueprint

## Purpose

The operator layer gives internal teams visibility into how users discover, query, and continue exploring Japan AI Guide.

## Future Dashboard Areas

### Growth Dashboard

- Traffic overview
- UTM campaign performance
- Landing page performance
- Device and language distribution

### Analytics Dashboard

- Query volume
- Top intents
- Query chains
- Suggested prompt clicks
- Conversation continuation rate

### Recommendation Dashboard

- Recommendation impressions
- Recommendation clicks
- Section CTR
- Related card performance
- Suggested prompt performance

### Partner Analytics

Future-only. R016 only defines governance metadata and does not implement real sponsor ranking.

Rules:

- Relevance remains first.
- Partner boost cannot override poor relevance.
- Sponsor override is forbidden.

### Attribution Center

- `utm_source`
- `utm_campaign`
- `referrer`
- `landing_page`
- `device`
- `language`
- `country`

### Journey Replay

Shows a replayable query chain:

```text
京都
-> 清水寺
-> 京都亲子路线
-> 京都站酒店
```

## Current Mock Backend Structures

R016 adds:

- `OperatorDashboardSnapshot`
- `JourneyReplayItem`
- `build_query_replay()`
- `build_operator_dashboard_snapshot()`

These are in-memory prototypes. They are ready for future PostgreSQL, Redis, and BI dashboard integration, but no persistent storage is connected in this round.
