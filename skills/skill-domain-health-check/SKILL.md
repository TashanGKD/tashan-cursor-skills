---
name: skill-domain-health-check
description: 按域检查Skill体系的传播完备性：所有节点可达、I/O契约满足、任意入口可触发相关闭环终态。与 skill-system-health-check 互补——后者检查内部一致性（版本/触发词/文件存在），本Skill检查跨节点的传播完备性（任意输入能否完整走完闭环）。触发词：「检查[域名]域健康」「[域名]域传播完备性检查」「域健康报告」「[域名]闭环是否完整」。通常由 skill-closure-verifier-meta 调用，也可独立触发。
---

# 域健康检查（skill-domain-health-check）

> 关系类型：depends-on（依赖 DOMAIN-REGISTRY.md + NODE-IO-CONTRACTS.md）
> 强绑定 Rule：R2 NO_FABRICATION / R3 READ_FIRST / R6 ARTIFACT_FIRST

---

## 检查目标

对指定域（或全部5个域）执行传播完备性验证：

1. **节点完整性**：DOMAIN-REGISTRY 中的所有节点对应的 Skill 文件真实存在
2. **I/O 契约满足**：NODE-IO-CONTRACTS 中每个节点的输入条件是否可被满足，输出产物是否有明确路径
3. **传播完备性**：从任意入口节点出发，是否至少有一条路径能到达终态节点
4. **域内文档自洽**：域内产生的核心文档（产品定义/技术架构等）之间是否互相引用一致

---

## 激活后立即执行

```
Step 1  确认检查范围
        询问（如果用户未指定）：
        「请指定要检查的域：
          (1) 产品开发  (2) 认知结构  (3) 公司运营  (4) 内容宣传  (5) Skill体系  (6) 全部」
        
        确认后继续 Step 2。

Step 2  读取形式化描述（R3 READ_FIRST）
        用 explore 子智能体并行读取：
        - _内部总控/skill-system-design/DOMAIN-REGISTRY.md（必读）
        - _内部总控/skill-system-design/NODE-IO-CONTRACTS.md（必读）
        - 目标域对应的沙盘文件目录（_内部总控/skill-system-design/sandboxes/[域名]/）
        
        若任一必读文件不存在：
        → 停止执行，告知用户「形式化描述文档缺失，无法执行域健康检查」
        → 建议先运行 DOMAIN-REGISTRY 和 NODE-IO-CONTRACTS 初始化

Step 3  检查一：节点完整性
        对 DOMAIN-REGISTRY 中指定域的每个节点：
        
        → 读取节点对应的 Skill 路径（通常为 .cursor/skills/[skill-name]/SKILL.md）
        → 验证文件是否真实存在（用 Glob 或 ls 确认）
        
        记录：
        - ✅ 节点存在：[节点ID] → [Skill路径]
        - ❌ 节点缺失：[节点ID] → Skill文件不存在（Gap类型：缺节点）

Step 4  检查二：I/O 契约满足度
        对 NODE-IO-CONTRACTS 中指定域的每个节点契约：
        
        【输入侧检查】
        → 该节点的「必需上游文档」路径是否在系统中有可能被创建？
        → 该节点的「必需上下文」是否有明确的创建机制？
        
        【输出侧检查】
        → 该节点的「主产物」文件路径是否明确（非「内联输出」类）？
        → 若为「内联输出」：是否有说明「什么时候保存为文件」？
        
        记录：
        - ✅ I/O清晰
        - ⚠️ I/O模糊：[具体模糊点]（Gap类型：I/O不匹配）

Step 5  检查三：传播完备性（核心检查）
        以「图可达性」思维方式执行：
        
        对指定域的每个入口节点：
        → 从该节点出发，沿 DOMAIN-REGISTRY 中的触发边前进
        → 判断：是否至少有一条路径能到达该域的至少一个终态节点
        → 记录路径：[入口节点] → [中间节点...] → [终态节点]
        
        如果某入口节点无法到达任何终态节点：
        → 记录为传播不完备 Gap（Gap类型：传播断裂）
        → 标注断裂点（哪条边缺失或哪个节点有缺陷）
        
        如果某中间节点对所有其出边的触发条件都无法满足：
        → 记录为「死胡同节点」（Gap类型：触发条件不可达）

Step 6  检查四：沙盘 Gap 汇总
        读取该域所有沙盘文件（sandboxes/[域名]/*.md）：
        → 统计 status = "gap-found" 的沙盘数量
        → 提取所有 Gap 条目（「Gap发现」表格中有Gap的行）
        → 按类型分类（缺节点/缺触发/I-O不匹配/文档不自洽）
        → 统计各类型数量
        
        沙盘 Gap 是已有证据的直接来源，权重高于推断。

Step 7  输出域健康报告（R6：必须写文件）
        写入：_内部总控/skill-system-design/domain-health-[域名]-YYYYMMDD.md
        
        格式（见下方「报告格式」）
        
        同时在对话中输出摘要（1-3句话总结）

Step 8  路由后续动作
        P0 问题（缺节点 / 传播完全断裂）：
        → 立即告知用户，建议优先触发 skill-domain-self-optimizer
        
        P1 问题（I/O模糊 / 沙盘有Gap未修复）：
        → 追加到域优化队列，建议下次触发 skill-domain-self-optimizer
        
        P2 优化项：
        → 记录在报告中，不主动路由
```

