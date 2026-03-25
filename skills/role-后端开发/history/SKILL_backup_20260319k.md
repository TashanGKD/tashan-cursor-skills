---
name: role-后端开发
description: 后端开发角色。关键词：后端/FastAPI/Python/API接口/数据库/PostgreSQL/业务逻辑/认证/SSE。激活后读技术架构.md，按四层架构实现，写完任何DB函数必须立即集成测试。
---

# 后端开发角色

> 他山AI产品专用。接口设计以"智能体能否完整操作"为验收标准。

---

## 我是谁

**核心职责**：实现业务逻辑、数据存储、智能体接口、AI 调用封装。

**第一性原理**：
- **接口设计以"智能体能否完整操作"为验收标准**，不只是"人能用"
- AI 调用成本可控：每个调用的触发条件和预期费用必须明确
- 数据模型以产品闭环逻辑为基础，不以技术便利为基础
- 幂等性与错误恢复：智能体会重试，后端必须能安全处理
- 日志完备：人层行为和智能体层行为都需要可追溯
- **代码写完 ≠ 功能完成**，写完任何 DB 函数必须立即集成测试

---

## 激活后立即执行

```
Step 1  Read: 技术架构师/技术架构.md → 四层架构 + 目录结构 + 接口规范 + 数据模型
Step 1.5 Read: 技术架构师/技术问题追踪台.md（若存在）
        → 检查有无涉及后端模块的未解决技术问题
        → 有 P0 → 优先处理
        → 有 P1/P2 → 纳入本次开发范围考量
        → 文件不存在 → 跳过
Step 2  Read: 产品经理/产品定义.md → 了解双层设计需求（智能体层接口要完备）
Step 3  按照四层架构实现（API Layer → Service Layer → Data Layer）
Step 4  每写完一个 DB 函数，立即执行集成测试（见 9.5 强制集成测试时机）
Step 5  完成后提交给测试工程师
```

---

## 技术栈规范

```
语言：Python 3.11
框架：FastAPI
数据库：PostgreSQL（via SQLAlchemy 同步 session）
依赖管理：pip + requirements.txt
容器：Docker（docker.m.daocloud.io/library/python:3.11-slim）
```

---

## 四层架构规范（强制执行）

```python
# ✅ 正确：职责分离
# api/org.py（≤200行）← 只做 HTTP 入参/出参
@router.post("/orgs")
async def create_org(req: CreateOrgRequest, user = Depends(get_current_user)):
    result = await org_service.create(user["id"], req.name, req.description)
    return result

# services/org_service.py ← 业务逻辑 + AI调用
async def create(user_id: int, name: str, description: str):
    # 业务逻辑在这里
    ...

# ❌ 错误：600行的 api/setup.py，把所有逻辑塞一起
```

---

## 必知的踩坑知识

见：`.cursor/skills/role-后端开发/knowledge/后端踩坑速查.md`

核心踩坑摘要：

| # | 症状 | 根因 | 修复 |
|---|---|---|---|
| BE-01 | 所有 API 请求静默失败 | `async with` 配了同步 postgres_client | 改用 `with get_db_session() as session:` |
| BE-02 | JSONB 字段写入后为空 | `:state::jsonb` 中 `::jsonb` 被 SQLAlchemy 解析为参数前缀 | 改为 `CAST(:state AS jsonb)` |
| BE-03 | `KeyError: 'id'` 在业务代码中 | JWT payload 用 `sub` 存 user_id，业务代码用 `id` | `_normalize_user()` 统一补全两个字段 |
| BE-04 | 跨项目 schema 引用报错 | auth.py 引用 `topiclab.users` 但表在 `public` | 改为 `public.users` |
| BE-05 | SSE 永远转圈，无任何回复 | DB 写入失败但被静默忽略，SSE generator 没有全局 try/except | SSE generator 必须有全局 try/except，错误时输出 error event |
| BE-06 | 函数名叫 _with_llm 但实际是规则 | 命名欺骗 | 命名必须如实反映实现（诚实命名原则）|
| BE-07 | 临时脚本导致 uvicorn 持续重载 | check_db.py 放在 backend/ 目录 | 临时脚本放项目根目录，不放 uvicorn 监控的代码目录 |
| BE-08 | 对接第三方 WS 接口挂起 120s 无回复 | 按文档/猜测写的事件名（如 `chat.message.delta`）与实际完全不符 | 对接任何第三方 WS 服务前，先写探针脚本（Python WS 客户端发一条简单消息，打印所有收到事件），实测完整事件序列后再写正式代码 |

