from app.schemas.answer_card import AnswerCard
from app.schemas.itinerary import Itinerary, ItineraryBlock, ItineraryStop, TravelFlow
from app.schemas.multi_card_response import RecommendationSection
from app.schemas.travel_memory import MemorySnapshot
from app.schemas.traveler_persona import TravelerPersona, TravelStyle
from app.services.pace_engine import block_titles_for_persona, break_note_for_persona, estimated_total_time, stop_limit_for_persona
from app.services.route_composition_rules import choose_duration, choose_route_type, dedupe_cards, split_by_pacing, transport_note_for
from app.services.travel_narrative_builder import build_itinerary_narrative, build_stop_narrative


JOURNEY_PROMPTS = [
    "帮我安排京都一日游",
    "适合老人路线",
    "适合亲子路线",
    "适合情侣路线",
    "适合第一次来日本",
]


def build_travel_flow(
    query: str,
    intent_type: str,
    main_card: AnswerCard,
    related_cards: list[AnswerCard],
    sections: list[RecommendationSection],
    persona: TravelerPersona,
    memory_snapshot: MemorySnapshot | None = None,
) -> TravelFlow | None:
    source_cards = _personalize_cards(_collect_cards(main_card, related_cards, sections), persona)
    if not source_cards:
        return None

    route_type = _route_type_for_persona(query, intent_type, persona, memory_snapshot)
    duration = choose_duration(route_type)
    city = _infer_city(source_cards)
    title = _build_title(city, route_type, duration, persona, memory_snapshot)
    stop_limit = stop_limit_for_persona(persona)
    stops = [
        ItineraryStop(
            title=card.title,
            subtitle=card.subtitle,
            stop_type=str(card.metadata.ranking.get("content_type") or "spot"),
            estimated_time=_estimated_stop_time(index, persona),
            transport_notes="按当前内容库顺路编排，未接真实地图距离。",
            narrative=build_stop_narrative(card, index, route_type, persona),
        )
        for index, card in enumerate(source_cards[:stop_limit])
    ]
    morning, afternoon = split_by_pacing(source_cards[:stop_limit])
    morning_title, afternoon_title = block_titles_for_persona(persona)
    blocks = [
        _build_block(morning_title, "上午", morning, route_type, persona),
        _build_block(afternoon_title, "下午", afternoon, route_type, persona),
    ]
    blocks = [block for block in blocks if block.stops]

    itinerary = Itinerary(
        title=title,
        city=city,
        duration=duration,
        route_type=route_type,
        persona=persona.persona.value,
        persona_label=persona.label,
        pace=persona.preference.pace.value,
        journey_style=persona.journey_style,
        stops=stops,
        foods=[stop for stop in stops if stop.stop_type == "food"],
        culture=[stop for stop in stops if stop.stop_type == "culture"],
        hotel=next((stop for stop in stops if stop.stop_type == "hotel"), None),
        blocks=blocks,
        transport_notes=f"{transport_note_for(route_type)} {break_note_for_persona(persona)}",
        estimated_time=estimated_total_time(persona, duration),
        narrative=build_itinerary_narrative(title, route_type, persona),
    )
    return TravelFlow(
        flow_type="personalized_itinerary_flow",
        title=title,
        summary=_build_summary(persona, memory_snapshot),
        persona=persona.persona.value,
        pace=persona.preference.pace.value,
        journey_style=persona.journey_style,
        itineraries=[itinerary],
        journey_prompts=JOURNEY_PROMPTS,
    )


def _collect_cards(
    main_card: AnswerCard,
    related_cards: list[AnswerCard],
    sections: list[RecommendationSection],
) -> list[AnswerCard]:
    section_cards = [card for section in sections for card in section.cards]
    return dedupe_cards([main_card, *related_cards, *section_cards])


