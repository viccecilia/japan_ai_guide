# JAG-R022 Timeline UX Guide

## 产品原则

Timeline 不是后台排班表，而是 AI 旅行助手给用户的多日路线叙事。用户应先理解每天的节奏，再看到 stop、酒店和跨城移动。

## 页面层级

1. 旅行总览：城市、天数、路线风格。
2. Day Tabs：Day 1 / Day 2 / Day 3，用于快速切换。
3. Daily Narrative：解释当天为什么这样安排。
4. Timeline Blocks：上午主线、下午延展。
5. Hotel Block：每天住宿建议。
6. Transition Block：跨城市移动建议。

## Daily Pacing

- `slow`: 减少 stop，强调休息和少步行。
- `normal`: 保留经典体验和弹性时间。
- `dense`: 增加停留密度，但仍保留午间休息。

## Travel Fatigue Awareness

多日路线不能把每天都排满。跨城市当天应减少 stop 数量，并把移动放在上午或午后早段，避免压缩晚间休息。

## Transition Narrative

跨城文案要面向用户解释节奏，而不是暴露内部规则：

- 推荐：从京都前往大阪时，建议把移动放在上午，下午再进入大阪市区体验。
- 禁止：ranking score 较高，所以推荐大阪。

## Hotel Insertion Tone

酒店建议只表达区域逻辑，不假装拥有实时库存：

- 推荐：京都站附近适合作为多日路线 base，方便第二天移动。
- 禁止：这家酒店现在可订，价格最低。

## Editing UX

R022 支持轻量 daily editing：

- 删除某一天 stop
- 切换某一天 pace
- 重新生成某一天 narrative

不做拖拽，不做复杂配置面板，避免让旅行助手变成后台工具。
