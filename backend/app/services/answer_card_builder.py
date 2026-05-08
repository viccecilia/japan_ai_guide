from app.mock.mock_answer_cards import get_mock_answer_card
from app.schemas.answer_card import AnswerCard, AnswerCardAction, CardType
from app.schemas.analytics_event import AnalyticsEventType
from app.schemas.content_library import BaseContent
from app.schemas.intent import IntentResult, IntentType
from app.schemas.multi_card_response import MainAnswerCard, MultiCardResponse
from app.schemas.traffic_attribution import TrafficAttribution
from app.services.analytics_service import event_count, recent_events, track_query, track_recommendation
from app.services.adaptive_journey_engine import build_adaptive_journey
from app.services.content_resolver import ResolvedContent, resolve_content
from app.services.conversation_journey_builder import record_query
from app.services.conversation_replay_builder import build_operator_dashboard_snapshot, build_query_replay
from app.services.fallback_copy import get_fallback_copy
from app.services.itinerary_builder import build_travel_flow
from app.services.journey_session_store import save_current_itinerary
from app.services.persona_detector import detect_traveler_persona
from app.services.preference_learning_engine import apply_memory_to_persona, learn_preferences_from_query
from app.services.recommendation_boost_engine import evaluate_governance
from app.services.recommendation_orchestrator import build_recommendation_plan
from app.services.recommendation_section_builder import build_itinerary_section, build_recommendation_sections
from app.services.related_card_builder import build_related_cards
from app.services.timeline_builder import build_journey_timeline
from app.services.token_gate import TokenGateResult
from app.services.travel_constraint_engine import annotate_timeline_with_constraints, evaluate_timeline_constraints
from app.services.travel_context_engine import build_travel_context
from app.services.travel_memory_store import get_memory_snapshot, load_memory, update_memory


def build_answer_card(query: str, intent: IntentResult, token_gate: TokenGateResult) -> AnswerCard:
    return build_multi_card_response(query, intent, token_gate).main_card