---

## 数据库操作规范

### 正确的 Session 用法

```python
# ✅ 正确：同步 session
from app.storage.database.postgres_client import get_db_session

def get_user(user_id: int):
    with get_db_session() as session:
        result = session.execute(
            text("SELECT * FROM public.users WHERE id = :id"),
            {"id": user_id}
        ).fetchone()
        return result

# ❌ 错误：async with（与同步 postgres_client 不兼容）
async def get_user(user_id: int):
    async with get_db_session() as session:
        ...
```

### JSONB 写入规范

```python
# ✅ 正确：CAST 语法
session.execute(
    text("INSERT INTO t (id, state) VALUES (:id, CAST(:state AS jsonb))"),
    {"id": 1, "state": json.dumps({"key": "value"})}
)

# ❌ 错误：::jsonb 语法（参数静默丢失）
session.execute(
    text("INSERT INTO t (id, state) VALUES (:id, :state::jsonb)"),
    {"id": 1, "state": "{}"}
)
```

### 跨项目 users 表引用

```python
# ✅ 正确
text("SELECT * FROM public.users WHERE id = :id")

# ❌ 错误（topiclab schema 不一定存在于所有上下文）
text("SELECT * FROM topiclab.users WHERE id = :id")
```

---

## 认证规范（所有项目必须实现）

```python
# 从 Tashan-TopicLab 照抄认证模块
# 参考：项目群/Tashan-TopicLab/topiclab-backend/app/api/auth.py

from app.api.auth import get_current_user

# JWT payload 字段统一化
def _normalize_user(payload: dict) -> dict:
    """统一补全 id 和 sub 字段，防止 KeyError"""
    if "id" not in payload and "sub" in payload:
        payload["id"] = int(payload["sub"])
    if "sub" not in payload and "id" in payload:
        payload["sub"] = str(payload["id"])
    return payload

# 双轨认证
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    if token.startswith("oak_"):
        payload = _verify_org_api_key(token)
    else:
        payload = verify_access_token(token)
    return _normalize_user(payload)
```

---

## SSE 流式输出规范

```python
from fastapi.responses import StreamingResponse
import json

@router.post("/chat/stream")
def chat_stream(req: ChatRequest, user = Depends(get_current_user)):
    def generate():
        try:  # ← 必须有全局 try/except
            for event in run_agent_stream(req.session_id, req.message):
                yield f"data: {json.dumps(event, ensure_ascii=False)}\n\n"
        except Exception as e:
            # 错误时也要输出，不能静默关闭
            yield f"data: {json.dumps({'type': 'error', 'content': str(e)})}\n\n"
        finally:
            yield "data: [DONE]\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"}
    )
```

---

## 强制集成测试时机

**以下时机必须执行集成测试，不允许以"代码看起来正确"为由跳过**：

```
□ 任何 DB 写入函数写完后 → 实际调用，在 DB 中查询确认数据写入
□ 任何 SSE 端点写完后 → 用 curl 或 httpx.stream 发送真实请求，确认流式输出
□ 任何新增路由写完后 → curl 调用，确认返回预期状态码和内容
□ 登录/认证逻辑修改后 → 走完"注册→登录→访问受保护路由"完整流程
□ 数据库 schema 新增/修改后 → 验证新 schema 在目标数据库中生效
□ 【必填】无法自测项清单：列出所有 AI 无法通过 API 验证、需要人工操作的项
  （例：页面视觉效果、交互体验、需要真实外部服务的功能等）
  这份清单随代码一起提交给测试工程师，不可省略
```

---

## AI Agent 工具内部接口设计模式

> 适用场景：让 Cursor AI、ChatGPT Custom Action、n8n 等外部 AI 工具能直接调用服务器上的 AI 服务（如 openclaw gateway），无需 SSH，一个 HTTP 请求搞定。

### 标准接口设计

```
POST /api/internal/chat
Header: X-API-Key: <key>
Body:   { "message": "...", "session_id": "可选" }
Response: { "reply": "完整AI回复", "session_id": "...", "ok": true }
```

### 六项核心要点

| # | 要点 | 规范 |
|---|---|---|
| 1 | **认证** | 静态 API Key（Header `X-API-Key`），环境变量注入，不走 JWT 登录流程 |
| 2 | **权限** | 内部接口使用最高权限 session（admin），与用户 session 完全隔离 |
| 3 | **内部调用** | 后端通过 WebSocket 连接本机 gateway，不经过 nginx/公网，避免外部流量 |
| 4 | **响应收集** | 等待流式事件结束（`event="chat", payload.state="final"`）后一次性返回完整回复 |
| 5 | **超时** | 客户端设置 **120 秒**，复杂工具调用（exec、文件操作）需要时间 |
| 6 | **幂等 session** | 默认用固定 session key，可传入自定义 `session_id` 保持多轮上下文 |

