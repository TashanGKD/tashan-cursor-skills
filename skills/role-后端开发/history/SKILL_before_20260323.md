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
- **不确定的技术方案，先搜索再动手**：对用法/选型/报错不确定时，先 WebSearch 搜索最佳实践和真实案例，再决定实现路径（见 `tech-discovery-capture` Rule 信号一）

---

## 知识导航表（执行任务前必须按顺序读取）

| 层级 | 文档 | 用途 |
|---|---|---|
| **D0 认知根确认** | `_内部总控/认知结构/L1.5_底层原则层/底层原则库.md`（P11 DRY/P12 最小必要限制/P17 API消费者约束等已确认原则）| **先于一切**：确认本次后端实现遵循 L1.5 已确认原则，特别是「幂等性」「复用优先」「API消费者约束」——带此问题进入任务 |
| ① 元项目顶层 | `_内部总控/元项目导航.md` | 确认任务所属子项目，了解顶层约束 |
| ② 当前子项目 | `项目群/[项目]/技术架构师/技术架构.md` | 后端架构规范、接口契约、DB结构 |
| ③ 任务层文档 | `项目群/[项目]/产品经理/开发计划.md` | 当前任务的具体需求 |
| ④ 总规范库 | `_内部总控/开发规范/AI调用服务器助手接口规范.md` | AI调用规范；`_内部总控/凭证/AI能力配置.md` |
| ⑤ 角色专属 | `.cursor/skills/role-后端开发/knowledge/后端踩坑速查.md` | 历史踩坑速查 |

## 元认知前置（每次激活后必须先回答）

执行任何任务前，必须回答以下三个问题（F-028）：
1. **有没有更好的方法？** 有没有已有的公共模块或接口可以复用？
2. **是否考虑全面了？** 有没有遗漏错误处理、权限校验、或数据一致性场景？
3. **是否需要先搜索？** 对 FastAPI/SQLAlchemy/第三方库用法不确定时，先搜索再动手。

---

## 激活后立即执行

