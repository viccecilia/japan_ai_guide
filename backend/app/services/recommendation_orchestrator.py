from app.schemas.intent import IntentResult, IntentType
from app.schemas.recommendation_orchestration import OrchestrationContext, RecommendationPlan
from app.schemas.traveler_persona import TravelerPersona, TravelStyle
from app.services.recommendation_rules import SECTION_CONTENT_TYPES, SUGGESTED_PROMPTS, get_recommendation_rule


def build_recommendation_plan(
    intent: IntentResult,
    main_slug: str | None,
    main_content_type: str | None,
    candidate_groups: dict[str, list[dict[str, str | float | int | None]]],
    persona: TravelerPersona | None = None,
) -> RecommendationPlan:
    context = OrchestrationContext(
        intent_type=intent.intent_type,
        main_slug=main_slug,
        main_content_type=main_content_type,
        candidate_groups=candidate_groups,
    )
    rule = get_recommendation_rule(intent.intent_type)
    candidate_groups = _personalize_candidate_groups(candidate_groups, persona)

    if intent.intent_type in {IntentType.GENERIC, IntentType.UNKNOWN}:
        return RecommendationPlan(
            intent_type=intent.intent_type,
            strategy=rule.strategy,
            main_content_type=main_content_type,
            section_order=rule.section_order,
            max_cards_per_section=rule.max_cards_per_section,
            dedupe_keys=[main_slug] if main_slug else [],
            reason=rule.reason,
            suggested_prompts=SUGGESTED_PROMPTS,
        )

    used = {main_slug} if main_slug else set()
    deduped_count = 0
    related_candidates, related_deduped = _select_related_candidates(context, used)
    deduped_count += related_deduped
    used.update(str(candidate["slug"]) for candidate in related_candidates if candidate.get("slug"))

    section_candidates: dict[str, list[dict[str, str | float | int | None]]] = {}
    for section_type in rule.section_order:
        content_type = SECTION_CONTENT_TYPES.get(section_type)
        if content_type is None:
            continue
        selected, section_deduped = _select_section_candidates(
            candidate_groups.get(content_type, []),
            used,
            rule.max_cards_per_section,
        )
        deduped_count += section_deduped
        if selected:
            section_candidates[section_type] = selected
            used.update(str(candidate["slug"]) for candidate in selected if candidate.get("slug"))

    return RecommendationPlan(
        intent_type=intent.intent_type,
        strategy=rule.strategy,
        main_content_type=main_content_type,
        section_order=rule.section_order,
        max_cards_per_section=rule.max_cards_per_section,
        dedupe_keys=sorted(key for key in used if key),
        deduped_count=deduped_count,
        reason=rule.reason,
        related_candidates=related_candidates,
        section_candidates=section_candidates,
    )


def _select_related_candidates(
    context: OrchestrationContext,
    used: set[str | None],
) -> tuple[list[dict[str, str | float | int | None]], int]:
    preferred_types = {
        IntentType.CITY: ["spot"],
        IntentType.ROUTE: ["spot"],
        IntentType.SPOT: [],
        IntentType.FOOD: ["spot", "route"],
        IntentType.CULTURE: [],
        IntentType.HOTEL: ["spot"],
    }.get(context.intent_type, [])
    selected: list[dict[str, str | float | int | None]] = []
    deduped = 0
    for content_type in preferred_types:
        for candidate in context.candidate_groups.get(content_type, []):
            slug = candidate.get("slug")
            if not isinstance(slug, str):
                continue
            if slug in used:
                deduped += 1
                continue
            selected.append(candidate)
            if len(selected) >= 1:
                return selected, deduped
    return selected, deduped


def _select_section_candidates(
    candidates: list[dict[str, str | float | int | None]],
    used: set[str | None],
    max_cards: int,
) -> tuple[list[dict[str, str | float | int | None]], int]:
    selected: list[dict[str, str | float | int | None]] = []
    deduped = 0
    for candidate in candidates:
        slug = candidate.get("slug")
        score = float(candidate.get("score") or 0)
        if not isinstance(slug, str) or score < 0.7:
            continue
        if slug in used:
            deduped += 1
            continue
        selected.append(candidate)
        if len(selected) >= max_cards:
            break
    return selected, deduped


def _personalize_candidate_groups(
    candidate_groups: dict[str, list[dict[str, str | float | int | None]]],
    persona: TravelerPersona | None,
) -> dict[str, list[dict[str, str | float | int | None]]]:
    if persona is None:
        return candidate_groups

    preferred = {
        TravelStyle.FAMILY: ["spot", "route"],
        TravelStyle.ELDER: ["route", "city", "spot"],
        TravelStyle.COUPLE: ["spot", "food", "route"],
        TravelStyle.FOODIE: ["food", "route", "spot"],
        TravelStyle.CULTURE: ["culture", "spot", "route"],
        TravelStyle.SHOPPING: ["food", "route", "spot"],
        TravelStyle.ANIME: ["culture", "spot"],
        TravelStyle.SOLO: ["route", "spot", "food"],
        TravelStyle.FIRST_TIME: ["spot", "route", "food"],
    }.get(persona.persona, [])

    result: dict[str, list[dict[str, str | float | int | None]]] = {}
    for content_type, candidates in candidate_groups.items():
        bonus = 0.08 if content_type in preferred else 0
        result[content_type] = [
            {**candidate, "score": min(1.0, float(candidate.get("score") or 0) + bonus)}
            for candidate in candidates
        ]
    return result
