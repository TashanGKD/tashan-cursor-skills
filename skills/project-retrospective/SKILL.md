---
name: project-retrospective
description: 项目级 Skill 批量复盘。在一个项目/任务闭环完成后，主动扫描本次对话中调用过的所有 Skill，逐个判断是否需要新建或更新，批量调用 skill-capture-closure 完成沉淀，最后输出复盘报告。触发词：「项目做完了」「更新一下Skill」「基于刚刚的过程更新规范」「做个项目复盘」「沉淀一下经验」「把这次的经验记下来」。
---

# 项目级 Skill 复盘（project-retrospective）

> 单次经验用 `skill-capture-closure`（随时触发）。
> 项目结束后的系统性批量复盘用本 Skill（一次扫描全部）。
> 本 Skill 是外壳，`skill-capture-closure` 是内核——扫描由本 Skill 负责，每个具体更新动作仍走 `skill-capture-closure` 标准流程。

---

## 知识导航表（执行前必须理解的概念根）

> 本 Skill 的步骤设计基于以下文档的核心概念。若不理解这些概念，步骤无法正确执行。

| 层级 | 文档 | 需要理解的概念 |
|---|---|---|
| **D0 认知根（必读）** | `_内部总控/认知结构/L1_系统性文档/系统架构思维维度/自进化智能体系统形式规范_v1.0.md` | 层1：B/K/S三类对象；层2：间隙（Gap）定义；层5：R/M/G基础设施 + M的批量处理逻辑；层7：D_op = {create, modify, delete, merge, split} |
| **D3 规范参考** | `_内部总控/认知结构/L1_系统性文档/系统架构思维维度/Skill体系设计原则_v1.0.md` | §2.5 三型决策树（判断新建 Rule/Agent/Skill）；§2.2/2.3/2.4 各类型本质 |
| **D4 运行时数据** | `.cursor/skills/skill-index/PENDING-EXPERIENCES.md` + `CO-BUILD-LOG.md` + `SKILL-INDEX.md` | G缓冲区（待处理Gap）+ 过程决策日志 + B-objects 注册表 |

**核心概念速查**：
① B-object（行为对象）= Skill/Rule/Agent，编码「在条件C下执行动作A」
② K-object（知识对象）= 所有文档，编码「什么是真的」
③ D_op = modify（修复已有）vs create（沉淀新建）—— 批量复盘需同时处理两类

---

## 激活后立即执行（顺序不可跳过）

