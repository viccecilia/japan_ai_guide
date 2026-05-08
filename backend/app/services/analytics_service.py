from app.schemas.analytics_event import AnalyticsEvent, AnalyticsEventType


EVENTS: list[AnalyticsEvent] = []


def track_event(event: AnalyticsEvent) -> AnalyticsEvent:
    EVENTS.append(event)
    return event


def track_query(session_id: str, query: str, intent: str, metadata: dict[str, object] | None = None) -> AnalyticsEvent:
    return track_event(
        AnalyticsEvent(
            event_type=AnalyticsEventType.QUERY_SUBMITTED,
            session_id=session_id,
            query=query,
            intent=intent,
            metadata=metadata or {},
        )
    )


def track_recommendation(
    session_id: str,
    event_type: AnalyticsEventType,
    query: str,
    intent: str,
    card_slug: str | None = None,
    section_type: str | None = None,
    position: int | None = None,
    metadata: dict[str, object] | None = None,
) -> AnalyticsEvent:
    return track_event(
        AnalyticsEvent(
            event_type=event_type,
            session_id=session_id,
            query=query,
            intent=intent,
            card_slug=card_slug,
            section_type=section_type,
            position=position,
            metadata=metadata or {},
        )
    )


def track_external_jump(
    session_id: str,
    query: str,
    intent: str,
    card_slug: str,
    jump_type: str,
    destination: str,
) -> AnalyticsEvent:
    return track_event(
        AnalyticsEvent(
            event_type=AnalyticsEventType.EXTERNAL_JUMP,
            session_id=session_id,
            query=query,
            intent=intent,
            card_slug=card_slug,
            source="external_jump",
            metadata={"jump_type": jump_type, "destination": destination},
        )
    )


def event_count(session_id: str | None = None) -> int:
    if session_id is None:
        return len(EVENTS)
    return sum(1 for event in EVENTS if event.session_id == session_id)


def recent_events(session_id: str, limit: int = 20) -> list[dict[str, object]]:
    return [event.model_dump(mode="json") for event in EVENTS if event.session_id == session_id][-limit:]
