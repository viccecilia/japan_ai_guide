from copy import deepcopy

from app.schemas.editable_itinerary import EditableItinerary, EditableStop, JourneyInteraction, JourneyInteractionType, JourneyState
from app.schemas.itinerary import Itinerary, ItineraryBlock
from app.schemas.journey_api import EditableJourneyResponse, JourneyAnalytics
from app.services.conversation_journey_builder import build_journey
from app.services.journey_interaction_narrative import interaction_narrative


JOURNEY_SESSIONS: dict[str, JourneyState] = {}

REPLACEMENT_POOL = ["金阁寺", "岚山", "祗园", "黑门市场", "梅田蓝天大厦"]


def save_current_itinerary(session_id: str, itinerary: Itinerary) -> JourneyState:
    editable = _to_editable_itinerary(itinerary)
    state = JourneyState(
        session_id=session_id,
        current_itinerary=editable,
        persona=itinerary.persona,
        pace=itinerary.pace,
        edited_stops=[],
        interaction_history=[],
    )
    JOURNEY_SESSIONS[session_id] = state
    return state


def get_journey_state(session_id: str) -> JourneyState:
    return JOURNEY_SESSIONS.get(session_id, JourneyState(session_id=session_id))


def to_journey_response(state: JourneyState) -> EditableJourneyResponse:
    return EditableJourneyResponse(
        journey_state=state,
        editable_itinerary=state.current_itinerary,
        interaction_history=[event.model_dump() for event in state.interaction_history],
        analytics=_analytics_for_state(state),
        replay=_replay_for_state(state),
    )


def switch_persona(session_id: str, persona: str) -> JourneyState:
    state = get_journey_state(session_id)
    state.persona = persona
    if state.current_itinerary:
        state.current_itinerary.current_persona = persona
        state.current_itinerary.itinerary.persona = persona
        state.current_itinerary.itinerary.persona_label = _persona_label(persona)
        state.current_itinerary.itinerary.narrative = f"已调整为{_persona_label(persona)}的路线，停留点和节奏会围绕这个旅行者类型重新组织。"
    return _record(state, JourneyInteractionType.PERSONA_SWITCH, {"to": persona})


def switch_pace(session_id: str, pace: str) -> JourneyState:
    state = get_journey_state(session_id)
    state.pace = pace
    if state.current_itinerary:
        state.current_itinerary.current_pace = pace
        state.current_itinerary.itinerary.pace = pace
        state.current_itinerary.active_stops = _trim_by_pace(state.current_itinerary.active_stops, pace)
        state.current_itinerary.itinerary.stops = state.current_itinerary.active_stops
        state.current_itinerary.itinerary.blocks = _rebuild_blocks(state.current_itinerary.itinerary)
        state.current_itinerary.itinerary.narrative = f"已切换为{_pace_label(pace)}，路线会重新控制停留数量和休息节奏。"
    return _record(state, JourneyInteractionType.PACE_SWITCH, {"to": pace})


def remove_stop(session_id: str, stop_title: str) -> JourneyState:
    state = get_journey_state(session_id)
    if state.current_itinerary:
        kept: list[EditableStop] = []
        for stop in state.current_itinerary.active_stops:
            if stop.title == stop_title:
                state.current_itinerary.removed_stops.append(stop)
            else:
                kept.append(stop)
        state.current_itinerary.active_stops = kept
        state.current_itinerary.itinerary.stops = kept
        state.current_itinerary.itinerary.blocks = _rebuild_blocks(state.current_itinerary.itinerary)
        state.edited_stops.append(stop_title)
    return _record(state, JourneyInteractionType.STOP_REMOVE, {"stop": stop_title})


def replace_stop(session_id: str, old_title: str, new_title: str | None = None) -> JourneyState:
    state = get_journey_state(session_id)
    replacement = new_title or _next_replacement(old_title)
    if state.current_itinerary:
        for stop in state.current_itinerary.active_stops:
            if stop.title == old_title:
                state.current_itinerary.replaced_stops.append({"from": old_title, "to": replacement})
                stop.title = replacement
                stop.replaced_by = replacement
                stop.narrative = f"这里替换成{replacement}，让路线保持新鲜感。"
                break
        state.current_itinerary.itinerary.stops = state.current_itinerary.active_stops
        state.current_itinerary.itinerary.blocks = _rebuild_blocks(state.current_itinerary.itinerary)
        state.edited_stops.append(old_title)
    return _record(state, JourneyInteractionType.STOP_REPLACE, {"from": old_title, "to": replacement})


