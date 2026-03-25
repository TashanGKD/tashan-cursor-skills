# Skill：Skill体系完善执行（skill-system-evolution-executor）

> 关系类型：implements → `_内部总控/认知结构/L1_系统性文档/系统架构思维维度/Skill体系设计原则_v1.0.md` §9.7

---

## 一、Skill 定位

**层级**：流程层（Process Layer）
**类型**：L4 系统型完善项目编排器
**本质**：当 Skill 体系需要多组件/多层级的系统性重构时，提供从「用户确认规模」到「经验沉淀」的完整项目流程（Phase 0~5），解决 §9.2 Level 4 的悬空终止符问题。

**VSM 完备性检验（§3.4）**：

| 条件 | 本 Skill 的对应内容 |
|---|---|
| S4 激活：什么时候触发我？ | 用户明确说「执行Skill体系完善」「L4系统型重构」「按完善计划执行」「开始Skill体系完善项目」|
| S1 执行：我做什么？ | Phase 0~5 完整编排：规模确认→分析计划→双审核→分批执行→整体验证→经验沉淀 |
| S3 质量：输出合格标准？ | Phase 4 通过 skill-system-health-check + skill-closure-verifier-meta，且验收标准逐条满足 |
| 告警：何时暂停/上报？ | Phase 0 等用户确认；Phase 1 等用户确认计划；Phase 2 Critical问题暂停；Phase 3 新冲突暂停 |
| S5 边界：我明确不做什么？ | 不处理单个 Skill 的 L1~L3 修改（→直接走skill-rule-修改规范）；不自动触发；不跳过 Phase 2 双审核 |

**与相邻 Skill 的边界**：

| Skill | 关系 |
|---|---|
| `skill-system-health-check` | 本 Skill 的子步骤（Phase 1 诊断、Phase 3/4 验证）|
| `skill-evolution-planner-meta` | 本 Skill 的子步骤（Phase 1 战略分析）|
| `skill-designer` | 本 Skill 调用它处理 Phase 3 中的 L2/L3 条目 |
| `project-retrospective` | 本 Skill 的最后子步骤（Phase 5）|
| `skill-rule-修改规范` | Phase 3 中 L1 条目的执行依据 |

---

## 二、触发词

```
「执行Skill体系完善」
「Skill体系L4改造」
「系统型Skill重构」
「按完善计划执行」
「按计划执行Skill体系更新」
「开始Skill体系完善项目」
```

**重要**：本 Skill 必须由用户明确触发，不自动触发。触发后 Phase 0 必须等用户确认才能继续。

---

## 三、执行流程（严格按 Skill体系设计原则_v1.0.md §9.7）

### Phase 0：规模确认（必须等用户决策，不可跳过）

```
Step 0.1  扫描以下来源，建立本次改动的完整清单：
          - .cursor/skills/skill-index/PENDING-EXPERIENCES.md（积压信号）
          - .cursor/skills/skill-index/PENDING-SKILLS.md（需求积压）
          - .cursor/skills/skill-index/skill-system-inventory-*.md（已知 Gap）
          - 本次对话中用户提出的改动意向

Step 0.2  输出规模评估报告：
          ┌─────────────────────────────────────────┐
          │ 涉及层级：[文档层/约束层/角色层/流程层/能力层/Agent层]
          │ 涉及组件数：[N 个，逐一列出]
          │ 影响的执行路径：[枚举]
          │ 建议分批：P0（N个）/ P1（N个）/ P2（N个）
          │ 预估工作量：[小/中/大]
          └─────────────────────────────────────────┘

Step 0.3  等待用户确认「规模和分批策略」
          IF 用户确认 → 进入 Phase 1
          IF 用户要求缩减范围 → 重新扫描后再出评估报告
          IF 用户要求推迟 → 记录到 PENDING-SKILLS，本次结束
```

---

### Phase 1：分析与计划制定（S4 战略层）

```
Step 1.1  运行 skill-system-health-check
          → 获取当前 PASS/NEEDS-ATTENTION/CRITICAL 状态
          → 记录所有 P0/P1 问题作为必做项

Step 1.2  运行 skill-evolution-planner-meta
          → 基于 CO-BUILD-LOG + PENDING-EXPERIENCES + SYSTEM-BLUEPRINT
          → 获取演进方向分析（补充 Phase 0 可能遗漏的条目）

Step 1.3  输出《Skill体系完善计划_[YYYYMMDD].md》，包含：
          - 目标状态描述（North Star，可量化）
          - 各条目清单（按 L1/L2/L3 分类，按 P0/P1/P2 排序）
          - 成功验收标准（与 Phase 4 逐条对照用）
          - 估计批次数量和顺序

Step 1.4  等用户确认计划文档（策略选择属于用户决策）
          IF 确认 → 进入 Phase 2
          IF 调整 → 修改计划后再确认
```

---

### Phase 2：计划双审核（等价关卡 A + B）

