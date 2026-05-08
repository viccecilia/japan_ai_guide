from collections import defaultdict


JOURNEYS: dict[str, list[dict[str, object]]] = defaultdict(list)


def record_query(
    session_id: str,
    query: str,
    intent: str,
    main_slug: str | None,
    related_slugs: list[str],
    section_types: list[str],
    persona: str | None = None,
) -> dict[str, object]:
    entry = {
        "query": query,
        "intent": intent,
        "main_slug": main_slug,
        "related_slugs": related_slugs,
        "section_types": section_types,
        "persona": persona,
    }
    JOURNEYS[session_id].append(entry)
    return build_journey(session_id)


def build_journey(session_id: str) -> dict[str, object]:
    entries = JOURNEYS.get(session_id, [])
    return {
        "session_id": session_id,
        "query_sequence": [entry["query"] for entry in entries],
        "intent_evolution": [entry["intent"] for entry in entries],
        "persona_evolution": [entry.get("persona") for entry in entries],
        "recommendation_path": [
            {
                "main_slug": entry["main_slug"],
                "related_slugs": entry["related_slugs"],
                "section_types": entry["section_types"],
            }
            for entry in entries
        ],
    }
