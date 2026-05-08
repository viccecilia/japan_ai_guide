from pydantic import BaseModel, Field

from app.schemas.editable_itinerary import EditableItinerary, JourneyState
from app.schemas.itinerary import Itinerary


class JourneyRequest(BaseModel):
    session_id: str | None = None
    itinerary: Itinerary
    persona: str | None = None
    pace: str | None = None


class JourneyInteractionRequest(BaseModel):
    session_id: str
    persona: str | None = None
    pace: str | None = None
    stop_title: str | None = None
    replacement_title: str | None = None
    prompt: str | None = None


class JourneyAnalytics(BaseModel):
    journey_session_id: str
    interaction_count: int = 0
    regeneration_count: int = 0
    persona_changes: int = 0
    pace_changes: int = 0
    latest_interaction_type: str | None = None


class JourneyResponse(BaseModel):
    journey_state: JourneyState
    editable_itinerary: EditableItinerary | None = None
    interaction_history: list[dict[str, object]] = Field(default_factory=list)
    analytics: JourneyAnalytics
    replay: dict[str, object] = Field(default_factory=dict)


class EditableJourneyResponse(JourneyResponse):
    pass
