from app.schemas.intent import IntentType
from app.schemas.recommendation_orchestration import RecommendationRule


SECTION_CONTENT_TYPES = {
    "recommended_spots": "spot",
    "nearby_spots": "spot",
    "related_spots": "spot",
    "recommended_routes": "route",
    "recommended_foods": "food",
    "recommended_culture": "culture",
    "recommended_hotels": "hotel",
}

SECTION_TITLES = {
    "recommended_spots": "推荐景点",
    "nearby_spots": "附近景点",
    "recommended_routes": "推荐路线",
    "recommended_foods": "推荐美食",
    "recommended_culture": "文化故事",
    "recommended_hotels": "住宿建议",
    "related_spots": "相关景点",
    "suggested_prompts": "你还可以继续了解",
}

SECTION_NARRATIVES = {
    "recommended_spots": {
        "intro": "如果你第一次来到这里，可以先把这些经典地点放进清单。",
        "narrative": "它们更适合作为行程的主骨架，再根据体力和天气删减。",
    },
    "nearby_spots": {
        "intro": "如果你已经在主景点附近，这些地点适合顺路串联。",
        "narrative": "优先选择步行或短距离移动，能让半日行程更从容。",
    },
    "recommended_routes": {
        "intro": "下面这些路线更适合直接拿来做当天安排。",
        "narrative": "路线建议会优先考虑移动成本、经典程度和第一次到访的体验密度。",
    },
    "recommended_foods": {
        "intro": "逛完景点后，可以用这些美食方向补足当地体验。",
        "narrative": "先选区域，再选店型，会比只搜索单个餐厅更稳定。",
    },
    "recommended_culture": {
        "intro": "如果你想听懂日本旅行里的细节，可以继续看这些文化故事。",
        "narrative": "这些解释能帮助你在参观时理解建筑、仪式和当地习惯。",
    },
    "recommended_hotels": {
        "intro": "住宿建议先看交通和夜间安全感，再看价格。",
        "narrative": "第一次来日本时，住在车站或核心街区附近通常更省心。",
    },
    "related_spots": {
        "intro": "这些地点和当前主题关系更直接，适合继续深入。",
        "narrative": "它们可以作为下一问，也可以加入同一天的轻量补充。",
    },
    "suggested_prompts": {
        "intro": "你还可以继续了解：",
        "narrative": "选择一个方向，我会继续按 AI 导游的方式帮你展开。",
    },
}

SUGGESTED_PROMPTS = [
    "京都第一次怎么玩？",
    "清水寺有什么故事？",
    "大阪一日游怎么安排？",
    "神社和寺庙有什么区别？",
]

RULES = {
    IntentType.CITY: RecommendationRule(
        intent_type=IntentType.CITY,
        strategy="city_query_default",
        section_order=[
            "recommended_spots",
            "recommended_routes",
            "recommended_foods",
            "recommended_culture",
            "recommended_hotels",
        ],
        reason="city query prioritizes spots and routes",
    ),
    IntentType.ROUTE: RecommendationRule(
        intent_type=IntentType.ROUTE,
        strategy="route_query_default",
        section_order=["recommended_spots", "recommended_foods", "recommended_hotels", "recommended_culture"],
        reason="route query prioritizes stops and practical support",
    ),
    IntentType.SPOT: RecommendationRule(
        intent_type=IntentType.SPOT,
        strategy="spot_query_default",
        section_order=["nearby_spots", "recommended_foods", "recommended_routes", "recommended_culture"],
        reason="spot query prioritizes nearby context and next actions",
    ),
    IntentType.FOOD: RecommendationRule(
        intent_type=IntentType.FOOD,
        strategy="food_query_default",
        section_order=["recommended_foods", "nearby_spots", "recommended_routes"],
        reason="food query prioritizes food and nearby itinerary options",
    ),
    IntentType.CULTURE: RecommendationRule(
        intent_type=IntentType.CULTURE,
        strategy="culture_query_default",
        section_order=["recommended_culture", "related_spots", "recommended_routes"],
        reason="culture query prioritizes explanations and related places",
    ),
    IntentType.HOTEL: RecommendationRule(
        intent_type=IntentType.HOTEL,
        strategy="hotel_query_default",
        section_order=["recommended_hotels", "nearby_spots", "recommended_routes"],
        reason="hotel query prioritizes lodging and area convenience",
    ),
    IntentType.GENERIC: RecommendationRule(
        intent_type=IntentType.GENERIC,
        strategy="generic_query_fallback",
        section_order=["suggested_prompts"],
        reason="generic query returns suggested prompts instead of unrelated cards",
    ),
    IntentType.UNKNOWN: RecommendationRule(
        intent_type=IntentType.UNKNOWN,
        strategy="generic_query_fallback",
        section_order=["suggested_prompts"],
        reason="unknown query returns suggested prompts instead of unrelated cards",
    ),
}


def get_recommendation_rule(intent_type: IntentType) -> RecommendationRule:
    return RULES.get(intent_type, RULES[IntentType.GENERIC])
