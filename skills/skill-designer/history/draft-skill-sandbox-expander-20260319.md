# Skill 产品定义卡片 — skill-sandbox-expander

---

## 基本信息

| 字段 | 内容 |
|---|---|
| 组件名称 | skill-sandbox-expander |
| 组件类型 | Skill |
| 复杂度级别 | Level 3（集成型） |
| 开发日期 | 2026-03-19 |
| 需求来源 | PENDING-EXPERIENCES（缺失Skill信号，来自 skill-closure-verifier-meta 创建过程）|

---

## 一、人层设计（Human Layer）

### 1.1 解决什么问题？

```
沙盘库（sandbox library）是全新工件类型，没有系统化的扩充机制：
AI 目前只能凭格式规范手动逐个写沙盘，既不知道「哪些场景缺失覆盖」，
也容易在 Phase 1 阶段不自觉地参考了现有 Skill 实现（污染两阶段分离约束）。

这个 Skill 让 AI 能够：
① 系统识别当前沙盘库的覆盖缺口
② 按优先级生成高质量的两阶段沙盘（严格遵守 Phase 1 不读 SKILL.md 的约束）
③ 持续扩充沙盘库，最终达到 100 个目标
```

### 1.2 触发条件（人的视角）

```
典型触发语句：
- 「扩充沙盘/增加沙盘/写更多沙盘」
- 「沙盘库不够，继续写」
- 「把[域名]域的沙盘补到N个」
- 「填充沙盘覆盖缺口」
- 「沙盘数量太少，帮我多写几个」

触发场景：
- 沙盘库初始化后（如当前35个），想系统扩充到100个
- skill-closure-verifier-meta 运行后建议「沙盘数量不足，可靠性低」
- 用户发现某个域的某类场景没有沙盘覆盖

明确不应该触发的情况：
- 用户想「修改已有沙盘」（这是 skill-rule-修改规范 的工作）
- 用户想「运行验证」（这是 skill-closure-verifier-meta 的工作）
- 用户想「生成修复方案」（这是 skill-domain-self-optimizer 的工作）
```

### 1.3 成功标准（人的视角）

```
产出物：
- N 个新沙盘文件（在 sandboxes/[域]/ 目录下）
- 每个沙盘：Phase 1（预想）+ Phase 2（实际验证）均已完成
- 覆盖缺口报告（说明本次新增的场景类型 + 剩余覆盖缺口）

质量判断标准：
- Phase 1 内容与现有 Skill 实现无明显关联（说明没有被污染）
- 每个沙盘至少得出一个「有/无Gap」的明确结论
- 沙盘 ID 连续，不重复
```

### 1.4 MVP 边界

```
✅ 做：
- 读取覆盖缺口（哪些域/场景类型没有沙盘）
- 建议本次优先写的场景（给出理由）
- Phase 1 生成（严格不读 SKILL.md）
- Phase 2 验证（读对应 SKILL.md，逐节点验证）
- 写入沙盘文件，更新 status

❌ 不做：
- 修改已有沙盘（留给 skill-rule-修改规范）
- 运行完整元验证（留给 skill-closure-verifier-meta）
- 生成修复建议报告（留给 skill-domain-self-optimizer）
- 批量修复已发现的 Gap（留给对应角色 Skill）
```

---

## 二、Agent 层设计（Agent Layer）

### 2.1 触发条件（AI 视角）

```
触发条件（精确描述）：
  IF 用户说了包含「扩充/增加/补充/写更多」AND「沙盘」的语句
  OR 用户说了「沙盘库不够」「沙盘覆盖缺口」
  OR skill-closure-verifier-meta Step 4 中发现某域 "draft" 状态沙盘且调用本 Skill
  THEN 触发 skill-sandbox-expander

与其他组件的优先级：
- vs skill-closure-verifier-meta：后者调用本 Skill 作为子任务；用户直接触发时二者不冲突
- vs skill-domain-self-optimizer：后者读沙盘 Gap 生成修复方案；本 Skill 创建新沙盘，不生成修复方案
- vs skill-rule-修改规范：后者修改已有 Skill 文件；本 Skill 只写新沙盘文件
```

