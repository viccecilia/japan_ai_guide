from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class AnalyticsEventType(str, Enum):
    QUERY_SUBMITTED = "query_submitted"
    CARD_IMPRESSION = "card_impression"
    CARD_CLICK = "card_click"
    SECTION_VIEW = "section_view"
    PROMPT_CLICK = "prompt_click"
    EXTERNAL_JUMP = "external_jump"
    CONVERSATION_CONTINUE = "conversation_continue"
    PERSONA_SWITCH = "persona_switch"
    PACE_SWITCH = "pace_switch"
    STOP_REMOVE = "stop_remove"
    STOP_REPLACE = "stop_replace"
    JOURNEY_REGENERATE = "journey_regenerate"


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class AnalyticsEvent(BaseModel):
    event_type: AnalyticsEventType
    session_id: str
    query: str | None = None
    intent: str | None = None
    card_slug: str | None = None
    section_type: str | None = None
    position: int | None = None
    source: str = "server"
    timestamp: datetime = Field(default_factory=utc_now)
    metadata: dict[str, Any] = Field(default_factory=dict)