def build_multi_card_response(query: str, intent: IntentResult, token_gate: TokenGateResult) -> MultiCardResponse:
    session_id = "jag-local-session"
    memory = load_memory(session_id)
    memory_snapshot = get_memory_snapshot(session_id)
    persona = apply_memory_to_persona(detect_traveler_persona(query), memory)
    resolved = resolve_content(query, intent)
    main_card = _build_main_card(query, intent, token_gate, resolved)
    main_slug = main_card.metadata.content_source.get("slug")
    plan = build_recommendation_plan(
        intent=intent,
        main_slug=main_slug if isinstance(main_slug, str) else None,
        main_content_type=main_card.metadata.ranking.get("content_type") if main_card.metadata.ranking else None,
        candidate_groups=resolved.candidate_groups,
        persona=persona,
    )
    related_cards = build_related_cards(
        main_slug if isinstance(main_slug, str) else None,
        plan.related_candidates,
        intent.language,
        intent.intent_type,
    )
    sections = build_recommendation_sections(plan, intent.language)
    travel_flow = build_travel_flow(query, intent.intent_type.value, main_card, related_cards, sections, persona, memory_snapshot)
    timeline = build_journey_timeline(query, travel_flow, persona)
    timeline_constraint = evaluate_timeline_constraints(timeline, persona)
    timeline = annotate_timeline_with_constraints(timeline, timeline_constraint)
    adaptive_journey = build_adaptive_journey(timeline, timeline_constraint, persona, memory_snapshot)
    travel_context = build_travel_context(query, timeline, timeline_constraint, adaptive_journey, persona)
    memory = learn_preferences_from_query(memory, query, persona, travel_context)
    memory = update_memory(session_id, memory)
    memory_snapshot = get_memory_snapshot(session_id)
    itinerary_section = build_itinerary_section(travel_flow.itineraries if travel_flow else [])
    if itinerary_section is not None:
        sections = [itinerary_section, *sections]
    group_counts = {"main": 1, "related": len(related_cards), "sections": len(sections)}
    orchestration = {
        "strategy": plan.strategy,
        "section_order": plan.section_order,
        "deduped_count": plan.deduped_count,
        "reason": plan.reason,
    }

    related_slugs = [_card_slug(card) for card in related_cards]
    section_types = [section.section_type for section in sections]
    journey = record_query(
        session_id=session_id,
        query=query,
        intent=intent.intent_type.value,
        main_slug=main_slug if isinstance(main_slug, str) else None,
        related_slugs=[slug for slug in related_slugs if slug],
        section_types=section_types,
        persona=persona.persona.value,
    )
    analytics = _track_response_events(
        session_id=session_id,
        query=query,
        intent=intent,
        main_slug=main_slug if isinstance(main_slug, str) else None,
        related_cards=related_cards,
        sections=sections,
        journey=journey,
        travel_flow=travel_flow.model_dump() if travel_flow else None,
        timeline=timeline.model_dump() if timeline else None,
        timeline_constraint=timeline_constraint.model_dump() if timeline_constraint else None,
        adaptive_journey=adaptive_journey.model_dump(),
        travel_context=travel_context.model_dump(),
        memory_snapshot=memory_snapshot.model_dump(),
        memory_updates=memory.memory_updates,
        persona=persona.model_dump(),
    )
    governance = _build_governance_metadata(main_card, related_cards)
    attribution = TrafficAttribution(language=intent.language).model_dump()
    operator = build_operator_dashboard_snapshot(session_id).model_dump()
    replay = build_query_replay(session_id).model_dump()
    if travel_flow is not None:
        replay["itinerary_flow"] = travel_flow.model_dump()
        save_current_itinerary(session_id, travel_flow.itineraries[0])
    if timeline is not None:
        replay["timeline"] = timeline.model_dump()
        replay["timeline_events"] = [
            f"Generated {timeline.total_duration} timeline",
            f"Inserted {len(timeline.hotels)} hotel suggestions",
            f"Created {len(timeline.transitions)} city transitions",
        ]
    if timeline_constraint is not None:
        replay["constraint_changes"] = [
            {
                "timeline_id": timeline_constraint.timeline_id,
                "timeline_feasibility": timeline_constraint.timeline_feasibility,
                "fatigue_level": timeline_constraint.estimated_fatigue,
            }
        ]
        replay["timeline_feasibility_changes"] = [timeline_constraint.timeline_feasibility]
    replay["adaptation_events"] = [adaptation.model_dump() for adaptation in adaptive_journey.adaptations]
    if adaptive_journey.applied:
        replay["timeline_feasibility_changes"] = [
            adaptive_journey.before_feasibility,
            adaptive_journey.after_feasibility,
        ]
    replay["weather_context"] = travel_context.weather.model_dump()
    replay["fatigue_context"] = travel_context.fatigue.model_dump()
    replay["dynamic_adaptation"] = [suggestion.model_dump() for suggestion in travel_context.suggestions]
    replay["preference_evolution"] = [evolution.model_dump() for evolution in memory_snapshot.evolution]
    replay["memory_adaptation"] = memory_snapshot.model_dump()

    main_card.metadata.card_groups = group_counts
    main_card.metadata.orchestration = orchestration
    response_metadata = {
        "intent": intent.model_dump(),
        "cache": main_card.metadata.cache,
        "ranking": main_card.metadata.ranking,
        "content_source": main_card.metadata.content_source,
        "card_groups": group_counts,
        "candidate_groups": resolved.candidate_groups,
        "orchestration": orchestration,
        "analytics": analytics,
        "governance": governance,
        "attribution": attribution,
        "operator": operator,
        "replay": replay,
        "travel_flow": travel_flow.model_dump() if travel_flow else None,
        "timeline": timeline.model_dump() if timeline else None,
        "timeline_constraint": timeline_constraint.model_dump() if timeline_constraint else None,
        "adaptive_journey": adaptive_journey.model_dump(),
        "travel_context": travel_context.model_dump(),
        "travel_memory": memory_snapshot.model_dump(),
        "persona": persona.model_dump(),
    }
    return MultiCardResponse(
        main_card=MainAnswerCard.model_validate(main_card.model_dump()),
        related_cards=related_cards,
        sections=sections,
        metadata=response_metadata,
    )


