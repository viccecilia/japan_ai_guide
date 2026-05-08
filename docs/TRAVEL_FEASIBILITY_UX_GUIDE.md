# JAG-R023 Travel Feasibility UX Guide

## 原则

Feasibility 提示要帮助用户调整路线，而不是制造焦虑。不要显示 score、内部规则、ranking 或技术字段。

## 推荐表达

- 轻松路线：这条路线适合慢节奏体验。
- 节奏均衡：这条路线整体节奏均衡。
- 行程偏紧：这条路线跨城较多，建议把移动日安排得更轻松。
- 建议减负：体力压力较高，建议减少停留点或拆成更多天。

## 禁止表达

- `fatigue_score=0.88`
- `transition_load=high`
- `constraint engine flagged overload`
- `hotel_distance=tight`

## 跨城疲劳提示

跨城多时，提示应给出行动建议：

- 把跨城移动放在上午或午后早段。
- 抵达后减少额外景点。
- 保留晚间休息时间。

## Persona-aware Tone

- Elder: 更强调少步行、休息和拆天。
- Family: 更强调弹性和孩子体力。
- Couple: 可接受适度散步，但避免赶场。
- Foodie: 可以减少景点，把用餐作为节奏节点。

## 前端呈现

`TimelineConstraintBadge` 只展示用户语言：

- badge label
- feasibility reason
- 步行 / 跨城 / 疲劳 的友好标签

public mode 不显示内部 metadata。
