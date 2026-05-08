from app.schemas.answer_card import AnswerCard


def dedupe_cards(cards: list[AnswerCard]) -> list[AnswerCard]:
    seen: set[str] = set()
    result: list[AnswerCard] = []
    for card in cards:
        slug = _card_slug(card) or card.id
        if slug in seen:
            continue
        seen.add(slug)
        result.append(card)
    return result


def choose_route_type(query: str, intent_type: str) -> str:
    if "亲子" in query or "family" in query.lower():
        return "family"
    if "美食" in query or "吃" in query:
        return "food"
    if "文化" in query or "神社" in query or "寺庙" in query:
        return "culture"
    if "一日" in query or intent_type == "route_query":
        return "one_day"
    return "half_day"


def choose_duration(route_type: str) -> str:
    if route_type == "one_day":
        return "one_day"
    return "half_day"


def split_by_pacing(cards: list[AnswerCard]) -> tuple[list[AnswerCard], list[AnswerCard]]:
    midpoint = max(1, min(2, len(cards)))
    return cards[:midpoint], cards[midpoint:4]


def transport_note_for(route_type: str) -> str:
    if route_type == "one_day":
        return "本轮不接真实地图，路线按顺路和节奏做启发式编排；实际交通请在出发前再次确认。"
    return "半日路线优先减少跨区移动，适合用步行或短距离公共交通串联。"


def _card_slug(card: AnswerCard) -> str | None:
    slug = card.metadata.content_source.get("slug")
    return slug if isinstance(slug, str) else None
