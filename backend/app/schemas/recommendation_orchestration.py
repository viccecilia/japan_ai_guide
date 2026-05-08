from pydantic import BaseModel, Field

from app.schemas.intent import IntentType


class SectionPlan(BaseModel):
    section_type: str
    content_type: str | None = None
    max_cards: int = 2
    reason: str = ""


class RecommendationRule(BaseModel):
    intent_type: IntentType
    strategy: str
    section_order: list[str]
    max_cards_per_section: int = 2
    reason: str


class OrchestrationContext(BaseModel):
    intent_type: IntentType
    main_slug: str | None = None
    main_content_type: str | None = None
    candidate_groups: dict[str, list[dict[str, str | float | int | None]]] = Field(default_factory=dict)


class RecommendationPlan(BaseModel):
    intent_type: IntentType
    strategy: str
    main_content_type: str | None = None
    section_order: list[str] = Field(default_factory=list)
    max_cards_per_section: int = 2
    dedupe_keys: list[str] = Field(default_factory=list)
    deduped_count: int = 0
    reason: str
    related_candidates: list[dict[str, str | float | int | None]] = Field(default_factory=list)
    section_candidates: dict[str, list[dict[str, str | float | int | None]]] = Field(default_factory=dict)
    suggested_prompts: list[str] = Field(default_factory=list)
