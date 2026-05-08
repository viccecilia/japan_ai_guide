from dataclasses import dataclass

from app.schemas.intent import IntentResult, IntentType
from app.services.content_index import ContentIndexItem


@dataclass(frozen=True)
class RankingResult:
    slug: str | None
    score: float
    matched_by: str
    content_type: str | None = None
    priority: int = 0

    def as_metadata(self) -> dict[str, str | float | int | None]:
        return {
            "slug": self.slug,
            "score": self.score,
            "matched_by": self.matched_by,
            "content_type": self.content_type,
            "priority": self.priority,
        }


INTENT_CONTENT_TYPES = {
    IntentType.SPOT: {"spot", "city", "food", "route", "culture", "hotel"},
    IntentType.CITY: {"city", "spot", "food", "route", "culture", "hotel"},
    IntentType.FOOD: {"food", "city", "spot"},
    IntentType.ROUTE: {"route", "spot", "city", "food"},
    IntentType.CULTURE: {"culture", "spot", "city"},
    IntentType.HOTEL: {"hotel", "city", "spot"},
}


def rank_query(query: str, intent: IntentResult, index: list[ContentIndexItem]) -> RankingResult:
    results = rank_top_k(query, intent, index, top_k=1)
    if results:
        return results[0]
    return RankingResult(slug=None, score=0, matched_by="none")


def rank_top_k(
    query: str,
    intent: IntentResult,
    index: list[ContentIndexItem],
    top_k: int = 5,
) -> list[RankingResult]:
    candidates = _filter_candidates(intent, index)
    normalized_query = query.strip().lower()
    target_values = [value for value in [intent.entity, intent.city, query] if value]
    results: list[RankingResult] = []

    for item in candidates:
        score, matched_by = _score_item(normalized_query, target_values, item)
        score = _apply_intent_cap(intent.intent_type, item.content_type, score)
        if score <= 0:
            continue
        results.append(
            RankingResult(
                slug=item.slug,
                score=score,
                matched_by=matched_by,
                content_type=item.content_type,
                priority=item.priority,
            )
        )

    results.sort(key=lambda result: (result.score, _type_weight(intent.intent_type, result.content_type), result.priority), reverse=True)
    return results[:top_k]


def _filter_candidates(intent: IntentResult, index: list[ContentIndexItem]) -> list[ContentIndexItem]:
    allowed_types = INTENT_CONTENT_TYPES.get(intent.intent_type)
    return [
        item
        for item in index
        if item.language == intent.language and (allowed_types is None or item.content_type in allowed_types)
    ]


def _score_item(query: str, target_values: list[str], item: ContentIndexItem) -> tuple[float, str]:
    title = item.title.lower()
    aliases = [alias.lower() for alias in item.aliases]
    tags = [tag.lower() for tag in item.tags]
    slug = item.slug.lower()
    targets = [value.lower() for value in target_values]

    if any(value == title for value in targets):
        return 1.0, "title"
    if any(value in aliases for value in targets):
        return 0.95, "alias"
    if title and title in query:
        return 0.9, "title_contains"
    if any(tag and (tag in query or any(tag in target for target in targets)) for tag in tags):
        return 0.75, "tag"
    if slug and slug in query:
        return 0.7, "slug"
    return 0, "none"


def _type_weight(intent_type: IntentType, content_type: str | None) -> int:
    if intent_type == IntentType.CITY:
        city_weights = {"city": 6, "spot": 5, "food": 5, "route": 4, "culture": 3, "hotel": 2}
        return city_weights.get(content_type or "", 0)

    orders = {
        IntentType.SPOT: ["spot", "city", "food", "route", "culture", "hotel"],
        IntentType.FOOD: ["food", "city", "spot"],
        IntentType.ROUTE: ["route", "spot", "city", "food"],
        IntentType.CULTURE: ["culture", "spot", "city"],
        IntentType.HOTEL: ["hotel", "city", "spot"],
    }
    order = orders.get(intent_type, [])
    if content_type not in order:
        return 0
    return len(order) - order.index(content_type)


def _apply_intent_cap(intent_type: IntentType, content_type: str, score: float) -> float:
    primary_types = {
        IntentType.FOOD: "food",
        IntentType.ROUTE: "route",
        IntentType.CULTURE: "culture",
        IntentType.HOTEL: "hotel",
    }
    primary_type = primary_types.get(intent_type)
    if primary_type is None or content_type == primary_type:
        return score
    return min(score, 0.74)
