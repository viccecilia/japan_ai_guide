# JAG-R004 AnswerCard Schema Foundation

## 修改了什么

- 新增前端 AnswerCard TypeScript 类型：`frontend/types/answer-card.ts`。
- 新增前端 Mock AnswerCard 数据：`frontend/mock/answer-cards.ts`。
- 将前端 `AnswerCard` 改为协议 Renderer，按 `card_type` 区分展示。
- Renderer 支持缺失字段兜底，不因 optional 字段缺失崩坏。
- 更新后端 `backend/app/schemas/chat.py`，建立 AnswerCard Schema 和 `CardType` 枚举。
- 更新后端 `backend/app/services/chat_service.py`，返回协议化 Mock AnswerCard。
- 输出协议文档：`docs/ANSWER_CARD_SCHEMA.md`。
- 创建本轮结果目录并归档验证结果。

## 每个任务状态

| 任务 | 状态 |
| --- | --- |
| 定义 AnswerCard TypeScript 类型 | 完成 |
| 定义后端 AnswerCard Schema | 完成 |
| 统一 `card_type` 枚举 | 完成 |
| 建立 Mock AnswerCard 数据 | 完成 |
| 建立前端 AnswerCard Renderer | 完成 |
| 支持 `spot_card` | 完成 |
| 支持 `city_card` | 完成 |
| 支持 `food_card` | 完成 |
| 支持 `route_card` | 完成 |
| 支持 `culture_card` | 完成 |
| 支持 `generic_card` | 完成 |
| Mock 包含清水寺、伏见稻荷大社、大阪城、奈良公园 | 完成 |
| 输出 `docs/ANSWER_CARD_SCHEMA.md` | 完成 |
| 创建结果目录 | 完成 |

## 验证结果

- 前端 `npm.cmd run check`: 通过。
- 前端 `npm.cmd run build`: 通过。
- 后端 AST 语法检查：通过，18 个 Python 文件。
- 后端 `uvicorn app.main:app --reload`: 已运行，`http://127.0.0.1:8000`。
- 前端 `npm.cmd run dev`: 已运行，`http://127.0.0.1:3000`。
- `/api/chat/query`: 返回新 AnswerCard 协议。
- `card_type` 区分展示：后端和前端 Mock 覆盖 6 种类型。
- 中文内容：接口样例中正常显示。
- 字段缺失：前端 Renderer 使用 `Partial<AnswerCardData>`、`fallbackCard` 和空数组兜底。

## 协作验收结果

归档文件：

- `runtime/task_results/JAG-R004/answer-card-api-samples.json`
- `runtime/task_results/JAG-R004/validation-results.json`
- `runtime/task_results/JAG-R004/frontend-dev.stdout.log`
- `runtime/task_results/JAG-R004/backend-dev.stderr.log`

## AnswerCard JSON 样例

完整样例见 `answer-card-api-samples.json`。核心结构：

```json
{
  "id": "spot_kiyomizu",
  "card_type": "spot_card",
  "title": "清水寺 Kiyomizu-dera",
  "subtitle": "京都 · 寺院文化 · 半日路线",
  "summary": "京都代表性寺院，适合第一次来京都的游客理解寺院文化和东山路线。",
  "sections": [
    {
      "title": "景点讲解",
      "body": "清水寺以木造舞台和东山景观闻名，是京都最具代表性的寺院之一。",
      "source": "ai"
    }
  ],
  "meta": {
    "language": "zh-CN",
    "mock": true,
    "sources": ["mock"]
  }
}
```

## 字段来源标记

- AI 未来生成：`summary`、`sections`、部分 `highlights`。
- 数据库未来提供：`id`、景点基础信息、附近景点、美食、城市/分类信息。
- 计算逻辑未来生成：路线顺序、可用 actions、动线建议。
- Mock 当前提供：全部字段当前均为 Mock 或协议占位。

## 未完成 / 风险

- 本轮不接真实 AI、数据库、地图、TTS。
- TypeScript 类型和 Pydantic schema 是双份定义，未来需要考虑 OpenAPI 生成类型，避免协议漂移。
- 前端目前仍使用本地 Mock Renderer，尚未调用后端 `/api/chat/query`。

## 下一轮建议

- JAG-R005 建议将前端输入流接入 `/api/chat/query`，用后端 Mock AnswerCard 替换本地 Mock。
- 同时补充 loading、API error、empty AnswerCard 的交互状态。
