# Intent Router

Round: JAG-R008

## Intent Types

| intent_type | Meaning |
| --- | --- |
| `spot_query` | User asks about a specific attraction. |
| `city_query` | User asks about a city or destination area. |
| `food_query` | User asks about food, restaurants, or what to eat. |
| `route_query` | User asks for a route, day trip, half-day trip, or itinerary. |
| `culture_query` | User asks about culture, shrines, temples, stories, etiquette, or reasons. |
| `hotel_query` | User asks about hotels, stays, or lodging. |
| `generic_query` | User input is valid but not specific enough. |
| `unknown` | Empty or unusable input. |

## Current Rule-Based Recognition

The first Intent Router is deterministic and low cost:

- `清水寺` / `伏见稻荷` / `大阪城` / `奈良公园` -> `spot_query`
- `京都` / `大阪` / `奈良` / `东京` -> `city_query`
- `美食` / `吃` / `餐厅` / `拉面` / `寿司` -> `food_query`
- `路线` / `一日游` / `半日游` / `怎么玩` -> `route_query`
- `神社` / `寺庙` / `文化` / `传说` / `为什么` -> `culture_query`
- `酒店` / `住宿` / `旅馆` -> `hotel_query`

Priority is currently:

```text
hotel -> food -> route -> culture -> spot -> city -> generic
```

This means `京都美食` becomes `food_query`, not `city_query`.

## Why No AI Yet

This phase needs a stable protocol and predictable costs. A rule-based router:

- is deterministic,
- is easy to test,
- costs no tokens,
- is enough for MVP routing,
- keeps AnswerCard Builder design separate from AI provider selection.

## Relation To AnswerCard

`/api/chat/query` now returns:

```json
{
  "question": "清水寺",
  "intent": {
    "intent_type": "spot_query",
    "entity": "清水寺",
    "city": "京都",
    "language": "zh",
    "confidence": 0.95
  },
  "answer_card": {
    "metadata": {
      "intent": {
        "intent_type": "spot_query",
        "entity": "清水寺",
        "city": "京都",
        "language": "zh",
        "confidence": 0.95
      }
    }
  }
}
```

The frontend can render the AnswerCard normally and show intent debug info in development mode.

## Upgrade Path

Future AI Intent Router can replace `backend/app/services/intent_router.py` while preserving the same `IntentResult` schema.

Recommended path:

1. Keep rule router as a fast first pass.
2. Use AI only when confidence is low or multiple intents conflict.
3. Cache query -> intent result.
4. Feed normalized intent into AnswerCard Builder.
