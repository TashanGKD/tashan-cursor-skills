---
name: document-pipeline
description: 统一写作流水线。任何文档/文章/报告均走此流程：研究→草稿→逻辑自检→真实性校对→画图规划→批量画图→图片自审→审稿→格式转换（HTML/LaTeX/MD）。可从任意阶段入场（已有草稿直接审核，已审稿直接转格式）。触发词：「写一篇/帮我写/写一份/我有初稿了/帮我检查逻辑/帮我配图/从画图开始/从[Stage名称]开始继续/转成HTML/转成LaTeX」。注意：「只要审稿」请直接触发 article-proofreading；「帮我审稿」不触发本 Skill。
---

# 统一写作流水线（document-pipeline）

> **适用范围**：任何类型的文档——知识库文章、微信公众号、学术论文、技术报告、产品分析等
> **核心价值**：一条完整的、任意阶段可入场的写作闭环，最终产出带原始 Mermaid + qwen-image 嵌入的 MD 手稿，以及可选的格式转换
> **与旧 Skill 的关系**：wechat-article-writer / general-article-writer / research-output 均为本 Skill 的 thin wrapper，触发词不变，内部转发到此处

---

## 触发判断（先执行）

```
触发条件：
IF 用户表达了「产出一篇文档/文章/报告」的意图
   OR 用户提供了草稿并要求「继续/检查/配图/审稿/转格式」
   OR 用户明确说「从 Stage X 开始」/ 「只要做 Y」
THEN 执行 Stage 0，确定入场点和目标格式

不应触发的情况（让 AI 直接回答即可）：
- 用户只问一个知识性问题（「XX 是什么？」）
- 用户要修改代码 → role-前端/后端开发
- 用户要更新 L1 认知结构文档 → cognitive-update-knowledge
- 用户要做学术 SI 补充材料 → academic-si-writer（全局 Skill）
```

---

## Stage 0：入场检测（必须执行）

> 确认 3 件事：① 从哪个 Stage 开始 ② 目标格式 ③ 若是调研模式，确认维度

```
A. 判断 target_format：
   - 用户说「公众号/微信/WeChat/推文」→ target_format = html
   - 用户说「学术论文/LaTeX/论文/期刊」→ target_format = latex
   - 用户说「知识库/认知结构/调研笔记/研究报告」→ target_format = md + mode = research
   - 其他/未说明 → target_format = md（默认，不询问，直接继续）

B. 判断入场 Stage（规则1优先于规则2，触发词优先）：
   规则1：用户说了明确的操作关键词时，直接采用，不检查草稿信号：
   - 用户提供了完整草稿（有目录/多节/超过500字）+ 说「检查逻辑/审核结构/逻辑有没有问题」→ 入场 Stage 2
   - 用户提供了完整草稿（有目录/多节/超过500字）+ 说「核实/真实性/事实有没有错/来源」→ 入场 Stage 3
   - 用户提供了完整草稿（有目录/多节/超过500字）+ 说「配图/画图/加图/从画图开始」→ 入场 Stage 4
   - 用户提供了完整草稿（已有图）+ 说「审稿/给审稿者/交给审核」→ 入场 Stage 7
   - 用户提供了已审稿的 MD + 说「转 HTML/转 LaTeX/发布」→ 入场 Stage 8
   - 用户说「写一篇/帮我写/我想写/研究一下并写成文档」→ 入场 Stage 1
   - 无法判断 → 询问「你现在在哪个阶段？有现成草稿吗？」

C. 若 mode = research，判断文档所属维度（存储路径用）：
   - 技术/工具/架构/系统/API → 系统架构思维维度
   - 认知科学/学习/注意力 → 认知科学基础维度
   - 产品设计/商业/市场/用户研究 → 产品视野维度
   - 写作/内容/表达/传播 → 写作维度
   - 研究方法/学术规范/论文写作 → 研究范式维度
   - 组织管理/团队/协作/运营 → 组织管理维度
   research 模式的 6 个维度选项：
   ① 系统架构思维维度：技术/工具/架构/系统/API/框架/开源项目
   ② 认知科学基础维度：认知/学习/注意力/记忆/心理/神经
   ③ 产品视野维度：产品设计/商业/市场/用户研究
   ④ 写作维度：写作/内容/表达/传播/媒体
   ⑤ 研究范式维度：研究方法/学术规范/论文写作
   ⑥ 组织管理维度：组织/团队/协作/运营/管理
   - 多维度命中（话题横跨多个维度）→ 列出候选维度询问用户选择
   - 零维度命中（话题不在任何维度关键词中）→ 默认存入①系统架构思维维度，标注 [待分类]
   - 完全无法判断 → 列出以上 6 个选项让用户选择

Stage 0 输出：[target_format, entry_stage, dimension（research 模式）]

  ⚠️ 单任务声明：整条流水线（Stage 0-8）视为一次完整任务。
  auto-experience-hook 仅在流水线最终完成（Stage 8 结束或用户明确终止）时触发一次，
  不在每个 Stage 完成时独立触发。
```

