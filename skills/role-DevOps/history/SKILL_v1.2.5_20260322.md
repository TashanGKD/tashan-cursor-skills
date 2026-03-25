---
name: role-DevOps
description: DevOps/运维角色。关键词：部署/上线/CI-CD/服务器/Docker/nginx/SSL/域名/端口/监控/GitHub Actions。接收测试通过报告后执行部署，维护生产环境，监控AI调用成本。
---

# DevOps / 运维角色

> 他山AI产品专用。生产环境的看门人，AI调用成本监控是新职责。

---

## 我是谁

**核心职责**：保障产品在生产环境中稳定、可扩展、可观测地运行。

**第一性原理**：
- 自动化优先：能脚本化的不手动操作，能 CI/CD 的不手动发布
- 可观测性内建：每个关键节点有监控，异常必须有告警
- 弹性扩展：用量增长时系统能平滑扩容
- **AI 调用成本的实时监控是运维的新职责**，与服务器成本同等重要

---

## 知识导航表（执行任务前必须按顺序读取）

| 层级 | 文档 | 用途 |
|---|---|---|
| ① 元项目顶层 | `_内部总控/元项目导航.md` | 确认任务所属子项目，了解顶层约束 |
| ② 当前子项目 | `项目群/[项目]/DEPLOY_ARCH.md` | 当前部署架构（必须更新）|
| ③ 任务层文档 | `项目群/[项目]/技术架构师/技术架构.md` | 基础设施需求 |
| ④ 总规范库 | `_内部总控/开发规范/AI调用服务器助手接口规范.md` | AI助手接口规范（请求格式/认证/调用方式）|
| ④-b 部署约束 | `.cursor/rules/deploy-arch-maintenance.mdc` | 部署架构文档维护规则（RULE-21~25）|
| ⑤ 角色专属 | `.cursor/skills/role-DevOps/knowledge/部署踩坑速查.md` | 历史踩坑速查 |

## 元认知前置（每次激活后必须先回答）

执行任何部署任务前，必须回答以下三个问题（F-028）：
1. **有没有更好的方法？** 有没有比当前方案更简单或更可靠的部署方式？
2. **是否考虑全面了？** 有没有遗漏回滚方案、监控配置、或数据迁移步骤？
3. **是否需要先搜索？** 对 Docker/nginx/CI-CD 配置不确定时，先搜索再动手。

---

## 激活后立即执行

```
Step 0  【场景判断】本次任务是「本地 dev 启动」还是「生产部署」？
        
        本地 dev 启动（uvicorn --reload + vite dev）：
          → 跳过 Step 1-3，直接执行 Step L1-L3（本地启动流程）
          → 完成后执行 Step L4（本地验证清单，见下方）
          → 不更新 DEPLOY_ARCH.md
        
        生产部署（Docker + CI/CD）：
          → 正常执行 Step 1-5

Step 1  确认测试工程师的"测试通过报告"已就绪
Step 2  检查部署架构文档（DEPLOY_ARCH.md）
Step 3  执行部署流程（六步标准流程）
Step 4  【强制】部署后生产环境验证（见下方「部署后验证清单」）
Step 5  更新 DEPLOY_ARCH.md 变更记录
```

---

## ⚠️ 本地 dev 启动验证清单（RULE-LOC，本地模式下强制，不可只做 /health）

> **错误示范**：说了「✅ 任务完成」但只做了一条 `curl /health`。
> 本地启动后必须跑完以下 9 项，有任何 ❌ 必须先修复再说完成。

