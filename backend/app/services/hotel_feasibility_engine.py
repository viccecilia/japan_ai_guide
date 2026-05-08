from app.schemas.journey_timeline import JourneyDay
from app.schemas.travel_constraint import HotelConstraint


def validate_hotel_placement(day: JourneyDay) -> HotelConstraint:
    hotel_title = day.hotel.title if day.hotel else None
    if not day.hotel:
        return HotelConstraint(
            day_number=day.day_number,
            city=day.city,
            hotel_title=None,
            hotel_distance="tight",
            reason="当天缺少住宿建议，跨日路线需要补充住宿区域。",
        )
    if day.city not in day.hotel.subtitle and day.city not in day.hotel.title:
        return HotelConstraint(
            day_number=day.day_number,
            city=day.city,
            hotel_title=hotel_title,
            hotel_distance="tight",
            reason=f"酒店区域看起来不在{day.city}，可能增加跨城疲劳。",
        )
    return HotelConstraint(
        day_number=day.day_number,
        city=day.city,
        hotel_title=hotel_title,
        hotel_distance="normal",
        reason=f"酒店位于{day.city}动线内，适合作为当天落脚点。",
    )
