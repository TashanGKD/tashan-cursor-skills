# Skill 产品定义卡片：document-pipeline

> 关系类型：implements → 用户在对话中描述的「统一写作链路」设计方案
> 由 skill-designer 引导生成，2026-03-19

---

## 基本信息

| 字段 | 内容 |
|---|---|
| 组件名称 | `document-pipeline` |
| 组件类型 | Skill |
| 复杂度级别 | Level 4（系统型）—— 合并/重构 3 个已有 Skill，新建 3 个子 Skill |
| 开发日期 | 2026-03-19 |
| 需求来源 | 用户直接提出（对话：「写作→审核→绘图（绘图审核）→最终 MD 手稿」完整链路） |

---

## 一、人层设计（Human Layer）

### 1.1 解决什么问题？

```
现有写作 Skill 碎片化（wechat-article-writer / general-article-writer / research-output），
各自有不同的链路、不同的触发词、不同的缺口（有的有审核无配图审核，有的有配图无审核）。
用户需要一条完整的、任意 Stage 可入场的写作流水线，
最终产出：带原始 Mermaid + 大量 qwen-image 嵌入图的 MD 手稿，以及可选的格式转换（HTML/LaTeX）。
```

### 1.2 触发条件（人的视角）

```
典型触发语句：
- 「写一篇关于XXX的文章/文档/报告」
- 「帮我研究一下XXX，写成文档」
- 「我有初稿了，帮我检查逻辑」
- 「帮我画一下这篇文章的图」
- 「这篇文章/文档准备好了，给审稿者审一下」
- 「把这个 MD 转成 HTML / LaTeX」
- 「继续完成这篇文章」
- 「从配图开始」/ 「只要审稿」/ 「只转格式」

触发场景：
- 用户要写任何形式的文章/文档/报告（不限题材）
- 用户已有草稿，需要继续走后续步骤
- 用户明确说明从哪个阶段入场

明确不应该触发的情况：
- 用户只是问一个问题（「XX 是什么意思？」）→ 直接回答
- 用户要修改现有代码 → role-前端/后端开发
- 用户要做认知结构更新 → cognitive-update-knowledge
- 用户要做 L1 文档的受控更新 → cognitive-update-knowledge
```

### 1.3 成功标准（人的视角）

```
产出物：
- 主产出：完整 Markdown 手稿（含原始 Mermaid 代码块 + qwen-image base64 嵌入）
- 可选产出：HTML 文件（微信公众号场景）/ LaTeX + PDF（学术论文场景）
- 审稿报告：article-proofreading 的问题清单

质量判断标准（人如何判断「Skill 工作了」）：
- 文章逻辑自洽（无前后矛盾、无跳跃）
- 所有关键主张有来源或标注「[待核实]」
- 图文对应（图解释了文字，文字引用了图）
- 有结构化目录
- 审稿者通过（article-proofreading）
- 参考资料完整列出
```

### 1.4 MVP 边界

```
✅ 做（v1.0）：
- 统一的 Stage 0-8 流水线
- 任意阶段入场（Stage 0 检测用户当前状态）
- Stage 1：研究 + 草稿（WebSearch + 写作风格手册）
- Stage 2：逻辑自检（coherence + 概念一致性）
- Stage 3：真实性校对（fact-check，来源标注）
- Stage 4：画图规划（基于全场景绘图指南）
- Stage 5：批量画图（Mermaid + qwen-image，Mermaid 保留原始代码）
- Stage 6：图片自审（每张图是否准确表达意图）
- Stage 7：交给审稿者（article-proofreading 自动触发）
- Stage 8（可选）：格式转换分叉（HTML / LaTeX / 保持 MD）
- 已有 Skill 变为 thin wrapper（保持触发词兼容，内部调用 document-pipeline）

❌ 不做（v1.0）：
- image-ideation 多视角构思子 Skill（保留 Step 4 内联规划，等 v2.0 独立）
- image-generator 独立子 Skill（Stage 5 内联执行）
- image-reviewer 独立子 Skill（Stage 6 内联执行）
- 多人协作（实时协同审稿）
- 自动发布（告知步骤，不代执行）
```

