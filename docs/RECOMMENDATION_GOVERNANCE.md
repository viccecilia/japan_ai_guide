# Recommendation Governance

JAG-R015 establishes recommendation governance for Japan AI Guide.

## Principle

Commercial weight must never override user relevance.

## Governance Fields

- `partner_weight`: allowed but capped.
- `relevance_score`: primary signal.
- `user_fit_score`: future personalization signal.
- `safety_threshold`: minimum relevance safety boundary.
- `promotion_flag`: marks boosted content.

## Prohibited Behavior

Do not:

- Force unrelated sponsor content.
- Push options above the user's budget.
- Push content that breaks the route context.
- Degrade user experience to maximize partner exposure.
- Hide that a result was promoted once real partner systems exist.

## Current Round

This round only defines the architecture. No real partner ranking, payment, ads, or commercial feed is connected.

## Future Use

Future partner, season, and campaign boosts must be bounded by relevance-first scoring and auditable metadata.