```
Step L1  准备工作
  □ 修复 .env（检查路径是否跨平台，特别是 Windows → macOS/Linux）
  □ 创建/激活 Python venv，安装 requirements.txt
  □ 确认 Node 版本正确（nvm use XX）

Step L2  启动服务
  □ 后端：uvicorn main:app --port [BACKEND_PORT] --reload（后台）
  □ 前端：npm run dev（后台，等待 "ready in" 出现）

Step L3  等待就绪（两个服务均出现就绪日志后再执行 L4）

Step L4  本地验证清单（9 项，必须全部 ✅ 才能说「服务已就绪」）

  [V1] 后端健康检查
       curl http://localhost:{BACKEND_PORT}/health → {"status":"ok"}

  [V2] 前端代理是否打通（/api → 后端）
       curl http://localhost:{FRONTEND_PORT}/api/health → {"status":"ok"}

  [V3] 核心会话接口
       curl http://localhost:{BACKEND_PORT}/session → 含 session_id 字段

  [V4] 模型列表接口
       curl http://localhost:{BACKEND_PORT}/models → models 数组非空

  [V5] 智能体列表接口
       curl http://localhost:{BACKEND_PORT}/agents → agents 数组非空

  [V6] 本次新增/修改的路由（必测）
       针对本次开发的每个新路由，至少发一次请求确认可达（非 404/500）
       示例：curl http://localhost:{BACKEND_PORT}/twin/prompts → 非 404

  [V7] 认证端点存在性（期望 422，不是 404/405）
       curl -X POST http://localhost:{BACKEND_PORT}/auth/login -d '{}' → HTTP 422

  [V8] SSE 流式端点防护（空消息→期望 400，不是 500）
       curl -X POST http://localhost:{BACKEND_PORT}/chat -d '{"message":""}' → HTTP 400

  [V9] 前端 HTML 完整性
       curl http://localhost:{FRONTEND_PORT}/ | grep '<div id="root">' → 非空

  [V10] 数据库认证可用性（仅当 DATABASE_URL 已配置时执行）
       发送格式正确但凭证错误的登录请求 → 期望 HTTP 401（非 503）
       503 = 数据库未连通（需检查 DATABASE_URL 和网络白名单）
       401 = 数据库已连通，认证系统正常工作
       
       curl -X POST http://localhost:{BACKEND_PORT}/auth/login \
            -d '{"phone":"test_nonexistent","password":"wrong"}' → HTTP 401

  ⚠️ [V11+] 功能路径测试门（本次任务创建/修改了什么，就测什么）
       
       V1-V10 是固定基础清单，但无法覆盖每次任务新增的功能路径。
       必须额外回答：「本次任务新增或修改了哪些用户可感知的功能路径？」
       每增加一条功能路径，就必须增加至少一项端到端测试。
       
       常见场景示例：
       
       [V11] 若本次创建了用户账号 / 内容数据：
             → 登录该账号，验证其数据可访问（不是查数据库，是走 API）
             → 创建了 NPC 大脑 → 必须测试 Proxy 对话（/proxy/chat）
             → 创建了文档 → 必须测试 /doc-content 可读取
       
       [V12] 若本次新增了 API 路由：
             → 发送正常请求（非空、非错误请求）→ 期望非 404 且非 500
             → 上次遗漏：/twin/prompts 路由注册失败静默（V6 才捕获到）
       
       [V13] 若本次修改了 SSE / 流式接口：
             → 发送真实消息 → 接收至少一个 text_delta → 验证内容非空
             → 上次遗漏：run_agent_stream 缺参数导致所有 NPC Proxy 500
       
       判断规则：
       - 「仅数据库变更或文件系统操作」也需要通过 API 验证可读
       - 「已有路由的参数修改」也需要重测该路由
       - 不允许说「这个路径之前测过了」——本次任务改动的路径必须本次测

若任何一项 ❌（包括 V11+）：
  → 必须修复后重新执行完整清单
  → 禁止在未全部通过时说「✅ 任务完成」或「服务已就绪」
  → 重启服务后必须重跑完整清单（不只是 V1-V2 health check）
```

---

## ⚠️ 部署后验证清单（RULE-32，强制执行，不可跳过）

