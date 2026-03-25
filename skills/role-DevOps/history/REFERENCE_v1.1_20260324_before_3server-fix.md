# DevOps 运营参考手册

> **文件类型**：D0-R（角色运营参考，K-object）
> **读取时机**：每次执行任何部署/运维任务时，Step 1 固定 Read 本文件
> **更新方式**：StrReplace 修改对应章节 + 变更记录追加一行（轻量，无需关卡）
> **不包含**：方法论原则（见 SKILL.md 的「第一性原理」节）/ 项目特定配置（见各项目 DEPLOY_ARCH.md）

---

## §1 服务器清单

| 服务器名 | IP / 域名 | 类型 | 用途 | 连接方式 |
|---------|----------|------|------|---------|
| **主服务器（aup）** | `101.200.234.115` | 阿里云 ECS 北京 | 所有他山产品的生产环境 | GitHub Actions SSH / 服务器助手 API |
| _(下一台服务器在此添加)_ | | | | |

### 连接方式说明

```bash
# 方式一：服务器助手 API（推荐，无需手动 SSH）
# 接口规范见：_内部总控/开发规范/AI调用服务器助手接口规范.md

# 方式二：GitHub Actions SSH（生产部署用）
# SSH 私钥：服务器上 cat ~/.ssh/github_actions

# 方式三：bore 隧道 SSH（本地调试用）
# bore 隧道占用关系：bore 一个端口只支持 1 条并发 TCP 连接
# AI 需要独立 bore 端口（与用户主连接分开），避免互相阻断
# 用法：bore local 2222 --to bore.pub（开独立 AI 连接端口）

# ⚠️ bore 限制：不支持 SSH subsystem 模式，scp/rsync 无法用
# 文件传输改用：tar czf - files/ | ssh ... "tar xzf -"
```

---

## §2 端口分配表

> 规则：新项目前端从 3xxx 分配，后端从 8xxx 分配，步进 +100

| 端口 | 项目 | 说明 |
|------|------|------|
| 3000 / 8000-8001 | Tashan-TopicLab | 论坛产品 |
| 3100 / 8100 | tashan-world | 世界产品 |
| 3101 / 8101-8102 | ai-org-builder | AI组织产品 |
| **下一个新项目** | 前端 3103+，后端 8103+ | ← 每次分配后更新此表 |

---

## §3 DNS 与域名

```
通配符证书/DNS：*.tashan.chat → 101.200.234.115
新子域名：无需配置 DNS，直接申请 SSL 证书即可

SSL 工具：acme.sh（已安装，~/.acme.sh/acme.sh）
申请命令：
  systemctl stop nginx
  ~/.acme.sh/acme.sh --issue --standalone -d [subdomain].tashan.chat
  systemctl start nginx
```

---

## §4 数据库

| 项目 | 值 |
|------|---|
| PostgreSQL RDS | `rm-cn-m1e4mlhns00027ro.rwlb.rds.aliyuncs.com:5432` |
| 凭据查看 | `cat /var/www/github-actions/repos/Tashan-TopicLab/.env \| grep DATABASE_URL` |
| JWT 密钥 | `97c24dcb8ccdd9691c795b3a1106781211caa1283f863140caac917d39029776` |
| 代码目录模式 | `/var/www/github-actions/repos/[项目名]/` |

> ⚠️ 注意：通过 pg_dump 导入数据后，SERIAL sequence 不会自动同步
> 修复命令：`SELECT setval('public.users_id_seq', (SELECT MAX(id) FROM public.users))`

---

## §5 GitHub 组织配置

```bash
# 官方仓库（推代码时确认 origin 指向这里）
GitHub 组织：TashanGKD
创建仓库：gh repo create TashanGKD/[name] --private

# GitHub Secrets（每个项目部署必须配置）
DEPLOY_HOST / DEPLOY_USER / DEPLOY_PORT / DEPLOY_PATH
SSH_PRIVATE_KEY / DEPLOY_TOKEN / DEPLOY_ENV

# ⚠️ 坑：推到 fork 仓库（Boyuan-Zheng/）不触发 Actions
# 检查：git remote -v 确认 origin 指向 TashanGKD/
```

