---
name: skill-evolution-planner-meta
description: Skill体系演进规划 Skill。基于CO-BUILD-LOG（决策轨迹）、PENDING-EXPERIENCES（踩坑模式）、PENDING-SKILLS（需求积压）和SYSTEM-BLUEPRINT（体系蓝图），主动分析Skill体系的演进方向——哪些Skill应该新建、哪些应该合并/拆分、哪些描述需要重写、哪些触发词需要调整、整体编排架构是否需要升级。对应产品侧的 product-evolution-planner。触发词：「Skill体系怎么演进」「Skill体系应该怎么完善」「有没有新的Skill需要建」「Skill体系演进建议」「主动分析Skill体系」「Skill体系下一步」。
---

# Skill 体系演进规划（skill-evolution-planner-meta）

> 对应关系：
> - product-evolution-planner → 对照产品原则，主动规划产品演进
> - **skill-evolution-planner-meta → 对照积累的模式，主动规划 Skill 体系演进**
>
> 强绑定 Rule：R2 NO_FABRICATION / R3 READ_FIRST / R1 EVIDENCE_FIRST / R6 ARTIFACT_FIRST

---

## 知识导航表（执行前必须理解的概念根）

| 层级 | 文档 | 需要理解的概念 |
|---|---|---|
| **D0 认知根（必读）** | `_内部总控/认知结构/L1_系统性文档/系统架构思维维度/自进化智能体系统形式规范_v1.0.md` | 层2：自进化定义（系统能检测并消除自身Gap）；层5：G（间隙感知）→M（变更引擎）→R（注册表）完整闭环 |
| **D3 规范参考** | `_内部总控/认知结构/L1_系统性文档/系统架构思维维度/Skill体系设计原则_v1.0.md` | §1 唯一最终原则（自我进化能力）；§2.5 三型统一决策树 |
| **D4 运行时数据** | `.cursor/skills/skill-index/PENDING-EXPERIENCES.md` + `CO-BUILD-LOG.md` + `PENDING-SKILLS.md` + `SYSTEM-BLUEPRINT.md` | G缓冲区（已积累的Gap信号）+ 需求积压 + 体系蓝图 |

**核心概念速查**：
① 演进规划 = S4层智能（环境感知+战略分析），不是修复现有Gap而是规划未来的Gap
② 证据驱动：每条建议必须引用≥2次历史记录（CO-BUILD-LOG或PENDING-EXPERIENCES）
③ 输出必须是正式文件（R6 ARTIFACT_FIRST）：skill-evolution-plan-YYYYMMDD.md

---

## 激活后立即执行