def regenerate_journey(session_id: str, prompt: str) -> JourneyState:
    state = get_journey_state(session_id)
    if state.current_itinerary:
        if "轻松" in prompt or "少走路" in prompt:
            state = switch_pace(session_id, "slow")
        elif "更多" in prompt or "紧凑" in prompt:
            state = switch_pace(session_id, "dense")
        if state.current_itinerary:
            state.current_itinerary.itinerary.narrative = interaction_narrative(
                JourneyInteractionType.JOURNEY_REGENERATE,
                {"prompt": prompt},
            )
    return _record(state, JourneyInteractionType.JOURNEY_REGENERATE, {"prompt": prompt})


def _to_editable_itinerary(itinerary: Itinerary) -> EditableItinerary:
    cloned = deepcopy(itinerary)
    active = [EditableStop.model_validate(stop.model_dump()) for stop in cloned.stops]
    return EditableItinerary(
        itinerary=cloned,
        current_persona=cloned.persona,
        current_pace=cloned.pace,
        active_stops=active,
    )


def _record(state: JourneyState, interaction_type: JourneyInteractionType, detail: dict[str, str | int | bool | None]) -> JourneyState:
    event = JourneyInteraction(
        interaction_type=interaction_type,
        detail=detail,
        narrative=interaction_narrative(interaction_type, detail),
    )
    state.interaction_history.append(event)
    if state.current_itinerary:
        state.current_itinerary.interaction_history.append(event)
    JOURNEY_SESSIONS[state.session_id] = state
    return state


def _analytics_for_state(state: JourneyState) -> JourneyAnalytics:
    interaction_types = [event.interaction_type for event in state.interaction_history]
    latest = interaction_types[-1].value if interaction_types else None
    return JourneyAnalytics(
        journey_session_id=state.session_id,
        interaction_count=len(interaction_types),
        regeneration_count=sum(1 for item in interaction_types if item == JourneyInteractionType.JOURNEY_REGENERATE),
        persona_changes=sum(1 for item in interaction_types if item == JourneyInteractionType.PERSONA_SWITCH),
        pace_changes=sum(1 for item in interaction_types if item == JourneyInteractionType.PACE_SWITCH),
        latest_interaction_type=latest,
    )


def _replay_for_state(state: JourneyState) -> dict[str, object]:
    journey = build_journey(state.session_id)
    return {
        "session_id": state.session_id,
        "query_sequence": list(journey.get("query_sequence", [])),
        "intent_evolution": list(journey.get("intent_evolution", [])),
        "persona_evolution": list(journey.get("persona_evolution", [])),
        "interaction_history": [event.model_dump() for event in state.interaction_history],
        "final_journey": state.current_itinerary.itinerary.model_dump() if state.current_itinerary else None,
    }


def _trim_by_pace(stops: list[EditableStop], pace: str) -> list[EditableStop]:
    if pace == "slow":
        return stops[:3]
    if pace == "dense":
        return stops[:6]
    return stops[:5]


def _rebuild_blocks(itinerary: Itinerary) -> list[ItineraryBlock]:
    midpoint = max(1, min(2, len(itinerary.stops)))
    first = itinerary.stops[:midpoint]
    second = itinerary.stops[midpoint:]
    blocks = [
        ItineraryBlock(block_title="上午调整后路线", time_of_day="上午", stops=first, narrative="这一段按当前编辑结果重新排列。"),
    ]
    if second:
        blocks.append(ItineraryBlock(block_title="下午继续体验", time_of_day="下午", stops=second, narrative="这一段保留弹性，方便继续调整。"))
    return blocks


def _next_replacement(old_title: str) -> str:
    for title in REPLACEMENT_POOL:
        if title != old_title:
            return title
    return "替代景点"


def _persona_label(persona: str) -> str:
    labels = {
        "family": "适合亲子家庭",
        "couple": "适合情侣散步",
        "elder": "适合带老人慢慢体验",
        "foodie": "适合美食探索",
        "first_time": "适合第一次来日本",
    }
    return labels.get(persona, persona)


def _pace_label(pace: str) -> str:
    return {"slow": "慢节奏", "normal": "标准节奏", "dense": "紧凑节奏"}.get(pace, pace)
