from fastapi import APIRouter

from app.schemas.api_response import ApiResponse, success_response
from app.schemas.history import HistoryListData
from app.services.history_service import list_mock_history

router = APIRouter(prefix="/api/history", tags=["history"])


@router.get("/list", response_model=ApiResponse[HistoryListData])
def list_history() -> ApiResponse[HistoryListData]:
    return success_response(list_mock_history(), meta={"mock": True})
