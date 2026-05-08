from app.schemas.itinerary import ItineraryStop


HOTEL_BY_CITY = {
    "京都": ("京都站附近酒店", "交通方便，适合作为京都多日路线的 base。"),
    "大阪": ("难波附近酒店", "适合美食和购物动线，夜间也比较方便。"),
    "东京": ("新宿附近酒店", "适合城市交通换乘，也方便安排购物和夜间活动。"),
    "奈良": ("奈良站附近酒店", "适合慢节奏停留，但也可以从京都当天往返。"),
}


def insert_hotel_for_city(city: str) -> ItineraryStop:
    name, narrative = HOTEL_BY_CITY.get(city, (f"{city}站附近酒店", "优先选择车站附近，方便第二天继续移动。"))
    return ItineraryStop(
        title=name,
        subtitle=f"{city} · 住宿建议",
        stop_type="hotel",
        estimated_time="入住后休息",
        narrative=narrative,
    )
