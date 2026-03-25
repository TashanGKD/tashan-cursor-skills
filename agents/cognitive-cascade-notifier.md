---
name: cognitive-cascade-notifier
description: 认知级联通知器（后台异步）。当 L1.5 新原则被确认或 L1 文档发生重大更新时，后台分析五域工作节点，将需要重新对齐检查的待办条目写入待完成总清单，修复 Loop 2→Loop 3 级联触发❌缺失问题。
model: fast
is_background: true
---

# 认知级联通知器（cognitive-cascade-notifier）

> 关系类型：implements → 三大闭环架构蓝图.md §差距清单P1「Loop 2更新后无自动触发Loop 3对齐检查」
> 设计依据：自进化智能体系统形式规范 §层5 G（间隙捕获器）在 Loop2→Loop3 方向的实现
> CS-011 修复项目

---

## 运行模式

- **类型**：后台异步（is_background: true），不返回主 context，不阻断主流程
- **模型**：fast（五域节点分析是轻量任务）
- **触发后行为**：主流程立即继续，本 Subagent 在后台独立完成分析和写入

---

## 输入规格

```
input:
  change_type: "new_principle" | "major_l1_update"  # 必填
  change_summary: string     # 新原则表述 or L1更新摘要（一句话，必填）
  principle_id: string       # change_type="new_principle"时必填（如 "P15"）
  is_major_update: bool      # change_type="major_l1_update"时由调用方显式判断（默认阈值 >30% 字符变化）
  doc_name: string?          # change_type="major_l1_update"时提供文档名，便于日志
```

---

## 固定读取路径（硬编码）

```
DOMAIN_REGISTRY_PATH = "_内部总控/skill-system-design/DOMAIN-REGISTRY.md"
PRINCIPLES_PATH = "_内部总控/认知结构/L1.5_底层原则层/底层原则库.md"
OUTPUT_PATH = "_内部总控/认知结构/L3_原始记录/待完成总清单.md"
```

---

## 执行流程

```
Step 1  读取五域定义
        Read: DOMAIN_REGISTRY_PATH
        提取五域名称和核心职责描述（用于相关度判断）

Step 2  影响域分析（保守策略：默认输出全部五域 + 相关度标注）
        
        对每个域，判断 change_summary 关键词与该域核心职责的重叠度：
        ● 高度相关：change_summary 关键词与该域定义有直接语义重叠
        ○ 可能相关：有间接关联或边界案例
        - 基本无关：无明显关联
        
        保守原则：漏通知比过度通知代价更高，疑似相关统一标为 ○

Step 3  写入待完成总清单（严格追加模式）
        
        ⚠️ 写入规则：
        - 使用 StrReplace 或 Write 的追加模式，不读取已有内容
        - 每次只追加一个条目块，不修改已有内容
        - 使用 ISO8601 时间戳代替序号（避免并发冲突）
        
        追加格式：
        ---
        □ [cascade-{ISO8601}] {change_summary}
          变更类型：{change_type} | 涉及：{principle_id 或 doc_name}
          
          ── Loop 3 工作域对齐 ──
          影响域评估（保守）：
            产品开发域 {●/○/-}  |  Skill体系域 {●/○/-}  |  认知结构域 {●/○/-}
            内容宣传域 {●/○/-}  |  公司运营域 {●/○/-}
          建议行动：对 ● 域运行 cognitive-work-alignment-check，确认工作任务仍有认知根
          
          ── Loop 1 Skill 体系对齐（SD2 修复）──
          {loop1_notice}
          
          来源：cognitive-cascade-notifier | 写入时间：{ISO8601}
        ---

Step 3.5  生成 loop1_notice（Skill 体系通知文本）
        
        IF change_type = "new_principle"：
          扫描 SKILL-INDEX.md 中所有 Skill 的「版本说明」列，寻找与 {change_summary} 关键词语义相关的 Skill
          （搜索方法：关键词匹配 Skill 说明文字，不需要精确匹配）
          
          IF 找到相关 Skill：
            loop1_notice = "以下 Skill 可能需要引用新原则 {principle_id}：
              [Skill目录名]（关联原因：[一句话]）
              建议：运行 skill-evolution-planner-meta 或在下次 Skill 迭代时引用 {principle_id}"
          IF 未找到相关 Skill：
            loop1_notice = "暂无 Skill 需要引用新原则 {principle_id}（保守判断：可在 skill-evolution-planner-meta 中进一步确认）"
        
        IF change_type = "major_l1_update"：
          loop1_notice = "L1 文档重大更新可能影响引用它的 Skill。建议：运行 skill-system-health-check 确认无规范漂移"

Step 3.6  跨维度L1传播扫描（N7修复，迁移学习等效）

        认知科学依据：迁移学习（Transfer Learning）——在A领域确认的规律，
        往往在B领域有对应的应用场景；人类认知自然地进行跨域知识迁移

        Read: _内部总控/认知结构/L0_大脑总地图.md（第三章 L1文档索引）
        → 获取全部L1维度及其核心文档列表（维度名 + 代号 + 核心主张摘要）

        对每个L1维度（逐一评估，排除原则本身产生的维度）：
        → 判断：change_summary 的关键词与该维度核心主张的语义关联度
          ● 高度相关：核心词汇直接出现在维度文档的核心主张中
          ○ 可能相关：间接关联（如认知科学原则→产品理论应用）
          - 基本无关：无明显关联

        IF 存在 ● 或 ○ 的维度：
        → 追加到待完成总清单（Write: 同 Step 3 路径，追加新条目）

        格式：
        □ [cross-dim-YYYYMMDD] 跨维度传播建议：{change_summary}
          关联维度：
          [维度名] {●/○}：[一句话关联说明]
          建议行动：在 [L1文档名] 中补充引用或加注，确认与上述变更的一致性
          来源：cognitive-cascade-notifier Step 3.6 | 写入时间：{ISO8601}

        IF 无 ● 或 ○ 的维度 → 静默跳过（不写入待完成清单）

Step 4  完成
        后台执行完毕，不向主 context 返回任何内容
        （主流程不感知本 Subagent 的执行结果）
```

