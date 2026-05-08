from copy import deepcopy

from app.schemas.adaptive_journey import AdaptationResult
from app.schemas.journey_timeline import JourneyTimeline
from app.schemas.travel_constraint import TimelineConstraint
from app.schemas.travel_context import FatigueContext, JourneyCondition, TimeContext, TravelContext
from app.schemas.traveler_persona import TravelerPersona
from app.services.contextual_narrative_builder import build_contextual_narrative
from app.services.contextual_suggestion_engine import build_contextual_suggestions
from app.services.mock_weather_service import get_mock_weather_context


def build_travel_context(
    query: str,
    timeline: JourneyTimeline | None,
    constraint: TimelineConstraint | None,
    adaptive_journey: AdaptationResult | None,
    persona: TravelerPersona,
) -> TravelContext:
    weather = get_mock_weather_context(query)
    time_context = _time_context(query)
    fatigue = _fatigue_context(timeline, constraint, adaptive_journey)
    condition = _journey_condition(weather.condition, time_context, fatigue, constraint)
    context = TravelContext(weather=weather, time=time_context, fatigue=fatigue, condition=condition)
    context.suggestions = build_contextual_suggestions(context)
    context.narrative = build_contextual_narrative(context)
    context.context_optimized_timeline = _contextual_timeline(timeline, context, persona)
    context.contextual_adaptation_count = len(context.suggestions)
    return context


def _time_context(query: str) -> TimeContext:
    text = query.lower()
    if any(token in text for token in ["很晚", "深夜", "late"]):
        return TimeContext(time_of_day="late", summary="时间已经偏晚，不建议远距离移动。", long_transition_allowed=False)
    if any(token in text for token in ["晚上", "傍晚", "evening"]):
        return TimeContext(time_of_day="evening", summary="晚上更适合就近轻松安排。", long_transition_allowed=False)
    if any(token in text for token in ["下午", "4点", "16点", "16:", "afternoon"]):
        return TimeContext(time_of_day="afternoon", summary="下午后不建议再安排远距离跨城。", long_transition_allowed=False)
    return TimeContext(time_of_day="morning", summary="时间充足，可以按正常节奏推进。", long_transition_allowed=True)


def _fatigue_context(
    timeline: JourneyTimeline | None,
    constraint: TimelineConstraint | None,
    adaptive_journey: AdaptationResult | None,
) -> FatigueContext:
    dense_days = 0
    if timeline:
        dense_days = sum(1 for day in timeline.days if day.pace == "dense" or sum(len(block.stops) for block in day.blocks) >= 5)
    fatigue = constraint.estimated_fatigue if constraint else "normal"
    if adaptive_journey and adaptive_journey.fatigue_reduction == "reduced" and fatigue == "overload":
        fatigue = "high"
    if dense_days >= 3 and fatigue == "normal":
        fatigue = "high"
    return FatigueContext(
        travel_fatigue="high" if fatigue == "tight" else fatigue,
        accumulated_dense_days=dense_days,
        summary="连续密集日较多，建议下一段放慢节奏。" if dense_days >= 3 else "当前体力负担可控。",
    )


def _journey_condition(weather: str, time_context: TimeContext, fatigue: FatigueContext, constraint: TimelineConstraint | None) -> JourneyCondition:
    level = "calm"
    reasons: list[str] = []
    if weather in {"rainy", "hot"}:
        level = "adjust"
        reasons.append("天气需要调整路线。")
    if weather == "crowded":
        level = "watch"
        reasons.append("热门区域可能拥挤。")
    if not time_context.long_transition_allowed:
        level = "adjust"
        reasons.append("当前时间不适合长距离移动。")
    if fatigue.travel_fatigue in {"high", "overload"}:
        level = "urgent" if fatigue.travel_fatigue == "overload" else "adjust"
        reasons.append("旅行疲劳已经累积。")
    density = constraint.daily_density if constraint else "normal"
    return JourneyCondition(
        daily_density=density,
        context_level=level,
        adaptation_reason=" ".join(reasons) if reasons else "当前旅行状态稳定。",
    )


def _contextual_timeline(timeline: JourneyTimeline | None, context: TravelContext, persona: TravelerPersona) -> JourneyTimeline | None:
    if timeline is None:
        return None
    optimized = deepcopy(timeline)
    should_reduce_outdoor = context.weather.condition in {"rainy", "hot", "crowded"}
    should_reduce_fatigue = context.fatigue.travel_fatigue in {"high", "overload"} or persona.preference.walking_tolerance == "low"
    should_reduce_transition = not context.time.long_transition_allowed

    for day in optimized.days:
        for block in day.blocks:
            target = len(block.stops)
            if should_reduce_outdoor or should_reduce_fatigue:
                target = max(1, target - 1)
            block.stops = block.stops[:target]
            if should_reduce_outdoor and block.narrative:
                block.narrative = f"{block.narrative} 已根据天气减少连续户外停留。"
        if should_reduce_fatigue:
            day.pace = "slow"
            day.daily_narrative = f"{day.daily_narrative} 已按当前体力状态放慢节奏。"

    if should_reduce_transition and optimized.transitions:
        optimized.transitions = optimized.transitions[: max(0, len(optimized.transitions) - 1)]
    optimized.timeline_id = f"{optimized.timeline_id}-context"
    optimized.title = f"{optimized.title} · 当前状态优化"
    return optimized
