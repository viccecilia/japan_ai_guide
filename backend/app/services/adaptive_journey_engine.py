from app.schemas.adaptive_journey import AdaptationResult, JourneyAdaptation, RegenerationReason
from app.schemas.journey_timeline import JourneyTimeline
from app.schemas.travel_constraint import TimelineConstraint
from app.schemas.travel_memory import MemorySnapshot
from app.schemas.traveler_persona import TravelerPersona
from app.services.adaptive_narrative_builder import adaptation_narrative, adaptation_summary
from app.services.auto_balance_engine import auto_balance_timeline
from app.services.constraint_suggestion_engine import build_constraint_suggestions
from app.services.travel_constraint_engine import annotate_timeline_with_constraints, evaluate_timeline_constraints


def build_adaptive_journey(
    timeline: JourneyTimeline | None,
    constraint: TimelineConstraint | None,
    persona: TravelerPersona,
    memory_snapshot: MemorySnapshot | None = None,
) -> AdaptationResult:
    suggestions = build_constraint_suggestions(constraint)
    if timeline is None or constraint is None:
        return AdaptationResult(suggestions=suggestions, narrative="当前没有可优化的时间轴。")

    before = constraint.timeline_feasibility
    if memory_snapshot and memory_snapshot.preference.crowd_tolerance == "low":
        suggestions.append(
            {
                "adaptation_type": "stop_reduce",
                "title": "降低热门点密度",
                "description": "我会延续你避开拥挤的偏好，减少连续热门景点。",
                "trigger_reason": "memory: low crowd tolerance",
                "priority": 2,
            }
        )

    if before not in {"tight", "overloaded"}:
        return AdaptationResult(
            applied=False,
            before_feasibility=before,
            after_feasibility=before,
            suggestions=suggestions,
            optimized_timeline=timeline,
            optimized_constraint=constraint,
            adaptation_count=0,
            narrative="当前路线已经比较稳定，暂不需要自动减负。",
        )

    optimized_timeline, removed_stops, transition_reduction = auto_balance_timeline(timeline, persona)
    optimized_constraint = evaluate_timeline_constraints(optimized_timeline, persona)
    optimized_timeline = annotate_timeline_with_constraints(optimized_timeline, optimized_constraint)
    after = optimized_constraint.timeline_feasibility if optimized_constraint else before

    adaptations = [
        JourneyAdaptation(
            adaptation_type="auto_balance",
            trigger_reason=constraint.feasibility_reason,
            before_feasibility=before,
            after_feasibility=after,
            removed_stops=removed_stops,
            transition_reduction=transition_reduction,
            fatigue_reduction=_fatigue_reduction(constraint, optimized_constraint),
            narrative=adaptation_narrative("auto_balance"),
        )
    ]
    if removed_stops:
        adaptations.append(
            JourneyAdaptation(
                adaptation_type="stop_reduce",
                trigger_reason="部分日期停留点偏多。",
                before_feasibility=before,
                after_feasibility=after,
                removed_stops=removed_stops,
                fatigue_reduction=_fatigue_reduction(constraint, optimized_constraint),
                narrative=adaptation_narrative("stop_reduce", 1),
            )
        )
    if transition_reduction:
        adaptations.append(
            JourneyAdaptation(
                adaptation_type="transition_reduce",
                trigger_reason="跨城移动较多。",
                before_feasibility=before,
                after_feasibility=after,
                transition_reduction=transition_reduction,
                fatigue_reduction=_fatigue_reduction(constraint, optimized_constraint),
                narrative=adaptation_narrative("transition_reduce"),
            )
        )

    return AdaptationResult(
        applied=True,
        before_feasibility=before,
        after_feasibility=after,
        suggestions=suggestions,
        adaptations=adaptations,
        optimized_timeline=optimized_timeline,
        optimized_constraint=optimized_constraint,
        regeneration_reason=RegenerationReason(
            before_feasibility=before,
            trigger_reason=constraint.feasibility_reason,
            user_facing_reason="已根据体力和跨城负担自动优化路线。",
        ),
        fatigue_reduction=_fatigue_reduction(constraint, optimized_constraint),
        transition_reduction=transition_reduction,
        adaptation_count=len(adaptations),
        narrative=adaptation_summary(before, after, adaptations),
    )


def _fatigue_reduction(before: TimelineConstraint, after: TimelineConstraint | None) -> str:
    if after is None:
        return "unknown"
    order = {"easy": 0, "normal": 1, "tight": 2, "overload": 3}
    before_score = order.get(before.estimated_fatigue, 1)
    after_score = order.get(after.estimated_fatigue, 1)
    if after_score < before_score:
        return "reduced"
    if after_score == before_score:
        return "stable"
    return "increased"