```
Step 1  读取 Skill 总索引，了解所有现有 Skill
        Read: .cursor/skills/skill-index/SKILL-INDEX.md
        → 获取全量 Skill 列表，用于后续匹配

Step 2  获取「Skill 相关事件」清单（三路来源合并）
        
        【来源一：读取暂存文件（优先，已由 auto-experience-hook 自动积累）】
        Read: .cursor/skills/skill-index/PENDING-EXPERIENCES.md
        → 提取所有「🔲 待处理」条目
        → 捕捉：任务中的踩坑/新发现/步骤偏差（结果层）
        
        【来源二：读取协作建设日志（co-build-log 积累的决策轨迹）】
        Read: .cursor/skills/skill-index/CO-BUILD-LOG.md
        → 提取「待处理日志条目」区域的所有条目
        → 捕捉：任务中的推理链/决策轨迹/转折理由（过程层）
        → 重点关注类型 II（方案）和 III（转折）——这是提炼 Skill 的最高价值来源
        → 若文件不存在或无条目，跳过
        
        【来源三：补充扫描本次对话上下文（兜底，捕捉两个文件的遗漏）】
        回溯整个对话，识别以下信号（排除已在前两路中的条目，避免重复）：
        
        【A. 调用了某个 Skill 且执行顺利】
           → 候选：状态升级为 ✅ 已验证（如果原来是 🔵 待验证）
        【B. 调用了某个 Skill 但执行有偏差/需要补充步骤】
           → 候选：更新该 Skill 的内容（修复/补充）
        【C. 遇到了某个场景，但没有合适的 Skill 覆盖，AI 凭感觉执行】
           → 候选：新建 Skill（Level 2）
        【D. 某个 Skill 的触发词不准（该触发没触发，或错误触发）】
           → 候选：更新 description 字段
        【E. 架构级发现（系统层面改进，不只是单个 Skill）】
           → 以下情况标为 E 类，不走 skill-updater，走 skill-designer 或规范修改流程：
           E1. AI 行为规律性不符预期，根因不在某个 Skill 的步骤里，需要新建 Rule
               → 候选：新建 alwaysApply Rule（.cursor/rules/）
           E1b. 已有 Rule 存在歧义/覆盖范围错误/需要修订
               → 候选：更新已有 Rule（走 skill-rule-修改规范）
           E2. 某类任务因上下文污染导致质量不稳定，子智能体隔离不够，需要新建
               → 候选：新建独立子智能体（.cursor/agents/）
           E2b. 已有 Agent 有设计缺陷/行为错误/描述不准确
               → 候选：更新已有 Agent（走 skill-rule-修改规范 Agent 分支）
           E3. 两个或多个 Skill/Agent/Rule 协作时有系统性摩擦或冲突
               → 候选：Level 3 集成型改造（走 skill-designer + 关卡A/B/C）
           E4. 需要重构多个组件的交互关系
               → 候选：Level 4 系统型调整（走 skill-designer 完整八步）
           E5. 发现某份规范/参考文档（非 .cursor/ 组件）内容有误、遗漏、需补充
               → 候选：更新规范文档（走 project-doc-versioning-guard 四步留痕）
               覆盖：开发规范手册 / 项目测试规范 / 技术架构文档 / 任何 _内部总控/开发规范/*.md 等
           E6. 【结构性设计问题】——AI 反复失败，但根因不是执行疏忽，而是规范/机制本身设计有缺陷
               判断标准（满足任一）：
               ① 同类失败出现 ≥2 次，且每次复盘结论都是「AI 疏忽」
               ② 规范只在 Skill 里（被触发才生效），但该规范需要普遍约束
               ③ 重要文档/规范没有进入任何 D0 / alwaysApply Rule，AI 靠记忆才知道
               ④ 规范表述是「建议/应该」，实际需要「禁止/必须」级别的强制
               ⑤ 某个正确做法需要 AI 主动记住，而不是被机制强制
               → 候选：根据具体缺陷类型路由
               → 连接缺口 → 补 D0 / 新建 Rule（路径③）
               → 类型错误（Skill→Rule）→ 新建 alwaysApply Rule（路径③）
               → 规范质量 → 更新规范文档（路径⑦）
               → 执行力度 → 修改 Rule/Skill 的约束强度（路径⑥）
        
        → 将三路来源合并为一张完整清单，标注每条的类别（A/B/C/D/E）

Step 3  输出「待处理清单」，等用户确认
        格式：
        「本次项目系统复盘扫描结果：

          📋 Skill 更新类（A/B/C/D，走 skill-updater 路径）：
          ① [Skill目录名] — [类型] — [一句话说明]
          ② ...

          🏗️ 架构级改进类（E，按子类走不同路径）：
          ① [改进名称] — [E1/E1b/E2/E2b/E3/E4/E5] — [一句话说明]
          ② ...

          ⓪ 无需处理（执行符合预期）：[列表]

          说明：
          - A/B/C/D 类：直接由 skill-updater 子智能体处理（快，无关卡）
          - E1/E2（新建Rule/Agent）：走 skill-designer Level 2 流程（含关卡A+C）
          - E1b/E2b（更新已有Rule/Agent）：走 skill-rule-修改规范（三问+备份+修改）
          - E3（多组件集成）：走 skill-designer Level 3（含关卡A+B+C）
          - E4（系统重构）：暂停，用户决策后开专题会话
          - E5（规范文档）：走 project-doc-versioning-guard 四步留痕（快，无关卡）
          - E6（结构性设计问题）：先诊断具体缺陷类型，再按连接缺口→③ / 类型错误→③ / 规范质量→⑦ / 执行力度→⑥ 分流

          请确认：[全部处理] [只处理Skill更新类] [只处理架构类] [跳过某项]」

        → 等用户确认后继续

Step 4  生成本次复盘的 ClosureCase 快照（13态状态机，显式追踪）
        
        创建文件：.cursor/skills/skill-index/closure-case-YYYYMMDD.yaml
        内容（状态机来自 user_global_rules_v1 闭环元模型）：
        
        case_id: "project-retrospective-[日期]"
        goal: "本次复盘的目标"
        
        # 13态状态机（NEW→NORMALIZED→CONSTRAINED→PLANNED→RUNNING→
        #              WAITING_CHILDREN→MERGING→VERIFYING→QA_PENDING→
        #              DONE / BLOCKED / ESCALATED / ARCHIVED）
        status: "PLANNED"
        
        source_of_truth: ".cursor/skills/skill-index/SKILL-INDEX.md"
        current_stage: "implementation"   # context|model|plan|implementation|verification|delivery
        
        active_branches: [每个待处理 Skill 一个 branch_id]
        closed_branches: []
        repair_branches: []               # 验证失败后产生的 repair 分支
        artifacts: []
        
        acceptance_criteria:
          - "所有 🔲 待处理条目已处理"
          - "SKILL-INDEX 已同步更新"
          - "PENDING-EXPERIENCES 和 CO-BUILD-LOG 已清理"
          - "所有 repair_branches 已完成或已升级"
          - "QA 通过（无活动分支，无未解决冲突）"
        
        # 递归保护（来自 agent-io-contract.md）
        recursion_depth: 0
        branch_policy:
          max_children: 10              # 每次复盘最多10个并发 Skill 更新分支
          allowed: true
        escalation_policy:
          max_depth: 2
          escalate_on_block: true
        
        owner: "orchestrator"

Step 5  按条目类型路由分发处理（串行，A/B/C/D 与 E 类走不同路径）

        【路由规则（每条条目必须先判断类型再执行）】
        
        A/B/D 类（更新已有 Skill）→ 路径①：skill-updater 子智能体
        C 类（新建独立 Skill，Level 2）→ 路径②：skill-designer Level 2 流程
        E1 类（新建 Rule）→ 路径③：skill-designer Level 2 流程（创建 .cursor/rules/）
        E2 类（新建 Agent）→ 路径③：skill-designer Level 2 流程（创建 .cursor/agents/）
        E1b 类（更新已有 Rule）→ 路径⑥：skill-rule-修改规范（三问+备份+修改+变更记录）
        E2b 类（更新已有 Agent）→ 路径⑥：skill-rule-修改规范 Agent 分支（备份到 agents/history/）
        E3 类（多组件集成改造，Level 3）→ 路径④：skill-designer Level 3 流程（含关卡A+B+C）
        E4 类（系统重构，Level 4）→ 路径⑤：暂停，向用户确认规模后再执行
        E5 类（规范/参考文档更新）→ 路径⑦：project-doc-versioning-guard 四步（读版本→备份→修改→变更记录）
        E6 类（结构性设计问题）→ 先在 Step 5 内做二次分类，再按缺陷类型路由：
               · 连接缺口（缺 D0/Rule）→ 路径③（新建 Rule，skill-designer Level 2）
               · 类型错误（Skill→Rule）→ 路径③（新建 alwaysApply Rule）
               · 规范质量（表述歧义/覆盖错误）→ 路径⑦（更新规范文档）
               · 执行力度（建议→禁止）→ 路径⑥（修改已有 Rule/Skill 约束强度）
        
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        【路径①：A/B/D 类 → skill-updater（串行，快速）】
        
        a. 明确宣告：「▶ 正在处理 [N/总数]：[Skill目录名] — [类型]（路径①）」
        
        b. 构造统一任务信封（参见 skill-designer/agent-io-contract.md）：
           task_id / case_id / branch_id / goal / scope /
           allowed_write_set / done_criteria / recursion_depth: 0
        
        c. 调用 /skill-updater，等待完成
        
        d. 解析输出：pass → 移入 closed_branches；fail → 创建 repair branch
        
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        【路径②③：C/E1/E2 类 → skill-designer Level 2（含关卡A + 关卡C）】
        
        a. 明确宣告：「▶ 正在处理 [N/总数]：[组件名] — [类型]（路径②/③，走 skill-designer）」
        
        b. 加载 skill-designer Skill，传入：
           - 需要创建的组件类型（Skill / Rule / Agent）
           - 来自复盘清单的需求描述
           - 当前 SKILL-INDEX 摘要
        
        c. skill-designer 走完 Step 3-7（双视角产品定义 → 编写 → 关卡A → 关卡C）
        
        d. 通过后由 skill-designer 执行 Step 8（部署）
        
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        【路径④：E3 类 → skill-designer Level 3（含关卡A + B + C）】
        
        a. 明确宣告：「▶ 正在处理 [N/总数]：[改进名称] — E3（路径④，Level 3，含关卡B）」
        
        b. 加载 skill-designer Skill，Level 3 完整流程（Step 3-8）
        
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        【路径⑥：E1b/E2b 类 → skill-rule-修改规范（更新已有 Rule 或 Agent）】

        a. 明确宣告：「▶ 正在处理 [N/总数]：[组件名] — [E1b/E2b]（路径⑥，更新已有组件）」

        b. 执行 skill-rule-修改规范 完整流程：
           - 修改前三问（根因/影响/验证）
           - 备份：Rule → .cursor/rules/history/ / Agent → .cursor/agents/history/
           - 最小化修改
           - 追加变更记录

        c. 更新 SKILL-INDEX（若 Rule/Agent 在索引中有条目）

        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        【路径⑦：E5 类 → project-doc-versioning-guard（更新规范/参考文档）】

        a. 明确宣告：「▶ 正在处理 [N/总数]：[文档名] — E5（路径⑦，更新规范文档）」

        b. 执行 project-doc-versioning-guard 四步留痕：
           1. Read 文件头部 → 获取当前版本号
           2. cp 备份 → [所在目录]/history/[文件名]_v[版本]_YYYYMMDD.md
           3. 最小化修改（只改本次经验相关部分）
           4. 追加变更记录到文档末尾

        c. 本路径无需 skill-updater，主 Agent 直接执行

        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        【路径⑤：E4 类 → 暂停，用户决策】
        
        a. 输出：「⚠️ 发现 Level 4 系统型调整：[描述]
                  这将影响多个现有组件，建议开一个专门会话处理。
                  是否现在开始，还是加入 PENDING-SKILLS 后续规划？」
        
        b. 等待用户决策，不自行启动
        
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        所有条目处理完后，若有 repair branch，按原路径串行处理

Step 6  输出复盘报告，更新 ClosureCase，清理暂存区
        「📊 项目系统复盘完成

          Skill 更新（路径①）：
          ✅ 更新已有 Skill：N 个（含版本升级）
          ✅ 状态升级：N 个（🔵→✅）
          🔧 repair 处理：N 个

          架构级改进（路径②③④⑥⑦）：
          ✅ 新建 Skill（Level 2）：N 个
          ✅ 新建 Rule：N 个
          ✅ 更新已有 Rule：N 个
          ✅ 新建 Agent：N 个
          ✅ 更新已有 Agent：N 个
          ✅ Level 3 集成改造：N 个
          ✅ 更新规范/参考文档：N 个

          待后续处理（路径⑤）：
          📋 Level 4 系统调整：N 个（已加入 PENDING-SKILLS）

          ⏭ 跳过：N 个
          Skill 体系健康度：共 N 个，✅ X 个已验证，🔵 Y 个待验证」
        
        更新 ClosureCase 快照（closure-case-[日期].yaml）：
        → status: "closed"
        → 所有处理完的 branch 移入 closed_branches
        
        清理暂存区（两个文件同步清理）：
        → PENDING-EXPERIENCES.md：将所有 🔲 待处理 条目标记为 ✅ 已处理，移入归档区
        → CO-BUILD-LOG.md：将「待处理日志条目」中已提炼的条目移入「已处理归档」区
```

