# Japan AI Guide · PHASE 1 Round & Task 细则

# PHASE 1 总目标

建立 Japan AI Guide 的基础平台阶段，让项目形成：

- ChatGPT 风格主界面
- 前后端基础通信
- 标准化 UI Design System
- AnswerCard 基础协议
- Mock AnswerCard 渲染
- 基础聊天体验

本阶段不接真实 AI，不接数据库，不接 TTS，不接地图，不接包车系统。

---

# PHASE 1 执行原则

## 允许做

- UI 骨架
- 前后端 Mock API
- AnswerCard Mock Schema
- 基础组件拆分
- 设计系统文档
- 前后端联通
- 本地验证脚本
- Round 结果归档

## 禁止做

- 不接 OpenAI / DeepSeek / Claude
- 不接真实 TTS
- 不接地图
- 不接数据库
- 不接 DaDa
- 不做支付
- 不做包车调度
- 不做复杂 AI Agent
- 不改 Workbench 核心执行器

---

# JAG-R001

## Round ID

JAG-R001

## Round Name

ChatGPT UI Foundation

## 本轮目标

建立 Japan AI Guide 的 ChatGPT 风格前端基础 UI。

用户打开页面后，应看到：

- 左侧历史栏
- 中间 Logo / 欢迎语
- 输入框
- 快捷问题按钮
- 右上语言选择
- 基础回答区域

本轮只做前端 UI，不接真实后端，不接 AI。

## 本轮任务

### 执行任务

- 建立或整理前端页面入口。
- 实现 ChatGPT 风格页面布局。
- 实现左侧历史栏组件。
- 实现主聊天区域组件。
- 实现输入框组件。
- 实现快捷问题按钮组件。
- 实现语言选择组件。
- 实现基础 AnswerCard 静态展示占位。
- 将 Demo 中的视觉风格迁移到 Next.js 前端。
- 创建本轮结果目录：`runtime/task_results/JAG-R001/`

### 测试任务

- 运行前端开发服务。
- 检查页面是否可正常打开。
- 检查输入框是否可输入。
- 检查快捷按钮是否可点击。
- 检查语言选择器是否可切换。
- 检查桌面尺寸下布局是否正常。
- 检查手机尺寸下布局是否不崩坏。

### 协作验收任务

- 输出截图或截图路径。
- 输出页面结构说明。
- 输出组件清单。
- 标记哪些只是 Mock。
- 标记下一轮需要接 API 的位置。

## 允许修改

```text
frontend/
frontend/app/
frontend/components/
frontend/styles/
docs/
runtime/task_results/JAG-R001/
```

## 禁止修改

```text
backend/
data/
content/
scripts/
workbench/
DaDa 平台相关目录
```

## 必须运行的验证

```bash
cd frontend
npm run dev
```

可选：

```bash
npm run lint
```

## 完成定义

- 页面可以正常打开。
- 页面视觉接近 ChatGPT 风格。
- 左侧历史栏存在。
- 中间输入区存在。
- 快捷按钮存在。
- 语言选择存在。
- 基础 AnswerCard 占位存在。
- 本轮输出结果已归档到 `runtime/task_results/JAG-R001/`。

## 输出格式

- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

---

# JAG-R002

## Round ID

JAG-R002

## Round Name

API Foundation

## 本轮目标

建立 FastAPI 后端基础 API 骨架。

本轮目标不是做真实业务，而是让前端未来有稳定 API 接口可以调用。

## 本轮任务

### 执行任务

- 整理 FastAPI 项目结构。
- 保留 `/health` 健康检查接口。
- 建立 `routers/` 目录。
- 建立 `schemas/` 目录。
- 建立 `services/` 目录。
- 建立统一 API Response 结构。
- 建立以下 Mock Router：
  - `/api/chat/query`
  - `/api/spots/search`
  - `/api/history/list`
  - `/api/language/list`
- `/api/chat/query` 暂时返回 Mock AnswerCard。
- 创建本轮结果目录：`runtime/task_results/JAG-R002/`

### 测试任务

- 启动 FastAPI 服务。
- 访问 `/health`。
- 访问 `/api/chat/query`。
- 检查 API 返回 JSON 格式。
- 检查错误时返回结构统一。

### 协作验收任务

- 输出 API 列表。
- 输出 Mock 返回样例。
- 输出启动命令。
- 输出本轮未接真实业务说明。

## 允许修改

```text
backend/app/
backend/app/main.py
backend/app/routers/
backend/app/schemas/
backend/app/services/
backend/requirements.txt
docs/
runtime/task_results/JAG-R002/
```

## 禁止修改

```text
frontend/
data/
content/
DaDa 平台相关目录
workbench 核心执行器
```

除非为了补充接口说明文档，不得修改前端代码。

## 必须运行的验证

```bash
cd backend
uvicorn app.main:app --reload
```

检查：

```text
/health
/api/chat/query
```

可选：

```bash
python -m compileall app
```

## 完成定义

