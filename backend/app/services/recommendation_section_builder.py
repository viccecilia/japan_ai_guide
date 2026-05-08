from app.schemas.multi_card_response import RecommendationSection
from app.schemas.recommendation_orchestration import RecommendationPlan
from app.services.recommendation_rules import SECTION_NARRATIVES, SECTION_TITLES
from app.services.related_card_builder import build_related_card_from_candidate


def build_recommendation_sections(plan: RecommendationPlan, language: str) -> list[RecommendationSection]:
    sections: list[RecommendationSection] = []

    if plan.suggested_prompts:
        sections.append(
            RecommendationSection(
                section_type="suggested_prompts",
                title=SECTION_TITLES["suggested_prompts"],
                section_intro=SECTION_NARRATIVES["suggested_prompts"]["intro"],
                section_narrative=SECTION_NARRATIVES["suggested_prompts"]["narrative"],
                cards=[],
                prompts=plan.suggested_prompts,
            )
        )
        return sections

    for section_type in plan.section_order:
        candidates = plan.section_candidates.get(section_type, [])
        if not candidates:
            continue
        cards = [
            card
            for index, candidate in enumerate(candidates)
            if (card := build_related_card_from_candidate(candidate, language, index)) is not None
        ]
        if not cards:
            continue
        sections.append(
            RecommendationSection(
                section_type=section_type,
                title=SECTION_TITLES.get(section_type, section_type),
                section_intro=SECTION_NARRATIVES.get(section_type, {}).get("intro"),
                section_narrative=SECTION_NARRATIVES.get(section_type, {}).get("narrative"),
                cards=cards,
            )
        )
    return sections


def build_itinerary_section(itineraries: list[object]) -> RecommendationSection | None:
    if not itineraries:
        return None
    return RecommendationSection(
        section_type="itinerary_section",
        title="AI 行程流",
        section_intro="我把上面的回答和推荐内容，整理成一条可以直接参考的旅行路线。",
        section_narrative="当前路线按顺路、节奏和体验密度启发式编排；还没有接真实地图和实时交通。",
        cards=[],
        itineraries=itineraries,
    )
