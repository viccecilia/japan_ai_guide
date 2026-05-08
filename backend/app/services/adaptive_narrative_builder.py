from app.schemas.adaptive_journey import JourneyAdaptation


def adaptation_summary(before: str, after: str, adaptations: list[JourneyAdaptation]) -> str:
    if not adaptations:
        return "当前路线已经比较稳定，可以按现有节奏继续规划。"
    if after in {"balanced", "easy"}:
        return "已调整为更适合实际旅行的路线，减少体力压力并保留核心体验。"
    if after == "tight":
        return "已降低路线负担，但仍建议把跨城日安排得更轻松。"
    return "已做初步减负，但这条路线仍偏满，建议继续减少停留点。"


def adaptation_narrative(adaptation_type: str, day_number: int | None = None) -> str:
    if adaptation_type == "stop_reduce":
        return f"已降低 Day {day_number} 的停留密度，让当天更容易完成。" if day_number else "已减少部分停留点。"
    if adaptation_type == "transition_reduce":
        return "已减少重复跨城移动，降低交通疲劳。"
    if adaptation_type == "pace_optimize":
        return "已把节奏调整得更轻松，保留更多休息空间。"
    if adaptation_type == "rest_insert":
        return "已插入休息提示，避免连续赶场。"
    return "已自动平衡多日行程。"
