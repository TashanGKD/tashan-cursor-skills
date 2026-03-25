---
name: scenario-sandbox-builder
description: 从现有 role-* Skills 动态发现所有任务场景，为每个场景生成包含「认知根 D0 节点」和「认知反馈节点」的完整大闭环沙盘文件（status: draft），供 skill-closure-verifier-meta 做 Phase 2 验证。⚠️ 与 skill-sandbox-expander 的区别：后者从已有域的缺口扩充；本 Skill 从零发现所有场景，生成覆盖全体系的初始沙盘库。触发词：「场景沙盘生成」「为当前体系生成场景沙盘」「发现所有任务场景并建沙盘」「场景化沙盘覆盖」「从零建沙盘库」。
---

# 场景沙盘生成器（scenario-sandbox-builder）

> 关系类型：feeds → skill-closure-verifier-meta（生成的 draft 沙盘供其做 Phase 2 验证）
> 关系类型：references → SANDBOX-FORMAT（遵循沙盘格式规范）
> 关系类型：extends → skill-sandbox-expander（本 Skill 做初始全量发现，expander 做后续缺口扩充）
> 认知根：三大闭环架构蓝图.md §三（场景投射原则）+ Skill体系设计原则_v1.0.md §4.3.5（认知根原则）

---

## ⚠️ 两阶段分离保证（核心约束）

本 Skill 遵循 `skill-sandbox-expander` 建立的两阶段分离原则：

- **Phase 1（本 Skill 负责）**：基于 Skill 的高层描述（`description` 字段）生成「理想系统应该如何工作」的预想链路。**通过 Read limit 参数实现技术层隔离，确保执行步骤不进入 working memory。**
- **Phase 2（skill-closure-verifier-meta 负责）**：对照实际 SKILL.md 执行步骤验证是否符合预想。

本 Skill 的 Step 2a 使用 `Read [path] limit: 12` 读取 SKILL.md——只返回 frontmatter（前12行），后续的「激活后立即执行」章节通过工具层的 limit 参数被硬截断，不会进入 AI 的 working memory。这是技术隔离，而非仅依赖认知自我约束。

---

## 激活后立即执行

