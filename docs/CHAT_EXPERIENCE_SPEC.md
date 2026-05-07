# JAG-R006 Chat Experience Spec

## Scope

本轮优化 Japan AI Guide 的第一阶段聊天体验外壳。前端仍调用既有 Mock API，不接真实 AI、数据库、地图、TTS 或包车业务。

## Chat Flow

```text
输入问题 / 点击快捷问题
  -> 当前会话新增一条历史记录
  -> 展示 loading 动画
  -> 调用 /api/chat/query
  -> 展示 streaming mock 文案
  -> 渲染最终 AnswerCard
```

## Session History

- 历史记录只保存在当前 React 会话状态内。
- 刷新浏览器后历史会清空。
- 每次有效提问都会新增一条记录。
- 左侧历史栏显示当前会话内的问题、状态和返回卡片摘要。
- 点击历史记录不会重新请求后端，只恢复该条记录的 question 与 AnswerCard。
- 移动端不显示左侧栏，改为顶部横向历史条，避免布局崩坏。

## Keyboard Interaction

- `Enter`：发送当前问题。
- `Shift + Enter`：在输入框内换行，不触发请求。
- 请求中或 streaming mock 中，输入框和发送按钮进入 disabled 状态，避免重复提交。

## UI States

- Empty：欢迎页展示 Logo、说明、快捷问题和体验提示。
- Loading：请求后端时显示三点跳动动画和 Mock API 提示。
- Streaming：后端返回后，前端模拟短文本流式输出。
- Success：streaming mock 完成后，渲染后端返回的 AnswerCard。
- Error：网络失败或 API 异常时显示错误卡片，提示检查本地后端地址。

## Mobile Behavior

- 桌面端保留左侧历史栏。
- 移动端隐藏左侧栏，保留顶部 `新对话` 按钮和横向历史条。
- 主聊天区域、AnswerCard、输入框均使用响应式宽度和换行策略。

## Mock Boundary

仍属于 Mock 的部分：

- AnswerCard 数据来自后端 Mock service。
- Streaming 是前端本地模拟，不是真实 token stream。
- 历史只存在内存，不接数据库或 localStorage。
- TTS、地图、行程保存、路线生成按钮仍为占位。
- 语言选择器只做 UI 切换，不影响 API 请求语言。

## Next API Positions

后续接 API 时优先处理：

- 会话持久化：`ChatShell` 中的 `turns` 状态。
- 真实 streaming：替换 `playStreamingMock`。
- 历史列表：替换当前内存历史为 `/api/history/list` 或会话 API。
- 多语言：将 `LanguageSelector` 当前选项传入 `queryChat`。
