from app.schemas.itinerary import TravelFlow
from app.schemas.journey_timeline import JourneyTimeline
from app.schemas.traveler_persona import TravelerPersona
from app.services.day_composition_engine import compose_day
from app.services.hotel_insertion_engine import insert_hotel_for_city
from app.services.multi_day_narrative_builder import build_transition


def build_journey_timeline(query: str, travel_flow: TravelFlow | None, persona: TravelerPersona) -> JourneyTimeline | None:
    if travel_flow is None or not travel_flow.itineraries:
        return None
    cities = _cities_for_query(query, travel_flow.itineraries[0].city)
    day_count = _day_count_for_query(query)
    scheduled_cities = [cities[index % len(cities)] for index in range(day_count)]
    source_stops = travel_flow.itineraries[0].stops
    days = [
        compose_day(index + 1, city, source_stops[index:] + source_stops[:index], persona.preference.pace.value)
        for index, city in enumerate(scheduled_cities)
    ]
    transitions = [
        build_transition(scheduled_cities[index], scheduled_cities[index + 1])
        for index in range(len(scheduled_cities) - 1)
        if scheduled_cities[index] != scheduled_cities[index + 1]
    ]
    hotels = [insert_hotel_for_city(city) for city in scheduled_cities]
    unique_cities = list(dict.fromkeys(scheduled_cities))
    return JourneyTimeline(
        timeline_id=f"timeline-{abs(hash(query)) % 100000}",
        title=_timeline_title(unique_cities, day_count),
        days=days,
        cities=unique_cities,
        hotels=hotels,
        transitions=transitions,
        total_duration=f"{day_count}-day",
        journey_style=persona.journey_style,
    )


def _day_count_for_query(query: str) -> int:
    normalized = query.lower()
    if any(token in normalized for token in ["五日", "5日", "五天", "5天", "five day"]):
        return 5
    if any(token in normalized for token in ["三日", "3日", "三天", "3天", "three day"]):
        return 3
    if any(token in normalized for token in ["两日", "二日", "2日", "两天", "二天", "2天", "two day"]):
        return 2
    return 1


def _cities_for_query(query: str, fallback_city: str | None) -> list[str]:
    candidates = [city for city in ["东京", "京都", "大阪", "奈良"] if city in query]
    if candidates:
        return candidates
    return [fallback_city or "京都"]


def _timeline_title(cities: list[str], day_count: int) -> str:
    return f"{' · '.join(cities)} {day_count}日旅行时间轴"