def _personalize_cards(cards: list[AnswerCard], persona: TravelerPersona) -> list[AnswerCard]:
    def score(card: AnswerCard) -> int:
        content_type = str(card.metadata.ranking.get("content_type") or "")
        title = card.title + " " + card.subtitle
        value = 0
        if persona.persona == TravelStyle.FOODIE and content_type == "food":
            value += 5
        if persona.persona == TravelStyle.CULTURE and content_type in {"culture", "spot"}:
            value += 4
        if persona.persona == TravelStyle.FAMILY and any(token in title for token in ["奈良", "公园", "小鹿", "动物"]):
            value += 5
        if persona.persona == TravelStyle.ELDER and content_type in {"city", "route"}:
            value += 3
        if persona.persona == TravelStyle.COUPLE and any(token in title for token in ["祗园", "京都", "夜", "散步"]):
            value += 3
        if persona.persona == TravelStyle.SHOPPING and any(token in title for token in ["心斋桥", "银座", "购物"]):
            value += 5
        return value

    return sorted(cards, key=score, reverse=True)


def _build_block(
    title: str,
    time_of_day: str,
    cards: list[AnswerCard],
    route_type: str,
    persona: TravelerPersona,
) -> ItineraryBlock:
    return ItineraryBlock(
        block_title=title,
        time_of_day=time_of_day,
        stops=[
            ItineraryStop(
                title=card.title,
                subtitle=card.subtitle,
                stop_type=str(card.metadata.ranking.get("content_type") or "spot"),
                estimated_time=_estimated_stop_time(index, persona),
                narrative=build_stop_narrative(card, index, route_type, persona),
            )
            for index, card in enumerate(cards)
        ],
        narrative=break_note_for_persona(persona),
    )


def _route_type_for_persona(query: str, intent_type: str, persona: TravelerPersona, memory_snapshot: MemorySnapshot | None = None) -> str:
    if memory_snapshot and memory_snapshot.preference.preferred_persona == "culture":
        return "culture"
    if memory_snapshot and memory_snapshot.preference.preferred_pace == "slow":
        return "slow"
    if persona.persona == TravelStyle.FAMILY:
        return "family"
    if persona.persona == TravelStyle.ELDER:
        return "slow"
    if persona.persona == TravelStyle.FOODIE:
        return "food"
    if persona.persona == TravelStyle.CULTURE:
        return "culture"
    if persona.persona == TravelStyle.COUPLE:
        return "couple"
    return choose_route_type(query, intent_type)


def _infer_city(cards: list[AnswerCard]) -> str | None:
    joined = " ".join([card.title + " " + card.subtitle for card in cards])
    for city in ["京都", "大阪", "奈良", "东京"]:
        if city in joined:
            return city
    return None


def _build_title(city: str | None, route_type: str, duration: str, persona: TravelerPersona, memory_snapshot: MemorySnapshot | None = None) -> str:
    city_name = city or "日本"
    if memory_snapshot and memory_snapshot.preference.preferred_pace == "slow":
        return f"{city_name}慢节奏偏好路线"
    if memory_snapshot and memory_snapshot.preference.preferred_persona == "culture":
        return f"{city_name}文化偏好路线"
    if route_type == "family":
        return f"{city_name}亲子轻松路线"
    if route_type == "slow":
        return f"{city_name}慢节奏安心路线"
    if route_type == "couple":
        return f"{city_name}情侣散步路线"
    if route_type == "food":
        return f"{city_name}美食旅行路线"
    if route_type == "culture":
        return f"{city_name}文化故事路线"
    if duration == "one_day":
        return f"{city_name}经典一日路线"
    return f"{city_name}{persona.label}路线"


def _build_summary(persona: TravelerPersona, memory_snapshot: MemorySnapshot | None = None) -> str:
    if memory_snapshot:
        return f"{memory_snapshot.summary} 这次路线会优先延续你的旅行偏好。"
    return f"基于当前问题和推荐内容，为“{persona.label}”生成的个性化旅行流。"


def _estimated_stop_time(index: int, persona: TravelerPersona) -> str:
    if persona.preference.pace.value == "slow":
        slots = ["60-90分钟", "60分钟", "45-60分钟"]
    elif persona.preference.pace.value == "dense":
        slots = ["45-60分钟", "45分钟", "30-45分钟", "30分钟", "30分钟", "20-30分钟"]
    else:
        slots = ["60-90分钟", "45-60分钟", "45分钟", "30-45分钟", "30分钟"]
    return slots[min(index, len(slots) - 1)]