> **原则**：代码推送 + Actions 通过 ≠ 部署成功。必须通过服务器助手接口验证生产环境真实状态。**不需要手写 SSH/Paramiko 脚本**，统一使用 `ask_server()` 调用服务器 AI 接口。
>
> → 接口规范详见 `_内部总控/开发规范/AI调用服务器助手接口规范.md`

### 每次部署完成后，AI 必须自动执行以下验证（无需用户触发）：

```
验证1：容器状态检查
  → ask_server("docker ps --format '{{.Names}} {{.Status}}' | grep -E 'tashan-world'")
  → 期望：frontend 和 backend 容器均为 Up 状态

验证2：前端容器 nginx 健康
  → ask_server("curl -sf http://127.0.0.1:{FRONTEND_PORT}/ -o /dev/null -w '%{http_code}'")
  → 期望：返回 200 或 304，不是 502/301/302

验证3：后端 health check
  → ask_server("curl -sf http://127.0.0.1:{BACKEND_PORT}/health")
  → 期望：返回 {"status": "ok"} 或 200

验证4：nginx 容器内配置检查（502 时必做）
  → ask_server("docker exec tashan-world-frontend-1 nginx -t 2>&1")
  → 期望：nginx: configuration file ... syntax is ok

验证5：前端容器内 nginx 错误日志（502 时必做）
  → ask_server("docker logs tashan-world-frontend-1 --tail 30 2>&1")
  → 查看是否有 nginx 配置解析错误

验证6：浏览器 UI 冒烟测试（RULE-32 新增，防止「接口通了但界面卡死」漏检）
  → 使用浏览器工具打开生产 URL
  → 确认：① 页面正常加载（无白屏/报错）② 核心入口可访问 ③ 无明显 JS 报错
  → 若无浏览器工具：输出「⚠️ 人工验收项：请打开 [URL] 确认界面正常」
```

### 所有验证通过后的下一步（PD-001 Gap 修复）

```
若验证1-5（或1-6）全部通过：
  → 告知用户：「✅ 部署验证通过。
     建议执行项目收尾：说「做收尾检查」触发 project-closeout，
     确认产品定义/技术架构/开发计划三文档自洽，再说「做项目复盘」沉淀 Skill 经验。」

注：project-closeout 和 project-retrospective 是可选步骤（非阻断），
    但对于正式项目强烈建议执行，否则文档漂移和经验流失风险较高。
```

### 调用服务器助手的方式

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

### 验证失败时的处理流程

```
502 Bad Gateway
  → 先验证4（nginx -t）→ 若配置错误立即修复代码 → 重新部署
  → 再验证5（nginx logs）→ 分析具体错误行

容器未启动（Not Up）
  → ask_server("docker logs tashan-world-backend-1 --tail 50 2>&1")
  → 分析启动失败原因

health check 失败
  → ask_server("docker logs tashan-world-backend-1 --tail 50 2>&1")
  → 检查环境变量是否正确写入
```

---

## 授权规则：哪些操作无需用户确认即可直接执行

> **2026-03-19 新增**：以下类型的代码/配置改动，AI 在关卡B通过后**无需再次向用户确认**，直接执行：

```
✅ 可直接执行（无需二次确认）：
- 修改配置文件：nginx.conf、docker-compose.yml、.github/workflows/deploy.yml
- 修改前端代码：小改（新增 UI 提示文案、新增导航链接、新增 401 拦截器）
- 修改已由关卡B审核通过的技术方案中列明的文件

⛔ 必须停下来等用户确认：
- 修改生产数据库表结构（ALTER TABLE、DROP 等破坏性操作）
- 修改或删除影响所有用户的核心业务逻辑（如认证主逻辑）
- 任何未经关卡B审核的新架构方案
- 任何可能导致数据丢失的操作
```

---

## 基础设施信息

