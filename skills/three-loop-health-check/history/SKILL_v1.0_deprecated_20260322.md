---
name: three-loop-health-check
description: ⚠️ v1.0 已废弃（状态仪表盘，设计方向错误），v2.0 重建中（场景化沙盘验证）。
---

# ⚠️ 本 Skill v1.0 已废弃，请勿使用

**废弃原因**：v1.0 读取状态文件计数，是「状态仪表盘」，不是真正的闭环验证。  
**正确设计（v2.0 重建中）**：
1. 扫描现有 Skills/Roles/Rules，动态归纳所有任务场景  
2. 对每个场景识别最小闭环和大闭环  
3. 为每个闭环设计完整沙盘（含认知根 + 认知反馈节点）  
4. 逐节点验证现有体系能否走通  
5. 输出场景级健康报告

**废弃时间**：2026-03-22

---

# 以下为 v1.0 历史内容（参考用，不执行）

# 三大闭环系统总健康检查（three-loop-health-check）

> 关系类型：orchestrates → skill-system-health-check / cognitive-consistency-check / cognitive-work-alignment-check
> 设计依据：三大闭环架构蓝图，全系统健康仪表盘缺口修复
> 强绑定 Rule：R2 NO_FABRICATION（报告数字来自实际读取，不得估算）/ R1 EVIDENCE_FIRST（❌/⚠️ 必须有文件路径证据）
> ⚠️ 重要：Full 模式调用子 Skill 时，这些子任务属于认知子任务（B0 排除清单），不触发各自的 session-bootstrap 序列B；由本 Skill 统一在完成后触发一次序列B。

---

## 与专项检查 Skill 的区别（路由决策表）

| 需求 | 使用哪个 Skill |
|---|---|
| 只查 Skill 体系内部一致性（触发词/版本/孤立组件）| `skill-system-health-check` |
| 只查 Skill 体系传播完备性（沙盘验证任意输入→终态）| `skill-closure-verifier-meta` |
| 只查认知结构自洽（C1-C11，L0/L1/L1.5三层）| `cognitive-consistency-check` |
| 只查工作任务是否有认知根（第四维）| `cognitive-work-alignment-check` |
| 只查认知结构状态快照 | `cognitive-review-brain-map` |
| **三大闭环 + 耦合全部一起查** | **`three-loop-health-check`（本 Skill）** |

---

## 激活后立即执行