---

## 二、Agent 层设计（Agent Layer）

### 2.1 触发条件（AI 视角）

```
触发条件（精确描述）：
IF 用户表达了「产出一篇文档/文章/报告」的意图
   OR 用户提供了一份草稿并要求「继续/审核/配图/转格式」
   OR 用户明确说「从[Stage名称]开始」
THEN 触发 document-pipeline

Stage 入场点识别（AI 需要在 Stage 0 判断）：
- 用户有草稿 + 要求「检查逻辑/审核逻辑」 → Stage 2 入场
- 用户有草稿 + 要求「检查真实性/核实内容」 → Stage 3 入场
- 用户有草稿 + 要求「画图/配图」 → Stage 4 入场
- 用户有草稿已配图 + 要求「审稿/给审稿者看」 → Stage 7 入场
- 用户有审稿通过的 MD + 要求「转 HTML/LaTeX」 → Stage 8 入场
- 无草稿 → Stage 1 入场

与其他组件的优先级：
- vs wechat-article-writer：wechat-article-writer 触发词命中时，转发到本 Skill 并标记 target_format=html
- vs general-article-writer：同上，标记 target_format=md
- vs research-output：调研类任务命中时，转发到本 Skill 并标记 mode=research，target=knowledge-library
- vs cognitive-update-knowledge：L1 认知结构文档更新 → 不触发本 Skill
```

### 2.2 执行步骤（精确序列）