```
Step 1  读取 Skill 体系的历史积累数据（R3 READ_FIRST）
        用 explore 子智能体并行读取：
        - .cursor/skills/skill-index/CO-BUILD-LOG.md（决策轨迹，过程层）
        - .cursor/skills/skill-index/PENDING-EXPERIENCES.md（踩坑模式，结果层）
        - .cursor/skills/skill-index/PENDING-SKILLS.md（需求积压）
        - .cursor/skills/skill-index/SYSTEM-BLUEPRINT.md（体系蓝图）
        - .cursor/skills/skill-index/SKILL-INDEX.md（当前状态）
        
        若某个文件不存在，跳过并在报告中标注「未找到」。

Step 2  从五个维度分析演进方向（R1 EVIDENCE_FIRST：每条必须引用具体数据来源）

        【维度1：重复模式 → 候选新 Skill】
        分析 PENDING-EXPERIENCES 和 CO-BUILD-LOG：
        → 哪类「踩坑/新发现」反复出现（≥2次）但没有对应 Skill？
        → CO-BUILD-LOG 中有没有「缺失 Skill」类型（E 类）的重复记录？
        → 这些模式是否已在 PENDING-SKILLS 中？若没有，应该加入。

        【维度2：架构压力 → 候选重构】
        分析 CO-BUILD-LOG 中的「转折/方向调整」（III 类条目）：
        → 哪些转折揭示了当前 Skill 体系的架构缺陷（不只是单个 Skill 的问题）？
        → 有没有多个 Skill 因相似原因被修改，暗示应该合并或提取公共机制？
        → 触发词体系是否已经变得复杂到用户难以记忆？

        【维度3：PENDING-SKILLS 优先级校准】
        → 当前 PENDING-SKILLS 的优先级排序是否仍然合理？
        → 有没有本来是 P0 但因为新情况变成了不那么紧急的项？
        → 有没有新出现的需求比现有 P0 更紧急？

        【维度4：SYSTEM-BLUEPRINT 准确性】
        → SYSTEM-BLUEPRINT.md 描述的任务类型清单是否仍然准确？
        → 有没有新的高频任务类型在蓝图中未被记录？
        → 子智能体编排方案是否需要更新？

        【维度5：Skill 质量层次分析】
        → SKILL-INDEX 中有多少 Skill 仍为「🔵 待验证」状态？
        → CO-BUILD-LOG 或 PENDING-EXPERIENCES 中，哪些 Skill 出现了「✅ 验证通过」的记录？
          → 这些 Skill 可以升级为「✅ 已验证」
        → 哪些 Skill 的「🔵 待验证」状态持续存在，且从未在 CO-BUILD-LOG/PENDING-EXPERIENCES 中出现过？
          → 可能从未被使用，考虑合并或废弃

Step 3  生成演进建议清单
        对每条建议：
        - 建议标题（一句话）
        - 数据来源（引用 CO-BUILD-LOG/PENDING-EXPERIENCES 的具体条目）
        - 建议类型：新建/重构/合并/废弃/描述更新/触发词调整/架构升级
        - 优先级：P0/P1/P2
        - 路由：→ skill-designer Level 2/3 / skill-rule-修改规范 Level 1

Step 4  输出「Skill 体系演进建议报告」（R6：必须写文件）
        写入：.cursor/skills/skill-index/skill-evolution-plan-YYYYMMDD.md

Step 5  路由询问
        「📊 Skill 体系演进分析完成。共发现 N 条建议（P0: N，P1: N，P2: N）。
        
          是否现在执行某项？
          - 新建/重构 → 加载 skill-designer（Level 2/3）
          - 修改描述/触发词 → 按 skill-rule-修改规范 Level 1
          - 加入需求积压 → 更新 PENDING-SKILLS.md
          - [选择某条执行] [先看报告，稍后决定]」
```

---

## 报告格式

```markdown
# Skill 体系演进建议报告

**分析日期**：YYYY-MM-DD
**数据来源**：CO-BUILD-LOG N 条 / PENDING-EXPERIENCES N 条 / PENDING-SKILLS N 项

## 维度分析摘要

| 维度 | 状态 | 关键发现 |
|---|---|---|
| 重复模式（候选新Skill）| ✅/⚠️ | [摘要] |
| 架构压力（候选重构）| ✅/⚠️ | [摘要] |
| PENDING-SKILLS 优先级 | ✅/⚠️ | [摘要] |
| SYSTEM-BLUEPRINT 准确性 | ✅/⚠️ | [摘要] |
| Skill 质量层次 | ✅/⚠️ | [摘要] |

## P0 演进建议（最高价值/最紧急）

### P0-01 [建议标题]
**数据来源**：[引用具体条目]
**建议类型**：新建/重构/合并/废弃/描述更新
**路由**：skill-designer Level [N] / skill-rule-修改规范 Level 1

## P1 演进建议
[同上格式]

## P2 中长期方向
[同上格式]

## PENDING-SKILLS 更新建议
需要新增到需求池：[列表]
需要调整优先级：[列表]

## 结论
[一段话：Skill 体系当前最大的演进机会是什么]
```

---

## 常见失败模式

失败模式1：建议过于泛泛，没有引用具体数据
→ 预防：每条建议必须引用 CO-BUILD-LOG 或 PENDING-EXPERIENCES 的具体条目编号

失败模式2：把「这次遇到的具体问题」错误地升格为「体系架构问题」
→ 预防：建议需要在历史数据中有 ≥2 次相似记录才能升格为架构级问题

---

## 变更记录

### v1.0 — 2026-03-19 — 初始创建

**根因**：Skill 体系缺少等价于 product-evolution-planner 的主动演进规划机制，无法基于历史积累数据主动发现体系改进机会。

**验证状态**：🔵 待验证