---

## Stage 1：研究 + 草稿

> 从零开始写。按需搜索，遵循写作风格手册。

```
输入：主题/指令 + 用户补充说明

Step 1.1  读取写作风格手册（必做，不可跳过）
  路径：_内部总控/认知结构/L1_系统性文档/待建维度/写作习惯与风格手册.md
  提取 4 类约束（语言风格 / 禁止事项 / 段落规范 / 结构原则）
  文件不存在 → 使用内置默认约束：
    - 禁止 AI 腔（不写「综上所述/值得注意/不难发现」等空话）
    - 每段有实质内容，不以罗列替代分析
    - 结论先行，论据在后
    - 禁止「一是…二是…三是…」排比句堆砌

Step 1.2  网络搜索（主题涉及外部知识时执行）
  执行 2-3 次 WebSearch（不同角度的查询词）
  对重要结果执行 WebFetch 获取原文
  来源记录：[来源N] 作者/机构 | 标题 | URL | YYYY-MM-DD

Step 1.3  写草稿（遵循 Step 1.1 风格约束）
  结构：
    - 文章类型/研究报告：摘要 → 目录 → 正文各节 → 参考资料
    - 知识库文档（research 模式）：REF-EXT 头部占位 → 摘要 → 目录 → 各节 → 参考资料
  
  写作要求：
    - 重要主张标注来源 [来源N] 或 [待核实]
    - 关键概念首次出现时定义
    - 段落间有显式的逻辑连接（不允许段落跳跃）
    - 结尾必须有「## 参考资料」节（格式：[来源N] 作者 | 标题 | URL | 日期）

输出：草稿（内存，不写文件，等 Stage 8 统一写入）
失败处理：
  WebSearch 全部失败 → 继续写，在摘要后标注「[本文基于 AI 训练知识，无实时来源，请核实]」
```

---

## Stage 2：逻辑自检

> 以批判者视角扫描，不只是格式整理。

```
输入：草稿（来自 Stage 1，或用户提供的初稿）

检查项（逐节执行）：
  A. 论点-论据完整性：
     有结论但无过程的段落 → 标注「[?? 需补充论据：此处结论跳跃]」
  
  B. 概念一致性：
     扫描同一概念的不同表述（如「用户」vs「客户」vs「访客」）
     若存在混用 → 统一为最准确的表述，全文替换
  
  C. 段落间跳跃：
     前段到后段若存在未说明的推理步骤 → 补出过渡句
  
  D. 结构合理性：
     说明类：定义 → 展开 → 示例
     分析类：问题 → 分析 → 结论
     比较类：维度 → 逐项比较 → 综合判断
     若结构不符 → 调整节顺序，不修改内容

  ⚠️ 硬约束：
  - 禁止改写任何句子的措辞和风格（哪怕 AI 觉得「这句话可以更好」）
  - 只允许：插入标注、补充过渡句、调整节顺序、统一概念表述
  - 如果判断不了是否属于「逻辑修复」，默认不修改，标注供用户决策

输出：
  - 修订后草稿（已修复小问题）
  - 逻辑自检报告（3行以内：主要发现 + 已修/未修说明）

失败处理：
  若发现严重概念矛盾（同一概念两处含义根本不同）→
  停下，向用户描述矛盾：「[概念X] 在第N节指的是A，但在第M节指的是B，请确认哪个是正确的」
  等用户决策后继续
```

---

## Stage 3：真实性校对

> 核实来源，标注无法核实的内容。不删除，只标注。

