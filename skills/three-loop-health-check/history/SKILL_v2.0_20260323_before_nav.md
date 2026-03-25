---
name: three-loop-health-check
description: 三大闭环日常健检（v2.0）。快速读取系统状态文件（约1分钟），从三个层次输出健康仪表盘：①运营指标层（PENDING-EXPERIENCES/碎片积压/一致性检查日期/cascade/PENDING-SKILLS）②沙盘状态层（sandboxes/目录的 validated/draft/gap-found 分布）③D0覆盖率层（role-* Skills 有多少已有认知根行）。触发词：「三大闭环健康检查」「全系统健康报告」「整体系统健康」「三个闭环都健康吗」「三大闭环状态怎么样」。⚠️ 本 Skill 为快速只读健检，无 Full 模式。深度场景沙盘验证→skill-closure-verifier-meta；生成场景沙盘→scenario-sandbox-builder；单一Loop专项→对应专项Skill。
---

# 三大闭环日常健检（three-loop-health-check v2.0）

> 关系类型：reads → scenario-sandbox-builder 产出（sandboxes/ 目录）
> 关系类型：references → skill-closure-verifier-meta（深度验证，本 Skill 不替代它）
> 认知根：三大闭环架构蓝图.md §五（Loop 1/2/3 现状缺口）+ AI智能体任务分类体系 §九（通用后置动作）

---

## 设计定位：三个层次的快速健康仪表盘

| 层次 | 检查内容 | 数据来源 |
|---|---|---|
| **①运营指标层** | 积压/延迟/待处理数量 | PENDING-EXPERIENCES/碎片索引/系统日志/待完成总清单/PENDING-SKILLS |
| **②沙盘状态层** | 场景验证覆盖率 | sandboxes/ 目录（scenario-sandbox-builder 产出）|
| **③D0覆盖率层** | 认知根落地程度 | SKILL-INDEX（Grep 搜索 role-* + D0 关键词）|

**⚠️ 无 Full 模式**：本 Skill 仅做快速只读健检（~1分钟）。需要深度验证时请触发 `skill-closure-verifier-meta`。

---

## 激活后立即执行