```
Step 0  读取设计原则（D0）
        Read: /Users/boyuan/aiwork/0310_huaxiang/_内部总控/认知结构/L1_系统性文档/系统架构思维维度/Skill体系设计原则_v1.0.md
             → 重点读取 §4.3.5「认知根原则」，带此认知进入沙盘设计
        Read: /Users/boyuan/aiwork/0310_huaxiang/_内部总控/skill-system-design/SANDBOX-FORMAT.md
             → 确认沙盘文件格式要求（frontmatter + Phase 1 + Phase 2 格式）

Step 1  读取当前体系状态
        
        Read: /Users/boyuan/aiwork/0310_huaxiang/.cursor/rules/role-menu.mdc
             → 读取「可用角色一览」表格，提取所有 role-* 条目（目录名 + 触发场景描述列）
        
        Read: /Users/boyuan/aiwork/0310_huaxiang/.cursor/skills/skill-index/SKILL-INDEX.md
             → 读取 Skill 表格，提取 role-* Skills 的「版本备注」列（功能说明）
             → 作为 role-menu 的补充数据源（SKILL-INDEX 更新及时，role-menu 可能滞后）
        
        Read: /Users/boyuan/aiwork/0310_huaxiang/_内部总控/skill-system-design/DOMAIN-REGISTRY.md
             → 读取五个工作域定义（产品开发/认知结构/公司运营/内容宣传/Skill体系）
             → 用于场景归属域名映射
        
        扫描现有沙盘状态：
        ls /Users/boyuan/aiwork/0310_huaxiang/_内部总控/skill-system-design/sandboxes/
        → 列出所有子域目录
        → 对每个域目录，读取前3个沙盘文件的 frontmatter（获取 status 分布）
        → 输出：{域名: {validated: N, draft: M, gap-found: K}}
        
        ⚠️ 注意：SKILL-INDEX 可能比 role-menu 更新。若某个 role-* Skill 在 SKILL-INDEX 中存在但不在 role-menu 触发词表中，以 SKILL-INDEX 为准纳入场景发现。

Step 2  场景发现（两阶段：先读描述，再聚类）
        
        2a. 读取每个 role-* Skill 的高层描述（⚠️ 使用 Read limit 参数实现技术层隔离）：
            对 Step 1 识别出的每个 role-* Skill，执行：
            Read: /Users/boyuan/aiwork/0310_huaxiang/.cursor/skills/[Skill目录名]/SKILL.md
                  limit: 12
                 → 只读前12行（SKILL.md 的 frontmatter 通常在前8-12行）
                 → 从返回内容中提取 description 字段
                 → 不读「激活后立即执行」等后续章节（通过 limit 参数实现硬截断）
            
            输出中间数据：role_descriptions（{Skill名: description内容}）
            
            ⚠️ 技术隔离说明：limit 参数确保只有 frontmatter 进入 working memory，
               Phase 1 生成时对实现步骤一无所知，符合两阶段分离原则。
        
        2b. 按以下规则聚类（按优先级顺序，取第一个命中的规则）：
            
            规则1：产品开发类
              判断标准：Skill 的 description 中包含以下任意词组：
              「产品定义」「技术架构」「前端实现」「后端实现」「测试验收」「部署」「UI设计」「数据分析」「闭环验证」「系统设计」
              → 归入「产品开发」场景
            
            规则2：内容创作类
              判断标准：description 中包含：「文章」「写作」「推文」「调研」「报告」「研究」
              → 归入「内容创作」场景
            
            规则3：Skill体系管理类
              判断标准：description 中包含：「Skill」「Rule」「沙盘」「体系健康」「演进」「复盘」「索引」「经验沉淀」
              → 归入「Skill体系管理」场景
            
            规则4：认知结构管理类
              判断标准：description 中包含：「碎片」「L1」「L2」「L1.5」「整合」「原则提炼」「认知结构」「知识库」
              → 归入「认知结构管理」场景
            
            规则5：科研画像类
              判断标准：description 中包含：「量表」「画像」「科研」「人格」「AMS」「IPIP」「RCSS」「数字分身」
              → 归入「科研画像」场景
            
            规则6：独立场景
              不符合以上任何规则 → 单独成场景（场景名 = 该 Skill 的触发词领域）
            
            聚类后验证：
            - 独立场景数 > 3 → 重新扫描一次，优先合并进最近的规则1-5；若仍 > 3 → 保留，继续执行
            - 每个 role-* Skill 只属于一个场景（主要场景）
        
        输出：discovered_scenarios（{场景名: [Skill目录名列表], 触发入口: 第一个按 role-menu 顺序的 Skill, 终态描述: 基于 description 推断}）

Step 3  识别每个场景的大闭环（基于 description，不读执行步骤）
        
        对每个 discovered_scenarios 中的场景：
        
        3a. 检查该场景是否已有覆盖沙盘（Step 1 扫描结果）：
            → 已有 validated 沙盘 → 跳过，输出「[场景名]：✅ 已有已验证沙盘，跳过」
            → 已有 draft/gap-found → 标注「建议更新」，继续生成新版本
            → 无沙盘 → 继续 3b
        
        3b. 识别最小闭环（基于 description 和 role-menu 触发场景描述推断，不读执行步骤）：
            - 入口：role-menu 中该场景触发入口 Skill 的「触发场景」描述
            - 主要产物：从各 Skill 的 description 推断该场景完成后的核心工作产物
            - 终态：「[核心工作产物] 已存在且可被下游消费」
        
        3c. 扩展为大闭环（基于认知根原则，不依赖执行步骤）：
            
            ① D0 节点（大闭环开始前）：
               「执行者读取认知根文档，确认本次工作的认知框架」
               判断使用哪个 L1 文档：
               - 产品开发场景 → L1 产品理论维度/AI时代产品问题全景框架.md
               - 内容创作场景 → L1 个人方法论维度/写作习惯与风格手册.md
               - Skill体系管理场景 → L1 系统架构思维维度/Skill体系设计原则_v1.0.md
               - 认知结构管理场景 → L1 系统架构思维维度/三大闭环架构蓝图.md
               - 科研画像场景 → /Users/boyuan/aiwork/0310_huaxiang/_内部总控/认知结构/L1_系统性文档/研究范式维度/（扫描该目录找第一个★CURRENT文档；若目录为空 → 标注「认知根文档待建立」）
               - 独立场景 → 标注「认知根文档待确认」
               
               验证认知根文档是否存在：
               Read: [上述对应文档路径]（只看第一行，确认文件存在即可）
               → 存在 → D0 节点状态 ✅
               → 不存在 → D0 节点状态 ❌，标注「认知根文档缺失」
            
            ② 认知反馈节点（大闭环末端）：
               「执行者通过 session-bootstrap 序列B + write-task-log 步骤五，
               触发 cognitive-task-reflector，将本次工作的洞见写入 L2 碎片层」
               → 该节点是标准的认知反馈机制，对所有场景一致

Step 4  生成沙盘文件
        
        对需要生成/更新沙盘的每个场景：
        
        4a. 确定域名和序号：
            - 域名：从 DOMAIN-REGISTRY.md 中找与该场景最对应的工作域名称
              - 若找到 → 使用该域名（如「产品开发」→ 域目录 sandboxes/产品开发/）
              - 若无对应 → 以场景名作为域目录名（新建目录）
            - 序号：
              ls sandboxes/[域名]/ → 找所有 sandbox-NNN.md 中最大的 NNN
              新序号 = max(NNN) + 1
              若目标文件已存在（冲突）→ 自动 +1，最多重试 3 次
        
        4b. 按 SANDBOX-FORMAT.md 格式生成 Phase 1（⚠️ 基于 description 推断，不读执行步骤）：
            
            格式：
            ---
            sandbox-id: [域缩写]-[NNN]
            domain: [域名]
            scenario-type: [new-start/iteration/maintenance/integration]
            difficulty: [simple/medium/complex]
            status: draft
            phase1-source: description-based（标注 Phase 1 来源，供 verifier-meta 识别）
            last-updated: YYYY-MM-DD
            ---
            
            # 沙盘 [sandbox-id]：[场景名称]
            
            ## 场景描述
            [基于 description 推断的场景背景，1-3句话]
            
            ## 输入
            - **入口节点**：[触发入口 Skill 名]
            - **输入内容**：「[基于 role-menu 触发场景描述]」
            - **前置状态**：[基于 description 推断]
            
            ## Phase 1：预想行为（基于高层描述的理想系统预想）
            
            > ⚠️ 本 Phase 1 基于各 Skill 的 description 字段推断，不含执行步骤细节。
            > Phase 2 验证（由 skill-closure-verifier-meta 执行）将对照实际执行步骤检验。
            
            ### 预想触发链路（大闭环全路径）
            
            ```
            D0  读取认知根文档 → [L1文档名]（[存在✅/缺失❌]）
              ↓
            [触发入口 Skill] 激活
              ↓
            [基于 description 推断的主要执行阶段]
              ├─ [正常路径] → ... → [主要工作产物存在]
              └─ [失败/修复路径] → ...
              ↓
            认知反馈节点：session-bootstrap 序列B → write-task-log 步骤五 → L2 碎片写入
            ```
            
            ### 分支覆盖声明
            | 分叉点 | 分支数 | 本沙盘覆盖 | 待其他沙盘覆盖 |
            |---|---|---|---|
            | [主要分叉] | 2 | 正常路径 | 错误恢复路径 |
            
            ### 预想终态输出
            | 产物 | 位置 | 格式 |
            |---|---|---|
            | [核心工作产物] | [推断路径] | [基于 description 推断] |
            
            ### 自洽检查点
            
            - Phase 1 链路中的 D0 文档：[认知根文档路径] → [✅存在/❌缺失]
            - Phase 1 末端工作产物与触发入口描述一致性：[一句话说明]
            - 认知反馈节点与 session-bootstrap 序列B 的触发条件一致：✅
            
            ### 用户视角预想（v1.2新增，借鉴产品沙盘用户类型思维）
            
            > ⚠️ 不得回头看 SKILL.md 执行步骤，仅凭对 Skill description 的直觉回答。
            
            | 维度 | 预想内容 |
            |---|---|
            | 典型触发场景 | [用户在什么处境/动机下触发这个 Skill] |
            | 用户期望的响应 | [一句话，不是技术输出] |
            | 最容易误触发的情形 | [触发词盲区 / 用户说了什么但实际不适合这个Skill] |
            | 认知根确认 | [执行者需要读哪个 L1/L1.5 文档才能正确使用此 Skill] |
            
            ## Phase 2：实际验证（待 skill-closure-verifier-meta 填写）
            
            ### 通过判定标准（Phase 2 执行前预先定义，不可事后修改）
            
            - **validated 门槛**：所有节点触发/输出/下游三项均为 ✅，且 Gap 数量为零
            - **gap-found 门槛**：有至少一项 ❌，或有 ⚠️ 且无法接受
            
            ### 节点逐一验证
            
            | 节点 | Skill | 触发了吗 | 输出了吗 | 触发下游了吗 | 备注 |
            |---|---|---|---|---|---|
            | （待 Phase 2 验证时填写）| | | | | |
            
            ### Gap 发现
            - **有Gap**：待验证
            
            | # | Gap描述 | 类型 | **严重程度** | 证据 |
            |---|---|---|---|---|
            | （待填写）| | | Critical/High/Medium | |
            
            ### 接受风险记录
            | Gap# | 严重程度 | 接受原因 | 决策记录 |
            |---|---|---|---|
            | — | — | 无接受风险项 | — |
            
            ### 总结
            - **Phase 1 vs Phase 2 差距**：待验证
            - **系统是否自洽**：待验证
            
            ### Gap 发现
            - **有Gap**：待验证
            
            ### 总结
            - **Phase 1 vs Phase 2 差距**：待验证
            - **系统是否自洽**：待验证
        
        4c. 若域目录不存在 → 先创建目录，再写文件
        
        4d. Write: /Users/boyuan/aiwork/0310_huaxiang/_内部总控/skill-system-design/sandboxes/[域名]/sandbox-[NNN].md

Step 5  输出摘要（处理完所有场景后统一输出，不等用户确认）
        
        「━━ 场景沙盘生成完成 ━━
         发现场景数：N
         
         [场景名1]（[域名]）：✅ 已有 validated 沙盘，跳过
         [场景名2]（[域名]）：📄 新生成 → sandboxes/[域名]/sandbox-[NNN].md（status: draft）
         [场景名3]（[域名]）：⚠️ D0 认知根文档缺失，已标注在沙盘 Phase 1 的 D0 节点行中
         ...
         
         新生成沙盘：M 个
         
         ⚠️ 所有新沙盘 Phase 1 基于 description 推断（status: draft，phase1-source: description-based）。
         下一步：触发 skill-closure-verifier-meta 对新沙盘执行 Phase 2 验证，
         将 Phase 1 预想与实际 SKILL.md 执行步骤对比，填写 Gap 发现。
         ━━━━━━━━━━━━━━━━━━━━━━━」
```