```
Stage 0  入场检测（必须执行，确认 3 件事）
         输入：用户消息 + 上下文中是否有草稿文件/粘贴内容
         操作：
           A. 判断目标格式（target_format）：
              - 「公众号/微信/WeChat」→ html
              - 「学术论文/LaTeX/论文」→ latex
              - 其他/未说明 → md（询问是否需要转换）
           B. 判断入场 Stage（per 2.1 Stage 入场点识别）
           C. 判断文档维度（用于保存路径，仅 mode=research 时）：
              per research-output Step 0 的维度映射表
         输出：[target_format, entry_stage, dimension（若 research 模式）]
         失败时：若无法判断入场 Stage → 明确询问「你现在在哪个阶段？有初稿了吗？」

Stage 1  研究 + 草稿
         输入：主题/指令 + 写作风格手册（Read WG）+ WebSearch 结果
         操作：
           1. Read 写作风格手册（路径：认知结构/L1/写作维度/写作习惯与风格手册.md）
              文件不存在 → 使用默认约束（防AI腔/段落有实质内容/逻辑先行）
           2. 对主题执行 2-3 次 WebSearch，读取关键页面
           3. 按风格手册约束写草稿
              - 每节标题 + 实质内容（不写空话）
              - 重要主张标注来源 [来源N]
              - 记录「待确认」内容用 [?? 待核实] 标注
              - 在文档末尾维护「参考资料」占位
         输出：草稿 MD（内存，不写文件）
         失败时：WebSearch 全部失败 → 继续写，但标注「此节基于 AI 训练知识，无实时来源」

Stage 2  逻辑自检
         输入：Stage 1 草稿（或用户提供的初稿）
         操作：
           逐节检查：
           A. 论点是否有论据支撑（「有结论无过程」的段落标出）
           B. 概念是否前后一致（同一概念不同说法 → 统一）
           C. 段落间是否有跳跃（前一段到后一段有隐含的推理步骤 → 补出）
           D. 结构是否符合文章类型（说明类应有定义→展开→示例；分析类应有问题→分析→结论）
         输出：
           - 修订后的草稿（自动修复小问题）
           - 「逻辑自检报告」（3行以内：主要发现 + 已修/未修）
         失败时：如果概念冲突严重 → 停下来，向用户描述冲突，等决策后继续

Stage 3  真实性校对
         输入：Stage 2 草稿
         操作：
           A. 扫描所有 [来源N] 标注，抽查 2-3 条验证 URL 可访问
           B. 扫描所有无来源的「事实性主张」（包含数字/年份/机构名/论文引用）
           C. 对无法核实的内容一律标注 [待核实：原因]
           D. 不删除无来源内容，只标注
         输出：草稿（含 [待核实] 标注）+ 「核查摘要」（已核实N条 / 待核实M条）
         失败时：所有来源均无法访问 → 如实标注，不捏造

Stage 4  画图规划
         输入：Stage 3 草稿 + 全场景绘图指南（Read）
         操作：
           1. Read 全场景绘图指南
              路径：Glob **/全场景绘图指南.md
              未找到 → 使用内置基础判断（流程→flowchart，层级→graph LR，对比→table）
           2. 扫描草稿，识别以下位置：
              - 「流程/步骤/顺序关系」→ Mermaid flowchart
              - 「层级/架构/包含关系」→ Mermaid graph LR
              - 「时序/交互」→ Mermaid sequenceDiagram
              - 「多维比较/矩阵/空间分布」→ qwen-image（Mermaid 不适合）
              - 「概念框架/循环/飞轮」→ qwen-image
              - 「数据可视化/统计图」→ qwen-image
           3. 为每个画图位置生成：
              [图编号] 位置描述 | 图类型 | Mermaid代码/qwen提示词草稿
         输出：画图计划列表（内存）
         失败时：无法识别任何适合画图的位置 → 询问「这篇文章是否需要配图？哪些地方？」

Stage 5  批量画图
         输入：Stage 4 画图计划 + Stage 3 草稿
         操作：
           A. Mermaid 图：直接插入代码块到对应位置
           B. qwen-image 图：
              1. Read wechat-article-writer/SKILL.md Step 4 获取 Python 生成代码
              2. 替换 prompt 为画图计划中的提示词
              3. 执行 Shell → 生成 base64 图
              4. 嵌入格式：
                 ```mermaid
                 [原 Mermaid 代码，保留]
                 ```
                 > 可视化增强版：
                 ![图描述](data:image/png;base64,[base64])
                 
                 若无 Mermaid：
                 ![图描述](data:image/png;base64,[base64])
           C. 按顺序处理，全部完成后继续
         输出：草稿（含所有图）
         失败时：单张图失败 → 保留 Mermaid，标注 [qwen-image 生成失败，保留文字版]
                 全部失败 → 保留所有 Mermaid，末尾标注原因，继续流程

Stage 6  图片自审
         输入：Stage 5 草稿（含所有图）
         操作：
           对每张 qwen-image 图：
           A. 图与对应文字是否一致（图中展示的是文字描述的内容吗？）
           B. 图中元素是否正确（流向/标签/颜色语义）
           C. 是否需要重生成？
              - 严重不符 → 重新生成（最多重试 1 次，失败则保留标注）
              - 轻微偏差 → 标注「[图待优化：XXX]」，继续
         输出：
           - 修订后草稿（含修复/标注）
           - 「图片自审报告」（通过/待优化/失败各多少张）
         失败时：所有图均失败 → 如实告知，询问是否继续审稿

Stage 7  交给审稿者
         输入：Stage 6 草稿
         操作：
           自动调用 article-proofreading Skill，传入：
           - 草稿全文
           - 文章类型标注（research/article/report）
         输出：
           - 审稿报告（article-proofreading 产出）
           - 修订后草稿（根据审稿意见修改后）
         失败时：article-proofreading Skill 未找到 → 执行内置简化审稿
                 （检查：AI腔/绝对表达/标题写法/结语完整性）

Stage 8  格式转换（可选，按 target_format 分叉）
         输入：Stage 7 草稿 + target_format
         操作：
           target_format = html：
             → 调用 wechat-article-writer Stage 5-8（转换 + 排版核查 + 底部模板）
           target_format = latex：
             → 调用 academic-si-writer（LaTeX 格式转换 + PDF 生成）
           target_format = md（默认）：
             → 保存到对应路径（research 模式：L1/[维度]/知识库/；其他：由用户指定）
             → 执行 research-output Step 5 的三处注册（若 research 模式）
         输出：
           - md：Markdown 文件已保存
           - html：HTML 文件 + 发布指引
           - latex：.tex 文件 + 编译指令
         失败时：
           html 转换失败 → 保存 MD，提示用户手动转换
           latex 转换失败 → 保存 MD，提示用户手动处理
```

