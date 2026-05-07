from app.schemas.content_library import BaseContent
from app.schemas.intent import IntentResult, IntentType
from app.services.content_index import get_content_index
from app.services.content_library_loader import (
    load_city_content,
    load_culture_content,
    load_food_content,
    load_hotel_content,
    load_route_content,
    load_spot_content,
)
from app.services.query_ranking import RankingResult, rank_query, rank_top_k


class ContentRepository:
    def find_by_slug(self, slug: str, language: str, content_type: str | None = None) -> BaseContent | None:
        loaders = {
            "spot": load_spot_content,
            "city": load_city_content,
            "food": load_food_content,
            "route": load_route_content,
            "culture": load_culture_content,
            "hotel": load_hotel_content,
        }
        if content_type in loaders:
            return loaders[content_type](slug, language)
        for loader in loaders.values():
            content = loader(slug, language)
            if content is not None:
                return content
        return None

    def search(self, query: str, intent_type: IntentType, language: str) -> str | None:
        index = get_content_index()
        ranking = rank_query(query, _IntentLike(intent_type, language), index)
        return ranking.slug

    def search_candidates(
        self,
        query: str,
        intent_type: IntentType,
        language: str,
        top_k: int = 5,
    ) -> list[RankingResult]:
        index = get_content_index()
        return rank_top_k(query, _IntentLike(intent_type, language), index, top_k=top_k)


class _IntentLike(IntentResult):
    def __init__(self, intent_type: IntentType, language: str) -> None:
        super().__init__(intent_type=intent_type, language=language, confidence=0.5)


content_repository = ContentRepository()
