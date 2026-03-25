---
name: tashan-workbench-dev
description: 他山工作台（tashan-workbench）开发专属 Skill。接手/开发/调试工作台时激活：启动命令、架构速查、历史踩坑、测试方法。触发词：「他山工作台」「openwork-local」「tashan-workbench 开发」「工作台怎么启动」「接手工作台」「工作台调试」。
---

# 他山工作台 · 开发 Skill

> 他山工作台（tashan-workbench）是基于 OpenWork fork 的本地 AI 桌面应用，内嵌 opencode 执行引擎，搭载 Tashan Cognitive Pack 认知内核。
> 代码位置：`项目群/tashan-workbench/`

---

## 激活后立即执行

```
Step 1  Read: 项目群/openwork-local/产品经理/产品定义.md（v0.7）→ 了解产品边界
Step 2  Read: 项目群/openwork-local/技术架构师/技术架构_v0.2_正式版.md → 架构契约
Step 3  Read: 项目群/tashan-workbench/DEPLOY_ARCH.md → 部署状态和端口信息
Step 4  本次任务的具体需求 → 按「五类测试维度」执行
```

---

## 核心架构速查

```
tashan-workbench/（monorepo）
├── packages/app/          ← 前端（React 18 + Tailwind + Noto Serif SC）
│   └── src/
│       ├── App.tsx        ← 三栏布局（左:对话 / 中:预览 / 右:搜索+记忆）
│       ├── api/client.ts  ← openwork-server API 封装（含4优先级 token 解析）
│       └── types/         ← 共享类型
│
├── packages/server/       ← openwork-server（Bun TypeScript，端口 4897）
│   └── src/
│       ├── server.ts      ← 所有 API 路由（含 /brain/* /workspace/:id/search）
│       ├── workspace-search.ts  ← BM25 全文检索（16单测）
│       └── brain-bridge.ts     ← 他山Brain HTTP 封装（17单测）
│
├── packages/tashan-mcp/   ← tashan-mcp MCP 服务器（stdio）
│   └── src/
│       ├── server.ts      ← brain_ask / spawn_task / list_tasks / cancel_task
│       ├── task-manager.ts ← 子任务生命周期（支持 SQLite 持久化）
│       └── task-store.ts  ← SQLite 持久化层（7单测）
│
├── packages/desktop/      ← Tauri 桌面应用壳层（Rust）
│   └── src-tauri/
│       └── sidecars/      ← 预编译 opencode/openwork-server/mcp 二进制
│
├── opencode.json          ← AI 模型配置（DashScope + tashan-mcp 注册）
└── .opencode/skills/      ← Tashan Cognitive Pack（系统提示词注入）
    ├── tashan-cognitive-pack/SKILL.md  ← 认知工作流
    └── tashan-brand-guard/SKILL.md     ← 前端品牌规范
```

---

## 本地开发启动（推荐：不打包直接验证）

```bash
# 终端1：启动 AI 执行引擎（opencode）
# （通常已在后台，检查：lsof -i:4900）

# 终端2：启动 openwork-server
export PATH="$HOME/.bun/bin:$PATH"
cd 项目群/tashan-workbench/packages/server
bun src/cli.ts \
  --workspace ~/aiwork/0310_huaxiang/项目群/tashan-workbench \
  --opencode-base-url http://127.0.0.1:4900 \
  --port 4897
# ⚠️ 记录输出的 Client token，每次重启都会变

# 终端3：更新前端 token 并启动 Vite
TOKEN="从终端2复制"
echo "VITE_OPENWORK_URL=http://127.0.0.1:4897
VITE_OPENWORK_TOKEN=$TOKEN" > packages/app/.env
cd packages/app && pnpm exec vite --port 5200

# 浏览器打开 http://localhost:5200
```

**完整 Tauri 桌面模式**（用于最终验收/打包）：
```bash
cd packages/desktop
env -u CI pnpm tauri dev
```

---

## 快速健康检查

```bash
# 服务状态
curl http://127.0.0.1:4897/health

# 工作区
TOKEN="xxx"
curl http://127.0.0.1:4897/workspaces -H "Authorization: Bearer $TOKEN"

# BM25 搜索
curl "http://127.0.0.1:4897/workspace/ws_e5fb359b2060/search?q=产品定义&limit=3" \
  -H "Authorization: Bearer $TOKEN"

# 全部单测
cd packages/server && bun test src/
cd packages/tashan-mcp && bun test src/
```

---

## 已实现功能清单（Phase A~E + 遗留修复）

| 功能 | 关键文件 | 单测 |
|---|---|---|
| LLM 对话（DashScope qwen3.5-plus）| opencode session API | — |
| BM25 工作区文件搜索 | `workspace-search.ts` | 16✅ |
| 子智能体编排（spawn/list/cancel）| `task-manager.ts` + `task-store.ts` | 16✅ |
| 分身代理提问（brain_ask）| `brain-bridge.ts` + `server.ts` | 17✅ |
| Tashan Cognitive Pack | `.opencode/skills/` | API✅ |
| token 持久化（4优先级）| `api/client.ts` | — |
| TaskManager SQLite 持久化 | `task-store.ts` | 7✅ |
| spawn_task 并发上限（默认5）| `task-manager.ts` | — |

---

## 历史踩坑速查（必读）

