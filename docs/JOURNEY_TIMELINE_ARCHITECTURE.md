# JAG-R022 Journey Timeline Architecture

## 目标

R022 将 single editable itinerary 扩展为 Multi-Day Journey Timeline。系统仍然不接真实 AI、地图、数据库、Redis 或真实酒店预订，只建立多日旅行协议、启发式编排和前端时间轴展示。

## 数据结构

```text
JourneyTimeline
├─ timeline_id
├─ title
├─ days[]
│  ├─ JourneyDay
│  ├─ blocks[]
│  ├─ hotel
│  └─ daily_narrative
├─ cities[]
├─ hotels[]
├─ transitions[]
└─ total_duration
```

## 生成流程

```text
query
→ intent / persona / travel_flow
→ timeline_builder
→ day_composition_engine
→ hotel_insertion_engine
→ city transition layer
→ multi_day_narrative_builder
→ response.metadata.timeline
→ JourneyTimelineView
```

## Day Composition

`day_composition_engine.py` 根据 pace 控制每天 stop 数量：

- `slow`: 最多 3 个停留点
- `normal`: 最多 4 个停留点
- `dense`: 最多 5 个停留点

每天默认分为上午主线和下午延展两个 block。当前不使用真实距离和地图，只做启发式顺序编排。

## Hotel Insertion

`hotel_insertion_engine.py` 提供区域性 mock 酒店建议：

- 京都：京都站附近酒店
- 大阪：难波附近酒店
- 东京：新宿附近酒店
- 奈良：奈良站附近酒店

本层只输出住宿建议，不做预订、价格、库存或 partner ranking。

## City Transition

`multi_day_narrative_builder.py` 输出 `JourneyTransition`：

- from_city
- to_city
- recommended_transport
- estimated_travel_time
- narrative

示例：东京 → 京都 使用新干线，京都 → 大阪 使用 JR / 私铁。

## Replay 与 Analytics

R022 在 response metadata 中补充：

```json
{
  "analytics": {
    "timeline_days": 5,
    "city_transition_count": 2,
    "hotel_insertions": 5,
    "timeline_regenerations": 0
  },
  "replay": {
    "timeline": {},
    "timeline_events": []
  }
}
```

前端当前的 daily editing 是轻量本地交互，用于验证 UX。后续可升级为后端 stateful timeline API。

## 未来扩展

- 地图接入：使用真实交通时间和步行距离重新排序 day blocks。
- AI Planner：在启发式规则之后做自然语言重排和叙事增强。
- Booking Integration：酒店 block 可转为可点击预订入口。
- DaDa Bridge：跨城市交通或包车需求可转为 DaDa 调度入口。
