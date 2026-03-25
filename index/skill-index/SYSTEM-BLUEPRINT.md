# Skill 体系系统蓝图

> 版本：v1.0 | 日期：2026-03-19
> 性质：基于全量历史对话（92条）+ 现有 Skill/Agent/Rule 系统的综合分析
> 目的：识别所有任务类型、闭环结构、Skill 缺口，设计子智能体编排完整方案

---

## 一、郑总核心工作模式分析

从 92 条历史对话中提炼出 7 种核心工作模式：

### 模式1：代码库探索与架构理解
**频率**：最高（~20次）  
**触发**：接手新项目、评估竞品、理解已有代码  
**典型语句**：「阅读XXX项目，理解代码结构，写技术架构文档」  
**完整闭环**：
```
接触新代码库
  → 全量扫描目录和文件结构
  → 理解核心模块和依赖关系
  → 提取架构模式（前后端/数据/AI层）
  → 与产品定义/需求对比（差距分析）
  → 输出技术架构文档 or 理解报告
```
**当前状态**：❌ 无正式 Skill，每次凭 AI 经验执行

---

### 模式2：产品开发全链路
**频率**：高（每个项目必经）  
**触发**：新产品开发、功能迭代  
**典型语句**：「写[产品]的注册接口」「测试刚写完的功能」「部署到服务器」  
**完整闭环**：
```
产品方向确定
  → PM 设计产品定义（闭环递进法）
  → 关卡A 用户模拟审核（user-simulator）
  → 技术架构师设计系统架构
  → 关卡B 系统破坏审核（arch-destroyer）
  → UI设计师设计界面（ux-reviewer 审核）
  → 前端/后端/AI工程师实现
  → 关卡C 独立验证（verifier）
  → DevOps 部署上线
  → 数据分析师追踪闭环完成率
  → 问题反馈回 PM → 新一轮迭代
```
**当前状态**：✅ 全链路 Skill 覆盖，已有子智能体化审核

---

### 模式3：认知结构管理
**频率**：中（~8次，持续性）  
**触发**：产生新想法、整理思绪、做决策  
**典型语句**：「记录一下这个想法」「整合碎片」「基于我的文档回答」  
**完整闭环**：
```
产生碎片化思考
  → cognitive-capture-fragment 写入L2
  → 积累到一定量 → cognitive-integrate-fragments 整合进L1
  → 跨碎片发现规律 → cognitive-extract-principle 提炼L1.5原则
  → L1.5 原则约束所有L1文档写入
  → cognitive-ask 基于认知库回答问题
  → cognitive-daily-briefing 每日同步状态
  → cognitive-detect-contradiction 检查一致性
```
**当前状态**：✅ 完整 Skill 覆盖，Rule 体系完善

---

### 模式4：科研数字分身构建
**频率**：中（完整流程执行1-2次，迭代多次）  
**触发**：建立科研人员画像，供他山论坛/AI工具使用  
**典型语句**：「建立数字分身」「填量表」「生成论坛分身」  
**完整闭环**：
```
采集基础信息（collect-basic-info）
  → 施测量表（AMS/Mini-IPIP/RCSS）或推断（infer-profile-dimensions）
  → 导入AI记忆（import-ai-memory）
  → 审核画像（review-profile）
  → 修改/完善（update-profile）
  → 输出论坛分身（generate-forum-profile）
  → 生成AI记忆提示词（generate-ai-memory-prompt）
  → 持续迭代（update-profile）
```
**当前状态**：✅ 全链路 Skill 覆盖

---

### 模式5：Skill 体系自我进化
**频率**：新模式（今日建立）  
**触发**：完成任务、发现踩坑、建设新机制  
**完整闭环**：
```
任务执行中
  → auto-experience-hook → PENDING-EXPERIENCES（结果层）
  → co-build-log → CO-BUILD-LOG（过程层）
  ↓
任务完成确认
  → project-retrospective 读取三路来源
  → 展示清单 → 用户确认
  → skill-updater 串行写入 Skill
  → skill-rule-修改规范 执行备份+变更记录
  → SKILL-INDEX 同步更新
```
**当前状态**：✅ 今日完整建立

