from pydantic import BaseModel, Field


class RecommendationGovernance(BaseModel):
    partner_weight: float = Field(default=0, ge=0, le=1)
    relevance_score: float = Field(default=0, ge=0, le=1)
    user_fit_score: float = Field(default=0, ge=0, le=1)
    safety_threshold: float = Field(default=0.6, ge=0, le=1)
    promotion_flag: bool = False
    final_score: float = Field(default=0, ge=0, le=1)
    policy: str = "relevance_first_no_sponsor_override"
