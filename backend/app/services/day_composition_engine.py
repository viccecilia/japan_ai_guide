from app.schemas.itinerary import ItineraryStop
from app.schemas.journey_timeline import JourneyBlock, JourneyDay
from app.services.hotel_insertion_engine import insert_hotel_for_city
from app.services.multi_day_narrative_builder import day_narrative


def compose_day(day_number: int, city: str, source_stops: list[ItineraryStop], pace: str) -> JourneyDay:
    limit = 3 if pace == "slow" else 5 if pace == "dense" else 4
    selected = source_stops[:limit] or [_fallback_stop(city)]
    midpoint = max(1, min(2, len(selected)))
    morning = selected[:midpoint]
    afternoon = selected[midpoint:]
    blocks = [
        JourneyBlock(
            block_type="activity",
            title="上午主线",
            time_of_day="morning",
            stops=morning,
            narrative="上午先安排最重要的体验，减少临时决策成本。",
        )
    ]
    if afternoon:
        blocks.append(
            JourneyBlock(
                block_type="activity",
                title="下午延展",
                time_of_day="afternoon",
                stops=afternoon,
                narrative="下午保持弹性，根据体力决定是否完整走完。",
            )
        )
    return JourneyDay(
        day_number=day_number,
        title=f"Day {day_number} · {city}",
        city=city,
        blocks=blocks,
        hotel=insert_hotel_for_city(city),
        daily_narrative=day_narrative(day_number, city, pace),
        pace=pace,
    )


def regenerate_day(day: JourneyDay, pace: str) -> JourneyDay:
    stops = [stop for block in day.blocks for stop in block.stops]
    return compose_day(day.day_number, day.city, stops, pace)


def remove_stop_from_day(day: JourneyDay, stop_title: str) -> JourneyDay:
    stops = [stop for block in day.blocks for stop in block.stops if stop.title != stop_title]
    return compose_day(day.day_number, day.city, stops, day.pace)


def _fallback_stop(city: str) -> ItineraryStop:
    return ItineraryStop(
        title=f"{city}代表街区",
        subtitle=f"{city} · 基础体验",
        stop_type="spot",
        estimated_time="60分钟",
        narrative="作为当天的基础停留点，后续可以替换为更具体的景点。",
    )
