# JAG-R023 Travel Constraint Architecture

## 目标

R023 在 Multi-Day Timeline 之上建立现实旅行约束层，让系统开始判断路线是否可执行、是否过赶、跨城是否合理、酒店是否顺路，以及不同 persona 的体力负担。

本轮仍然不接真实 AI、地图 API、PostgreSQL、Redis 或真实酒店预订。

## 核心链路

```text
query
→ persona detection
→ timeline builder
→ daily load engine
→ transition feasibility
→ hotel placement validation
→ travel constraint engine
→ timeline_feasibility
→ response.metadata.timeline_constraint
```

## Constraint Schema

`backend/app/schemas/travel_constraint.py` 定义：

- `TravelLoad`
- `FeasibilityScore`
- `TravelConstraint`
- `DailyConstraint`
- `TransitionConstraint`
- `HotelConstraint`
- `TimelineConstraint`

核心字段：

- `walking_load`
- `transition_load`
- `daily_density`
- `hotel_distance`
- `estimated_fatigue`
- `timeline_feasibility`
- `feasibility_reason`

## Daily Load Engine

`daily_load_engine.py` 根据以下因素计算每天负载：

- stop 数量
- pace: slow / normal / dense
- persona: elder / family / couple 等

等级：

- `easy`
- `normal`
- `tight`
- `overload`

## Transition Feasibility

`JourneyTransition` 扩展字段：

- `estimated_transition_time`
- `transition_type`
- `transition_load`

当前规则是启发式：

- 东京 ↔ 京都 / 大阪：新干线，长距离移动，负载更高
- 京都 ↔ 大阪 / 奈良：JR / 私铁，负载正常

## Hotel Validation

`hotel_feasibility_engine.py` 检查酒店是否和当天城市一致。当前只做 mock 区域判断，不判断真实距离、价格或库存。

## Timeline Scoring

`travel_constraint_engine.py` 汇总：

- daily density
- transition load
- hotel distance
- estimated fatigue
- persona constraints

输出：

- `easy`
- `balanced`
- `tight`
- `overloaded`

## Future Integration

- Map API: 使用真实步行距离和交通时间校准 load。
- Live transit: 用实时交通延误调整 transition load。
- AI planner: 在约束结果基础上自动重排路线。
- Persistent journey: 保存 feasibility evolution。
