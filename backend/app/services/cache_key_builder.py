import re

from app.schemas.intent import IntentResult


def build_cache_key(query: str, intent: IntentResult, slug: str | None = None) -> str:
    raw_target = slug or intent.entity or intent.city or query
    target = normalize_cache_part(raw_target)
    language = normalize_cache_part(intent.language or "zh")
    return f"{intent.intent_type.value}:{target}:{language}"


def normalize_cache_part(value: str) -> str:
    normalized = re.sub(r"\s+", " ", value.strip().lower())
    return normalized.replace(" ", "_")