```
输入：Stage 2 草稿

Step 3.1  验证已标注来源
  抽查 2-3 条 [来源N]，尝试 WebFetch 验证 URL 可访问且内容对应
  URL 失效 → 标注「[来源N 链接失效，待更新]」

Step 3.2  扫描未标注的事实性主张
  触发标准（以下任一）：
    - 包含具体数字/百分比
    - 包含年份 + 事件
    - 引用机构/组织的政策或数据
    - 描述某技术/产品的具体能力（"支持X个/达到X%"）
  
  处理方式：
    - 可查到来源 → 添加 [来源N] 并加入参考资料节
    - 无法核实 → 标注「[待核实：需确认此数据来源]」
    - 基于已知 AI 训练知识 → 标注「[基于训练知识，建议人工核实]」

Step 3.3  不删内容原则
  即使某段内容疑似有误，也只标注，不删除。
  「[?? 可能有误：建议核实 XXX]」

输出：
  - 草稿（含 [待核实] 标注）
  - 核查摘要：「已核实 N 条 / 待核实 M 条 / 失效链接 K 条」

失败处理：
  所有来源 URL 均无法访问 → 如实标注，不捏造，告知用户
```

---

## Stage 4：画图规划

> 确定哪些地方需要图，哪种图，生成什么内容。

```
输入：Stage 3 草稿

Step 4.1  读取全场景绘图指南
  执行 Glob: **/全场景绘图指南.md
  找到 → 读取「关系类型 → 图类型映射」部分
  未找到 → 使用内置基础映射（见下方备用映射表）

Step 4.2  扫描草稿，标记画图位置
  对每一节，判断是否有以下信号：
  
  → Mermaid flowchart：
    流程/步骤/执行顺序/决策分支
    
  → Mermaid graph LR：
    层级/包含/架构/模块依赖/组织结构
    
  → Mermaid sequenceDiagram：
    时序/多方交互/API 调用链
    
  → qwen-image（Mermaid 不适合的）：
    多维比较/矩阵/象限图
    概念框架/循环/飞轮/生态系统
    数据可视化/统计图表
    需要视觉美感的架构概览图
    已有 Mermaid 的位置 → 同时安排 qwen-image 可视化增强版

Step 4.3  生成画图计划
  格式（每项）：
  [图编号] | 位置（第N节，段落描述） | 类型（Mermaid-flowchart/qwen-image/等）| 内容描述 | 提示词草稿

备用基础映射表（绘图指南不可用时）：
  流程/步骤 → Mermaid flowchart TD
  层级/架构 → Mermaid graph LR
  时序/API → Mermaid sequenceDiagram
  比较/分析/框架 → qwen-image
  已有 Mermaid → 额外添加 qwen-image 可视化版

输出：画图计划列表（内存）

失败处理：
  扫描完整篇，确实没有适合画图的位置（纯文字性文档） →
  询问「这篇文档是否需要配图？如需要，请告诉我哪些地方，或跳过直接进入 Stage 7 审稿」
```

---

## Stage 5：批量画图

> Mermaid 直接插入（保留原始代码），qwen-image 生成并嵌入 base64。

