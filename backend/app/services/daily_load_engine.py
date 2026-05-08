from app.schemas.journey_timeline import JourneyDay
from app.schemas.travel_constraint import TravelLoad
from app.schemas.traveler_persona import TravelerPersona, TravelStyle


def evaluate_daily_load(day: JourneyDay, persona: TravelerPersona) -> TravelLoad:
    stop_count = sum(len(block.stops) for block in day.blocks)
    score = _base_score(stop_count, day.pace)
    if persona.persona == TravelStyle.ELDER:
        score += 0.22
    elif persona.persona == TravelStyle.FAMILY:
        score += 0.12
    elif persona.persona == TravelStyle.COUPLE:
        score -= 0.04

    level = _level_for_score(score)
    return TravelLoad(
        level=level,
        score=min(1.0, round(score, 2)),
        reason=_reason_for_level(level, stop_count, day.pace, persona.persona.value),
    )


def _base_score(stop_count: int, pace: str) -> float:
    score = 0.2 + stop_count * 0.11
    if pace == "dense":
        score += 0.18
    elif pace == "slow":
        score -= 0.1
    return score


def _level_for_score(score: float) -> str:
    if score >= 0.88:
        return "overload"
    if score >= 0.68:
        return "tight"
    if score <= 0.38:
        return "easy"
    return "normal"


def _reason_for_level(level: str, stop_count: int, pace: str, persona: str) -> str:
    if level == "overload":
        return f"{persona} + {pace} 节奏下安排 {stop_count} 个停留点，体力压力过高。"
    if level == "tight":
        return f"当天停留点较多，建议保留弹性休息时间。"
    if level == "easy":
        return f"当天停留点较少，适合慢节奏体验。"
    return f"当天停留点数量正常，节奏相对均衡。"