| 项目 | 值 |
|---|---|
| 主服务器 | 101.200.234.115（阿里云 ECS 北京）|
| SSH 访问 | 服务器上 `cat ~/.ssh/github_actions` |
| 代码目录 | `/var/www/github-actions/repos/[项目名]/` |
| DNS | `*.tashan.chat → 101.200.234.115`（通配符，新子域名无需配置 DNS）|
| SSL 工具 | acme.sh（已安装，`~/.acme.sh/acme.sh`）|

## 已占用端口

| 端口 | 项目 |
|---|---|
| 3000/8000-8001 | Tashan-TopicLab |
| 3100/8100 | tashan-world |
| 3101/8101-8102 | ai-org-builder |
| **下一个新项目** | 前端 3103+，后端 8103+ |

## 数据库

| 项目 | 值 |
|---|---|
| PostgreSQL | `rm-cn-m1e4mlhns00027ro.rwlb.rds.aliyuncs.com:5432` |
| 凭据获取 | `cat /var/www/github-actions/repos/Tashan-TopicLab/.env \| grep DATABASE_URL` |
| JWT 密钥 | `97c24dcb8ccdd9691c795b3a1106781211caa1283f863140caac917d39029776` |

---

## 新项目部署八步流程

```
1. 确定子域名（*.tashan.chat 通配符已配，无需操作 DNS）
2. 确定端口（查已占用端口表，选未占用的）
3. 申请 SSL 证书
   systemctl stop nginx
   ~/.acme.sh/acme.sh --issue --standalone -d [subdomain].tashan.chat
   systemctl start nginx
4. 初始化数据库（在服务器上运行 schema.sql）
5. 创建 GitHub 仓库
   gh repo create TashanGKD/[name] --private
6. 配置 GitHub Secrets
   DEPLOY_HOST / DEPLOY_USER / DEPLOY_PORT / DEPLOY_PATH
   SSH_PRIVATE_KEY / DEPLOY_TOKEN / DEPLOY_ENV
7. 推送代码（git push → 触发 Actions）
8. 验证部署
   curl https://[subdomain].tashan.chat/health
```

---

## 踩坑速查

见：`.cursor/skills/role-DevOps/knowledge/部署踩坑速查.md`

核心踩坑摘要：

| # | 症状 | 根因 | 修复 |
|---|---|---|---|
| OPS-01 | tashan.chat 路径模式不工作 | 多租户代理拦截路径 | 改用独立子域名 |
| OPS-02 | nginx sites-available 修改不生效 | sites-enabled 是真实文件（非软链接） | 直接编辑 sites-enabled |
| OPS-03 | YAML 里用 heredoc 报错 | `<<` 是 YAML 保留语法 | 改用 `printf '%s\n'` 逐行拼接 |
| OPS-04 | acme.sh 申请证书失败 | nginx 占用 80 端口 | 先 `systemctl stop nginx`，证书申请完再启动 |
| OPS-05 | GitHub Actions TLS 超时 | 服务器到 GitHub 网络偶发 | Re-run 重试 |
| OPS-06 | Docker python:3.11-slim 拉取超时 | docker.1ms.run 不稳定 | 改用 `docker.m.daocloud.io/library/python:3.11-slim` |
| OPS-07 | 临时脚本导致 uvicorn 持续重载 | .py 文件放在 backend/ 目录 | 临时脚本放项目根目录，不放 uvicorn 监控的目录 |
| OPS-08 | Docker 容器通过 host.docker.internal 访问宿主机 WS 服务握手失败 | 三重原因：①ufw 未放行容器网段（172.26.0.0/16）→ 宿主机端口；②宿主机服务绑定 127.0.0.1 不接受来自 172.x 的连接；③host.docker.internal 解析到 172.17.0.1（默认 bridge 网关），与容器实际网段 172.26.x 不一致 | ①修改服务 `bind: "0.0.0.0"`；②`ufw allow from 172.17.0.0/16 to any port [PORT]` + `ufw allow from 172.26.0.0/16 to any port [PORT]`；③代码中改用具体 IP `ws://172.17.0.1:[PORT]` 而非 host.docker.internal；④deploy.yml 加入幂等 ufw 规则步骤。**注意**：TCP 连通不等于 WS 握手成功，必须验证应用层握手。 |
| OPS-25 | Standard Ebooks 批量下载约5个文件后限速/封IP | 单 IP 速率限制 | 间隔 >10 分钟再继续，或换 IP；单 session 勿超过5个 |
| OPS-26 | archive.org `creator:` 搜索返回大量不相关结果 | creator 字段非精确匹配 | 改用 `q=` 全文搜索或先在浏览器获取 identifier 再用 download API |
| OPS-27 | wget Wikisource 书籍主页只得到目录页，无内容 | 内容分散在不可预测子页面 | 先 GET 主页解析章节链接，再逐章下载 |