### 2.3 边界条件

```
情况A：用户中途打断（如 Stage 3 打断） → 询问「是否继续，还是修改草稿后再继续？」
情况B：文档非常长（>5000 字） → Stage 2/3 分节处理，不跳过任何节
情况C：research 模式 + target=knowledge-library + 维度判断失败
        → 明确询问「这属于哪个维度？[列出6个维度选项]」
情况D：用户说「只画图不审稿」→ 跳过 Stage 7，从 Stage 4 到 Stage 6 到 Stage 8
情况E：用户说「已经画好图了，但想要审稿」→ 从 Stage 7 入场，不重新画图
情况F：全场景绘图指南不存在 → Stage 4 使用内置基础判断，不终止
情况G：写作风格手册不存在 → Stage 1 使用内置默认约束，不终止
```

### 2.4 依赖声明

```
依赖的其他 Skill/Agent/Rule：
- article-proofreading：Stage 7 调用，传入草稿全文
- wechat-article-writer：Stage 8 html 分支调用其 Step 5-8
- academic-si-writer：Stage 8 latex 分支调用
- research-output Step 5：Stage 8 md+research 模式时调用三处注册

会影响的其他 Skill/Agent/Rule：
- wechat-article-writer：变为 thin wrapper，内部转发到本 Skill（保持触发词兼容）
- general-article-writer：同上
- research-output：变为 thin wrapper（research 模式入口）
```

### 2.5 常见失败模式

```
失败模式1：Stage 0 入场点判断错误（最常见）
  → 根本原因：用户有草稿但 AI 未识别，从 Stage 1 重新写导致覆盖草稿
  → 预防方法：Stage 0 检测上下文中是否有 「```、---、#标题」等草稿信号
              若检测到 → 明确问「你有现成草稿吗？从哪一步开始？」

失败模式2：Stage 5 qwen-image 全部失败后继续，导致最终输出无图
  → 根本原因：失败静默处理，用户不知道图没有生成
  → 预防方法：Stage 5 失败时明确告知「N张图生成失败，当前文档为文字+Mermaid版本」

失败模式3：Stage 7（审稿）通过后，用户认为已结束，但 Stage 8 转换未做
  → 根本原因：Stage 7 完成时的完成信号让用户误以为全部完成
  → 预防方法：Stage 7 完成时明确输出「✅ 审稿完成。下一步：Stage 8 格式转换（目标：[target_format]）。是否继续？」

失败模式4：同时有 wechat-article-writer 和 document-pipeline 触发词命中，AI 不知选哪个
  → 根本原因：触发词重叠
  → 预防方法：明确 wechat-article-writer 是 thin wrapper，优先级低于 document-pipeline

回退动作：
- 若 Stage 2 逻辑自检发现严重矛盾 → 停下，向用户呈现矛盾，由用户决策修改方向
- 若 Stage 3 核实内容严重不可信 → 停下，标注后等用户确认是否继续
```

### 2.6 强绑定 Rule

```
强绑定（违反则输出不可信）：
- R2 NO_FABRICATION：禁止捏造来源、数据、引用 —— 所有无法核实的内容必须标注
- R1 EVIDENCE_FIRST：来源类别明确标注（WebSearch / 知识 / 推断）
- R3 READ_FIRST：Stage 1 必须真正执行 WebSearch，不允许纯凭训练知识写有事实性主张的文档

