from app.schemas.answer_card import AnswerCard
from app.schemas.traveler_persona import TravelerPersona, TravelStyle


def build_stop_narrative(card: AnswerCard, index: int, route_type: str, persona: TravelerPersona) -> str:
    label = persona.label
    if index == 0:
        return f"先从{card.title}开始，{label}时更容易建立整条路线的方向感。"
    if persona.persona == TravelStyle.ELDER:
        return f"接着到{card.title}，这一站建议放慢节奏，中间留出休息时间。"
    if persona.persona == TravelStyle.FAMILY:
        return f"然后去{card.title}，让路线保留轻松和互动感，避免孩子太快疲劳。"
    if persona.persona == TravelStyle.COUPLE:
        return f"之后安排{card.title}，适合边走边看，给傍晚散步留出空间。"
    if route_type == "food":
        return f"接着把{card.title}放进中段，让路线不只是看景点，也有当地味道。"
    if route_type == "culture":
        return f"然后继续到{card.title}，把前面的背景故事和现场体验连起来。"
    return f"之后前往{card.title}，保持顺路节奏，避免一天里来回折返。"


def build_itinerary_narrative(title: str, route_type: str, persona: TravelerPersona) -> str:
    if persona.persona == TravelStyle.ELDER:
        return f"{title}会减少连续步行，把休息和交通便利放在前面，适合带老人慢慢体验。"
    if persona.persona == TravelStyle.FAMILY:
        return f"{title}会控制停留密度，优先选择轻松、有互动感、适合亲子节奏的安排。"
    if persona.persona == TravelStyle.COUPLE:
        return f"{title}会保留散步和拍照空间，适合情侣用更松弛的节奏体验城市。"
    if persona.persona == TravelStyle.FOODIE:
        return f"{title}会把用餐体验插入路线中段，避免只做景点打卡。"
    if persona.persona == TravelStyle.CULTURE:
        return f"{title}会先建立背景理解，再进入更适合慢慢看的地点。"
    if route_type == "one_day":
        return f"{title}会把上午、午间和下午节奏拆开，先看核心地点，再补美食和文化体验。"
    return f"{title}适合作为个性化旅行流，重点是顺路、清晰、不会过度塞满。"
