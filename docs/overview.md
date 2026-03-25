# 他山 Cursor Skill 体系 — 完整说明文档

> **版本**：v1.0 | **日期**：2026-03-25
> **维护方**：他山 AI（TashanGKD）

---

## 一、这套体系要做到什么

### 1.1 核心目标

> **让 AI 在执行任务时能自主判断、按规范执行、并从经验中自我进化——而无需用户每次都手动指定流程。**

具体来说，这套体系要解决三个问题：

**问题1：AI 每次任务从零开始**
- 现状：每次对话，AI 凭训练知识随意发挥，没有沉淀，没有规范
- 目标：AI 有成体系的「做事方式」，复杂任务自动走完整流程

**问题2：犯过的错还会再犯**
- 现状：踩坑了，下次换个对话又踩一次
- 目标：踩坑 → 自动捕捉信号 → 更新规范 → 下次自动规避

**问题3：用户要记住所有流程**
- 现状：用户得知道「先做产品设计，再做架构，再开发」
- 目标：说出任务描述，AI 自主识别类型，自动走完整流程

### 1.2 量化目标（来自 SYSTEM-BLUEPRINT.md）

基于对 92 条历史对话的分析，提炼出 7 种核心工作模式。目标覆盖率：
- 产品开发全链路（设计→审核→架构→开发→测试→上线）：✅ 已覆盖
- 认知更新与知识积累：✅ 已覆盖
- Bug 修复闭环：✅ 已覆盖
- 代码库探索与理解：✅ 已覆盖
- 内容创作（文章/推文）：✅ 已覆盖
- 数字分身构建：✅ 已覆盖
- Skill 体系自我进化：✅ 已覆盖

---

## 二、设计依据

### 2.1 第一性原理：系统自我进化能力

（来源：Skill体系设计原则_v1.0.md §一）

> **Skill 体系的设计质量，由它能否自我进化来衡量。**

「自我进化」意味着：
1. **感知失败**：执行中自动检测踩坑（Signal A-F 机制）
2. **归纳模式**：多次相似失败 → 识别共因 → 更新根本规范（而非逐条修补）
3. **自动改进**：通过标准化流程更新 Skill/Rule，留有完整变更记录
4. **验证改进**：下次执行时可检验修复是否奏效
5. **路由更准**：AI 越来越能自主判断任务类型，不依赖用户提示词

### 2.2 上下文工程原理

（来源：上下文工程与智能体能力参考手册 v2.0）

```
LLM 的本质：f(context_window) → tokens
「记忆」= 你放进 context window 的内容
「身份」= 你在 system prompt 里写的角色定义
「知识」= 训练数据 + 你注入的外部文档
```

因此：
- **Rules（alwaysApply）** = 注入 system prompt，始终生效的约束
- **Skills（SKILL.md）** = 被 JIT Read 进 messages context，按需加载的步骤序列
- **Agents** = 独立的 context，实现「视角隔离」（审核者看不到创作者的推理过程）

### 2.3 三大闭环架构

```
Loop 1（Skill系统）= 程序性记忆层 — 系统知道「怎么做」
  B-objects：Rules + Skills + Agent定义
  [公司视角]：公司的规章制度、SOP、岗位职责手册

Loop 2（认知系统）= 认知根层 — 系统知道「为什么这样判断」
  L0/L1/L1.5/L2/L3：知识地图→系统性文档→原则→碎片→原始记录
  [公司视角]：创始人方法论、思维框架、经验沉淀

Loop 3（工作系统）= 执行输出层 — 系统在「做什么」
  K4 项目文档（产品定义/技术架构/代码/测试）
  [公司视角]：公司正在进行的所有项目文件夹
```

三个闭环通过六条通路相互连接，形成「越用越聪明」的自进化机制。

### 2.4 通用质量闭环

任何需要质量保障的工作，都遵循同一个抽象结构：

```
创建（Creator-agent）
  ↓
独立验证（Verifier-agent，clean context + readonly）
  ↓
创建者响应（A:有意为之 / B:确认修复 / C:需要讨论）
  ↓
Orchestrator 二次审核（审核响应质量）
  ↓
关闭/推进（基于客观标准）
```

这套结构体现了五条设计原则：
1. **角色分离**：创作者不验证自己
2. **客观化**：所有判断必须有可测标准
3. **阶段门控**：阶段推进必须经过明确门控
4. **分级响应**：按「AI确定性 + 决策权」而非「问题严重程度」分级
5. **双重充分性**：执行前确认「知识充分 + 能力充分」

---

## 三、当前实现：三层架构

### 3.1 层次结构

