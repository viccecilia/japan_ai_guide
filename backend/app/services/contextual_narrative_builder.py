from app.schemas.travel_context import TravelContext


def build_contextual_narrative(context: TravelContext) -> str:
    parts: list[str] = []
    if context.weather.condition == "rainy":
        parts.append("今天适合把连续户外步行改成更稳妥的室内或短距离安排。")
    elif context.weather.condition == "hot":
        parts.append("天气偏热，建议减少下午连续步行，并把休息点前置。")
    elif context.weather.condition == "crowded":
        parts.append("热门区域可能拥挤，建议降低热门点密度。")
    if not context.time.long_transition_allowed:
        parts.append("当前时间不适合再安排远距离跨城移动。")
    if context.fatigue.travel_fatigue in {"high", "overload"}:
        parts.append("连续密集行程已经累积疲劳，下一段建议放慢节奏。")
    if not parts:
        return "当前旅行状态稳定，可以按原路线推进。"
    return " ".join(parts)
