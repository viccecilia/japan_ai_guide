from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field

from app.schemas.intent import IntentResult


class CardType(str, Enum):
    SPOT = "spot_card"
    CITY = "city_card"
    FOOD = "food_card"
    ROUTE = "route_card"
    CULTURE = "culture_card"
    GENERIC = "generic_card"


FieldSource = Literal["ai", "database", "mock", "computed"]
NearbyType = Literal["spot", "station", "shop", "restaurant", "hotel", "other"]
ActionType = Literal["ask_followup", "create_route", "save_to_trip", "open_map", "play_audio", "open_charter"]


class AnswerCardAudio(BaseModel):
    text: str | None = None
    voice: str | None = None
    audio_url: str | None = None
    duration_seconds: int | None = None
    source: FieldSource | None = None


class AnswerCardNearby(BaseModel):
    id: str | None = None
    name: str
    type: NearbyType | None = None
    distance_text: str | None = None
    description: str | None = None
    source: FieldSource | None = None


class AnswerCardFood(BaseModel):
    name: str
    description: str | None = None
    area: str | None = None
    source: FieldSource | None = None


class AnswerCardHotel(BaseModel):
    name: str
    description: str | None = None
    area: str | None = None
    source: FieldSource | None = None


class AnswerCardAction(BaseModel):
    label: str
    action: ActionType
    enabled: bool = True
    payload: dict[str, str | int | float | bool] = Field(default_factory=dict)
    source: FieldSource | None = None


class AnswerCardMetadata(BaseModel):
    language: str = "zh-CN"
    mock: bool = True
    sources: list[FieldSource] = Field(default_factory=list)
    ai_fields: list[str] = Field(default_factory=list)
    database_fields: list[str] = Field(default_factory=list)
    intent: IntentResult | None = None
    ai_runtime: dict[str, str | bool | int | float] = Field(default_factory=dict)
    content_source: dict[str, str | bool | int | float] = Field(default_factory=dict)
    cache: dict[str, str | bool | int | float] = Field(default_factory=dict)
    ranking: dict[str, str | bool | int | float | None] = Field(default_factory=dict)
    related_candidates: list[dict[str, str | bool | int | float | None]] = Field(default_factory=list)
    card_groups: dict[str, int] = Field(default_factory=dict)
    orchestration: dict[str, object] = Field(default_factory=dict)


class AnswerCard(BaseModel):
    id: str
    card_type: CardType
    title: str
    subtitle: str
    description: str
    story: str
    audio: AnswerCardAudio = Field(default_factory=AnswerCardAudio)
    nearby: list[AnswerCardNearby] = Field(default_factory=list)
    foods: list[AnswerCardFood] = Field(default_factory=list)
    hotels: list[AnswerCardHotel] = Field(default_factory=list)
    actions: list[AnswerCardAction] = Field(default_factory=list)
    metadata: AnswerCardMetadata = Field(default_factory=AnswerCardMetadata)
    card_group: str = "main"
    display_priority: int = 100
    display_style: str = "large"
    recommendation_reason: str | None = None
