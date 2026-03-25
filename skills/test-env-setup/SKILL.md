---
name: test-env-setup
description: 测试环境自动准备 Skill。在执行任何测试之前，自动检查并准备完整的测试环境：服务健康检查、自动启动后端、数据库就绪、测试账号创建、依赖验证。确保后续测试在稳定环境中执行。触发词：「准备测试环境」「环境预检」「初始化测试环境」「测试前准备」。也被 role-测试工程师 Step 0 和 fixer Step A0/B0 自动调用。
---

# 测试环境自动准备（test-env-setup）

> **使命**：让「说一句话就能开始测试」成为现实。
> 在测试智能体开始执行任何测试用例之前，自动完成所有环境准备工作。
> 若环境不可修复，输出明确的人工干预指引，不静默失败。

---

## 知识导航表

| 层级 | 文档 | 用途 |
|---|---|---|
| **D1 项目配置** | `项目群/[项目]/.cursor/test-config.md`（若存在）| 项目专属配置：端口/账号/技术栈 |
| **D2 技术架构** | `项目群/[项目]/2_技术架构/技术框架.md` | 了解服务架构和启动方式 |
| **D3 部署文档** | `项目群/[项目]/DEPLOY_ARCH.md` | 生产/测试账号信息 |

---

## 激活后立即执行

