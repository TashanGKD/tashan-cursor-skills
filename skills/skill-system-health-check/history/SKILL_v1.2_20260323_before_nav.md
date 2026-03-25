---
name: skill-system-health-check
description: Skill体系自洽性审查 Skill（由用户主动触发，不被其他组件调用）。主动检查整个Skill/Agent/Rule体系的内部一致性：触发词冲突、孤立组件、版本漂移、SKILL-INDEX与实际文件不一致、alwaysApply Rule叠加矛盾等。对应产品侧的 project-closeout。注意：与 skill-system-destroyer（子智能体，只读审查新组件冲突）不同——本 Skill 审查整个体系的历史一致性。触发词：「检查Skill体系」「Skill体系有没有问题」「Skill体系自检」「Skill体系自洽性」「Skill健康检查」。
---

# Skill 体系自洽性审查（skill-system-health-check）

> 对应关系：
> - project-closeout → 项目文档一致性检查
> - **skill-system-health-check → Skill/Agent/Rule 体系一致性检查**
>
> 强绑定 Rule：R2 NO_FABRICATION / R3 READ_FIRST / R6 ARTIFACT_FIRST

---

## 激活后立即执行

```
Step 1  读取 Skill 体系全量索引（R3 READ_FIRST）
        用 explore 子智能体并行读取：
        - .cursor/skills/skill-index/SKILL-INDEX.md（必读）
        - .cursor/rules/role-menu.mdc（必读）
        - .cursor/rules/ 目录下所有 .mdc 文件的 description 字段
        - .cursor/skills/ 目录结构（验证 SKILL-INDEX 与实际文件是否对齐）
        - .cursor/agents/ 目录结构（验证子智能体注册是否完整）

Step 2  执行六维自洽性检查

        【维度1：触发词冲突检查】
        对照 role-menu.mdc 和每个 Skill 的 description：
        → 有没有两个 Skill 的触发词高度重叠（语义相似度 > 70%）？
        → 用户说某句话，会同时匹配两个 Skill 吗？
        → 有没有 Skill 的触发词已被更精确的新 Skill 覆盖但旧 Skill 未更新？

        【维度2：孤立组件检查】
        → 有没有在 SKILL-INDEX 里注册但在 role-menu.mdc 里没有的 Skill？
        → 有没有被其他 Skill/Agent 调用但未在 SKILL-INDEX 注册的组件？
        → 有没有在 role-menu.mdc 的「配套文件」表格里引用但不存在的文件路径？

        【维度3：版本漂移检查】
        → SKILL-INDEX 里记录的版本号，与实际 SKILL.md 底部变更记录中的最新版本是否一致？
        → 有没有 Skill 被修改了但 SKILL-INDEX 版本号没有更新？

        【维度4：alwaysApply Rule 叠加矛盾检查】
        → 读取所有 alwaysApply: true 的 Rule 文件
        → 检查：有没有两条规则在同一场景下指向相反的行为？
        → 检查：knowledge-integrity-rules.mdc 的 R1-R15 与其他 Rule 是否有冲突？

        【维度5：子智能体 I/O 契约检查】
        → 所有 .cursor/agents/*.md 的 description 是否都说明了：谁调用它、输入是什么、输出是什么？
        → 有没有子智能体被 Skill 调用但该子智能体文件不存在？

        【维度6：PENDING-SKILLS 状态一致性】
        → PENDING-SKILLS.md 里标注为「已完成」的 Skill，在 SKILL-INDEX 里是否存在？
        → PENDING-SKILLS 里的 P0 项是否长期未处理（超过 2 周）？

Step 3  输出「Skill 体系健康报告」（R6：必须写文件）
        写入：.cursor/skills/skill-index/skill-health-report-YYYYMMDD.md

Step 4  路由后续动作
        P0 问题（触发词严重冲突 / 文件路径错误 / alwaysApply 矛盾）：
        → 立即输出警告标注：「🔴 P0 问题需要立即修复——此问题会导致 Skill 体系无法正常工作」
        → 自动引导用户修复：「建议说「这里有个规范问题，帮我修复」，触发 project-convention-resolver（E类：Skill/Rule文件），由其统一记录+路由执行 skill-rule-修改规范+验证闭环」
        → 告知用户：「P0 问题未修复时，不建议继续使用相关 Skill」

        P1 问题（版本漂移 / 孤立组件 / 描述不清晰）：
        → 加入 PENDING-SKILLS 或在本次立即修复（用户选择）

        P2 问题（优化项）：
        → 告知用户，建议下次 skill-evolution-planner 运行时一并考虑
```

