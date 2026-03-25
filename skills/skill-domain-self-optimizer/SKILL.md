---
name: skill-domain-self-optimizer
description: 基于域健康报告和沙盘Gap记录，识别断裂模式，生成具体的补全行动方案：新Skill提案/现有Skill修改建议/缺失触发链路描述。与 skill-evolution-planner-meta 的区别：后者基于历史日志做宏观演进规划；本Skill基于具体Gap证据做定向修复。触发词：「优化[域名]域」「修复[域名]域Gap」「[域名]域自优化」「根据健康报告生成修复方案」。通常由 skill-closure-verifier-meta 调用，也可独立触发。
---

# 域自我优化（skill-domain-self-optimizer）

> 关系类型：depends-on（依赖域健康报告 + 沙盘文件 + DOMAIN-REGISTRY）
> 强绑定 Rule：R2 NO_FABRICATION / R6 ARTIFACT_FIRST / R13 RULE_BEATS_STYLE

---

## 核心设计原则

**Gap → 行动** 原则：每个 Gap 必须对应一个具体可执行的行动建议（不能只说「缺什么」，必须说「用什么Skill填补、或新建什么Skill」）。

**证据优先** 原则：建议必须基于沙盘中已记录的具体 Gap，不能凭推断扩展到沙盘未覆盖的问题。

---

## 激活后立即执行

```
Step 1  确认处理范围
        询问（如果用户未指定）：
        「请指定要优化的域：
          (1) 产品开发  (2) 认知结构  (3) 公司运营  (4) 内容宣传  (5) Skill体系  (6) 全部」
        
        若是由 skill-closure-verifier-meta 调用，直接使用传入的域名称。

Step 2  读取输入数据（R3 READ_FIRST）
        并行读取：
        - _内部总控/skill-system-design/domain-health-[域名]-*.md（域健康报告，取最新）
        - _内部总控/skill-system-design/sandboxes/[域名]/*.md（该域所有沙盘）
        - _内部总控/skill-system-design/DOMAIN-REGISTRY.md（节点图）
        - _内部总控/skill-system-design/NODE-IO-CONTRACTS.md（I/O契约）
        
        若健康报告不存在：
        → 先调用 skill-domain-health-check 生成健康报告，再继续
        
        若沙盘数量 < 3：
        → 在报告中注明「沙盘样本不足，建议扩充后重新运行」
        → 但仍基于现有数据给出建议，不阻断

Step 3  Gap 分类与模式识别
        汇总所有 Gap 来源（健康报告 + 沙盘 Gap 发现表格）：
        
        按类型分类：
        - 【类型A】缺节点：对应Skill文件不存在
        - 【类型B】缺触发条件：节点间的触发边缺失或不明确
        - 【类型C】I/O不匹配：节点的输出与下游节点的输入要求不对应
        - 【类型D】文档不自洽：域内核心文档之间内容矛盾
        - 【类型E】边界盲区：入口节点未覆盖的触发词/场景
        
        识别模式：
        → 同一节点被多个沙盘标注 Gap？→ 该节点是高优先修复点
        → 同一边（触发条件）被多个沙盘标注断裂？→ 该链路是系统性缺陷

Step 4  生成行动建议
        对每类 Gap，生成对应的行动方案：
        
        【类型A处理：缺节点】
        → 直接建议：「新建 Skill [skill-name]，对应节点 [节点ID]」
        → 输出 Skill 产品定义草稿（2-3句话描述功能、触发词、I/O）
        → 标注：「建议通过 skill-designer（Level [N]）正式设计」
        
        【类型B处理：缺触发条件】
        → 定位缺失的触发边（哪个节点完成后应触发哪个下游节点）
        → 建议：「修改 [上游Skill].SKILL.md：在 [步骤N] 末尾增加触发下游的明确步骤」
        → 给出具体的修改建议文字（如：「在 Step X 末尾增加：触发条件满足时，建议用户执行 [下游节点]」）
        
        【类型C处理：I/O不匹配】
        → 定位不匹配点：上游输出的格式/路径 ≠ 下游需要的格式/路径
        → 建议：「修改 [Skill].SKILL.md：明确输出格式/路径」或「修改 NODE-IO-CONTRACTS 更正描述」
        
        【类型D处理：文档不自洽】
        → 建议触发 doc-consolidator 或 cognitive-consistency-check（域相关）
        
        【类型E处理：边界盲区】
        → 建议：「更新 [Skill].SKILL.md 的 description 触发词部分，增加 [场景描述]」

Step 5  优先级排序
        按以下规则排序行动建议：
        
        P0（立即执行）：
        - 缺节点且是关键传播路径上的节点
        - 多个沙盘均标注的相同 Gap
        
        P1（近期执行）：
        - 缺触发条件（影响闭环完整性）
        - I/O不匹配（影响数据流正确性）
        
        P2（计划执行）：
        - 边界盲区覆盖（扩展而非修复）
        - 文档自洽问题（可在下次复盘时处理）

Step 6  输出域优化建议报告（R6：必须写文件）
        写入：_内部总控/skill-system-design/domain-optimizer-[域名]-YYYYMMDD.md
        
        格式（见下方「报告格式」）
        
        同时在对话中输出摘要（已识别 N 个Gap，生成 M 条行动建议）

Step 7  路由执行建议
        P0 行动建议：
        → 询问用户：「是否现在立即处理 P0 项？」
        → 若同意：路由到对应 Skill（skill-designer / skill-rule-修改规范）
        
        P1/P2 行动建议：
        → 建议追加到 PENDING-SKILLS.md（如果是新建Skill）
        → 或告知用户「下次运行 skill-rule-修改规范 时处理」
```

