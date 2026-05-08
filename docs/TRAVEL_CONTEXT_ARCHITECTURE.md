# JAG-R025 Travel Context Architecture

## 目标

R025 将 Adaptive Journey 升级为 Context-aware Travel Companion。系统开始感知 mock 天气、当前时间、旅行疲劳和 daily density，并给出动态旅行建议。

本轮不接真实天气 API、真实 AI、地图 API、PostgreSQL、Redis 或账号系统。

## Core Flow

```text
query
→ timeline
→ constraint
→ adaptive journey
→ travel context engine
→ contextual suggestions
→ context optimized timeline
→ replay / analytics
```

## Context Schema

`backend/app/schemas/travel_context.py` 定义：

- `WeatherContext`
- `TimeContext`
- `FatigueContext`
- `JourneyCondition`
- `ContextualSuggestion`
- `TravelContext`

## Mock Weather

`mock_weather_service.py` 根据 query 识别：

- `rainy`: 下雨 / 雨天 / rain
- `hot`: 很热 / 高温 / hot
- `crowded`: 人多 / 拥挤 / crowded
- `sunny`: 默认稳定天气

## Dynamic Adaptation

`travel_context_engine.py` 当前使用启发式：

- rainy: 减少连续户外 stop
- hot: 减少连续步行并放慢节奏
- crowded: 降低热门点密度
- afternoon / evening / late: 减少长距离跨城移动
- high fatigue: 减少 stop，把 pace 调整为 slow

## Metadata

`/api/chat/query` 返回：

```json
{
  "metadata": {
    "travel_context": {
      "weather": {},
      "time": {},
      "fatigue": {},
      "condition": {},
      "suggestions": [],
      "context_optimized_timeline": {}
    }
  }
}
```

Analytics 增加：

- `weather_context`
- `fatigue_context`
- `dynamic_regenerations`
- `contextual_adaptation_count`

Replay 增加：

- `weather_context`
- `fatigue_context`
- `dynamic_adaptation`

## Future Live Context

后续可接入：

- live weather API
- live transit signal
- user location and time zone
- real walking distance
- persistent journey fatigue memory