```
Step 0  D0 认知根确认
        Read: /Users/boyuan/aiwork/0310_huaxiang/_内部总控/认知结构/L1_系统性文档/产品理论维度/三大闭环架构——思维代理系统集成设计蓝图.md
             limit: 30
        → 带三大闭环定义和 Loop 职责认知进入数据读取

Step 1  读取运营指标层数据
        
        ── Loop 1（Skill体系）──
        
        Read: /Users/boyuan/aiwork/0310_huaxiang/.cursor/skills/skill-index/PENDING-SKILLS.md
        → 统计：🔲 待处理条目数 → L1_pending_skills
        → 找最老「🔲 待处理」条目日期 → L1_oldest_skill
          （若无待处理 → L1_oldest_skill = "无积压"）
        
        ── Loop 2（认知结构）──
        
        Read: /Users/boyuan/aiwork/0310_huaxiang/_内部总控/认知结构/L2_碎片化思考/碎片整合索引.md
        → 统计：行内含「🔲 待整合」字样的行数 → L2_fragments
        
        Read: /Users/boyuan/aiwork/0310_huaxiang/_内部总控/认知结构/L3_原始记录/系统日志.md
             offset: -50（读取最后50行，日志按时间顺序追加）
        → 逆向搜索，找最近一行含「cognitive-consistency-check」的条目
        → 提取日期，计算距今天数 → L2_last_consistency_check
          （若未找到 → L2_last_consistency_check = "从未执行"）
        
        Read: /Users/boyuan/aiwork/0310_huaxiang/_内部总控/认知结构/L1.5_底层原则层/底层原则库.md
             limit: 100
        → 统计：含「待确认」「P?」「候选」字样的行数 → L2_candidate_principles
        
        ── Loop 3↔2（场景-认知耦合）──
        
        Read: /Users/boyuan/aiwork/0310_huaxiang/_内部总控/认知结构/L3_原始记录/待完成总清单.md
        → 统计：含「[cascade-」字样的行数 → L3_cascade_pending
        
        Read: /Users/boyuan/aiwork/0310_huaxiang/.cursor/skills/skill-index/PENDING-EXPERIENCES.md
        → 统计：🔲 待处理 条目数 → L3_exp_pending
        → 找最老「🔲 待处理」条目日期 → L3_oldest_exp
          （若无待处理 → L3_oldest_exp = "无积压"）

Step 2  读取沙盘状态层数据
        
        使用 Glob 工具扫描所有沙盘文件（限定目录，避免归档副本污染）：
        Glob pattern: "**/*.md"
        target_directory: "/Users/boyuan/aiwork/0310_huaxiang/_内部总控/skill-system-design/sandboxes"
        → 获取所有沙盘文件路径列表 sandbox_files
        
        IF sandbox_files 为空：
          sandbox_validated_total = 0
          sandbox_draft_total = 0
          sandbox_gap_total = 0
          sandbox_coverage_domains = []
          → 标注「沙盘库为空，建议触发 scenario-sandbox-builder 建立初始沙盘」
          → 跳到 Step 3
        
        对每个文件路径（最多处理100个文件，超过则抽样并标注「已抽样」）：
          Read: [文件路径] limit: 10（读 frontmatter，含 status 字段）
          → 提取 status 字段值
          → 提取 domain 字段值（用于统计覆盖的域）
        
        汇总：
        → sandbox_validated_total = status="validated" 的文件数
        → sandbox_draft_total = status="draft" 的文件数
        → sandbox_gap_total = status="gap-found" 的文件数
        → sandbox_coverage_domains = domain 字段唯一值列表
        
        Read: /Users/boyuan/aiwork/0310_huaxiang/_内部总控/skill-system-design/DOMAIN-REGISTRY.md
             limit: 40
        → 提取五域名称列表 all_domains
        → sandbox_uncovered_domains = all_domains 中不在 sandbox_coverage_domains 的域

Step 3  读取 D0 覆盖率层数据
        
        ⚠️ 只读 SKILL-INDEX.md 的主表区域（前60行），避免历史变更记录区域造成双重计数：
        Read: /Users/boyuan/aiwork/0310_huaxiang/.cursor/skills/skill-index/SKILL-INDEX.md
             limit: 60（前60行包含 role-* Skill 主表，不含变更历史）
        
        → 在读取内容中，统计：
          d0_covered = 同时满足以下两个条件的行数：
            ① 行内含「role-」（角色类 Skill 行）
            ② 行内含「D0」（已有认知根行）
          d0_total = 行内含「role-」且不含「---|」（排除表头分隔行）的行数
        
        D0 覆盖率 = d0_covered / d0_total

Step 4  评判各维度状态（固定规则，不自由裁量）
        
        ── Loop 1 状态 ──
          L1_pending_skills = 0 且 L1_oldest_skill = "无积压" → ✅
          L1_pending_skills > 0 且 L1_oldest_skill 距今 ≤30天 → ⚠️
          L1_oldest_skill 距今 > 30天 → ❌
        
        ── Loop 2 状态 ──
          L2_fragments < 8 AND L2_last_consistency_check ≤7天 AND L2_candidate_principles ≤3 → ✅
          L2_fragments 8-15 OR L2_last_consistency_check 7-30天 OR L2_candidate_principles 4-6 → ⚠️
          L2_fragments > 15 OR L2_last_consistency_check > 30天或从未执行 OR L2_candidate_principles > 6 → ❌
        
        ── Loop 3↔2 状态 ──
          L3_cascade_pending = 0 AND L3_oldest_exp = "无积压"（或距今≤7天）→ ✅
          L3_cascade_pending 1-3 OR L3_oldest_exp 距今 7-30天 → ⚠️
          L3_cascade_pending > 3 OR L3_oldest_exp 距今 > 30天 → ❌
        
        ── 沙盘状态 ──
          sandbox_files 为空 → ❌（沙盘库未建立）
          sandbox_gap_total > 0 OR sandbox_uncovered_domains 非空 → ⚠️
          全部 validated 且覆盖所有域 → ✅
        
        ── D0 覆盖率 ──
          d0_covered / d0_total ≥ 0.8 → ✅
          0.5 ≤ d0_covered / d0_total < 0.8 → ⚠️
          d0_covered / d0_total < 0.5 → ❌
        
        ── 整体结论 ──
          有任意 ❌ → CRITICAL
          无 ❌ 有 ⚠️ → NEEDS ATTENTION
          全部 ✅ → HEALTHY

Step 5  生成健康仪表盘（统一输出，不等用户确认）
        
        「━━━━━━━━━━━━━━━━━━━━━━━━━━━━
          🏥 三大闭环日常健检报告
          日期：YYYY-MM-DD
          ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
          
          整体结论：HEALTHY / NEEDS ATTENTION / CRITICAL
          
          ── ① 运营指标层 ──
          Loop 1（Skill体系）：✅/⚠️/❌
            · PENDING-SKILLS：{L1_pending_skills}条（最老：{L1_oldest_skill}）
          
          Loop 2（认知结构）：✅/⚠️/❌
            · 待整合碎片：{L2_fragments}条
            · 上次 C1-C11：{L2_last_consistency_check}
            · 候选原则积压：{L2_candidate_principles}个
          
          Loop 3↔2（场景-认知耦合）：✅/⚠️/❌
            · cascade 待处理：{L3_cascade_pending}条
            · 经验反馈积压：{L3_exp_pending}条（最老：{L3_oldest_exp}）
          
          ── ② 沙盘状态层 ──
          沙盘库：✅/⚠️/❌
            · Validated：{sandbox_validated_total}个 | Draft：{sandbox_draft_total}个 | Gap-found：{sandbox_gap_total}个
            · 未覆盖域：{sandbox_uncovered_domains（无则写「全域已覆盖」）}
          
          ── ③ D0 覆盖率层 ──
          认知根覆盖：✅/⚠️/❌
            · {d0_covered}/{d0_total} 个 role-* Skill 已有 D0 行（{覆盖率%}）
          
          ── 优先行动建议 ──
          {若全 ✅ → 「系统运营健康，无需紧急处理」}
          {若有问题 → 最多列3条，按严重程度排序}
          1. [P0/P1] [建议] → 触发：[对应 Skill 或操作]
          ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
          ⚠️ 快速健检（~1分钟，读取状态文件）。深度验证→ skill-closure-verifier-meta。
          
          [查看某层详情] [触发深度验证] [处理第1项建议]」
```

