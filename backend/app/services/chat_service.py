from app.schemas.chat import ChatQueryData
from app.services.answer_card_builder import build_multi_card_response
from app.services.intent_router import route_intent
from app.services.token_gate import evaluate_token_gate


def build_mock_answer(question: str, language: str = "zh") -> ChatQueryData:
    intent = route_intent(question, language=language)
    token_gate = evaluate_token_gate()
    response = build_multi_card_response(question, intent, token_gate)
    return ChatQueryData.from_multi_card(question=question, intent=intent, response=response)
