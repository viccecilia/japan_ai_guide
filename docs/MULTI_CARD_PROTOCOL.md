# Multi-Card Response Protocol

JAG-R013 upgrades chat output from one AnswerCard to an orchestrated response:

```json
{
  "main_card": {},
  "related_cards": [],
  "sections": [],
  "metadata": {}
}
```

The legacy `answer_card` field remains available and points to `main_card`.

## Why Multi-Card

Travel answers are rarely a single object. A city query can need a city overview, nearby spots, food, routes, and hotels. Multi-Card Response Protocol lets the backend turn Top-K candidates into a structured recommendation stream.

## Main Card

The main card is the best ranked candidate for the query. It uses:

- `card_group=main`
- `display_style=large`
- `display_priority=100`

## Related Cards

Related cards are built from remaining Top-K candidates after removing the main card.

Rules:

- Maximum 4 related cards.
- Low score candidates are filtered.
- `generic_query` does not generate related cards.
- Each card keeps its own `content_source` and `ranking` metadata.

## Recommendation Sections

Sections group related cards by content type:

- `recommended_spots`
- `recommended_routes`
- `recommended_foods`
- `recommended_culture`
- `recommended_hotels`

## Top-K To UI Mapping

```text
Top-K[0] -> main_card
Top-K[1..4] -> related_cards
related_cards grouped by content_type -> sections
```

## Display Fields

- `display_priority`: ordering hint for UI orchestration.
- `display_style`: `large` for main card, `compact` for related cards.
- `recommendation_reason`: developer-readable reason such as `tag match · score 0.75`.

## Future Recommendation System

Future ranking can come from PostgreSQL, Redis cache, vector retrieval, behavior signals, or AI reranking. The UI should continue consuming the same `main_card`, `related_cards`, and `sections` shape.
