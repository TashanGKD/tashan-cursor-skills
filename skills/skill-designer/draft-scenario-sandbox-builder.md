# Skill 产品定义卡片：scenario-sandbox-builder

> 填写日期：2026-03-22
> 复杂度：Level 3 集成型
> 认知根：三大闭环架构蓝图.md §三（场景投射原则）+ Skill体系设计原则_v1.0.md §4.3.5

---

## 基本信息

| 字段 | 内容 |
|---|---|
| 组件名称 | `scenario-sandbox-builder` |
| 组件类型 | Skill |
| 复杂度 | Level 3 |
| 开发日期 | 2026-03-22 |
| 需求来源 | three-loop-health-check 架构重设计，Option B：沙盘生成器 |

---

## 一、人层设计

### 1.1 解决什么问题？

```
skill-closure-verifier-meta 需要预置沙盘才能做深度验证，
但沙盘是人工写的，覆盖不全（现有约60个），且没有覆盖「认知根节点」。

scenario-sandbox-builder 从现有 Skills/Roles 出发，自动发现所有任务场景，
为每个场景生成包含「认知根」和「认知反馈」节点的完整大闭环沙盘，
保存为持久化文件，供 skill-closure-verifier-meta 和 three-loop-health-check v2.0 使用。
```

### 1.2 触发条件（人的视角）

```
典型触发语句：
- 「场景沙盘生成」「为当前体系生成场景沙盘」
- 「发现所有任务场景并建沙盘」「场景化沙盘覆盖」
- 「给现有体系的每个场景建一个沙盘」

触发场景：
- 体系新增了多个 Skill 后，想补全沙盘覆盖
- 第一次运行，为体系建立完整的沙盘库基础
- skill-closure-verifier-meta 发现某个域沙盘不足时，触发本 Skill 补充

明确不应该触发：
- 「扩充沙盘/沙盘不够/补全draft沙盘」→ skill-sandbox-expander（从已有域扩充）
- 「元验证/闭环验证」→ skill-closure-verifier-meta（做深度验证，消费沙盘）
- 「三大闭环健康检查」→ three-loop-health-check（读沙盘状态做快速健检）
```

### 1.3 成功标准

```
产出物：N 个新沙盘文件（保存到 sandboxes/[domain]/ 目录）

质量判断：
- 每个新生成的沙盘覆盖一个完整任务场景的大闭环（含认知根 D0 节点 + 认知反馈节点）
- 沙盘格式符合 SANDBOX-FORMAT.md 规范
- status: draft（等待 skill-closure-verifier-meta 做 Phase 2 验证）
```

### 1.4 MVP 边界

```
✅ 做：
- 动态场景发现（从 role-* Skills 聚类）
- 每个场景的大闭环识别（含 D0 + 认知反馈节点）
- 生成并保存 draft 沙盘文件
- 跳过已有 validated 沙盘的场景（不重复生成）

❌ 不做：
- Phase 2 验证（生成 draft，验证由 skill-closure-verifier-meta 做）
- 健康报告（那是 three-loop-health-check v2.0 的工作）
- 修改或删除已有沙盘
```

---

## 二、Agent 层设计

### 2.1 触发条件（AI 视角）

```
触发：用户消息含「场景沙盘生成」或「为场景建沙盘」或「发现场景并建沙盘」

优先级区分：
- 「扩充沙盘」「沙盘不够」「补全draft」→ skill-sandbox-expander 优先
- 「元验证」「闭环验证」→ skill-closure-verifier-meta 优先
- 「三大闭环健康」→ three-loop-health-check 优先
- 本 Skill：明确说「发现场景」「场景沙盘」「为体系建沙盘」时触发
```

### 2.2 执行步骤

