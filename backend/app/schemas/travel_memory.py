from pydantic import BaseModel, Field


class JourneyPreference(BaseModel):
    preferred_pace: str = "normal"
    preferred_cities: list[str] = Field(default_factory=list)
    preferred_persona: str = "first_time"
    preferred_journey_style: str = "classic_first_time"
    crowd_tolerance: str = "medium"
    walking_tolerance: str = "medium"
    fatigue_preference: str = "normal"
    last_journey_style: str = "classic_first_time"


class PreferenceMemory(BaseModel):
    pace_votes: dict[str, int] = Field(default_factory=dict)
    city_votes: dict[str, int] = Field(default_factory=dict)
    persona_votes: dict[str, int] = Field(default_factory=dict)
    style_votes: dict[str, int] = Field(default_factory=dict)
    disliked_contexts: list[str] = Field(default_factory=list)


class PreferenceEvolution(BaseModel):
    field: str
    before: str | None = None
    after: str
    reason: str


class MemorySnapshot(BaseModel):
    session_id: str
    preference: JourneyPreference = Field(default_factory=JourneyPreference)
    summary: str = "我会先按均衡节奏为你规划。"
    evolution: list[PreferenceEvolution] = Field(default_factory=list)


class TravelMemory(BaseModel):
    session_id: str
    preference: JourneyPreference = Field(default_factory=JourneyPreference)
    memory: PreferenceMemory = Field(default_factory=PreferenceMemory)
    evolution: list[PreferenceEvolution] = Field(default_factory=list)
    memory_updates: int = 0