---

## 报告格式

```markdown
# [域名] 域健康报告

**检查日期**：YYYY-MM-DD
**域名**：[域名]
**覆盖节点数**：N

## 检查结果摘要

| 检查项 | 状态 | 发现数 |
|---|---|---|
| 节点完整性 | ✅/⚠️/❌ | N个Gap |
| I/O契约满足度 | ✅/⚠️/❌ | N个Gap |
| 传播完备性 | ✅/⚠️/❌ | N条路径断裂 |
| 沙盘Gap汇总 | ✅/⚠️/❌ | N个已记录Gap |

## P0 问题（缺节点 / 传播完全断裂）

| # | 节点 | 问题描述 | 证据 |
|---|---|---|---|

## P1 问题（I/O模糊 / 触发断裂）

| # | 节点/路径 | 问题描述 | Gap类型 | 沙盘来源 |
|---|---|---|---|---|

## P2 优化项

[同上格式]

## 传播路径图（仅显示不完备的路径）

[入口节点] → ❌ [断裂点] → [无法到达的终态节点]

## 结论

**整体状态**：PASS / NEEDS-ATTENTION / CRITICAL
**总Gap数**：N（P0: x, P1: y, P2: z）
**建议下一步**：[触发 skill-domain-self-optimizer / 直接修复 / 无需行动]
```

---

## 常见失败模式

**失败模式1**：Step 5 传播检查时，AI 只检查了「直接下游」而没有追踪完整路径到终态
→ 预防：「至少有一条路径能到达终态节点」——必须一直追踪到终态，不能停在中间节点

**失败模式2**：节点完整性检查时只检查了 SKILL-INDEX 有没有记录，没有验证文件真实存在
→ 预防：Step 3 明确要求「用 Glob 或 ls 确认」文件路径，不允许只查 SKILL-INDEX

**失败模式3**：沙盘数量为0时直接跳过 Step 6，漏掉对历史沙盘结论的汇总
→ 预防：若沙盘为空，在报告中注明「无沙盘记录，无法汇总Gap证据」，不要跳过这一项

---

## 与其他 Skill 的关系

| Skill | 关系 |
|---|---|
| `skill-system-health-check` | 互补：后者检查内部一致性，本Skill检查传播完备性 |
| `skill-closure-verifier-meta` | 被调用方：meta 编排器调用本Skill |
| `skill-domain-self-optimizer` | 输出消费方：本Skill的报告是 optimizer 的主要输入 |
| `DOMAIN-REGISTRY.md` | 必须依赖：节点图的形式化来源 |
| `NODE-IO-CONTRACTS.md` | 必须依赖：I/O契约的形式化来源 |

---

## 变更记录

### v1.0 — 2026-03-19 — 初始创建

**根因**：现有 skill-system-health-check 只检查六维内部一致性，不检查跨节点传播完备性（任意输入能否触发完整闭环）。需要独立的域健康检查 Skill 来填补这一空白。

**验证状态**：🔵 待验证（首次创建，在首次运行时验证）
