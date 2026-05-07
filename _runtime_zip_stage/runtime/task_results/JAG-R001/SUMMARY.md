# JAG-R001 ChatGPT UI Foundation

## 修改了什么

- 重建 Next.js 首页入口，页面现在由 `ChatShell` 统一装配。
- 新增 ChatGPT 风格前端基础 UI：左侧历史栏、中间 Logo/欢迎语、输入框、快捷问题按钮、右上语言选择、基础 AnswerCard。
- 将页面拆分为可继续演进的前端组件。
- 修复 Round 0 页面中的乱码文案，恢复中文优先的旅游导览 UI。
- 调整移动端宽度、换行和 overflow，避免主要布局在小屏下崩坏。

## 页面结构说明

- `HistorySidebar`：桌面端左侧历史栏，包含历史问题、答案摘要和新对话入口。
- `ChatShell`：主页面容器，管理当前输入、当前主题和静态回答展示。
- `LanguageSelector`：右上角语言选择器。
- `QuickQuestionButtons`：快捷问题按钮组，点击后填充当前问题并更新 AnswerCard。
- `ChatInput`：底部输入框和发送按钮。
- `AnswerCard`：静态 AI 回答卡片，占位展示讲解、音频、看点、美食、附近景点和下一步操作。

## 组件清单

- `frontend/src/app/page.tsx`
- `frontend/src/components/chat/ChatShell.tsx`
- `frontend/src/components/chat/HistorySidebar.tsx`
- `frontend/src/components/chat/LanguageSelector.tsx`
- `frontend/src/components/chat/QuickQuestionButtons.tsx`
- `frontend/src/components/chat/ChatInput.tsx`
- `frontend/src/components/chat/AnswerCard.tsx`
- `frontend/src/app/globals.css`

## 任务状态

| 任务 | 状态 |
| --- | --- |
| 建立或整理前端页面入口 | 完成 |
| 实现 ChatGPT 风格页面布局 | 完成 |
| 实现左侧历史栏组件 | 完成 |
| 实现主聊天区域组件 | 完成 |
| 实现输入框组件 | 完成 |
| 实现快捷问题按钮组件 | 完成 |
| 实现语言选择组件 | 完成 |
| 实现基础 AnswerCard 静态展示占位 | 完成 |
| 将 Demo 视觉风格迁移到 Next.js 前端 | 完成 |
| 创建本轮结果目录 | 完成 |

## 验证结果

- `cd frontend && npm.cmd run dev`：已运行，服务监听 `http://127.0.0.1:3000`。
- `npm.cmd run check`：通过。
- `npm.cmd run build`：通过。
- 页面打开：HTTP 200。
- 输入框：可输入并可通过发送按钮更新当前问题。
- 快捷按钮：可点击并更新当前问题与 AnswerCard。
- 语言选择器：可切换到 English。
- 桌面布局：左侧历史栏、主内容、右上语言选择显示正常。
- 手机布局：移动断点截图已生成，主结构未崩坏。

## 截图

- 桌面：`runtime/task_results/JAG-R001/desktop-1440.png`
- 手机断点：`runtime/task_results/JAG-R001/mobile-500.png`
- 390px Chrome headless 参考：`runtime/task_results/JAG-R001/mobile-390.png`
- in-app browser：`runtime/task_results/JAG-R001/browser-current.png`

## Mock 标记

- 历史记录为静态 Mock。
- AnswerCard 文案、看点、附近景点、美食和下一步操作为静态 Mock。
- 音频播放器为静态 Mock。
- “生成路线 / 加入行程 / 查看地图”按钮只展示，不调用 API。
- 语言切换只更新选择状态，不触发翻译或内容刷新。

## 下一轮需要接 API 的位置

- `ChatInput.onSubmit`：接入提问 API。
- `QuickQuestionButtons.onSelect`：接入快捷问题提交或预填逻辑。
- `AnswerCard`：接入 AI 回答、推荐、路线、地图和 TTS 数据。
- `HistorySidebar`：接入会话历史 API 或本地会话缓存。
- `LanguageSelector`：接入语言偏好和翻译/本地化逻辑。

## 未完成 / 风险

- 本轮未接真实后端、AI、地图、TTS、数据库或登录。
- 390px Chrome headless CLI 截图受 Chrome headless 最小布局宽度影响，保留为参考；实际移动断点以 `mobile-500.png` 和响应式 CSS 验证为准。

## 下一轮建议

- JAG-R002 建议实现前端 Mock 会话流：发送问题后追加用户消息和 AI 回答卡片列表。
- 定义前端到后端的 `/api/chat` 响应结构。
- 将 AnswerCard 数据结构抽成 typed mock data，便于后续替换为真实 API。
