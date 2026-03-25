# Skill 产品定义卡片：three-loop-health-check

> 填写日期：2026-03-21
> 填写人：skill-designer（引导）

---

## 基本信息

| 字段 | 内容 |
|---|---|
| 组件名称 | `three-loop-health-check` |
| 组件类型 | Skill |
| 复杂度级别 | Level 3（集成型：调用多个已有检查 Skill，且有触发词重叠风险）|
| 开发日期 | 2026-03-21 |
| 需求来源 | 用户直接提出（基于「全量闭环 Gap 分析」发现缺口）|

---

## 一、人层设计（Human Layer）

### 1.1 解决什么问题？

```
现有健康检查工具分散（Loop 1/Loop 2/Loop 3 各一套），用户需记住并逐个触发，无法
一次性了解「整个体系现在健康吗」。本 Skill 提供三大闭环的统一健康仪表盘。
```

### 1.2 触发条件（人的视角）

```
典型触发语句：
- 「三大闭环健康检查」
- 「全系统健康报告」
- 「整体系统健康吗」
- 「系统现在状态怎么样」
- 「检查一下三大闭环」

触发场景：
- 一段时间（>7天）未做任何健康检查，想做定期全面扫描
- 系统似乎有点问题，不确定哪个层次出了问题，先做全面诊断
- 项目完成后，想确认整体体系仍然自洽

明确不应该触发的情况：
- 「检查Skill体系」「Skill健康」→ skill-system-health-check
- 「全域验证」「闭环验证」「元验证」→ skill-closure-verifier-meta
- 「一致性检查」「自洽检查」→ cognitive-consistency-check
- 「第四维健康检查」「认知根对齐」→ cognitive-work-alignment-check
- 「运行健康检查」但上下文明确指向某单一 Loop → 对应的专项检查
```

### 1.3 成功标准（人的视角）

```
产出物：综合健康报告（对话输出）
格式：从高到低——整体结论 → Loop 1/2/3 各自状态 → 三大闭环耦合状态 → 优先行动清单

质量判断标准：
- 用户看完报告后，知道「现在最需要处理什么」
- 每个 ❌/⚠️ 都有具体的「怎么修复」建议，不只是问题描述
- Quick 模式 < 2分钟，Full 模式明确告知耗时
```

### 1.4 MVP 边界

```
✅ 做：
- 两个模式：Quick（读取状态文件，无深度扫描，快速）和 Full（调用各专项检查 Skill）
- Quick 模式默认：避免每次都运行耗时的全套检查
- 三大闭环各自的状态摘要（各用1-3行描述）
- 三大闭环之间的耦合状态（cascade-notifier 积压、PENDING-EXPERIENCES 积压等）
- 优先行动清单（最多5条，按紧急程度排序）

❌ 不做：
- 不替代专项检查 Skill（发现问题后，用户应触发对应专项 Skill 处理）
- Full 模式下不执行修复，只诊断和报告
- 不自动触发任何修复操作（遵循「报告分析，行动由用户确认」原则）
```

---

## 二、Agent 层设计（Agent Layer）

### 2.1 触发条件（AI 视角）

```
触发条件（精确描述）：
用户消息同时满足：
  ① 包含「三大闭环」或「全系统」或「整体系统健康」中至少一个
  ② 包含「健康」「检查」「状态」「报告」「诊断」中至少一个

优先级（当触发词模糊时）：
  - 若用户消息包含「全域」「元验证」「沙盘验证」→ skill-closure-verifier-meta 优先
  - 若用户消息包含「Skill内部」「触发词冲突」「版本漂移」→ skill-system-health-check 优先
  - 若用户消息包含「C1-C11」「L0与L1」「认知自洽」→ cognitive-consistency-check 优先
  - 若用户消息包含「工作任务是否有认知根」「第四维」→ cognitive-work-alignment-check 优先
  - 其余情况（含「三大闭环」「全系统」的消息）→ 本 Skill
```

### 2.2 执行步骤（精确序列）