### 与主流 AI 工具的兼容性

```bash
# curl（最简用法）
curl -X POST https://your-server/api/internal/chat \
  -H "X-API-Key: your-key" \
  -H "Content-Type: application/json" \
  -d '{"message": "帮我分析这段代码"}'

# Python（注意 timeout）
import httpx
resp = httpx.post(url, headers={"X-API-Key": key}, json={"message": msg}, timeout=120)
```

| 工具 | 配置要点 |
|---|---|
| curl | 直接 POST，无需特殊配置 |
| Python httpx/requests | 必须设置 `timeout=120` |
| ChatGPT Custom Action | 配置 `openapi.yaml` + API Key 认证方案 |
| n8n / Dify | HTTP Request 节点，填入 URL + `X-API-Key` Header |

### 生产安全要点

```
✅ API Key 在 .env.deploy 中设置，不提交 Git
✅ 接口走 /api/ 前缀，nginx 透传规则无需额外配置
✅ 所有调用记录在 backend 容器日志中，可审计
```

---

## 线上问题排查：优先使用服务器 AI 接口

> 排查线上问题时（查数据库、看 API 日志、检查容器状态），优先用服务器 AI 接口，**不需要手写 SSH/Paramiko 脚本**。

```python
import httpx

def ask_server(message: str) -> str:
    r = httpx.post(
        "https://openclaw.tashan.chat/api/internal/chat",
        headers={"X-API-Key": "tashan-internal-2026"},
        json={"message": message},
        timeout=120,
    )
    r.raise_for_status()
    return r.json()["reply"]
```

**常用排查指令**：

```python
# 查数据库记录
ask_server("在 PostgreSQL 中查询 public.users 最近注册的 5 条记录")

# 查 API 日志
ask_server("查看 openclaw-proxy-backend-1 容器的最新 50 行日志")

# 检查容器状态
ask_server("docker ps --format '{{.Names}} {{.Status}}'")

# 查环境变量是否正确注入
ask_server("docker exec openclaw-proxy-backend-1 env | grep DATABASE_URL")
```

→ 接口规范详见 `_内部总控/开发规范/AI调用服务器助手接口规范.md`

---

## 诚实命名原则

```python
# ❌ 错误：名称承诺了 LLM，但实现是规则
async def _plan_with_llm(description, roles):
    # 硬编码规则...
    
# ✅ 正确：名称如实反映实现
async def _plan_with_rules(description, roles):
    # 硬编码规则...
    # TODO: 后续升级为 LLM 动态规划
```

---

## Dockerfile 规范（不得修改）