```
Step 1  确认检查模式
        询问（如果用户消息未明确说明）：
        「执行三大闭环健康检查。请选择模式：
          [Quick（~1分钟，读取系统状态文件快照，速度优先）]
          [Full（~5-10分钟，调用各专项检查 Skill 后输出整合报告）]」
        
        模式识别规则：
        - 用户消息含「快速」「quick」「简单」→ Quick 模式（无需询问）
        - 用户消息含「全量」「全面」「深度」「full」→ Full 模式（无需询问）
        - 未明确时 → 发出以上问题，等待用户明确回复后继续
        - ⚠️ 不设「无回应默认值」：等待用户明确选择后才继续执行
        
        ⚠️ Full 模式架构说明：
        Full 模式先收集完所有数据（包括调用子 Skill），再统一输出一份整合报告。
        不先输出 Quick 快照再追加——对话流式输出不支持回溯编辑。

Step 2  收集 Loop 1 数据
        
        必须读取以下文件（绝对路径），不得凭记忆报告：
        
        Read: /Users/boyuan/aiwork/0310_huaxiang/.cursor/skills/skill-index/SKILL-INDEX.md
        → 统计：状态列为「🔵 待验证」的 Skill 数量 → 记为 L1_pending
        → 统计：状态列为「⚠️」的 Skill 数量 → 记为 L1_issues
          （「⚠️」判断标准：SKILL-INDEX 表格「状态」列包含 ⚠️ emoji 的行）
        
        Read: /Users/boyuan/aiwork/0310_huaxiang/.cursor/skills/skill-index/PENDING-SKILLS.md
        → 统计：🔲 待处理 PENDING-SKILLS 条目数量 → 记为 L1_pending_skills
        → 找最老「🔲 待处理」条目日期 → 记为 L1_oldest_date
        
        Read: /Users/boyuan/aiwork/0310_huaxiang/_内部总控/任务日志.md（最后100行）
        → 在条目的「触发的 Skill」字段或「完成的工作」字段中，找最近一次包含
          「skill-system-health-check」的条目日期 → 记为 L1_last_health_check
          若未找到 → L1_last_health_check = "从未执行过"
        
        IF Full 模式：
          告知用户「[Loop 1] 正在运行 skill-system-health-check...（此操作为子任务，
          不单独写入任务日志，由本检查统一记录）」
          调用 skill-system-health-check
          等待其输出，提取结论摘要（通过/不通过/发现N个问题）
          → 记为 L1_deep_result

Step 3  收集 Loop 2 数据
        
        Read: /Users/boyuan/aiwork/0310_huaxiang/_内部总控/认知结构/L2_碎片化思考/碎片整合索引.md
        → 统计：「🔲 待整合」状态的行数 → 记为 L2_fragments
        
        Read: /Users/boyuan/aiwork/0310_huaxiang/_内部总控/认知结构/L3_原始记录/系统日志.md
        → 逆向搜索整个文件，找最近一行包含「cognitive-consistency-check」的日志条目
        → 提取该条目的日期（格式：[LOG-YYYYMMDD-NN]），计算距今天数 → 记为 L2_last_c_check
          若未找到 → L2_last_c_check = "从未执行过"
        
        Read: /Users/boyuan/aiwork/0310_huaxiang/_内部总控/认知结构/L1.5_底层原则层/底层原则库.md
        → 统计：标注「✅已确认」的原则数量 → 记为 L2_confirmed_principles
        → 统计：含「P?」「候选」「待确认」的候选原则数量 → 记为 L2_candidate_principles
          （识别标准：状态字段含「待确认」「候选」或编号含「?」的原则条目）
        
        IF Full 模式：
          告知用户「[Loop 2] 正在运行 cognitive-consistency-check...（子任务）」
          调用 cognitive-consistency-check
          等待其输出，提取结论（C1-C11 通过数、发现问题数）
          → 记为 L2_deep_result

Step 4  收集 Loop 3↔Loop 2 耦合数据
        
        Read: /Users/boyuan/aiwork/0310_huaxiang/_内部总控/认知结构/L3_原始记录/待完成总清单.md
        → 统计：以「□ [cascade-」开头的行数 → 记为 L3L2_cascade_pending
        → 统计：以「□」开头且包含「Skill体系对齐」或「skill-evolution」或「原则P」字样的行数
          → 记为 L3L2_skill_align_pending（Loop 2→Loop 1 指标）
        
        Read: /Users/boyuan/aiwork/0310_huaxiang/.cursor/skills/skill-index/PENDING-EXPERIENCES.md
        → 统计：「🔲 待处理」条目数量 → 记为 L3L2_exp_pending
        → 找最老「🔲 待处理」条目日期 → 记为 L3L2_oldest_exp
        
        IF Full 模式：
          告知用户「[Loop 3↔2] 正在运行 cognitive-work-alignment-check...（子任务）」
          调用 cognitive-work-alignment-check
          等待其输出，提取结论（对齐健康/发现N个漂浮任务）
          → 记为 L3L2_deep_result

Step 5  三大闭环耦合状态评估（基于 Step 2-4 收集的数据，无需额外读取）
        
        【Loop 1 状态判定】
          IF L1_issues = 0 AND L1_pending_skills 距今 ≤7天（或无积压）：✅
          ELIF L1_issues > 0 OR L1_pending_skills 距今 7-30天：⚠️
          ELSE（有❌Skill 或积压>30天）：❌
        
        【Loop 2 状态判定】
          IF L2_fragments < 8 AND L2_last_c_check 距今 ≤7天 AND L2_candidate_principles = 0：✅
          ELIF L2_fragments ≤15 AND L2_last_c_check 距今 ≤30天 AND L2_candidate_principles ≤3：⚠️
          ELSE：❌
        
        【Loop 3↔2 状态判定】
          IF L3L2_cascade_pending = 0 AND L3L2_exp_pending 距今 ≤7天（或无积压）：✅
          ELIF L3L2_cascade_pending ≤3 OR L3L2_exp_pending 距今 7-30天：⚠️
          ELSE：❌
        
        【Loop 2→Loop 3 耦合】基于 L3L2_cascade_pending：0→✅ | 1-3→⚠️ | >3→❌
        【Loop 3→Loop 2 耦合】基于 L3L2_exp_pending 最老日期：≤7天→✅ | 7-30天→⚠️ | >30天→❌
        【Loop 2→Loop 1 耦合】基于 L3L2_skill_align_pending：0→✅ | >0→⚠️
        
        【整体结论规则（固定，不允许自由裁量）】
          有任意 ❌ → CRITICAL
          无 ❌ 但有 ⚠️ → NEEDS ATTENTION
          全部 ✅ → HEALTHY

Step 6  输出综合健康报告（Quick 或 Full 均在此步骤统一输出）
        
        ⚠️ 在所有数据收集完成后才输出报告，不提前输出任何中间结果。
        
        输出格式（严格按此格式，不得自由排列）：
        
        ┌─────────────────────────────────────────┐
        │  🏥 三大闭环系统健康报告                   │
        │  日期：YYYY-MM-DD | 模式：Quick / Full    │
        ├─────────────────────────────────────────┤
        │  整体结论：HEALTHY / NEEDS ATTENTION / CRITICAL  │
        ├─────────────────────────────────────────┤
        │  ── 各闭环状态 ──                         │
        │                                          │
        │  Loop 1（Skill 体系）：✅/⚠️/❌          │
        │  · 待验证Skill：{L1_pending}个 | 有问题Skill：{L1_issues}个  │
        │  · PENDING-SKILLS积压：{L1_pending_skills}条（最老：{L1_oldest_date}）│
        │  · 上次 health-check：{L1_last_health_check}           │
        │  [Full] {L1_deep_result}                              │
        │                                          │
        │  Loop 2（认知结构）：✅/⚠️/❌           │
        │  · 待整合碎片：{L2_fragments}条 | 候选原则积压：{L2_candidate_principles}条 │
        │  · 上次C1-C11：{L2_last_c_check}                     │
        │  [Full] {L2_deep_result}                              │
        │                                          │
        │  Loop 3↔2（场景-认知对齐）：✅/⚠️/❌   │
        │  · cascade待处理：{L3L2_cascade_pending}条 | 经验反馈积压：{L3L2_exp_pending}条（最老：{L3L2_oldest_exp}）│
        │  [Full] {L3L2_deep_result}                            │
        │                                          │
        │  ── 闭环耦合状态 ──                       │
        │  Loop 2→Loop 3：✅/⚠️/❌ {cascade条目数说明}         │
        │  Loop 3→Loop 2：✅/⚠️/❌ {经验积压说明}             │
        │  Loop 2→Loop 1：✅/⚠️/❌ {原则-Skill对齐说明}       │
        │                                          │
        │  ── 优先行动清单 ──                       │
        │  1. [P0/P1] {行动描述} → 触发：{Skill名称}           │
        │  2. ...（最多5条）                         │
        │  （若无问题：「系统各闭环健康，无需处理」）           │
        │                                          │
        │  [Quick模式] ⚠️ 基于文件快照，非实时验证  │
        │  [如需深度验证：运行 Full 模式]             │
        │                                          │
        │  [按钮（条件输出）]                        │
        │  · Quick 模式下：[运行 Full 模式] [处理第1项优先行动] │
        │  · Full 模式下：[处理第1项优先行动]          │
        └─────────────────────────────────────────┘

Step 7  响应用户后续操作
        → 用户选「运行 Full 模式」→ 回到 Step 1 重新以 Full 模式执行
        → 用户选「处理第N项」→ 告知用户触发哪个 Skill 处理该问题，转交后触发序列B
        → 用户问某 Loop 详情 → 展示该 Loop 的详细原始数据，等待进一步指令或无指令时触发序列B
        → 用户无后续操作 → 执行 session-bootstrap 序列B（统一在此触发，不在子 Skill 中重复触发）
```

