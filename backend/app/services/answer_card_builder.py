from app.mock.mock_answer_cards import get_mock_answer_card
from app.schemas.answer_card import AnswerCard, AnswerCardAction, CardType
from app.schemas.content_library import BaseContent
from app.schemas.intent import IntentResult, IntentType
from app.schemas.multi_card_response import MainAnswerCard, MultiCardResponse
from app.services.content_resolver import ResolvedContent, resolve_content
from app.services.fallback_copy import get_fallback_copy
from app.services.recommendation_section_builder import build_recommendation_sections
from app.services.related_card_builder import build_related_cards
from app.services.token_gate import TokenGateResult


def build_answer_card(query: str, intent: IntentResult, token_gate: TokenGateResult) -> AnswerCard:
    return build_multi_card_response(query, intent, token_gate).main_card


def build_multi_card_response(query: str, intent: IntentResult, token_gate: TokenGateResult) -> MultiCardResponse:
    resolved = resolve_content(query, intent)
    main_card = _build_main_card(query, intent, token_gate, resolved)
    related_cards = build_related_cards(
        main_card.metadata.content_source.get("slug"),
        resolved.related_candidates,
        intent.language,
        intent.intent_type,
    )
    sections = build_recommendation_sections(related_cards)
    group_counts = {"main": 1, "related": len(related_cards), "sections": len(sections)}

    main_card.metadata.card_groups = group_counts
    response_metadata = {
        "intent": intent.model_dump(),
        "cache": main_card.metadata.cache,
        "ranking": main_card.metadata.ranking,
        "content_source": main_card.metadata.content_source,
        "card_groups": group_counts,
        "candidate_groups": resolved.candidate_groups,
    }
    return MultiCardResponse(
        main_card=MainAnswerCard.model_validate(main_card.model_dump()),
        related_cards=related_cards,
        sections=sections,
        metadata=response_metadata,
    )


def _build_main_card(
    query: str,
    intent: IntentResult,
    token_gate: TokenGateResult,
    resolved: ResolvedContent,
) -> AnswerCard:
    if resolved.content is not None:
        card = _build_from_content(resolved.content, _card_type_for_intent(intent.intent_type))
    else:
        card = _build_template_card(query, intent)
        copy = get_fallback_copy(intent.intent_type)
        card.description = _merge_copy(copy["description"], card.description)
        card.story = _merge_copy(copy["story"], card.story)

    card.card_group = "main"
    card.display_priority = 100
    card.display_style = "large"
    card.recommendation_reason = "Best ranked candidate for the current query."
    card.metadata.intent = intent
    card.metadata.ai_runtime = token_gate.model_dump()
    card.metadata.language = intent.language
    card.metadata.content_source = resolved.content_source
    card.metadata.cache = resolved.cache
    card.metadata.ranking = resolved.ranking
    card.metadata.related_candidates = resolved.related_candidates
    return card


def _build_template_card(query: str, intent: IntentResult) -> AnswerCard:
    builders = {
        IntentType.SPOT: spot_card_builder,
        IntentType.CITY: city_card_builder,
        IntentType.FOOD: food_card_builder,
        IntentType.ROUTE: route_card_builder,
        IntentType.CULTURE: culture_card_builder,
        IntentType.HOTEL: hotel_card_builder,
        IntentType.GENERIC: generic_card_builder,
        IntentType.UNKNOWN: generic_card_builder,
    }
    return builders.get(intent.intent_type, generic_card_builder)(query, intent)


def _build_from_content(content: BaseContent, card_type: CardType) -> AnswerCard:
    return AnswerCard(
        id=content.id,
        card_type=card_type,
        title=content.title,
        subtitle=content.subtitle,
        description=content.description,
        story=content.story,
        nearby=content.nearby,
        foods=content.foods,
        hotels=content.hotels,
        actions=[
            AnswerCardAction(label="继续追问", action="ask_followup", enabled=True, source="computed"),
            AnswerCardAction(label="生成路线", action="create_route", enabled=True, source="computed"),
            AnswerCardAction(label="收藏到行程", action="save_to_trip", enabled=True, source="computed"),
        ],
    )


def _card_type_for_intent(intent_type: IntentType) -> CardType:
    mapping = {
        IntentType.SPOT: CardType.SPOT,
        IntentType.CITY: CardType.CITY,
        IntentType.FOOD: CardType.FOOD,
        IntentType.ROUTE: CardType.ROUTE,
        IntentType.CULTURE: CardType.CULTURE,
        IntentType.HOTEL: CardType.CITY,
        IntentType.GENERIC: CardType.GENERIC,
        IntentType.UNKNOWN: CardType.GENERIC,
    }
    return mapping.get(intent_type, CardType.GENERIC)


def spot_card_builder(query: str, intent: IntentResult) -> AnswerCard:
    return get_mock_answer_card(intent.entity or query).model_copy(deep=True)


def city_card_builder(query: str, intent: IntentResult) -> AnswerCard:
    return get_mock_answer_card(intent.city or intent.entity or query).model_copy(deep=True)


def food_card_builder(query: str, intent: IntentResult) -> AnswerCard:
    return get_mock_answer_card("京都美食").model_copy(deep=True)


def route_card_builder(query: str, intent: IntentResult) -> AnswerCard:
    return get_mock_answer_card("路线").model_copy(deep=True)


def culture_card_builder(query: str, intent: IntentResult) -> AnswerCard:
    return get_mock_answer_card("神社").model_copy(deep=True)


def hotel_card_builder(query: str, intent: IntentResult) -> AnswerCard:
    card = get_mock_answer_card(intent.city or "京都").model_copy(deep=True)
    card.id = "hotel_template"
    card.card_type = CardType.CITY
    card.title = f"{intent.city or '日本'}住宿建议"
    card.subtitle = "住宿 · 区域选择"
    card.description = "我先按第一次来日本游客的需求，为你整理住宿区域的基础判断方式。"
    card.story = "优先看交通便利度、夜间安全感、行李移动成本和预算，再决定住在车站周边、景点周边或安静街区。"
    card.actions = [AnswerCardAction(label="继续说明预算和人数", action="ask_followup", enabled=True, source="mock")]
    return card


def generic_card_builder(query: str, intent: IntentResult) -> AnswerCard:
    return get_mock_answer_card(query).model_copy(deep=True)


def _merge_copy(prefix: str, body: str) -> str:
    if body.startswith(prefix):
        return body
    return f"{prefix} {body}"