```
Step 1  确认检查模式
        询问（如果未明确说）：
        「进行三大闭环健康检查。选择模式：
          [Quick（~1分钟，读取系统状态快照）]
          [Full（~5-10分钟，调用各专项检查 Skill，结果更准确）]」
        默认：用户无回应时选 Quick
        Full 模式下：先完成 Quick 出报告，再逐步运行各专项检查追加详情

Step 2  Loop 1 快速检查（两项读取）
        Read: .cursor/skills/skill-index/SKILL-INDEX.md
        → 计数：待验证🔵 Skill 数量、已知问题⚠️ Skill 数量
        → 扫描：有无版本号明显落后（>3个版本差）的核心 Skill
        
        Read: .cursor/skills/skill-index/PENDING-SKILLS.md
        → 计数：积压中的 Skill 需求数量和最老日期
        
        IF Full 模式：调用 skill-system-health-check（等待结果，追加到 Loop 1 报告）

Step 3  Loop 2 快速检查（三项读取）
        Read: _内部总控/认知结构/L2_碎片化思考/碎片整合索引.md
        → 计数：🔲 待整合碎片数量
        
        Read: _内部总控/认知结构/L3_原始记录/系统日志.md（最近20条）
        → 找最近一次 cognitive-consistency-check 执行日期，计算距今天数
        
        Read: _内部总控/认知结构/L1.5_底层原则层/底层原则库.md
        → 计数：✅已确认原则数 vs P?候选原则数（积压候选）
        
        IF Full 模式：调用 cognitive-consistency-check（等待结果，追加到 Loop 2 报告）

Step 4  Loop 3↔Loop 2 耦合检查（两项读取）
        Read: _内部总控/认知结构/L3_原始记录/待完成总清单.md
        → 计数：□ 待处理的 cascade-notifier 条目数量（格式为 □ [cascade-...]）
        → 计数：□ 待处理的原则约束检查条目数量
        
        Read: .cursor/skills/skill-index/PENDING-EXPERIENCES.md
        → 计数：🔲 待处理经验数量和最老日期
        
        IF Full 模式：调用 cognitive-work-alignment-check（等待结果，追加到 Loop 3 报告）

Step 5  三大闭环耦合状态评估（无需额外读取，基于前述数据）
        
        Loop 2→Loop 3：
          cascade 待处理条目数 N
          IF N = 0：✅ 无待对齐项
          IF 0 < N ≤ 3：⚠️ {N}条待对齐（建议近期处理）
          IF N > 3：❌ 级联对齐严重积压（{N}条）
        
        Loop 3→Loop 2：
          PENDING-EXPERIENCES 最老待处理日期
          IF ≤7天：✅ 认知反馈及时
          IF 7-30天：⚠️ 积压{N}条，最老{M}天
          IF >30天：❌ 认知反馈严重滞后
        
        Loop 2→Loop 1：
          「以最近是否有新原则确认（系统日志中有 cognitive-extract-principle 且
           cascade-notifier 待处理中有对应的 Skill 体系通知条目）」
          IF 有原则未对齐 Skill：⚠️ P?原则待 Skill 体系引用
          IF 无：✅ 原则-Skill 对齐良好

Step 6  生成综合健康报告
        
        「━━━━━━━━━━━━━━━━━━━━━━━
          🏥 三大闭环系统健康报告
          日期：YYYY-MM-DD | 模式：Quick/Full
          ━━━━━━━━━━━━━━━━━━━━━━━
          
          🔢 整体结论：[HEALTHY / NEEDS_ATTENTION / CRITICAL]
          
          ── 各闭环状态 ──
          Loop 1（Skill体系）：[✅/⚠️/❌] [一句话摘要]
            · 🔵待验证Skill：N个 | ⚠️有问题Skill：M个
            · PENDING-SKILLS积压：K条（最老：[日期]）
          
          Loop 2（认知结构）：[✅/⚠️/❌] [一句话摘要]
            · 待整合碎片：N条 | 候选原则积压：M条
            · 上次C1-C11检查：[N天前 / 从未运行]
          
          Loop 3↔Loop 2（场景-认知对齐）：[✅/⚠️/❌] [一句话摘要]
            · cascade待处理：N条 | 经验反馈积压：M条（最老：[日期]）
          
          ── 闭环耦合状态 ──
          Loop 2→Loop 3：[✅/⚠️/❌] [描述]
          Loop 3→Loop 2：[✅/⚠️/❌] [描述]
          Loop 2→Loop 1：[✅/⚠️/❌] [描述]
          
          ── 优先行动清单 ──
          1. [P0/P1/P2] [行动描述] → 触发：[对应 Skill 或操作]
          2. [...]（最多5条，若无问题则「无需处理」）
          ━━━━━━━━━━━━━━━━━━━━━━━」
        
        [查看详情] [运行 Full 模式] [处理第1项]

Step 7  响应用户后续操作
        → 用户选「查看详情」→ 展开对应 Loop 的详细数据
        → 用户选「运行 Full 模式」→ 逐个调用专项检查 Skill（告知耗时预估）
        → 用户选「处理第N项」→ 转发到对应的 Skill
```

### 2.3 边界条件

