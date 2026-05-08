# JAG-R016 UX Layer Architecture

## Layer Model

Japan AI Guide now separates the frontend into three modes:

- Public mode: default user experience. Shows AI answers, guide-style narrative, recommendations, and suggested prompts only.
- Debug mode: enabled with `NEXT_PUBLIC_DEBUG_MODE=true`. Shows analytics, ranking, orchestration, cache, and internal metadata.
- Operator mode: enabled with `NEXT_PUBLIC_OPERATOR_MODE=true`. Shows the same internal traces as debug mode and is reserved for future operations screens.

Public mode must never expose session ids, event counts, ranking scores, candidate scores, orchestration strategy, cache keys, or governance internals.

## Recommendation Explanation

User-facing recommendations use `recommendation_reason` instead of technical scores.

Good examples:

- 适合第一次来京都的人。
- 适合直接作为半日或一日路线参考。
- 适合在参观前先理解背景故事。

Forbidden examples in public mode:

- ranking_score=0.75
- matched_by=tag
- cache.hit=true
- orchestration.strategy=city_query_default

## Section Narrative

Recommendation sections now support:

- `section_intro`
- `section_narrative`

These fields let the UI behave more like an AI guide and less like a plain category list.

## Mode Rules

Public mode:

- Shows main card.
- Shows related cards.
- Shows recommendation sections.
- Shows suggested prompts.
- Hides all internal metadata.

Debug mode:

- Shows analytics debug.
- Shows ranking/cache/orchestration.
- Shows governance status.
- Uses the same user UI underneath.

Operator mode:

- Reserved for internal operations.
- Can show analytics, attribution, replay, governance, and recommendation monitoring.
- Must not change recommendation results in this round.

## Current Boundary

R016 does not connect real AI, PostgreSQL, Redis, payment, DaDa dispatch, real ads, or real partner ranking.
