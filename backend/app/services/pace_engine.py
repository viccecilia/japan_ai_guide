from app.schemas.traveler_persona import TravelerPersona, TravelPace


def stop_limit_for_persona(persona: TravelerPersona) -> int:
    if persona.preference.pace == TravelPace.SLOW:
        return 3
    if persona.preference.pace == TravelPace.DENSE:
        return 6
    return 5


def block_titles_for_persona(persona: TravelerPersona) -> tuple[str, str]:
    if persona.preference.pace == TravelPace.SLOW:
        return "上午慢慢进入状态", "下午留出休息余地"
    if persona.preference.pace == TravelPace.DENSE:
        return "上午高效串联重点", "下午继续补足体验"
    return "上午先抓主线", "下午补足体验"


def estimated_total_time(persona: TravelerPersona, duration: str) -> str:
    if persona.preference.pace == TravelPace.SLOW:
        return "约3-5小时" if duration == "half_day" else "约6-8小时"
    if persona.preference.pace == TravelPace.DENSE:
        return "约5-6小时" if duration == "half_day" else "约8-10小时"
    return "约4-6小时" if duration == "half_day" else "约7-9小时"


def break_note_for_persona(persona: TravelerPersona) -> str:
    if persona.preference.pace == TravelPace.SLOW:
        return "建议每1-2个点之间安排休息，减少连续步行。"
    if persona.preference.pace == TravelPace.DENSE:
        return "路线较紧凑，建议提前确认交通和开放时间。"
    return "中段保留用餐和休息时间，避免行程过满。"
