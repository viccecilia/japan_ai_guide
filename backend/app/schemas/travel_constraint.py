from typing import Literal

from pydantic import BaseModel, Field


LoadLevel = Literal["easy", "normal", "tight", "overload"]
FeasibilityLevel = Literal["easy", "balanced", "tight", "overloaded"]


class TravelLoad(BaseModel):
    level: LoadLevel = "normal"
    score: float = 0.5
    reason: str = "节奏正常。"


class FeasibilityScore(BaseModel):
    level: FeasibilityLevel = "balanced"
    score: float = 0.75
    reason: str = "整体节奏均衡。"


class TravelConstraint(BaseModel):
    walking_load: TravelLoad = Field(default_factory=TravelLoad)
    transition_load: TravelLoad = Field(default_factory=TravelLoad)
    daily_density: TravelLoad = Field(default_factory=TravelLoad)
    hotel_distance: TravelLoad = Field(default_factory=TravelLoad)
    estimated_fatigue: TravelLoad = Field(default_factory=TravelLoad)
    timeline_feasibility: FeasibilityScore = Field(default_factory=FeasibilityScore)


class DailyConstraint(BaseModel):
    day_number: int
    city: str
    stop_count: int
    pace: str
    load: TravelLoad


class TransitionConstraint(BaseModel):
    from_city: str
    to_city: str
    estimated_transition_time: str
    transition_type: str
    transition_load: LoadLevel
    reason: str


class HotelConstraint(BaseModel):
    day_number: int
    city: str
    hotel_title: str | None = None
    hotel_distance: LoadLevel = "normal"
    reason: str = "酒店区域与当天城市一致。"


class TimelineConstraint(BaseModel):
    timeline_id: str
    timeline_feasibility: FeasibilityLevel
    feasibility_reason: str
    walking_load: LoadLevel
    transition_load: LoadLevel
    daily_density: LoadLevel
    hotel_distance: LoadLevel
    estimated_fatigue: LoadLevel
    daily_constraints: list[DailyConstraint] = Field(default_factory=list)
    transition_constraints: list[TransitionConstraint] = Field(default_factory=list)
    hotel_constraints: list[HotelConstraint] = Field(default_factory=list)
