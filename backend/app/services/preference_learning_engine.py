from app.schemas.travel_context import TravelContext
from app.schemas.travel_memory import PreferenceEvolution, TravelMemory
from app.schemas.traveler_persona import TravelerPersona, TravelPace


def learn_preferences_from_query(
    memory: TravelMemory,
    query: str,
    persona: TravelerPersona,
    travel_context: TravelContext | None = None,
) -> TravelMemory:
    text = query.lower()
    _vote(memory.memory.pace_votes, persona.preference.pace.value)
    _vote(memory.memory.persona_votes, persona.persona.value)
    _vote(memory.memory.style_votes, persona.journey_style)

    for city in ["东京", "京都", "大阪", "奈良"]:
        if city in query:
            _vote(memory.memory.city_votes, city)

    if any(token in text for token in ["慢", "少走路", "老人", "轻松", "不赶"]):
        _vote(memory.memory.pace_votes, "slow", weight=2)
    if any(token in text for token in ["文化", "神社", "寺庙", "历史"]):
        _vote(memory.memory.persona_votes, "culture", weight=2)
        _vote(memory.memory.style_votes, "culture_slow", weight=1)
    if any(token in text for token in ["美食", "吃", "餐厅"]):
        _vote(memory.memory.persona_votes, "foodie", weight=2)
    if any(token in text for token in ["人多", "拥挤", "避开热门"]):
        memory.preference.crowd_tolerance = "low"
        _remember_context(memory, "crowded")
    if travel_context and travel_context.fatigue.travel_fatigue in {"high", "overload"}:
        memory.preference.fatigue_preference = "avoid_fatigue"

    _apply_votes(memory)
    return memory


def apply_memory_to_persona(persona: TravelerPersona, memory: TravelMemory) -> TravelerPersona:
    next_persona = persona.model_copy(deep=True)
    if memory.preference.preferred_pace == "slow":
        next_persona.preference.pace = TravelPace.SLOW
        next_persona.preference.walking_tolerance = "low"
    if memory.preference.preferred_persona == "culture":
        next_persona.journey_style = "culture_slow"
        next_persona.preference.culture_interest = max(next_persona.preference.culture_interest, 5)
    if memory.preference.crowd_tolerance == "low":
        next_persona.preference.walking_tolerance = "low"
    return next_persona


def _vote(bucket: dict[str, int], key: str, weight: int = 1) -> None:
    bucket[key] = bucket.get(key, 0) + weight


def _top(bucket: dict[str, int], default: str) -> str:
    if not bucket:
        return default
    return max(bucket.items(), key=lambda item: item[1])[0]


def _apply_votes(memory: TravelMemory) -> None:
    before_pace = memory.preference.preferred_pace
    before_persona = memory.preference.preferred_persona
    before_style = memory.preference.preferred_journey_style
    memory.preference.preferred_pace = _top(memory.memory.pace_votes, memory.preference.preferred_pace)
    memory.preference.preferred_persona = _top(memory.memory.persona_votes, memory.preference.preferred_persona)
    memory.preference.preferred_journey_style = _top(memory.memory.style_votes, memory.preference.preferred_journey_style)
    memory.preference.last_journey_style = memory.preference.preferred_journey_style
    memory.preference.preferred_cities = [_top(memory.memory.city_votes, "")] if memory.memory.city_votes else []
    _track_evolution(memory, "preferred_pace", before_pace, memory.preference.preferred_pace, "learned from repeated route choices")
    _track_evolution(memory, "preferred_persona", before_persona, memory.preference.preferred_persona, "learned from query themes")
    _track_evolution(memory, "preferred_journey_style", before_style, memory.preference.preferred_journey_style, "learned from journey style")


def _track_evolution(memory: TravelMemory, field: str, before: str, after: str, reason: str) -> None:
    if before == after:
        return
    memory.evolution.append(PreferenceEvolution(field=field, before=before, after=after, reason=reason))


def _remember_context(memory: TravelMemory, context: str) -> None:
    if context not in memory.memory.disliked_contexts:
        memory.memory.disliked_contexts.append(context)