---

## 报告格式

```markdown
# Skill 体系健康报告

**检查日期**：YYYY-MM-DD
**覆盖范围**：N 个 Skill / M 个 Agent / K 个 Rule

## 维度检查结果

| 维度 | 状态 | 发现 |
|---|---|---|
| 触发词冲突 | ✅/⚠️/❌ | [摘要] |
| 孤立组件 | ✅/⚠️/❌ | [摘要] |
| 版本漂移 | ✅/⚠️/❌ | [摘要] |
| Rule 叠加矛盾 | ✅/⚠️/❌ | [摘要] |
| Agent I/O 契约 | ✅/⚠️/❌ | [摘要] |
| PENDING-SKILLS 状态 | ✅/⚠️/❌ | [摘要] |

## P0 问题（必须修复）
| # | 问题描述 | 涉及组件 | 建议动作 |
|---|---|---|---|

## P1 问题（建议修复）
[同上格式]

## P2 优化项
[同上格式]

## 结论
[PASS / NEEDS-ATTENTION]
```

---

## 常见失败模式

失败模式1：维度2检查时遍历文件过多，AI 只读了部分目录就开始分析
→ 预防：Step 1 明确「必须读完 SKILL-INDEX 和 role-menu.mdc 全文，才能进入 Step 2」

失败模式2：触发词冲突判断过于严格，把「类似但不同」的 Skill 标为冲突
→ 预防：触发词重叠需同时满足「语义相似度 > 70%」AND「用户会在同一场景使用」，两个条件才算冲突

---

## 变更记录

### v1.1 → v1.2 — 2026-03-22 — P0路由改为 project-convention-resolver（GAP-SK017-1 修复）

**根因**：scenario-sandbox-builder Phase 2 验证（SK-017沙盘）发现：Step 4 P0路由直接引导用户触发 skill-rule-修改规范，绕过了 project-convention-resolver 的统一「记录+路由+验证+闭环」层。导致P0修复缺少追踪台记录和闭环验证。

**修改内容**：
- 修改：Step 4 P0路由「自动引导修复」文字 → 从「触发 skill-rule-修改规范」改为「触发 project-convention-resolver（E类：Skill/Rule文件），由其统一记录+路由+验证+闭环」
- 备份路径：`history/SKILL_v1.1_20260322_before_sk017.md`

**验证方法**：发现P0问题时，引导词应提及 project-convention-resolver 而非直接提 skill-rule-修改规范
**验证状态**：🔵 待验证

---

### v1.1 — 2026-03-19 — P0 问题路由加强（SK-002 Gap 修复）

**根因**：SK-002 沙盘发现：skill-system-health-check 发现 P0 问题后只「建议」修复，没有强制触发机制，P0 问题可能长期存在而未被处理。

**修改内容**：
- 修改：Step 4 P0 路由 → 从「建议通过...修复」改为「立即警告 + 强制引导修复 + 告知不建议继续使用」

**验证状态**：🔵 待验证

---

### v1.0 — 2026-03-19 — 初始创建

**根因**：Skill 体系缺少等价于 project-closeout 的自洽性检查机制，无法主动发现触发词冲突、版本漂移等问题。

**验证状态**：🔵 待验证（关卡A/B/C 已通过设计阶段模拟）
