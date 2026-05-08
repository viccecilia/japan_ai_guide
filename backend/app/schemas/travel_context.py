from typing import Literal

from pydantic import BaseModel, Field

from app.schemas.journey_timeline import JourneyTimeline


WeatherKind = Literal["sunny", "rainy", "hot", "crowded"]
TimeOfDay = Literal["morning", "afternoon", "evening", "late"]
ContextLevel = Literal["calm", "watch", "adjust", "urgent"]


class WeatherContext(BaseModel):
    condition: WeatherKind = "sunny"
    summary: str = "天气稳定，适合按原计划出行。"
    outdoor_pressure: str = "normal"


class TimeContext(BaseModel):
    time_of_day: TimeOfDay = "morning"
    summary: str = "时间充足，可以按正常节奏推进。"
    long_transition_allowed: bool = True


class FatigueContext(BaseModel):
    travel_fatigue: str = "normal"
    accumulated_dense_days: int = 0
    summary: str = "当前体力负担正常。"


class JourneyCondition(BaseModel):
    daily_density: str = "normal"
    context_level: ContextLevel = "calm"
    adaptation_reason: str = "当前旅行状态稳定。"


class ContextualSuggestion(BaseModel):
    suggestion_type: str
    title: str
    description: str
    trigger_context: str
    priority: int = 1


class TravelContext(BaseModel):
    weather: WeatherContext = Field(default_factory=WeatherContext)
    time: TimeContext = Field(default_factory=TimeContext)
    fatigue: FatigueContext = Field(default_factory=FatigueContext)
    condition: JourneyCondition = Field(default_factory=JourneyCondition)
    suggestions: list[ContextualSuggestion] = Field(default_factory=list)
    context_optimized_timeline: JourneyTimeline | None = None
    contextual_adaptation_count: int = 0
    narrative: str = "当前路线可以按原计划推进。"
