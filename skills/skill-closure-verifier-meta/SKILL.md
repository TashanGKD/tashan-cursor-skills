---
name: skill-closure-verifier-meta
description: 元级闭环验证编排器。读取五域形式化描述（DOMAIN-REGISTRY + NODE-IO-CONTRACTS），两阶段（Phase 1预想/Phase 2实际）执行沙盘验证，调用 skill-domain-health-check 检查传播完备性，调用 skill-domain-self-optimizer 生成修复方案，输出带证据链的全系统闭环验证报告。这是整个Skill体系自我验证的最高入口。触发词：「运行元验证」「闭环验证」「验证Skill体系传播完备性」「系统闭环检查」「全域验证」「元系统运行」。
---

# 元级闭环验证编排器（skill-closure-verifier-meta）

> 关系类型：triggers（触发 skill-domain-health-check + skill-domain-self-optimizer）
> 关系类型：depends-on（依赖 DOMAIN-REGISTRY + NODE-IO-CONTRACTS + 沙盘库）
> 强绑定 Rule：R2 NO_FABRICATION / R3 READ_FIRST / R6 ARTIFACT_FIRST / R1 EVIDENCE_FIRST

---

## 核心设计原则

**两阶段分离**：Phase 1（预想）必须在不参考现有 Skill 实现细节的情况下完成。这防止了「验证者被被验证的系统污染」的自我确认偏误。

**证据链完整**：每个 Gap 必须有具体的证据（文件路径 + 步骤描述），不允许模糊归因。

**可重复运行**：每次运行产出独立的报告文件（含日期），不覆盖旧报告，支持对比演进。

---

## 激活后立即执行

