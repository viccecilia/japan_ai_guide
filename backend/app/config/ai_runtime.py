from dataclasses import dataclass
import os


@dataclass(frozen=True)
class AIRuntimeConfig:
    realtime_ai_enabled: bool
    ai_mode: str
    daily_token_limit: int
    monthly_token_limit: int
    default_fallback_level: str


def get_ai_runtime_config() -> AIRuntimeConfig:
    return AIRuntimeConfig(
        realtime_ai_enabled=_read_bool("REALTIME_AI_ENABLED", default=False),
        ai_mode=os.getenv("AI_MODE", "template"),
        daily_token_limit=_read_int("DAILY_TOKEN_LIMIT", default=100000),
        monthly_token_limit=_read_int("MONTHLY_TOKEN_LIMIT", default=3000000),
        default_fallback_level=os.getenv("DEFAULT_FALLBACK_LEVEL", "template"),
    )


def _read_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _read_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        return default
