<!-- Logo -->
<p align="center">
  <a href="https://tashan.ac.cn" target="_blank" rel="noopener noreferrer">
    <img src="docs/assets/tashan.svg" alt="他山 Logo" width="280" />
  </a>
</p>

<!-- 标题 -->
<p align="center">
  <strong>他山 Cursor Skill 体系</strong><br>
  <em>Tashan Cursor Skill System — Self-Evolving AI Execution Framework</em>
</p>

<!-- 快速导航 -->
<p align="center">
  <a href="#项目简介">项目简介</a> •
  <a href="#功能特性">功能特性</a> •
  <a href="#快速开始">快速开始</a> •
  <a href="#代码结构">代码结构</a> •
  <a href="#生态位置">生态位置</a> •
  <a href="#贡献">贡献</a> •
  <a href="README.en.md">English</a>
</p>

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Skills](https://img.shields.io/badge/Skills-95-blue)](#功能特性)
[![Rules](https://img.shields.io/badge/Rules-32-green)](#功能特性)
[![Agents](https://img.shields.io/badge/SubAgents-18-purple)](#功能特性)

> 围绕「AI 自我进化」构建的 Cursor 执行规范体系：95 个 Skills、32 个 Rules、18 个 SubAgents，让 AI 在执行任务时能自主判断、按规范执行、并从经验中自我进化。

---

## 项目简介

「人—智能体混合数字世界」研究的核心主张之一，是让 AI Agent 不只是工具，而是具备完整规范、能自我进化的智能执行系统。本项目对应其中的**能力层（Skill 体系）**，负责解决 AI 在实际产品开发中「每次从零开始、犯过的错还会再犯、用户需要手动指定所有流程」这三个根本问题。

没有本项目，AI 每次对话都凭训练知识随意发挥，无规范、无沉淀、无进化；有了本项目，AI 拥有成体系的「做事方式」，能自主识别任务类型、走完整流程、把踩坑自动转化为规范更新。

**核心思想**

- **系统自我进化**：执行中自动捕捉踩坑信号（A-G 类），归纳共因，更新 Skill/Rule，下次自动规避
- **三层能力架构**：Rules（约束守门）→ Skills（步骤序列）→ SubAgents（独立视角验证），三层分工明确
- **通用质量闭环**：创建→独立验证（clean context）→响应→二次审核→关闭，适用于所有质量保障场景

**适合以下场景与读者**

- 使用 Cursor AI 进行产品开发的独立开发者和团队，希望建立标准化开发流程
- AI 工程师，研究如何让 AI Agent 具备自我进化能力
- 产品经理/技术负责人，希望用 AI 覆盖设计→架构→开发→测试→上线全链路
- 研究 Cursor Skill 体系设计原则的开发者

---

## 功能特性

**产品开发全链路自动化**
- **自动识别任务类型**：说出需求，AI 自主判断是「新功能 / Bug / 配置变更」，规划执行序列
- **完整关卡体系**：关卡 A（产品规格审核）→ 关卡 B（技术架构审核）→ 关卡 C（功能验证），每关独立视角，不可绕过
- **Bug 修复闭环**：发现 → TDD 修复（先写失败测试）→ 回归验证 → 追踪台更新，全程有记录

**自我进化机制**
- **Signal A-G 自动捕捉**：6类信号（踩坑/盲区/缺口/洞见/效果不符/意外行为/根因）在任务完成后自动路由
- **模式识别**：多次相似信号触发 project-retrospective，批量更新 Skill/Rule，解决根因而非逐条修补
- **三问变更协议**：修改任何 Skill/Rule/Agent 前必须回答根因/影响/验证，保证变更可追溯

**文档管理自动化**
- **自建领地**：每个项目角色激活时自动创建/维护标准文档结构（产品定义/技术架构/追踪台等）
- **版本留痕**：修改项目文档前自动备份旧版，追加变更记录
- **路径适配**：通过 project-config.md 解析文档路径，适配不同项目目录结构

**认知积累与沉淀**
- **L2 碎片捕捉**：工作中的洞见自动记录为认知碎片
- **知识升华**：碎片积累后整合进 L1 系统性文档，跨项目可复用
- **原则提炼**：发现跨领域模式时，提炼为底层原则供所有任务参考

---

## 安装方式

### 方式一：`ai-agent-skills` CLI（推荐，一行命令）

```bash
# 安装到当前项目
npx ai-agent-skills install TashanGKD/tashan-cursor-skills

# 或安装到全局（所有项目可用）
npx ai-agent-skills install --global TashanGKD/tashan-cursor-skills
```

重启 Cursor，Skills 自动生效。

### 方式二：Cursor 内置 GitHub 导入

1. 打开 Cursor 设置（`Cmd+Shift+J`）
2. 进入 **Rules** → **Add Rule** → **Remote Rule (Github)**
3. 输入仓库地址：`https://github.com/TashanGKD/tashan-cursor-skills`
4. 重启 Cursor

### 方式三：手动复制（完全控制）

```bash
git clone https://github.com/TashanGKD/tashan-cursor-skills.git

# 全量安装
cp -r tashan-cursor-skills/skills/* your-project/.cursor/skills/
cp -r tashan-cursor-skills/rules/* your-project/.cursor/rules/
cp -r tashan-cursor-skills/agents/* your-project/.cursor/agents/
```

---

## 快速开始

### 1. 安装（选择上面任意一种方式）

### 2. 重启 Cursor

关闭并重新打开 Cursor，所有 Skill 和 Rule 自动生效。

### 3. 创建项目配置文件（推荐）

在你的项目根目录创建 `.cursor/project-config.md`，帮助 AI 定位文档路径：

```markdown
# 项目配置

## 项目基本信息
项目名称：[你的项目名]
项目路径：[项目根目录路径]

## 核心文档路径
产品文档目录：[项目]/产品经理/
技术架构目录：[项目]/技术架构师/
测试文档目录：[项目]/3_开发计划/
```

### 5. 开始使用

直接描述你的需求，AI 会自动识别任务类型并执行：

```
「做一个用户登录功能」
→ AI 自动：产品设计 → 关卡A审核 → 技术架构 → 关卡B审核 → 开发 → 测试 → 上线

「登录接口报 500 错误」
→ AI 自动：issue 分类 → TDD 修复 → 回归验证 → 追踪台更新
```

### 选择性使用

只需要部分 Skill 时，至少复制核心 Rules（否则路由不生效）：

```bash
# 复制核心路由 Rules（必须）
cp tashan-cursor-skills/rules/role-menu.mdc your-project/.cursor/rules/
cp tashan-cursor-skills/rules/session-bootstrap.mdc your-project/.cursor/rules/

# 复制你需要的 Skill
cp -r tashan-cursor-skills/skills/role-产品经理 your-project/.cursor/skills/
cp -r tashan-cursor-skills/skills/role-技术架构师 your-project/.cursor/skills/
# ... 其他需要的 Skill
```

---

## 代码结构

```
tashan-cursor-skills/
├── README.md                    # 中文说明（本文件）
├── README.en.md                 # 英文说明
├── CHANGELOG.md                 # 版本变更记录
├── CONTRIBUTING.md              # 贡献指南
├── LICENSE                      # MIT 许可证
├── docs/
│   ├── assets/
│   │   └── tashan.svg           # 他山 Logo
│   ├── overview.md              # 完整系统说明文档
│   ├── Skill体系设计原则_v1.0.md # 设计哲学原文
│   └── SYSTEM-BLUEPRINT.md     # 体系蓝图（来自历史对话分析）
├── skills/                      # 95 个 Skill（每个含 SKILL.md）
│   ├── role-产品开发协调者/     # 域协调者：识别任务类型，规划执行序列
│   ├── role-产品经理/           # 产品定义 + 开发计划
│   ├── role-技术架构师/         # 技术方案 + 接口规范
│   ├── role-前端开发/           # React + TS + Vite 实现
│   ├── role-后端开发/           # Python + FastAPI + PostgreSQL
│   ├── role-AI工程师/           # Prompt 设计 + Agent 构建
│   ├── role-测试工程师/         # 关卡 C：全量验证
│   ├── role-DevOps/             # 部署 + 运维
│   ├── role-审核者-用户模拟/    # 关卡 A：产品规格审核
│   ├── role-审核者-系统破坏/    # 关卡 B：架构安全审核
│   ├── bug-fix-loop-coordinator/ # Bug 修复闭环
│   ├── issue-tracker/           # 问题分类追踪
│   ├── project-backlog/         # 外部反馈统一 Inbox
│   ├── expert-bootstrap/        # 按需培养领域专家 Agent
│   ├── project-retrospective/   # 项目复盘 + Skill 进化
│   ├── cognitive-*/             # 认知积累系列（碎片/整合/原则提炼等）
│   ├── skill-index/             # 体系索引（SKILL-INDEX.md 等）
│   └── ...（完整清单见 index/skill-index/SKILL-INDEX.md）
├── rules/                       # 32 个 Rule（.mdc 文件，alwaysApply）
│   ├── session-bootstrap.mdc    # ★ 核心：每次对话的执行协议（序列A+B）
│   ├── role-menu.mdc            # ★ 核心：所有角色的触发词路由表
│   ├── comprehensive-change-guard.mdc  # 多层变更强制按序执行
│   ├── bug-fix-tdd-guard.mdc   # Bug 修复强制 TDD
│   ├── test-coverage-guard.mdc # 测试完成对账主文档
│   ├── document-lifecycle-guard.mdc    # 文档版本管理
│   ├── product-alignment-guard.mdc     # 修复必须符合产品意图
│   ├── frontend-brand-guard.mdc        # 品牌规范守门
│   └── ...（完整清单见 rules/ 目录）
├── agents/                      # 18 个 SubAgent 定义
│   ├── verifier.md              # 独立功能验证（只读）
│   ├── fixer.md                 # TDD 修复执行者（可写）
│   ├── arch-destroyer.md        # 架构破坏者审核（只读）
│   ├── user-simulator.md        # 用户视角模拟（只读）
│   ├── ai-evaluator.md          # AI 效果评测（只读）
│   └── ...（完整清单见 agents/ 目录）
└── index/
    └── skill-index/
        ├── SKILL-INDEX.md       # 所有 Skill 的完整索引（版本/状态/触发词）
        └── SYSTEM-BLUEPRINT.md  # 体系设计蓝图
```

---

## 生态位置

本项目是「他山」大项目生态的组成部分，提供 AI 辅助产品开发的执行规范层。

```
他山生态
│
├── Resonnet                    ← 多智能体认知协作后端
│   └── tashan-openbrain        ← 认知分身应用（基于 Resonnet）
│
├── Tashan-TopicLab             ← 多专家圆桌讨论平台
│
├── tashan-cursor-skills ★     ← 本仓库：AI 执行规范体系（Skill/Rule/Agent）
│   └── 为所有产品开发提供 AI 执行标准
│
└── world-axiom-framework       ← 人—智能体数字世界公理框架（理论基础）
```

### 相关仓库

| 仓库 | 定位 | 链接 |
|------|------|------|
| Resonnet | 多智能体认知协作后端 | [TashanGKD/Resonnet](https://github.com/TashanGKD/Resonnet) |
| Tashan-TopicLab | 多专家圆桌讨论平台 | [TashanGKD/Tashan-TopicLab](https://github.com/TashanGKD/Tashan-TopicLab) |
| world-axiom-framework | 数字世界公理框架 | [TashanGKD/world-axiom-framework](https://github.com/TashanGKD/world-axiom-framework) |
| tashan-cursor-skills | 本仓库（AI 执行规范体系）| 当前页面 |

---

## 贡献

欢迎贡献！详见 [CONTRIBUTING.md](CONTRIBUTING.md)。

- **新增 Skill**：遵循 [Skill 设计原则](docs/Skill体系设计原则_v1.0.md)，并在 `index/skill-index/SKILL-INDEX.md` 注册
- **修改 Skill/Rule/Agent**：必须先阅读 `skills/skill-rule-修改规范/SKILL.md`，执行三问协议（根因/影响/验证）
- **文档贡献**：欢迎改进 README 或补充 `docs/`

---

## 更新日志

版本变更见 [CHANGELOG.md](CHANGELOG.md)。

---

## 许可证

MIT License. See [LICENSE](LICENSE) for details.
