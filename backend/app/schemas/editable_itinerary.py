from datetime import datetime, timezone
from enum import Enum

from pydantic import BaseModel, Field

from app.schemas.itinerary import Itinerary, ItineraryStop


class JourneyInteractionType(str, Enum):
    PERSONA_SWITCH = "persona_switch"
    PACE_SWITCH = "pace_switch"
    STOP_REMOVE = "stop_remove"
    STOP_REPLACE = "stop_replace"
    JOURNEY_REGENERATE = "journey_regenerate"


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class EditableStop(ItineraryStop):
    active: bool = True
    replaced_by: str | None = None


class JourneyInteraction(BaseModel):
    interaction_type: JourneyInteractionType
    detail: dict[str, str | int | bool | None] = Field(default_factory=dict)
    narrative: str
    timestamp: datetime = Field(default_factory=utc_now)


class EditableItinerary(BaseModel):
    itinerary: Itinerary
    current_persona: str | None = None
    current_pace: str | None = None
    active_stops: list[EditableStop] = Field(default_factory=list)
    removed_stops: list[EditableStop] = Field(default_factory=list)
    replaced_stops: list[dict[str, str]] = Field(default_factory=list)
    interaction_history: list[JourneyInteraction] = Field(default_factory=list)


class JourneyState(BaseModel):
    session_id: str
    current_itinerary: EditableItinerary | None = None
    persona: str | None = None
    pace: str | None = None
    edited_stops: list[str] = Field(default_factory=list)
    interaction_history: list[JourneyInteraction] = Field(default_factory=list)
