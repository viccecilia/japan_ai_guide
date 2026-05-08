from app.schemas.editable_itinerary import JourneyInteractionType


def interaction_narrative(interaction_type: JourneyInteractionType, detail: dict[str, object]) -> str:
    if interaction_type == JourneyInteractionType.PERSONA_SWITCH:
        return f"已调整为更适合 {detail.get('to')} 的旅行路线。"
    if interaction_type == JourneyInteractionType.PACE_SWITCH:
        return f"已切换为 {detail.get('to')} 节奏，并重新调整停留密度。"
    if interaction_type == JourneyInteractionType.STOP_REMOVE:
        return f"已移除 {detail.get('stop')}，路线会更轻松一些。"
    if interaction_type == JourneyInteractionType.STOP_REPLACE:
        return f"已将 {detail.get('from')} 替换为 {detail.get('to')}。"
    if interaction_type == JourneyInteractionType.JOURNEY_REGENERATE:
        return f"已按“{detail.get('prompt')}”重新生成路线方向。"
    return "已更新当前旅行路线。"