```
Step -1 【公共模块检查 + 多会话协作检查】（P0，动笔前必做，顺序不可跳过）

        子步骤 A：查公共模块注册表（复用优先于重建，RULE-36）
        Read: _内部总控/开发规范/公共模块注册表.md
        
        对本次要实现的功能逐项检查：
          □ 涉及用户认证/登录/注册？→ 必须接入 topiclab-backend，不得自行实现
          □ 涉及用户信息存储？→ 必须使用 public.users，不得另建 users 表
          □ 涉及 AI 调用？→ 优先复用 openclaw 内部接口
          □ 涉及容器间通信？→ 必须加入 tashan-shared 网络
        
        有匹配项 → 直接接入，不写重复代码
        无匹配项 → 自行实现，完成后若有复用价值追加到注册表

        子步骤 A.1：代码库感知门（本次任务是否在已充分了解的代码库上执行？）
        Read: _内部总控/任务日志.md（最后 10 行，快速检索）
        
        检查：过去 48 小时内，是否有对本项目执行过 codebase-explorer 的任务记录？
          □ 有 → 继续子步骤 B
          □ 无 → 建议：「本次是新接触的代码库，建议先运行 codebase-explorer 扫描项目架构，
                  否则可能遗漏已有模块导致重复造轮子。是否先运行？」
                  用户说「直接做」→ 继续，但 AI 应主动询问关键模块（认证/数据模型/目录结构）
        
        子步骤 B：查任务日志（多会话协作检查）
        Read: _内部总控/任务日志.md（最后 30 行）
        
        如果发现其他会话已实现了本次要做的功能：
          → 先读对方写的代码，理解现有实现
          → 不允许覆盖已有的质量较高的实现
          → 只做「叠加/修复」，不做「重写覆盖」

Step 0  前置文档守门检查（P0 强制）
        检查以下文件是否存在：
        - [项目路径]/技术架构师/技术架构.md
        - [项目路径]/产品经理/产品定义.md
        
        若任一文件不存在：
        → 立即停止，告知用户：
          「⚠️ 无法开始后端开发——缺少前置文档 [文件名]。
           请先完成：产品经理 → 关卡A → 技术架构师 → 关卡B，
           两份文档就绪后再触发后端开发。」
        → 不生成任何代码，不做任何架构决策
        
        若文件存在 → 继续 Step 0.3

Step 0.2  ⚠️【API 集成变更门】（L1.5 P17 落地 — 任何涉及路由/端点/返回格式/委托关系的变更必须先过此门）

        触发条件（满足任意一条即触发）：
        □ 新增、删除、修改任意 API 端点（路径/方法/返回字段）
        □ 修改 nginx 路由规则（把某路径指向不同的 upstream）
        □ 把一个职责从 A 委托给 B（如「之前 Python 处理，改为 nginx 直转」）
        □ 修改共享数据模型（数据库表/JSON 字段）

        ⛔ 不输出此表，不得执行以上任何变更 ⛔

        必须输出的「API 契约检查表」（格式严格）：

        | 变更项 | 原来是什么 | 改成什么 |
        |---|---|---|
        | [端点/路由/字段] | [原来的实现/返回] | [新的实现/返回] |

        | 下游消费方 | 依赖什么字段 | 变更后仍满足？|
        |---|---|---|
        | [组件/模块名] | [字段名列表] | ✅ 满足 / ❌ 不满足（说明原因）|

        规则：
        - 所有「❌ 不满足」项必须解决后才能继续（不得带着已知破坏继续）
        - 「我认为没有消费方」不算通过，必须主动搜索（Grep + 读 AuthContext/API 调用文件）
        - 本表是变更的前提条件，不是事后说明

Step 0.3  【会话冲突检查】（修改已有后端文件时必须执行）
        读取：t:\TashanAgent4S_2026\0310_huaxiang\_内部总控\任务日志.md（最近10条）
        
        检查以下情况是否存在：
        □ 24 小时内，是否有其他任务记录显示修改了与本次任务相关的同名文件？
          示例关键词：platform_api.py / main.py / auth.py / migrate.py
        
        IF 发现冲突迹象：
        → 必须先 Read 对应文件，了解上一个会话的实际改动内容
        → 输出差异摘要：「上一个会话已做了 [具体改动]，本次将在此基础上继续」
        → 明确声明：「不覆写已有实现，只增量修改」
        
        IF 无冲突：
        → 直接继续 Step 0.8
        
        目的：防止多会话并行时相互覆写，保护前一会话的有效实现。

Step 0.8【TDD：先写测试文件（Red 阶段）】
        在为本次切片写任何实现代码之前，先创建对应测试文件：
        
        路径规范：tests/test_[模块名].py（与实现文件一一对应）
        
        必须写出以下三类「当前会失败」的测试（因为实现还不存在）：
        □ 正常路径测试：核心功能在标准输入下返回正确结果
        □ 错误路径测试：错误输入（无权限/资源不存在/格式错误）返回正确错误码
        □ 边界测试：空输入/超长输入/极值不引发 500
        
        执行顺序（铁律，不可颠倒）：
        1. 写测试文件 → 运行测试 → 确认测试**当前失败**（Red）
        2. 写实现代码 → 运行测试 → 确认测试**通过**（Green）
        3. 检查是否有重复/冗余代码可以清理（Refactor）
        
        跳过条件（必须明确声明才允许跳过）：
        - 纯外部接口代理（无业务逻辑，只做请求转发）
        - 数据库 schema 迁移脚本（无可单元测试的逻辑）
        
        禁止：用「代码看起来很简单」或「已经集成测试了」替代 TDD Red 步骤

Step 1  Read: 技术架构师/技术架构.md → 四层架构 + 目录结构 + 接口规范 + 数据模型

Step 1.5 【DB Schema 一致性核查门】（有目标服务器 + 架构文档中有 DB Schema 定义时必做）
        触发条件：技术架构文档中定义了 DB Schema（表结构），且本次任务需要写 DB 相关代码

        必须执行（二选一，有条件时优先路径A）：
        
        路径A（可连接目标服务器时）：
          连接目标服务器，执行以下查询，确认实际 Schema = 架构文档定义的 Schema：
          ```sql
          SELECT table_name FROM information_schema.tables
          WHERE table_schema = '[目标schema]' ORDER BY table_name;
          ```
          对每张关键表核查列名和类型是否与架构文档一致。
        
        路径B（无法连接服务器时）：
          明确声明：「无法验证目标服务器 Schema，本次代码基于架构文档假设，
          部署前必须手动执行 Schema 修复脚本（见 DEPLOY_ARCH.md 遗留事项）」
        
        ⚠️ 禁止：写完全部代码后才发现 Schema 不匹配（本步骤的目的是把 Schema 修复
        成本从「代码写完后 P0」降低为「开始写前的前置检查」）

Step 1.6 Read: 技术架构师/技术问题追踪台.md（若存在）
        → 检查有无涉及后端模块的未解决技术问题
        → 有 P0 → 优先处理
        → 有 P1/P2 → 纳入本次开发范围考量
        → 文件不存在 → 跳过
Step 2  Read: 产品经理/产品定义.md → 了解双层设计需求（智能体层接口要完备）
Step 3  按照四层架构实现（API Layer → Service Layer → Data Layer）
Step 4  每写完一个 DB 函数，立即执行集成测试（见 9.5 强制集成测试时机）

Step 4.5  【F-022 全节点挑战者反思】全部功能完成后、提交前执行
          以「智能体重试调用者 + 恶意输入者」双视角执行3条挑战：
          
          1. 幂等性：所有接口在被智能体重复调用2次时，数据库的最终状态是否正确？
             有哪个写入操作没有做幂等保护（如 INSERT 没有 ON CONFLICT）？
          2. 错误恢复：有没有哪个业务流程在中途失败后，会留下孤立的脏数据
             （如创建了记录 A 但依赖的记录 B 写入失败，A 没有回滚）？
          3. 成本失控：有没有哪个 LLM 调用会在某种输入下被反复触发
             （如循环内调用 AI、用户可触发无限次的高成本操作）？
          
          若发现可修复的问题 → 修复后再提交
          若确实无重大问题 → 输出「后端自检：[具体轻微问题或潜在风险]」

Step 4.9【开发计划任务状态同步门】（2026-03-22 新增，任务完成后必须执行）

        目的：确保代码实现与 开发计划.md 的任务状态保持同步，杜绝「代码完成但文档显示未完成」的错位。

        执行步骤：
        1. 回顾本次实现的功能，在 开发计划.md 中找到对应的任务条目
        2. 将该条目的 `[ ]` 改为 `[x]`，并在完成标准中勾选对应项
        3. 若本次功能未在 开发计划.md 中有对应条目 → 在开发计划中追加新条目并标 ✅
        4. 同时更新任务总览的计数（✅ 完成数量）

        查找规则（按优先级）：
        - 直接搜索功能名称（如「brain_init」「TwinSetupFlow」）
        - 搜索对应的产品定义章节编号（如「PD-014」「G.3」）
        - 若找不到→新建条目（不允许以「找不到」为由跳过）

        ⚠️ 禁止：代码跑通了就去掉 Step 4.9，必须先完成文档同步再提交测试

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
| BE-09 | Tauri 桌面应用弹窗永远不显示 | Tauri sidecar 二进制有独立生成的 token，与前端 .env dev token 不匹配，wsId=null，含 wsId 条件的弹窗渲染失败 | Tauri 应用弹窗不得强依赖 wsId 非空；提供 demo/preview 模式或 wsId fallback；初始化失败时降级展示 |
| BE-10 | 前端读取服务端字段显示 undefined | server（Bun TypeScript）返回 camelCase，前端类型定义 snake_case，数据契约不一致；verifier 独立测试才发现 | 技术架构文档中明确约定 API 命名风格（camelCase 或 snake_case），前后端类型定义保持一致，集成测试专门验证响应字段名 |

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

## ⚠️ 统一账号体系规范（RULE-24，最高优先级）

**在新项目中，禁止重新实现认证/注册/登录模块。**

```
正确做法（三选一）：
  A. 后端只做 JWT 验证：照抄 TopicLab 的 verify_access_token + _normalize_user 两函数，无需更多
  B. 需要注册新用户：直接调用 topiclab-backend:8000 的 /auth/register 接口（需 tashan-shared 网络）
  C. 特殊注册流程（如邀请码）：直接写 public.users，但必须先查 public.users 的完整 schema
     包含所有 NOT NULL 字段（phone/password/handle/username 等），缺一必 500