推荐注入：
- R6 ARTIFACT_FIRST：输出必须落到正式文件，不允许只在对话中展示
- R8 VERIFY_BEFORE_FREEZE：Stage 7 审稿通过后才能执行 Stage 8 保存
```

---

## 三、人层 vs Agent 层张力分析

```
人层设计中「不言而喻」的假设：
- 「逻辑自检」是 AI 以批判者视角扫描，而非只格式化 → AI 可能只做格式整理
  修订：Stage 2 明确要求「找出无论据的结论、概念不一致、段落跳跃」
- 「任意 Stage 入场」意味着用户可以跳过之前的 Stage → AI 可能坚持从 Stage 1 开始
  修订：Stage 0 明确：用户说「从 Stage X 开始」或「已经有 Y 了」时，尊重用户判断，不强制从头
- 「Mermaid 原始代码必须保留」→ AI 可能只保留图片，删除代码块
  修订：Stage 5 明确：qwen-image 是对 Mermaid 的补充，不替代

AI 可能产生歧义的点：
- 「审稿者」：AI 可能以为自己就是审稿者 → 明确是 article-proofreading Skill（独立视角）
- 「画图规划」中的「Mermaid 不适合」判断 → AI 判断标准不一致 → 给出明确的图类型→工具映射表
- 「thin wrapper」：AI 可能不知道如何实现 → 需要在 wechat-article-writer 变更记录中明确写转发逻辑

两层对齐后的修订：
- Stage 0 增加「草稿检测信号」（解决失败模式1）
- Stage 5 增加「Mermaid 保留」的明确约束
- Stage 7 结束时增加「下一步提示」（解决失败模式3）
```

---

## 四、复杂度评估

```
与现有 Skill/Rule 的交互点：
- wechat-article-writer：变为 thin wrapper，调用本 Skill
- general-article-writer：变为 thin wrapper
- research-output：变为 thin wrapper（research 模式入口）
- article-proofreading：Stage 7 调用
- academic-si-writer：Stage 8 latex 分支调用
- role-menu.mdc：新增触发词注册 + 现有触发词路由修改
- skill-index/SKILL-INDEX.md：新增条目
- auto-experience-hook：任务完成后自动触发（已有规则，不需修改）

Level 判断依据：
[x] Level 4：重构现有系统（wechat/general/research 三个 Skill 变 thin wrapper），
             影响多个组件的交互关系，新建核心统一组件

最终级别：Level 4
```

---

## 五、关卡执行记录

### 关卡A：AI 执行者模拟（待执行）

```
执行者：/skill-simulator 子智能体
执行日期：待执行

结论：[ ] 通过 / [ ] 需修改后重新审核
```

### 关卡B：Skill 系统破坏（待执行）

```
执行者：/skill-system-destroyer 子智能体
执行日期：待执行

结论：[ ] 通过 / [ ] 需修改后重新审核
```

### 关卡C：行为验证（待执行）

```
执行者：/verifier 子智能体
执行日期：待执行

结论：[ ] 通过 / [ ] 需修改后重新审核
```

---

## 六、配套变更计划（Level 4 必填）

```
需要同步修改的已有组件：

A. wechat-article-writer → 改为 thin wrapper
   变更：description 保持不变（触发词兼容）
   新 Step 1：触发后转发到 document-pipeline，标注 target_format=html
   废弃：原 Step 1-8 内部逻辑（保留在 history/ 备份）

B. general-article-writer → 改为 thin wrapper
   变更：同上，target_format=md

C. research-output → 改为 thin wrapper
   变更：description 保持不变（触发词兼容）
   新 Step 1：转发到 document-pipeline，标注 mode=research，target=knowledge-library

D. role-menu.mdc → 新增 document-pipeline 条目，更新 wechat/general/research 触发词指向

E. SKILL-INDEX.md → 新增 document-pipeline 条目

需要新建的组件（v2.0 规划，本版不做）：
- image-ideation（独立子 Skill，Stage 4 调用）
- image-generator（独立子 Skill，Stage 5 调用）
- image-reviewer（独立子 Skill，Stage 6 调用）
```
