import time
from dataclasses import dataclass
from typing import Any

from app.schemas.content_cache import CacheLookupResult, CacheWriteResult


DEFAULT_TTL_SECONDS = 600


@dataclass
class _CacheEntry:
    value: Any
    expires_at: float
    created_at: float
    ttl_seconds: int
    intent_type: str
    language: str
    slug: str | None


class InMemoryContentCache:
    def __init__(self) -> None:
        self._store: dict[str, _CacheEntry] = {}
        self._hits = 0
        self._misses = 0

    def get(
        self,
        key: str,
        *,
        intent_type: str,
        language: str,
        slug: str | None = None,
    ) -> tuple[Any | None, CacheLookupResult]:
        now = time.time()
        entry = self._store.get(key)
        if entry is None or entry.expires_at <= now:
            if entry is not None:
                self._store.pop(key, None)
            self._misses += 1
            return None, CacheLookupResult(
                key=key,
                hit=False,
                intent_type=intent_type,
                language=language,
                slug=slug,
                ttl_seconds=DEFAULT_TTL_SECONDS,
            )

        self._hits += 1
        return entry.value, CacheLookupResult(
            key=key,
            hit=True,
            intent_type=entry.intent_type,
            language=entry.language,
            slug=entry.slug,
            ttl_seconds=entry.ttl_seconds,
        )

    def set(
        self,
        key: str,
        value: Any,
        *,
        intent_type: str,
        language: str,
        slug: str | None = None,
        ttl_seconds: int = DEFAULT_TTL_SECONDS,
    ) -> CacheWriteResult:
        now = time.time()
        self._store[key] = _CacheEntry(
            value=value,
            expires_at=now + ttl_seconds,
            created_at=now,
            ttl_seconds=ttl_seconds,
            intent_type=intent_type,
            language=language,
            slug=slug,
        )
        return CacheWriteResult(
            key=key,
            written=True,
            intent_type=intent_type,
            language=language,
            slug=slug,
            ttl_seconds=ttl_seconds,
        )

    def clear(self) -> None:
        self._store.clear()
        self._hits = 0
        self._misses = 0

    def stats(self) -> dict[str, int]:
        self._purge_expired()
        return {"hits": self._hits, "misses": self._misses, "size": len(self._store)}

    def _purge_expired(self) -> None:
        now = time.time()
        expired = [key for key, entry in self._store.items() if entry.expires_at <= now]
        for key in expired:
            self._store.pop(key, None)


content_cache = InMemoryContentCache()
