from copy import deepcopy

from app.schemas.journey_timeline import JourneyTimeline
from app.schemas.traveler_persona import TravelerPersona, TravelStyle


def auto_balance_timeline(timeline: JourneyTimeline, persona: TravelerPersona) -> tuple[JourneyTimeline, list[str], int]:
    optimized = deepcopy(timeline)
    removed_stops: list[str] = []
    transition_reduction = 0

    target_per_day = _target_stop_count(persona)
    for day in optimized.days:
        day.pace = "slow" if persona.persona in {TravelStyle.ELDER, TravelStyle.FAMILY} else "normal"
        for block in day.blocks:
            if len(block.stops) > target_per_day:
                removed_stops.extend(stop.title for stop in block.stops[target_per_day:])
                block.stops = block.stops[:target_per_day]
            if block.narrative:
                block.narrative = f"{block.narrative} 已按体力负担减少赶场。"
        day.daily_narrative = f"{day.daily_narrative} 已重新平衡这一天的停留密度，保留核心体验并增加休息余地。"

    if len(optimized.transitions) >= 4:
        original_count = len(optimized.transitions)
        optimized.transitions = optimized.transitions[:1]
        transition_reduction = original_count - len(optimized.transitions)
        optimized.cities = list(dict.fromkeys([day.city for day in optimized.days]))

    optimized.timeline_id = f"{optimized.timeline_id}-balanced"
    optimized.title = f"{optimized.title} · 已优化"
    return optimized, removed_stops, transition_reduction


def _target_stop_count(persona: TravelerPersona) -> int:
    if persona.persona == TravelStyle.ELDER:
        return 1
    if persona.persona == TravelStyle.FAMILY:
        return 2
    return 2