---

### 模式6：内容抓取与分析
**频率**：低（~3次）  
**触发**：需要批量获取外部内容（公众号/RSS/学术论文）  
**典型语句**：「抓取他山公众号文章」「分析排版规范」  
**完整闭环**：
```
确定内容来源（公众号/RSS/学术库）
  → wechat-scraper / RSS抓取 → 本地存储
  → LLM 多维度分析（格式/主题/风格）
  → 提炼规范/洞察输出
```
**当前状态**：🟡 wechat-scraper 子智能体已建，分析部分无正式 Skill

---

### 模式7：文章/内容写作与审稿
**频率**：中（周期性）  
**触发**：写微信公众号文章、审稿  
**完整闭环**：
```
确定主题和写作意图
  → 写作草稿（参考写作手册）
  → article-proofreading 审稿（AI腔/标题/绝对表达检查）
  → 修改定稿
  → 排版发布
```
**当前状态**：🟡 article-proofreading Skill 已建，写作部分无正式 Skill

---

## 二、全量任务类型分类

### 2.1 已有完整 Skill 覆盖的任务

| 任务类型 | 覆盖 Skill | 审核子智能体 |
|---|---|---|
| 产品定义设计 | role-产品经理 | user-simulator（关卡A）|
| 技术架构设计 | role-技术架构师 | arch-destroyer（关卡B）|
| 前端开发 | role-前端开发 | verifier（关卡C）|
| 后端开发 | role-后端开发 | verifier（关卡C）|
| AI工程 | role-AI工程师 | ai-evaluator |
| UI设计 | role-UI设计师 | ux-reviewer |
| 测试验收 | role-测试工程师 | verifier |
| 部署上线 | role-DevOps | — |
| 数据分析 | role-数据分析师 | — |
| 问题追踪 | issue-tracker | — |
| 认知碎片捕捉 | cognitive-capture-fragment | — |
| 认知知识整合 | cognitive-integrate-fragments | — |
| 认知问答 | cognitive-ask | — |
| 认知每日汇报 | cognitive-daily-briefing | — |
| 原则提炼 | cognitive-extract-principle | — |
| 矛盾检测 | cognitive-detect-contradiction | — |
| 自我反思 | cognitive-self-reflect | — |
| 画像采集 | collect-basic-info + 量表 Skills | — |
| 画像更新 | update-profile | — |
| 论坛分身生成 | generate-forum-profile | — |
| 文章审稿 | article-proofreading | — |
| Skill 修改 | skill-rule-修改规范 | — |
| 项目复盘 | project-retrospective + skill-updater | — |

### 2.2 缺乏正式 Skill 的高频任务（缺口清单）

| 任务类型 | 频率 | 重要性 | 推荐 Skill 名 |
|---|---|---|---|
| **代码库探索与架构文档生成** | 最高（~20次）| 🔴 极高 | `codebase-explorer` |
| **新项目骨架初始化** | 高（每项目1次）| 🔴 极高 | `project-bootstrap` |
| **学术论文阅读与摘要** | 中（~5次）| 🟠 高 | `paper-reader` |
| **竞品/同类项目对比分析** | 中（~5次）| 🟠 高 | `competitive-analysis` |
| **微信公众号文章分析** | 中（~3次）| 🟡 中 | `content-analyzer` |
| **公司运营文档管理** | 低（~2次）| 🟡 中 | `company-ops` |
| **写作（非审稿）** | 低（但周期性）| 🟡 中 | `article-writer` |
| **工作区/文件整理** | 低（~3次）| 🟢 低 | `workspace-organizer` |

---

## 三、缺口 Skill 详细设计

### 3.1 codebase-explorer（代码库探索）
**触发词**：「阅读XXX项目」「理解这个代码库」「写技术架构文档」「这个项目是做什么的」