```
Step 1  前置检查（硬性门槛）
        检查以下文件是否存在：
        - _内部总控/skill-system-design/DOMAIN-REGISTRY.md
        - _内部总控/skill-system-design/NODE-IO-CONTRACTS.md
        - _内部总控/skill-system-design/SANDBOX-FORMAT.md
        
        若任一文件不存在：
        → 停止执行，明确告知「元验证所需的形式化描述文档缺失」
        → 说明哪个文件缺失，以及如何创建它
        → 不允许「跳过缺失文件继续执行」
        
        若文件存在但有明显过期迹象（最后修改时间 > 30天）：
        → 告知用户「形式化文档可能需要更新」，询问是否继续

Step 2  读取系统全景（R3 READ_FIRST 强制）
        用 explore 子智能体并行完成以下读取：
        
        组A（必须完成后才能进入 Phase 1）：
        - DOMAIN-REGISTRY.md：读取五域节点图和终态定义
        - NODE-IO-CONTRACTS.md：读取所有节点的I/O契约
        - .cursor/skills/skill-index/SKILL-INDEX.md：读取现有37个Skill的状态
        
        组B（为 Phase 2 准备）：
        - _内部总控/skill-system-design/sandboxes/ 所有子目录中的文件列表
        - .cursor/rules/role-menu.mdc：触发词路由规则

Step 3  Phase 1：预想验证（两阶段的第一阶段）
        
        ⚠️ 重要约束：此阶段不允许打开任何 SKILL.md 文件。
        Phase 1 的标准是「理想系统」，与现有实现无关。
        
        对每个域（5个域），执行以下操作：
        
        3.1 读取该域在 DOMAIN-REGISTRY 中的节点图和终态定义
        3.2 读取该域所有入口节点的 I/O 契约（从 NODE-IO-CONTRACTS）
        3.3 预想：若系统完美，从每个入口节点输入后，应该发生什么？
            - 预想触发链路：[入口] → [中间节点...] → [终态]
            - 预想终态输出：应该产出哪些文档/状态/产物
            - 预想自洽检查点：哪些文档应该相互一致
        3.4 将预想结果记录为「Phase 1 预想记录」（暂存在工作内存，不写文件）
        
        本步骤预计输出：5域 × N个入口节点 × 预想链路记录

Step 4  Phase 2：实际验证（两阶段的第二阶段）
        
        ⚠️ 注意：此阶段需要读取实际的 SKILL.md 文件，与 Phase 1 的预想对比。
        
        对每个域的每个沙盘文件（sandboxes/[域]/*.md）：
        
        4.1 读取沙盘的「Phase 2 实际验证」部分
            - 若状态为 "validated"（无Gap）：记录为通过，无需额外验证
            - 若状态为 "gap-found"：提取Gap列表
            - 若状态为 "draft"（Phase 2未完成）：对该沙盘执行实际验证
        
        4.2 对 "draft" 状态的沙盘，补全 Phase 2：
            读取该沙盘中涉及的每个节点的 SKILL.md（此时才读Skill文件）
            逐节点验证：触发了吗 / 输出了吗 / 触发下游了吗
            更新沙盘文件状态（draft → validated 或 gap-found）
        
        4.3 对照 Phase 1 预想：
            Phase 1 预想链路 vs Phase 2 实际链路 → 差异 = Gap 候选
            仅保留有沙盘证据支持的 Gap（无证据的不记录）

Step 5  Gap 汇总与分级
        汇总所有域的 Gap：
        
        5.1 合并来源：沙盘 Gap + Phase 1 vs Phase 2 对比差异
        
        5.2 为每个 Gap 分级：
            P0：传播完全断裂 / 缺失关键节点（Skill文件不存在）/ 系统无法自洽
            P1：触发条件缺失 / I/O不匹配 / 部分传播路径断裂
            P2：边界盲区 / 体验优化项（闭环完整但不够流畅）
        
        5.3 去重：相同根因的 Gap 合并为一条
        
        5.4 为每条 Gap 确认证据：
            - 沙盘文件路径（sandbox-ID + Gap行号）
            - 相关 Skill 文件路径
            - 具体说明（R2 NO_FABRICATION：无法找到具体证据的Gap不记录）

Step 6  调用 skill-domain-health-check（各域）
        对每个域调用 skill-domain-health-check，传入域名：
        
        → 等待各域健康报告生成
        → 将传播完备性检查结果纳入总报告
        
        若某域的健康报告已存在且日期为今天，跳过重复生成。

Step 7  调用 skill-domain-self-optimizer（有Gap的域）
        对 Step 5 中识别出有 P0 或 P1 Gap 的域：
        
        → 调用 skill-domain-self-optimizer，传入域名
        → 等待优化建议报告生成
        → 将行动建议纳入总报告的「整改计划」部分

Step 8  输出总验证报告（R6：必须写文件）
        写入：_内部总控/skill-system-design/validation-report-YYYYMMDD.md
        
        格式（见下方「总报告格式」）

Step 9  呈现摘要与下一步建议
        在对话中输出：
        - 验证覆盖范围（几个域/几个沙盘/几个节点）
        - 发现的总 Gap 数（P0: x, P1: y, P2: z）
        - 最高优先级的行动建议（P0项）
        - 是否建议立即执行修复
```

---

## 总报告格式

