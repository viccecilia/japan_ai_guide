# Recommendation Orchestrator

JAG-R014 adds an orchestration layer after ranking. Ranking answers "which content is relevant"; orchestration answers "how should the product present it".

## Flow

```text
query
  -> intent
  -> top-k candidates
  -> recommendation orchestrator
  -> related cards
  -> ordered recommendation sections
```

## Intent To Section Order

| Intent | Strategy | Section order |
| --- | --- | --- |
| city_query | city_query_default | recommended_spots, recommended_routes, recommended_foods, recommended_culture, recommended_hotels |
| route_query | route_query_default | recommended_spots, recommended_foods, recommended_hotels, recommended_culture |
| spot_query | spot_query_default | nearby_spots, recommended_foods, recommended_routes, recommended_culture |
| food_query | food_query_default | recommended_foods, nearby_spots, recommended_routes |
| culture_query | culture_query_default | recommended_culture, related_spots, recommended_routes |
| hotel_query | hotel_query_default | recommended_hotels, nearby_spots, recommended_routes |
| generic_query | generic_query_fallback | suggested_prompts |

## Related Cards Vs Sections

Related cards are direct neighbors to the main card. Sections are product-level recommendation groups ordered by intent.

## Dedupe Rules

- Main card slug is excluded from related cards.
- Related cards are unique by slug.
- Sections are unique by slug.
- Related cards and sections do not intentionally duplicate the same slug.
- Empty card sections are not returned.

## Suggested Prompts

Generic fallback returns `suggested_prompts` instead of unrelated recommendations:

- 京都第一次怎么玩？
- 清水寺有什么故事？
- 大阪一日游怎么安排？
- 神社和寺庙有什么区别？

## Metadata

```json
{
  "orchestration": {
    "strategy": "city_query_default",
    "section_order": ["recommended_spots", "recommended_routes", "recommended_foods"],
    "deduped_count": 2,
    "reason": "city query prioritizes spots and routes"
  }
}
```

## Future AI Rerank

Future AI rerank or personalization should modify ranking scores or section plans, but keep the same `main_card`, `related_cards`, `sections`, and `metadata.orchestration` protocol.
