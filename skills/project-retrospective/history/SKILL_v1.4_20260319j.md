---
name: project-retrospective
description: 项目级 Skill 批量复盘。在一个项目/任务闭环完成后，主动扫描本次对话中调用过的所有 Skill，逐个判断是否需要新建或更新，批量调用 skill-capture-closure 完成沉淀，最后输出复盘报告。触发词：「项目做完了」「更新一下Skill」「基于刚刚的过程更新规范」「做个项目复盘」「沉淀一下经验」「把这次的经验记下来」。
---

# 项目级 Skill 复盘（project-retrospective）

> 单次经验用 `skill-capture-closure`（随时触发）。
> 项目结束后的系统性批量复盘用本 Skill（一次扫描全部）。
> 本 Skill 是外壳，`skill-capture-closure` 是内核——扫描由本 Skill 负责，每个具体更新动作仍走 `skill-capture-closure` 标准流程。

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
           → 候选：新建 Skill
        【D. 某个 Skill 的触发词不准（该触发没触发，或错误触发）】
           → 候选：更新 description 字段
        
        → 将三路来源合并为一张完整清单

Step 3  输出「待处理清单」，等用户确认
        格式：
        「本次项目 Skill 复盘扫描结果：

          📋 待处理清单（共 N 项）：
          ① [Skill目录名] — [A/B/C/D类型] — [一句话说明需要做什么]
          ② [Skill目录名] — [A/B/C/D类型] — [一句话说明需要做什么]
          ...
          ⓪ 无需处理（执行符合预期）：[Skill列表]

          请确认：[全部处理] [跳过某项] [调整说明]」

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

Step 5  逐项调用 skill-updater 子智能体处理（串行，使用统一任务信封）
        
        对待处理清单中的每一项，按顺序执行：
        
        a. 明确宣告当前处理第几项：
           「▶ 正在处理 [N/总数]：[Skill目录名] — [类型]」
        
        b. 构造统一任务信封（参见 skill-designer/agent-io-contract.md）：
           task_id: TASK-[日期]-[NN]
           case_id: project-retrospective-[日期]
           branch_id: skill-update-[Skill名称]
           goal: [经验草稿核心]
           scope: [具体修改范围]
           allowed_write_set: [受影响的 SKILL.md + SKILL-INDEX.md]
           done_criteria: [变更记录已追加, 版本号已更新]
        
        c. 启动前台子智能体（等待完成后再处理下一项）：
           调用 /skill-updater，传入任务信封
        
        d. 子智能体返回后，解析输出信封：
           - gate_recommendation = pass → 更新 ClosureCase 将此 branch 移入 closed_branches
           - gate_recommendation = fail → 自动创建 repair branch，记录 suggested_next_branches
           - 输出小结：「✅/❌ [N/总数] [操作摘要]」
        
        e. 若有 repair branch：处理完正常项后，逐个处理 repair branch（同样串行）
        
        f. 处理完一项，再开始下一项（严格串行）

Step 6  输出复盘报告，更新 ClosureCase，清理暂存区
        「📊 项目 Skill 复盘完成

          处理结果：
          ✅ 新建：N 个 Skill
          ✅ 更新：N 个 Skill（含版本升级）
          ✅ 状态升级：N 个 Skill（🔵→✅）
          🔧 repair 处理：N 个（验证失败后已修复）
          ⏭ 跳过：N 个（无需修改）

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

**验证状态**：✅ 已验证（2026-03-19 首次真实跑通）

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

**验证状态**：🔵 待验证