```
前置检查（Stage 5 入场时必做）：
  A. 是否有内存草稿（来自 Stage 1-4）或用户提供的文档？
     无 → 询问「请提供要插入图片的文档，或输入占位符（我会创建空白文档嵌入图片）」
     有 → 继续
  B. 是否有 Stage 4 的画图计划列表？
     无（用户直接给了图描述）→ 将用户输入解析为画图计划格式：
       [图编号] | 内容描述（用户给的） | 类型（根据内容判断 Mermaid/qwen-image） | 嵌入位置（草稿末尾）
     有 → 继续

输入：Stage 4 画图计划 + Stage 3 草稿

对每个 Mermaid 图（按计划顺序）：
  在草稿对应位置插入：
  \`\`\`mermaid
  [Mermaid 代码]
  \`\`\`

对每个 qwen-image 图：
  Step 5.1  执行 qwen-image 生成（API 参数内嵌，不依赖其他 Skill）
    API_KEY 获取顺序（按优先级）：
    1. 读取 _内部总控/凭证/dashscope_key.md 中的 key 值（首选）
    2. 读取环境变量 QWEN_API_KEY（次选）
    3. 使用内嵌备用 Key：sk-68b70d6863b94c299ecd27e9d49b41ba（仅用于测试场景）
    
    执行以下 Shell 命令（替换 PROMPT 为画图计划中的提示词）：
    \`\`\`bash
    python -c "
import requests, base64, json
url = 'https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis'
headers = {'Authorization': 'Bearer sk-68b70d6863b94c299ecd27e9d49b41ba', 'Content-Type': 'application/json', 'X-DashScope-Async': 'enable'}
body = {'model': 'wanx2.1-t2i-turbo', 'input': {'prompt': 'PROMPT'}, 'parameters': {'size': '1024*1024', 'n': 1}}
r = requests.post(url, headers=headers, json=body)
task_id = r.json()['output']['task_id']
import time; time.sleep(8)
r2 = requests.get(f'https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}', headers={'Authorization': 'Bearer sk-68b70d6863b94c299ecd27e9d49b41ba'})
img_url = r2.json()['output']['results'][0]['url']
img = requests.get(img_url).content
print(base64.b64encode(img).decode())
"
    \`\`\`
    获取 base64 字符串（stdout 输出）
  
  Step 5.2  嵌入文档
    若该位置已有 Mermaid：
    \`\`\`mermaid
    [原 Mermaid 代码，保留不删]
    \`\`\`
    > 可视化增强版：
    ![图描述](data:image/png;base64,[base64字符串])
    
    若该位置无 Mermaid：
    ![图描述](data:image/png;base64,[base64字符串])

输出：草稿（含所有 Mermaid 代码块 + qwen-image base64）
⚠️ 不输出完成信号，不等用户确认，立即进入 Stage 6。

失败处理：
  单张 qwen-image 生成失败 → 保留 Mermaid，标注「[图生成失败：XXX，保留文字版本]」
  所有 qwen-image 全部失败 →
    保留所有 Mermaid
    末尾标注「[图片生成服务暂时不可用，已保留 Mermaid 版本]」
    明确告知用户后继续 Stage 6
```

---

## Stage 6：图片自审

> 每张 qwen-image 图与对应文字对照，严重不符则重生成（最多 1 次）。

```
输入：Stage 5 草稿（含所有图）

对每张 qwen-image 图执行：
  A. 图与文字一致性：
     图展示的内容 == 对应段落描述的内容？
     
  B. 图内元素正确性：
     流向/箭头方向正确？
     标签/文字无错误？
     颜色语义一致（如红色=危险/蓝色=信息）？
     
  C. 处理决策：
     严重不符（图展示了完全不相关的内容）→ 重新生成（最多 1 次）
       重新生成失败 → 删除该图，标注「[图片无法生成符合要求的版本，已删除]」
     轻微偏差（大体正确，细节不够精确）→ 标注「[图待优化：XXX]」，不重生成
     完全准确 → 无需操作

输出：
  - 修订后草稿（含重生成的图或删除/标注）
  - 图片自审报告：「N 张通过 / M 张轻微偏差待优化 / K 张删除重试失败」

失败处理：
  图片服务完全不可用 → 跳过自审，直接进 Stage 7，末尾标注「[Stage 6 跳过：图片服务不可用]」
```

---

## Stage 7：交给审稿者

> 自动触发 article-proofreading，独立视角，全面挑问题。

