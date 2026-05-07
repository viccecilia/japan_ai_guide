from app.schemas.intent import IntentResult, IntentType


SPOT_ENTITIES = {
    "清水寺": ("清水寺", "京都"),
    "伏见稻荷": ("伏见稻荷大社", "京都"),
    "伏见稻荷大社": ("伏见稻荷大社", "京都"),
    "大阪城": ("大阪城", "大阪"),
    "奈良公园": ("奈良公园", "奈良"),
}

CITY_ENTITIES = {
    "京都": "京都",
    "大阪": "大阪",
    "奈良": "奈良",
    "东京": "东京",
}

FOOD_KEYWORDS = ["美食", "吃", "餐厅", "拉面", "寿司", "料理", "甜点", "抹茶"]
ROUTE_KEYWORDS = ["路线", "一日游", "半日游", "怎么玩", "行程", "安排"]
CULTURE_KEYWORDS = ["神社", "寺庙", "文化", "传说", "为什么", "礼仪"]
HOTEL_KEYWORDS = ["酒店", "住宿", "旅馆", "住哪里", "饭店"]


def route_intent(query: str, language: str = "zh") -> IntentResult:
    text = query.strip()
    if not text:
        return IntentResult(intent_type=IntentType.UNKNOWN, language=language, confidence=0.1)

    city = _find_city(text)

    if _contains_any(text, HOTEL_KEYWORDS):
        return IntentResult(intent_type=IntentType.HOTEL, entity=_first_keyword(text, HOTEL_KEYWORDS), city=city, language=language, confidence=0.9)
    if _contains_any(text, FOOD_KEYWORDS):
        return IntentResult(intent_type=IntentType.FOOD, entity=_first_keyword(text, FOOD_KEYWORDS), city=city, language=language, confidence=0.88)
    if _contains_any(text, ROUTE_KEYWORDS):
        return IntentResult(intent_type=IntentType.ROUTE, entity=_first_keyword(text, ROUTE_KEYWORDS), city=city, language=language, confidence=0.88)
    if _contains_any(text, CULTURE_KEYWORDS):
        return IntentResult(intent_type=IntentType.CULTURE, entity=_first_keyword(text, CULTURE_KEYWORDS), city=city, language=language, confidence=0.86)

    for keyword, (entity, entity_city) in SPOT_ENTITIES.items():
        if keyword in text:
            return IntentResult(intent_type=IntentType.SPOT, entity=entity, city=entity_city, language=language, confidence=0.95)

    if city:
        return IntentResult(intent_type=IntentType.CITY, entity=city, city=city, language=language, confidence=0.9)

    return IntentResult(intent_type=IntentType.GENERIC, entity=None, city=None, language=language, confidence=0.45)


def _contains_any(text: str, keywords: list[str]) -> bool:
    return any(keyword in text for keyword in keywords)


def _first_keyword(text: str, keywords: list[str]) -> str | None:
    for keyword in keywords:
        if keyword in text:
            return keyword
    return None


def _find_city(text: str) -> str | None:
    for keyword, city in CITY_ENTITIES.items():
        if keyword in text:
            return city
    return None
