# JAG-R002 API Foundation

## 修改了什么

- 整理 FastAPI 后端结构，新增 `routers/`、`schemas/`、`services/`。
- 保留 `/health` 健康检查。
- 新增统一 API Response 结构：`ok`、`data`、`error`、`meta`。
- 新增 Mock Router：
  - `POST /api/chat/query`
  - `POST /api/spots/search`
  - `GET /api/history/list`
  - `GET /api/language/list`
- `/api/chat/query` 返回 Mock AnswerCard。
- 增加统一错误响应处理：请求校验错误和 404 等 HTTP 错误都返回统一结构。
- 新增接口说明文档：`docs/api-foundation.md`。

## 每个任务状态

| 任务 | 状态 |
| --- | --- |
| 整理 FastAPI 项目结构 | 完成 |
| 保留 `/health` | 完成 |
| 建立 `routers/` | 完成 |
| 建立 `schemas/` | 完成 |
| 建立 `services/` | 完成 |
| 建立统一 API Response | 完成 |
| 建立 `/api/chat/query` | 完成 |
| 建立 `/api/spots/search` | 完成 |
| 建立 `/api/history/list` | 完成 |
| 建立 `/api/language/list` | 完成 |
| Mock AnswerCard 返回 | 完成 |
| 创建结果目录 | 完成 |

## API 列表

| Method | Path | 说明 |
| --- | --- | --- |
| GET | `/health` | 健康检查 |
| POST | `/api/chat/query` | Mock AI 导览回答 |
| POST | `/api/spots/search` | Mock 景点搜索 |
| GET | `/api/history/list` | Mock 历史记录 |
| GET | `/api/language/list` | 语言列表 |

## 启动命令

```powershell
cd backend
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

当前验证服务地址：

```text
http://127.0.0.1:8000
```

## Mock 返回样例

完整样例已归档：

- `runtime/task_results/JAG-R002/api-samples.json`
- `runtime/task_results/JAG-R002/validation-results.json`

`/api/chat/query` 返回核心结构：

```json
{
  "ok": true,
  "data": {
    "question": "清水寺怎么安排半日游",
    "answer_card": {
      "title": "清水寺怎么安排半日游",
      "mock": true
    }
  },
  "error": null,
  "meta": {
    "mock": true,
    "language": "zh-CN"
  }
}
```

统一错误结构：

```json
{
  "ok": false,
  "data": null,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed."
  },
  "meta": {
    "path": "/api/chat/query",
    "detail_count": 1
  }
}
```

## 验证结果

- FastAPI dev server：已启动。
- `/health`：通过。
- `/api/chat/query`：通过，返回 Mock AnswerCard。
- `/api/spots/search`：通过。
- `/api/history/list`：通过。
- `/api/language/list`：通过。
- 请求校验错误：通过，返回统一结构。
- 404 错误：通过，返回统一结构。
- AST 语法检查：通过，18 个 Python 文件。

说明：`python -m compileall app` 在本机 Windows 环境触发 `__pycache__` 写入权限和控制台编码问题，因此本轮使用不写字节码的 AST 解析检查替代。

## 本轮未接真实业务

- 未接真实 AI。
- 未接数据库。
- 未接景点搜索引擎。
- 未接地图。
- 未接 TTS。
- 未接用户会话或历史持久化。

## 未完成 / 风险

- API 结构是 v1 Mock 契约，后续接真实业务前仍需要确认字段是否完全满足前端 AnswerCard。
- 当前 `/health` 沿用简单结构，不包统一 response envelope，便于运维健康检查。

## 下一轮建议

- JAG-R003 建议让前端调用 `/api/chat/query`，把 Mock AnswerCard 从前端静态数据切换为后端 Mock API。
- 同时定义前端请求错误展示方式和加载状态。