```
输入：Stage 6 草稿

Step 7.1  触发 article-proofreading Skill
  传入草稿全文 + 文章类型标注（research/article/report/analysis）
  
  article-proofreading Skill 会检查：
    - AI 腔检测（绝对表达/套话/无实质内容的结构）
    - 标题写法（4种错误类型）
    - 逻辑跳跃（补充逻辑）
    - 概念一致性（再次验证）
    - 结语完整性

Step 7.2  根据审稿结论执行
  P0（严重，必须修改）→ AI 直接在草稿中修复
  P1/P2（建议）→ 输出建议清单，询问用户是否采纳

Step 7.3  完成信号
  审稿通过后，明确输出：
  「✅ 审稿完成。
   选择下一步（必须选一个）：
   A. 进行 Stage 8 格式转换（目标：[target_format]）
   B. 跳过格式转换，直接保存为 Markdown 文件（询问保存路径）
   C. 不保存，结束
   
   ⚠️ 选 A 或 B 才会保存文件，选 C 会丢失所有工作。」

  若用户选 C：AI 必须发出独立二次确认：
  「⚠️ 确认放弃？从 Stage 1 到 Stage 7 的所有工作将全部丢失，无法恢复。
   输入「确认放弃」继续，或选择 A/B 保存文档。」
  用户明确说「确认放弃」后 → 终止，不写任何文件。

备用方案（article-proofreading Skill 不可用时）：
  执行内置简化审稿：
  1. 扫描「综上所述/值得注意/不难发现/显而易见」等 AI 腔词语 → 建议删除
  2. 检查标题是否含感叹号/过度修饰词 → 建议修改
  3. 检查结尾段落是否存在 → 不存在则提醒添加
  标注「[使用内置简化审稿，建议后续补充完整审稿]」

输出：
  - 审稿通过的草稿（已修复 P0）
  - P1/P2 建议清单（若有）
```

---

## Stage 8：格式转换与保存（可选）

> 按 target_format 分叉，保存到对应位置。

```
输入：Stage 7 草稿 + target_format + dimension（research 模式）

分叉 A：target_format = html
  ⚠️ 不调用 wechat-article-writer（避免循环调用，HTML 逻辑内联执行）
  
  Step A.0  Markdown 真源确认（内联 wechat-article-writer Step 4.5 逻辑）
    确认手稿内容已冻结，不再修改
    任何内容修改必须先改 MD 手稿，再生成 HTML
  
  Step A.1  F-022 挑战者反思（公众号专属，内联 wechat-article-writer Step 6.8 逻辑）
    以「第一次读这篇文章的普通读者」视角检查 3 点：
    1. 哪个段落理解障碍最大（信息密度过高/概念跳跃）？
    2. 标题与正文最核心内容是否一致？
    3. 文章最弱的一段在哪里（内容最空洞/逻辑最跳跃）？
    发现可修复问题 → 修复后继续；无重大问题 → 输出「内容自检：[轻微问题描述]」
  
  Step A.2  转换为微信 HTML
    参照 _内部总控/AI思维碎片/微信公众号发布手册.md §2 HTML 规范
    图片：base64 嵌入，不引用本地路径
    颜色：H2=#2980b9，H3=#e67e22，strong=#e74c3c，协会简介=#7f8c8d
  
  Step A.3  添加底部模板
    参照发布手册 §4.3：署名 → 分隔线 → TA SHAN logo → 协会简介 → 二维码 → 官网说明
  
  Step A.4  排版核查（运行 C:/Temp/check_html.py 或手动核查15项）
    → 15项全部 [OK] 才输出最终 HTML
  
  Step A.5  告知用户发布步骤（用浏览器打开 HTML 文件，复制到微信编辑器）
  
  输出：HTML 文件 + 发布指引

分叉 B：target_format = latex
  调用 academic-si-writer
  输出：.tex 文件 + 编译指令

分叉 C：target_format = md + mode != research
  询问保存路径（或使用用户指定路径）
  执行 Write：[用户指定路径]/[文件名]_YYYYMMDD.md
  输出：Markdown 文件路径

分叉 D：target_format = md + mode = research
  Step 8.1  确认保存路径
    路径：_内部总控/认知结构/L1_系统性文档/[dimension]/知识库/[文件名]_YYYYMMDD.md
    目录不存在 → 自动创建
  
  Step 8.2  补全 REF-EXT 头部（替换 Stage 1 的占位）
    > 文档类型：REF-EXT（外部参考知识）
    > 创建日期：YYYY-MM-DD
    > 使用目标：[填写]
    > 来源说明：[WebSearch/WebFetch获取]
    > 关联关系：[若有]
    > 注意：本文档为外部知识汇编，不算知识结构 L1/L2/L3 正文
    > 分类注记：文档分类清单.md 第十二节
  
  Step 8.3  写入文件
    执行 Write
  
  Step 8.4  三处注册（research 模式专属，不可跳过）
    ① 更新 文档分类清单.md 第十二节
       追加格式：| L1_系统性文档/[维度]/知识库/[文件名] | REF-EXT | [维度] | ★ CURRENT | [摘要，含行数+日期] |
    
    ② 更新 知识图谱_正式文档.md（REF-EXT 区段）
       路径：_内部总控/认知结构/知识图谱_正式文档.md
       操作：在 REF-EXT 表格最后一行之后追加一行
       格式：| REF-EXT-[序号] | [文件简称] | REF-EXT | [核心内容一句话] | L1/[维度]/知识库 |
       序号：读取现有 REF-EXT 条目的最大序号 +1
       注意：知识库/路径豁免 write-guard 的备份/变更记录要求，但知识图谱注册仍必须执行
    
    ③ 追加系统日志：_内部总控/认知结构/L3_原始记录/系统日志.md
       格式：[LOG-YYYYMMDD-NN] document-pipeline | 保存知识库文档 | [文件名]

  输出：
    - 已保存的 MD 文件路径
    - 分类清单更新确认
    - 系统日志条目

失败处理：
  HTML 转换失败 → 保存 MD，提示「HTML 转换失败，已保留 MD 版本，请手动转换」
  LaTeX 转换失败 → 保存 MD，提示「LaTeX 转换失败，已保留 MD 版本，请手动处理」
  写入失败 → 告知用户，提供草稿完整内容，请求手动保存
```