---

## AI 自动判断触发粒度的规则

本规则写在此处，供 AI 在用户说「更新 Skill」类语句时自行判断：

```
判断逻辑：
  IF 用户描述了具体的单个踩坑/经验点
     → 触发 skill-capture-closure（单次）

  IF 用户说「项目/任务做完了」「基于整个过程」「全部更新一下」
     → 触发 project-retrospective（批量）

  IF 用户只说「更新 Skill」但上下文是刚完成一个完整项目
     → 默认触发 project-retrospective，并在 Step 3 输出清单时让用户确认范围

  IF 不确定
     → 先问用户：「是针对某个具体经验记录，还是对本次完整项目做系统复盘？」
```

---

## 注意事项

- **Step 4 必须串行**：每次只处理一个 Skill，等该 Skill 的变更记录和索引都写完，再处理下一个。并行处理极易导致变更记录写错文件。
- **Step 2 主动扫描，不依赖用户描述**：AI 应从对话历史中自主提取，用户只需最终确认清单，而非重新描述一遍。
- **Step 3 必须等用户确认**：清单可能有误判（AI 认为某个 Skill 需要更新，但用户不认同），必须先对齐再执行。
- **跳过项也要记录**：在索引「变更记录」中追加「[日期] | 项目复盘扫描 | 以下 Skill 确认无需更新：[列表]」，便于追溯。