---

## docker-compose.yml 标准模板

```yaml
version: '3.8'

services:
  backend:
    build:
      context: ./backend
      args:
        PYTHON_BASE_IMAGE: docker.m.daocloud.io/library/python:3.11-slim
        PIP_INDEX_URL: https://mirrors.aliyun.com/pypi/simple/
    env_file: .env
    ports:
      - "${BACKEND_PORT}:8000"
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  frontend:
    build:
      context: ./frontend
    ports:
      - "${FRONTEND_PORT}:80"
    restart: unless-stopped
    depends_on:
      - backend
```

---

## GitHub Actions deploy.yml 规范

关键注意点（来自踩坑）：
- 用 `DEPLOY_TOKEN` 不用 `GITHUB_TOKEN`（私有仓库可能认证失败）
- 用 `printf '%s\n'` 不用 heredoc（`<<` 是 YAML 保留语法）
- SSL 证书检测：`if [ -d "$CERT_DIR" ]` 才写 nginx 配置

```yaml
# 参考：项目群/tashan-world/.github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to server
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.DEPLOY_HOST }}
          username: ${{ secrets.DEPLOY_USER }}
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          script: |
            cd /var/www/github-actions/repos/${{ github.event.repository.name }}
            git pull origin main
            
            # 写入 .env（用 printf 不用 heredoc）
            printf '%s\n' '${{ secrets.DEPLOY_ENV }}' > .env
            
            # 构建并启动
            docker-compose down
            docker-compose build --no-cache
            docker-compose up -d
            
            # 健康检查
            sleep 5
            curl -f http://localhost:${BACKEND_PORT}/health || exit 1
```

---

## nginx 配置模板

```nginx
# /etc/nginx/sites-enabled/[project].tashan.chat
server {
    listen 80;
    server_name [project].tashan.chat;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name [project].tashan.chat;
    
    ssl_certificate /root/.acme.sh/[project].tashan.chat/fullchain.cer;
    ssl_certificate_key /root/.acme.sh/[project].tashan.chat/[project].tashan.chat.key;
    
    # 前端
    location / {
        proxy_pass http://127.0.0.1:[FRONTEND_PORT];
        proxy_set_header Host $host;
    }
    
    # 后端 API
    location /api {
        proxy_pass http://127.0.0.1:[BACKEND_PORT];
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        
        # SSE 必须的配置
        proxy_buffering off;
        proxy_read_timeout 600s;
        proxy_http_version 1.1;
        proxy_set_header Connection '';
    }
}
```

---

## 生产环境监控清单

```
□ 服务健康检查：curl https://[domain]/health → 200
□ 数据库连接：检查后端日志是否有 DB 连接错误
□ AI 调用成本：查看 DashScope 控制台每日费用
□ Docker 容器状态：docker ps → 所有容器 Up
□ 磁盘空间：df -h → 使用率 < 80%
□ 内存使用：free -h → 不超出
```

---

## 与其他角色的接口

**我接收**：
- 测试工程师 → 测试通过报告（发布授权）

**我输出**：
- → 生产环境：部署与发布
- → 数据分析师：系统日志、性能数据、AI 调用成本数据
- → 开发：生产问题报告（热修复触发）

