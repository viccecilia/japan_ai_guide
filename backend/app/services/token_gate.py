from pydantic import BaseModel

from app.config.ai_runtime import AIRuntimeConfig, get_ai_runtime_config


class TokenGateResult(BaseModel):
    allow_realtime_ai: bool
    mode: str
    reason: str
    fallback_level: str
    realtime_ai_used: bool = False


def evaluate_token_gate(config: AIRuntimeConfig | None = None) -> TokenGateResult:
    runtime_config = config or get_ai_runtime_config()
    if not runtime_config.realtime_ai_enabled:
        return TokenGateResult(
            allow_realtime_ai=False,
            mode=runtime_config.ai_mode,
            reason="disabled_by_config",
            fallback_level=runtime_config.default_fallback_level,
            realtime_ai_used=False,
        )

    return TokenGateResult(
        allow_realtime_ai=False,
        mode=runtime_config.ai_mode,
        reason="realtime_ai_not_connected",
        fallback_level=runtime_config.default_fallback_level,
        realtime_ai_used=False,
    )
