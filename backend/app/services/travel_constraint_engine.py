from app.schemas.journey_timeline import JourneyTimeline
from app.schemas.travel_constraint import TimelineConstraint, TransitionConstraint
from app.schemas.traveler_persona import TravelerPersona, TravelStyle
from app.services.daily_load_engine import evaluate_daily_load
from app.services.hotel_feasibility_engine import validate_hotel_placement


LOAD_WEIGHT = {"easy": 0.15, "normal": 0.35, "tight": 0.7, "overload": 1.0, "high": 0.78}


def evaluate_timeline_constraints(timeline: JourneyTimeline | None, persona: TravelerPersona) -> TimelineConstraint | None:
    if timeline is None:
        return None

    daily_constraints = [
        {
            "day_number": day.day_number,
            "city": day.city,
            "stop_count": sum(len(block.stops) for block in day.blocks),
            "pace": day.pace,
            "load": evaluate_daily_load(day, persona),
        }
        for day in timeline.days
    ]
    hotel_constraints = [validate_hotel_placement(day) for day in timeline.days]
    transition_constraints = [_transition_constraint(transition) for transition in timeline.transitions]

    daily_level = _max_load([item["load"].level for item in daily_constraints])
    transition_level = _transition_load(transition_constraints, persona)
    hotel_level = _max_load([item.hotel_distance for item in hotel_constraints])
    walking_level = _walking_load(daily_level, persona)
    fatigue_level = _fatigue_level(daily_level, transition_level, hotel_level, persona)
    feasibility = _timeline_feasibility(daily_level, transition_level, hotel_level, fatigue_level)

    return TimelineConstraint(
        timeline_id=timeline.timeline_id,
        timeline_feasibility=feasibility,
        feasibility_reason=_feasibility_reason(feasibility, daily_level, transition_level, persona),
        walking_load=walking_level,
        transition_load=transition_level,
        daily_density=daily_level,
        hotel_distance=hotel_level,
        estimated_fatigue=fatigue_level,
        daily_constraints=daily_constraints,
        transition_constraints=transition_constraints,
        hotel_constraints=hotel_constraints,
    )


def annotate_timeline_with_constraints(timeline: JourneyTimeline | None, constraint: TimelineConstraint | None) -> JourneyTimeline | None:
    if timeline is None or constraint is None:
        return timeline
    if timeline.days:
        first = timeline.days[0]
        if constraint.feasibility_reason not in first.daily_narrative:
            first.daily_narrative = f"{first.daily_narrative} {constraint.feasibility_reason}"
    if constraint.transition_load in {"tight", "overload"}:
        for transition in timeline.transitions:
            addition = "这段跨城会增加体力消耗，建议抵达后减少额外停留。"
            if addition not in transition.narrative:
                transition.narrative = f"{transition.narrative} {addition}"
    return timeline


def _transition_constraint(transition) -> TransitionConstraint:
    raw_load = transition.transition_load
    level = "tight" if raw_load == "high" else raw_load
    return TransitionConstraint(
        from_city=transition.from_city,
        to_city=transition.to_city,
        estimated_transition_time=transition.estimated_transition_time,
        transition_type=transition.transition_type,
        transition_load=level,
        reason="跨城时间较长。" if level == "tight" else "跨城移动压力正常。",
    )


def _transition_load(transitions: list[TransitionConstraint], persona: TravelerPersona) -> str:
    if not transitions:
        return "easy"
    tight_count = sum(1 for item in transitions if item.transition_load == "tight")
    if persona.persona in {TravelStyle.ELDER, TravelStyle.FAMILY} and tight_count >= 2:
        return "overload"
    if tight_count >= 2 or len(transitions) >= 4:
        return "tight"
    return _max_load([item.transition_load for item in transitions])


def _walking_load(daily_level: str, persona: TravelerPersona) -> str:
    if persona.persona == TravelStyle.ELDER and daily_level in {"normal", "tight"}:
        return "tight"
    if persona.persona == TravelStyle.FAMILY and daily_level == "tight":
        return "tight"
    return daily_level


def _fatigue_level(daily_level: str, transition_level: str, hotel_level: str, persona: TravelerPersona) -> str:
    score = max(LOAD_WEIGHT.get(daily_level, 0.35), LOAD_WEIGHT.get(transition_level, 0.35), LOAD_WEIGHT.get(hotel_level, 0.35))
    if persona.persona == TravelStyle.ELDER:
        score += 0.18
    elif persona.persona == TravelStyle.FAMILY:
        score += 0.08
    return _level_for_score(score)


def _timeline_feasibility(daily_level: str, transition_level: str, hotel_level: str, fatigue_level: str) -> str:
    worst = _max_load([daily_level, transition_level, hotel_level, fatigue_level])
    return {
        "easy": "easy",
        "normal": "balanced",
        "tight": "tight",
        "overload": "overloaded",
    }.get(worst, "balanced")


def _feasibility_reason(feasibility: str, daily_level: str, transition_level: str, persona: TravelerPersona) -> str:
    if feasibility == "overloaded":
        return "这条路线对当前旅行者偏过载，体力压力较高，建议减少停留点或拆成更多天。"
    if feasibility == "tight":
        if transition_level in {"tight", "overload"}:
            return "这条路线跨城较多，建议把移动日安排得更轻松。"
        return "这条路线节奏偏紧，建议预留休息时间。"
    if feasibility == "easy":
        return "这条路线适合慢节奏体验。"
    if persona.persona == TravelStyle.ELDER:
        return "这条路线已按慢节奏控制体力消耗。"
    return "这条路线整体节奏均衡。"


def _max_load(levels: list[str]) -> str:
    if not levels:
        return "easy"
    order = {"easy": 0, "normal": 1, "tight": 2, "overload": 3}
    return max(levels, key=lambda level: order.get(level, 1))


def _level_for_score(score: float) -> str:
    if score >= 0.92:
        return "overload"
    if score >= 0.68:
        return "tight"
    if score <= 0.34:
        return "easy"
    return "normal"