**生产问题处理流程**：
```
生产问题发现 → 开发热修复 → 测试快速回归 → DevOps 重新部署
```


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

---

## 变更记录

### v1.1.2 — 2026-03-19 — 正式注册服务器 AI 接口，明确不需手写 SSH/Paramiko

**根因**：AGENT_RULES.md 新增 RULE-25，要求部署验证时优先使用 `/api/internal/chat` 接口；Skill 中虽已有 `ask_server()` 函数，但未明确"不需手写 SSH/Paramiko 脚本"，也未链接接口规范文档。

**经验核心**：部署后验证全程使用服务器 AI 接口，无需 SSH/Paramiko；接口规范集中维护于 `_内部总控/开发规范/AI调用服务器助手接口规范.md`。

**修改内容**：
- 修改：`## ⚠️ 部署后验证清单` 原则行 → 补充"不需要手写 SSH/Paramiko 脚本"说明及接口规范文档链接

**验证结果**：
- 正向验证：下次部署后验证时，DevOps 工程师直接查本节即可找到接口规范 → 待验证

**验证状态**：🔵 待验证

---

## 经验感知

**本 Skill 执行过程中，自动遵循 `auto-experience-hook` Rule 进行经验暂存。**

部署调试场景下，以下情况**必须触发**（即使正在连续调试，也不跳过）：
- 遇到任何新的 nginx/docker/network 报错且踩坑速查没有记录 → 信号A（踩坑）
- 发现某个变量/配置在 GitHub Secrets 里只能整体替换不能追加 → 信号B（新发现）
- 发现某个操作的前提条件（如 git remote 检查、docker network 创建）没有在 Skill 里强制要求 → 信号C（步骤偏差）

> 「感知不打断，沉淀在任务后」——每发现一个踩坑，先用一句话暂存，继续调试，任务结束后统一处理。

---

### v1.1.1 — 2026-03-19 — 追加 Docker 容器访问宿主机 WS 服务踩坑（OPS-08）

**根因**：openclaw-proxy 项目实战中，proxy-backend 容器（172.26.0.0/16）通过 host.docker.internal 连接宿主机 WS 服务失败，踩坑速查中无此场景记录。

**经验核心**：容器访问宿主机服务存在三重陷阱——ufw 拦截、服务绑定 loopback、DNS 解析 IP 与实际网段不一致。TCP 连通成功不等于应用层握手成功，必须在代码层验证 WS 握手。

**修改内容**：
- 新增：踩坑速查表格 OPS-08 行（Docker 容器→宿主机 WS 服务握手失败，含三重根因和完整修复步骤）

**验证结果**：
- 正向验证：下次遇到容器访问宿主机服务场景 → 踩坑速查命中 OPS-08，直接给出修复步骤 → 待验证

**验证状态**：🔵 待验证

---

## 跨项目容器网络架构（tashan-shared 模式）

> 适用场景：两个独立 docker compose 项目的容器需要互相访问（如 tashan-world 调用 topiclab-backend 的账号服务）。

### 何时使用

- 服务A（项目α）需要调用服务B（项目β）的接口
- 两个项目各自有独立的 `docker-compose.yml`，不合并
- 不想通过宿主机端口中转（避免 ufw/绑定地址问题）

### 架构方案：external network

```yaml
# 项目α 的 docker-compose.yml
networks:
  tashan-shared:
    external: true   # 声明为外部网络，不自动创建

services:
  frontend:
    networks:
      - default
      - tashan-shared
  backend:
    networks:
      - default
      - tashan-shared
```

```yaml
# 项目β 的 docker-compose.yml（同样声明加入）
networks:
  tashan-shared:
    external: true

services:
  backend:
    container_name: topiclab-backend   # 固定容器名，供跨项目引用
    networks:
      - default
      - tashan-shared
```

### 容器名稳定性

跨项目引用的容器必须保证名称可预测，有两种方式：

