# JAG-R025 Context-aware UX Guide

## 原则

Context-aware 提示要像旅行助手在观察当前状态，而不是像天气插件或报警系统。

## 推荐表达

- 今天可能下雨，建议减少连续户外步行。
- 当前时间不适合再安排远距离跨城移动。
- 连续密集行程已经累积疲劳，下一段建议放慢节奏。
- 根据当前状态，我可以帮你把路线调得更轻松。

## 避免表达

- `weather_context=rainy`
- `dynamic_regenerations=1`
- `contextual_adaptation_count=2`
- `fatigue_context=high`

这些字段只保留在 metadata / debug / operator 层。

## UI Rules

TravelContextCard 展示：

- 今日旅行状态
- 天气 / 时间 / 疲劳 的友好标签
- 1-3 条 contextual suggestions
- 根据当前状态优化按钮

不要展示内部 score、raw context key 或规则命中。

## 降低焦虑

不要说：

- 今天路线很糟糕。
- 你现在太累了。

应该说：

- 今天可以把节奏放轻一点。
- 下午更适合就近安排。
- 我先帮你减少连续步行。

## AI Companion 感

按钮使用：

- 根据当前状态优化

点击后应用 context optimized timeline，并用自然文案说明调整原因。
