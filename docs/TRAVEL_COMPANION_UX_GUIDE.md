# JAG-R019 Travel Companion UX Guide

## Interaction Tone

The itinerary should feel like collaboration:

- 已调整为更轻松的路线。
- 已减少步行较多的景点。
- 已替换为更适合拍照的停留点。
- 已切换为亲子节奏。

Avoid technical wording:

- mutation
- state update
- ranking
- cache
- token

## Editable Itinerary UX

Controls should be lightweight:

- persona chips
- pace chips
- small remove/replace buttons
- one regenerate button

Do not turn the itinerary into an operations console.

## Regeneration UX

Regenerate should explain what changed in one short sentence.

Examples:

- 已重新生成更轻松的路线。
- 已重新生成更均衡的路线。
- 已增加适合拍照的节奏。

## Settings Boundary

Avoid overwhelming settings. R019 only exposes persona and pace because these directly affect the route.

## Current Boundary

R019 does not connect real AI, maps, PostgreSQL, Redis, payment, booking, DaDa dispatch, ads, or user accounts.