```
Step 0  读取设计原则（D0）
        Read: _内部总控/认知结构/L1_系统性文档/系统架构思维维度/Skill体系设计原则_v1.0.md
             § 4.3.5（认知根原则）——带入后续沙盘设计
        Read: _内部总控/skill-system-design/SANDBOX-FORMAT.md
             ——确认沙盘文件格式要求

Step 1  读取当前体系状态
        Read: .cursor/rules/role-menu.mdc
             → 提取全部 role-* 条目（目录名 + 触发场景描述）
        Read: .cursor/skills/skill-index/SKILL-INDEX.md
             → 提取 Skills 的分类和功能说明
        Read: _内部总控/skill-system-design/DOMAIN-REGISTRY.md
             → 读取已定义的五个工作域（参考，不强制对齐）
        Read: _内部总控/skill-system-design/sandboxes/ 各子目录 → 已有沙盘数量和 status

Step 2  场景发现（确定性聚类算法）
        
        聚类规则（按以下顺序判断，取第一个命中的）：
        
        规则1：共享工作产物型
          多个 role-* Skills 在同一项目中操作同一组文档（产品定义.md / 技术架构.md / 开发计划.md）
          → 归为「产品开发」场景
        
        规则2：流水线型
          role-A 的主要输出是 role-B 的主要输入
          → 归为同一场景（标注依赖关系）
        
        规则3：相同产物类型
          多个 role-* Skills 产出同类型工件（文章/报告/研究文档）
          → 归为「内容创作」场景
        
        规则4：相同操作对象
          多个 Skills 操作同类系统文件（.cursor/skills/ 目录 / Skill 索引）
          → 归为「Skill体系管理」场景
        
        规则5：独立（不符合以上规则）
          → 单独成一个场景
        
        聚类结果验证（必须执行）：
          检查每个 role-* Skill 是否被归入了至少一个场景
          → 遗漏的 → 加入最相关场景 or 单独成场景
          → 重叠的（一个 Skill 属于多个场景）→ 取主要场景，次要场景标注「参与」
        
        输出：discovered_scenarios 列表
          每个场景：{ 场景名, 主要 Roles 列表, 触发入口, 终态描述 }

Step 3  识别每个场景的大闭环
        对每个发现的场景：
        
        3a. 读取该场景「触发入口 Role」的 SKILL.md（激活后立即执行步骤）
        3b. 识别最小闭环：
            触发条件 → 主要执行步骤（含关键关卡节点）→ 工作产物存在（终态）
        3c. 扩展为大闭环，在最小闭环基础上增加：
            ① D0 节点（大闭环开始处）：
               「执行者读取 [场景对应的 L1 认知文档]，确认任务认知根」
               → 具体 L1 文档：参考该场景主要 Roles 的知识导航表 D0 行
               → 若无 D0 行：标注「认知根缺失，需补充」
            ② 认知反馈节点（大闭环末端）：
               「任务完成后，write-task-log 步骤五触发 cognitive-task-reflector，
               洞见写回 L2 碎片层」
               → 验证：该场景的末端 Role 完成后是否经过 session-bootstrap 序列B？
            ③ 级联节点（如存在）：
               「本场景的工作产物，触发了 [下一场景] 的入口条件」
        
        检查该场景是否已有覆盖沙盘（Step 1 读取的现有沙盘状态）：
        → 已有 validated 沙盘 → 跳过该场景（输出「[场景名]：已有已验证沙盘，跳过」）
        → 已有 draft/gap-found 沙盘 → 标注「建议更新」，生成新版本
        → 无沙盘 → 生成新沙盘

Step 4  生成沙盘文件（对未覆盖或需更新的场景）
        
        对每个需要生成沙盘的场景，按 SANDBOX-FORMAT.md 格式生成内容：
        
        ⚠️ 格式强制要求（来自 SANDBOX-FORMAT.md）：
        - sandbox-id: [域缩写]-[NNN]（NNN 为该域下一个未使用序号）
        - domain: [场景所属域名]
        - scenario-type: [新场景类型标签，见下方]
        - difficulty: simple/medium/complex
        - status: draft（生成即 draft，等待 Phase 2 验证）
        - Phase 1 完整填写（含大闭环全部节点，包括 D0 和认知反馈）
        - Phase 2 表格留空（只填表头，等 skill-closure-verifier-meta 验证时填写）
        
        场景类型标签（scenario-type）：
        scenario-type = "new-start"（首次触发场景，从零开始）
           or "iteration"（基于已有产物的迭代）
           or "maintenance"（体系维护/健检类）
           or "integration"（跨场景集成）
        
        Phase 1 预想链路格式（大闭环完整链路树）：
        
        ```
        D0  读取认知根 → [L1文档名称]
          ↓
        [入口触发] → [role-* 激活]
          ↓
        [步骤1] → [中间产物1]
          ↓
        [步骤2] → [中间产物2]
          ├─ [正常路径] → ... → [工作产物终态]
          └─ [失败路径] → ... → [修复终态]
          ↓（工作产物存在后）
        [认知反馈] → write-task-log → cognitive-task-reflector → 洞见写入L2
          ↓（如有级联）
        [级联触发] → [下一场景入口]
        ```
        
        保存规则：
        → Write: _内部总控/skill-system-design/sandboxes/[域名]/sandbox-[NNN].md
        → 域名 = 与 DOMAIN-REGISTRY 已有域名对齐（若是新域，先建目录）
        → NNN = 读取该域目录下现有最大序号 + 1

Step 5  输出摘要
        
        「━━ 场景沙盘生成完成 ━━
         发现场景数：N
         
         [场景名1]：✅ 已有 validated 沙盘，跳过
         [场景名2]：📄 新生成沙盘 → [文件路径]（status: draft）
         [场景名3]：🔄 更新现有 draft → [文件路径]
         ...
         
         新生成/更新沙盘：M 个
         
         ⚠️ 所有新沙盘状态为 draft。
         下一步：触发 skill-closure-verifier-meta 对新沙盘执行 Phase 2 验证，
         或手动审查后修改 status 为 validated。
         ━━━━━━━━━━━━━━━━━━━━━━━」
```

