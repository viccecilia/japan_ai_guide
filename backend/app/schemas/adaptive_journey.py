from typing import Literal

from pydantic import BaseModel, Field

from app.schemas.journey_timeline import JourneyTimeline
from app.schemas.travel_constraint import TimelineConstraint


AdaptationType = Literal["auto_balance", "stop_reduce", "transition_reduce", "pace_optimize", "rest_insert"]


class AdaptiveSuggestion(BaseModel):
    adaptation_type: AdaptationType
    title: str
    description: str
    trigger_reason: str
    day_number: int | None = None
    priority: int = 1


class RegenerationReason(BaseModel):
    before_feasibility: str
    trigger_reason: str
    user_facing_reason: str


class JourneyAdaptation(BaseModel):
    adaptation_type: AdaptationType
    trigger_reason: str
    before_feasibility: str
    after_feasibility: str
    removed_stops: list[str] = Field(default_factory=list)
    reordered_stops: list[str] = Field(default_factory=list)
    transition_reduction: int = 0
    fatigue_reduction: str = "none"
    narrative: str


class AdaptationResult(BaseModel):
    applied: bool = False
    before_feasibility: str = "balanced"
    after_feasibility: str = "balanced"
    suggestions: list[AdaptiveSuggestion] = Field(default_factory=list)
    adaptations: list[JourneyAdaptation] = Field(default_factory=list)
    optimized_timeline: JourneyTimeline | None = None
    optimized_constraint: TimelineConstraint | None = None
    regeneration_reason: RegenerationReason | None = None
    fatigue_reduction: str = "none"
    transition_reduction: int = 0
    adaptation_count: int = 0
    narrative: str = "当前路线不需要明显调整。"
