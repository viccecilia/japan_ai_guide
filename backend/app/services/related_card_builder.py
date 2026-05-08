from app.schemas.answer_card import AnswerCard, AnswerCardAction, CardType
from app.schemas.content_library import BaseContent
from app.schemas.intent import IntentType
from app.schemas.multi_card_response import RelatedAnswerCard
from app.services.content_repository import content_repository


MAX_RELATED_CARDS = 3
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
    used = {main_slug} if main_slug else set()
    for candidate in candidates:
        card = build_related_card_from_candidate(candidate, language, len(cards))
        slug = candidate.get("slug")
        score = float(candidate.get("score") or 0)
        if card is None or not isinstance(slug, str) or slug in used or score < MIN_RELATED_SCORE:
            continue
        cards.append(card)
        used.add(slug)
        if len(cards) >= MAX_RELATED_CARDS:
            break
    return cards


def build_related_card_from_candidate(
    candidate: dict[str, str | float | int | None],
    language: str,
    index: int,
) -> RelatedAnswerCard | None:
    slug = candidate.get("slug")
    score = float(candidate.get("score") or 0)
    content_type = candidate.get("content_type")
    if not isinstance(slug, str) or score < MIN_RELATED_SCORE:
        return None
    content = content_repository.find_by_slug(slug, language, str(content_type) if content_type else None)
    if content is None:
        return None
    return _content_to_related_card(content, candidate, index)


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
            AnswerCardAction(label="继续了解", action="ask_followup", enabled=True, source="computed"),
        ],
        card_group="related",
        display_priority=80 - index,
        display_style="compact",
        recommendation_reason=_recommendation_reason(content.content_type),
    )
    card.metadata.content_source = {"type": "content_library", "slug": content.slug, "language": content.language}
    card.metadata.ranking = candidate
    return RelatedAnswerCard.model_validate(card.model_dump())


def _recommendation_reason(content_type: str) -> str:
    reasons = {
        "spot": "适合加入同一天的顺路景点。",
        "city": "适合先建立整体旅行方向。",
        "food": "适合在行程中安排一段当地用餐体验。",
        "route": "适合直接作为半日或一日路线参考。",
        "culture": "适合在参观前先理解背景故事。",
        "hotel": "适合关注交通便利和夜间安全感的游客。",
    }
    return reasons.get(content_type, "适合作为下一步继续探索。")


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
