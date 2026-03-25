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

## 激活后立即执行

```
Step 1  确认测试工程师的"测试通过报告"已就绪
Step 2  检查部署架构文档（DEPLOY_ARCH.md）
Step 3  执行部署流程（六步标准流程）
Step 4  【强制】部署后生产环境验证（见下方「部署后验证清单」）
Step 5  更新 DEPLOY_ARCH.md 变更记录
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
