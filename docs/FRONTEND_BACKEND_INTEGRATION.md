# JAG-R005 Frontend Backend Integration

## Scope

本轮实现前端和 FastAPI 后端的真实联通，但仍然只返回 Mock AnswerCard。

已完成链路：

```text
用户输入问题或点击快捷按钮
  -> frontend/services/chat-api.ts
  -> POST http://127.0.0.1:8000/api/chat/query
  -> backend/app/routers/chat.py
  -> backend/app/services/chat_service.py
  -> 前端 AnswerCard Renderer 渲染返回卡片
```

本轮未接入真实 AI、数据库、地图、TTS 或登录。

## 启动方式

后端：

```powershell
cd C:\PycharmProjects\pythonProject01\Japan Guide\japan_ai_guide\backend
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

前端：

```powershell
cd C:\PycharmProjects\pythonProject01\Japan Guide\japan_ai_guide\frontend
npm.cmd run dev -- --hostname 127.0.0.1 --port 3000
```

浏览器访问：

```text
http://127.0.0.1:3000
```

## Frontend API Service

文件：`frontend/services/chat-api.ts`

默认后端地址：

```text
http://127.0.0.1:8000
```

可用环境变量覆盖：

```text
NEXT_PUBLIC_API_BASE_URL
```

核心方法：

```ts
queryChat(question: string, language = "zh-CN"): Promise<AnswerCard | null>
```

## Request Sample

```http
POST /api/chat/query HTTP/1.1
Content-Type: application/json

{
  "question": "清水寺",
  "language": "zh-CN"
}
```

## Response Sample

```json
{
  "ok": true,
  "data": {
    "question": "清水寺",
    "answer_card": {
      "id": "spot_kiyomizu",
      "card_type": "spot_card",
      "title": "清水寺 Kiyomizu-dera",
      "subtitle": "京都 · 寺院文化 · 半日路线",
      "summary": "京都代表性寺院，适合第一次来京都的游客理解寺院文化和东山路线。",
      "sections": [],
      "highlights": [],
      "recommendations": [],
      "actions": [],
      "meta": {
        "language": "zh-CN",
        "mock": true,
        "sources": ["mock"]
      }
    }
  },
  "error": null,
  "meta": {
    "mock": true,
    "language": "zh-CN"
  }
}
```

## Mock Matching Logic

后端根据 `question` 中的关键词返回不同 Mock 卡片：

- `清水寺` / `kiyomizu` -> `spot_kiyomizu`
- `大阪城` / `osaka castle` -> `spot_osaka_castle`
- `伏见稻荷` / `稻荷` / `fushimi` -> `spot_fushimi_inari`
- `奈良公园` / `奈良鹿` / `nara` -> `spot_nara_park`
- `京都` -> `city_kyoto`
- `抹茶` -> `food_matcha`
- `路线` -> `route_kyoto_half_day`
- `神社` / `寺庙` -> `culture_shrine_temple`
- 其他问题 -> `generic_fallback`

## UI States

前端当前支持：

- Empty：初始状态或空输入，不请求后端。
- Loading：请求发送后展示“正在请求后端”。
- Success：渲染后端返回的 AnswerCard。
- Error：网络失败、后端关闭、响应不可解析或 API 返回 `ok=false` 时展示错误卡片。

## Next API Hooks

下一轮接真实 API 或业务逻辑时优先替换：

- `backend/app/services/chat_service.py`：当前 Mock 匹配逻辑。
- `frontend/services/chat-api.ts`：当前仅有 chat query 方法。
- `frontend/src/components/chat/ChatShell.tsx`：当前没有会话 ID、历史持久化或流式输出。
- `backend/app/main.py`：当前 CORS 只开放本地前端地址。
