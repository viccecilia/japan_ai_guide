from uuid import uuid4

from app.schemas.editable_itinerary import JourneyInteraction, JourneyInteractionType
from app.schemas.journey_storage import JourneyListItem, JourneyRestoreResponse, JourneySaveRequest, SavedJourney, utc_now
from app.services.journey_session_store import JOURNEY_SESSIONS, get_journey_state, to_journey_response


SAVED_JOURNEYS: dict[str, SavedJourney] = {}


def save_journey(payload: JourneySaveRequest) -> SavedJourney:
    state = get_journey_state(payload.session_id)
    response = to_journey_response(state)
    if response.editable_itinerary is None:
        raise ValueError("No active journey session to save.")
    itinerary = response.editable_itinerary.itinerary
    journey_id = uuid4().hex
    now = utc_now()
    saved = SavedJourney(
        journey_id=journey_id,
        session_id=payload.session_id,
        user_id=payload.user_id,
        title=payload.title or itinerary.title,
        city=itinerary.city,
        persona=response.editable_itinerary.current_persona,
        pace=response.editable_itinerary.current_pace,
        editable_itinerary=response.editable_itinerary,
        interaction_history=response.interaction_history,
        analytics=response.analytics,
        replay={**response.replay, "journey_saved": True, "journey_id": journey_id},
        created_at=now,
        updated_at=now,
        status="saved",
    )
    SAVED_JOURNEYS[journey_id] = saved
    return saved


def restore_journey(journey_id: str) -> JourneyRestoreResponse | None:
    saved = SAVED_JOURNEYS.get(journey_id)
    if saved is None or saved.status == "deleted":
        return None
    JOURNEY_SESSIONS[saved.session_id] = get_journey_state(saved.session_id).model_copy(
        update={
            "current_itinerary": saved.editable_itinerary,
            "persona": saved.persona,
            "pace": saved.pace,
            "interaction_history": [
                JourneyInteraction.model_validate(item) for item in saved.interaction_history
            ],
        }
    )
    saved.replay["journey_restored"] = True
    saved.updated_at = utc_now()
    return JourneyRestoreResponse(
        saved_journey=saved,
        restored_session_id=saved.session_id,
        analytics={
            "journey_restored": True,
            "saved_journey_count": len(list_journeys()),
        },
        replay=saved.replay,
    )


def list_journeys() -> list[JourneyListItem]:
    return [
        JourneyListItem(
            journey_id=item.journey_id,
            session_id=item.session_id,
            user_id=item.user_id,
            title=item.title,
            city=item.city,
            persona=item.persona,
            pace=item.pace,
            updated_at=item.updated_at,
            status=item.status,
        )
        for item in sorted(SAVED_JOURNEYS.values(), key=lambda record: record.updated_at, reverse=True)
        if item.status != "deleted"
    ]


def delete_journey(journey_id: str) -> bool:
    saved = SAVED_JOURNEYS.get(journey_id)
    if saved is None or saved.status == "deleted":
        return False
    saved.status = "deleted"
    saved.updated_at = utc_now()
    saved.interaction_history.append(
        JourneyInteraction(
            interaction_type=JourneyInteractionType.JOURNEY_REGENERATE,
            detail={"journey_id": journey_id, "storage_action": "delete"},
            narrative="已删除保存的路线。",
        ).model_dump()
    )
    saved.replay["journey_deleted"] = True
    return True