### 2.2 执行步骤（精确序列）

```
Step 1  确认扩充范围
        输入：用户指令（指定域名 or 「全部」）
        操作：
          若用户指定了域名 → 只处理该域
          若用户说「全部」或未指定 → 处理所有5个域，按优先级排序
          询问：「本次要新增几个沙盘？（建议5-10个，不建议单次超过20个）」
        输出：确认的处理域 + 目标新增数量
        失败时：若用户没有给出数量，默认5个

Step 2  读取覆盖状态（R3 READ_FIRST）
        输入：目标域名
        操作（并行执行）：
          A. 读取 _内部总控/skill-system-design/DOMAIN-REGISTRY.md
             → 提取每个域的入口节点列表和场景类型覆盖范围
          B. 扫描 _内部总控/skill-system-design/sandboxes/[域]/ 目录
             → 统计已有沙盘数量、scenario-type 分布、最大序号
          C. 读取 _内部总控/skill-system-design/SANDBOX-FORMAT.md
             → 确认场景类型标签和格式规范
        输出：
          - 每个域：已有N个沙盘 / 覆盖了哪些 scenario-type
          - 覆盖缺口表（哪些 scenario-type 在该域没有沙盘）
          - 下一个可用沙盘序号（最大ID + 1）
        失败时：若某域目录不存在 → 报告目录缺失，不继续该域

Step 3  建议优先场景（不读 SKILL.md）
        输入：覆盖缺口表 + 目标新增数量
        操作：
          对每个覆盖缺口，提出候选沙盘场景：
          - 优先级A：跨域触发场景（cross-domain），因为这类 Gap 最多
          - 优先级B：边界/异常场景（edge-case），最容易暴露隐藏问题
          - 优先级C：其他未覆盖的 scenario-type
          列出候选场景清单（场景名 + 入口节点 + 场景描述1句话）
        输出：候选场景清单（数量 ≥ 目标新增数量）
        → 询问用户：「以下是建议优先写的场景，是否全部采纳还是选择？」
           若用户确认全部 → 继续 Step 4
           若用户选择/调整 → 更新列表后继续
        失败时：若域的所有 scenario-type 都已覆盖 → 报告「该域已全覆盖标准场景类型，建议写变体场景」

Step 4  Phase 1 生成（核心约束：此步骤禁止读任何 SKILL.md）
        
        ⚠️ 关键约束：在 Step 4 全程，不允许打开任何 .cursor/skills/*/SKILL.md 文件。
        ⚠️ 仅允许读取：DOMAIN-REGISTRY.md、NODE-IO-CONTRACTS.md、SANDBOX-FORMAT.md
        
        对每个确认的候选场景，逐一执行：
        
        4.1  从 DOMAIN-REGISTRY.md 读取该场景涉及的节点链路
        4.2  从 NODE-IO-CONTRACTS.md 读取相关节点的 I/O 契约
        4.3  生成 Phase 1 内容：
             - 预想触发链路（基于节点图，不基于 Skill 实现）
             - 预想终态输出（基于 I/O 契约，不基于 Skill 步骤）
             - 自洽检查点（基于域终态定义）
        4.4  写入沙盘文件（status = "draft"，Phase 2 留空）
             文件路径：sandboxes/[域]/sandbox-[NNN].md
             NNN = Step 2 确认的下一个序号，每写一个递增1
        
        输出：N 个 status="draft" 的沙盘文件（Phase 1 已填写）
        失败时：若某场景的节点在 DOMAIN-REGISTRY 中不存在 → 跳过，在报告中说明

Step 5  Phase 2 验证（此步骤才允许读 SKILL.md）
        
        对 Step 4 生成的每个沙盘文件，逐一执行：
        
        5.1  读取该沙盘涉及的每个节点对应的 SKILL.md
        5.2  按节点逐一验证：
             - 触发了吗：该 Skill 的触发词/条件是否能被场景输入激活
             - 输出了吗：该 Skill 是否有明确步骤产生对应输出
             - 触发下游了吗：该 Skill 是否有步骤触发下游节点
             记录为 ✅/❌/⚠️
        5.3  识别 Gap：
             - 对照 Phase 1 预想链路 vs Phase 2 实际验证
             - 差异 = Gap 候选
             - 每个 Gap 必须引用「哪个 SKILL.md 的哪个步骤」作为证据
        5.4  更新沙盘文件：
             - 填写 Phase 2「节点逐一验证」表格
             - 填写「Gap 发现」部分
             - 更新 status：无 Gap → "validated"，有 Gap → "gap-found"
        
        输出：N 个完整沙盘文件（Phase 1 + Phase 2 均已完成）
        失败时：若某节点的 SKILL.md 文件不存在 → 记为「❌ 缺失」Gap，写入沙盘

Step 6  输出覆盖缺口更新报告
        输入：本次新增的沙盘列表
        操作：
          - 统计：本次新增N个，其中 validated: X 个，gap-found: Y 个
          - 更新后各域沙盘数量 + 各场景类型覆盖情况
          - 剩余覆盖缺口（还有哪些 scenario-type 未被覆盖）
          - 发现的新 Gap 总数（来自 gap-found 沙盘）
        输出：覆盖缺口更新报告（内联输出）
        失败时：无（报告总是可以生成）
```