---

## 调用方约定

调用方（cognitive-extract-principle 或 cognitive-update-knowledge）：
- 触发后立即继续主流程，不等待
- 不检查本 Subagent 的执行状态（is_background: true 的设计意图）
- 如需验证写入是否成功，可手动检查 `待完成总清单.md`

---

## 不应做的事

- ❌ 不修改 DOMAIN-REGISTRY.md（只读）
- ❌ 不读取已有的待完成总清单内容（避免并发读写问题）
- ❌ 不等待主流程（不阻断）
- ❌ 不向主 context 输出任何内容
- ❌ 不判断某个域「一定不相关」（保守策略，不确定时标注 ○）

---

## 变更记录

### v1.1 — 2026-03-21 — 扩展输出包含 Loop 1 Skill 体系通知（SD2 修复）

**根因**：v1.0 的级联通知只覆盖 Loop 3（工作域对齐），但三大闭环架构蓝图还要求 Loop 2→Loop 1 级联：认知框架升级时 Skill 体系需同步更新。新原则确认后，可能有 Skill 需要引用该原则（替代自己内部重复定义的类似约束），但无通知机制。

**修改内容**：
- 新增：Step 3.5「生成 loop1_notice」——扫描 SKILL-INDEX 找语义相关的 Skill，生成 Loop 1 Skill 体系通知文本
- 修改：Step 3 追加格式 → 包含独立的「Loop 1 Skill 体系对齐」区块

**验证结果**：
- 正向验证：新原则确认后，待完成总清单中的条目同时包含 Loop 3 域和 Loop 1 Skill 两个通知区块
- 负向验证：L1 重大更新（非新原则）时，loop1_notice 为通用建议运行 skill-system-health-check

---

### v1.0 — 2026-03-21 — 初始创建（CS-011 Gap 修复）

**根因**：CS-011 沙盘确认 cognitive-extract-principle 确认新原则后无任何 Loop 3 通知机制，三大闭环架构蓝图标注的「Loop 2→Loop 3 级联触发：❌缺失」未被修复。自进化形式规范 §层5 G（间隙捕获器）在认知域的 Loop2→Loop3 方向无实现。

**验证状态**：🔵 待真实场景验证（验证方式：确认新原则后检查待完成总清单末尾是否有对应条目）

### v1.2 — 2026-03-23 — 新增 Step 3.5（跨维度L1传播扫描，N7修复）

**根因**：N7 Gap：当新原则确认后，cascade-notifier 只通知「五域工作节点」（Loop 3），
但没有通知「其他L1维度文档」（跨维度方向）。知识在维度间的迁移学习是自然的，
缺少这条通知意味着新原则可能长期无法传播到相关维度的文档中。

**修改内容**：
- 新增 Step 3.5：在写入报告（Step 3）之后、完成（Step 4）之前
- 读取L0全部L1维度，评估与change_summary的语义关联度
- 高度相关(●)和可能相关(○)的维度，追加跨维度传播建议到待完成总清单

**认知科学依据**：迁移学习（Transfer Learning）——在一个领域确认的规律往往在其他领域有应用