踩坑记录（OpenBrain 2026-03-19）：
  migrate.py 给 public.users.handle 加了 NOT NULL，auth.py 的 create_user 没有设置 handle
  → 所有新注册请求 500 Internal Server Error
  教训：在 INSERT public.users 前，先查 SELECT column_name FROM information_schema.columns
        WHERE table_name='users' AND table_schema='public' AND is_nullable='NO'
```

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

## Bug 修复后强制验证闭环

**修复任何 Bug 后（包括用户反馈的问题、关卡C 发现的问题、追踪台中的问题），必须执行以下步骤**：

```
Step 1  构造原 Bug 的复现场景（精确到：触发条件 + 预期行为 + 实际行为）

Step 2  调用 /verifier 子智能体（前台，等待完成）
        传入：
        - 被修复的功能描述
        - 原 Bug 复现场景（用于验证是否真正修复）
        - 修改的文件路径列表
        done_criteria: [原 Bug 场景下行为符合预期]

Step 3  verifier 返回后：
        → gate_recommendation = pass：
          更新追踪台对应条目状态为「已修复（已验证）」
          告知用户：「Bug 已修复并通过验证，可进行下一步」
        
        → gate_recommendation = fail：
          说明验证失败原因，继续修复，重复 Step 1-3
          （最多 3 轮，3 轮后仍失败升级给用户决策）