- FastAPI 可以启动。
- `/health` 返回正常。
- `/api/chat/query` 返回 Mock AnswerCard。
- API Response 结构统一。
- Router 结构清晰。
- 本轮结果已归档。

## 输出格式

- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

---

# JAG-R003

## Round ID

JAG-R003

## Round Name

UI Design System

## 本轮目标

建立 Japan AI Guide 的基础 UI 设计系统。

目标是让后续所有页面、组件、AnswerCard 视觉统一。

## 本轮任务

### 执行任务

- 创建或整理设计 token 文件。
- 定义颜色系统。
- 定义字体系统。
- 定义圆角系统。
- 定义阴影系统。
- 定义间距系统。
- 定义按钮样式。
- 定义卡片样式。
- 定义 Sidebar 样式。
- 定义 AnswerCard 样式。
- 输出设计系统文档：`docs/UI_DESIGN_SYSTEM.md`
- 创建本轮结果目录：`runtime/task_results/JAG-R003/`

### 测试任务

- 检查前端页面是否仍可正常打开。
- 检查 UI token 是否被页面引用。
- 检查按钮、卡片、输入框、Sidebar 样式是否统一。
- 检查移动端下样式是否不崩坏。

### 协作验收任务

- 输出设计 token 清单。
- 输出组件样式清单。
- 输出本轮前后对比说明。
- 标记后续组件必须遵守的 UI 规则。

## 允许修改

```text
frontend/styles/
frontend/app/
frontend/components/
docs/UI_DESIGN_SYSTEM.md
runtime/task_results/JAG-R003/
```

## 禁止修改

```text
backend/
data/
content/
scripts/
DaDa 平台相关目录
```

## 必须运行的验证

```bash
cd frontend
npm run dev
```

可选：

```bash
npm run lint
```

## 完成定义

- UI token 文件存在。
- `UI_DESIGN_SYSTEM.md` 存在。
- 页面视觉统一。
- AnswerCard、Sidebar、按钮、输入框样式有统一规则。
- 不引入后端逻辑。
- 本轮结果已归档。

## 输出格式

- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

---

# JAG-R004

## Round ID

JAG-R004

## Round Name

AnswerCard Schema Foundation

## 本轮目标

建立 Japan AI Guide 的 AnswerCard 基础协议。

这是整个项目最关键的协议层。

本轮不做真实 AI，不做数据库查询，只定义返回结构与前端渲染协议。

## 本轮任务

### 执行任务

- 定义 AnswerCard TypeScript 类型。
- 定义后端 AnswerCard Schema。
- 统一 `card_type` 枚举。
- 建立 Mock AnswerCard 数据。
- 建立前端 AnswerCard Renderer。
- 支持以下卡片类型占位：
  - `spot_card`
  - `city_card`
  - `food_card`
  - `route_card`
  - `culture_card`
  - `generic_card`
- Mock 数据至少包含：
  - 清水寺
  - 伏见稻荷大社
  - 大阪城
  - 奈良公园
- 输出协议文档：`docs/ANSWER_CARD_SCHEMA.md`
- 创建本轮结果目录：`runtime/task_results/JAG-R004/`

### 测试任务

- 前端可渲染 Mock AnswerCard。
- 后端可返回 Mock AnswerCard。
- 检查字段缺失时前端不崩坏。
- 检查不同 `card_type` 是否可区分展示。
- 检查中文内容是否正常显示。

### 协作验收任务

- 输出 AnswerCard JSON 样例。
- 输出字段说明。
- 输出前端渲染说明。
- 输出后端返回说明。
- 标记哪些字段未来由 AI 生成，哪些字段来自数据库。

## 允许修改

```text
frontend/components/
frontend/types/
frontend/mock/
backend/app/schemas/
backend/app/services/
docs/ANSWER_CARD_SCHEMA.md
runtime/task_results/JAG-R004/
```

## 禁止修改

```text
真实 AI API 接入
数据库接入
地图接入
TTS 接入
DaDa 平台相关目录
```

## 必须运行的验证

前端：

```bash
cd frontend
npm run dev
```

后端：

```bash
cd backend
uvicorn app.main:app --reload
```

可选：

```bash
cd frontend
npm run lint
```

```bash
cd backend
python -m compileall app
```

## 完成定义

- AnswerCard 协议文档存在。
- 前端 AnswerCard Renderer 可用。
- 后端 Mock AnswerCard 可返回。
- 至少 4 个 Mock 景点卡片存在。
- `card_type` 枚举存在。
- 不接真实 AI。
- 不接数据库。
- 本轮结果已归档。

## 输出格式

- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

---

# JAG-R005

## Round ID

JAG-R005

## Round Name

Frontend Backend Integration

## 本轮目标

实现前端和后端真实联通。

用户在前端输入问题后：

```text
前端发送请求
↓
后端返回 Mock AnswerCard
↓
前端渲染 AnswerCard
```

本轮仍然不接真实 AI，不接数据库。

