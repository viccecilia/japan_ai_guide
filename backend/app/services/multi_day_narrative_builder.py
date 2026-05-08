from app.schemas.journey_timeline import JourneyTransition


def day_narrative(day_number: int, city: str, pace: str) -> str:
    if day_number == 1:
        return f"Day {day_number} 先体验{city}的经典区域，建立整趟旅程的方向感。"
    if pace == "slow":
        return f"Day {day_number} 节奏放慢，适合深入{city}的街区和文化细节，中间保留休息时间。"
    if pace == "dense":
        return f"Day {day_number} 停留密度更高，建议午间安排休息，避免傍晚前体力透支。"
    return f"Day {day_number} 继续补足{city}的代表体验，让路线保持连续。"


def transition_narrative(from_city: str, to_city: str, load: str = "normal") -> str:
    base = f"从{from_city}前往{to_city}时，建议把跨城移动放在上午或午后早段，避免挤压当天体验。"
    if load == "high":
        return f"{base} 这段移动会增加疲劳，抵达后当天不建议再安排太多景点。"
    return base


def build_transition(from_city: str, to_city: str) -> JourneyTransition:
    time = {
        ("东京", "京都"): "约2小时15分钟",
        ("京都", "大阪"): "约30-45分钟",
        ("大阪", "京都"): "约30-45分钟",
        ("京都", "奈良"): "约45-60分钟",
        ("东京", "大阪"): "约2小时30分钟",
        ("大阪", "东京"): "约2小时30分钟",
    }.get((from_city, to_city), "约1-3小时")
    transition_load = "high" if "2小时" in time or "3小时" in time else "normal"
    transport = "新干线" if {from_city, to_city} & {"东京"} else "JR / 私铁"
    return JourneyTransition(
        from_city=from_city,
        to_city=to_city,
        recommended_transport=transport,
        estimated_travel_time=time,
        estimated_transition_time=time,
        transition_type="shinkansen" if transport == "新干线" else "rail",
        transition_load=transition_load,
        narrative=transition_narrative(from_city, to_city, transition_load),
    )
