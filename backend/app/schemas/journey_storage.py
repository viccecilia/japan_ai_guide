from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field

from app.schemas.editable_itinerary import EditableItinerary
from app.schemas.journey_api import JourneyAnalytics


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class JourneySaveRequest(BaseModel):
    session_id: str
    user_id: str | None = None
    title: str | None = None


class JourneyListItem(BaseModel):
    journey_id: str
    session_id: str
    user_id: str | None = None
    title: str
    city: str | None = None
    persona: str | None = None
    pace: str | None = None
    updated_at: datetime
    status: str = "saved"


class SavedJourney(BaseModel):
    journey_id: str
    session_id: str
    user_id: str | None = None
    title: str
    city: str | None = None
    persona: str | None = None
    pace: str | None = None
    editable_itinerary: EditableItinerary
    interaction_history: list[dict[str, Any]] = Field(default_factory=list)
    analytics: JourneyAnalytics
    replay: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)
    status: str = "saved"


class JourneyStorageRecord(SavedJourney):
    pass


class JourneyRestoreResponse(BaseModel):
    saved_journey: SavedJourney
    restored_session_id: str
    analytics: dict[str, Any] = Field(default_factory=dict)
    replay: dict[str, Any] = Field(default_factory=dict)
