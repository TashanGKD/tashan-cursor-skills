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
  <a href="#这是什么">这是什么</a> •
  <a href="#三大闭环架构">三大闭环</a> •
  <a href="#三个场景的完整闭环">三个场景</a> •
  <a href="#认知体系的构建与更新">认知体系</a> •
  <a href="#skill-体系的自循环">Skill自循环</a> •
  <a href="#完整-skill-速查">Skill 速查</a> •
  <a href="#安装方式">安装</a> •
  <a href="README.en.md">English</a>
</p>

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Skills](https://img.shields.io/badge/Skills-95-blue)](#完整-skill-速查)
[![Rules](https://img.shields.io/badge/Rules-32-green)](#安装方式)
[![Agents](https://img.shields.io/badge/SubAgents-18-purple)](#完整-skill-速查)

> 围绕「AI 自我进化」构建的 Cursor 执行规范体系：覆盖产品设计→架构→开发→测试→上线全链路，自动识别任务类型，自动触发对应流程，并将踩坑经验自动转化为规范更新。

---

## 这是什么

**这套体系解决三个核心问题：**

| 问题 | 表现 | 解决方式 |
|------|------|---------|
| AI 每次从零开始 | 每次对话凭训练知识随意发挥，没有规范 | 完整的角色体系 + 强制执行协议，无论什么任务都有标准流程 |
| 犯过的错还会再犯 | 踩坑了，换个对话又踩一次 | Signal 机制自动捕捉错误 → 更新 Skill/Rule → 下次自动规避 |
| 用户要记住所有流程 | 得手动告诉 AI「先做产品设计，再做架构…」| 说出任务描述，AI 自主识别类型，自动完成全链路 |

**用一句话描述**：你说「做一个登录功能」，AI 自动完成产品评审 → 架构评审 → 开发 → 测试 → 上线的全部流程。

---

## 三大闭环架构

> 这是理解整套体系的核心概念。

这套体系由三个相互连接的闭环构成，每个闭环对应一种能力层次：

```
┌─────────────────────────────────────────────────────────────┐
│  Loop 2（认知系统）= 系统「知道为什么」                        │
│  · L0/L1 知识地图 + 系统性文档（产品理论、架构原则等）         │
│  · L1.5 底层原则库（提炼出的跨领域规律）                       │
│  · L2 碎片层（工作中产生的洞见，待整合）                       │
│  · L3 原始记录（任务日志、决策档案）                           │
│  [公司视角：创始人的方法论、思维框架、经验积累]                  │
└───────────────────────────┬─────────────────────────────────┘
                            │ 通路A：认知根激活工作方式
                            │ 通路B：工作产生洞见→L2碎片
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Loop 3（工作系统）= 系统「正在做什么」                        │
│  · K4 项目文档（产品定义/技术架构/测试规格）                    │
│  · S 状态对象（orchestration-state/decision-log）             │
│  · 实际代码、测试、部署产物                                     │
│  [公司视角：公司正在进行的所有项目文件夹]                        │
└───────────────────────────┬─────────────────────────────────┘
                            │ 通路C：Skill能力支撑执行
                            │ 通路D：工作暴露能力缺口
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Loop 1（Skill系统）= 系统「知道怎么做」                       │
│  · Rules（alwaysApply，始终在场的约束）                        │
│  · Skills（按需加载的执行步骤序列）                             │
│  · SubAgents（独立 context 的专项验证者）                      │
│  [公司视角：规章制度、岗位职责、SOP 流程手册]                   │
└─────────────────────────────────────────────────────────────┘
```

**六条通路把三个环连接起来：**

| 通路 | 方向 | 触发机制 | 效果 |
|------|------|---------|------|
| **通路A** | Loop2→Loop3 | 每次任务开始，读取认知根 | 用方法论指导当次任务，而非凭感觉 |
| **通路B** | Loop3→Loop2 | D5 D信号（洞见）→ `cognitive-capture-fragment` | 工作中的洞见沉淀为认知碎片 |
| **通路C** | Loop1→Loop3 | Skill 版本更新后，下次执行读取新版 | 上次沉淀的经验，这次任务自动应用 |
| **通路D** | Loop3→Loop1 | D5 E信号（流程缺口）→ PENDING-SKILLS | 工作中发现缺少某类能力 → 建新 Skill |
| **通路E** | Loop2→Loop1 | L1文档更新后，Grep找依赖Skill → 更新D0-B | 认知进化驱动Skill方法论同步 |
| **通路F** | Loop1→Loop2 | B信号重复3次 → 认知层反思 | 持续失败模式触发方法论层面的重审 |

---

## 三个场景的完整闭环

### 场景一：开发一个新功能

#### 任务产出

| 产出物 | 文件 | 类型 |
|--------|------|------|
| 产品规格 | 产品定义.md（含功能状态表）| K4 K-object |
| 技术方案 | 技术架构.md + decision-log 追加 | K4 K-object |
| 实现代码 | 代码文件 | 实现产物 |
| 验收报告 | 测试报告.md | S1* 审计对象 |
| 关卡报告 | 关卡A/B/C审核报告.md | S1* 只读审计 |

#### 完整闭环

```
[开始前：通路A — 认知根激活]
role-产品经理 Step D0：
  读取「AI时代产品设计原则」（L1认知文档）
  确认认知根：「本次产品设计基于 §三：闭环完整性原则」
  → 这决定了产品设计的「为什么」：为什么要这样设计用户流

            ↓

[执行阶段：Loop 3]
产品定义 → [关卡A] → 技术架构 → [关卡B] → 并行开发 → [关卡C] → 上线
  ↑关卡A用独立视角（user-simulator）防止「设计者看不到的盲点」
  ↑关卡B用破坏者视角（arch-destroyer）防止「架构师忽略的安全/性能问题」

            ↓

[任务完成后：D5信号自动路由]

  ┌─ D信号（洞见）──────────────────────────────────────────────────┐
  │ 「发现：Redis作为AI应用短期记忆层，比PostgreSQL快10x」          │
  │ → [cognitive-capture-fragment] → L2碎片                         │
  │ → 积累后 [cognitive-integrate-fragments] → L1技术架构文档        │
  │ → [通路E] → 架构师Skill D0-B 更新，下次架构任务读到这条经验      │
  └──────────────────────────────────────────────────────────────────┘

  ┌─ A信号（踩坑）──────────────────────────────────────────────────┐
  │ 「PostgreSQL序列在pg_dump后不同步，导致注册报主键冲突」          │
  │ → 立即追加到 role-后端开发 Skill 的「踩坑速查」步骤             │
  │ → 下次后端开发任务读到 Skill 时，这条警告自动在场              │
  └──────────────────────────────────────────────────────────────────┘

  ┌─ E信号（缺口）──────────────────────────────────────────────────┐
  │ 「每次部署前需要检查向量索引，但没有对应Skill步骤」             │
  │ → 追加到 PENDING-SKILLS.md → 下次 project-retrospective 处理    │
  │ → [skill-designer] 建新 Skill → [通路C] 下次任务自动使用        │
  └──────────────────────────────────────────────────────────────────┘

            ↓

[迭代认知体系：通路B完整链]
碎片积累 → [cognitive-integrate-fragments] → L1文档更新
                                              ↓
                          [通路E] rg 搜索依赖此文档的Skills
                                              ↓
                          PENDING-SKILLS 追加对齐通知
                                              ↓
                          [project-retrospective] 处理 → Skill D0-B更新
                                              ↓
                          下次同类任务，AI读到更新的方法论，做出更好的决策
```

**这个场景的闭环价值**：第1次做功能时踩坑的Redis用法，自动变成了第2次的「架构师最佳实践」，不需要人工记录和传递。

---

### 场景二：修复一个 Bug

#### 任务产出

| 产出物 | 文件 | 类型 |
|--------|------|------|
| Bug记录 | bug-log.md（追加）| S-object，只追加 |
| 修复代码 | 代码文件 | 实现产物 |
| 追踪台更新 | 技术问题追踪台.md | K4 K-object |
| 工程原则（若有）| 研发规范.md 或 Skill 步骤 | K3 K-object 或 B-object |

#### 完整闭环

```
[开始前：通路A — 认知根激活]
fixer 子智能体 Step D0：
  读取产品定义.md → 「确认：修复必须符合产品意图，不能只图技术方便」
  [product-alignment-guard Rule 强制执行这一点]
  → 这防止了一种常见错误：技术上修了，但产品体验更差了

            ↓

[执行阶段：TDD修复循环]
[issue-tracker] 分类 → P0/P1技术Bug
[bug-fix-loop-coordinator] 读追踪台 → dispatch fixer
  循环：
    [fixer] → Step1: 写失败测试（先确认能复现）
            → Step2: 修复代码（让测试通过）
            → Step3: CI验证
            → Step4: 更新追踪台状态
  → [verifier] 独立回归验证（不看修复者的推理，独立判断）

            ↓

[任务完成后：D5信号分流]

  ┌─ A信号（踩坑）──────────────────────────────────────────────────┐
  │ 「bore SSH每个端口只支持1条并发TCP，AI和用户会互相断连」        │
  │ → 追加到 role-DevOps Skill 的踩坑速查                          │
  │ → REFERENCE.md §踩坑速查 更新                                   │
  └──────────────────────────────────────────────────────────────────┘

  ┌─ G信号（结构性根因）────────────────────────────────────────────┐
  │ 「第3次出现并发锁问题，根因是架构设计时没有并发边界」           │
  │ → PENDING-PROPOSALS.md [HUMAN-REQUIRED]                         │
  │ → 触发架构层讨论：「是否需要在架构规范里加并发边界检查清单？」  │
  │ → 用户确认后 → 研发规范.md 更新（K3 K-object）                 │
  │ → [通路E] 通知依赖此规范的 Skill 重新对齐                      │
  └──────────────────────────────────────────────────────────────────┘

  ┌─ D信号（洞见）──────────────────────────────────────────────────┐
  │ 「TDD发现的根本价值：不是测试覆盖率，而是先定义完成标准」      │
  │ → L2认知碎片 → 积累后整合进「AI智能体任务分类体系.md」L1文档   │
  └──────────────────────────────────────────────────────────────────┘

            ↓

[迭代认知体系]
G信号的架构规范更新 → 研发规范.md v2.0
                      → [通路E] role-技术架构师 Skill D0-B 更新
                      → 下次架构任务，架构师自动带着「并发边界检查清单」
```

**这个场景的闭环价值**：同类 Bug 的第3次出现变成了架构规范的一部分，第4次在设计阶段就被拦截，而不是等到线上再修。

---

### 场景三：积累一个认知洞见

> 这个场景展示的是认知系统（Loop 2）的自我迭代过程本身。

#### 任务产出

| 产出物 | 文件 | 类型 |
|--------|------|------|
| 认知碎片 | L2_碎片化思考/xxx.md | L2 K-object |
| 系统性文档更新 | L1_系统性文档/xxx.md | L1 K-object |
| 底层原则 | L1.5_底层原则库.md | L1.5 K-object |
| Skill方法论更新 | D0-B 摘要（嵌入 Skill system prompt）| B-object |

#### 完整闭环

```
[触发：日常工作中产生洞见]
你说：「记录一下，我发现当用户和AI的多轮对话超过20轮时，
       AI对早期约定的记忆会显著衰减，需要在Prompt里加上关键约定的摘要」

            ↓

[捕捉阶段]
[cognitive-capture-fragment]
  → 结构化写入 L2 碎片：
    title: "长对话的关键约定摘要机制"
    domain: "AI工程/上下文工程"
    insight: "20轮后关键约定记忆衰减，需在每次Prompt头部注入约定摘要"
    evidence: "tashan-openbrain 实测，2026-03-25"
    generalizability: "所有超过10轮的AI对话场景"

            ↓

[积累后整合阶段]
当 L2 同域碎片积累到一定量：
[cognitive-integrate-fragments]
  → 「小人机制」：从认知文档居民视角判断这条碎片放在哪里最合适
  → 整合进「上下文工程与智能体能力参考手册.md」L1文档
  → 追加变更记录，留档旧版本（project-doc-versioning-guard Rule 强制）

            ↓

[原则提炼阶段]
当发现多个碎片指向同一底层规律：
[cognitive-extract-principle]
  → 提炼新原则 P_new：「AI长对话的上下文稳定性原则：关键约定必须周期性重注入」
  → 写入 L1.5 底层原则库（需用户确认）
  → 追加到认知体系不变量中

            ↓

[通路E：认知更新→Skill对齐]
L1文档「上下文工程手册」更新后：
  rg "上下文工程与智能体" .cursor/skills/ → 找到 role-AI工程师
  → PENDING-SKILLS 追加：「role-AI工程师 D0-B需对齐新增的长对话稳定性原则」
  → [project-retrospective] 处理 → role-AI工程师 D0-B 更新
  → 下次AI工程任务，AI自带「关键约定需重注入」这条经验

            ↓

[通路A：新认知激活新工作]
下一次 role-AI工程师 任务开始：
  读取更新后的 D0-B → 「长对话中，确认是否已设计约定重注入机制」
  → 这次任务的Prompt设计会更完整，减少20轮后的对话质量下降
```

**这个场景的闭环价值**：实践中一次踩坑 → 变成 L2 碎片 → 整合进 L1 → 提炼为 L1.5 原则 → 内化进 Skill D0-B → 下次任务自动带着这个认知，形成「越用越聪明」的飞轮。

---

## 认知体系的构建与更新

认知体系（Loop 2）是整套体系的「认知根」层，它有 7 种构建和更新模式：

### 模式一：日常碎片捕捉

**触发：** 「记录一下 / 有个洞见 / 我发现」
```
[cognitive-capture-fragment]
输入：原始想法（一句话到一段话）
输出：结构化 L2 碎片（含 title/domain/insight/evidence/generalizability）
时机：随时，不需要积累，立即执行
```

### 模式二：碎片整合

**触发：** 「整合碎片 / 哪些碎片没整合 / 处理积压」
```
[cognitive-integrate-fragments]
输入：多条同域 L2 碎片 + 对应的 L1 文档
输出：L1 文档更新（精准追加，非重写）+ history/ 备份
机制：「小人机制」—— 以L1文档居民视角判断碎片放在哪个章节
```

### 模式三：原则提炼

**触发：** 「这些碎片有共性 / 提炼一下规律 / 有什么底层逻辑」
```
[cognitive-extract-principle]
输入：多条指向同一规律的碎片
输出：L1.5 底层原则（需用户确认后写入）
价值：将具体经验升华为可跨场景应用的规律
```

### 模式四：受控知识更新

**触发：** 「更新[文档名] / 在[文档]里加上XXX」
```
[cognitive-update-knowledge]
输入：明确的修改意图 + 目标 L1 文档
输出：L1 文档更新 + 自动备份 + 一致性验证 + 变更记录
安全机制：修改前备份，[cognitive-verifier] 子智能体独立验证自洽性
```

### 模式五：系统重组

**触发：** 「系统整理 / 认知结构乱了 / 全量梳理」
```
[cognitive-reorganize]
输入：全工作区文档
输出：文档归属建议 + 分类路由方案（按三大闭环框架）
时机：文档散乱后的大扫除，或新启动一个认知维度时
```

### 模式六：一致性检查

**触发：** 「一致性检查 / 自洽验证 / 跑一遍验证」
```
[cognitive-consistency-check]
输入：认知结构全量文档
输出：C1-C10 一致性报告（矛盾列表 + 建议修复方案）
定期执行，防止认知文档随时间产生内部矛盾
```

### 模式七：矛盾检测

**触发：** 「[文档A]和[文档B]是否一致 / 检查矛盾」
```
[cognitive-detect-contradiction]
输入：两份或多份 L1 文档
输出：矛盾点列表 + 基于 L1.5 原则的消解方案
```

---

## Skill 体系的自循环

> Skill 体系不只是工具集，它本身也是一个能自我进化的系统。

### 单次经验 → Skill 更新

```
任何任务完成后，D5信号自动路由：

A信号（踩坑）──────────────→ 立即追加到对应 Skill 步骤（B-object Level 1修改）
B信号（Skill意外行为）──────→ PENDING-SKILLS，等 skill-system-health-check 处理
E信号（流程缺口）──────────→ PENDING-SKILLS，后续 skill-designer 建新 Skill
G信号（结构性根因）────────→ PENDING-PROPOSALS [HUMAN-REQUIRED]，人工确认后修规范

手动触发：
「踩坑了/经验值得记」──────→ [skill-capture-closure]
                               判断：修改已有Skill / 新建Skill / 记录原则
                               执行：三问协议 + 备份 + 变更记录
```

### 项目级批量复盘

```
「项目做完了/批量复盘」──────→ [project-retrospective]
                               扫描本次所有用到的Skills
                               逐个判断：是否需要更新？
                               批量调用 [skill-updater 子智能体] 执行更新
                               输出：复盘报告 + 更新清单
```

### 体系健康检查

```
定期或发现异常时：
[skill-system-health-check]
  → 检查：触发词冲突 / 孤立组件 / 版本漂移 / Rule叠加矛盾
  → 输出：健康报告

[skill-domain-health-check]
  → 检查某个域（如「产品开发」）的传播完备性
  → 任意入口是否能到达正确终态

[skill-domain-self-optimizer]
  → 基于健康报告，生成定向修复方案
  → 新Skill提案 / 现有Skill修改 / 触发链补全
```

### Skill 体系战略演进

```
[skill-evolution-planner-meta]
  输入：CO-BUILD-LOG（决策轨迹）+ PENDING-EXPERIENCES + PENDING-SKILLS
  输出：体系演进路线图（哪些Skill需新建/合并/拆分/废弃）

[skill-system-evolution-executor]
  执行 L4 级别的体系重构（Phase0规模确认→Phase1分析→Phase2双审核→Phase3执行）

[expert-bootstrap]
  按需为新领域培养专家Agent（调研→自问自答→专家配置）
  输出：可复用的领域专家 B-object（Agent定义文件）
```

### 自循环的完整图景

```
实际任务执行
    │
    ▼ D5信号
  A/E信号 ─────→ PENDING-SKILLS ──→ [skill-designer] ──→ 新 Skill
  B信号   ─────→ [skill-system-health-check] ──→ [skill-domain-self-optimizer]
  G信号   ─────→ PENDING-PROPOSALS ──→ 人工确认 ──→ 规范更新
  D信号   ─────→ L2碎片 ──→ L1整合 ──→ [通路E] ──→ Skill D0-B更新
    │
    ▼ 批量处理
[project-retrospective]
    │
    ▼
[skill-updater] × N ──→ Skill 版本更新
    │
    ▼ 通路C
下次任务 ──→ 读取更新后的 Skill ──→ 更好的执行
    │
    └──────────── 飞轮 ──────────────────────────────────────┘
```

**飞轮效应**：每次任务 → 至少一个信号 → 至少一次体系更新 → 下次同类任务更好。
用的越多，每次任务质量越高，积累的规范越完善。

---

## 用户工作流指南

> 理解了上面的闭环，以下工作流的每一步「为什么要这样做」就都清楚了。

### 工作流一：开发新功能

**你说什么触发：** 「做一个XXX功能」「新需求：用户要能XXX」「帮我做一个XXX」

```
你说需求
  │
  ▼ [自动识别：新功能任务]
[role-产品开发协调者] 规划执行序列
  │
  ▼ [1. 产品设计阶段]
[role-产品经理] → 输出：产品定义.md + 功能状态表
  │
  ▼ [关卡A：独立审核，clean context]
[role-审核者-用户模拟 + user-simulator 子智能体]
  → 用挑剔用户视角走所有核心路径，找出设计漏洞
  → PASS → 产品定义冻结，进入下一阶段
  → NEEDS-REVISION → 返回 PM 修改，再次关卡A
  │
  ▼ [2. 技术架构阶段]
[role-技术架构师] → 输出：技术架构.md + 接口规范
  │
  ▼ [关卡B：独立审核]
[role-审核者-系统破坏 + arch-destroyer 子智能体]
  → 以黑客/极端用量视角找安全漏洞、性能瓶颈、架构缺陷
  → PASS → 架构冻结，开发启动
  │
  ▼ [3. 并行开发阶段]
[test-env-setup] 准备测试环境
[role-前端开发] + [role-后端开发] + [role-AI工程师] 并行实现
  │
  ▼ [关卡C：独立验证]
[role-测试工程师 + verifier 子智能体]
  → 对照产品定义逐一验证，发现 Bug 自动记录
  → PASS → 可上线
  │
  ▼ [4. 上线阶段]
[role-DevOps] → 部署 + 验证 + 监控配置
  │
  ▼ [5. 自动收尾]
D5 信号路由：踩坑 → Skill 更新 / 洞见 → 认知碎片 / 缺口 → PENDING-SKILLS
```

---

### 工作流二：修复 Bug

**你说什么触发：** 「登录接口报500」「这个功能不对」「发现了bug」「有个问题」

```
你描述问题
  │
  ▼
[issue-tracker] 分类：产品设计问题 or 技术实现问题
                写入两个追踪台（产品/技术分开管理）
  │
  ▼
[bug-fix-loop-coordinator] 读追踪台，规划修复顺序
  │
  循环 × N：
  ▼
  [fixer 子智能体] TDD 修复流程：
    1. 复现 Bug（写失败测试）
    2. 修复代码（让测试通过）
    3. 运行 CI
    4. 更新追踪台（P0/P1 是否清零？）
  │
  ▼ [所有 P0/P1 清零]
[verifier 子智能体] 独立回归验证
  │
  ▼ 可选：[role-DevOps] 部署上线
```

**[`bug-fix-tdd-guard`]（Rule，自动生效）** — 任何修复 Bug 的操作都强制走 TDD 7步，禁止不写测试直接改代码。

---

### 工作流三：收集和处理外部反馈

**你说什么触发：** 「记录这几个待办」「用户说XXX」「先存到待办文档」「处理项目待办」

```
[模式A：收集]
你说「有几个反馈/需求/问题，先记下来」
  │
  ▼
[project-backlog] Inbox 模式
  → 所有类型的信息都追加到「项目待办.md」
  → 不即时处理，积累后批量处理
  → 格式：原话保存 + 来源标注

[模式B：处理]
你说「处理项目待办/按待办文档修复」
  │
  ▼
[project-backlog] 处理模式
  → 逐条分类：技术Bug / UX问题 / 新功能 / 建议
  → 自动路由到对应工作流（Bug→修复闭环，新功能→产品设计…）
  → 生成批次处理报告
```

---

### 工作流四：接手新代码库

**你说什么触发：** 「读一下这个项目」「理解这个代码库」「接手项目」「帮我读一下这个代码」

```
你指向代码库
  │
  ▼
[codebase-explorer] 全量扫描
  → 目录结构 → 核心模块 → 依赖关系 → 数据流
  → 与已有产品定义/文档对比（如有）
  → 输出：架构理解文档（可读的技术全景）
  │
  ▼ 可选：
[architecture-gap-mapper] 与另一个系统/竞品对比
  → 输出：兼容/冲突/缺失三类，带代码证据
```

---

### 工作流五：内容创作

**你说什么触发：** 「写一篇技术文章」「帮我写公众号推文」「写一篇关于XXX的文章」「调研一下XXX」

```
[调研]
「调研一下XXX / 系统了解XXX」
  → [research-output] 调研 → 图文 Markdown → 注册到知识库

[公众号文章]
「写一篇公众号文章」
  → [wechat-article-writer] 内容撰写 → HTML排版 → 配图 → 底部模板 → 审稿

[技术文章/长文]
「写一篇技术文章」
  → [general-article-writer] 大纲确认 → 正文 → 审稿 → 格式输出

[审稿]
「帮我检查这篇文章」
  → [article-proofreading] 按标准检查 AI 腔/标题/绝对表达/结语
```

---

### 工作流六：系统自我进化

> 这是整套体系最独特的部分。AI 不只执行任务，还自动积累经验并更新规范。

**踩坑后的自动沉淀：**
```
任务执行中出现问题
  │
  ▼ [D5 信号自动路由，任务完成后]
  ├── A信号（踩坑）→ 立即追加到对应 Skill 步骤的警告
  ├── B信号（意外行为）→ PENDING-SKILLS.md，等待 Skill 更新
  ├── D信号（洞见）→ [cognitive-capture-fragment] → L2 认知碎片
  ├── E信号（流程缺口）→ PENDING-SKILLS.md，后续建新 Skill
  └── G信号（结构性根因）→ PENDING-PROPOSALS.md [人工确认]

[project-retrospective] 项目完成后批量处理
  → 读取所有未处理信号 → 归纳共性 → 更新 Skills/Rules
  → [skill-updater 子智能体] 执行实际更新（三问协议 + 备份）
```

**手动记录经验：**
```
「这次踩坑了 / 这个经验值得记」
  → [skill-capture-closure] 单次经验沉淀
  → 判断：新建 Skill / 更新已有 Skill / 记录原则

「立一个原则 / 以后所有X都要Y」
  → [engineering-principle-recorder] 写入对应执行层
```

---

### 工作流七：认知积累

> 适合研究者、知识工作者记录和管理自己的认知体系。

```
日常记录想法：
「记录一下 / 我发现 / 有个洞见」
  → [cognitive-capture-fragment] → L2 碎片（结构化保存）

整合碎片：
「整合碎片 / 哪些碎片没整合」
  → [cognitive-integrate-fragments] → 合并进 L1 系统性文档

提炼原则：
「这些碎片有没有共性 / 提炼一下规律」
  → [cognitive-extract-principle] → L1.5 底层原则库

每日汇报：
「今天有什么 / 同步状态」
  → [cognitive-daily-briefing] → 认知状态快照 + 积压提醒

按你的认知文档回答问题：
「基于我的文档 / 我之前怎么想的」
  → [cognitive-ask] → 带引用、置信度、矛盾的回答
```

---

### 工作流八：按需培养领域专家

**你说什么触发：** 「需要一个并发性能专家」「这个任务需要安全审查专家」「培养专家」

```
「需要X领域的专家 / 我们没有X方面的专家」
  │
  ▼
[expert-bootstrap] 四阶段专家培养：
  Phase 1：调研（WebSearch + 内部知识库 + 项目代码）
  Phase 2：对标整理（最佳实践 vs 项目现状差距表）
  Phase 3：自问自答反思（生成10+资深从业者视角的问题，自己回答）
  Phase 4：专家配置输出（压缩为D0-B → 写入 Agent 定义文件）
  │
  ▼
产出：可被直接 dispatch 的专家 Agent（.cursor/agents/xxx-expert.md）
```

---

## 完整 Skill 速查

### 一、产品开发全链路

| Skill / Agent | 触发方式 | 做什么 |
|--------------|---------|--------|
| **role-产品开发协调者** | 「新项目/做个功能/有个bug/全量测试」| 识别任务类型，规划执行序列，不执行具体任务 |
| **role-产品经理** | 「产品/需求/用户流/MVP/产品定义」| 产品定义 + 开发计划，含关卡A前置检查 |
| **role-技术架构师** | 「技术架构/系统设计/接口规范/技术选型」| 技术方案 + 接口规范，关卡B前 |
| **role-前端开发** | 「前端/React/TypeScript/Vite/UI实现」| React+TS 实现，含接口联调 |
| **role-后端开发** | 「后端/FastAPI/Python/API接口/PostgreSQL」| FastAPI 后端实现，含 DB 集成测试 |
| **role-AI工程师** | 「AI/LLM/Prompt/上下文工程/RAG/智能体」| Prompt 设计 + Agent 构建 + 效果评测 |
| **role-UI设计师** | 「设计/UI/UX/交互设计/体验感/视觉」| UX/视觉设计 + 组件规范 |
| **role-测试工程师** | 「测试/验收/Bug报告/关卡C/闭环测试」| 关卡C：全量功能验证 + 人工验收清单 |
| **role-DevOps** | 「部署/上线/CI-CD/服务器/Docker/nginx」| 部署 + 运维 + 监控配置 |
| **role-数据分析师** | 「数据分析/指标/用户行为/产品健康度报告」| 上线后指标分析 + 断裂节点识别 |

### 二、质量关卡（独立视角，readonly + clean context）

| Agent | 调用方 | 做什么 |
|-------|--------|--------|
| **user-simulator** | role-审核者-用户模拟（关卡A）| 以挑剔用户视角走核心路径，找设计漏洞 |
| **arch-destroyer** | role-审核者-系统破坏（关卡B）| 以黑客视角找安全漏洞、性能瓶颈、架构缺陷 |
| **verifier** | role-测试工程师（关卡C）| 独立验证实现是否真正完成，避免自我确认偏差 |
| **ux-reviewer** | role-UI设计师 | 以陌生用户视角审查 UI/UX 体验 |
| **ai-evaluator** | role-AI工程师 | 独立评测 LLM 调用链效果 |

### 三、Bug 修复闭环

| Skill / Agent | 触发方式 | 做什么 |
|--------------|---------|--------|
| **issue-tracker** | 「有个问题/发现bug/这里不对/用不了」| 将问题分类拆解，分别写入产品/技术追踪台 |
| **bug-fix-loop-coordinator** | 「全自动修复/按Bug清单修复/循环修复」| 读追踪台 → dispatch fixer × N → 回归 → 收敛 |
| **fixer（Agent）** | bug-fix-loop-coordinator 调用 / 「spawn fixer」| TDD 修复循环：复现→失败测试→修复→CI→追踪台 |
| **test-env-setup** | 「准备测试环境/环境预检/测试前准备」| 启动服务、数据库、账号配置，让测试在已知环境运行 |

### 四、外部反馈管理

| Skill | 触发方式 | 做什么 |
|-------|---------|--------|
| **project-backlog** | 收集：「先记到待办/存到待办文档」<br>处理：「处理项目待办/按待办文档修复」| 统一 Inbox：收集所有类型反馈，激活时分类路由处理 |

### 五、代码库 & 架构分析

| Skill | 触发方式 | 做什么 |
|-------|---------|--------|
| **codebase-explorer** | 「阅读XXX项目/理解代码库/接手项目」| 扫描架构，与文档对比，输出架构理解文档 |
| **architecture-gap-mapper** | 「对比XXX和YYY/找差距/竞品分析」| 兼容/冲突/缺失三类差距报告，带代码证据 |

### 六、系统自我进化

| Skill / Agent | 触发方式 | 做什么 |
|--------------|---------|--------|
| **skill-capture-closure** | 「踩坑了/经验值得记/做个复盘/总结经验」| 单次经验沉淀：修改或新建 Skill/Rule/知识 |
| **project-retrospective** | 「项目做完了/更新Skill/批量复盘」| 批量复盘：扫描用到的所有 Skill，逐个沉淀 |
| **skill-updater（Agent）** | project-retrospective 调用 | 执行单条经验更新（备份+三问+变更记录）|
| **engineering-principle-recorder** | 「立一个原则/以后都要XXX/记下这条规则」| 将原则记录到正确执行层（Skill/Rule/约束文档）|
| **expert-bootstrap** | 「需要X领域专家/培养专家/没有X方面专家」| 调研→自问自答反思→产出专家 Agent 定义文件 |

### 七、内容创作

| Skill | 触发方式 | 做什么 |
|-------|---------|--------|
| **research-output** | 「调研/研究/系统了解/深度研究XXX」| 系统调研 → 图文 Markdown → 注册知识库 |
| **wechat-article-writer** | 「写公众号文章/他山推文」| 内容 → HTML排版 → 配图 → 底部模板 → 审稿 |
| **general-article-writer** | 「写技术文章/对外分享/通用长文」| Markdown 长文 + 审稿闭环 |
| **document-pipeline** | 「写一篇/有初稿/帮我配图/转HTML」| 全阶段写作流水线，可从任意阶段入场 |
| **article-proofreading** | 「审稿/检查这篇文章/review一下」| 检查 AI 腔/标题/绝对表达/结语 |

### 八、认知积累（适合研究者/知识工作者）

| Skill / Agent | 触发方式 | 做什么 |
|--------------|---------|--------|
| **cognitive-capture-fragment** | 「记录一下/有个洞见/我发现/随手记」| 捕捉 L2 认知碎片，结构化保存 |
| **cognitive-integrate-fragments** | 「整合碎片/处理积压/消化碎片」| 碎片整合进 L1 系统性文档 |
| **cognitive-extract-principle** | 「提炼原则/这些碎片有共性吗/总结规律」| 跨领域模式提炼为 L1.5 底层原则 |
| **cognitive-update-knowledge** | 「更新[文档名]/完善[文档名]」| 受控 L1 文档更新（备份+验证+级联）|
| **cognitive-ask** | 「基于我的文档/我之前怎么想的/从我的角度」| 按你的认知文档回答（带引用和置信度）|
| **cognitive-daily-briefing** | 「今天有什么/同步状态/今日简报」| 认知系统状态快照 + 积压提醒 |
| **cognitive-review-brain-map** | 「大脑地图/认知状态/看一下状态」| 全景认知结构图，帮助确定今日优先级 |
| **cognitive-self-reflect** | 「反思/我注意到我有个习惯/我又犯了」| 结构化自我反思，记录到反思日志 |
| **cognitive-detect-contradiction** | 「矛盾/不一致/检查一致性」| 找 L1 文档内部/之间的矛盾，提出消解方案 |
| **cognitive-consistency-check** | 「一致性检查/自洽检查/验证认知结构」| 运行 C1-C10 完整一致性验证 |
| **cognitive-input-classifier** | 「帮我判断这是认知更新还是任务执行/先分类」| 路由分类器：认知更新路径 vs 任务执行路径 |
| **cognitive-verifier（Agent）** | cognitive-update-knowledge 调用 | 独立验证 L1 文档更新的自洽性 |
| **cognitive-fragment-integrator（Agent）** | cognitive-integrate-fragments 调用（≥5碎片）| 从 L1 居民视角生成精确整合方案 |
| **cognitive-task-reflector（Agent）** | write-task-log 完成后自动调用 | 从任务日志中萃取认知价值，生成 L2 碎片候选 |
| **cognitive-cascade-notifier（Agent）** | 原则确认/L1重大更新后自动调用 | 后台分析工作节点，写入对齐待办 |

### 九、健康检查与系统维护

| Skill | 触发方式 | 做什么 |
|-------|---------|--------|
| **three-loop-health-check** | 「三大闭环健康/全系统健康报告/整体状态」| 三大闭环仪表盘（积压/沙盘/覆盖率）|
| **skill-system-health-check** | 「检查Skill体系/Skill健康/自检」| Skill/Rule/Agent 内部一致性审计 |
| **project-closeout** | 「项目收尾/做收尾检查/确保文档自洽」| 多角色文档审查 + 对话历史追踪 |
| **project-convention-resolver** | 「这里有个规范问题/这不符合规范」| 规范偏差分类 → 路由执行修复 → 验证 |
| **role-pm-auditor（Agent）** | project-closeout 调用 | 只读审查产品定义的完整性和一致性 |
| **role-arch-auditor（Agent）** | project-closeout 调用 | 只读审查技术架构与产品定义的对齐 |
| **role-dev-auditor（Agent）** | project-closeout 调用 | 只读审查开发计划与实际完成情况的对齐 |
| **product-evolution-planner** | 「产品还缺什么/迭代建议/从原则看产品」| 对照产品原则，识别缺口，生成战略建议 |
| **product-launch-validator** | 「新项目立项/立项前检查/兼容性检查」| 立项前验证与三大闭环的兼容性 |

### 十、Skill 体系设计与进化（元层）

| Skill / Agent | 触发方式 | 做什么 |
|--------------|---------|--------|
| **skill-rule-修改规范** | 「修改Skill/修改Rule/修改Agent/规范修改」| 修改任何 .cursor 组件的强制协议（三问+备份）|
| **skill-designer** | 「新建Skill/设计一个Skill/写个Agent」| 端到端 Skill/Rule/Agent 设计，含双视角审核 |
| **skill-evolution-planner-meta** | 「Skill体系怎么演进/有没有新Skill要建」| 基于历史数据规划 Skill 体系演进方向 |
| **skill-simulator（Agent）** | skill-designer 关卡A | 模拟第一次接触的 AI 执行者，找歧义和缺失分支 |
| **skill-system-destroyer（Agent）** | skill-designer 关卡B | 找新 Skill/Rule 与现有体系的冲突 |
| **skill-updater（Agent）** | project-retrospective | 执行单条更新（备份+三问+变更记录+索引更新）|
| **history-auditor** | 「审查历史对话/分析做过什么/找可沉淀的Skill」| 挖掘对话历史中的重复模式和 Skill 升级候选 |
| **cross-project-coordinator** | 「多项目并行/建协调框架/几个项目同时做」| 生成跨项目协调框架（项目地图/API契约/并行轨道）|

### 十一、数字分身（研究者画像管理）

| Skill | 触发方式 | 做什么 |
|-------|---------|--------|
| **collect-basic-info** | 「建立画像/收集基础信息」| 采集研究阶段、学科、方法等基础字段 |
| **administer-ams** | 「AMS/学术动机量表」| 施测 AMS-GSR 28题（动机测量）|
| **administer-mini-ipip** | 「人格/大五人格/Mini-IPIP」| 施测 Mini-IPIP 20题（大五人格）|
| **administer-rcss** | 「RCSS/认知风格量表/认知偏好」| 施测 RCSS 认知风格量表 |
| **infer-profile-dimensions** | 「推断画像/快速估算/不想填量表」| 无需量表，基于对话推断画像维度 |
| **update-profile** | 「修改画像/更新画像/补充」| 精准更新特定字段 |
| **review-profile** | 「查看画像/确认画像」| 完整画像审查工作流 |
| **generate-forum-profile** | 「生成论坛分身/数字分身/导出档案」| 导出四节式论坛分身 Markdown |

---

## 自动化说明：为什么「说一句话」就能做完

整套体系的自动化来自三层协作：

**第一层：Rule（始终在场的约束，每次对话自动注入）**
- `session-bootstrap`：定义了每次对话的「序列A（任务开始前做什么）」和「序列B（任务完成后做什么）」——这就是为什么 D5 信号可以自动路由
- `role-menu`：定义了所有触发词路由规则——这就是为什么说「做一个功能」就能启动协调者
- `comprehensive-change-guard`：多层变更时强制按序执行——这就是为什么关卡顺序不会乱

**第二层：Skill（按需加载的执行步骤）**
- 当触发词命中，对应 SKILL.md 被读入 context，AI 按步骤执行
- 每个 Skill 定义了完整的前置条件、步骤序列、完成标准

**第三层：SubAgent（独立 context 的视角隔离验证）**
- 所有关卡（A/B/C）都使用独立 SubAgent，`readonly=true`，看不到创作者的推理过程
- 这保证了「审核者不被创作者视角污染」

---

## 安装方式

### 方式一：`ai-agent-skills` CLI（推荐，一行命令）

```bash
# 安装到当前项目
npx ai-agent-skills install TashanGKD/tashan-cursor-skills

# 或安装到全局（所有项目可用）
npx ai-agent-skills install --global TashanGKD/tashan-cursor-skills
```

### 方式二：Cursor 内置 GitHub 导入

1. 打开 Cursor 设置（`Cmd+Shift+J`）
2. 进入 **Rules** → **Add Rule** → **Remote Rule (Github)**
3. 输入：`https://github.com/TashanGKD/tashan-cursor-skills`
4. 重启 Cursor

### 方式三：手动复制（完全控制）

```bash
git clone https://github.com/TashanGKD/tashan-cursor-skills.git

cp -r tashan-cursor-skills/skills/* your-project/.cursor/skills/
cp -r tashan-cursor-skills/rules/* your-project/.cursor/rules/
cp -r tashan-cursor-skills/agents/* your-project/.cursor/agents/
```

重启 Cursor，所有 Skill 和 Rule 自动生效。

---

## 代码结构

```
tashan-cursor-skills/
├── README.md / README.en.md     # 中英文说明（本文件）
├── CHANGELOG.md                 # 版本记录
├── CONTRIBUTING.md              # 贡献指南
├── docs/
│   ├── assets/tashan.svg        # 他山 Logo
│   ├── overview.md              # 完整系统说明
│   └── Skill体系设计原则_v1.0.md # 设计哲学
├── skills/                      # 95 个 Skills
│   ├── role-*/                  # 角色类 Skills（产品/架构/前端/后端/AI/测试/DevOps等）
│   ├── cognitive-*/             # 认知积累类 Skills
│   ├── bug-fix-loop-coordinator/ project-backlog/ expert-bootstrap/ # 辅助工作流
│   ├── skill-index/             # 体系索引（SKILL-INDEX.md）
│   └── ...
├── rules/                       # 32 个 Rules（.mdc，自动注入 system prompt）
│   ├── session-bootstrap.mdc   # ★ 核心：每次对话执行协议
│   ├── role-menu.mdc           # ★ 核心：触发词路由表
│   ├── bug-fix-tdd-guard.mdc   # 强制 TDD 修复流程
│   └── ...
└── agents/                      # 18 个 SubAgents（独立 context 验证）
    ├── verifier.md / fixer.md  # 关卡验证 + 修复执行
    ├── user-simulator.md / arch-destroyer.md # 关卡A/B
    └── cognitive-*.md           # 认知处理子智能体
```

---

## 生态位置

```
他山生态
├── Resonnet / tashan-openbrain  ← 多智能体认知协作平台
├── Tashan-TopicLab              ← 多专家圆桌讨论
├── tashan-cursor-skills ★      ← 本仓库：AI 执行规范体系
└── world-axiom-framework        ← 数字世界公理框架（理论基础）
```

### 相关仓库

| 仓库 | 定位 | 链接 |
|------|------|------|
| Resonnet | 多智能体认知协作后端 | [TashanGKD/Resonnet](https://github.com/TashanGKD/Resonnet) |
| Tashan-TopicLab | 多专家圆桌讨论平台 | [TashanGKD/Tashan-TopicLab](https://github.com/TashanGKD/Tashan-TopicLab) |
| world-axiom-framework | 数字世界公理框架 | [TashanGKD/world-axiom-framework](https://github.com/TashanGKD/world-axiom-framework) |

---

## 贡献

详见 [CONTRIBUTING.md](CONTRIBUTING.md)。修改任何 Skill/Rule/Agent 前，必须先读 `skills/skill-rule-修改规范/SKILL.md`（三问协议）。

---

## 更新日志

见 [CHANGELOG.md](CHANGELOG.md)。

---

## 许可证

MIT License. See [LICENSE](LICENSE) for details.