### 2.3 边界条件

```
情况A：用户要求单次写 > 20 个沙盘
→ 处理方式：告知「建议分批执行，每次 5-10 个，保证质量」，询问是否缩减

情况B：Phase 1 写完后，用户说「先看看 Phase 1，不要继续 Phase 2」
→ 处理方式：停在 Step 4，所有文件保留 status="draft"，告知后续可再次触发继续

情况C：某域沙盘文件数量已达 20 个（5域 × 20 = 100 目标）
→ 处理方式：告知「该域已达到 100 目标的单域上限」，建议写变体或跨域场景

情况D：用户要求「把已有沙盘的 Phase 2 补完」（而不是写新沙盘）
→ 处理方式：告知这是不同场景，可以只执行 Step 5（跳过 Step 3-4）

情况E：某节点既是入口节点也是传递节点（多角色入口）
→ 处理方式：写两个沙盘分别覆盖（一个直接触发，一个被上游触发）
```

### 2.4 依赖声明

```
依赖的其他 Skill/Agent/Rule：
- SANDBOX-FORMAT.md：Step 1 读取格式规范
- DOMAIN-REGISTRY.md：Step 2/4 读取节点图
- NODE-IO-CONTRACTS.md：Step 4 读取 I/O 契约
- 现有沙盘文件（sandboxes/*）：Step 2 读取覆盖状态
- 各域 SKILL.md 文件：Step 5 读取（Phase 2 验证）

会影响的其他 Skill/Agent/Rule：
- skill-closure-verifier-meta：沙盘数量增加后，下次运行的验证覆盖率会更高
- skill-domain-self-optimizer：新 gap-found 沙盘会增加 Gap 证据库
- skill-domain-health-check：新沙盘的 Gap 汇总会影响域健康报告
```

### 2.5 常见失败模式

```
失败模式1：Phase 1 被 SKILL.md 内容污染
  → 根本原因：AI 在生成 Phase 1 时「顺手」读了相关 SKILL.md，导致预想链路直接描述了现有实现
  → 预防方法：Step 4 开头明确标注「⚠️ 此步骤禁止读 SKILL.md」，所有读取操作仅限 DOMAIN-REGISTRY + NODE-IO-CONTRACTS
  → 识别方法：Phase 1 中若出现「根据 SKILL.md Step X」类表述，即为污染

失败模式2：Phase 2 验证流于形式，全部标为 ✅
  → 根本原因：AI 想快速完成，对「触发了吗/输出了吗/触发下游了吗」三项都标 ✅ 而不仔细验证
  → 预防方法：Step 5.2 要求每个 ⚠️/❌ 必须有引用（「[SKILL名] Step X 缺少...」），仅有 ✅ 的沙盘需人工抽查

失败模式3：沙盘内容雷同，场景本质相同但换了名字
  → 根本原因：追求数量目标，写了多个同质场景
  → 预防方法：Step 3 建议场景时，必须说明「与现有沙盘的本质区别是什么」

失败模式4：沙盘 ID 跳号或重复
  → 根本原因：Step 2 读取的最大序号不准确，或并行写多个时序号冲突
  → 预防方法：Step 2 必须 glob 扫描实际文件，不能靠记忆；写沙盘时顺序执行（不并行）

回退动作：
- 若 Phase 1 疑似被污染 → 删除该沙盘文件，回到 Step 3 重新确认场景，重新执行 Step 4
- 若 Phase 2 验证不充分 → 更新 status 为 "draft"，等待下次重跑 Step 5
```