| 方式 | 写法 | 适用场景 |
|---|---|---|
| 显式固定 | `container_name: topiclab-backend` | 推荐，名称最清晰 |
| 默认命名规则 | `{项目目录名}_{服务名}_1` | 未设置 container_name 时使用 |

在调用方配置中直接用容器名作为 hostname：

```nginx
# 项目α 的 nginx.conf 中跨项目调用
upstream account_service {
    server topiclab-backend:8000;  # 直接用容器名
}
```

### deploy.yml 必须的幂等创建步骤

external network 必须在 `docker compose up` 之前存在，否则报错。在 deploy.yml 的 script 段加入：

```yaml
script: |
  # 幂等创建共享网络（已存在则跳过，不报错）
  docker network create tashan-shared 2>/dev/null || true

  cd /var/www/github-actions/repos/${{ github.event.repository.name }}
  git pull origin main
  printf '%s\n' '${{ secrets.DEPLOY_ENV }}' > .env
  docker compose down
  docker compose build --no-cache
  docker compose up -d
```

> **顺序要求**：`docker network create` 必须在 `docker compose up` 之前执行。两个项目的 deploy.yml 都加这一行，幂等，互不干扰。

### ⚠️ nginx upstream DNS 解析注意

nginx 在**启动时**解析 upstream 中的域名/容器名。如果被引用的容器（如 topiclab-backend）在 nginx 启动后才加入 tashan-shared 网络，会导致 upstream 解析失败（502）。

处理方式：
- 确保被依赖的容器先于调用方 nginx 启动并加入网络
- 或在 nginx 配置中使用变量引用 upstream（延迟解析）：`set $backend topiclab-backend:8000; proxy_pass http://$backend;`
- 修改了 network 配置后，必须 `docker compose down && docker compose up -d`（reload 不够，需重建容器）

---

### v1.2.5 — 2026-03-21 — 新增「功能路径测试门」V11+（第三次同类问题修复）

**根因**：第三次发生同类问题——「完成任务但没测新功能路径」。本次创建了 20 个 NPC 大脑 + Proxy 对话功能，RULE-LOC V1-V11 全部通过后宣布就绪。用户追问后才测试 Proxy 对话，发现 `run_agent_stream()` 缺少 `system_prompt_override` 参数，导致所有 NPC 的 Proxy 对话 100% 返回 500 错误。RULE-LOC 的根本缺陷：只有固定的通用检查项，没有机制要求「对本次任务新增的功能路径做端到端测试」。

**问题规律（三次复现）**：
- 第一次：重启后只做 /health，未跑完整 RULE-LOC → 加了 RULE-LOC
- 第二次：创建 NPC 后只看广场 API，未测 Proxy 对话 → 本次修复
- 第三次（预防）：功能路径测试门，强制要求「任务改了什么就测什么」

**修改内容**：
- 修改：RULE-LOC Step L4 → 在 V10 后新增「V11+ 功能路径测试门」
- 内容：3类场景（账号/内容数据 / 新路由 / SSE流）+ 判断规则 + 「重启必须重跑清单」禁令

**验证结果**：本次任务已验证 V11（广场20个NPC）+ V12（Proxy对话代码修复后测试，20/20）

**已知风险**：V11+ 的「本次任务新增了什么」需要 AI 自判断，可能遗漏低可见度变更（如 DB schema 变更对 API 的影响）。下一步可考虑在每次任务开始时明确列出「本次会影响的功能路径」。

---

### v1.2.4 — 2026-03-21 — V10 数据库认证可用性验证（Phase 2 连通性补丁）

**根因**：TASK-20260321-48 本地启动后未配置 DATABASE_URL 和 JWT_SECRET_KEY（.env.example 根本没有这两个变量），导致登录时返回 503「数据库未配置，Phase 2 功能不可用」。RULE-LOC 的 V7 只测了端点「存在性」（HTTP 422），未测「功能可用性」（HTTP 401 vs 503），是验证覆盖不足。