---

## 文件路径索引（Step 2-4 引用的所有文件）

```
Loop 1:
  SKILL-INDEX:     .cursor/skills/skill-index/SKILL-INDEX.md
  PENDING-SKILLS:  .cursor/skills/skill-index/PENDING-SKILLS.md
  任务日志:         _内部总控/任务日志.md

Loop 2:
  碎片整合索引:    _内部总控/认知结构/L2_碎片化思考/碎片整合索引.md
  系统日志:        _内部总控/认知结构/L3_原始记录/系统日志.md
  底层原则库:      _内部总控/认知结构/L1.5_底层原则层/底层原则库.md

Loop 3↔2:
  待完成总清单:    _内部总控/认知结构/L3_原始记录/待完成总清单.md
  PENDING-EXPS:    .cursor/skills/skill-index/PENDING-EXPERIENCES.md
```

---

## 若文件不存在的处理

```
任何文件读取失败（文件不存在 / 路径错误）：
→ 对应 Loop 状态标记为「⚠️ 数据缺失（文件未找到）」
→ 不停止整个检查，继续执行其他 Loop
→ 在优先行动清单中加入：「修复数据路径：[文件名]」
```

---

## 注意事项

- **纯只读，不修改任何文件**：本 Skill 不写入任何文件，不触发任何修复
- **Full 模式子任务声明**：调用 skill-system-health-check / cognitive-consistency-check / cognitive-work-alignment-check 时，这三个 Skill 属于本 Skill 的子任务，不单独触发 session-bootstrap 序列B（见 B0 排除清单）
- **不替代专项 Skill**：发现问题后，建议用户触发对应专项 Skill 处理，本 Skill 只诊断不修复
- **Quick 模式局限**：必须在报告末尾标注「Quick 模式基于文件快照」

---

## 变更记录

### v1.0 — 2026-03-21 — 初始创建（经关卡A+B修订）

**根因**：全量闭环 Gap 分析发现三大闭环无统一健康仪表盘入口。

**关卡A修复（4项Critical）**：
- 补全所有文件绝对路径
- Full 模式改为「先收集后统一输出」，解决流式输出不可回溯问题
- L1_last_health_check 从任务日志.md 读取，而非 SKILL-INDEX 变更记录
- 「Skill体系对齐类条目」添加关键词识别标准

**关卡B修复（2项Critical，2项High）**：
- C-1：在 Step 7 明确声明「子任务不触发序列B」（配合 B0 排除清单更新）
- C-2：Full 模式重构为「收集后统一报告」架构
- H-1：删除触发词「系统现在状态怎么样」（与 cognitive-review-brain-map 重叠）
- H-2：L1_last_health_check 读取路径改为任务日志.md

**验证状态**：🔵 待关卡C验证
