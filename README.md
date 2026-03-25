# 他山 Cursor Skill 体系

> **让 AI 在执行任务时能自主判断、按规范执行、并从经验中自我进化。**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/Skills-95-blue)](skills/)
[![Rules](https://img.shields.io/badge/Rules-32-green)](rules/)
[![Agents](https://img.shields.io/badge/SubAgents-18-purple)](agents/)

---

## 这是什么

这是[他山 AI](https://tashan.chat)在实际产品开发过程中积累的 **Cursor AI 执行规范体系**，包含：

- **95 个 Skills**：从「产品经理」到「DevOps」，覆盖产品开发全链路、认知积累、Bug修复、内容创作等完整工作流
- **32 个 Rules**：自动注入的质量守门规则，保证流程顺序、文档规范、代码质量
- **18 个 SubAgents**：独立视角的专项 Agent（审核者/修复者/评测者），实现真正的认知隔离验证

体系的核心目标：**AI 不只是执行命令的工具，而是一个有完整规范、会自我进化的智能执行系统。**

---

## 快速了解

### 说一句话，AI 自动走完整流程

```
你说：「做一个用户登录功能」
系统做：
  → 识别为「新功能」任务
  → role-产品经理：输出产品定义 + 功能状态表
  → role-审核者-用户模拟（关卡A）：用挑剔用户视角审查
  → role-技术架构师：设计技术方案
  → role-审核者-系统破坏（关卡B）：找安全漏洞和架构缺陷
  → role-后端开发 + role-前端开发：并行实现
  → role-测试工程师（关卡C）：验证功能 + 输出人工验收清单
  → role-DevOps：部署上线
```

### 踩坑自动沉淀，下次不再犯

```
执行中发现问题
  → Signal 机制自动捕捉（A:踩坑 / B:盲区 / C:缺口 / D:洞见 / ...）
  → PENDING-EXPERIENCES 队列暂存
  → project-retrospective 分析共性 → 更新 Skill/Rule
  → 下次遇到同类场景：自动规避
```

---

## 目录结构

```
tashan-cursor-skills/
├── README.md                    ← 你在这里
├── docs/
│   ├── overview.md             ← 完整说明文档（推荐先读）
│   ├── Skill体系设计原则_v1.0.md ← 设计哲学
│   └── SYSTEM-BLUEPRINT.md     ← 体系蓝图
├── skills/                      ← 95个 Skill
├── rules/                       ← 32个 Rule
├── agents/                      ← 18个 SubAgent
└── index/
    └── skill-index/
        └── SKILL-INDEX.md       ← 完整索引
```

---

## 核心 Skills 一览

### 产品开发链路

| Skill | 触发场景 | 作用 |
|-------|---------|------|
| `role-产品开发协调者` | 「新项目/做个功能/有个bug」| 识别任务类型，规划执行序列 |
| `role-产品经理` | 「产品设计/需求/用户流」| 输出产品定义 + 开发计划 |
| `role-技术架构师` | 「技术架构/系统设计」| 技术方案 + 接口规范 |
| `role-前端开发` | 「前端/React/TypeScript」| React + TS + Vite 实现 |
| `role-后端开发` | 「后端/FastAPI/API接口」| Python + FastAPI + PostgreSQL |
| `role-AI工程师` | 「LLM/Prompt/智能体」| Prompt 设计 + Agent 构建 |
| `role-测试工程师` | 「测试/验收/关卡C」| 功能验证 + 人工验收清单 |
| `role-DevOps` | 「部署/上线/服务器」| 发布 + 运维 |
| `role-审核者-用户模拟` | 「产品审核/关卡A」| 用户视角破坏性审查 |
| `role-审核者-系统破坏` | 「架构审核/关卡B」| 系统安全/性能破坏性审查 |

### 辅助工作流

| Skill | 触发场景 | 作用 |
|-------|---------|------|
| `bug-fix-loop-coordinator` | 「测试完成后」| Bug 修复闭环（dispatch fixer × N）|
| `issue-tracker` | 「发现问题时」| 问题分类 → 两个追踪台 |
| `project-backlog` | 「收到外部反馈」| 统一 Inbox，积累后批量处理 |
| `expert-bootstrap` | 「需要某领域专家」| 调研→自问自答→产出专家 Agent |
| `project-retrospective` | 「项目完成后」| 批量复盘，沉淀 Skill 体系 |

### 认知积累

| Skill | 触发场景 | 作用 |
|-------|---------|------|
| `cognitive-capture-fragment` | 「记录想法/有洞见」| 捕捉 L2 碎片 |
| `cognitive-integrate-fragments` | 「整合碎片」| 升华进 L1 系统文档 |
| `cognitive-extract-principle` | 「提炼原则」| 识别跨领域模式 → L1.5 原则库 |

---

## 核心 Rules 一览

```
session-bootstrap.mdc        ← 每次对话的执行协议（序列A+B）
role-menu.mdc               ← 所有角色的触发词路由表
comprehensive-change-guard  ← 多层变更强制按序执行
bug-fix-tdd-guard           ← Bug修复强制 TDD 流程
test-coverage-guard         ← 测试完成对账主测试文档
document-lifecycle-guard    ← 自建领地 + 文档版本管理
product-alignment-guard     ← 修复必须符合产品意图
frontend-brand-guard        ← 品牌规范强制守门
```

---

## 快速安装

### 方式一：直接复制

```bash
git clone https://github.com/TashanGKD/tashan-cursor-skills.git

# 复制到你的项目
cp -r tashan-cursor-skills/skills/* your-project/.cursor/skills/
cp -r tashan-cursor-skills/rules/* your-project/.cursor/rules/
cp -r tashan-cursor-skills/agents/* your-project/.cursor/agents/
```

重启 Cursor，所有 Skill 和 Rule 自动生效。

### 方式二：选择性使用

只复制你需要的 Skill：

```bash
# 例：只使用产品开发角色
cp -r tashan-cursor-skills/skills/role-产品经理 your-project/.cursor/skills/
cp -r tashan-cursor-skills/skills/role-技术架构师 your-project/.cursor/skills/
# ... 等

# 必须同时复制核心 Rules（否则路由不生效）
cp tashan-cursor-skills/rules/role-menu.mdc your-project/.cursor/rules/
cp tashan-cursor-skills/rules/session-bootstrap.mdc your-project/.cursor/rules/
```

---

## 修改和贡献

新建或修改 Skill/Rule/Agent 前，必须先阅读：
1. [设计原则](docs/Skill体系设计原则_v1.0.md)：什么场景用 Skill vs Rule vs Agent
2. [skill-rule-修改规范](skills/skill-rule-修改规范/SKILL.md)：三问协议 + 版本留痕

欢迎 PR，每个变更需要：
- 说明根因（为什么需要这个改动）
- 说明影响范围
- 说明验证方法

---

## 设计理念

> 「Skill 体系的设计质量，由它能否自我进化来衡量。」— Skill体系设计原则 §一

这套体系不是工具集合，而是 AI 的行为规范结构。评判标准不是「有多少 Skill」，而是「AI 能否从执行中学习并自动更新规范」。

详细设计理念见 [docs/overview.md](docs/overview.md)。

---

## 关于他山

他山 AI 是一个「AI + 认知协作」产品，致力于让用户的认知可以外化、传播、进化。
- 产品：[tashan.chat](https://tashan.chat)
- GitHub：[TashanGKD](https://github.com/TashanGKD)

---

## License

MIT License — 自由使用，保留署名即可。