---

## 变更记录

### v1.0 — 2026-03-19 — 初始创建

**触发事件**：沙盘推演发现 `skill-capture-closure` 按「单次经验」设计，无法覆盖「项目结束后批量更新多个 Skill」的场景（漏洞③）。同时发现 AI 在「更新 Skill」触发词下无法自动判断粒度（漏洞①的一部分）。

**经验核心**：需要「外壳+内核」两层结构：`project-retrospective` 负责扫描和批量调度，`skill-capture-closure` 负责每个具体更新动作。触发粒度判断逻辑内置在本 Skill 中。

**修改内容**：
- 新增：本 Skill 全部内容（首次创建）

**验证状态**：🔵 待验证

---

### v1.1 — 2026-03-19 — 对接经验自动感知机制

**根因**：新建了 `auto-experience-hook` Rule 和 `PENDING-EXPERIENCES.md` 暂存文件，`project-retrospective` 的 Step 2 需要优先读取暂存文件（而不是从零扫描对话），同时新增 Step 5 的暂存区清理动作。

**经验核心**：暂存文件是经过任务执行中自动感知的高质量草稿，应作为 Step 2 的主要来源；对话扫描作为兜底，避免遗漏。

**修改内容**：
- 修改：Step 2 → 改为「两路来源合并」：先读暂存文件，再补充扫描对话
- 修改：Step 5 → 报告完成后，同步清理暂存区（标记已处理并归档）