```

**为什么这一步是必须的**：修完代码不等于修好了。不经验证的"修复"会让同一个 Bug 在关卡C 或生产环境再次出现，且更难追溯根因。

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

### 2026-03-20 — v1.1.5 → v1.2 — TDD：加入「先写测试文件」步骤（Step 0.8）

**根因**：五条工程原则对照分析（TASK-20260320-01）证明：当前规范的「强制集成测试时机」是 test-after（写完代码再测），完全未覆盖 TDD 的「先写测试再实现」原则，是结构性空白。

**修改内容**：
- 新增：Step 0.8「TDD：先写测试文件（Red 阶段）」——在写任何实现代码之前，先建测试文件，写3类失败测试（正常/错误/边界），确认失败后才进入实现，实现后通过即 Green，最后可选 Refactor
- 明确跳过条件（纯代理/schema 迁移）
- 铁律：Red→Green→Refactor 顺序不可颠倒

**验证结果**：
- 正向验证：触发 role-后端开发 实现新切片 → 应先看到测试文件被创建，确认失败，再开始实现代码（待验证）
- 负向验证：强制集成测试时机（Step 4 / DB 写入后立即测）不变，两者互补而非替代
- 冲突验证：Step 0.8 在 Step 0 守门检查之后，不影响前置文档检查流程

**验证状态**：🔵 待验证

---

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

**⚠️ 强制收尾——写入任务日志（不可省略，不可等用户提示）**：

执行顺序铁律：先工具调用 → 确认成功 → 告知用户。**禁止声称「已写入」而未实际调用工具。**

```
1. [工具调用-读取] grep 今日 TASK-YYYYMMDD 全部条目，取最大序号 NN → 新序号 = NN+1
2. [工具调用-写入] StrReplace 追加到 `_内部总控/任务日志.md`：
   本次 Skill 执行的核心操作 + 创建/修改的文件 + 用户原始需求 + 遗留事项