```
Step 0  【读取项目配置】
        先尝试读取 .cursor/test-config.md（项目专属配置）
        IF 不存在：使用智能推断（见后文「自动推断逻辑」）

Step 1  【后端服务健康检查 + 自动启动】

        1.1 检查服务是否在目标端口响应：
        ```bash
        curl -s --max-time 3 http://localhost:[PORT]/health 2>/dev/null
        ```
        
        IF 响应正常（含 "ok" 或 HTTP 200）：
          → 输出「✅ 后端服务正常（端口 [PORT]）」
          → 跳到 Step 2
        
        IF 无响应：
          1.2 检查是否有进程占用端口：
          ```bash
          lsof -i :[PORT] 2>/dev/null | head -5
          ```
          
          IF 有进程但未响应 → kill 并重启：
          ```bash
          pkill -f "uvicorn.*[PORT]" 2>/dev/null || true
          pkill -f "node.*[PORT]" 2>/dev/null || true
          sleep 2
          ```
          
          1.3 自动启动服务（根据技术栈）：
          
          FastAPI/Python 项目：
          ```bash
          cd [项目根目录]
          # 激活虚拟环境（优先 .venv，其次 venv，其次系统 Python）
          PYTHON=$([ -f .venv/bin/python ] && echo .venv/bin/python || \
                   [ -f venv/bin/python ] && echo venv/bin/python || \
                   echo python3)
          # 后台启动，日志写入 /tmp/test-backend.log
          nohup $PYTHON -m uvicorn backend.app.main:app \
            --host 0.0.0.0 --port [PORT] --workers 1 \
            > /tmp/test-backend.log 2>&1 &
          echo "启动PID: $!"
          ```
          
          Node.js/Next.js 项目：
          ```bash
          cd [项目根目录]
          nohup npm run dev > /tmp/test-frontend.log 2>&1 &
          ```
          
          1.4 等待服务就绪（最多 30 秒）：
          ```bash
          for i in $(seq 1 10); do
            sleep 3
            curl -s http://localhost:[PORT]/health && echo "✅ 服务就绪" && break
            echo "等待中... ($i/10)"
          done
          ```
          
          IF 30 秒后仍无响应：
          → 读取启动日志诊断：cat /tmp/test-backend.log | tail -20
          → 输出错误信息和诊断建议
          → 停止，输出：「❌ 后端服务无法自动启动，需要人工检查」
          → 附上日志内容供人工排查

Step 2  【数据库连接验证】
        ```bash
        # 通过服务健康端点间接验证 DB
        curl -s http://localhost:[PORT]/config-check 2>/dev/null | python3 -c "
        import sys, json
        d = json.load(sys.stdin)
        print('DB:', '✅' if d.get('db_configured') else '❌')
        " 2>/dev/null || echo "config-check 端点不可用（跳过DB验证）"
        ```
        
        IF DB 未连接（db_configured=false）：
          → 尝试启动数据库（如有 docker-compose）：
          ```bash
          docker-compose -f docker-compose.dev.yml up -d postgres 2>/dev/null || true
          sleep 5
          ```
          → 重新检查
          IF 仍然无法连接 → 输出「❌ 数据库连接失败，需要人工检查」

Step 3  【测试账号验证 + 自动创建（完整 Persona 体系）】
        
        需要创建以下 4 类测试人格账号（Personas）：
        
        ```python
        # 测试 Persona 定义（从 test-config.md 读取，以下为默认值）
        PERSONAS = [
            # admin：管理员，生成邀请码
            {"phone": "10000000001", "password": "admin2026",
             "role": "admin",    "handle": "test_admin", "display_name": "测试管理员"},
            
            # rich：丰富认知库，Proxy 测试目标 + Owner 模式测试
            {"phone": "19900000001", "password": "sim2026",
             "role": "creator",  "handle": "user_rich",  "display_name": "认知丰富用户",
             "seed_workspace": True,  # 需要预装知识库
             "visibility": "public_free"},  # 公开供 Proxy 测试
            
            # empty：空 workspace，冷启动/新用户测试
            {"phone": "19900000088", "password": "newuser2026",
             "role": "creator",  "handle": "user_empty", "display_name": "新用户"},
            
            # visitor：访客，专门用于 Proxy 对话 / 消息系统测试
            {"phone": "19900000099", "password": "visitor2026",
             "role": "user",     "handle": "user_visitor", "display_name": "访客测试者"},
        ]
        ```
        
        验证并创建缺失账号：
        ```python
        import requests, json
        
        BASE_URL = "http://localhost:[PORT]"
        
        def check_account(phone, password):
            r = requests.post(f"{BASE_URL}/auth/login", json={"phone": phone, "password": password})
            return r.status_code == 200, r.json() if r.status_code == 200 else None
        
        # 先确保 admin 账号存在（用 SQL 直接创建，绕过邀请码）
        admin_exists, _ = check_account("10000000001", "admin2026")
        IF not admin_exists:
            # 用终端执行 Python 脚本直接写 DB
            python -c "
            import sys; sys.path.insert(0, 'backend')
            from core.db import get_db
            from core.auth import create_user, hash_password, create_profile
            with get_db() as db:
                uid = create_user(db, '10000000001', hash_password('admin2026'))
                create_profile(db, uid, role='admin', display_name='测试管理员')
                print(f'Admin 创建成功: {uid}')
            "
        
        # 用 admin 账号生成邀请码并创建其他账号
        _, admin_data = check_account("10000000001", "admin2026")
        admin_token = admin_data["access_token"]
        
        r = requests.post(f"{BASE_URL}/admin/invite-codes",
                          headers={"Authorization": f"Bearer {admin_token}"},
                          params={"count": 10, "expire_days": 365})
        codes = r.json()["codes"]
        code_idx = 0
        
        for persona in PERSONAS[1:]:  # 跳过 admin
            exists, _ = check_account(persona["phone"], persona["password"])
            if not exists:
                r = requests.post(f"{BASE_URL}/auth/register", json={
                    "phone": persona["phone"],
                    "password": persona["password"],
                    "invite_code": codes[code_idx],
                    "display_name": persona["display_name"],
                    "handle": persona["handle"],
                })
                print(f"注册 {persona['handle']}: {r.status_code}")
                code_idx += 1