**验证结果**：
- 正向验证：有暂存条目时，Step 2 应直接读到草稿，无需 AI 从零扫描对话（待真实场景验证）
- 负向验证：无暂存条目时，Step 2 仍走对话扫描兜底，流程不中断（待真实场景验证）

**验证状态**：🔵 待验证

---

### v1.2 — 2026-03-19 — Step 4 改用 skill-updater 子智能体

**根因**：Cursor 2.4/2.5 子智能体功能完整可用。之前 Step 4 是主 Agent 自己处理每条经验，占用主对话 context。改用 skill-updater 子智能体后，每条经验在独立 context 中处理，主 Agent 只看最终摘要，节省 token，且上下文不互相污染。

**经验核心**：「重复、有固定流程、需要独立上下文」的操作，是子智能体的理想使用场景。

**修改内容**：
- 修改：Step 4 → 改为调用 `/skill-updater` 前台子智能体，串行传入每条经验草稿，等待返回后再处理下一条

**验证结果**：
- 正向验证：skill-updater 接收经验草稿，能正确判断新建/更新并写入文件（待真实场景验证）
- 负向验证：主对话 context 不包含子智能体的中间步骤（待验证）

**验证状态**：🔵 待验证

---

### v1.3 — 2026-03-19 — Step 2 加入第三路输入（CO-BUILD-LOG）

**根因**：用户提出「协作建设新 Skill 时，过程中的设计意图/AI推理/试错轨迹/转折决策是最有提炼价值的隐性知识，但 PENDING-EXPERIENCES 只捕捉结果，不捕捉过程」。新建了 co-build-log 机制，需要接入 project-retrospective。

**经验核心**：过程日志（推理链/决策轨迹）与结果日志（踩坑/发现）是互补的两层记录，合并后的复盘质量远高于单一来源。

**修改内容**：
- 修改：Step 2 → 从「两路来源合并」改为「三路来源合并」：PENDING-EXPERIENCES（结果层）+ CO-BUILD-LOG（过程层）+ 对话扫描（兜底）
- 修改：Step 5 清理步骤 → 同步清理 CO-BUILD-LOG 中已处理的条目

**验证结果**：
- 正向验证：做复盘时，若有 CO-BUILD-LOG 条目，应出现在待处理清单中（待真实场景验证）
- 负向验证：PENDING-EXPERIENCES 的处理逻辑不变，对话扫描兜底逻辑不变

**验证状态**：✅ 已验证（2026-03-19 tashan-openbrain 部署复盘中首次真实执行三路来源合并，CO-BUILD-LOG 条目成功出现在待处理清单中）

---

### v1.4 — 2026-03-19 — 加入 ClosureCase 快照 + repair branch + 统一任务信封

**根因**：对比 closure-orchestration-package 发现三个缺口：①子智能体调用无结构化 I/O（主控无法可靠续跑）；②无显式状态追踪（靠 AI 记忆）；③验证失败无 repair branch 自动回路。

**经验核心**：从「文本流水」到「状态机」的关键一步是：给每个处理单元一个 task_id/case_id/branch_id，给输出一个 gate_recommendation。

**修改内容**：
- 新增：Step 4（原 Step 4 后移为 Step 5）→ 生成 ClosureCase 快照文件
- 修改：Step 5（原 Step 4）→ 调用 skill-updater 时使用统一任务信封；解析 gate_recommendation；自动创建 repair branch
- 修改：Step 6（原 Step 5）→ 复盘报告加入 repair 统计；更新 ClosureCase 状态为 closed

