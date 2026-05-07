from app.schemas.intent import IntentType


FALLBACK_COPY: dict[IntentType, dict[str, str]] = {
    IntentType.SPOT: {
        "description": "这是适合第一次了解该景点的基础讲解。",
        "story": "我先为你整理一版经典看点：先理解位置和背景，再看附近可以顺路安排的地方。",
    },
    IntentType.CITY: {
        "description": "我先为你推荐一版经典城市玩法。",
        "story": "适合第一次到访的游客先抓住区域、交通和代表性体验，再决定是否深入小众路线。",
    },
    IntentType.FOOD: {
        "description": "下面是适合旅行途中继续探索的美食方向。",
        "story": "可以先从当地代表食物开始，再结合你所在区域选择餐厅和甜点。",
    },
    IntentType.ROUTE: {
        "description": "我先给你一版容易执行的经典路线思路。",
        "story": "路线会优先考虑顺路、少折返和第一次到访的理解成本，后续可以再按时间细化。",
    },
    IntentType.CULTURE: {
        "description": "这是适合旅行者快速理解的基础讲解。",
        "story": "先掌握核心区别和参观礼仪，再到现场观察建筑、标识和参拜流程，会更容易理解。",
    },
    IntentType.HOTEL: {
        "description": "我先为你整理住宿区域的基础判断方式。",
        "story": "第一次到访优先考虑交通、换乘复杂度和晚上用餐便利度，再看价格和房型。",
    },
    IntentType.GENERIC: {
        "description": "下面是你可以继续探索的方向。",
        "story": "你可以继续输入景点、城市、美食、路线、文化或住宿问题，我会整理成更明确的旅行卡片。",
    },
    IntentType.UNKNOWN: {
        "description": "下面是你可以继续探索的方向。",
        "story": "你可以换一种问法，或者直接输入一个景点、城市、美食、路线、文化或住宿主题。",
    },
}


def get_fallback_copy(intent_type: IntentType) -> dict[str, str]:
    return FALLBACK_COPY.get(intent_type, FALLBACK_COPY[IntentType.GENERIC])