---

## 注意事项

- **不读执行步骤**：本 Skill 只读 SKILL.md 的 frontmatter（description/name）。Phase 1 基于高层描述生成。
- **phase1-source 字段**：所有生成的沙盘 frontmatter 中必须包含 `phase1-source: description-based`，让 verifier-meta 知道 Phase 1 是「描述推断」而非「实现分析」。
- **不是 skill-sandbox-expander**：本 Skill 做「从零发现所有场景」，expander 做「在已有域基础上填充缺口」。两者输出格式相同，可由 verifier-meta 消费。
- **生成后即 draft**：本 Skill 不做 Phase 2 验证，不修改 status 为 validated。

---

## 与现有 Skill 的关系

| Skill | 关系 |
|---|---|
| skill-closure-verifier-meta | 本 Skill 产出 draft 沙盘，verifier-meta 做 Phase 2 验证（validates）|
| skill-sandbox-expander | 互补：本 Skill 初始全量，expander 后续缺口扩充（both generate sandboxes）|
| three-loop-health-check v2.0 | 本 Skill 产出的 sandboxes 被 v2.0 读取做快速状态检查 |
| cognitive-task-reflector | 大闭环中认知反馈节点的实现机制（被描述在沙盘中，不调用）|

---

## 变更记录

### v1.0 — 2026-03-22 — 初始创建（关卡A/B修订后）

