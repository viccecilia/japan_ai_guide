from typing import Literal

from pydantic import BaseModel, Field

from app.schemas.answer_card import AnswerCardFood, AnswerCardHotel, AnswerCardNearby


ContentSourceType = Literal["content_library", "template"]


class BaseContent(BaseModel):
    id: str
    slug: str
    content_type: str = "generic"
    title: str
    subtitle: str
    description: str
    story: str
    aliases: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    nearby: list[AnswerCardNearby] = Field(default_factory=list)
    foods: list[AnswerCardFood] = Field(default_factory=list)
    hotels: list[AnswerCardHotel] = Field(default_factory=list)
    priority: int = 50
    updated_at: str = "2026-05-06"
    source: str = "content_library"
    language: str = "zh"


class SpotContent(BaseContent):
    pass


class CityContent(BaseContent):
    pass


class FoodContent(BaseContent):
    pass


class RouteContent(BaseContent):
    pass


class CultureContent(BaseContent):
    pass


class HotelContent(BaseContent):
    pass


class ContentSource(BaseModel):
    type: ContentSourceType
    slug: str | None = None
    language: str | None = None