---

## §6 服务器助手 API 快速参考

```python
# 接口调用模板（完整规范见 _内部总控/开发规范/AI调用服务器助手接口规范.md）
import httpx

def ask_server(message: str) -> str:
    r = httpx.post(
        "http://101.200.234.115:8000/api/v1/chat/stream",
        json={"message": message, "session_id": "devops-session"},
        headers={"Authorization": "Bearer [TOKEN]"},
        timeout=30
    )
    return r.text

# 常用命令
ask_server("docker ps --format '{{.Names}} {{.Status}}'")
ask_server("nginx -t")
ask_server("tail -n 50 /var/log/nginx/error.log")
```

> ⚠️ 服务器助手 API 不稳定（OPS-18）：长 session 后频繁超时。
> 优先用 `gh run view --log` 确认 Actions 状态，服务器助手仅作辅助。

---

## §7 踩坑速查（精选高频）

完整踩坑列表见：`.cursor/skills/role-DevOps/knowledge/部署踩坑速查.md`

以下是最高频的坑（每周都可能踩到的）：

| # | 症状 | 解决 |
|---|------|------|
| docker compose restart 无效 | restart 不重读 .env，新变量不生效 | `docker compose down && docker compose up -d` |
| nginx 修改不生效 | sites-enabled 里是真实文件（不是软链） | 直接编辑 sites-enabled 目录里的文件 |
| Python 3.9 `X\|Y` 类型报错 | 系统 Python 太旧 | `uv venv .venv --python 3.12` |
| bore SSH 连接立即断开 | bore 只支持 1 条并发连接，用户已占用 | 等用户断开，或开独立端口 bore local 2222 |
| push 不触发 Actions | 推到了个人 fork 仓库 | `git remote -v` 检查，确认 origin = TashanGKD/ |

---

## 变更记录（Append-Only）

| 日期 | 修改内容 |
|------|---------|
| 2026-03-24 | v1.0 初始创建，从 SKILL.md §「基础设施信息」和「已占用端口」章节提炼，补充连接方式说明 + 精选踩坑 |
| 2026-03-24 | 新增 §8 P0 应急授权（I9 立项，PP-002 交付物）|

---

## §8 P0 应急授权

> **适用场景**：生产发生 P0，用户告知 AI「有 P0 问题」，AI 立即切换 DevOps 角色响应
> **核心认知**：AI 没有不可达问题；P0 响应关键在「谁第一个发现并告知 AI」

### 8.1 AI 响应时机

以下情况立即切换 DevOps 角色处理：
- 用户说「生产有问题」「API 挂了」「容器崩了」等 P0 信号
- 用户分享错误截图或日志，显示服务不可用

**不需要等待**：AI 随时可用，收到告知立刻响应。

### 8.2 DevOps 角色的操作权限

| 操作 | 允许 | 说明 |
|------|------|------|
| `docker compose restart [service]` | ✅ | 重启单个服务 |
| `docker compose down && up -d` | ✅ | 完整重启所有服务（需用户确认，不可逆）|
| `systemctl reload nginx` | ✅ | 重载 nginx 配置 |
| `docker compose stop [非核心服务]` | ✅ | 临时降级（需用户确认）|
| 修改代码 / 配置文件 | ❌ | 超出 P0 紧急操作范围，走正常开发流程 |
| 删除数据 | ❌ | 永远不在紧急响应中做 |

### 8.3 标准响应流程

完整操作步骤见：`_内部总控/开发规范/P0应急手册.md §3`

响应后必须执行：
1. 在 `decision-log.md` 追加 P0 记录（见 P0应急手册.md §4 格式）
2. 若根因是系统性设计缺陷 → G 信号 → `PENDING-PROPOSALS.md` 追加

### 8.4 检测缺口（I9 ⚠️ 的剩余项）

当前：用户手动发现 → 告知 AI（Level 0）
目标：接入 UptimeRobot 等外部监控，自动告警（Level 1）
详见：P0应急手册.md §2