**根因**：three-loop-health-check v1.0 废弃重建决策，将「场景沙盘生成」和「日常健检」分离为两个独立组件。本 Skill 负责生成覆盖全体系任务场景的初始沙盘库（Option B）。

**关卡A修复（4项Critical）**：
- 聚类算法改为基于 description 关键词匹配（确定性规则1-6）
- 补全所有文件的绝对路径
- D0 行判断改为按场景类型映射到对应 L1 文档
- Step 5 明确「处理完所有场景后统一输出，不等用户确认」

**关卡B修复（2项Critical）**：
- Phase 1 生成改为基于 description 字段，不读执行步骤（修复 Phase 1 污染问题）
- 新增 `phase1-source: description-based` frontmatter 字段（供 verifier-meta 区分）

**验证状态**：🔵 待关卡C验证

---

### v1.1 — 2026-03-24 — Phase 1 模板加入 SANDBOX-FORMAT v1.2 新字段

**根因**：同 skill-sandbox-expander v1.0.4，SANDBOX-FORMAT.md v1.2 新增了用户视角预想、通过判定标准、Gap 严重程度、接受风险记录，但 scenario-sandbox-builder 的 Step 4b 模板未更新。

**修改内容**：
- 新增：Phase 1「用户视角预想」表格（4维度：典型触发场景/用户期望响应/误触发情形/认知根确认）
- 修改：Phase 2 占位结构 → 加入通过判定标准、完整 Gap 记录表（含严重程度列）、接受风险记录表

**备份路径**：`history/SKILL_v1.0_20260324_before_v12fields.md`

**验证状态**：🔵 待验证
