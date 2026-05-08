from app.schemas.operator_dashboard_schema import JourneyReplayItem, OperatorDashboardSnapshot
from app.services.conversation_journey_builder import build_journey
from app.services.journey_session_store import get_journey_state


def build_query_replay(session_id: str = "jag-local-session") -> JourneyReplayItem:
    journey = build_journey(session_id)
    state = get_journey_state(session_id)
    return JourneyReplayItem(
        session_id=session_id,
        query_sequence=list(journey.get("query_sequence", [])),
        intent_evolution=list(journey.get("intent_evolution", [])),
        persona_evolution=list(journey.get("persona_evolution", [])),
        interaction_history=[event.model_dump() for event in state.interaction_history],
        recommendation_path=list(journey.get("recommendation_path", [])),
    )


def build_operator_dashboard_snapshot(session_id: str = "jag-local-session") -> OperatorDashboardSnapshot:
    replay = build_query_replay(session_id)
    top_intents: dict[str, int] = {}
    for intent in replay.intent_evolution:
        top_intents[intent] = top_intents.get(intent, 0) + 1

    return OperatorDashboardSnapshot(
        traffic_overview={
            "total_sessions": 1 if replay.query_sequence else 0,
            "top_sources": [{"source": "direct/mock", "sessions": 1 if replay.query_sequence else 0}],
        },
        query_overview={
            "total_queries": len(replay.query_sequence),
            "top_queries": [{"query": query, "count": 1} for query in replay.query_sequence[-5:]],
        },
        top_intents=[{"intent": intent, "count": count} for intent, count in top_intents.items()],
        recommendation_ctr=[
            {"section_type": "recommended_spots", "impressions": 0, "clicks": 0, "ctr": 0.0},
            {"section_type": "suggested_prompts", "impressions": 0, "clicks": 0, "ctr": 0.0},
        ],
        traffic_source=[{"source": "direct/mock", "sessions": 1 if replay.query_sequence else 0}],
        journey_replay=[replay],
        governance_status={
            "relevance_first": True,
            "no_sponsor_override": True,
            "partner_boost_disabled": True,
        },
    )