---

## 若文件不存在或读取失败

```
任何文件读取失败 → 对应指标标注「数据缺失（文件不可读）」，状态评判为 ⚠️
→ 继续读取其他文件，不中断整体流程
→ Step 5 报告末尾列出所有不可读文件路径
```

---

## 注意事项

- **纯只读**：不写入任何文件，不修改任何状态
- **快速健检**：每次读取约10个文件，约1分钟完成
- **无 Full 模式**：v2.0 只有快速健检，无分支。深度验证请触发 `skill-closure-verifier-meta`
- **沙盘层依赖 Option B**：若 scenario-sandbox-builder 从未运行，沙盘层会显示「沙盘库为空」❌，这是正常的诊断结果

---

## 变更记录

### v2.0 — 2026-03-22 — 完整重建（v1.0 废弃后正确实现）

**根因**：v1.0 废弃，经三大闭环架构重设计，v2.0 定位为「快速日常健检」（Option A）。

**关卡A修复（3项Critical）**：
- `limit: -50` → `offset: -50`（系统日志末尾读取）
- 通配符读取 → Glob 工具扫描（Step 2）
- Step 4 Loop 3↔2 评判中 `L3_exp_pending` 改为 `L3_oldest_exp` 进行时间比较

**关卡B修复（2项Critical）**：
- 删除 Full 模式（仅存在于 role-menu 和 session-bootstrap 中，SKILL.md 无实现）
- 同步修改 role-menu.mdc 和 session-bootstrap.mdc，移除 Full 模式描述和 B0 死代码

**关卡B H-1 修复**：`ls` 命令 → Glob 工具（支持只读模式）
**关卡B H-2 修复**：SKILL-INDEX.md 无限读取 → 改为 Grep 搜索

**验证状态**：🔵 待关卡C验证
