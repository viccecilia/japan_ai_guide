# AI Token Gate

Round: JAG-R009

## What It Is

Token Gate is the backend decision layer that checks runtime configuration before any AnswerCard construction strategy attempts realtime AI.

Current default:

```text
REALTIME_AI_ENABLED=false
AI_MODE=template
DEFAULT_FALLBACK_LEVEL=template
```

No real AI provider is connected in this round.

## Why Realtime AI Is Off By Default

The project needs predictable cost and stable demos before connecting live models. With realtime AI disabled by default:

- every request still returns an AnswerCard,
- no token cost is incurred,
- frontend behavior remains stable,
- the backend can later enable AI without changing the response contract.

## User-Invisible Fallback

The user must not see operational details such as token limits or model state.

Allowed user-facing copy:

- “我先为你推荐一版经典玩法。”
- “这是适合第一次来日本游客的基础讲解。”
- “下面是你可以继续探索的方向。”

Forbidden user-facing copy:

- “AI 已关闭”
- “Token 不足”
- “模型不可用”
- “系统降级”

Operational reasons are only stored in metadata.

## Fallback Levels

| Level | Meaning |
| --- | --- |
| `template` | Use local template/mock AnswerCard content. Current default. |
| `cached` | Future cached AI/content-library result. |
| `content_library` | Future database/content library generated card. |
| `realtime_ai` | Future live AI generation when allowed by config and token policy. |

## metadata.ai_runtime

`answer_card.metadata.ai_runtime` is backend/debug metadata, not normal product copy.

Example:

```json
{
  "allow_realtime_ai": false,
  "mode": "template",
  "reason": "disabled_by_config",
  "fallback_level": "template",
  "realtime_ai_used": false
}
```

Frontend development mode may show:

- `AI Mode`
- `Realtime AI Used`
- `Fallback Level`

It deliberately does not show `reason` in the normal UI.

## Relation To AnswerCard Builder

```text
query
  -> Intent Router
  -> Token Gate
  -> AnswerCard Builder
  -> AnswerCard
```

The Builder receives both `IntentResult` and `TokenGateResult`, then chooses one of these strategies:

- `spot_card_builder`
- `city_card_builder`
- `food_card_builder`
- `route_card_builder`
- `culture_card_builder`
- `hotel_card_builder`
- `generic_card_builder`

In this round all strategies use template/mock content.

## Future Realtime AI Integration

Recommended path:

1. Keep Token Gate as the only place that decides whether realtime AI is allowed.
2. Add token counters and cached usage checks.
3. Use AI only when cache/content-library/template cannot satisfy the request.
4. Store operational metadata in `metadata.ai_runtime`.
5. Keep frontend AnswerCard rendering unchanged.