---

## 边界条件总表

| 情况 | 处理方式 |
|---|---|
| 用户中途打断 | 询问「是否继续，还是修改草稿后再从当前 Stage 继续？」|
| 文档超长（>5000字）| Stage 2/3 分节执行，不跳过任何节 |
| 用户说「只画图不审稿」| Stage 4→5→6→8，跳过 Stage 7 |
| 用户说「只转格式，其他都好了」| 直接 Stage 8 |
| 全场景绘图指南不存在 | Stage 4 使用内置映射，不终止 |
| 写作风格手册不存在 | Stage 1 使用内置默认约束，不终止 |
| research 模式维度无法判断 | 列出 6 个选项，等用户确认 |
| 用户同时触发 wechat-article-writer | 识别为 target_format=html，进入本 Skill |

---

## 强绑定规则

- **R2 NO_FABRICATION**：禁止捏造来源、数据、引用——无法核实的必须标注
- **R1 EVIDENCE_FIRST**：来源类别必须明确（WebSearch / AI知识 / 推断）
- **R3 READ_FIRST**：Stage 1 必须真正执行 WebSearch，不允许纯凭训练知识写含事实性主张的文档
- **R6 ARTIFACT_FIRST**：输出必须落到文件，不允许只在对话中展示
- **R8 VERIFY_BEFORE_FREEZE**：Stage 7 审稿通过后才能执行 Stage 8 保存

---

## 与现有 Skill 的关系

| Skill | 关系 | 行为 |
|---|---|---|
| wechat-article-writer | thin wrapper | 触发词命中 → 设置 target_format=html → 转发到本 Skill |
| general-article-writer | thin wrapper | 触发词命中 → 设置 target_format=md → 转发到本 Skill |
| research-output | thin wrapper | 触发词命中 → 设置 mode=research → 转发到本 Skill |
| article-proofreading | Stage 7 调用 | 传入草稿，接收审稿报告 |
| academic-si-writer | Stage 8 latex 调用 | 传入草稿，生成 LaTeX |
| article-image-angles | 可选增强 | Stage 4 用户主动说「我想看多个配图视角」时调用 |
| article-image-styles | 可选增强 | Stage 5 用户主动说「用某种风格」时调用 |

---

## 变更记录

### v1.0 — 2026-03-19 — 初始创建

**根因**：现有写作 Skill 碎片化（wechat-article-writer / general-article-writer / research-output），
各自有不同链路和缺口（有的有审核无配图审核，有的有配图无审核）。
用户需要一条完整的、任意 Stage 可入场的写作流水线，
最终产出带原始 Mermaid + qwen-image 嵌入的 MD 手稿 + 可选格式转换。

**设计决策**：
- Stage 0-8 统一核心链路，所有文档类型共用
- wechat/general/research 变为 thin wrapper，保持触发词兼容
- v1.0 Stage 4-6 内联实现，image-ideation/generator/reviewer 作为独立子 Skill 放 v2.0

**经历关卡**：关卡A / 关卡B / 关卡C（待执行）

**验证状态**：🔵 待验证