Step 3.5  【预装知识库（seed_workspace 标记的账号）】
        
        对标记了 seed_workspace=True 的账号（默认：user_rich），
        将预制知识库内容复制到其 workspace：
        
        ```bash
        # 检查 fixture 目录是否存在
        FIXTURE_DIR="tests/fixtures/rich_workspace"
        
        if [ ! -d "$FIXTURE_DIR" ]; then
            echo "⚠️ Fixture 目录不存在，正在从模板创建..."
            mkdir -p "$FIXTURE_DIR/sources"
            mkdir -p "$FIXTURE_DIR/docs/L1/产品理论维度"
            mkdir -p "$FIXTURE_DIR/docs/L2"
            
            # 创建已知内容的 fixture 文档（用于精确断言）
            cat > "$FIXTURE_DIR/sources/认知杠杆论.md" << 'EOF'
        # 认知杠杆论
        
        AI时代的核心竞争力是认知结构而非执行效率。
        知识管理的本质是建立连接，而非存储。
        个人认知结构的稀缺性，决定了它在AI时代的价值。
        EOF
            
            cat > "$FIXTURE_DIR/sources/研究方法论.md" << 'EOF'
        # 自下而上的系统性研究方法
        
        从具体案例出发，逐步归纳规律，最后升维到原则。
        避免一开始就构造大框架的陷阱。
        EOF
            
            echo "✅ Fixture 内容已创建"
        fi
        ```
        
        将 fixture 触发 build-cognition（让 AI 真正处理并建立认知结构）：
        
        ```python
        import requests, time
        
        # 登录 rich 账号
        _, rich_data = check_account("19900000001", "sim2026")
        rich_token = rich_data["access_token"]
        rich_ws = rich_data["workspace_id"]
        rich_headers = {"Authorization": f"Bearer {rich_token}"}
        
        # 检查是否已有认知内容（避免重复 seed）
        r = requests.get(f"{BASE_URL}/doc-registry", headers=rich_headers)
        existing_docs = r.json().get("docs", [])
        
        if len(existing_docs) < 3:  # 少于3个文档，说明需要 seed
            # 上传 fixture 文件
            import os
            from pathlib import Path
            
            fixture_files = list(Path("tests/fixtures/rich_workspace/sources").glob("*.md"))
            files = [("files", (f.name, open(f, "rb"), "text/markdown")) for f in fixture_files]
            
            r = requests.post(f"{BASE_URL}/twin/upload", headers=rich_headers, files=files)
            print(f"上传 fixture 文件: {r.status_code}, 文件数: {r.json().get('file_count')}")
            
            # 触发认知构建（通过 SSE 等待完成）
            print("⏳ 触发认知构建，等待完成（最多3分钟）...")
            with requests.post(f"{BASE_URL}/twin/build-cognition",
                               headers=rich_headers, stream=True, timeout=180) as r:
                for line in r.iter_lines():
                    if b'"done"' in line or b'build_done' in line:
                        print("✅ 认知构建完成")
                        break
        else:
            print(f"✅ rich 账号已有 {len(existing_docs)} 个文档，跳过 seed")
        
        # 设置 rich 账号的分身为公开（供 Proxy 测试）
        requests.post(f"{BASE_URL}/brain-square/visibility",
                      headers=rich_headers,
                      json={"visibility": "public_free"})
        print("✅ rich 账号设为公开（供 Proxy 测试）")
        ```

Step 4  【Python 依赖验证】
        ```bash
        cd [项目根目录]
        # 验证关键依赖是否安装
        $PYTHON -c "import requests, pytest, sseclient" 2>/dev/null && \
          echo "✅ Python 依赖齐全" || \
          (echo "⚠️ 安装缺失依赖..." && pip install requests pytest sseclient-py 2>&1 | tail -5)
        ```

Step 5  【最终就绪确认 + 输出报告】
        ```bash
        # 最终健康检查
        HEALTH=$(curl -s http://localhost:[PORT]/health 2>/dev/null)
        echo "服务状态: $HEALTH"
        
        # 验证两个测试账号均可登录
        TOKEN_MAIN=$(curl -s -X POST http://localhost:[PORT]/auth/login \
          -H "Content-Type: application/json" \
          -d '{"phone":"[TEST_PHONE_MAIN]","password":"[TEST_PASSWORD_MAIN]"}' \
          | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('access_token','FAIL')[:20])")
        
        echo "主账号 Token: $TOKEN_MAIN"
        ```
        
        输出就绪报告：
        「✅ 测试环境就绪
         
         服务状态：✅ localhost:[PORT]/health → ok
         数据库：✅ 已连接
         主测试账号（[TEST_PHONE_MAIN]）：✅ 可登录
         新用户账号（[TEST_PHONE_NEW]）：✅ 可登录
         Python 依赖：✅ 齐全
         
         准备就绪，可以开始测试。」
```

---

## 自动推断逻辑（无 test-config.md 时）

```
推断后端端口：
  grep -r "port.*810[0-9]\|:810[0-9]" [项目目录]/backend/ 2>/dev/null | head -3
  → 默认端口尝试顺序：8100 → 8000 → 3000

推断技术栈：
  IF exists requirements.txt AND exists backend/ → FastAPI/Python
  IF exists package.json AND exists pages/ → Next.js
  IF exists package.json AND exists src/ → React/Node

推断数据库：
  grep DATABASE_URL [项目目录]/.env 2>/dev/null
```

---

## 项目配置文件规范（.cursor/test-config.md）

```markdown
# 测试环境配置