```
关卡 A 等价：调用 skill-simulator 子智能体
  输入：完善计划文档
  任务：以「第一次看到这个计划的 AI 执行者」视角走一遍
        找出：歧义步骤 / 触发词混淆 / 隐含假设 / 边界条件缺失
  输出：关卡A审核报告（每个发现注明 Critical/Important/Minor）

关卡 B 等价：调用 skill-system-destroyer 子智能体
  输入：完善计划文档 + SKILL-INDEX + role-menu（现有体系清单）
  任务：以「想让 Skill 体系失效的破坏者」视角审查
        找出：新旧组件冲突 / 触发词歧义 / 优先级缺失 / Rule叠加矛盾 / 死锁依赖
  输出：关卡B审核报告

处理审核发现：
  Critical → 修改计划文档后重跑对应关卡
  Important → 修改计划文档后继续
  Minor → 记录到计划的「风险项」节，执行时注意

两关都通过（或修改消解所有 Critical/Important 问题）→ 进入 Phase 3
```

---

### Phase 3：分批执行

```
Step 3.1  按 P0 → P1 → P2 顺序逐条执行
          每个条目路由到对应复杂度流程：
            L1 补丁型 → 三问 + 备份 + 修改 + 变更记录
            L2 新增型 → 调用 skill-designer（触发 关卡A + C）
            L3 集成型 → 调用 skill-designer（触发 关卡A + B + C）

Step 3.2  每批（同优先级所有条目）执行完后：
          运行 skill-system-health-check 快速验证
          IF 新 P0/P1 问题出现 → 执行 §5.2 反思机制（Step R1-R4），暂停告知用户
          IF 无新问题 → 继续下一批

Step 3.3  每个条目完成后写一行到 CO-BUILD-LOG（信号 V：任务完成）
```

---

### Phase 4：整体验证（等价关卡 C）

```
Step 4.1  运行 skill-system-health-check（六维自洽性全量检查）
Step 4.2  运行 skill-closure-verifier-meta（全系统传播完备性验证）
Step 4.3  输出《完善验证报告_[YYYYMMDD].md》，存放于：
          .cursor/skills/skill-index/
Step 4.4  逐条对照 Phase 1 验收标准：
          IF 全部通过 → 进入 Phase 5
          IF 有未达标项 → 回到 Phase 3 处理剩余条目
          IF 出现新的架构问题 → 评估是否需要新增一轮 L4
```

---

### Phase 5：经验沉淀

```
Step 5.1  【强制触发】运行 project-retrospective（批量复盘本次完善过程）
          ⚠️ 注意：Step 5.4（写任务日志）不等于 Phase 5 完成。
          必须先执行本步骤（触发 project-retrospective Skill，走其Step 1-6），
          才能标注 Phase 5 为完成。不可跳过或以写日志替代。
Step 5.2  本次发现的新原则/踩坑 → 写入 PENDING-EXPERIENCES（信号 B/C）
Step 5.3  如需更新 Skill体系设计原则_v1.0.md → 走 skill-rule-修改规范 Level 1
Step 5.4  更新 _内部总控/任务日志.md
Step 5.5  告知用户：完善项目完成，附《完善验证报告》链接
```

---

## 四、ESR 成熟度

本 Skill 当前处于**探索期**（首次创建，验证状态 🔵）。
按 §9.6 策略：允许修改，每次 project-retrospective 评估，重点快速获得真实执行反馈。

---

## 变更记录

### v1.0 — 2026-03-21 — 初始创建

**根因**：Skill体系设计原则_v1.0.md §9.2 Level 4「系统型：重构多个组件交互关系 → 暂停等用户二次确认规模」后续路径悬空，且原则文档自身建设若不遵循所规定的原则则违反自洽性。用户明确指出此问题并要求补全后再执行。

**关卡A模拟（内联，skill-simulator视角）**：
- AI执行者读到触发词「执行Skill体系完善」→ 能触发本 Skill ✅
- Phase 0 输出规模评估报告 → 步骤清晰，但「本次对话中用户提出的改动意向」需要 AI 主动读取对话上下文，有隐含假设 ⚠️（已知风险，可接受）
- Phase 2 双审核 → skill-simulator 和 skill-system-destroyer 已在系统中存在 ✅
- Phase 3 L2/L3 路由到 skill-designer → 触发词已在 role-menu 注册 ✅
- 失败路径（暂停等用户）→ 4处明确标注 ✅
- 边界（不做什么）→ S5 已明确 ✅
- 关卡A结论：Important 问题1个（隐含假设，已标注），无 Critical → 通过

**验证状态**：🔵 待验证（需真实执行 Phase 0~5 时验证各步骤有效性）

### 2026-03-21 — Phase 5 Step 5.1 强制约束补充

**根因**：首次执行时 Step 5.1 被跳过，AI 写完任务日志即宣告完成，project-retrospective 未被触发。
**修改**：Step 5.1 加入「⚠️ 不可用写任务日志替代 project-retrospective」的明确说明。
**验证状态**：🔵 待验证