def _build_main_card(
    query: str,
    intent: IntentResult,
    token_gate: TokenGateResult,
    resolved: ResolvedContent,
) -> AnswerCard:
    if resolved.content is not None:
        card = _build_from_content(resolved.content, _card_type_for_intent(intent.intent_type))
    else:
        card = _build_template_card(query, intent)
        copy = get_fallback_copy(intent.intent_type)
        card.description = _merge_copy(copy["description"], card.description)
        card.story = _merge_copy(copy["story"], card.story)

    card.card_group = "main"
    card.display_priority = 100
    card.display_style = "large"
    card.recommendation_reason = _main_recommendation_reason(intent.intent_type)
    card.metadata.intent = intent
    card.metadata.ai_runtime = token_gate.model_dump()
    card.metadata.language = intent.language
    card.metadata.content_source = resolved.content_source
    card.metadata.cache = resolved.cache
    card.metadata.ranking = resolved.ranking
    card.metadata.related_candidates = resolved.related_candidates
    return card


def _build_template_card(query: str, intent: IntentResult) -> AnswerCard:
    builders = {
        IntentType.SPOT: spot_card_builder,
        IntentType.CITY: city_card_builder,
        IntentType.FOOD: food_card_builder,
        IntentType.ROUTE: route_card_builder,
        IntentType.CULTURE: culture_card_builder,
        IntentType.HOTEL: hotel_card_builder,
        IntentType.GENERIC: generic_card_builder,
        IntentType.UNKNOWN: generic_card_builder,
    }
    return builders.get(intent.intent_type, generic_card_builder)(query, intent)


def _build_from_content(content: BaseContent, card_type: CardType) -> AnswerCard:
    return AnswerCard(
        id=content.id,
        card_type=card_type,
        title=content.title,
        subtitle=content.subtitle,
        description=content.description,
        story=content.story,
        nearby=content.nearby,
        foods=content.foods,
        hotels=content.hotels,
        actions=[
            AnswerCardAction(label="继续追问", action="ask_followup", enabled=True, source="computed"),
            AnswerCardAction(label="生成路线", action="create_route", enabled=True, source="computed"),
            AnswerCardAction(label="收藏到行程", action="save_to_trip", enabled=True, source="computed"),
        ],
    )


def _card_type_for_intent(intent_type: IntentType) -> CardType:
    mapping = {
        IntentType.SPOT: CardType.SPOT,
        IntentType.CITY: CardType.CITY,
        IntentType.FOOD: CardType.FOOD,
        IntentType.ROUTE: CardType.ROUTE,
        IntentType.CULTURE: CardType.CULTURE,
        IntentType.HOTEL: CardType.CITY,
        IntentType.GENERIC: CardType.GENERIC,
        IntentType.UNKNOWN: CardType.GENERIC,
    }
    return mapping.get(intent_type, CardType.GENERIC)


def spot_card_builder(query: str, intent: IntentResult) -> AnswerCard:
    return get_mock_answer_card(intent.entity or query).model_copy(deep=True)


def city_card_builder(query: str, intent: IntentResult) -> AnswerCard:
    return get_mock_answer_card(intent.city or intent.entity or query).model_copy(deep=True)


def food_card_builder(query: str, intent: IntentResult) -> AnswerCard:
    return get_mock_answer_card("京都美食").model_copy(deep=True)


def route_card_builder(query: str, intent: IntentResult) -> AnswerCard:
    return get_mock_answer_card("路线").model_copy(deep=True)


def culture_card_builder(query: str, intent: IntentResult) -> AnswerCard:
    return get_mock_answer_card("神社").model_copy(deep=True)


def hotel_card_builder(query: str, intent: IntentResult) -> AnswerCard:
    card = get_mock_answer_card(intent.city or "京都").model_copy(deep=True)
    card.id = "hotel_template"
    card.card_type = CardType.CITY
    card.title = f"{intent.city or '日本'}住宿建议"
    card.subtitle = "住宿 · 区域选择"
    card.description = "我先按第一次来日本游客的需求，为你整理住宿区域的基础判断方式。"
    card.story = "优先看交通便利度、夜间安全感、行李移动成本和预算，再决定住在车站周边、景点周边或安静街区。"
    card.actions = [AnswerCardAction(label="继续说明预算和人数", action="ask_followup", enabled=True, source="mock")]
    return card


def generic_card_builder(query: str, intent: IntentResult) -> AnswerCard:
    return get_mock_answer_card(query).model_copy(deep=True)


