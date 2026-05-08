from app.schemas.travel_context import ContextualSuggestion, TravelContext


def build_contextual_suggestions(context: TravelContext) -> list[ContextualSuggestion]:
    suggestions: list[ContextualSuggestion] = []
    if context.weather.condition == "rainy":
        suggestions.append(
            ContextualSuggestion(
                suggestion_type="weather_indoor",
                title="今天适合减少户外路线",
                description="把连续户外景点压缩，优先保留交通方便、可短暂停留的点。",
                trigger_context="rainy",
                priority=1,
            )
        )
    if context.weather.condition == "hot":
        suggestions.append(
            ContextualSuggestion(
                suggestion_type="weather_heat",
                title="减少下午连续步行",
                description="把步行较多的区域拆开，中午和下午增加休息。",
                trigger_context="hot",
                priority=1,
            )
        )
    if context.weather.condition == "crowded":
        suggestions.append(
            ContextualSuggestion(
                suggestion_type="crowd_avoidance",
                title="避开热门密集 stop",
                description="热门景点不要连续排在同一时间段，避免体验被排队消耗。",
                trigger_context="crowded",
                priority=2,
            )
        )
    if not context.time.long_transition_allowed:
        suggestions.append(
            ContextualSuggestion(
                suggestion_type="time_transition",
                title="减少下午或夜间跨城",
                description="当前时间更适合就近安排，长距离移动建议放到明天上午。",
                trigger_context=context.time.time_of_day,
                priority=1,
            )
        )
    if context.fatigue.travel_fatigue in {"high", "overload"}:
        suggestions.append(
            ContextualSuggestion(
                suggestion_type="fatigue_reduce",
                title="下一段改成轻松节奏",
                description="连续密集日之后建议减少 stop，保留吃饭和休息时间。",
                trigger_context=context.fatigue.travel_fatigue,
                priority=1,
            )
        )
    return suggestions