**完整闭环**：
```
Step 1  用 explore 子智能体扫描目录结构
Step 2  识别技术栈（前/后端/AI/DB/基础设施）
Step 3  读核心文件（README/主入口/配置/核心模块）
Step 4  提取架构模式
Step 5  与产品定义/需求对比（若存在）
Step 6  输出：技术架构文档 + 关键设计决策 + 与需求的差距
```

**子智能体设计**：
- `explore` 内置子智能体：并行扫描目录
- `verifier` 复用：验证生成的文档是否准确

---

### 3.2 project-bootstrap（新项目骨架初始化）
**触发词**：「新建项目」「初始化项目」「从零开始一个新项目」

**完整闭环**：
```
Step 1  确认项目类型（全栈/纯后端/纯前端/AI服务等）
Step 2  创建标准目录结构
Step 3  复制开发规范.md 并定制
Step 4  初始化 README.md、DEPLOY_ARCH.md
Step 5  创建产品经理/技术架构师/等空目录
Step 6  初始化 git 仓库 + .gitignore
Step 7  更新 _内部总控/项目索引.md
```

**子智能体设计**：
- `bash` 内置子智能体：执行文件创建命令

---

### 3.3 paper-reader（学术论文阅读）
**触发词**：「阅读这篇论文」「理解这篇文章」「总结这个研究」

**完整闭环**：
```
Step 1  识别论文类型（实验/理论/综述/方法论）
Step 2  提取：核心问题 + 方法 + 结论 + 局限
Step 3  关联到郑总现有认知结构（是否有对应L1/L2）
Step 4  输出结构化摘要
Step 5  触发 cognitive-capture-fragment 记录关键洞见
```

---

### 3.4 competitive-analysis（竞品对比分析）
**触发词**：「对比XXX和YYY」「这两个项目有什么异同」「XXX的本质局限是什么」

**完整闭环**：
```
Step 1  读取两个代码库/产品描述
Step 2  按维度对比：技术架构/产品功能/用户体验/商业模式
Step 3  识别本质局限（不是「功能不够好」而是「设计哲学的根本差异」）
Step 4  输出对比矩阵 + 战略洞察
```

**子智能体设计**：
- 两个并行的 `explore` 子智能体分别扫描两个代码库
- 主 Agent 做综合对比分析

---

## 四、完整闭环映射

### 4.1 产品开发大闭环（核心，已完整）

```
战略方向
  ↓
role-产品经理 → 产品定义.md
  ↓ 关卡A
user-simulator（子智能体）
  ↓
role-技术架构师 → 技术架构.md
  ↓ 关卡B
arch-destroyer（子智能体）
  ↓
role-UI设计师 → 设计稿
  ↓ UI审核
ux-reviewer（子智能体）
  ↓
[role-前端开发 ‖ role-后端开发 ‖ role-AI工程师] ← 并行
  ↓ 关卡C
verifier（子智能体）
  ↓
role-测试工程师
  ↓
role-DevOps → 生产环境
  ↓
role-数据分析师 → 闭环完成率 → 反馈回PM
  ↓
新一轮迭代
```

### 4.2 认知结构大闭环（完整）

```
日常工作/思考
  ↓
cognitive-capture-fragment → L2碎片
  ↓ 积累到阈值
cognitive-integrate-fragments → L1文档
  ↓
cognitive-extract-principle → L1.5原则
  ↓ 原则约束所有写入（Rule: cognitive-principle-check）
  ↓
cognitive-ask 使用认知库 → 回答问题/做决策
  ↓
cognitive-daily-briefing → 状态同步
  ↓
下一轮思考产生新碎片
```

### 4.3 Skill 进化大闭环（今日建立，完整）

```
任务执行中
  ↓ [自动]
experience-logger（后台）→ PENDING-EXPERIENCES（结果层）
co-build-logger（后台）→ CO-BUILD-LOG（过程层）
  ↓
用户确认「做项目复盘」
  ↓
project-retrospective：三路输入合并 → 待处理清单 → 用户确认
  ↓ 串行
skill-updater（子智能体）× N 条经验
  ↓ 每条经验
skill-rule-修改规范（三问+备份+变更记录）
  ↓
SKILL-INDEX.md 同步更新
  ↓
下一次任务使用更好的 Skill
```

