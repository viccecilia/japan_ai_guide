from dataclasses import dataclass

from app.schemas.content_library import BaseContent
from app.schemas.intent import IntentResult
from app.services.cache_key_builder import build_cache_key
from app.services.content_cache import content_cache
from app.services.content_index import get_content_index
from app.services.content_repository import content_repository
from app.services.query_ranking import RankingResult, rank_top_k


@dataclass(frozen=True)
class ResolvedContent:
    content: BaseContent | None
    content_source: dict[str, str]
    cache: dict[str, str | bool | int | float]
    ranking: dict[str, str | float | int | None]
    related_candidates: list[dict[str, str | float | int | None]]
    candidate_groups: dict[str, list[dict[str, str | float | int | None]]]


def resolve_content(query: str, intent: IntentResult) -> ResolvedContent:
    candidates = rank_top_k(query, intent, get_content_index(), top_k=5)
    best = candidates[0] if candidates else RankingResult(slug=None, score=0, matched_by="none")
    cache_key = build_cache_key(query, intent, best.slug)

    cached_content, lookup = content_cache.get(
        cache_key,
        intent_type=intent.intent_type.value,
        language=intent.language,
        slug=best.slug,
    )
    if cached_content is not None:
        return ResolvedContent(
            content=cached_content,
            content_source=_content_source(cached_content),
            cache=_cache_metadata(lookup),
            ranking=best.as_metadata(),
            related_candidates=_related_candidates(candidates),
            candidate_groups=_candidate_groups(candidates),
        )

    content = content_repository.find_by_slug(best.slug, intent.language, best.content_type) if best.slug else None
    if content is None:
        return ResolvedContent(
            content=None,
            content_source={"type": "template"},
            cache=_cache_metadata(lookup),
            ranking=best.as_metadata(),
            related_candidates=_related_candidates(candidates),
            candidate_groups=_candidate_groups(candidates),
        )

    write = content_cache.set(
        cache_key,
        content,
        intent_type=intent.intent_type.value,
        language=intent.language,
        slug=content.slug,
    )
    return ResolvedContent(
        content=content,
        content_source=_content_source(content),
        cache={"hit": False, "key": write.key, "source": write.source, "ttl_seconds": write.ttl_seconds},
        ranking=best.as_metadata(),
        related_candidates=_related_candidates(candidates),
        candidate_groups=_candidate_groups(candidates),
    )


def _content_source(content: BaseContent) -> dict[str, str]:
    return {"type": "content_library", "slug": content.slug, "language": content.language}


def _cache_metadata(lookup: object) -> dict[str, str | bool | int | float]:
    return {
        "hit": bool(getattr(lookup, "hit")),
        "key": str(getattr(lookup, "key")),
        "source": str(getattr(lookup, "source")),
        "ttl_seconds": int(getattr(lookup, "ttl_seconds")),
    }


def _related_candidates(candidates: list[RankingResult]) -> list[dict[str, str | float | int | None]]:
    return [
        {
            "slug": candidate.slug,
            "score": candidate.score,
            "matched_by": candidate.matched_by,
            "content_type": candidate.content_type,
            "priority": candidate.priority,
        }
        for candidate in candidates[1:]
    ]


def _candidate_groups(candidates: list[RankingResult]) -> dict[str, list[dict[str, str | float | int | None]]]:
    groups: dict[str, list[dict[str, str | float | int | None]]] = {}
    for candidate in candidates:
        key = candidate.content_type or "unknown"
        groups.setdefault(key, []).append(
            {
                "slug": candidate.slug,
                "score": candidate.score,
                "matched_by": candidate.matched_by,
                "content_type": candidate.content_type,
                "priority": candidate.priority,
            }
        )
    return groups