def _merge_copy(prefix: str, body: str) -> str:
    if body.startswith(prefix):
        return body
    return f"{prefix} {body}"


def _main_recommendation_reason(intent_type: IntentType) -> str:
    reasons = {
        IntentType.SPOT: "适合第一次了解这个地点的核心信息。",
        IntentType.CITY: "适合先建立城市旅行的整体判断。",
        IntentType.FOOD: "适合从当地代表性美食开始探索。",
        IntentType.ROUTE: "适合直接作为行程安排的起点。",
        IntentType.CULTURE: "适合在参观前理解文化背景。",
        IntentType.HOTEL: "适合先判断住宿区域和交通便利度。",
        IntentType.GENERIC: "适合先从经典日本旅行方向开始。",
        IntentType.UNKNOWN: "适合先从经典日本旅行方向开始。",
    }
    return reasons.get(intent_type, "适合作为下一步继续探索。")


def _track_response_events(
    session_id: str,
    query: str,
    intent: IntentResult,
    main_slug: str | None,
    related_cards: list[object],
    sections: list[object],
    journey: dict[str, object],
    travel_flow: dict[str, object] | None,
    timeline: dict[str, object] | None,
    timeline_constraint: dict[str, object] | None,
    adaptive_journey: dict[str, object] | None,
    travel_context: dict[str, object] | None,
    memory_snapshot: dict[str, object] | None,
    memory_updates: int,
    persona: dict[str, object],
) -> dict[str, object]:
    track_query(session_id=session_id, query=query, intent=intent.intent_type.value)
    if main_slug:
        track_recommendation(
            session_id=session_id,
            event_type=AnalyticsEventType.CARD_IMPRESSION,
            query=query,
            intent=intent.intent_type.value,
            card_slug=main_slug,
            position=0,
            metadata={"card_group": "main"},
        )
    for position, card in enumerate(related_cards, start=1):
        track_recommendation(
            session_id=session_id,
            event_type=AnalyticsEventType.CARD_IMPRESSION,
            query=query,
            intent=intent.intent_type.value,
            card_slug=_card_slug(card),
            position=position,
            metadata={"card_group": "related"},
        )
    for position, section in enumerate(sections):
        section_type = getattr(section, "section_type", None)
        track_recommendation(
            session_id=session_id,
            event_type=AnalyticsEventType.SECTION_VIEW,
            query=query,
            intent=intent.intent_type.value,
            section_type=section_type,
            position=position,
            metadata={"card_count": len(getattr(section, "cards", [])), "prompt_count": len(getattr(section, "prompts", []))},
        )
    return {
        "session_id": session_id,
        "event_count": event_count(session_id),
        "query_chain": journey["query_sequence"],
        "intent_evolution": journey["intent_evolution"],
        "recommendation_path": journey["recommendation_path"],
        "recent_events": recent_events(session_id, limit=8),
        "recommendation_source": "content_library_or_template",
        "itinerary_generated": travel_flow is not None,
        "itinerary_type": _first_itinerary_field(travel_flow, "route_type"),
        "stop_count": _first_itinerary_stop_count(travel_flow),
        "journey_flow": travel_flow,
        "timeline_days": _timeline_day_count(timeline),
        "city_transition_count": _timeline_transition_count(timeline),
        "hotel_insertions": _timeline_hotel_count(timeline),
        "timeline_regenerations": 0,
        "timeline_feasibility": _constraint_field(timeline_constraint, "timeline_feasibility"),
        "fatigue_level": _constraint_field(timeline_constraint, "estimated_fatigue"),
        "transition_count": _timeline_transition_count(timeline),
        "walking_load": _constraint_field(timeline_constraint, "walking_load"),
        "adaptation_count": _adaptive_field(adaptive_journey, "adaptation_count", 0),
        "feasibility_before": _adaptive_field(adaptive_journey, "before_feasibility", None),
        "feasibility_after": _adaptive_field(adaptive_journey, "after_feasibility", None),
        "fatigue_reduction": _adaptive_field(adaptive_journey, "fatigue_reduction", None),
        "transition_reduction": _adaptive_field(adaptive_journey, "transition_reduction", 0),
        "weather_context": _context_path(travel_context, "weather", "condition"),
        "fatigue_context": _context_path(travel_context, "fatigue", "travel_fatigue"),
        "dynamic_regenerations": 1 if _context_path(travel_context, "context_optimized_timeline", "timeline_id") else 0,
        "contextual_adaptation_count": _context_field(travel_context, "contextual_adaptation_count", 0),
        "memory_updates": memory_updates,
        "preference_changes": _memory_evolution_count(memory_snapshot),
        "memory_based_regenerations": 1 if memory_updates > 1 else 0,
        "persona": persona.get("persona"),
        "pace": _persona_preference_field(persona, "pace"),
        "journey_style": persona.get("journey_style"),
        "interaction_count": 0,
        "interaction_type": None,
        "journey_edit_history": [],
    }


