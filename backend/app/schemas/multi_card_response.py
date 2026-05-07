from pydantic import BaseModel, Field

from app.schemas.answer_card import AnswerCard


class MainAnswerCard(AnswerCard):
    card_group: str = "main"
    display_priority: int = 100
    display_style: str = "large"


class RelatedAnswerCard(AnswerCard):
    card_group: str = "related"
    display_priority: int = 50
    display_style: str = "compact"


class RecommendationSection(BaseModel):
    section_type: str
    title: str
    cards: list[RelatedAnswerCard] = Field(default_factory=list)


class MultiCardResponse(BaseModel):
    main_card: MainAnswerCard
    related_cards: list[RelatedAnswerCard] = Field(default_factory=list)
    sections: list[RecommendationSection] = Field(default_factory=list)
    metadata: dict[str, object] = Field(default_factory=dict)