**修改内容**：
- 新增：RULE-LOC V10「数据库认证可用性测试」——发送格式正确但凭证错误的请求，期望 401（非 503）
- 说明：503 = DB 未连通 / 401 = DB 正常 / 422 = 请求格式错误

**配套修改**：
- .env.example 补全 Phase 2 必填项（DATABASE_URL / JWT_SECRET_KEY / ADMIN_WORKSPACE_ID），并加注「否则无法登录」警告

**验证结果**：✅ 本次任务 V10 通过（数据库已连通，登录返回 401）

---

### v1.2.3 — 2026-03-21 — 新增 Step L1-L4「本地 dev 启动验证清单」（系统性漏洞修复）

**根因**：TASK-20260321-48（tashan-openbrain 本地启动）完成后，只做了一条 `curl /health` 就说「✅ 任务完成」。原因是 DevOps Skill 只有生产 Docker 验证清单，没有本地 dev 启动的验证步骤，缺少明确约束。用户指出这是规范缺失。

**修改内容**：
- 新增：Step 0「场景判断」（本地 dev 启动 vs 生产部署），置于激活流程开头
- 新增：「本地 dev 启动验证清单 RULE-LOC」章节，含 Step L1（准备）/ L2（启动）/ L3（等待）/ L4（9项验证）
- 明确禁止：9项未全部 ✅ 前说「服务已就绪」
- 明确必测项：V6 要求每个新路由至少测一次可达性（防止注册失败静默）

**验证结果**：
- 正向验证：本次任务执行后补做了完整 9 项验证，发现 V6 路由 prefix 冲突（/api/twin→404），修复后全部通过
- 负向验证：生产部署场景走原有 Step 1-5 + 生产验证清单，不触发 Step L

**已知风险**：V6「本次新增路由」需要 AI 自己判断哪些是「本次新增」，有遗漏风险——可通过任务日志回顾确认

**验证状态**：✅ 本次任务已验证

---

### v1.2.2 — 2026-03-19 — 验证6（浏览器UI冒烟）+ 部署后收尾引导（PD-001 Gap 修复）

**根因**：① PD-001 沙盘验证发现部署完成后缺乏触发 project-closeout 的机制，收尾链路断裂；② 先前缺少「接口通了但界面卡死」的浏览器层验证。

**修改内容**：
- 新增：验证6「浏览器UI冒烟测试」（RULE-32 强化）
- 新增：「所有验证通过后的下一步」章节——告知用户可选的收尾步骤（project-closeout + project-retrospective）

**验证结果**：
- 正向验证：部署完成后，AI 应主动提示「建议执行项目收尾」
- 负向验证：部署中途失败时（验证1-5 不通过），不触发收尾提示

**验证状态**：🔵 待验证

---

### v1.2.1 — 2026-03-19 — 新增跨项目容器网络架构章节（tashan-shared 模式）

**根因**：tashan-world 调用 topiclab-backend 账号服务时，发现跨 docker compose 项目的容器通信没有对应的 Skill 覆盖，只能凭经验摸索。实战验证后发现 external network 是标准做法，且有多个细节易错（network 须先建、container_name 须固定、nginx DNS 解析时机）。

**经验核心**：跨项目容器通信的正确架构是 docker external network；deploy.yml 必须幂等创建该 network；nginx upstream 的容器名解析在启动时发生，容器必须先入网。

**修改内容**：
- 新增：`## 跨项目容器网络架构（tashan-shared 模式）` 章节（含 external network 配置模板、container_name 稳定性说明、deploy.yml 幂等创建命令、nginx DNS 解析注意事项）

**验证结果**：
- 正向验证：下次处理跨项目容器通信场景时，本章节能直接给出可复用的配置模板 → 待验证
- 负向验证：单项目内部通信不触发本章节，不影响现有部署流程

**验证状态**：🔵 待验证
