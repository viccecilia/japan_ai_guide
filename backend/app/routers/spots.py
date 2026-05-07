from fastapi import APIRouter

from app.schemas.api_response import ApiResponse, success_response
from app.schemas.spot import SpotSearchData, SpotSearchRequest
from app.services.spot_service import search_mock_spots

router = APIRouter(prefix="/api/spots", tags=["spots"])


@router.post("/search", response_model=ApiResponse[SpotSearchData])
def search_spots(payload: SpotSearchRequest) -> ApiResponse[SpotSearchData]:
    return success_response(
        search_mock_spots(payload.query),
        meta={"mock": True, "language": payload.language},
    )
