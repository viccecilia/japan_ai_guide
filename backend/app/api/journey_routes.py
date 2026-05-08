from fastapi import APIRouter, HTTPException

from app.schemas.api_response import ApiResponse, success_response
from app.schemas.journey_api import EditableJourneyResponse, JourneyInteractionRequest, JourneyRequest
from app.schemas.journey_storage import JourneyListItem, JourneyRestoreResponse, JourneySaveRequest, SavedJourney
from app.services.journey_session_store import (
    get_journey_state,
    regenerate_journey,
    remove_stop,
    replace_stop,
    save_current_itinerary,
    switch_pace,
    switch_persona,
    to_journey_response,
)
from app.services.journey_storage_service import delete_journey, list_journeys, restore_journey, save_journey

router = APIRouter(prefix="/api/journey", tags=["journey"])


@router.post("/create", response_model=ApiResponse[EditableJourneyResponse])
def create_journey(payload: JourneyRequest) -> ApiResponse[EditableJourneyResponse]:
    session_id = payload.session_id or "jag-local-session"
    state = save_current_itinerary(session_id, payload.itinerary)
    if payload.persona:
        state = switch_persona(session_id, payload.persona)
    if payload.pace:
        state = switch_pace(session_id, payload.pace)
    return success_response(to_journey_response(state), meta={"session_id": session_id})


@router.post("/persona", response_model=ApiResponse[EditableJourneyResponse])
def update_persona(payload: JourneyInteractionRequest) -> ApiResponse[EditableJourneyResponse]:
    if not payload.persona:
        raise HTTPException(status_code=422, detail="persona is required")
    return success_response(to_journey_response(switch_persona(payload.session_id, payload.persona)))


@router.post("/pace", response_model=ApiResponse[EditableJourneyResponse])
def update_pace(payload: JourneyInteractionRequest) -> ApiResponse[EditableJourneyResponse]:
    if not payload.pace:
        raise HTTPException(status_code=422, detail="pace is required")
    return success_response(to_journey_response(switch_pace(payload.session_id, payload.pace)))


@router.post("/remove-stop", response_model=ApiResponse[EditableJourneyResponse])
def remove_journey_stop(payload: JourneyInteractionRequest) -> ApiResponse[EditableJourneyResponse]:
    if not payload.stop_title:
        raise HTTPException(status_code=422, detail="stop_title is required")
    return success_response(to_journey_response(remove_stop(payload.session_id, payload.stop_title)))


@router.post("/replace-stop", response_model=ApiResponse[EditableJourneyResponse])
def replace_journey_stop(payload: JourneyInteractionRequest) -> ApiResponse[EditableJourneyResponse]:
    if not payload.stop_title:
        raise HTTPException(status_code=422, detail="stop_title is required")
    return success_response(
        to_journey_response(replace_stop(payload.session_id, payload.stop_title, payload.replacement_title))
    )


@router.post("/regenerate", response_model=ApiResponse[EditableJourneyResponse])
def regenerate(payload: JourneyInteractionRequest) -> ApiResponse[EditableJourneyResponse]:
    return success_response(to_journey_response(regenerate_journey(payload.session_id, payload.prompt or "重新生成路线")))


@router.post("/save", response_model=ApiResponse[SavedJourney])
def save_active_journey(payload: JourneySaveRequest) -> ApiResponse[SavedJourney]:
    try:
        saved = save_journey(payload)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return success_response(saved, meta={"journey_saved": True})


@router.get("/saved", response_model=ApiResponse[list[JourneyListItem]])
def get_saved_journeys() -> ApiResponse[list[JourneyListItem]]:
    saved = list_journeys()
    return success_response(saved, meta={"saved_journey_count": len(saved)})


@router.get("/saved/{journey_id}", response_model=ApiResponse[JourneyRestoreResponse])
def restore_saved_journey(journey_id: str) -> ApiResponse[JourneyRestoreResponse]:
    restored = restore_journey(journey_id)
    if restored is None:
        raise HTTPException(status_code=404, detail="saved journey not found")
    return success_response(restored, meta={"journey_restored": True})


@router.delete("/saved/{journey_id}", response_model=ApiResponse[dict[str, bool | str]])
def delete_saved_journey(journey_id: str) -> ApiResponse[dict[str, bool | str]]:
    deleted = delete_journey(journey_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="saved journey not found")
    return success_response({"deleted": True, "journey_id": journey_id}, meta={"journey_deleted": True})


@router.get("/{session_id}", response_model=ApiResponse[EditableJourneyResponse])
def get_journey(session_id: str) -> ApiResponse[EditableJourneyResponse]:
    return success_response(to_journey_response(get_journey_state(session_id)))