## 服务
BACKEND_PORT: 8100
HEALTH_ENDPOINT: /health
STARTUP_CMD: python -m uvicorn backend.app.main:app --port 8100 --workers 1

## 测试账号
TEST_PHONE_MAIN: 19900000001
TEST_PASSWORD_MAIN: sim2026
TEST_PHONE_NEW: 19900000088
TEST_PASSWORD_NEW: newuser2026

## 技术栈
LANGUAGE: python
TEST_CMD: python -m pytest tests/ -x -v --timeout=120
VENV_PATH: .venv

## P2 处理
P2_HANDLING: skip   # skip / fix_all / ask
```

---

## 日志驱动断言工具（测试必用）

> 产品天然对 AI 透明：`/logs` 端点暴露所有工具调用、节点状态、SSE 事件。
> 用这些做断言，比「检查 AI 回答了什么文字」可靠 10 倍。

```python
import requests

BASE_URL = "http://localhost:[PORT]"

def get_session_logs(headers, session_id=None):
    """获取当前 session 的完整操作日志"""
    r = requests.get(f"{BASE_URL}/logs", headers=headers)
    logs = r.json() if r.status_code == 200 else []
    if session_id:
        logs = [l for l in logs if l.get("session_id") == session_id]
    return logs

def clear_logs(headers):
    """清空日志（每条 Layer 1 测试前调用，防止干扰）"""
    requests.delete(f"{BASE_URL}/logs", headers=headers)

def assert_tool_called(logs, tool_name, args_contains=None):
    """验证某个工具被调用（不管 AI 输出了什么）"""
    for log in logs:
        if log.get("tool") == tool_name or tool_name in str(log.get("action", "")):
            if args_contains is None:
                return True
            if args_contains in str(log.get("args", "")):
                return True
    return False

def assert_workflow_completed(events):
    """验证工作流完整执行完毕"""
    event_types = [e.get("type") for e in events if isinstance(e, dict)]
    return "workflow_done" in event_types

def assert_proposal_created(workspace_path):
    """验证工作流真的创建了 Proposal（文件系统状态断言）"""
    from pathlib import Path
    proposals = list(Path(workspace_path) / "proposals").glob("p-*.json"))
    return len(proposals) > 0

def assert_doc_modified(workspace_path, doc_pattern, after_timestamp):
    """验证某文档在测试操作后被修改"""
    from pathlib import Path
    import os
    for doc in Path(workspace_path).rglob(doc_pattern):
        if os.path.getmtime(doc) > after_timestamp:
            return True
    return False

def count_l2_fragments(workspace_path):
    """统计 L2 碎片数量（认知积累断言）"""
    from pathlib import Path
    return len(list((Path(workspace_path) / "docs/L2").glob("*.md")))
```

### 断言优先级

```
1. 文件系统状态（最可靠）：Proposal 出现了吗？L2 有新文件吗？
2. 日志工具调用：read_skill 被调用了吗？write_file 被调用了吗？
3. SSE 事件序列：workflow_done 在所有 node_update 之后吗？
4. 接口响应结构：返回了正确的字段吗？
5. 文字内容（最后手段）：仅在格式强制要求时（如第三人称检查）
```

---

## 失败处理（人工干预指引）

| 情况 | 自动尝试 | 无法自动处理时的指引 |
|------|---------|------------------|
| 后端服务无法启动 | kill+restart × 3 | 「查看 /tmp/test-backend.log，检查端口冲突或环境变量」 |
| 数据库无法连接 | 尝试 docker-compose up | 「检查 .env 的 DATABASE_URL，确认 PostgreSQL 在运行」 |
| 测试账号无法创建 | 尝试管理员 API 创建 | 输出手动创建 SQL |
| 依赖缺失 | pip install | 「运行 pip install -r requirements.txt」 |

---

## 变更记录

### v1.0 — 2026-03-24 — 初始创建

**根因**：Agent 拥有完整终端权限，但之前测试流程的「第一步」仍是人工确认环境就绪。
需要一个专门的 Skill 把环境准备工作完全自动化，让「说一句话就能开始测试」成为现实。

**设计决策**：
- 5步串行（健康检查→DB→账号→依赖→就绪确认）
- 每步有自动修复逻辑，修复3次失败才报告人工干预
- 支持 .cursor/test-config.md 项目配置，无配置时智能推断
- 输出就绪报告，让调用方知道环境状态

**验证状态**：🔵 待验证
