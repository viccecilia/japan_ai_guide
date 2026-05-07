from pydantic import BaseModel, Field, model_validator

from app.schemas.answer_card import AnswerCard
from app.schemas.intent import IntentResult
from app.schemas.multi_card_response import MultiCardResponse, RecommendationSection, RelatedAnswerCard


class ChatQueryRequest(BaseModel):
    question: str | None = Field(default=None, min_length=1, max_length=500)
    query: str | None = Field(default=None, min_length=1, max_length=500)
    language: str = Field(default="zh", max_length=20)

    @model_validator(mode="after")
    def require_question_or_query(self) -> "ChatQueryRequest":
        if not self.question and not self.query:
            raise ValueError("Either question or query is required.")
        if not self.question:
            self.question = self.query
        return self


class ChatQueryData(BaseModel):
    question: str
    intent: IntentResult
    answer_card: AnswerCard
    main_card: AnswerCard
    related_cards: list[RelatedAnswerCard] = Field(default_factory=list)
    sections: list[RecommendationSection] = Field(default_factory=list)
    metadata: dict[str, object] = Field(default_factory=dict)

    @classmethod
    def from_multi_card(
        cls,
        question: str,
        intent: IntentResult,
        response: MultiCardResponse,
    ) -> "ChatQueryData":
        return cls(
            question=question,
            intent=intent,
            answer_card=response.main_card,
            main_card=response.main_card,
            related_cards=response.related_cards,
            sections=response.sections,
            metadata=response.metadata,
        )