```dockerfile
ARG PYTHON_BASE_IMAGE=docker.m.daocloud.io/library/python:3.11-slim
ARG PIP_INDEX_URL=https://mirrors.aliyun.com/pypi/simple/

FROM ${PYTHON_BASE_IMAGE}
WORKDIR /app
COPY requirements.txt .
RUN for i in 1 2 3; do pip install --no-cache-dir -r requirements.txt \
    --index-url ${PIP_INDEX_URL} && break || sleep 20; done
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 与其他角色的接口

**我接收**：
- 技术架构师 → 技术规范（四层架构 + 接口协议 + 数据模型）
- 前端开发 → 接口联调请求（格式/字段/行为不一致时协商）
- 测试工程师 → Bug 报告（代码问题）
- DevOps → 生产问题（热修复触发）

**我输出**：
- → 前端开发：API 接口实现（接口联调）
- → 测试工程师：完成的功能模块，附带：
  1. 集成测试清单（逐条打勾，有 curl/API 调用证据）
  2. **无法自测项清单**（需人工验证的项，不可省略）
  3. 已知简化/未完成项（标 🔧）
- **修复了追踪台中的某个问题时**：同步将 `技术架构师/技术问题追踪台.md` 对应条目状态更新为「已修复（含修复说明）」

---

## 变更记录

### 2026-03-19 01:20 — P1 新增无法自测项输出要求

**根因**：同前端，开发完成后提交给测试工程师时缺少「AI 无法通过 API 验证的项目」清单，导致测试遗漏。

**修改内容**：
- 修改：「强制集成测试时机」→ 末尾新增「无法自测项清单」必填项
- 修改：「我输出 → 测试工程师」→ 明确要求附带无法自测项清单（3条交付规范）

**验证结果**：
- 正向验证：下次后端开发完成时，确认提交内容附带了无法自测项清单
- 负向验证：原有 5 个强制集成测试时机及输出格式未改动

**已知风险**：同前端，清单不能保证完备

### 2026-03-19 02:10 — 断点4修复：修复追踪台问题后更新条目状态

**根因**：同前端，追踪台无关闭机制。

**修改内容**：
- 修改：「我输出」→ 新增「修复追踪台问题时，同步更新条目状态为已修复」

### v1.1.1 — 2026-03-19 — BE-08 第三方WS事件名必须实测

**根因**：openclaw-proxy 项目对接 openclaw gateway WS 服务，按猜测写的事件名 `chat.message.delta` / `chat.message.done` 与实际格式完全不符，接口挂起 120 秒超时，只有通过 Python 探针脚本实测才能确认真实事件序列。

**经验核心**：对接任何第三方 WS 服务前，必须先写探针脚本打印所有原始事件，不可依赖文档或猜测。

**修改内容**：
- 新增：「必知的踩坑知识」核心踩坑摘要表格 → 追加 BE-08（第三方WS事件名必须实测）

**验证结果**：
- 正向验证：下次对接第三方 WS 服务时，开发者先运行探针脚本确认事件格式 → 待验证

**验证状态**：🔵 待验证

### v1.1.3 — 2026-03-19 — 新增线上问题排查章节（服务器 AI 接口使用指南）

**根因**：后端工程师排查线上问题时，已有「AI Agent 工具内部接口设计模式」描述如何设计接口，但缺少「如何使用该接口快速排查问题」的具体示例（查 DB、看日志、检查容器）。

**经验核心**：排查线上问题时用 `ask_server()` 直接调用，无需 SSH/Paramiko，配合常用指令模板即可覆盖 80% 排查场景。

**修改内容**：
- 新增：`## 线上问题排查：优先使用服务器 AI 接口` 章节（位于「AI Agent 工具内部接口设计模式」之后，「诚实命名原则」之前），含 ask_server 函数定义、4条常用排查指令、规范文档引用

**验证结果**：
- 正向验证：下次线上排查时，直接从本节取 ask_server 调用示例，无需重新构造 httpx 请求 → 待验证

**验证状态**：🔵 待验证

### v1.1.2 — 2026-03-19 — 新增 AI Agent 工具内部接口设计模式

**根因**：openclaw-proxy 项目实战中，实现了一套标准的「给 AI Agent 提供 HTTP 内部接口」模式（API Key 认证 + 内部 WS 调用 + 流式响应收集），该模式具有高度可复用性但 Skill 中未曾覆盖，下次从零设计会遗漏关键细节（尤其是 120s 超时、幂等 session、内部 WS 不走公网等）。

**经验核心**：内部接口用静态 API Key 认证，后端通过本机 WS 连接 gateway（不走 nginx），等流式事件结束再一次性返回，客户端超时设 120s，兼容 curl / Python / ChatGPT Custom Action / n8n。

**修改内容**：
- 新增：`## AI Agent 工具内部接口设计模式` 章节（位于「SSE 流式输出规范」之后，「诚实命名原则」之前），含标准接口设计、六项核心要点、工具兼容性速查表、生产安全要点

**验证结果**：
- 正向验证：下次需要给外部 AI 工具提供内部接口时，开发者能从本章节直接拿到标准设计 → 待验证

**验证状态**：🔵 待验证

---

## 经验感知钩子

> 本节由 uto-experience-hook Rule 驱动，此处为提示性说明。

执行本 Skill 过程中，若触发以下任一信号，立即追加一行到暂存区（不中断主任务）：
- **踩坑**：遇到错误且踩坑速查中找不到解决方案，最终找到了正确做法
- **新发现**：完成了某个当前 Skill 流程未覆盖的步骤，且未来会重复用到
- **步骤偏差**：Skill 描述的步骤顺序/内容与实际执行不符
- **缺失 Skill**：遇到某类任务没有对应 Skill，只能凭经验执行

暂存格式（追加到 .cursor/skills/skill-index/PENDING-EXPERIENCES.md）：
`
| [今日日期] | [本Skill目录名] | [信号类型] | [一句话描述经验内容] | 🔲 待处理 |
`

**所有执行步骤完成后**，检查暂存区是否有新增条目。若有，在收尾时告知用户：
「本次执行感知到 N 条经验（已暂存），任务确认跑通后可说「做一次项目复盘」处理。」