```
┌─────────────────────────────────────────────────────────────┐
│  约束层（Rules）：alwaysApply，每次对话自动注入 system prompt│
│  流程守门 + 文档管理 + 代码质量守门                          │
└────────────────────┬────────────────────────────────────────┘
                     │ 约束
┌────────────────────▼────────────────────────────────────────┐
│  步骤层（Skills）：触发词命中时 JIT Read，进入 messages context│
│  角色 Skill + 辅助 Skill + 认知 Skill + 内容创作 Skill      │
└────────────────────┬────────────────────────────────────────┘
                     │ 调用
┌────────────────────▼────────────────────────────────────────┐
│  子智能体层（Agents）：独立 context，视角隔离                  │
│  审核者（readonly）+ 修复者（writable）+ 认知处理器           │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 Rules（约束层）— 32个

#### 流程守门类（控制执行顺序和权限）

| Rule | 触发场景 | 作用 |
|------|---------|------|
| `session-bootstrap` | 每次对话 | 序列A（消息处理前）+ 序列B（任务完成后）的完整执行协议 |
| `role-menu` | 每次对话 | 所有角色的触发词路由表 + 14条强制规则 |
| `comprehensive-change-guard` | 多层变更（产品+技术+UI+代码≥2层）| 强制按序执行，禁止跳关卡 |
| `product-alignment-guard` | 影响用户可见行为的修复/变更 | 修复必须符合产品意图 |
| `bug-fix-tdd-guard` | 修复 Bug 时 | 强制 TDD 7步（先写失败测试→修→CI→追踪台）|
| `test-coverage-guard` | 宣布「测试完成」时 | 强制对账主测试文档，有🔲项禁止声明完成 |

#### 文档管理类

| Rule | 触发场景 | 作用 |
|------|---------|------|
| `document-path-resolver` | 读取项目文档前 | 从 project-config.md 解析实际路径 |
| `document-lifecycle-guard` | 角色激活时 | 自建领地、in-place 更新、旧版存档 |
| `project-doc-versioning-guard` | 修改项目 .md 前 | 备份旧版到 history/，追加变更记录 |
| `document-reference-guard` | 文档被引用/移动时 | 引用留痕 + 级联更新 |
| `cognitive-structure-write-guard` | 写入 L1/L1.5 文档时 | 历史备份+归因标注+级联写入 |

#### 代码质量类

| Rule | 触发场景 | 作用 |
|------|---------|------|
| `frontend-brand-guard` | 前端开发/UI 设计 | 强制遵守品牌规范（字体/配色/圆角）|
| `code-reuse-guard` | 含「复用」关键词 | 必须先 grep 找原始实现，禁止重新实现 |
| `tech-discovery-capture` | 开发中遇到不确定方案 | 强制搜索验证，高价值方案写入技术洞察库 |
| `skill-design-guard` | 设计/修改 Skill/Agent/Rule | 读取 Skill体系设计原则，确认三型判断 |

### 3.3 Skills（步骤层）— 95个

#### 角色类（产品开发全链路）

| Skill | 对应角色 | 核心职责 |
|-------|---------|---------|
| `role-产品开发协调者` | 域协调者 | 识别任务类型（新功能/Bug/配置变更），规划执行序列 |
| `role-产品经理` | PM | 产品定义 + 开发计划 |
| `role-技术架构师` | 技术架构师 | 技术架构 + 接口规范 |
| `role-前端开发` | 前端工程师 | React/TS/Vite 实现 |
| `role-后端开发` | 后端工程师 | FastAPI/Python 实现 |
| `role-AI工程师` | AI工程师 | Prompt设计 + Agent构建 + 效果评测 |
| `role-UI设计师` | UI/UX设计师 | 体验设计 + 视觉规范 |
| `role-测试工程师` | QA | 关卡C：全量验证 |
| `role-DevOps` | 运维工程师 | 部署 + 上线 |
| `role-数据分析师` | 数据分析师 | 上线后监控 + 指标分析 |
| `role-审核者-用户模拟` | 关卡A | 产品定义审核（用户视角）|
| `role-审核者-系统破坏` | 关卡B | 架构审核（破坏者视角）|

#### 辅助/维护类

| Skill | 触发时机 | 核心作用 |
|-------|---------|---------|
| `issue-tracker` | 发现问题时 | Bug/需求分类，写入追踪台 |
| `bug-fix-loop-coordinator` | 测试完成后 | 读追踪台→dispatch fixer→回归→收敛 |
| `project-convention-resolver` | 发现规范偏差 | 分类→路由执行修复→验证 |
| `project-retrospective` | 项目完成后 | 批量复盘，沉淀 Skill 体系 |
| `project-backlog` | 收到外部反馈时 | 统一 Inbox：收集所有类型反馈，激活时分类路由处理 |
| `expert-bootstrap` | 需要领域专家视角时 | 调研→对标→自问自答→产出专家 Agent 定义 |

#### 认知积累类

| Skill | 触发时机 | 核心作用 |
|-------|---------|---------|
| `cognitive-capture-fragment` | 有新洞见/思考碎片 | 捕捉 L2 层碎片 |
| `cognitive-integrate-fragments` | 碎片积累后 | 整合进 L1 系统性文档 |
| `cognitive-extract-principle` | 发现跨领域模式 | 提炼 L1.5 底层原则 |
| `cognitive-daily-briefing` | 每日汇报 | 生成认知系统状态快照 |
| `cognitive-review-brain-map` | 复盘时 | 生成认知结构全景图 |

### 3.4 SubAgents（子智能体层）— 18个

| SubAgent | 可写 | 调用方 | 作用 |
|---------|------|-------|------|
| `verifier` | ❌只读 | role-测试工程师 | 独立验证代码实现 |
| `fixer` | ✅可写 | bug-fix-loop-coordinator | TDD修复：复现→Red→Green→CI |
| `arch-destroyer` | ❌只读 | role-审核者-系统破坏 | 架构漏洞扫描 |
| `user-simulator` | ❌只读 | role-审核者-用户模拟 | 挑剔用户视角审查 |
| `ux-reviewer` | ❌只读 | role-UI设计师 | UI/UX 陌生用户视角审查 |
| `ai-evaluator` | ❌只读 | role-AI工程师 | LLM 调用链效果评测 |
| `skill-updater` | ✅可写 | project-retrospective | 处理单条经验，更新 Skill |
| `skill-simulator` | ❌只读 | skill-designer | 模拟执行新 Skill，找歧义 |
| `skill-system-destroyer` | ❌只读 | skill-designer | 新 Skill 与体系的冲突检测 |
| `cognitive-verifier` | ❌只读 | cognitive-update-knowledge | 认知文档更新的独立验证 |

---

## 四、目前做到了哪些

### ✅ 已实现

**产品开发全链路**：
- 从「你说需求」到「上线验收」的完整流程，无需用户手动触发每一步
- 关卡 A（产品审核）→ 关卡 B（架构审核）→ 关卡 C（功能测试）的完整门控
- Bug 修复闭环：发现 → TDD修复 → 回归验证 → 追踪台更新

**自我进化机制**：
- Signal A-G 自动捕捉（6类信号：踩坑/盲区/缺口/洞见/效果不符/意外行为/根因）
- PENDING-EXPERIENCES 积压队列 + project-retrospective 批量处理
- skill-rule-修改规范 三问协议 + 版本留痕

**文档管理体系**：
- 每个项目自动维护「领地」（产品定义/技术架构/追踪台等）
- 版本留痕、变更记录、级联更新

**认知积累体系**：
- 工作中的洞见 → L2碎片 → 整合进 L1 知识文档
- 跨领域原则提炼 → L1.5 原则库
- 每日/定期认知状态汇报

### ⚠️ 基本实现但待完善

- **expert-bootstrap**（v1.0）：调研→自问自答→专家 Agent，首次实现，待真实场景验证
- **project-backlog**（v1.0）：统一 Inbox 收集外部反馈，激活时路由，待验证
- **域协调者 role-产品开发协调者**（v1.0）：任务类型识别 + 执行序列规划，待真实验证

### ❌ 已知缺口（PENDING-SKILLS）

- 多专家视角报告合并协议（Orchestrator 合并5个专项视角审查结果的机制）
- 自动监控集成（P0 检测无需手动触发，Level 1 外部监控服务接入）

---

## 五、体系文件结构

```
tashan-cursor-skills/
├── README.md                    ← 快速入门
├── docs/
│   ├── overview.md             ← 本文档（完整说明）
│   ├── Skill体系设计原则_v1.0.md ← 设计哲学原文
│   └── SYSTEM-BLUEPRINT.md     ← 系统蓝图（来自历史对话分析）
├── skills/                      ← 95个 Skill（每个含 SKILL.md）
│   ├── role-产品经理/
│   ├── role-技术架构师/
│   ├── role-前端开发/
│   ├── ...（见 SKILL-INDEX.md 完整清单）
├── rules/                       ← 32个 Rule（.mdc 文件）
│   ├── session-bootstrap.mdc   ← 最核心：执行协议
│   ├── role-menu.mdc           ← 最核心：路由表
│   └── ...
├── agents/                      ← 18个 SubAgent 定义
│   ├── verifier.md
│   ├── fixer.md
│   └── ...
└── index/
    └── skill-index/
        ├── SKILL-INDEX.md      ← 所有 Skill 的完整索引
        └── SYSTEM-BLUEPRINT.md ← 体系设计来源分析
```

---

## 六、如何使用

### 6.1 在 Cursor 中使用

1. 将 `skills/` 目录内容复制到你的项目的 `.cursor/skills/`
2. 将 `rules/` 目录内容复制到你的项目的 `.cursor/rules/`
3. 将 `agents/` 目录内容复制到你的项目的 `.cursor/agents/`

重启 Cursor 后，所有 Skill 和 Rule 自动生效。

### 6.2 定制适配

每个 Skill 的触发词在 `SKILL.md` 文件的 frontmatter 中定义：
```yaml
---
name: role-产品经理
description: 产品经理角色。关键词：产品/需求/用户流/...（触发词列表）
---
```

修改 `description` 字段可以调整触发场景。

### 6.3 修改和扩展

新建或修改 Skill/Rule/Agent 前，必须先阅读：
- `rules/skill-design-guard.mdc`（三型判断：是 Rule / Skill / Agent？）
- `skills/skill-rule-修改规范/SKILL.md`（三问协议）

---

## 七、版本历史

| 版本 | 日期 | 主要变化 |
|------|------|---------|
| v1.0 | 2026-03-25 | 初始公开发布（95 Skills / 32 Rules / 18 Agents）|
