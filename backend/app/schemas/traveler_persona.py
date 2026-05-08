from enum import Enum

from pydantic import BaseModel, Field


class TravelPace(str, Enum):
    SLOW = "slow"
    NORMAL = "normal"
    DENSE = "dense"


class TravelStyle(str, Enum):
    FIRST_TIME = "first_time"
    FAMILY = "family"
    COUPLE = "couple"
    ELDER = "elder"
    FOODIE = "foodie"
    CULTURE = "culture"
    SHOPPING = "shopping"
    ANIME = "anime"
    SOLO = "solo"


class TravelerPreference(BaseModel):
    pace: TravelPace = TravelPace.NORMAL
    walking_tolerance: str = "medium"
    budget_level: str = "mid"
    food_interest: int = 3
    culture_interest: int = 3
    shopping_interest: int = 2
    photo_interest: int = 3
    family_friendly: bool = False


class TravelerPersona(BaseModel):
    persona: TravelStyle = TravelStyle.FIRST_TIME
    label: str = "适合第一次来日本"
    preference: TravelerPreference = Field(default_factory=TravelerPreference)
    confidence: float = 0.7
    detected_by: str = "heuristic"
    journey_style: str = "classic_first_time"
