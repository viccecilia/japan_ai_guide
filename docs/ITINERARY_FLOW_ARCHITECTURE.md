# JAG-R017 Itinerary Flow Architecture

## Goal

R017 upgrades Japan AI Guide from answer cards into a travel journey prototype.

Current flow:

```text
query
-> intent
-> recommendation orchestration
-> main card + related cards + sections
-> itinerary builder
-> itinerary section
-> frontend travel flow
```

## Itinerary Flow

The backend creates a `TravelFlow` with one or more `Itinerary` objects.

Each itinerary contains:

- title
- city
- duration
- route_type
- stops
- foods
- culture
- hotel
- blocks
- transport_notes
- estimated_time
- narrative

## Route Composition

R017 does not use a real map. Route composition is heuristic:

- remove duplicate cards
- keep the main card first
- use related cards and section cards as candidate stops
- split stops into morning and afternoon blocks
- insert food and culture content when available
- prefer reasonable pacing over dense lists

## Narrative

`travel_narrative_builder.py` turns stop lists into guide-style copy. The goal is for the user to feel the system is leading a trip, not just listing items.

## Future Map Integration

Future rounds can replace heuristic ordering with:

- geocoded content
- walking/transit travel time
- map APIs
- route optimization

## Future AI Planner

Future AI can rewrite route narrative, adapt pacing, or personalize route type, but R017 keeps all logic template-based and deterministic.

## Future DaDa Bridge

The itinerary flow can later become the bridge into DaDa charter or dispatch workflows, but R017 does not connect DaDa dispatch, payment, booking, or real partner ranking.