---

## 报告格式

```markdown
# [域名] 域优化建议报告

**生成日期**：YYYY-MM-DD
**基于**：domain-health-[域名]-YYYYMMDD.md + [N]个沙盘
**总Gap数**：N（P0: x, P1: y, P2: z）

## Gap 模式分析

| Gap类型 | 数量 | 高频节点 |
|---|---|---|
| 缺节点 | N | [节点ID列表] |
| 缺触发条件 | N | [边列表] |
| I/O不匹配 | N | [节点ID列表] |
| 文档不自洽 | N | [文档对] |
| 边界盲区 | N | [Skill列表] |

## P0 行动建议（立即执行）

### P0-[序号]：[行动标题]

- **Gap来源**：[沙盘ID] Gap # [N] / 健康报告 [节点]
- **Gap描述**：[具体问题]
- **行动类型**：[新建Skill / 修改现有Skill / 更新DOMAIN-REGISTRY]
- **行动建议**：[具体执行步骤]
- **执行方式**：触发 [skill-name] 执行

## P1 行动建议（近期执行）

[同上格式]

## P2 行动建议（计划执行）

[同上格式]

## 新建 Skill 草案（如有）

| Skill名称 | 功能描述 | 触发词 | 输入 | 输出 | 建议级别 |
|---|---|---|---|---|---|
| [name] | [1句话] | [触发词] | [输入文档] | [输出产物] | L[N] |

## 结论

[总结：最高优先级的行动是什么，预计可以解决多少比例的传播不完备问题]
```

---

## 常见失败模式

**失败模式1**：扩展建议超出已有Gap证据，变成「AI认为应该有的东西」而非「沙盘中证明缺失的东西」
→ 预防：每条行动建议必须引用「Gap来源」（沙盘ID + Gap行号），无法引用则不写入报告

**失败模式2**：类型A（缺节点）的行动建议直接生成完整的 SKILL.md，绕过了 skill-designer 的设计流程
→ 预防：Step 4 类型A处理只输出「Skill草案（2-3句话）」，明确标注「需通过 skill-designer 正式设计」，不直接生成完整Skill

**失败模式3**：所有 Gap 都被标注为 P0，失去优先级区分
→ 预防：P0 必须满足「缺节点且在关键传播路径上」OR「多个沙盘均标注相同Gap」两个硬性判断条件

---

## 与其他 Skill 的关系

| Skill | 关系 |
|---|---|
| `skill-domain-health-check` | 输入来源：健康报告是本Skill的主要输入 |
| `skill-closure-verifier-meta` | 被调用方：meta 编排器调用本Skill |
| `skill-designer` | 路由目标：P0类型A建议会路由到skill-designer |
| `skill-rule-修改规范` | 路由目标：P0/P1类型B/C建议会路由到此 |
| `skill-evolution-planner-meta` | 区别：后者做宏观演进规划，本Skill做Gap定向修复 |

---

## 变更记录

### v1.0 — 2026-03-19 — 初始创建

**根因**：需要一个从「发现Gap」到「具体行动方案」的转化机制。现有 skill-evolution-planner-meta 基于历史日志做宏观规划，不能对具体的沙盘Gap证据做定向修复建议。

**验证状态**：🔵 待验证（首次创建，在首次运行时验证）
