from pydantic import BaseModel, Field


class TrafficOverview(BaseModel):
    total_sessions: int = 0
    top_sources: list[dict[str, int | str]] = Field(default_factory=list)


class QueryOverview(BaseModel):
    total_queries: int = 0
    top_queries: list[dict[str, int | str]] = Field(default_factory=list)


class RecommendationCtr(BaseModel):
    section_type: str
    impressions: int = 0
    clicks: int = 0
    ctr: float = 0.0


class JourneyReplayItem(BaseModel):
    session_id: str
    query_sequence: list[str] = Field(default_factory=list)
    intent_evolution: list[str] = Field(default_factory=list)
    persona_evolution: list[str | None] = Field(default_factory=list)
    interaction_history: list[dict[str, object]] = Field(default_factory=list)
    recommendation_path: list[dict[str, object]] = Field(default_factory=list)


class OperatorDashboardSnapshot(BaseModel):
    traffic_overview: TrafficOverview = Field(default_factory=TrafficOverview)
    query_overview: QueryOverview = Field(default_factory=QueryOverview)
    top_intents: list[dict[str, int | str]] = Field(default_factory=list)
    recommendation_ctr: list[RecommendationCtr] = Field(default_factory=list)
    traffic_source: list[dict[str, int | str]] = Field(default_factory=list)
    journey_replay: list[JourneyReplayItem] = Field(default_factory=list)
    governance_status: dict[str, str | bool] = Field(default_factory=dict)