### 4.4 内容生产大闭环（半覆盖）

```
确定内容主题
  ↓ [缺 article-writer Skill]
写作草稿（参考写作手册/排版规范）
  ↓
article-proofreading → 审稿报告
  ↓
修改定稿
  ↓ [缺排版发布自动化]
微信排版 → 发布
  ↓
数据追踪（阅读量/互动）← 待建立
```

### 4.5 代码库理解闭环（缺 Skill）

```
接触新代码库
  ↓ [缺 codebase-explorer Skill]
explore 子智能体并行扫描
  ↓
架构文档生成
  ↓
与产品定义对比（差距分析）
  ↓
技术方案建议
```

---

## 五、子智能体编排完整蓝图

### 5.1 现有子智能体（9个）

| 子智能体 | 模式 | 模型 | 调用场景 |
|---|---|---|---|
| experience-logger | 后台 | fast | 任务中感知踩坑/发现时自动触发 |
| co-build-logger | 后台 | fast | 协作建设任务中感知关键决策点时自动触发 |
| skill-updater | 前台串行 | inherit | project-retrospective Step 4，每条经验一次 |
| user-simulator | 前台只读 | inherit | 关卡A：产品定义完成后 |
| arch-destroyer | 前台只读 | inherit | 关卡B：技术架构完成后 |
| verifier | 前台只读 | inherit | 关卡C：代码完成后 |
| ux-reviewer | 前台只读 | inherit | UI设计审核 |
| ai-evaluator | 前台只读 | inherit | AI工程师效果评测 |
| wechat-scraper | 前台 | inherit | 微信公众号文章抓取 |

### 5.2 建议新增子智能体（基于缺口分析）

| 子智能体 | 模式 | 模型 | 设计说明 |
|---|---|---|---|
| `codebase-scanner` | 前台 | fast | 并行扫描代码目录，提取模块结构和依赖关系，供 codebase-explorer Skill 调用 |
| `paper-summarizer` | 前台只读 | inherit | 学术论文结构化提取（问题/方法/结论/局限），供 paper-reader Skill 调用 |
| `project-initializer` | 前台 | fast | 创建标准项目目录骨架，供 project-bootstrap Skill 调用 |

### 5.3 完整编排架构图

```
╔══════════════════════════════════════════════════════════════╗
║                    郑总的工作意图                              ║
╚══════════════════════════════════════════════════════════════╝
                           ↓
╔══════════════════════════════════════════════════════════════╗
║                  主对话（主 Agent）                           ║
║  role-menu.mdc 路由 → 加载对应 Skill                         ║
╚══════════════════════════════════════════════════════════════╝
         ↓                    ↓                    ↓
╔═══════════════╗   ╔═══════════════╗   ╔══════════════════╗
║  产品开发流    ║   ║  认知结构流   ║   ║  Skill进化流     ║
╠═══════════════╣   ╠═══════════════╣   ╠══════════════════╣
║ PM            ║   ║ capture-frag  ║   ║ auto-experience  ║
║ ↓关卡A        ║   ║ ↓             ║   ║ co-build-log     ║
║ user-sim(子)  ║   ║ integrate     ║   ║ ↓                ║
║ ↓             ║   ║ ↓             ║   ║ project-retro    ║
║ 架构师        ║   ║ extract-princ ║   ║ ↓                ║
║ ↓关卡B        ║   ║ ↓             ║   ║ skill-updater(子)║
║ arch-des(子)  ║   ║ cognitive-ask ║   ╚══════════════════╝
║ ↓             ║   ╚═══════════════╝
║ UI设计师      ║
║ ↓UI审核       ║
║ ux-rev(子)    ║
║ ↓             ║
║ [并行开发]    ║
║ 前端‖后端‖AI  ║
║ ↓关卡C        ║
║ verifier(子)  ║
║ ↓             ║
║ 测试工程师    ║
║ ↓             ║
║ DevOps        ║
║ ↓             ║
║ 数据分析师    ║
╚═══════════════╝

后台自动运行（不占主对话 context）：
  experience-logger  → PENDING-EXPERIENCES
  co-build-logger    → CO-BUILD-LOG
  
内置子智能体（Cursor 自动调用）：
  explore   → 代码库/文档扫描
  bash      → 命令执行
  browser   → 浏览器自动化
```

