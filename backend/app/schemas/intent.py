from enum import Enum

from pydantic import BaseModel, Field


class IntentType(str, Enum):
    SPOT = "spot_query"
    CITY = "city_query"
    FOOD = "food_query"
    ROUTE = "route_query"
    CULTURE = "culture_query"
    HOTEL = "hotel_query"
    GENERIC = "generic_query"
    UNKNOWN = "unknown"


class IntentResult(BaseModel):
    intent_type: IntentType
    entity: str | None = None
    city: str | None = None
    language: str = "zh"
    confidence: float = Field(ge=0, le=1)
