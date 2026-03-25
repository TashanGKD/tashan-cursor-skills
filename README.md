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
  <a href="#用户工作流指南">工作流指南</a> •
  <a href="#完整-skill-速查">Skill 速查</a> •
  <a href="#安装方式">安装</a> •
  <a href="#代码结构">代码结构</a> •
  <a href="#生态位置">生态位置</a> •
  <a href="#贡献">贡献</a> •
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

## 用户工作流指南

> 这是本文档最重要的部分。理解以下工作流，你就理解了整个体系。

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
