from collections import defaultdict

from app.schemas.multi_card_response import RecommendationSection, RelatedAnswerCard


SECTION_TITLES = {
    "spot": ("recommended_spots", "推荐景点"),
    "route": ("recommended_routes", "推荐路线"),
    "food": ("recommended_foods", "推荐美食"),
    "culture": ("recommended_culture", "推荐文化"),
    "hotel": ("recommended_hotels", "推荐住宿"),
}


def build_recommendation_sections(cards: list[RelatedAnswerCard]) -> list[RecommendationSection]:
    grouped: dict[str, list[RelatedAnswerCard]] = defaultdict(list)
    for card in cards:
        content_type = str(card.metadata.ranking.get("content_type") or "")
        if content_type in SECTION_TITLES:
            grouped[content_type].append(card)

    sections: list[RecommendationSection] = []
    for content_type in ["spot", "route", "food", "culture", "hotel"]:
        cards_for_type = grouped.get(content_type, [])
        if not cards_for_type:
            continue
        section_type, title = SECTION_TITLES[content_type]
        sections.append(RecommendationSection(section_type=section_type, title=title, cards=cards_for_type))
    return sections
