from fastapi import APIRouter

from app.schemas.api_response import ApiResponse, success_response
from app.schemas.language import LanguageListData
from app.services.language_service import list_supported_languages

router = APIRouter(prefix="/api/language", tags=["language"])


@router.get("/list", response_model=ApiResponse[LanguageListData])
def list_languages() -> ApiResponse[LanguageListData]:
    return success_response(list_supported_languages(), meta={"mock": True})