### 2.3 边界条件

```
情况A：某个 role-* Skill 的 SKILL.md 不可读
  → 该 Skill 不参与聚类，在摘要中标注「[Skill名] 读取失败，未纳入场景发现」

情况B：所有场景均已有 validated 沙盘
  → 输出「当前体系沙盘覆盖完整，无需新生成」，终止

情况C：聚类结果只有 1 个场景（极端情况）
  → 告知用户「场景聚类结果较少，可能是体系体量小，继续生成」

情况D：DOMAIN-REGISTRY.md 不存在
  → 警告「DOMAIN-REGISTRY 不可读，域名将基于场景名自动生成」，继续执行
```

### 2.4 依赖声明

```
读取：
- role-menu.mdc（场景发现）
- SKILL-INDEX.md（Skill 功能说明）
- _内部总控/skill-system-design/DOMAIN-REGISTRY.md（域名参考）
- _内部总控/skill-system-design/SANDBOX-FORMAT.md（格式规范）
- _内部总控/skill-system-design/sandboxes/ 目录（现有沙盘状态）
- 场景触发入口 Roles 的 SKILL.md（大闭环识别）
- Skill体系设计原则_v1.0.md §4.3.5（认知根原则）

写入：
- _内部总控/skill-system-design/sandboxes/[域名]/sandbox-[NNN].md（新生成的沙盘文件）

被以下 Skill 消费（不调用，但输出供其使用）：
- skill-closure-verifier-meta（Phase 2 验证）
- three-loop-health-check v2.0（快速健检时读取 status）

认知根文档（L1）：
- 三大闭环架构蓝图.md（场景投射原则 + 工作域定义）
- AI智能体任务分类体系与闭环完成标准_v1.0.md（任务类型分类）
- Skill体系设计原则_v1.0.md §4.3.5（认知根原则）
```

### 2.5 常见失败模式

```
失败模式1：Step 2 聚类后产生过多碎片场景（每个 Skill 自成一场景）
  → 根本原因：规则5「独立」被过度使用
  → 预防：聚类完成后，检查独立场景数 > 3 时重新审视规则1-4是否有适用项

失败模式2：Step 3 读取 SKILL.md 时读全文导致 context 超出
  → 根本原因：某些 SKILL.md 超过500行
  → 预防：只读「激活后立即执行」章节（找到该章节标题后读到下一个 ## 标题停止）

失败模式3：沙盘 Phase 1 链路只写了 2-3 步，没有完整覆盖大闭环
  → 根本原因：AI 在「简洁」和「完整」之间倾向简洁
  → 预防：Step 4 的 Phase 1 链路必须包含：D0 节点 / 所有关卡节点 / 认知反馈节点（缺一不可）

失败模式4：生成沙盘时 sandbox-id 序号冲突（并发写入）
  → 根本原因：多 session 同时运行
  → 预防：Step 4 写入前先 ls 该目录，取当前最大序号+1
```

### 2.6 强绑定 Rule

```
强绑定：
- R2 NO_FABRICATION：场景发现和闭环识别必须来自实际读取，不得凭训练知识假设体系结构
- R1 EVIDENCE_FIRST：D0 节点的 L1 文档路径必须来自 SKILL.md 知识导航表实际读取

推荐：
- R6 ARTIFACT_FIRST：生成沙盘文件（不只在对话中描述）
```

---

## 三、人层 vs Agent 层张力分析

```
人层「不言而喻」的假设：
- 「场景」粒度刚好合适——不会太细（每个 Skill 一个场景）也不会太粗（所有 Skill 一个场景）
  Agent 层修订：Step 2 的聚类规则按优先级顺序执行，规则5（独立）最后才用

AI 可能产生歧义的点：
- 「触发入口 Role」不等于「第一个触发的 Skill」——有些场景没有明确的第一个
  → 修订：触发入口 = role-menu 中有「用户直接说X就触发」的那个 Role
- Step 3 中「大闭环末端」在哪里——有些场景循环运行
  → 修订：末端 = 工作产物进入持久化存储（文件写入）的那个步骤

修订结论：Step 2 算法规则已修正为确定性顺序；Step 3 末端判断已明确化。
```

---

## 四、复杂度评估

```
与现有 Skill 的交互点：
- skill-sandbox-expander：同为沙盘相关，触发词「场景」vs「域扩充」需要明确区分
- skill-closure-verifier-meta：本 Skill 产出供其消费，无触发词重叠
- DOMAIN-REGISTRY.md：读取参考，不强制对齐

最终级别：Level 3 集成型
需走关卡A + 关卡B + 关卡C
```

---

## 五、关卡执行记录（待填写）