## 本轮任务

### 执行任务

- 创建前端 API Service。
- 实现 chat query 请求。
- 前端输入框触发真实请求。
- 快捷按钮触发真实请求。
- 后端根据 query 返回不同 Mock AnswerCard。
- 实现 loading 状态。
- 实现 error 状态。
- 实现 empty 状态。
- 输出联调说明文档：`docs/FRONTEND_BACKEND_INTEGRATION.md`
- 创建本轮结果目录：`runtime/task_results/JAG-R005/`

### 测试任务

- 同时启动前端和后端。
- 输入“清水寺”，返回清水寺卡片。
- 输入“大阪城”，返回大阪城卡片。
- 输入未知问题，返回 `generic_card`。
- 断开后端时，前端显示错误提示。
- 快捷按钮可触发请求。

### 协作验收任务

- 输出联调路径。
- 输出请求样例。
- 输出返回样例。
- 输出错误状态截图或说明。
- 输出当前 Mock 逻辑说明。

## 允许修改

```text
frontend/
backend/app/
docs/
runtime/task_results/JAG-R005/
```

## 禁止修改

```text
data/
content/
真实 AI API
数据库
TTS
地图
DaDa 平台相关目录
workbench 核心执行器
```

## 必须运行的验证

后端：

```bash
cd backend
uvicorn app.main:app --reload
```

前端：

```bash
cd frontend
npm run dev
```

建议手动验证：

```text
清水寺
大阪城
伏见稻荷大社
未知问题
```

可选：

```bash
cd frontend
npm run lint
cd backend
python -m compileall app
```

## 完成定义

- 前后端可以同时启动。
- 前端输入问题会请求后端。
- 后端返回 Mock AnswerCard。
- 前端渲染返回卡片。
- loading / error / empty 状态存在。
- 快捷按钮可用。
- 本轮结果已归档。

## 输出格式

- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

---

# JAG-R006

## Round ID

JAG-R006

## Round Name

Chat Experience Polish

## 本轮目标

优化基础聊天体验，让 Japan AI Guide 的第一阶段外壳具备可展示的产品感。

本轮目标是体验打磨，不做真实 AI、不做数据库、不做包车。

## 本轮任务

### 执行任务

- 实现聊天记录在当前会话内保存。
- 左侧历史栏点击可恢复回答。
- 实现自动滚动到底部。
- 实现 Enter 发送。
- 实现 Shift + Enter 换行。
- 实现基础 streaming mock 效果。
- 实现移动端响应式优化。
- 优化空状态欢迎页。
- 优化错误状态提示。
- 优化 loading 动画。
- 输出体验说明文档：`docs/CHAT_EXPERIENCE_SPEC.md`
- 创建本轮结果目录：`runtime/task_results/JAG-R006/`

### 测试任务

- 连续提问 3 次。
- 左侧历史记录出现 3 条。
- 点击历史记录可恢复回答。
- Enter 可发送。
- Shift + Enter 可换行。
- 移动端布局不崩坏。
- loading 与 error 状态可见。
- streaming mock 不影响 AnswerCard 最终渲染。

### 协作验收任务

- 输出聊天体验说明。
- 输出历史栏行为说明。
- 输出键盘交互说明。
- 输出移动端检查说明。
- 标记仍属于 Mock 的部分。

## 允许修改

```text
frontend/
docs/
runtime/task_results/JAG-R006/
```

必要时可轻微修改：

```text
backend/app/
```

但只允许为了支持已有 Mock API，不允许新增真实业务。

## 禁止修改

```text
真实 AI API
数据库
TTS
地图
包车
DaDa 平台相关目录
workbench 核心执行器
```

## 必须运行的验证

前端：

```bash
cd frontend
npm run dev
```

后端：

```bash
cd backend
uvicorn app.main:app --reload
```

可选：

```bash
cd frontend
npm run lint
```

## 完成定义

- 聊天体验自然。
- 历史记录可用。
- 输入体验接近 ChatGPT。
- 移动端可用。
- loading/error/empty 状态完整。
- PHASE 1 可以作为可展示 MVP 外壳。
- 本轮结果已归档。

## 输出格式

- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

---

# PHASE 1 完成定义

当 JAG-R001 ~ JAG-R006 全部完成后，PHASE 1 视为完成。

必须达到：

- 前端页面具备 ChatGPT 风格。
- 后端 API 骨架存在。
- 前后端可真实联通。
- AnswerCard Mock 协议稳定。
- 用户可输入问题并看到 AnswerCard。
- 历史记录、快捷按钮、语言选择可用。
- 不依赖真实 AI。
- 不依赖数据库。
- 不依赖 TTS。
- 不依赖地图。
- 所有 Round 都有结果归档。

---

# PHASE 1 之后进入

# PHASE 2 · AnswerCard Engine

下一阶段重点：

- Intent Router
- AnswerCard Builder
- 内容库查询
- 缓存策略
- 数据库接入
- 低 Token 成本架构
