from fastapi import APIRouter

from app.schemas.api_response import ApiResponse, success_response
from app.schemas.chat import ChatQueryData, ChatQueryRequest
from app.services.chat_service import build_mock_answer

router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post("/query", response_model=ApiResponse[ChatQueryData])
def query_chat(payload: ChatQueryRequest) -> ApiResponse[ChatQueryData]:
    question = payload.question or payload.query or ""
    return success_response(
        build_mock_answer(question, language=payload.language),
        meta={"mock": True, "language": payload.language},
    )