### W-01 点击发送按钮无反应
**症状**：输入文字后点「↑」按钮，页面无反应。
**根因**：`wsId` 为 null，`handleSend` 第一行静默 return。
**原因**：`getWorkspaces()` 用旧 token 返回 401 → 初始化失败 → wsId=null。
**修复**：每次重启 server 后更新 `.env` 的 `VITE_OPENWORK_TOKEN`。若已修复但仍无反应，检查浏览器 DevTools Console。

### W-02 BrainConfirmModal 一直弹出
**症状**：「以你的名义向专家分身提问」弹窗不停出现。
**根因**：`brain_ask_requests` 表里有 `pending_confirm` 状态的测试数据，前端每 5 秒轮询一次就触发弹窗。
**修复**：清除测试数据：
```bash
bun -e "
const {Database}=require('bun:sqlite');
const {homedir}=require('os');
const {join}=require('path');
const db=new Database(join(homedir(),'.tashan-workbench','brain.db'));
db.run(\"DELETE FROM brain_ask_requests WHERE question_draft LIKE '%test%'\");
db.run('DELETE FROM brain_rate_limit');
db.close();
"
```

### W-03 Tauri sidecar token 与 dev server token 不匹配
**症状**：`pnpm tauri dev` 启动后 wsId=null，页面无法使用。
**根因**：Tauri sidecar 有自己的 token 管理，与手动启动的 dev server token 不同。
**修复**：浏览器直接访问 `http://localhost:5200`（不走 Tauri 窗口），或在 Tauri 窗口中按 `Cmd+Option+I` 打开 DevTools 查看实际 token。

### W-04 openclaw 插件 SDK 与 openwork-server 不兼容
**症状**：想接入 openclaw memory-core / subagents，发现无法注册。
**根因**：openclaw 使用 `openclaw/plugin-sdk`，openwork-server 使用 opencode 生态，两套体系完全不兼容。
**修复**：自建等效功能（BM25 搜索、tashan-mcp MCP 工具），见 opencode-plugin-compatibility Rule。

### W-05 BM25 单字 CJK 误触发
**症状**：搜索明显不相关的词，也返回结果。
**根因**：CJK 单字（"在"、"的"）太常见，bigram 化不够时会误触发。
**修复**：分词器已修复为「只产出 bigram，不产出单字」（workspace-search.ts）。

### W-06 pnpm tauri build bundle_dmg.sh 失败
**症状**：`pnpm tauri build` 编译成功但报 `bundle_dmg.sh` 错误，无 .dmg 产出。
**根因**：Tauri 0.11.169 在 macOS 26（Darwin 25.3.0）上 bundle_dmg.sh 调用参数缺失。
**修复**：手动用 `hdiutil create` 打包：
```bash
hdiutil create -volname "他山工作台" \
  -srcfolder target/release/bundle/macos/他山工作台.app \
  -ov -format UDZO \
  target/release/bundle/dmg/他山工作台_0.11.169_aarch64.dmg
```

### W-07 API 命名风格数据契约不一致
**症状**：前端读到 `undefined` 字段。
**根因**：server 返回 camelCase（`questionDraft`），前端类型定义 snake_case（`question_draft`）。
**修复**：统一约定所有 API 使用 camelCase，types/index.ts 已修复。

---

## 关键配置文件

| 文件 | 用途 |
|---|---|
| `opencode.json` | LLM 模型 + tashan-mcp 注册；修改后需重启 openwork-server |
| `packages/app/.env` | 前端 token 配置；每次重启 server 后更新 `VITE_OPENWORK_TOKEN` |
| `~/.tashan-workbench/brain.db` | brain_ask 请求状态（SQLite）|
| `~/.tashan-workbench/task-manager.db` | spawn_task 任务状态（SQLite）|
| `~/.config/openwork/tokens.json` | openwork-server token 持久化 |

---

## 前端品牌规范速查

- **字体**：`font-serif`（Noto Serif SC），禁止 Inter/Roboto/Arial
- **主色**：`bg-black text-white`（按钮），`text-gray-600/700`（内容）
- **圆角**：`rounded-lg`（卡片/按钮），`rounded-xl`（模态框），`rounded-full`（头像）
- **禁止**：渐变背景、紫色配色、CSS-in-JS

---

## 产品边界（Phase A~E 已实现）

详见：`项目群/openwork-local/产品经理/产品定义.md`（v0.7）

未实现（待后续迭代）：
- E2：分享任务结果到他山Brain（需他山Brain发帖API）
- E3：多人协作工作台（工程量大）
- brain_ask 真实分身对话（需设置 `BRAIN_JWT_DEV`）

---

## 变更记录

### v1.0 — 2026-03-21 — 初始创建

**触发事件**：tashan-workbench Phase A~E 完整开发完成，project-closeout 通过，用户要求沉淀开发经验为 Skill。

**经验核心**：
1. opencode/openclaw 两套生态不兼容，必须先验证 plugin SDK 再设计方案
2. Tauri sidecar token 与 dev server token 不同，浏览器直接访问是更好的迭代方式
3. BM25 + CJK bigram 分词是纯本地工作区搜索的有效方案
4. brain_ask 的 SOUL.md 人格化：必须用结构化字段提取，防 Prompt Injection

**验证状态**：✅ 已验证（本次完整项目开发实测）