```
情况A：某个读取文件不存在（如从未运行 consistency-check，系统日志无记录）
  → 在对应字段显示「未找到记录」，状态标为 ⚠️，建议运行对应 Skill

情况B：Full 模式下某个专项 Skill 运行超时或报错
  → 标注「[Loop N] 深度检查未完成（运行出错）」，Quick 数据仍展示

情况C：用户说「快速检查一下」「全量检查」等模糊语言
  → 「快速/quick/简单」→ Quick 模式；「全量/全面/深度」→ Full 模式；其余→询问
```

### 2.4 依赖声明

```
调用（Full 模式）：
- skill-system-health-check：Loop 1 内部一致性深度检查（Step 2）
- cognitive-consistency-check：Loop 2 C1-C11 全套验证（Step 3）
- cognitive-work-alignment-check：Loop 3↔Loop 2 对齐深度检查（Step 4）

读取（Quick 模式，所有步骤）：
- SKILL-INDEX.md / PENDING-SKILLS.md
- 碎片整合索引.md / 系统日志.md / 底层原则库.md
- 待完成总清单.md / PENDING-EXPERIENCES.md

不会修改任何文件（纯只读 + 报告输出）

影响的其他 Skill：
- 无（本 Skill 不修改任何状态）
```

### 2.5 常见失败模式

```
失败模式1：AI 把「整体系统健康」误解为应触发 skill-system-health-check
  → 根本原因：「系统」「健康」两词在 skill-system-health-check 触发词中也出现
  → 预防：Step 2.1 明确列出与现有 Skill 的优先级规则；description 中明确区分

失败模式2：Quick 模式下数据不够新鲜，AI 却声称「系统健康」
  → 根本原因：Quick 模式读取的是静态文件，不执行动态检查
  → 预防：报告末尾始终标注「Quick 模式（基于文件快照，非实时验证）」提示

失败模式3：Full 模式下 AI 一个个串行等待各专项 Skill，耗时极长
  → 根本原因：没有并行执行机制
  → 预防：Full 模式说明「各专项检查将逐步执行，每个完成后追加结果」，不承诺并行

失败模式4：读取 cascade 待处理条目时，无法区分「已处理但未标记」和「真正未处理」
  → 根本原因：待完成总清单没有「已处理」标记（只有 □/✅）
  → 预防：只统计 □ 开头的条目，备注「以文件中□标记为准」

回退动作：
- 若任何读取失败 → 标注「未能读取」，不停止整个检查，继续其他步骤
- 若 Full 模式某专项失败 → 回退到用该步骤的 Quick 数据，标注「深度检查未完成」
```

### 2.6 强绑定 Rule

```
强绑定（必须遵守）：
- R2 NO_FABRICATION：报告中的所有数字必须来自实际读取的文件，不得估算
- R1 EVIDENCE_FIRST：每个 ❌/⚠️ 必须有具体文件+行数证据，不得主观判断
- R3 READ_FIRST：Step 2-4 必须真实执行读取操作，不得凭记忆报告状态

推荐注入：
- R6 ARTIFACT_FIRST：生成正式健康报告（格式化输出）
```

---

## 三、人层 vs Agent 层张力分析

```
人层「不言而喻」的假设：
- 「三大闭环健康」包含了各闭环内部健康 + 闭环之间耦合健康（两层）
  AI 可能只检查内部健康，忘记耦合状态检查

- 「Quick 模式」意味着不需要调用重型子 Skill
  AI 可能不清楚「不调用 skill-closure-verifier-meta」是刻意设计

AI 可能产生歧义的点：
- 「全系统健康」可能被理解为触发 skill-system-health-check（因为「系统」「健康」是其核心触发词）
- 「Quick 模式 <2分钟」—— AI 不知道各读取操作的实际耗时

两层对齐后的修订：
- 触发词设计：「三大闭环」必须作为核心触发词，单独「系统健康」不触发
- 耦合检查独立成 Step 5，明确与 Loop 内部检查分开
- 报告格式中「各闭环状态」和「闭环耦合状态」两个区块分开展示
```

---

## 四、复杂度评估

```
与现有 Skill/Rule 的交互点：
- skill-system-health-check：触发词有「健康」重叠；Full 模式下调用
- skill-closure-verifier-meta：触发词「验证」「闭环」有重叠；Full 模式下可建议用户触发
- cognitive-consistency-check：触发词「检查」重叠；Full 模式下调用
- cognitive-work-alignment-check：触发词「健康检查」有重叠；Full 模式下调用
- PENDING-EXPERIENCES.md / 待完成总清单.md：Quick 模式读取

最终级别：Level 3（集成型）
需走关卡A + 关卡B + 关卡C
```

---

## 五、关卡执行记录

（待关卡执行后填写）