---

## 六、郑总核心反馈模式总结

从历史对话中提炼出郑总的核心反馈规律：

### 6.1 产品设计反馈
- **「先从人性/马斯洛出发，再谈产品」** → 已内化为 role-产品经理 的第一性原理
- **「AI时代双层设计：人层体验+智能体层接口」** → 已内化为所有 Skill 的设计原则
- **「闭环完整性优先于功能丰富性」** → 已内化为 role-产品经理 的第一性原理
- **「体验感先于功能」** → 已内化为 role-UI设计师 的核心原则

### 6.2 执行质量反馈
- **「沙盘推演，看有没有问题」** → 导致了关卡A/B/C 子智能体化的设计
- **「严格按规范执行」** → 形成了 skill-rule-修改规范 的三问+备份+变更记录体系
- **「先备份再改」** → 已成为所有 Skill 修改的强制要求
- **「最小化修改原则」** → 已内化为 skill-rule-修改规范

### 6.3 上下文管理反馈
- **「上下文释放问题」** → 导致了子智能体化策略（隔离上下文）
- **「失败重试的 context 污染」** → 导致了 wechat-scraper 等任务型子智能体
- **「过程中存入，完成后确认」** → 导致了 co-build-log 机制

### 6.4 知识沉淀反馈
- **「像认知结构一样管理 Skill」** → 导致了 SKILL-INDEX + skill-capture-closure 设计
- **「跑通闭环就沉淀，出现问题就更新」** → 导致了 project-retrospective + skill-updater
- **「记录过程，不只记录结果」** → 导致了 co-build-log 机制

---

## 七、下一步建议

### 短期（下次项目开始前）
1. **建立 `codebase-explorer` Skill**（最高优先级，使用最频繁）
2. **建立 `project-bootstrap` Skill**（每个项目都需要）
3. **更新 `role-menu.mdc`**，注册新增 Skill 的触发词

### 中期（1-2个项目后）
4. **建立 `competitive-analysis` Skill**
5. **建立 `paper-reader` Skill**
6. **完善内容生产闭环**（article-writer + 排版发布）

### 长期
7. **数据飞轮**：通过 CO-BUILD-LOG 积累足够的协作建设过程记录，定期提炼为新 Skill 设计模式
8. **跨项目 Skill 同步**：当个人级 Skill 在项目实践中被验证后，提炼为项目级 Skill

---

## 八、关键发现：三个「一直存在但从未被命名」的任务类型

这是从历史对话中发现的三个高频却从未被正式命名的工作模式，建议优先建立 Skill：

### 类型A：「接手已有代码库，快速理解并推进」
这是郑总最常做的事——接触一个新代码库（可能是自己的旧项目、参考项目、竞品），快速理解它，然后决定是「继续开发」「参考学习」还是「评估差距」。目前每次都是 AI 从零开始，没有标准流程。

### 类型B：「高密度产品思考，发散后收敛」
多次出现相同的第一条消息（AI-native三判断），说明郑总有一种「产品思考模式」：先提出几个底层判断，然后想把这些判断用来分析具体行业/产品。这个模式需要一个「产品思维工具」Skill，不是 role-产品经理（那是执行层），而是更上层的思维框架应用层。

### 类型C：「认知迁移：把一个领域的洞见应用到另一个领域」
「基于认知结构回答：可以如何把AI用到音乐行业」这类问题，本质是认知迁移（cross-domain transfer）。目前 cognitive-ask Skill 勉强能做，但没有专门针对「用我的框架分析新领域」的引导流程。

---

*本文档将随每次项目复盘持续更新。下次更新时间：下一个项目完成后。*