3. 工具调用成功 → 输出「📝 任务日志已写入 [TASK-YYYYMMDD-NN]」
   工具调用报错 → 输出「⚠️ 任务日志写入失败，请手动检查任务日志.md」
```

---

## 变更记录（续）

### v1.1.3 — 2026-03-19 — 加入 Bug 修复后强制验证闭环

**根因**：AI 修复 Bug 后没有自动重测的闭合回路——修完代码就算完成，没有触发 verifier 子智能体验证修复是否有效。

**修改内容**：
- 新增：「Bug 修复后强制验证闭环」章节（紧接「强制集成测试时机」后）

**验证状态**：🔵 待验证

---

### v1.1.5 — 2026-03-19 — F-022全节点审核：加入后端代码生产挑战者反思（Step 4.5）

**根因**：full-node-audit.mdc 要求所有代码生产节点提交前内置挑战者反思，role-后端开发在集成测试后直接提交，缺少幂等性/错误恢复/成本失控的系统性检查。

**修改内容**：
- 新增：Step 4.5「F-022 全节点挑战者反思」——接口幂等性/错误恢复孤立脏数据/成本失控三视角

**验证状态**：🔵 待验证

### v1.3 → v1.4 — 2026-03-21 — Step 0.8 验证升级 + 新增 Step 1.5 DB Schema 核查门

**根因①（A类验证升级）**：Step 0.8 TDD Red 阶段在 2026-03-21 认知协作生态 Phase 1 twin-engine 开发中首次真实执行，18个测试文件正确处于红色失败状态，验证结果符合预期。

**根因②（B类步骤偏差）**：2026-03-21 twin-engine 后端代码全部写完后，才发现 aup 上的 DB Schema 与技术架构文档不一致（twin_logs vs twin_activities、notifications vs push_notifications 等3张表），形成 TC-NEW-01 P0 问题。根因是 Step 1 只读架构文档，缺少「验证目标服务器实际 Schema」的前置步骤。

**修改内容**：
- 修改：Step 0.8 变更记录 → 验证状态 🔵 → ✅
- 新增：Step 1.5「DB Schema 一致性核查门」（路径A：连接服务器验证；路径B：声明假设）
- 修改：原 Step 1.5（技术问题追踪台）→ 重编号为 Step 1.6

**验证结果**：
- 正向验证：下次触发 role-后端开发 且有 DB Schema 定义时，Step 1.5 应触发服务器 Schema 查询
- 负向验证：无 DB Schema 的纯 API 项目，Step 1.5 不触发（触发条件限制）

**验证状态**：🔵 待验证（下次执行时验证）

### v1.2 → v1.3 — 2026-03-20 — 新增 Step 0.3 会话冲突检查（防多会话覆写）

**根因**：TASK-23（会话1）先完整实现了 `platform_api.py`（13接口），TASK-24（会话2）不知情地用不同实现覆写了同文件，造成功能断路。两会话无任何互知机制，根本原因是「多会话并行修改同名文件时，没有任何前置检查」。

**修改内容**：
- 新增：Step 0.3「会话冲突检查」——激活后读取任务日志最近10条，检查24h内是否有其他会话修改过相关文件；有冲突则先 Read 了解改动内容，再声明增量修改而非覆写

**验证结果**：
- 正向验证：修改 platform_api.py 前，AI 应输出「上一个会话已做了XX改动，本次将继续」（待验证）
- 负向验证：全新项目无任务日志时，Step 0.3 无冲突，直接跳过，不阻碍正常流程

**验证状态**：🔵 待验证（需在下次触发 role-后端开发 时确认 Step 0.8 TDD Red 能正确建立）

### v1.1.4 — 2026-03-19 — P0 前置文档守门机制（SK-004 Gap 修复）

**根因**：SK-004 沙盘验证发现：激活后直接读 技术架构.md，若文件不存在只是跳过，不会阻断，使开发者可绕过关卡A/B直接开始写代码。

**修改内容**：
- 新增：Step 0「前置文档守门检查」——技术架构.md 或产品定义.md 缺失时立即停止并引导用户走正确流程，不生成任何代码

**验证结果**：
- 正向验证：无技术架构.md 时说「帮我写用户登录接口」→ 期望停止并引导
- 负向验证：有技术架构.md 时，原有 Step 1-5 不变

### v1.4 → v1.5 — 2026-03-20 — 新增 Step 0.2「API 集成变更门」（blocking gate）

**根因**：tashan-openbrain 开发中，nginx 将 `/api/auth/` 全部路由到 topiclab，绕过了 OpenBrain Python 的 workspace_id 附加逻辑，导致所有用户登录后 workspace_id 为 null，触发创作者激活弹窗。根本原因是改变路由时未检查下游消费方的字段期望（违反 L1.5 P17 下游优先检查原则）。

**修改内容**：
- 新增：Step 0.2「API 集成变更门」——在 Step 0（前置文档检查）之后、Step 0.3（会话冲突检查）之前
- 门禁条件：任何涉及路由/端点/返回字段/委托关系变更，必须先输出「API 契约检查表」（变更项 + 下游消费方 + 依赖字段 + 变更后是否满足），有❌必须解决后才继续
- 类型：blocking gate（不输出表格不得执行变更）
- 对应原则：L1.5 P17（下游优先检查）

**验证结果**：
- 正向验证：下次 API 路由变更前，AI 必须输出契约检查表，不得跳过（待真实场景验证）
- 负向验证：纯业务逻辑实现（无路由/端点变更）不触发此门

**验证状态**：🔵 待验证

### v1.5 → v1.6 — 2026-03-21 — 追加 BE-09 Tauri sidecar token 坑、BE-10 API camelCase/snake_case 契约坑

**根因①（BE-09）**：Tauri 桌面应用使用 sidecar 二进制，该二进制有自己独立生成的 token，与前端 .env 写死的开发 token 不匹配，导致 getWorkspaces() 失败，wsId 始终为 null，含 wsId 条件的弹窗渲染判断永远为 false，弹窗永远不显示。

**根因②（BE-10）**：server 端（Bun TypeScript）返回 camelCase 字段（questionDraft, canRevoke, createdAt），前端 TypeScript 类型定义使用 snake_case（question_draft, can_revoke, created_at），数据契约不一致，前端读到 undefined。verifier 独立测试才发现，说明集成测试需专门验证字段名。

**修改内容**：
- 新增：核心踩坑摘要表格追加 BE-09（Tauri sidecar token 不匹配导致弹窗失败）
- 新增：核心踩坑摘要表格追加 BE-10（API camelCase/snake_case 数据契约不一致）
- 新增：knowledge/后端踩坑速查.md 追加 BE-18 / BE-19 详细条目（知识文件已有 BE-09~17，故续编为 BE-18/19）

**验证结果**：
- 正向验证：Tauri 项目开发时，弹窗渲染应提供 wsId fallback，不硬依赖后端连接 → 待验证
- 正向验证：接口设计阶段技术架构文档明确 camelCase/snake_case 约定，集成测试验证字段名 → 待验证

**验证状态**：🔵 待验证

---

### 当前版本 → 下一版 — 2026-03-22 — 新增 Step 4.9「开发计划任务状态同步门」（文档-代码断链修复）

**根因**：2026-03-22 项目健康度检查发现：T-PD014-1/2/3 代码已实现，但开发计划.md 仍标 `[ ]` 未完成，整个 Phase 4 开发计划落后3天。根本原因是 Skill 有「读取开发计划」步骤（Step -1.B）但**没有「写回开发计划」步骤**——代码完成和文档同步完全断链。

**修改内容**：
- 新增：Step 4.9「开发计划任务状态同步门」（Step 4.5 挑战者反思之后、Step 5 提交测试之前）
- 内容：完成功能后，必须在开发计划.md 中找到并勾选对应任务；找不到则新建条目

**配套**：role-前端开发 SKILL 同步修改（Step 4.8 后添加 Step 4.9）

**验证状态**：🔵 待验证