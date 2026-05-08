# JAG-R024 Adaptive Journey Architecture

## 目标

R024 将 R023 的 feasibility 判断升级为 adaptive optimization。系统不只判断路线偏紧或过载，还会生成优化建议，并预先构建一版优化后的 timeline。

本轮仍然不接真实 AI、地图 API、PostgreSQL、Redis、真实酒店预订或账号系统。

## Core Flow

```text
timeline
→ constraint evaluation
→ adaptive suggestion engine
→ auto balance engine
→ optimized timeline
→ optimized constraint
→ replay evolution
→ adaptive analytics
```

## Backend Modules

- `adaptive_journey.py`: AdaptiveSuggestion / JourneyAdaptation / RegenerationReason / AdaptationResult
- `constraint_suggestion_engine.py`: 根据 constraint 输出用户可理解的优化建议
- `auto_balance_engine.py`: 自动减少 stop、降低 pace、减少跨城移动
- `adaptive_narrative_builder.py`: 生成 AI companion 风格优化说明
- `adaptive_journey_engine.py`: 汇总 suggestion、adaptation、optimized timeline 和 analytics 数据

## Auto Balancing

当前启发式策略：

- elder: 每个 block 降到 1 个主要停留点
- family: 每个 block 降到 2 个停留点
- tight / overloaded: 生成智能优化建议
- 多跨城: 减少重复跨城 transition
- 每天 narrative 增加减负说明

## Metadata

`/api/chat/query` 返回：

```json
{
  "metadata": {
    "adaptive_journey": {
      "applied": true,
      "before_feasibility": "overloaded",
      "after_feasibility": "tight",
      "suggestions": [],
      "adaptations": [],
      "optimized_timeline": {},
      "optimized_constraint": {}
    }
  }
}
```

Analytics 增加：

- `adaptation_count`
- `feasibility_before`
- `feasibility_after`
- `fatigue_reduction`
- `transition_reduction`

Replay 增加：

- `adaptation_events`
- `timeline_feasibility_changes`

## Future AI Planner

后续可把当前 heuristic engine 替换为：

- real map distance
- live transit
- AI route rewriter
- user memory
- persisted journey state

但 Builder / UI 仍可继续使用当前 `adaptive_journey` 协议。
