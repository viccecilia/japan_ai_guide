from app.schemas.adaptive_journey import AdaptiveSuggestion
from app.schemas.travel_constraint import TimelineConstraint


def build_constraint_suggestions(constraint: TimelineConstraint | None) -> list[AdaptiveSuggestion]:
    if constraint is None:
        return []

    suggestions: list[AdaptiveSuggestion] = []
    if constraint.timeline_feasibility in {"tight", "overloaded"}:
        suggestions.append(
            AdaptiveSuggestion(
                adaptation_type="auto_balance",
                title="智能平衡路线",
                description="减少过密停留点，并把移动日安排得更轻松。",
                trigger_reason=constraint.feasibility_reason,
                priority=1,
            )
        )
    if constraint.daily_density in {"tight", "overload"}:
        busiest = max(constraint.daily_constraints, key=lambda item: item.stop_count, default=None)
        suggestions.append(
            AdaptiveSuggestion(
                adaptation_type="stop_reduce",
                title="减少当天停留点",
                description=f"建议减少 Day {busiest.day_number if busiest else 1} 的 stop，让体验更稳定。",
                trigger_reason="当天停留点偏多。",
                day_number=busiest.day_number if busiest else None,
                priority=2,
            )
        )
    if constraint.transition_load in {"tight", "overload"}:
        suggestions.append(
            AdaptiveSuggestion(
                adaptation_type="transition_reduce",
                title="减少跨城疲劳",
                description="建议避免连续跨城，把长距离移动日做轻量安排。",
                trigger_reason="跨城移动较多。",
                priority=2,
            )
        )
    if constraint.hotel_distance in {"tight", "overload"}:
        suggestions.append(
            AdaptiveSuggestion(
                adaptation_type="rest_insert",
                title="优化住宿区域",
                description="建议把住宿放在当天城市或交通枢纽附近。",
                trigger_reason="住宿动线可能增加疲劳。",
                priority=3,
            )
        )
    return suggestions
