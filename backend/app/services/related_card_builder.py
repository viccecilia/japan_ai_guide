from app.schemas.answer_card import AnswerCard, AnswerCardAction, CardType
from app.schemas.content_library import BaseContent
from app.schemas.intent import IntentType
from app.schemas.multi_card_response import RelatedAnswerCard
from app.services.content_repository import content_repository


MAX_RELATED_CARDS = 4
MIN_RELATED_SCORE = 0.7


def build_related_cards(
    main_slug: str | None,
    candidates: list[dict[str, str | float | int | None]],
    language: str,
    intent_type: IntentType,
) -> list[RelatedAnswerCard]:
    if intent_type == IntentType.GENERIC:
        return []

    cards: list[RelatedAnswerCard] = []
    for candidate in candidates:
        slug = candidate.get("slug")
        score = float(candidate.get("score") or 0)
        content_type = candidate.get("content_type")
        if not isinstance(slug, str) or slug == main_slug or score < MIN_RELATED_SCORE:
            continue
        content = content_repository.find_by_slug(slug, language, str(content_type) if content_type else None)
        if content is None:
            continue
        cards.append(_content_to_related_card(content, candidate, len(cards)))
        if len(cards) >= MAX_RELATED_CARDS:
            break
    return cards


def _content_to_related_card(
    content: BaseContent,
    candidate: dict[str, str | float | int | None],
    index: int,
) -> RelatedAnswerCard:
    card = AnswerCard(
        id=content.id,
        card_type=_card_type_for_content(content.content_type),
        title=content.title,
        subtitle=content.subtitle,
        description=content.description,
        story=content.story,
        nearby=content.nearby,
        foods=content.foods,
        hotels=content.hotels,
        actions=[
            AnswerCardAction(label="查看建议", action="ask_followup", enabled=True, source="computed"),
        ],
        card_group="related",
        display_priority=80 - index,
        display_style="compact",
        recommendation_reason=f"{candidate.get('matched_by')} match · score {float(candidate.get('score') or 0):.2f}",
    )
    card.metadata.content_source = {"type": "content_library", "slug": content.slug, "language": content.language}
    card.metadata.ranking = candidate
    return RelatedAnswerCard.model_validate(card.model_dump())


def _card_type_for_content(content_type: str) -> CardType:
    mapping = {
        "spot": CardType.SPOT,
        "city": CardType.CITY,
        "food": CardType.FOOD,
        "route": CardType.ROUTE,
        "culture": CardType.CULTURE,
        "hotel": CardType.CITY,
    }
    return mapping.get(content_type, CardType.GENERIC)
