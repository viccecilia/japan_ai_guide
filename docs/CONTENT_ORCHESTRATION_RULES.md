# Content Orchestration Rules

## Main Card

Use the main card for the strongest candidate:

- Exact title match.
- Alias match.
- High-confidence intent match.
- The object that directly answers the user query.

## Related Cards

Use related cards for nearby or adjacent content:

- Same city but different content type.
- Same theme but lower score.
- Useful next step after the main answer.

Avoid duplicates:

- Do not include the main slug again.
- Do not include candidates below the score threshold.
- Do not include generic fallback cards as related cards.

## Recommendation Sections

Sections should group related cards by the job they do:

- Recommended spots for places.
- Recommended routes for planning.
- Recommended foods for eating.
- Recommended culture for explanations.
- Recommended hotels for lodging.

## Generic Query Fallback

For `generic_query`, return a normal main card and leave `related_cards` and `sections` empty. This keeps fallback predictable and avoids unrelated recommendations.

## Future Rules

When real recommendation data exists, section ordering can use user intent, season, location, budget, and saved trip context.