def _timeline_day_count(timeline: dict[str, object] | None) -> int:
    days = timeline.get("days") if timeline else None
    return len(days) if isinstance(days, list) else 0


def _timeline_transition_count(timeline: dict[str, object] | None) -> int:
    transitions = timeline.get("transitions") if timeline else None
    return len(transitions) if isinstance(transitions, list) else 0


def _timeline_hotel_count(timeline: dict[str, object] | None) -> int:
    hotels = timeline.get("hotels") if timeline else None
    return len(hotels) if isinstance(hotels, list) else 0


def _constraint_field(timeline_constraint: dict[str, object] | None, field: str) -> object | None:
    if not timeline_constraint:
        return None
    return timeline_constraint.get(field)


def _adaptive_field(adaptive_journey: dict[str, object] | None, field: str, default: object) -> object:
    if not adaptive_journey:
        return default
    return adaptive_journey.get(field, default)


def _context_field(travel_context: dict[str, object] | None, field: str, default: object) -> object:
    if not travel_context:
        return default
    return travel_context.get(field, default)


def _context_path(travel_context: dict[str, object] | None, section: str, field: str) -> object | None:
    if not travel_context:
        return None
    value = travel_context.get(section)
    if isinstance(value, dict):
        return value.get(field)
    return None


def _memory_evolution_count(memory_snapshot: dict[str, object] | None) -> int:
    if not memory_snapshot:
        return 0
    evolution = memory_snapshot.get("evolution")
    return len(evolution) if isinstance(evolution, list) else 0


def _persona_preference_field(persona: dict[str, object], field: str) -> object | None:
    preference = persona.get("preference")
    return preference.get(field) if isinstance(preference, dict) else None


def _first_itinerary_field(travel_flow: dict[str, object] | None, field: str) -> object | None:
    if not travel_flow:
        return None
    itineraries = travel_flow.get("itineraries")
    if not isinstance(itineraries, list) or not itineraries:
        return None
    first = itineraries[0]
    return first.get(field) if isinstance(first, dict) else None


def _first_itinerary_stop_count(travel_flow: dict[str, object] | None) -> int:
    if not travel_flow:
        return 0
    itineraries = travel_flow.get("itineraries")
    if not isinstance(itineraries, list) or not itineraries:
        return 0
    first = itineraries[0]
    stops = first.get("stops") if isinstance(first, dict) else None
    return len(stops) if isinstance(stops, list) else 0


def _build_governance_metadata(main_card: AnswerCard, related_cards: list[object]) -> dict[str, object]:
    main_relevance = float(main_card.metadata.ranking.get("score") or 0)
    main = evaluate_governance(relevance_score=main_relevance).model_dump()
    related = []
    for card in related_cards:
        ranking = getattr(getattr(card, "metadata", None), "ranking", {})
        related.append(
            {
                "slug": _card_slug(card),
                **evaluate_governance(relevance_score=float(ranking.get("score") or 0)).model_dump(),
            }
        )
    return {
        "principle": "commercial_weight_cannot_override_user_relevance",
        "main": main,
        "related": related,
        "external_jump_tracking": {
            "supported_types": ["hotel_click", "restaurant_click", "booking_jump", "future_dada_jump"],
            "active": False,
        },
    }


def _card_slug(card: object) -> str | None:
    metadata = getattr(card, "metadata", None)
    if metadata is None:
        return None
    content_source = getattr(metadata, "content_source", {})
    slug = content_source.get("slug") if isinstance(content_source, dict) else None
    return slug if isinstance(slug, str) else None
