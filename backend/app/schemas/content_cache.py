from datetime import datetime, timezone

from pydantic import BaseModel, Field


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class CacheMetadata(BaseModel):
    key: str
    hit: bool = False
    source: str = "memory"
    language: str = "zh"
    intent_type: str
    slug: str | None = None
    created_at: datetime = Field(default_factory=utc_now)
    ttl_seconds: int


class CacheLookupResult(BaseModel):
    key: str
    hit: bool
    source: str = "memory"
    language: str = "zh"
    intent_type: str
    slug: str | None = None
    created_at: datetime = Field(default_factory=utc_now)
    ttl_seconds: int


class CacheWriteResult(BaseModel):
    key: str
    written: bool
    source: str = "memory"
    language: str = "zh"
    intent_type: str
    slug: str | None = None
    created_at: datetime = Field(default_factory=utc_now)
    ttl_seconds: int
