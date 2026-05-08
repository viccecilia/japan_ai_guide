from app.schemas.traveler_persona import TravelerPersona, TravelerPreference, TravelPace, TravelStyle


def detect_traveler_persona(query: str) -> TravelerPersona:
    text = query.lower()
    if any(word in text for word in ["老人", "长辈", "父母", "少走路", "慢慢", "elder"]):
        return TravelerPersona(
            persona=TravelStyle.ELDER,
            label="适合带老人慢慢体验",
            preference=TravelerPreference(pace=TravelPace.SLOW, walking_tolerance="low", culture_interest=4),
            confidence=0.92,
            journey_style="slow_elder",
        )
    if any(word in text for word in ["亲子", "孩子", "小孩", "家庭", "带娃", "family"]):
        return TravelerPersona(
            persona=TravelStyle.FAMILY,
            label="适合亲子家庭",
            preference=TravelerPreference(pace=TravelPace.SLOW, walking_tolerance="medium", family_friendly=True, photo_interest=4),
            confidence=0.9,
            journey_style="family_light",
        )
    if any(word in text for word in ["情侣", "约会", "夫妻", "浪漫", "couple"]):
        return TravelerPersona(
            persona=TravelStyle.COUPLE,
            label="适合情侣散步",
            preference=TravelerPreference(pace=TravelPace.NORMAL, walking_tolerance="medium", food_interest=4, photo_interest=5),
            confidence=0.88,
            journey_style="couple_scenic",
        )
    if any(word in text for word in ["美食", "吃", "餐厅", "拉面", "寿司", "food"]):
        return TravelerPersona(
            persona=TravelStyle.FOODIE,
            label="适合美食探索",
            preference=TravelerPreference(pace=TravelPace.NORMAL, food_interest=5, culture_interest=2),
            confidence=0.86,
            journey_style="foodie_route",
        )
    if any(word in text for word in ["文化", "神社", "寺庙", "历史", "传说", "culture"]):
        return TravelerPersona(
            persona=TravelStyle.CULTURE,
            label="适合文化体验",
            preference=TravelerPreference(pace=TravelPace.NORMAL, culture_interest=5, photo_interest=3),
            confidence=0.84,
            journey_style="culture_deep",
        )
    if any(word in text for word in ["购物", "买", "商场", "心斋桥", "银座", "shopping"]):
        return TravelerPersona(
            persona=TravelStyle.SHOPPING,
            label="适合购物安排",
            preference=TravelerPreference(pace=TravelPace.DENSE, shopping_interest=5, food_interest=3),
            confidence=0.82,
            journey_style="shopping_dense",
        )
    if any(word in text for word in ["动漫", "二次元", "秋叶原", "圣地巡礼", "anime"]):
        return TravelerPersona(
            persona=TravelStyle.ANIME,
            label="适合动漫主题",
            preference=TravelerPreference(pace=TravelPace.NORMAL, shopping_interest=4, photo_interest=4),
            confidence=0.82,
            journey_style="anime_theme",
        )
    if any(word in text for word in ["一个人", "独自", "solo"]):
        return TravelerPersona(
            persona=TravelStyle.SOLO,
            label="适合一个人旅行",
            preference=TravelerPreference(pace=TravelPace.NORMAL, walking_tolerance="medium"),
            confidence=0.78,
            journey_style="solo_balanced",
        )
    if any(word in text for word in ["第一次", "初次", "首次", "first"]):
        return TravelerPersona(
            persona=TravelStyle.FIRST_TIME,
            label="适合第一次来日本",
            preference=TravelerPreference(pace=TravelPace.NORMAL, culture_interest=4, photo_interest=4),
            confidence=0.86,
            journey_style="classic_first_time",
        )
    return TravelerPersona()