### 2.6 强绑定 Rule

```
强绑定（必须遵守）：
- R2 NO_FABRICATION：Phase 2 中不允许凭印象写 Gap 证据，必须实际读 SKILL.md 后再写
- R3 READ_FIRST：Step 2 必须完整读取覆盖状态才能建议场景，不允许「跳过读取凭经验建议」
- R6 ARTIFACT_FIRST：每个沙盘必须落到文件（不能只在对话中描述）

推荐注入：
- R1 EVIDENCE_FIRST：Phase 2 每条 Gap 有证据链（文件路径 + 步骤描述）
```

---

## 三、人层 vs Agent 层张力分析

```
人层设计中「不言而喻」的假设：
- 「Phase 1 不读 SKILL.md」是对人类而言显而易见的，但 AI 在执行时会「顺手查资料」
- 人知道「50个沙盘比10个好」，但 AI 若不约束质量，会用相似场景快速凑数
- 人知道「覆盖缺口」指的是场景类型维度，而 AI 可能只按数量判断

AI 可能产生歧义的点：
1. 「Phase 1 阶段不读 SKILL.md」——AI 可能理解为「不直接引用 SKILL.md 的原话」而非「完全不打开文件」
   修订：Step 4 改为「禁止打开 .cursor/skills/*/SKILL.md 文件（用文件路径禁止而非语义禁止）」
   
2. 「覆盖缺口」——AI 可能只计数（「这个域只有3个沙盘，不够」）而不分析场景类型分布
   修订：Step 2 明确要求输出「已覆盖的 scenario-type 列表」而非只输出数量

3. 「建议优先场景」——AI 可能认为自己的判断就是最终结论，跳过用户确认
   修订：Step 3 末尾强制要求「询问用户确认场景列表」，不允许直接进入 Step 4

两层对齐后的修订（已在 2.2 中体现）：
- 将 Phase 1 约束改为文件路径级禁止（更精确）
- 将「建议场景」改为「建议 + 等用户确认」两步
- 将 Phase 2 验证改为「每个 ⚠️/❌ 必须有引用」（防止流于形式）
```

---

## 四、复杂度评估

```
与现有 Skill/Rule 的交互点：
- SANDBOX-FORMAT.md：读取依赖
- DOMAIN-REGISTRY.md：读取依赖
- NODE-IO-CONTRACTS.md：读取依赖
- sandboxes/* 目录：读写（创建新文件）
- 各域 SKILL.md：Step 5 读取（Phase 2）
- skill-closure-verifier-meta：被调用/调用关系（verifier-meta Step 4 可调用本 Skill）
- skill-domain-self-optimizer：输出消费关系（本 Skill 的 gap-found 沙盘是 optimizer 的输入）
- skill-domain-health-check：间接影响（沙盘数量变化影响健康报告的 Gap 汇总）

Level 判断依据：
[x] Level 3：新建组件，与多个现有组件有交互（依赖 DOMAIN-REGISTRY / NODE-IO-CONTRACTS / 各 SKILL.md；被 verifier-meta 调用；影响 optimizer 和 health-check 的输入）

最终级别：Level 3
```

---

## 五、关卡执行记录

### 关卡A：AI 执行者模拟（Level 2+）

```
执行者：/skill-simulator 子智能体
执行日期：2026-03-19
（待 skill-simulator 执行后填写）
```

### 关卡B：Skill 系统破坏（Level 3+）

```
执行者：/skill-system-destroyer 子智能体
执行日期：2026-03-19
（待 skill-system-destroyer 执行后填写）
```

### 关卡C：行为验证（Level 2+）

```
执行者：/verifier 子智能体
执行日期：2026-03-19
（待 verifier 执行后填写）
```