**验证结果**：
- 正向验证：下次复盘应生成 closure-case-[日期].yaml（待真实场景验证）
- 负向验证：三路来源合并逻辑不变，清理逻辑不变

**验证状态**：✅ 已验证（2026-03-19 tashan-openbrain 复盘：ClosureCase 快照文件已生成，repair branch 机制 ready，统一任务信封格式运行正常）

---

### v1.5 — 2026-03-19 — 加入架构级反思维度 + 路由分发逻辑

**根因**：沙盘推演发现两个结构性漏洞：①扫描维度只有 A/B/C/D（Skill 相关），缺乏 Rule/Agent/编排架构维度；②所有条目统一走 skill-updater，绕过了 skill-designer 的关卡体系。

**修改内容**：
- 修改：Step 2 → 新增 E 类扫描维度（E1新建Rule/E2新建Agent/E3集成改造/E4系统重构）
- 修改：Step 3 → 清单分为「Skill更新类」和「架构级改进类」两组，说明路径差异
- 修改：Step 5 → 从「统一调 skill-updater」改为「五路路由分发」（路径①②③④⑤）
- 修改：Step 6 → 复盘报告加入架构级改进分类统计

**验证结果**：
- 正向验证：复盘时若有新建 Rule 需求，应出现 E1 类条目并路由到 skill-designer（待验证）
- 负向验证：「更新已有 Skill」类条目仍走 skill-updater 路径①，不受影响

**验证状态**：✅ 已验证（2026-03-19 tashan-openbrain 复盘：E类条目正确识别，五路路由分发机制运行正常）

---

### v1.6 — 2026-03-23 — 新增 E1b/E2b/E5 + 路径⑥⑦（产物类型覆盖修复）

**根因**：E 类扫描维度（v1.5新增）中 E1/E2 只有「新建」，无「更新已有Rule/Agent」分支；且无「更新规范/参考文档」（E5）维度。导致复盘时若发现已有 Rule 歧义或规范文档有误，无对应路由。

**修改内容**：
- 新增：E1b（更新已有Rule）、E2b（更新已有Agent）、E5（更新规范/参考文档）三种扫描类别
- 新增：路径⑥（E1b/E2b → skill-rule-修改规范，三问+备份+修改+变更记录）
- 新增：路径⑦（E5 → project-doc-versioning-guard 四步留痕，快速，无关卡）
- 修改：Step 3 清单格式 → 路径说明更新为七路
- 修改：Step 6 复盘报告 → 统计项增加「更新已有Rule/Agent/规范文档」

**备份路径**：`history/SKILL_v1.5_20260323_before_e1b-e2b-e5.md`

**验证状态**：🔵 待验证

---

### v1.7 — 2026-03-23 — 新增 E6（结构性设计问题）扫描维度（元反思层修复）

**根因**：同上，project-retrospective 的 E 类扫描维度缺少「结构性根因」诊断——复盘时若发现 AI 反复失败且根因是规范机制设计缺陷（连接缺口/类型错误/执行力度不足等），应被识别为 E6 而非只是「AI 疏忽」

**修改内容**：
- 新增：E6 扫描类别（判断标准：同类失败≥2次 / Skill里的规范需要是Rule / 靠AI记忆才知道文档 / 建议语气需要禁止语气 / 靠AI主动记忆）
- E6 内含二次分类（连接缺口/类型错误/规范质量/执行力度），各有对应路由
- 路由表和复盘报告统计项同步更新

**备份路径**：`history/SKILL_v1.6_20260323_before_e6.md`

**验证状态**：🔵 待验证

---

### v1.3.1 — 2026-03-23 — 新增知识导航表（D0/D3/D4 + 核心概念速查）

**根因**：Skill 只有机械步骤，没有指向背景概念文档。AI 执行时不理解「B-object」「K-object」「D_op」「ceremony」等核心概念的来源（连接缺口）。

**经验核心**：根因 = 连接缺口——核心概念来自自进化智能体系统形式规范，但 Skill 没有指向这些文档。

**修改内容**：
- 新增：「知识导航表」章节（D0 认知根 + D3 规范参考 + D4 运行时数据 + 核心概念速查 3 条）

**验证状态**：🔵 待验证

**备份路径**：`history/SKILL_v1.3_20260323_before_nav.md`
