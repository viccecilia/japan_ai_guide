# Travel Memory UX Guide

## Product Principle

Travel memory should make Japan AI Guide feel like a companion that remembers useful travel habits, not a surveillance or profiling system.

The user-facing tone should be light:

- `AI 已记住你更喜欢慢节奏文化路线。`
- `这次路线会延续你偏好的轻松节奏。`
- `已根据你之前的路线偏好减少跨城移动。`

Avoid technical explanations in public mode.

## What To Show

Public UI can show:

- current travel style
- preferred pace
- preferred route focus
- a short companion summary
- an easy override through existing journey controls

Public UI should not show:

- raw event counts
- internal confidence
- memory update counters
- scoring fields
- hidden metadata keys

## Avoid Creepy Personalization

Do not write copy that implies surveillance or permanent profiling.

Avoid:

- `我们追踪了你的所有行为。`
- `系统判定你属于某类用户。`
- `你的历史数据证明你不喜欢人多。`

Prefer:

- `看起来你更喜欢轻松一点的节奏。`
- `我先按慢节奏文化路线帮你安排。`
- `你可以随时切换节奏或路线风格。`

## Override Rules

Memory should guide defaults, not lock decisions.

Users must be able to:

- switch pace
- switch persona
- remove or replace stops
- regenerate a route
- override the companion's inferred preference

## Public / Debug / Operator Separation

Public mode:

- show only companion-style memory summary.

Debug mode:

- may show memory update counts and raw preference fields.

Operator mode:

- may show aggregate preference evolution and memory-driven regeneration rates.

## Future Account Sync

When real accounts are introduced, memory UX must add:

- opt-in consent
- clear memory/reset controls
- account-level storage disclosure
- export/delete support

R026 does not implement real accounts or permanent persistence.
