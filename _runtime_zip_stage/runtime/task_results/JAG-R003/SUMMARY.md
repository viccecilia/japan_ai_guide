# JAG-R003 UI Design System

## 修改了什么

- 新增设计 token 文件：`frontend/styles/tokens.css`。
- 在 `frontend/src/app/globals.css` 中引入 token，并定义 `.jag-*` 共享样式类。
- 统一按钮、卡片、输入框、Sidebar、AnswerCard 的基础视觉规则。
- 将当前 ChatGPT UI 组件改为引用 token 和共享样式类。
- 修复前端组件中损坏的中文 UI 文案。
- 新增设计系统文档：`docs/UI_DESIGN_SYSTEM.md`。

## 每个任务状态

| 任务 | 状态 |
| --- | --- |
| 创建或整理设计 token 文件 | 完成 |
| 定义颜色系统 | 完成 |
| 定义字体系统 | 完成 |
| 定义圆角系统 | 完成 |
| 定义阴影系统 | 完成 |
| 定义间距系统 | 完成 |
| 定义按钮样式 | 完成 |
| 定义卡片样式 | 完成 |
| 定义 Sidebar 样式 | 完成 |
| 定义 AnswerCard 样式 | 完成 |
| 输出 `docs/UI_DESIGN_SYSTEM.md` | 完成 |
| 创建本轮结果目录 | 完成 |

## Design Token 清单

- Colors: `--jag-color-page`, `--jag-color-page-soft`, `--jag-color-surface`, `--jag-color-surface-muted`, `--jag-color-ink`, `--jag-color-ink-soft`, `--jag-color-muted`, `--jag-color-line`, `--jag-color-primary`, `--jag-color-primary-strong`, `--jag-color-primary-soft`, `--jag-color-audio`
- Typography: `--jag-font-sans`, `--jag-font-size-xs`, `--jag-font-size-sm`, `--jag-font-size-md`, `--jag-font-size-lg`, `--jag-font-size-xl`, `--jag-font-size-hero`
- Radius: `--jag-radius-sm`, `--jag-radius-md`, `--jag-radius-lg`, `--jag-radius-pill`
- Shadows: `--jag-shadow-sm`, `--jag-shadow-md`, `--jag-shadow-lg`, `--jag-shadow-primary`
- Spacing: `--jag-space-1`, `--jag-space-2`, `--jag-space-3`, `--jag-space-4`, `--jag-space-5`, `--jag-space-6`, `--jag-space-8`, `--jag-space-10`

## 组件样式清单

- `.jag-page`: app 背景和页面 shell
- `.jag-sidebar`: 桌面历史栏
- `.jag-card`: AnswerCard 主卡片
- `.jag-panel`: AnswerCard 内部模块
- `.jag-button-primary`: 主按钮
- `.jag-button-secondary`: 次按钮和快捷按钮
- `.jag-button-compact`: 移动端菜单等紧凑按钮
- `.jag-input-shell`: 底部输入框容器
- `.jag-answer-badge`: AnswerCard 状态标签

## 前后对比说明

Before:

- 颜色、阴影、圆角散落在组件 className 中。
- 按钮、卡片、Sidebar 视觉规则重复。
- 部分中文文案编码损坏。

After:

- token 集中在 `frontend/styles/tokens.css`。
- 共享视觉规则集中在 `.jag-*` classes。
- 组件使用统一按钮、卡片、输入框和 AnswerCard 样式。
- 页面文案恢复为中文优先。

## 后续组件必须遵守的 UI 规则

- 新按钮必须优先使用 `.jag-button-primary`、`.jag-button-secondary` 或 `.jag-button-compact`。
- 新卡片必须优先使用 `.jag-card` 或 `.jag-panel`。
- 新 Sidebar 必须基于 `.jag-sidebar`。
- 新 AnswerCard 内部状态标签必须使用 `.jag-answer-badge`。
- 新颜色、阴影、圆角、间距必须先加入 token，再在组件中引用。
- 移动端必须保留换行、`min-w-0` 和 overflow 约束，避免长中文/日文撑破页面。

## 验证结果

- `npm.cmd run check`: 通过。
- `npm.cmd run build`: 通过。
- `npm.cmd run dev`: 已运行。
- 页面 HTTP 访问：通过。
- token 引用检查：通过，组件已引用 `.jag-*` classes 和 CSS variables。
- 桌面截图：已生成。
- 移动端截图：已生成。

## 截图

- 桌面：`runtime/task_results/JAG-R003/desktop-1440.png`
- 移动端：`runtime/task_results/JAG-R003/mobile-500.png`

## 未完成 / 风险

- 本轮只建立基础设计系统，没有引入 Storybook、视觉回归测试或组件库打包。
- `--jag-space-*` 间距 token 已定义，当前页面仍有一部分布局间距继续使用 Tailwind scale，后续新增复杂页面时应逐步收敛。

## 下一轮建议

- JAG-R004 建议将 AnswerCard 数据结构和前端 UI 与 `/api/chat/query` 对接。
- 同时补充 loading、error、empty state 的设计系统规则。
