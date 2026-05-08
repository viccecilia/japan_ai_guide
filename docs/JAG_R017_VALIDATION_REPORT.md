# JAG-R017 Validation Report

## Round

JAG-R017 - Itinerary Flow & Travel Journey Composition

## Required Checks

- Backend compileall: PASS
- Frontend build: PASS
- Frontend lint: PASS
- API itinerary validation: PASS
- Public/debug/operator separation regression: PASS by code path and public browser check

## API Queries

- 京都
- 大阪一日游
- 清水寺

Expected:

- itinerary section exists
- narrative exists
- stop order is stable
- duplicates are removed
- analytics includes itinerary metadata

## API Validation Result

```json
[
  {
    "query": "京都",
    "itinerary_title": "京都经典半日路线",
    "route_type": "half_day",
    "stop_count": 5,
    "duplicates_removed": true,
    "has_narrative": true,
    "analytics_itinerary_generated": true,
    "replay_has_itinerary_flow": true
  },
  {
    "query": "大阪一日游",
    "itinerary_title": "大阪经典一日路线",
    "route_type": "one_day",
    "stop_count": 3,
    "duplicates_removed": true,
    "has_narrative": true,
    "analytics_itinerary_generated": true,
    "replay_has_itinerary_flow": true
  },
  {
    "query": "清水寺",
    "itinerary_title": "京都经典半日路线",
    "route_type": "half_day",
    "stop_count": 4,
    "duplicates_removed": true,
    "has_narrative": true,
    "analytics_itinerary_generated": true,
    "replay_has_itinerary_flow": true
  }
]
```

## Notes

- Uvicorn was run during validation through a short-lived subprocess on `127.0.0.1:8010` and terminated after checks.
- Public mode page was checked in the in-app browser at `http://127.0.0.1:3000/`; no internal debug text was visible on the welcome screen.
- Debug/operator visibility remains controlled by `NEXT_PUBLIC_DEBUG_MODE` and `NEXT_PUBLIC_OPERATOR_MODE`.