```markdown
# Skill 体系闭环验证总报告

**验证日期**：YYYY-MM-DD
**验证版本**：[基于 DOMAIN-REGISTRY 和 NODE-IO-CONTRACTS 的版本]
**覆盖范围**：5域 / [N]个沙盘 / [M]个节点

---

## Phase 1 vs Phase 2 对比摘要

| 域 | 预想链路数 | 实际验证链路数 | 一致率 |
|---|---|---|---|
| 产品开发 | N | N | X% |
| 认知结构 | N | N | X% |
| 公司运营 | N | N | X% |
| 内容宣传 | N | N | X% |
| Skill体系 | N | N | X% |

---

## 域健康状态

| 域 | 节点完整性 | 传播完备性 | I/O契约 | 沙盘Gap数 | 整体状态 |
|---|---|---|---|---|---|
| 产品开发 | ✅/⚠️/❌ | ✅/⚠️/❌ | ✅/⚠️/❌ | N | PASS/WARN/CRITICAL |

---

## 全域 Gap 清单

### P0 Gap（必须修复，影响核心闭环）

| # | 域 | Gap描述 | 类型 | 证据来源 |
|---|---|---|---|---|

### P1 Gap（近期修复，影响传播效率）

| # | 域 | Gap描述 | 类型 | 证据来源 |
|---|---|---|---|---|

### P2 Gap（优化项）

| # | 域 | Gap描述 | 类型 | 证据来源 |
|---|---|---|---|---|

---

## 整改计划（来自各域 skill-domain-self-optimizer）

[各域优化建议报告的摘要，按P0/P1/P2分组]

---

## 跨域关系检查

| 跨域触发链路 | 状态 | Gap（如有） |
|---|---|---|
| 产品开发-RETRO → Skill体系-CAPTURE_IN | ✅/❌ | [描述] |
| 认知结构-FRAG_IN → 产品开发-ITER_IN | ✅/❌ | [描述] |
| 公司运营-HISTORY_IN → Skill体系-EVOLVE_IN | ✅/❌ | [描述] |
| 内容宣传-PROOF → Skill体系-MODIFY_IN | ✅/❌ | [描述] |

---

## 系统整体结论

**整体自洽性**：PASS / NEEDS-ATTENTION / CRITICAL
**总Gap数**：N（P0: x, P1: y, P2: z）
**最高优先级行动**：[1-3条最关键的行动建议]
**建议下次验证时间**：[下次运行 skill-closure-verifier-meta 的建议时间]
```

---

## 常见失败模式

**失败模式1**：Phase 1 和 Phase 2 混淆——在 Phase 1 中参考了现有 SKILL.md，导致预想被现有实现污染
→ 预防：Step 3 明确注明「⚠️ 此阶段不允许打开任何 SKILL.md 文件」，AI必须遵守

**失败模式2**：Gap 来自推断而非证据，导致报告中充斥「可能有问题」而无具体证明
→ 预防：Step 5.4 要求每条 Gap 必须有沙盘来源（sandbox-ID + 行号），无证据不记录

**失败模式3**：跳过 skill-domain-health-check / skill-domain-self-optimizer 调用，直接自己输出优化建议
→ 预防：Step 6-7 明确「调用子技能」，本Skill只做编排，不自己做健康检查和优化建议

**失败模式4**：沙盘数量为0时全部推断，导致整份报告无实际价值
→ 预防：沙盘数量 < 5（全域合计）时，在报告开头明确标注「⚠️ 沙盘样本严重不足，验证结论可靠性低」

---

## 与其他 Skill 的关系

| Skill | 关系 |
|---|---|
| `skill-domain-health-check` | 被编排：本Skill调用，负责传播完备性检查 |
| `skill-domain-self-optimizer` | 被编排：本Skill调用，负责生成修复方案 |
| `skill-system-health-check` | 互补：后者检查内部一致性，本Skill检查传播完备性和跨域闭环 |
| `skill-evolution-planner-meta` | 共同消费 CO-BUILD-LOG 等历史数据，但关注点不同 |
| `DOMAIN-REGISTRY.md` | 必须依赖，Phase 1 的形式化来源 |
| `NODE-IO-CONTRACTS.md` | 必须依赖，I/O验证的形式化来源 |
| `sandboxes/*` | 必须依赖，Phase 2 的证据来源 |

---

## 变更记录

### v1.0 — 2026-03-19 — 初始创建

**根因**：Skill体系缺少从「预想」到「实际」的两阶段验证机制，现有工具（skill-system-health-check / skill-evolution-planner-meta）只能检查内部状态或规划演进方向，无法做「任意输入→完整闭环」的传播完备性验证。

**设计核心**：两阶段分离（Phase 1 不看Skill实现，Phase 2 才逐节点对照）防止验证者被验证对象污染，是整个元系统的关键创新。

**验证状态**：🔵 待验证（首次创建，在首次运行时验证）
