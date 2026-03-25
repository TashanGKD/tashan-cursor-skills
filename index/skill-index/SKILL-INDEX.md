# Skill 总索引

> 本文件是全部 Skill 的中央索引，用于追踪 Skill 版本、触发词、L0 聚类归属。
> 初始建立：2026-03-19
> 维护规则：
> - 新建 Skill 时，必须在此索引中追加一行 + 记录变更
> - 版本号变更时，更新此索引 + 记录变更 + 说明
> - 废弃 Skill 时，标注状态为「已废弃」
> - 修改 Skill 时，更新版本号 + 说明

---

## 状态说明

| 状态 | 含义 |
|---|---|
| ✅ 已验证 | 已在真实场景中验证，行为符合预期 |
| 🔵 待验证 | 已设计并实现，等待真实场景验证 |
| ⚠️ 部分验证 | 部分步骤已验证，部分待验证 |
| ❌ 已废弃 | 不再使用，保留作历史记录 |
| ? 未知状态 | 老版本遗留，状态未跟踪 |

---

## 域协调者 Skill（分层治理 — 团队负责人层）[2026-03-23 新增]

> 分层治理架构：CEO（session-bootstrap）→ 域协调者（本层）→ 工人（各 role-* Skill）
> 域协调者不执行任务，负责：任务类型识别 → 执行序列规划 → briefing生成 → 门控把控

| Skill 名称 | 版本 | 状态 | 最新日期 | 触发词（部分）| 备注 |
|---|---|---|---|---|---|
| role-产品开发协调者 | v1.0 | 🔵 待验证 | 2026-03-23 | 新项目/新产品/做个功能/有个bug/发现问题/全量测试/产品开发 | 产品开发域团队负责人，5种任务类型决策树，测试驱动原则，含完整briefing协议 |

---

## 产品开发类 Skill（角色体系）

| Skill 名称 | 版本 | 状态 | 最新日期 | 触发词（部分）| 备注 |
|---|---|---|---|---|---|
| role-产品经理 | v1.7 | 🔵 待验证 | 2026-03-22 | 产品/需求/用户流/闭环/MVP/产品定义/开发计划 | v1.7：知识导航表新增 D0 认知根确认行（L1产品理论维度/AI时代产品问题全景框架）|
| role-技术架构师 | v1.2.1 | 🔵 待验证 | 2026-03-23 | 技术架构/系统设计/数据模型/接口规范/技术选型/API设计 | v1.2.1：新增知识导航表（D0→技术架构方案.md + ①②③④⑤）+ 元认知前置 |
| role-前端开发 | v1.7 | 🔵 待验证 | 2026-03-22 | 前端/React/TypeScript/Vite/UI实现/组件/页面/接口联调 | v1.7：Step 0.2 补 BE修复路由——发现❌后端字段问题时暂停前端并路由到 role-后端开发 修复（GAP-PD015-1）|
| role-后端开发 | v1.4 | 🔵 待验证 | 2026-03-20 | 后端/FastAPI/Python/API接口/数据库/PostgreSQL | 按四层架构实现，写完任何DB函数必须立即集成测试，Bug修复后强制 verifier 关卡C验证 |
| role-AI工程师 | v1.3 | 🔵 待验证 | 2026-03-22 | AI/LLM/智能体/Prompt/上下文工程/工作流/RAG | v1.3：知识导航表新增 D0 认知根确认行（L1 AI智能体任务分类体系与闭环完成标准）|
| role-测试工程师 | v1.11 | 🔵 待验证 | 2026-03-22 | 测试/验收/Bug报告/关卡C/功能验证/闭环测试/体验验收 | v1.11：知识导航表新增 D0 认知根确认行（L1 AI智能体任务分类体系五维度闭环完成标准）|
| role-DevOps | v1.3.1 | ✅ 已验证 | 2026-03-23 | 部署/上线/CI-CD/服务器/Docker/nginx/SSL/Tailscale | v1.3.1：知识导航表新增 D0 认知根行（先确认部署架构总览）|（无Homebrew安装/tailnet前置验证/Windows管理员公钥配置/SSH config别名/IP变化注意）|
| role-UI设计师 | v1.3 | 🔵 待验证 | 2026-03-22 | 设计/UI/UX/用户界面/交互设计/体验感/视觉/组件规范 | v1.3：知识导航表新增 D0 认知根确认行（L1产品理论维度体验相关章节）|
| role-数据分析师 | v1.3 | 🔵 待验证 | 2026-03-22 | 数据分析/指标/闭环完成率/用户行为/断裂节点/AI调用成本/产品健康度报告 | v1.3：知识导航表新增 D0 认知根确认行（L1产品理论维度/闭环指标设计章节）|
| role-审核者-用户模拟 | v1.4 | 🔵 待验证 | 2026-03-22 | 审核/产品审核/用户流/闭环验证/体验审核/关卡A/沙盘推演 | v1.4：D0认知根确认行+A-11认知根核查+闭环第7条（产品核心假设是否有L1产品理论支撑）|
| role-审核者-系统破坏 | v1.3 | 🔵 待验证 | 2026-03-22 | 架构审核/安全审查/系统破坏/压力测试/关卡B/技术审核 | v1.3：D0认知根+原则基础行+B-13 L1.5原则合规检查+L1.5原则合规性独立表格 |

---

## 认知结构类 Skill

| Skill 名称 | 版本 | 状态 | 最新日期 | 触发词（部分）| 备注 |
|---|---|---|---|---|---|
| cognitive-capture-fragment | v1.3.1 | 🔵 待验证 | 2026-03-21 | 碎片/记录一下/想法/新洞见/我发现/我觉得/随手记/想记一个 | v1.3：Step 5.8 新增 L2 积累阈值监控，≥8条待整合时主动提示触发整合（CS-014修复）|
| cognitive-ask | v1.4.1 | 🔵 待验证 | 2026-03-22 | 基于我的文档/我之前怎么想的/我对X的看法/从我的角度 | v1.4：致命矛盾强化触发——🔴 致命冲突使用「强烈建议立即运行」，与轻度张力差异化处理（GAP-CS016-1）|
| cognitive-daily-briefing | v1.1.1 | 🔵 待验证 | 2026-03-21 | 汇报/今天有什么/有什么更新/同步状态/有什么积压/今日简报/最近新了什么 | v1.1：Step 2.5 新增全量一致性检查日期监控，>7天未运行则在积压区提示（CS-015修复）|
| cognitive-detect-contradiction | v1.0 | 🔵 待验证 | 2026-03-10 | 矛盾/不一致/检查一致性/[文档A]和[文档B]是否一致/有没有冲突 | 检测L1文档之间或内部的矛盾，基于L1.5原则提出消解方案 |
| cognitive-extract-principle | v1.2.1 | 🔵 待验证 | 2026-03-21 | 提炼原则/有什么规律/这些碎片有没有共性/总结模式/有什么底层逻辑 | v1.2：新增 Step 4e——新原则确认后后台触发 cognitive-cascade-notifier（Loop2→Loop3级联，CS-011修复）|
| cognitive-integrate-fragments | v1.4.1 | 🔵 待验证 | 2026-03-21 | 整合碎片/哪些碎片没整合/更新文档/处理积压/消化碎片 | v1.4：新增 Step 0.5——碎片≥5条时调用 cognitive-fragment-integrator（CS-012修复）|
| cognitive-review-brain-map | v1.0 | 🔵 待验证 | 2026-03-10 | 大脑地图/认知状态/今天做什么/复盘/系统状态/看一下状态 | 生成认知结构当前状态快照，帮助了解知识体系全貌 |
| cognitive-self-reflect | v1.1 | 🔵 待验证 | 2026-03-20 | 反思/我发现我有个习惯/我注意到/我又犯了/这个模式/我有个问题/感觉自己 | v1.1新增五维度强制覆盖+最低追问10轮门槛+Step4.5检查点 |
| cognitive-update-knowledge | v1.2.1 | 🔵 待验证 | 2026-03-21 | 更新[文档名]/完善[文档名]/修改[文档名]/在[文档]里加上 | v1.2：新增 Step 8（cognitive-verifier自洽验证）+ Step 9（重大更新级联通知）+ B4时机修订（CS-010修复）|
| cognitive-version-snapshot | v1.0 | 🔵 待验证 | 2026-03-19 | 创建新版本/打一个快照/这是v2.0了/记录一下这个版本 | 为L1文档创建x.0版本快照，标志重大变更里程碑 |
| cognitive-consistency-check | v1.0.1 | 🔵 待验证 | 2026-03-19 | 一致性检查/自洽检查/验证认知结构/跑一遍验证 | C1-C10全套一致性验证，输出验证报告并修复不一致 |
| cognitive-reorganize | v1.2 | 🔵 待验证 | 2026-03-21 | 系统整理/重组认知结构/全量梳理/认知结构乱了/全工作区整理/文档归属梳理/如何加入认知结构/按规范加入/未更新的文档怎么处理/这些文档要怎么整理 | v1.2：Step 0.5 新增 Step d——单文件询问时执行四轴快速分类，输出目标路径推荐（CS-009 Gap修复） |

---

## 科研数字分身类 Skill

| Skill 名称 | 版本 | 状态 | 最新日期 | 触发词（部分）| 备注 |
|---|---|---|---|---|---|
| collect-basic-info | v1.0 | 🔵 待验证 | 2026-03-10 | 基础信息/建立画像/研究阶段 | 采集科研数字分身基础信息（研究阶段/学科/方法/技术能力）|
| administer-ams | v1.0 | 🔵 待验证 | 2026-03-10 | AMS/学术动机量表/动机测试 | 施测 AMS-GSR 28 题 |
| administer-mini-ipip | v1.0 | 🔵 待验证 | 2026-03-10 | 人格/大五人格测试/Mini-IPIP | 施测大五人格量表 20 题 |
| administer-rcss | v1.0 | 🔵 待验证 | 2026-03-10 | RCSS/认知风格量表/认知偏好 | 施测科研人员认知风格量表 |
| infer-profile-dimensions | v1.0 | 🔵 待验证 | 2026-03-10 | 推断画像/快速估算/不想填量表 | AI 基于已有信息推断动机/人格/认知风格 |
| import-ai-memory | v1.0 | 🔵 待验证 | 2026-03-10 | 导入记忆/ChatGPT记忆/AI记忆 | 解析 AI 记忆回复，整合到已有画像 |
| generate-ai-memory-prompt | v1.0 | 🔵 待验证 | 2026-03-10 | 生成提示词/给AI的记忆提示/提示词 | 生成结构化提示词，供提交给带记忆功能 AI |
| update-profile | v1.0 | 🔵 待验证 | 2026-03-10 | 修改画像/更新画像/补充 | 对已有画像进行精确字段补充或修改 |
| review-profile | v1.0 | 🔵 待验证 | 2026-03-10 | 查看画像/确认画像/审核 | 展示完整画像供用户审核，收集反馈 |
| modify-profile-schema | v1.0 | 🔵 待验证 | 2026-03-10 | 修改维度/新增字段/删除维度/修改字段定义 | 对画像系统维度结构进行增加、删除或修改 |
| generate-forum-profile | v1.0 | 🔵 待验证 | 2026-03-10 | 生成论坛分身/论坛画像/数字分身/导出论坛档案 | 将科研数字分身整合为他山论坛分身（4节 Markdown）|

---

## 画像类 Skill（Skill/Rule 不适用）

| Skill 名称 | 版本 | 状态 | 最新日期 | 触发词（部分）| 备注 |
|---|---|---|---|---|---|
| skill-rule-修改规范 | v1.7.1 | 🔵 待验证 | 2026-03-23 | 修改Skill/修改Rule/修改Agent/规范修改流程 | v1.7.1：新增知识导航表（D0→Skill体系设计原则 + D3→系统对象全量分类表 + D4→目标文件 + 核心概念速查）|
| skill-designer | v1.4 | 🔵 待验证 | 2026-03-22 | 新建Skill/设计一个Skill/新建Agent/设计规则/修改Rule | v1.4：知识导航表（D0行）+经验感知钩子章节+Step8经验沉淀触发（G-01/G-02/G-03，SK-015元验证修复）|
| project-backlog | v1.0 | 🔵 待验证 | 2026-03-24 | 有几个问题先记到待办/加到项目待办/处理项目待办/按待办文档逐条修复 | v1.0：新建。两种模式：收集（混合输入→项目待办.md）+ 处理（读文档→决策收集→逐条路由执行→批次报告）。触发词必须含「待办」关键词 |
| engineering-principle-recorder | v1.0 | 🔵 待验证 | 2026-03-24 | 立一个原则/记下这个原则/这是条工程原则/以后所有X都要Y/把这条原则记在文档里 | v1.0：新建。工程/执行原则录入（4类：认知/AI行为/工程设计/代码违规），写入执行层+违规审计+覆盖报告。与 cognitive-extract-principle 互补（前者认知原则，本Skill执行约束）|
| skill-capture-closure | v2.0 | 🔵 待验证 | 2026-03-23 | 复盘一下/做个复盘/这次踩坑了/这个经验值得记/跑通了/总结经验/沉淀一下/记录一下这次 | v2.0：重构主分类轴（现象分类→B/K对象类型），同时覆盖修改（B/K.modify）和沉淀（B/K.create），新增完整 K-object ceremony 路径组 |
| project-retrospective | v1.3.1 | 🔵 待验证 | 2026-03-23 | 项目做完了/更新一下Skill/基于刚刚的过程更新规范/做个项目复盘 | v1.3.1：新增知识导航表（D0→自进化形式规范 + D3→Skill体系设计原则 + D4→运行时数据 + 核心概念速查）|
| issue-tracker | v1.1.1 | 🔵 待验证 | 2026-03-22 | 有个问题/发现了bug/这里不对/用不了/有个bug | v1.1：Step 4 补技术-产品冲突后 GATE-A 重触发提醒（GAP-PD014-1）|
| write-task-log | v1.4 | 🔵 待验证 | 2026-03-22 | 写日志/更新日志/任务记录/日志 | v1.4：序号生成改为 grep全文取最大序号+1，防多 session 并发冲突（GAP-CO009-1）|
| **ai-image-generator** | **v1.1** | **🔵 待验证** | **2026-03-20** | **需要绘图/生成配图/画一张图/信息图** | **能力层Skill：qwen-image-2.0-pro/wan2.6-t2i API+多视角草图+风格库+配图索引联动** |
| skill-simulator | v1.0 | ✅ 已验证 | 2026-03-21 | 关卡A执行/AI执行者模拟/Skill设计审核/以第一次看到Skill的AI执行者视角找歧义 | 以「刚拿到这个Skill的AI执行者」身份审查：歧义步骤/触发词混淆/隐含假设/边界条件缺失；Phase 2 Gate A 首次真实执行通过（发现5 Critical+6 Important问题） |
| skill-system-destroyer | v1.0 | ✅ 已验证 | 2026-03-21 | Skill体系L4改造/想让Skill体系失效/破坏审查/关卡B等价 | 关卡B等价审核器：以破坏者视角找出新组件与现有系统的冲突（触发词歧义/优先级缺失/Rule叠加矛盾）|

---

## Skill 分层架构（新增，2026-03-20）

> 每个 Skill 必须属于以下三层之一。分层决定了 Skill 的设计原则。

| 层级 | 定义 | 判断标准 | 包含内容 |
|---|---|---|---|
| **能力层** | 可被2个及以上不同流程/角色 Skill 调用的执行操作 | 包含 API 调用、外部工具调用、可复用操作 | ai-image-generator、write-task-log |
| **流程层** | 描述完整任务的执行步骤，引用能力层 | 定义"做什么"，不嵌入"怎么调 API" | wechat-article-writer、document-pipeline、research-output |
| **角色层** | 描述人机协作角色的行为准则 | 定义"谁来做"，引用流程层和能力层 | role-产品经理、role-后端开发 等所有 role-* |

**设计原则（强制）**：
- ⛔ 流程层/角色层 Skill 不得硬编码 API Key、模型名、Endpoint URL
- ⛔ 新建 Skill 前必须先检查：所需能力是否已有能力层 Skill
- ✅ 能力变更时（如模型升级），只改能力层 Skill，流程层/角色层自动受益

**配置真源**：
- API Key / 模型名 / Endpoint → `_内部总控/凭证/` 目录
- 图片风格 → `_内部总控/产品定义/图片风格库.md`
| trigger-linkage-rules | v1.0 | 🔵 待验证 | 2026-03-10 | 跨项目联动/联动通知/触发联动/联动规则 | 指导 AI 正确执行跨项目联动通知 |
| modify-theory-system | v1.0 | 🔵 待验证 | 2026-03-10 | 修改公理/修改体系结构/发现规则漏洞 | 指导 AI 正确修改公理体系或体系结构（A-C-B三粒子）|

---

## 通用协作 Skill（代码库/架构/文档/Skill体系/协作工具）

| Skill 名称 | 版本 | 状态 | 最新日期 | 触发词（部分）| 备注 |
|---|---|---|---|---|---|
| codebase-explorer | v1.0.1 | 🔵 待验证 | 2026-03-19 | 阅读XXX项目/理解这个代码库/接手这个项目/帮我读一下这个代码 | 扫描目录→模块→状态流，输出可信赖架构理解文档，与产品定义对比 |
| history-auditor | v1.1 | 🔵 待验证 | 2026-03-22 | 审查历史对话/回顾过去的工作/分析我们做过什么/有什么可以沉淀成Skill的 | v1.1：新增 Step 5.5——发现重复踩坑（≥2次）立即提示触发 skill-capture-closure（GAP-CO010-1）|
| architecture-gap-mapper | v1.0 | 🔵 待验证 | 2026-03-19 | 对比XXX和YYY/找出差距/找现有系统差距/竞品分析 | 并行读两个系统，输出兼容/冲突/缺失三类带证据链差距报告 |
| doc-consolidator | v1.0 | 🔵 待验证 | 2026-03-19 | 文档太乱/有好几个版本/整合文档/文档漂移/合并文档 | 识别主真源，提取补充，重建结构，制定废弃文档处理计划 |
| remediation-planner | v1.0 | 🔵 待验证 | 2026-03-19 | 基于分析制定整改计划/怎么修复这些问题/制定改进方案 | 将差距报告转化为有优先级、验证配对的可执行整改计划，branch结构建议 |
| project-closeout | v1.2.1 | 🔵 待验证 | 2026-03-21 | 做收尾检查/确保文档自洽/项目收尾/项目关闭 | 三角色审查（PM/Arch/Dev）+ 对话历史用户输入追踪，输出收尾报告；v1.2 文档扫描清单新增2项（开发计划完整性+高依赖度文档F-022检查）|
| cross-project-coordinator | v1.0 | 🔵 待验证 | 2026-03-21 | 多项目并行/建协调框架/几个项目同时做/分工要明确/并行开发/各自独立启动/RULE-37 | RULE-37执行层：收集项目清单→生成项目地图+API契约+并行轨道+Day1清单→F-022反思；Level 2 Skill |
| product-evolution-planner | v1.0.1 | 🔵 待验证 | 2026-03-19 | 基于产品原则看改进/产品还缺什么/迭代建议/从第一性原理看产品 | 对照AI时代产品框架五大原则主动诊断产品，生成战略级演进建议 |
| product-launch-validator | v1.0 | 🔵 待验证 | 2026-03-21 | 新项目立项/启动新产品/新产品兼容性检查/立项前检查/这个产品和我们体系兼容吗/三大闭环兼容性 | 立项时检查新产品与 Loop 1/2/3 的兼容性（Skill覆盖/认知根/工作域注册），输出兼容性报告（PD1修复）|
| three-loop-health-check | v2.0.1 | 🔵 待验证 | 2026-03-22 | 三大闭环健康检查/全系统健康报告/整体系统健康/三个闭环都健康吗/三大闭环状态怎么样 | v2.0完整重建：三层仪表盘（运营指标+沙盘状态+D0覆盖率），快速只读，无Full模式；关卡A/B/C通过，Glob绝对路径+SKILL-INDEX主表limit:60防双重计数 |
| project-convention-resolver | v1.1 | 🔵 待验证 | 2026-03-22 | 这里有个规范问题/这不符合规范/规范偏差/按规范修复 | v1.1：Step 5 E类修复后，若来源为 skill-system-health-check，建议重新运行健康检查验证消解（GAP-SK017-2）|
| skill-system-health-check | v1.2.1 | 🔵 待验证 | 2026-03-22 | 检查Skill体系/Skill体系自检/Skill健康检查/Skill体系自洽性 | v1.2：P0路由改为 project-convention-resolver（统一记录+路由+验证），而非直接触发 skill-rule-修改规范（GAP-SK017-1）|
| skill-evolution-planner-meta | v1.0.1 | 🔵 待验证 | 2026-03-19 | Skill体系怎么演进/有没有新Skill要建/Skill体系演进建议 | 基于CO-BUILD-LOG/PENDING-EXPERIENCES/PENDING-SKILLS规划Skill体系演进 |
| cognitive-input-classifier | v1.0.1 | 🔵 待验证 | 2026-03-22 | 帮我判断这是认知更新还是任务执行/这个输入是什么类型/先分类再执行/路由分类一下 | 输入路由分类器：基于信号词判断路径A（认知更新）or路径B（任务执行），强制停止等用户确认，不自动触发下游；新增「先按规范记录」触发词+CO-BUILD-LOG消歧；关卡A/C通过 |
| cognitive-work-alignment-check | v1.0 | 🔵 待验证 | 2026-03-19 | 检查工作任务与认知的对齐/第四维健康检查/认知根对齐/认知体系和工作任务是否自洽 | 四维健康检查第四维：读DOMAIN-REGISTRY+L0+L1.5，对5域做命题级追溯，输出对齐报告+漂浮任务+建议；关卡A/B/C通过 |
| role-Skill产品经理 | v1.0 | 🔵 待验证 | 2026-03-19 | 我有个Skill想法但没想清楚/帮我做Skill产品定义/作为Skill PM分析/帮我把Skill想清楚 | 纯产品定义层：双视角引导（节内切换+翻译笔记）→产出draft-*.md；三关卡通过 |
| skill-sandbox-expander | v1.0 | 🔵 待验证 | 2026-03-19 | 扩充沙盘/增加沙盘/写更多沙盘/沙盘库不够/填充覆盖缺口/补全draft沙盘/把草稿补完 | 识别域覆盖缺口→建议优先场景→严格两阶段生成（Phase1禁读SKILL.md→Phase2对照验证）→gap-summary持久化；三关卡全部通过 |
| skill-domain-health-check | v1.0 | 🔵 待验证 | 2026-03-19 | 检查[域名]域健康/[域名]域传播完备性检查/域健康报告/[域名]闭环是否完整 | 按域检查传播完备性：节点可达/I-O契约满足/任意入口→闭环终态（由 skill-closure-verifier-meta 调用） |
| skill-domain-self-optimizer | v1.0 | 🔵 待验证 | 2026-03-19 | 优化[域名]域/修复[域名]域Gap/[域名]域自优化/根据健康报告生成修复方案 | 基于域健康报告和沙盘Gap生成具体行动方案：新Skill提案/现有Skill修改/缺失触发链路补全 |
| skill-closure-verifier-meta | v1.0 | 🔵 待验证 | 2026-03-19 | 运行元验证/闭环验证/验证Skill体系传播完备性/系统闭环检查/全域验证/元系统运行 | 元级闭环验证编排器：两阶段（Phase 1预想/Phase 2实际）沙盘验证+调用域健康检查+自优化，输出带证据的总报告 |
| skill-system-evolution-executor | v1.0 | 🔵 待验证 | 2026-03-21 | 执行Skill体系完善/Skill体系L4改造/系统型Skill重构/按完善计划执行/开始Skill体系完善项目 | L4系统型完善项目编排器：Phase0规模确认→Phase1分析计划→Phase2双审核(关卡A+B)→Phase3分批执行→Phase4整体验证→Phase5沉淀（implements §9.7）|

---

## 写作与内容类 Skill

| Skill 名称 | 版本 | 状态 | 最新日期 | 触发词（部分）| 备注 |
|---|---|---|---|---|---|
| document-pipeline | v1.5.1 | 🔵 待验证 | 2026-03-20 | 统一写作流水线（任意Stage入场/研究→草稿→逻辑自检→真实性校对→画图→审稿→格式转换）| 写一篇/帮我写/写一份/我有初稿了/帮我检查逻辑/帮我配图/转成HTML/转成LaTeX |
| article-proofreading | v1.0.1 | 🔵 待验证 | 2026-03-19 | 审稿/帮我检查这篇文章/review一下 | 按郑总审稿标准审阅中文文章：AI腔/标题规范/绝对表达/结构层次/结语完整性 |
| article-review-tracker | v1.0 | 🔵 待验证 | 2026-03-19 | 追踪文章审稿意见 | 审稿意见/修改文章/审稿反馈/这里写得不好/帮我追踪这个意见 |
| expert-bootstrap | v1.0 | 🔵 待验证 | 2026-03-24 | 需要X领域的专家/培养专家/没有X方面的专家/expert-bootstrap/专家培养/专家视角 | 按需培养领域专家 Agent：调研→对标→自问自答反思→产出专家 Agent 定义文件（B-object）。与 research-output 区别：后者产出知识报告（K-object）供CEO决策；本 Skill 让 Agent 成为该领域专家（可 dispatch 专业审查）|
| research-output | v2.2.1 | 🔵 待验证 | 2026-03-22 | 帮我调研/调研一下/研究一下/完善[已有文档]/加图/按规范完善 | v2.2：Phase 9 补 L1矛盾检测提示——D0 找到相关L1文档时，调研完成后主动询问是否运行矛盾检测（GAP-CN009-1）|
| article-image-angles | v1.0 | 🔵 待验证 | 2026-03-19 | 文章配图多视角分析 | 配图角度/多视角草图/配图有几种选择/给我几个配图方案 |
| article-image-styles | v1.0 | 🔵 待验证 | 2026-03-19 | 配图风格库管理 | 调用风格库/用XX风格/存入风格库/更新风格模板/风格库有哪些风格 |
| general-article-writer | v1.0.1 | 🔵 待验证 | 2026-03-10 | 写技术文章/写对外分享/通用长文/产品思考 | 撰写通用长文（技术分析/产品思考/对外分享/个人随笔），Markdown输出 |
| wechat-article-writer | v1.5.1 | 🔵 待验证 | 2026-03-22 | 写公众号文章/帮我写他山文章/写公众号推文 | v1.5：Step 6.5 前补三层发布前质检架构说明（Layer1内容/Layer2 HTML/Layer3品牌）（GAP-CN008-1）|

---

## Skill 体系统计

> 最后更新：2026-03-22

| 指标 | 数量 |
|---|---|
| 总 Skill 数 | 51 |
| ✅ 已验证 | 13 |
| 🔵 待验证 | 35 |
| ⚠️ 部分验证 | 0 |
| ❌ 已废弃 | 0 |

---

## 变更历史

### 2026-03-19 — 初始建立

- 初始建立 SKILL-INDEX.md，记录所有 Skill 的版本状态与触发词
- 扫描 `.cursor/skills/` 目录，确认所有 Skill 文件存在并登记
- 通过 skill-capture-closure Skill 自动维护本索引的更新流程

### 2026-03-19 — skill-rule-修改规范 v1.0 → v1.1

- 修订 skill-rule-修改规范，强化三问协议、版本留痕要求

### 2026-03-19 — 项目复盘体系完善

- 更新 project-retrospective v1.0，补完批量 Skill 沉淀的完整流程
- 更新 skill-capture-closure v1.0 → v1.1，补完标准化沉淀步骤，Step 7 加入索引同步
- 更新 role-menu.mdc，完善 project-retrospective 的触发说明

### 2026-03-19 — 经验自动感知机制建立

- 更新 auto-experience-hook.mdc Rule，alwaysApply 强制收尾步骤
- 新建 PENDING-EXPERIENCES.md 暂存文件
- 更新 project-retrospective v1.0 → v1.1，Step 2 加入积压感知+主动推送，Step 5 加入碎片捕捉
- 回溯 11 个已有 Skill v1.x → v1.x+1，补充遗漏变更记录

### 2026-03-19 — 子智能体群组初始建立

- 新建 .cursor/agents/experience-logger.md，后台日志记录器（fast 模型，is_background）
- 新建 .cursor/agents/skill-updater.md，单条 Skill 经验沉淀，独立 context 处理
- 新建 .cursor/agents/verifier.md，独立验证子智能体（关卡C 专用）
- 新建 .cursor/agents/arch-destroyer.md，架构破坏审核子智能体（关卡B 专用）
- 新建 SYSTEM-BLUEPRINT.md，记录 92 个节点的完整 Skill/Agent/Rule/Context 体系蓝图

### 2026-03-19 — Skill 设计体系完善（双视角产品定义）

- 新建 PENDING-SKILLS.md，Skill 需求积压库，5个候选 Skill
- 新建 skill-product-definition-template.md（skill-designer/ 目录），双视角产品定义模板+Agent规格
- 新建 skill-simulator，执行者模拟（关卡A），以AI执行者视角找歧义/触发词混淆/边界
- 新建 skill-system-destroyer，系统破坏（关卡B），Skill体系冲突/优先级缺失/Rule叠加
- 新建 skill-designer v1.0，双视角引导，复杂度级别 L1-L4，L2+ 触发 A/B/C 关卡
- 更新 skill-rule-修改规范 v1.2 → v1.3，Step 0 加入触发词前置检查，L2+ 需用 skill-designer
- 更新 project-retrospective v1.1 → v1.2，Step 4 集成 skill-updater 调用
- 更新 auto-experience-hook.mdc，停用 experience-logger 子智能体

### 2026-03-19 — 审核子智能体补全（P0+P1+P2）

**P0 用户模拟+产品审核**：
- 新建 user-simulator，用户模拟审核（关卡A），以挑剔用户视角走完核心路径，产出 PM 决策清单
- 更新 role-审核者-用户模拟 v1.1 → v1.2，集成 user-simulator
- 更新 role-审核者-系统破坏 v1.1 → v1.2，集成 arch-destroyer
- 更新 role-技术架构师 v1.2 → v1.3，集成 verifier

**P1 体验层+独立context**：
- 新建 ux-reviewer，以陌生用户第一次接触视角审查 UI/UX 设计
- 更新 role-UI设计师 v1.1 → v1.2，集成 ux-reviewer
- 更新 role-数据分析师 v1.1 → v1.2，加入独立 explore 分析模式
- 更新 cognitive-integrate-fragments v1.0 → v1.1，以 explore 独立分析+L1 对比

**P2 AI效果评测**：
- 新建 ai-evaluator，以独立视角评测 LLM 调用链效果

### 2026-03-19 — Co-build Log 过程日志体系建立

- 新建 co-build-log.mdc Rule，alwaysApply，定义5类过程节点（启动/方案/转折/发现/完成）的记录规范
- 新建 co-build-logger.md 子智能体，fast 模型，后台模式，写入 CO-BUILD-LOG.md 过程条目
- 新建 CO-BUILD-LOG.md，协作建设过程日志，记录本次对话 Skill 演进决策链
- 更新 project-retrospective v1.2 → v1.3，Step 2 加入 CO-BUILD-LOG 积压处理

### 2026-03-19 — openclaw-proxy 部署踩坑

- 更新 role-DevOps v1.1 → v1.1.1，新增 OPS-08：Docker 容器内 host.docker.internal 解析失败导致 WS 连接失败的根因与修复

### 2026-03-19 — feed-archiver 爬虫修复

- 修复爬虫 3 个关键配置错误
- 更新 ai-media-crawler v1.0 → v1.1，补全微信公众号抓取规范（Cookie采集 + archiver.py 参数格式 + 限速处理）
- 新建 wechat-scraper.md 子智能体，独立上下文处理抓取+重试，主Agent只收最终结果

### 2026-03-19 — openclaw-proxy 后端 WS 问题修复

- 更新 role-后端开发 v1.1 → v1.1.1，新增 BE-08：处理 WS 连接在反向代理后需特殊升级头，多个错误模式与排查清单

### 2026-03-19 — openclaw-proxy 前端问题修复

- 更新 role-前端开发 v1.1 → v1.1.1，新增 FE-11：严格模式下不能将 string 类型 ref 用于函数组件，必须使用 useRef 并传回调函数

### 2026-03-19 — openclaw-proxy AI 接口层完整实现

- 更新 role-前端开发 v1.1.1 → v1.1.2，补全 AI Agent 调用前端规范：认证头格式 + API Key 注入 + 调试 WS + 错误处理 + 120s 超时 + 跨域 session，涵盖 curl/Python/ChatGPT/n8n 场景

### 2026-03-19 — 任务调度型 AI 接口完整实现（DevOps + 前端）

- 更新 role-DevOps v1.1.1 → v1.1.2，补全任务调度型 AI 接口的 SSH/Paramiko 远程执行规范与错误处理
- 更新 role-前端开发 v1.1.2 → v1.1.3，补全 ask_server 函数命名 + 错误处理 + 状态管理

### 2026-03-19 — 技术架构师中台接口规范 + AI 工程师角色建立

- 更新 role-技术架构师 v1.1 → v1.2，补全中台型 AI 接口架构规范（认证/安全/接口合约/知识路由/协作层规范）
- 更新 role-AI工程师 v1.1 → v1.1.1，补全中台型 AI 接口的 LLM 调用层规范，`ask_server_ai()` 函数标准 + 合规 Prompt 设计规范

### 2026-03-19 — Docker 多项目网络共享（DevOps）

- 更新 role-DevOps v1.1.2 → v1.2.1，补全多项目 Docker 跨容器通信规范：tashan-shared external 网络、container_name 强制规范、deploy.yml 幂等网络创建、nginx upstream DNS 延迟解析

### 2026-03-19 — role-技术架构师 初版完善

- 初版 role-技术架构师 完善，补全关卡C执行标准，加入完整架构约定+三层接口规范+4步并行开发

### 2026-03-19 — 新建 wechat-article-writer Skill（写作发布流水线）

- 新建 `.cursor/skills/wechat-article-writer/SKILL.md`，Level 2 发布流水线
- 包含8步骤（内容选题 → 写作 → 图片 → HTML → 底部模板 → 双重核查 → 审稿 → 发布）
- 包含14条踩坑速查，覆盖4类常见排版问题
- 与 `article-proofreading` 自动联动

### 2026-03-19 — project-retrospective 关键更新

- 初版 project-retrospective 关键更新：加入复盘模板 + skill-updater 自动分发 + 批量沉淀支持

---

## 子智能体（.cursor/agents/ 目录）

> 独立于 Skill 体系运行，Skill 调用 Agent 时以子进程方式注入独立 context，与主流程隔离，适合独立视角审核或并行执行的任务。

| 子智能体名 | 前后台 | 模型 | 调用方 | 功能描述 |
|---|---|---|---|---|
| ~~experience-logger.md~~ | ~~后台is_background~~ | ~~fast~~ | ~~auto-experience-hook Rule~~ | **已弃用归档（2026-03-20）**：auto-experience-hook v2.0 改回直接写文件，不再调用此 Agent；活跃文件已移至 history/experience-logger_archived_20260320.md |
| skill-updater.md | 前台（返回结果）| inherit | project-retrospective Step 4 | 单次 Skill 经验沉淀/更新 Skill 文件+备份+变更记录+更新索引，每次只处理一条经验 |
| verifier.md | 前台只读 | inherit | role-测试工程师（关卡C）| 独立验证子智能体（关卡C）：以测试工程师视角独立验证实现是否真正完成，与开发上下文完全隔离 |
| arch-destroyer.md | 前台只读 | inherit | role-审核者-系统破坏（关卡B）| 架构破坏审核：以黑客/极端用量视角找出安全漏洞/性能瓶颈/可演化性问题 |
| wechat-scraper.md | 后台 | inherit | wechat-article-writer（用户确认）+ Cookie获取 | 微信公众号文章批量抓取，独立 context 处理所有失败重试，主Agent只收最终结果（文件路径列表）|
| user-simulator.md | 前台只读 | inherit | role-审核者-用户模拟（关卡A）| 以挑剔用户视角走完所有核心路径，找出设计漏洞，与产品经理上下文完全隔离，产出 PM 决策清单 |
| ux-reviewer.md | 前台只读 | inherit | role-UI设计师（审稿阶段）| 以陌生用户第一次接触视角审查设计方案：视觉层级/词语歧义/跨设备适配/可访问性 |
| ai-evaluator.md | 前台只读 | inherit | role-AI工程师（效果评测）| 以独立视角评测 LLM 调用链/Prompt 设计/智能体输出质量：幻觉率/边界输入/一致性/成本效率 |
| co-build-logger.md | 后台（is_background=true）| fast | co-build-log Rule | 协作建设过程日志记录器，捕捉关键决策点写入 CO-BUILD-LOG.md，后台模式不阻断主任务 |
| skill-simulator.md | 前台只读 | inherit | skill-designer（关卡A）| 以「刚拿到这个Skill的AI执行者」身份走一遍，找出歧义步骤/触发词混淆/隐含假设/边界条件缺失 |
| skill-system-destroyer.md | 前台只读 | inherit | skill-designer（关卡B）| 以破坏者视角找出新Skill与现有系统冲突：触发词歧义/优先级缺失/Rule叠加矛盾/死锁依赖 |
| role-pm-auditor.md | 前台只读 | inherit | project-closeout Step 3 | 以PM读者视角审查产品定义完整性和用户决策覆盖情况 |
| role-arch-auditor.md | 前台只读 | inherit | project-closeout Step 3 | 以架构师读者视角审查技术架构与产品定义的对齐情况 |
| role-dev-auditor.md | 前台只读 | inherit | project-closeout Step 3 | 以开发者读者视角审查开发计划与实际完成情况的对齐 |
| **cognitive-verifier.md** | **前台只读** | **inherit** | **cognitive-update-knowledge Step 8 / cognitive-integrate-fragments Step 7** | **认知自洽验证器：独立 context 验证 L1 文档更新（CV-1 L0一致性/CV-2 L1.5原则/CV-3 邻域矛盾），输出通过/警告/不通过报告（CS-010修复）** |
| **cognitive-cascade-notifier.md** | **后台 is_background** | **fast** | **cognitive-extract-principle Step 4e / cognitive-update-knowledge Step 9** | **认知级联通知器：新原则确认或L1重大更新后，后台分析五域影响，写入待完成总清单（CS-011修复，Loop2→Loop3级联）** |
| **cognitive-fragment-integrator.md** | **前台（返回方案）** | **inherit** | **cognitive-integrate-fragments Step 0.5（碎片≥5条时）** | **碎片批量整合器：独立context以「L1内部居民」3规则分析，输出含 section_name+anchor_keyword 的精确整合方案（CS-012修复）** |
| **cognitive-task-reflector.md** | **前台（非只读）** | **inherit** | **write-task-log 步骤五（认知类任务后自动触发）** | **任务认知萃取器：独立context从高抽象层次萃取认知价值，L1.5候选正确路由到extract-principle（CS-013修复，Loop3→Loop2）** |

### 2026-03-19 — 新建 closure-orchestration-package 子智能体群组

- 新建 skill-designer/agent-io-contract.md：定义子智能体输入输出格式规范/统一任务信封
- 更新 verifier.md：补充 gate_recommendation + suggested_next_branches（repair branch 语义）
- 新建 skill-updater.md：单条经验处理/备份/写入
- 更新 project-retrospective v1.3 → v1.4：集成 ClosureCase 输入格式，支持自动分发给 skill-updater（repair branch 语义）
- 新建 codebase-explorer v1.0：P0 场景（接手代码库）专用架构分析工具
- 新建 history-auditor v1.0：历史对话审计，提炼工作规律到 Skill 体系
- 新建 architecture-gap-mapper v1.0：P1 系统差距分析/兼容冲突缺失三类带证据链
- 新建 doc-consolidator v1.0：多版本文档漂移恢复单一真源
- 新建 remediation-planner v1.0：将分析发现转化为优先级/branch结构整改计划

---

### 2026-03-19 — 写作+发布体系完整建立（本次对话沉淀）

**新建 Skills**：
- `article-proofreading` v1.0（Level 2 补完规范：backup到history/ + 变更记录）：五轮审稿体系，9个反面案例
- `wechat-article-writer` v1.0（Level 2 新建）：8步写作发布流程，联动 article-proofreading

**新建/更新文档**：
- `AI思维碎片/微信公众号发布手册.md`：HTML规范+图片生成+底部模板+历史排版规范（基于14篇文章）
- `AI思维碎片/写作习惯与风格手册.md`：新增 §5 ASCII图规范（4种类型）、§6 写作底层模型、§7 反面案例（问题6-9）、§8 公众号额外要求
- `产品定义/他山公众号运营技术全景规划.md`（新建）：当前可做+认证后可做+服务号扩展+路线图
- `feed-archiver/产品经理/微信抓取方案总结.md`（新建）：5种方案可行性对比

**AGENT_RULES 更新**：
- 新增 Rule-32（或类似）：AI能做的事必须自己做，不能甩给用户

**个人Skill更新**：
- `ai-media-crawler`（个人）：v1.1 → v1.2，更新微信抓取方案（wxsid无法获取的根本原因 + links.txt最优方案 + 命令格式纠正）

**凭据新增**：
- `credentials/tashan-wechat-mp.md`：他山公众号 AppID/AppSecret/biz

### 2026-03-19 — project-closeout Level 3 新建（三关卡全部通过）

- 新建 project-closeout v1.0（Skill）：三角色审查 + 对话历史用户输入追踪，输出收尾报告
- 新建 role-pm-auditor.md（Agent只读）：PM视角审查产品定义完整性和用户决策覆盖
- 新建 role-arch-auditor.md（Agent只读）：架构师视角审查技术架构与产品定义对齐
- 新建 role-dev-auditor.md（Agent只读）：开发者视角审查开发计划与实际完成情况
- 关卡A通过：修复了对话历史路径歧义、用户输入分类标准、子智能体失败处理
- 关卡B通过：修复了与 project-retrospective 的触发词冲突，description 已明确区分

### 2026-03-19 — Bug 修复后强制验证闭环（开发 Skill 补丁）

- 更新 role-后端开发 v1.1.2→v1.1.3：新增「Bug修复后强制验证闭环」章节，修复后自动调用 verifier，pass则更新追踪台，fail则最多3轮修复循环
- 更新 role-前端开发 v1.1.1→v1.1.2：同上，补充前端特有说明（体验类仍需人工确认）

### 2026-03-19 — product-evolution-planner v1.0 新建（Level 3，三关卡通过）

- 新建 product-evolution-planner v1.0：主动式产品演进规划，对照AI时代产品框架五大原则（马斯洛新瓶颈/AI放大/双层设计/闭环完整/研发壁垒），生成有原则依据的战略改进建议
- 关卡A修复：框架文档读取范围明确（指定必读章节），路由时传入完整建议内容
- 关卡B通过：触发词与role-产品经理、architecture-gap-mapper已明确区分

### 2026-03-19 — Skill体系自驱体系建立（两个新Skill + role-menu外源输入路由）

- 新建 skill-system-health-check v1.0：六维自洽性检查（触发词冲突/孤立组件/版本漂移/Rule叠加矛盾/Agent契约/PENDING状态）
- 新建 skill-evolution-planner-meta v1.0：基于CO-BUILD-LOG/PENDING-EXPERIENCES/PENDING-SKILLS，主动规划Skill体系演进
- 更新 role-menu.mdc：加入Skill体系触发词路由 + 外源输入（用户报告Skill问题/新想法）的响应路由 + 自驱节奏推荐（强制规则第8条）

### 2026-03-19 — project-convention-resolver v1.0（Skill操控体系完善：规范问题自动修复）

- 新建 project-convention-resolver v1.0（Level 3）：项目规范问题「接收→分类→路由执行→验证→归档」一体化
- 五类路由：A产品→role-产品经理 / B架构→role-技术架构师 / C代码→role-后端/前端+verifier / D文档→doc-consolidator / E Skill→skill-rule-修改规范
- 与 issue-tracker 互补：后者记录，本 Skill 执行修复

### 2026-03-19 — auto-experience-hook v2.0：三处结构性修复（回归旧版可靠逻辑）

- 修复：暂存操作回归直接写文件（去掉 experience-logger 子智能体调用，AI单线程下后台异步不可靠）
- 修复：收尾触发条件从「角色类Skill完成后」改为「任何实质性任务完成后」（覆盖直接任务模式）
- 修复：信号检测从「中途监控」改为「任务结束时回顾」（执行时专注，结束后回顾，认知不竞争）

### 2026-03-19 — auto-experience-hook v2.3→v2.4：信号B 增加 REF-EXT 错误位置检测

- 修复：信号B 判断标准新增「特别触发」——发现 `_内部总控/知识库/` 有文件时视为信号B，提示正确位置
- 根因：另一对话重建了已废弃的旧知识库目录并放入3个文件，说明规范对其他对话不可见

---

**Cursor 子智能体**（供参考）：

| 类型 | 说明 |
|---|---|
| explore | 代码库探索专用 Agent，快速理解文件结构 |
| bash | 执行 shell 命令专用 Agent，适合批量操作 |
| browser | 浏览器自动化专用 Agent，可操作 DOM |

### 2026-03-19 — 全域 Gap 修复（P0+P1+P2，基于沙盘验证）

**P0 修复（2项）**：
- role-前端开发 v1.1.2→v1.1.3：新增 Step 0 前置文档守门检查（无技术架构.md 时阻断，引导走正确流程）
- role-后端开发 v1.1.3→v1.1.4：同上
- role-menu v*→v*+1：加入强制规则第10条（开发角色前置文档守门，不允许绕过关卡）

**P1 链路修复（10项）**：
- role-DevOps v1.2.1→v1.2.2：加验证6（浏览器UI冒烟）+ Step 8 部署后收尾引导（DEVOPS→CLOSEOUT链路）
- project-closeout v1.0→v1.1：Step 6 引导触发 project-retrospective（CLOSEOUT→RETRO链路）
- cognitive-integrate-fragments v1.1→v1.1.1：Step 6 加入矛盾检测提示（INTEGRATE→DETECT链路）
- cognitive-update-knowledge v1.0→v1.0.1：Step 7 加入一致性检查提示（UPDATE→CONSIST链路）
- cognitive-extract-principle v1.0→v1.0.1：Step 5 明确触发 L1 文档同步更新（EXTRACT→L1链路）
- role-数据分析师 v1.0→v1.1：Step 5 加入跨域触发产品迭代（DATA→PM跨域链路）
- doc-consolidator v1.0→v1.1：Step 8 加入整合后一致性验证提示（DRIFT→CLOSEOUT链路）
- article-proofreading v1.0→v1.0.1：加入修改执行规范（P0问题AI直接修改，P1/P2输出建议）
- wechat-article-writer v1.0→v1.0.1：加入补全模式+触发词扩充
- wechat-article-writer v1.0.1→v1.1：五处实战踩坑修复（颜色规范/图片文件/Markdown真源/ASCII替换/排版核查）
- wechat-article-writer v1.1→v1.2：新增 Step 7.5 审稿意见追踪（原话保留+双栏格式+模板文件）
- ai-image-generator v1.0：新建能力层 Skill，从 wechat-article-writer 提取绘图能力（API+多视角+风格库+配图索引）；wechat-article-writer Step 4 改为引用此 Skill
- skill-designer v1.1→v1.2：Step 8 role-menu 更新改为强制步骤

**P2 修复（1项）**：
- skill-system-health-check v1.0→v1.1：P0 问题路由加强（警告+强制引导修复）

**沙盘库扩充**：35→50个（新增15个沙盘，覆盖修复验证+新Gap+跨域场景）

---

### 2026-03-19 — Skill 闭环验证元系统建立

**新建形式化文档（地基层）**：
- 新建 `_内部总控/skill-system-design/DOMAIN-REGISTRY.md`：五域节点图（产品开发/认知结构/公司运营/内容宣传/Skill体系），含mermaid触发链路图+终态定义
- 新建 `_内部总控/skill-system-design/NODE-IO-CONTRACTS.md`：40个节点的I/O契约卡片（含3个新建节点）
- 新建 `_内部总控/skill-system-design/SANDBOX-FORMAT.md`：沙盘格式规范
- 新建沙盘库（35个初始沙盘：5域×5基础+10个元验证专项）：`sandboxes/` 目录

**新建 Skill（3个）**：
- 新建 skill-domain-health-check v1.0：按域传播完备性检查（与 skill-system-health-check 互补）
- 新建 skill-domain-self-optimizer v1.0：基于Gap证据生成定向修复方案
- 新建 skill-closure-verifier-meta v1.0：元级闭环验证编排器（Level 4，两阶段验证）

**更新 skill-system-health-check 描述**：明确「内部一致性」定位，与新建的 skill-closure-verifier-meta「传播完备性」定位形成互补分工

---

### 2026-03-19 — tashan-openbrain 部署复盘

- 更新 role-DevOps v1.2.1 → v1.2.2：RULE-32 新增验证6（浏览器UI冒烟测试，防止"接口通了但界面卡死"漏检）；deploy.yml 规范新增 GITHUB_TOKEN vs SCP 推送双模式说明（OAuth token 不适用于 git clone）
- 更新 project-retrospective v1.3 验证状态：🔵 → ✅（CO-BUILD-LOG 三路来源合并已真实跑通）
- 无需处理：role-DevOps OPS-19/20/21 踩坑速查已在任务中直接写入

### 2026-03-19 — role-前端开发 v1.1.3 → v1.1.4

- 更新 role-前端开发 v1.1.3→v1.1.4：新增「跨产品前端统一的完整范围」章节，定义4层统一范围（模块层/页面容器层/设计系统层/路由层），强调「只复制 modules/ 目录不等于前端一致」最常见误区

---

### 2026-03-19 — F-021/F-022 两原则落地：全量搜索+全节点审核体系更新

**认知体系依据**：F-021「AI时代全量搜索原则」（L2碎片+L1.5候选P9?）/ F-022「全节点审核机制原则」（L2碎片+L1.5候选P10?）

**F-021（全量搜索）相关更新**：
- SANDBOX-FORMAT.md v1.0→v1.1：「核心设计原则」加入全量搜索原则；Phase 1 改为「全量分支树」格式；新增「分支覆盖声明」表格
- skill-sandbox-expander v1.0.2→v1.0.3：加入「全量搜索约束」（全入口×全链路×全分支）；Step 3 新增 P1b「已有入口缺失分支」+「全量搜索检查」
- role-审核者-用户模拟 v1.2→v1.3：Step 2 从「最短核心路径」改为「全量路径分支树」（含必须路径/建议路径分级）；新增「全量路径覆盖验证」表格
- role-测试工程师 v1.5→v1.6：新增硬性门槛1b「全量路径覆盖」（正常+错误+边界路径+路径覆盖矩阵）；步骤5 改为「全量用户路径测试」

**F-022（全节点审核）相关更新**：
- 新建 Rule full-node-audit.mdc v1.0：全节点审核通用原则（生产节点类型定义/最低3条挑战者反思/节点类型挑战重点对照表/与关卡层级关系/待更新Skill登记清单）
- role-产品经理：新增 Step 2.5「F-022 全节点挑战者反思」（产品定义草稿完成后、关卡A前）
- role-技术架构师：新增 Step 3.5「F-022 全节点挑战者反思」（架构草稿完成后、PM确认前）
- wechat-article-writer v1.1→v1.2：新增 Step 6.8「F-022 全节点挑战者反思」（内容完稿后、审稿前）
- wechat-article-writer v1.2→v1.3：新增 Step 0「强制读取 WG」，修复 WG/WX 参考路径至认知结构正确位置
- general-article-writer v1.0（新建，Level 2）：通用长文写作（技术分析/产品思考/对外分享/随笔），读WG+大纲确认门+挑战者自检+审稿闭环；经关卡A（4条严重问题修复）+ 关卡C（7场景通过）
- research-output v1.0（新建，Level 3）：系统调研 → 图文Markdown（Mermaid+qwen-image）→ 保存到认知结构知识库 → 自动注册三处；触发词「调研/研究一下/帮我系统了解」；经关卡A（3严重+5中等修复）+ 关卡B（2Critical修复：write-guard例外+维护协议矛盾）+ 关卡C（2项修复）
- cognitive-structure-write-guard v1.4→v1.5：新增知识库/路径例外条款（research-output 关卡B触发的规范修复）
- academic-si-writer（全局用户级Skill，路径：C:\Users\Boyuan\.cursor\skills\academic-si-writer\SKILL.md）：LaTeX学术SI写作，细胞力学/生物物理领域，PNAS/Nature风格；已在role-menu注册
- 4个写作类Skill（wechat-article-writer / general-article-writer / academic-si-writer / article-proofreading）已注册进 role-menu.mdc（此前遗漏）

**理论背景**：与深度学习使科研从「剪枝后有限实验」迁移到「全量提取」同理——AI智能体时代使得全量沙盘推演和全节点审核的成本趋近于零，因此方法论应做相应升级

---

### 2026-03-19 — F-022 全节点审核：剩余7个核心生产Skill挑战者步骤落地

**认知根**：F-022「全节点审核机制原则」/ full-node-audit.mdc v1.1（10/10完成）

**本次更新（批次2）**：
- role-前端开发 v1.1.4→v1.1.5：新增 Step 4.5（自测后/提交前）——边界输入崩溃/useEffect副作用/复用遗漏
- role-后端开发 v1.1.4→v1.1.5：新增 Step 4.5（集成测试后/提交前）——接口幂等性/孤立脏数据/成本失控
- role-AI工程师：新增 Step 4.5（staging测试后/提交前）——幻觉降级/成本失控/工作流断裂
- skill-designer v1.1→v1.2：新增 Step 4.5（初稿后/关卡A前）——AI执行者歧义/现有Skill冲突/最易截断步骤
- cognitive-capture-fragment v1.0→v1.1：新增 Step 5.5（用户确认后/写入前）——矛盾检测/置信度诚实/关联文档遗漏
- cognitive-update-knowledge v1.0.1→v1.1：新增 Step 3.5（备份后/写入前）——写入必要性/上游冲突/下游遗漏
- cognitive-extract-principle v1.0.1→v1.1：新增 Step 3.5（候选提出后/确认前）——是否真新/反例构造/操作化检验
- full-node-audit.mdc v1.0→v1.1：更新清单状态（10/10全✅）+ 新增各节点挑战视角重点字段

### 2026-03-19 — IDE 状态劫持意图安全修复

- role-menu.mdc：新增强制规则第11条「指令上下文优先级 — 禁止 IDE 状态劫持意图」，修复模糊指令被 IDE 当前打开文件误触发开发/部署任务的安全漏洞

### 2026-03-19 — 新建 multi-project-file-guard.mdc v1.0

- 新建 Rule `.cursor/rules/multi-project-file-guard.mdc` v1.0
- 根因：workspace 下多个项目（scholar-match / tashan-openbrain_myagent / tashan-world / _worktree_boyuan）存在大量同名文件（DEPLOY_ARCH.md / 技术架构.md / 产品定义.md / 开发计划.md），AI 无规范约束路径精确化，存在操作错误项目文件的风险
- 主要约束：Step 1 项目上下文锁定 / Step 2 路径精确化（禁止模糊路径操作）/ Step 3 READ_FIRST 多项目强化 / Step 4 跨文件引用概念自洽验证

---

### 2026-03-20 — 五条工程原则集成（grill-me / write-a-prd / prd-to-issues / tdd / improve-my-codebase）

**根因**：TASK-20260320-01 对照分析证明5条原则均有明确覆盖缺口，按 skill-rule-修改规范 Level 1 执行批量补丁。

**本次更新**：
- role-产品经理 v1.2→v1.3：新增 Step 0「grill-me 前置追问（Q1真实场景/Q2 MVP边界/Q3最大风险）」+ Step 0.5「write-a-prd 访谈模式（A1-A5 五问）」+ 开发计划垂直切片拆解原则
- 开发计划任务条目模板 v1.0→v1.1：新增「垂直切片范围」字段 +「测试先行（TDD Red 阶段）」字段，更新示例条目
- role-后端开发 v1.1.5→v1.2：新增 Step 0.8「TDD Red→Green→Refactor 循环」——实现前先建测试文件写3类失败测试
- role-前端开发 v1.1.5→v1.2：新增 Step 3.5「TDD」——有业务逻辑的单元先写 .test.ts，纯展示组件跳过
- codebase-explorer v1.0→v1.1：新增 Step 5.5「浅层模块识别」（接口复杂/实现轻薄的模块识别）+ Step 5.6「可测试性扫描」（隐式依赖/无接口抽象/全局副作用/超长函数四类模式）+ 输出格式新增两节表格

### 2026-03-20 — role-产品经理 v1.3→v1.4：权限设计章节 DRY（引用 L1.5 P12）

- **根因**：SKILL 内重复展开「最小必要限制」违背 P11（DRY），L1.5 方为权威层。
- **修改**：「⚠️ 权限设计」改为引用 `底层原则库.md` P12 + 保留产品层三问推论；索引表版本 v1.4、日期 2026-03-20。

### 2026-03-20 — 新建 frontend-brand-guard.mdc v1.0（品牌安全级别约束）

- 新建 Rule `.cursor/rules/frontend-brand-guard.mdc` v1.0，alwaysApply
- 根因：用户明确要求所有前端开发任务严格遵守他山品牌规范，当前无任何 Rule 约束前端输出风格，存在品牌一致性安全风险
- 主要约束：字体（强制 Noto Serif SC）/ 配色（黑白极简/品牌蓝绿两套场景）/ 圆角三级体系（rounded-lg/xl/full）/ 技术框架（React+TS+Vite+Tailwind）/ 禁止清单（9条硬性禁止）
- 关联：extends role-前端开发 / role-UI设计师，validates 由 关卡B 审核

### 2026-03-20 — 新建 frontend-brand Skill v1.0（前端品牌知识层）

- 新建 Skill `.cursor/skills/frontend-brand/SKILL.md` v1.0
- 根因：Rule 只是约束层，所有可复用设计系统内容需以 Skill 形式沉淀；原来 AI 执行前端任务须分散查阅多个 docs 文件，缺少统一知识层
- 覆盖内容：技术框架选型 / 设计令牌完整定义（字体/CSS变量/Tailwind配置）/ 配色场景区分 / 圆角系统 / 11类组件代码模板 / 布局间距 / 动画定义 / Markdown渲染 / a11y约定 / 禁止清单
- 同步更新：`frontend-brand-guard.mdc` Step 2 改为先读 Skill / `role-menu.mdc` 新增角色条目+触发词+配套知识库引用

### 2026-03-20 — frontend-brand Skill v1.0 → v1.1（严格对齐代码真相）

- 根因：用户要求严格验证 SKILL 与 TopicLab 实际代码（index.css / tailwind.config.js）完全一致；逐行比对发现多处严重偏差
- 严重错误修复：`--text-primary` 值（#0F172A→#1E293B）/ fadeIn/blink/slideIn keyframe 参数完全不同
- 缺失内容补全：--bg-tertiary / 旧兼容变量 / radius完整6个变量 / accent.info / surface.disabled / content.disabled / spacing / transitionDuration / .spinner/.status-badge*/.expert-dot-active / Markdown img+h4+hr+text-underline-offset / @layer base 完整属性 / 工具类8项
- 文档不一致说明：shape-system.md 表格说 rounded-lg=12px，实际代码 rounded-lg=16px，SKILL 以代码为准并加说明

### 2026-03-20 — skill-rule-修改规范 v1.4 → v1.5（新增 Rule-Skill 配套完整性检查）

- 根因：AI 在创建 frontend-brand-guard.mdc Rule 时未主动判断需配套 Skill，必须靠用户提醒，属于规范结构性漏洞
- 新增：「修改操作规范」第4条「Rule-Skill 配套完整性检查」——alwaysApply Rule 包含正向知识内容时，强制检查并创建配套 Skill
- 已备份：history/SKILL_v1.4_20260320.md

### 2026-03-20 — 新建 skill-library-search v1.0（全量搜索协议强制化）

- 根因：2026-03-20 真实事故——AI 仅执行3-4条查询就声称全量搜索完成，遗漏3个高星仓库。原协议只是参考文档无法强制执行
- 新建：`.cursor/skills/skill-library-search/SKILL.md`（7维度强制协议 + R2数据完整性规则 + 完成标准）
- 同步：role-menu.mdc 强制规则第11条 + 触发词 + 角色一览表注册
- 验证状态：🔵 待验证

### 2026-03-20 — cognitive-self-reflect v1.0 → v1.1（五维度强制覆盖+最低追问10轮）

- 根因：Step 4「按需追问」给了 AI 过大裁量，实践中 1-2 轮后就跳入写入阶段，反思深度不够
- 修改：Step 2 去掉「判断够了跳步」裁量；Step 4 改为五维度强制深挖（现象/触发/感受/根因/应对）；新增 Step 4.5 双条件门槛检查（5维度全覆盖 + 追问≥10轮）
- 已备份：history/SKILL_v1.0_20260320.md
- 验证状态：🔵 待验证

### 2026-03-20 — OpenBrain myagent 错误修复 + 规范完善（4 Skill 更新）

**背景**：基于对 e3440b7a 等历史对话的错误汇总分析，执行系统性规范修复。

| Skill | 版本 | 修改内容 |
|---|---|---|
| role-后端开发 | v1.2→v1.3 | 新增 Step 0.3「会话冲突检查」——激活后读任务日志检查24h内是否有其他会话改了同名文件 |
| role-测试工程师 | v1.8→v1.9 | 新增 Step 0「本地环境前置检查」——docker ps 检查 postgres；无 DB 禁止直接宣称关卡C通过 |
| role-技术架构师/templates | v1.0→v1.1 | 技术架构模板新增「九、废弃代码清单」节——产品范式变更时必填，列明需删除/替换的旧代码 |
| role-前端开发 | v1.2→v1.3 | 新增「跨产品组件复制：接口契约对比」章节——复制任何跨产品组件前必须先 curl 验证接口字段 |

**同步创建**：
- `backend/SCHEMA.md`：OpenBrain 全量数据库字段清单（SQL唯一真源），修复 display_name 高频踩坑

**所有备份**：
- `role-后端开发/history/SKILL_v1.2_20260320.md`
- `role-测试工程师/history/SKILL_v1.8_20260320.md`
- `role-技术架构师/templates/history/技术架构模板_v1.0_20260320.md`
- `role-前端开发/history/SKILL_v1.2_20260320.md`

验证状态：🔵 待验证
- `document-pipeline` v1.0（Level 4 新建，统一写作流水线）：8个Stage，任意Stage可入场，Stage 0-8（研究/草稿/逻辑自检/真实性校对/画图规划/批量画图/图片自审/审稿/格式转换），经关卡A（9修复）+ 关卡B（4修复+写循环防护）+ 关卡C（3修复）通过
- `document-pipeline` v1.2→v1.3：Stage 5 qwen-image 模型从 `wanx2.1-t2i-turbo` 升级为 `wan2.6-t2i`（官方最新最优模型，速度+50%）；轮询逻辑修复（固定单次sleep改为循环6轮×8s）
- `wechat-article-writer` v1.3→v1.4：thin wrapper 化，触发后转发到 document-pipeline（target_format=html）
- `general-article-writer` v1.0→v1.1：thin wrapper 化，触发后转发到 document-pipeline（target_format=md）
- `research-output` v1.1→v1.2：thin wrapper 化，触发后转发到 document-pipeline（mode=research）
- `research-output` v1.2→v1.3（2026-03-20）：双修复——① Step 4 pre-save 强制图片门（生成图片确认后才允许写文件）；② 触发判断新增 mode=improve 路径（完善已有REF-EXT文档从Step 2入场）；备份：history/SKILL_v1.2_20260320.md
- `research-output` v1.3→v1.4（2026-03-20）：Step 3 新增三条禁止——❌禁Cursor GenerateImage工具 ❌禁只输出提示词 ✅明确唯一路径Shell+Python+dashscope；新增混淆提示区分article-image-angles/GenerateImage/正确路径
- `research-output` v1.4→v1.5（2026-03-20）：Step 3 彻底重写——删除矛盾的「先读wechat-article-writer Step 4」旧指令；统一改为「加载ai-image-generator SKILL.md，按其Step 0-4执行」；新增❌禁article-image-angles混淆说明；ai-image-generator已在v1.1存在（之前Glob搜索方式失误未找到）
- `research-output` v1.6→v2.0（2026-03-21）：架构重写——废弃thin-wrapper恢复独立执行；新增Phase1关键词架构（种子词/扩展/聚类/Mermaid图谱/用户确认）；新增Phase2多轮迭代（WebFetch读原文强制、知识节点格式、第一轮盘点）；新增Phase3关键词更新+第二轮定向填空（对比搜索/批评类搜索）；新增Phase4知识网络三层合成（核心/中间/外围+连接图）；Phase5文档结构改为从知识网络映射；参考资料表新增「已读原文」列；备份：history/SKILL_v1.6_20260321.md

### 2026-03-20 — role-menu.mdc 新增强制规则第13条（Skill触发词强制前置拦截）

**根因**：真实漏洞——用户说「调研XXX」命中 research-output 触发词，AI 未加载 Skill 直接输出聊天，且被指出后又跳过 project-convention-resolver 直接补做任务。根本原因：role-menu 触发词检查是描述性的而非强制拦截性的。

**修改内容**：
- `role-menu.mdc` 强制规则第13条：Skill触发词强制前置拦截，命中触发词必须先加载 Skill，不允许直接回复
- 追加：发现规范偏差时必须先走 project-convention-resolver，不得跳过根因修复

**备份**：`.cursor/rules/history/role-menu_20260320.mdc`

验证状态：🔵 待验证（下次出现调研类请求时观察 AI 是否主动宣告加载 Skill）

---

### 2026-03-21 — skill-simulator v1.0 验证状态升级（🔵→✅）

| 日期 | Skill | 变更 | 说明 |
|---|---|---|---|
| 2026-03-21 | skill-simulator v1.0 | 状态升级 🔵→✅ | Phase 2 Gate A 首次真实执行：发现5 Critical+6 Important问题，验证有效 |

**根因**：skill-system-evolution-executor Phase 2（关卡A）中被真实调用，以「第一次看到这个计划的AI执行者」视角成功审核了Skill体系完善计划，发现§7.4编号冲突、P0-C静默失效等关键问题，首次真实验证效果显著。

**同步更新**：SKILL-INDEX 表格中新增 skill-simulator 行（原遗漏未收录），状态直接设为 ✅ 已验证。

### 2026-03-21 — cognitive-reorganize + cognitive-capture-fragment 触发词与前置扫描修复

| 日期 | Skill | 变更 | 说明 |
|---|---|---|---|
| 2026-03-21 | cognitive-reorganize v1.1.1→v1.2 | Step 0.5 单文件分类 | 新增 Step d：单文件询问时执行四轴快速分类，输出目标路径 + 写入方式推荐（CS-009 Gap修复）|
| 2026-03-21 | cognitive-reorganize v1.1→v1.1.1 | 触发词扩展 | 新增"如何加入认知结构"等6个自然语言变体；询问流程时先展示分类清单现状 |
| 2026-03-21 | cognitive-capture-fragment v1.1→v1.2 | Step 1 增加前置扫描 | 读取文档分类清单，发现相关已有文档时提示用户路由 |

**根因**：用户问"按照规范，要如何加入"时，AI未加载任何Skill（Rule 13违反），导致分类清单未读、已有文档漏查。两处修复共同保证：1）自然语言表达能触发正确Skill；2）即使走捕捉碎片路径，也能发现已有相关文档。

---

### 2026-03-21 — skill-system-destroyer v1.0 补录并验证状态升级（✅）

| 日期 | Skill | 变更 | 说明 |
|---|---|---|---|
| 2026-03-21 | skill-system-destroyer v1.0 | 状态升级/补录 ✅ | Phase 2 Gate B 首次真实执行：发现3 Critical+4 High问题，验证有效 |

**根因**：skill-system-evolution-executor Phase 2（关卡B）中被真实调用，以「想让Skill体系失效的破坏者」视角成功审核了完善计划，发现3个Critical（含 role-menu Rule 14 inline copy 导致 Step 1.5 静默失效的C1问题）+ 4个High问题，首次真实验证效果显著。

**同步更新**：SKILL-INDEX 表格中新增 skill-system-destroyer 行（原遗漏未收录），状态直接设为 ✅ 已验证。

### 2026-03-20 — role-后端开发 v1.3 → v1.4（新增 Step 0.2 API集成变更门）

| Skill | 版本 | 修改内容 |
|---|---|---|
| role-后端开发 | v1.3→v1.4 | 新增 Step 0.2「API 集成变更门（blocking gate）」——任何路由/端点/返回字段/委托关系变更前，必须输出 API 契约检查表（变更项+下游消费方+依赖字段+满足情况），有❌必须解决后才继续 |

**根因**：tashan-openbrain Phase 2 中，nginx 将 `/api/auth/` 全量转发到 topiclab，绕过 OpenBrain Python 的 workspace_id 附加逻辑，导致所有用户登录后触发创作者激活弹窗。根本原因：改变路由时未检查下游消费方字段期望（违反 L1.5 P17 下游优先检查原则）。

**备份**：`role-后端开发/history/SKILL_v1.3_20260320.md`

**验证状态**：🔵 待验证

### 2026-03-20 — role-前端开发 v1.3 → v1.4（新增 Step 0.2 前端 API 消费检查门）

| Skill | 版本 | 修改内容 |
|---|---|---|
| role-前端开发 | v1.3→v1.4 | 新增 Step 0.2「前端 API 消费检查门（blocking gate）」——修改 API 路径/响应字段消费/认证委托前须输出「前端 API 消费检查表」，所有❌须解决后才继续（L1.5 P17） |

**根因**：tashan-openbrain 开发中，backend 改变 nginx 路由时，前端 AuthContext 消费 `/auth/login`、`/auth/me` 响应中的 `workspace_id` 被静默破坏；改上游未检查下游字段期望。

**备份**：`role-前端开发/history/SKILL_v1.3_20260320.md`

**验证状态**：🔵 待验证

---

### 2026-03-21 — role-技术架构师 v1.2 → v1.3（Step 0.5 新增跨项目已有能力检查子步骤）

| Skill | 版本 | 修改内容 |
|---|---|---|
| role-技术架构师 | v1.2→v1.3 | Step 0.5 新增「跨项目已有能力检查（RULE-36 扩展）」子步骤——Read 元项目导航，对记忆/认知/AI调用/认证四类模块逐项检查是否已有跨项目实现，有则复用并声明来源，无则自行设计 |

**根因**：brain_ask 人格化架构设计时未检查 tashan-openbrain 已有 SOUL.md+MIND.md 体系，重新设计 Tri-Layer 框架造成重复造轮子，用户发现后才纠正。根因是 Step 0.5 只检查端口冲突，未覆盖跨项目能力复用。

**备份**：`role-技术架构师/history/SKILL_v1.2_20260321.md`

**验证状态**：🔵 待验证

---

### 2026-03-21 — role-前端开发 v1.4 → v1.5（新增 Step 4.8 服务运行检查门）

| Skill | 版本 | 修改内容 |
|---|---|---|
| role-前端开发 | v1.4→v1.5 | 新增 Step 4.8「服务运行检查门」——输出验收清单前先判断服务是否运行；未运行时改为「待部署后验收清单」并询问是否需要启动，禁止输出「请在浏览器中验证」类语句 |

**根因**：TASK-20260321-46（TwinSetupFlow 前端）完成后按 Step 5 输出了人工验收清单，但 tashan-openbrain 服务从未在本机启动（.env 为 Windows 路径），用户无法测试任何内容。Skill 缺少「服务是否运行」前置检查，同类问题在本对话中多次复现，属系统性漏洞。

**备份**：`role-前端开发/history/SKILL_v1.3_20260321.md`

**验证状态**：🔵 待验证

---

### 2026-03-21 — 新建 Rule opencode-plugin-compatibility.mdc v1.0

- 新建 Rule `.cursor/rules/opencode-plugin-compatibility.mdc` v1.0，agentRequested（按需触发）
- 根因：tashan-workbench Phase B 架构师提出集成 openclaw memory-core 插件，调研和设计投入大量时间后才发现 openclaw plugin SDK 与 openwork-server（opencode 生态）完全不兼容，被迫重新设计，浪费整个 Phase 工时
- 主要内容：opencode vs openclaw 生态对比表 / 三项强制前置检查 / 已踩坑典型案例 / 违反后果说明
- 触发条件：涉及 opencode、openclaw、openwork-server、tashan-workbench 集成第三方框架/插件的任务

**验证状态**：🔵 待验证（下次集成第三方框架时验证）

---

### 2026-03-21 — role-产品经理 v1.4 → v1.6

| 日期 | Skill | 版本 | 修改摘要 |
|---|---|---|---|
| 2026-03-21 | role-产品经理 | v1.4→v1.5 | Step 2.5 新增第4条「系统行为层缺失检查」，追问每个用户操作节点的系统后端自动行为（PD-014根因修复）|
| 2026-03-21 | role-产品经理 | v1.5→v1.6 | 新增 Step -1「单一真源检查」，创建新文档前先检查是否有归属主文档，防止文档漂移（R9 VERSION_CONTINUITY落地）|

---

### 2026-03-21 — role-DevOps v1.2.2 → v1.2.5

| 日期 | Skill | 版本 | 修改摘要 |
|---|---|---|---|
| 2026-03-21 | role-DevOps | v1.2.2→v1.2.3 | RULE-LOC 新增 Step L4 9项验证清单（服务未运行时禁止输出人工验收清单）|
| 2026-03-21 | role-DevOps | v1.2.3→v1.2.4 | RULE-LOC V10 数据库认证可用性（401非503）|
| 2026-03-21 | role-DevOps | v1.2.4→v1.2.5 | RULE-LOC V11+ 功能路径测试门（本次改了什么就测什么，修复第三次「完成但没测新路径」问题）|

---

### 2026-03-21 — 全量闭环 Gap 修复（9个组件，SD/CG/CP/PD 类缺口）

| 日期 | 组件 | 版本 | 修改摘要 |
|---|---|---|---|
| 2026-03-21 | session-bootstrap.mdc | v1.4→v1.5 | 新增 A2.5 PENDING-EXPERIENCES 主动推进（积压≥5条时任务开始前提示，SD4修复）|
| 2026-03-21 | skill-capture-closure | v1.1→v1.2 | 新增 Step 7.5 role-menu 同步检查（新建Skill后自动判断是否加入role-menu，SD1修复）|
| 2026-03-21 | write-task-log | v1.1→v1.2 | 任务日志格式新增可选 triggered_skills 字段（SD3修复，支持Skill频率数据采集）|
| 2026-03-21 | cognitive-cascade-notifier.md | v1.0→v1.1 | 扩展输出包含 Loop 1 Skill 体系通知（新原则确认后扫描相关Skill，SD2修复）|
| 2026-03-21 | cognitive-capture-fragment | v1.2→v1.3 | 新增 Step 5.8 L2积累阈值监控（≥8条时主动提示整合，CS-014修复）|
| 2026-03-21 | cognitive-daily-briefing | v1.0→v1.1 | 新增 Step 2.5 全量一致性检查日期监控（>7天未运行时积压提示，CS-015修复）|
| 2026-03-21 | role-数据分析师 | v1.1→v1.2 | 新增 Step 5.5 自动写入产品问题追踪台（断裂节点发现后自动记录，PD2修复）|
| 2026-03-21 | wechat-article-writer | thin wrapper更新 | 文章发布后询问原创洞见回流（CP1修复，L1回流提示）|
| 2026-03-21 | product-launch-validator（新建）| v1.0 | 立项时三大闭环兼容性检查（Loop1/2/3，PD1修复）|
| 2026-03-21 | 沙盘 CS-014/CS-015 | validated | cognitive-capture-fragment L2积累 / cognitive-daily-briefing一致性检查 |

---

### 2026-03-21 — 认知域 Subagent 体系批次1（CS-010+CS-011 修复）

| 日期 | 组件 | 版本 | 修改摘要 |
|---|---|---|---|
| 2026-03-21 | cognitive-verifier.md（新建） | v1.0 | 认知自洽验证器：独立 context 验证 L1 更新后的 CV-1/CV-2/CV-3 三项，修复创作者视角偏差（CS-010）|
| 2026-03-21 | cognitive-cascade-notifier.md（新建）| v1.0 | 认知级联通知器：新原则/L1重大更新后后台触发五域对齐检查待办（CS-011，Loop2→Loop3级联）|
| 2026-03-21 | cognitive-update-knowledge | v1.1→v1.2 | 新增 Step 8（verifier）+ Step 9（cascade），B4 时机后移至 verifier 结论后 |
| 2026-03-21 | cognitive-integrate-fragments | v1.2→v1.3 | 新增 Step 7（verifier 调用，整合完成后独立自洽验证）|
| 2026-03-21 | cognitive-extract-principle | v1.1→v1.2 | 新增 Step 4e（cascade-notifier 后台触发，原则确认后级联通知）|
| 2026-03-21 | session-bootstrap.mdc | v1.3→v1.4 | 新增 B0 认知子任务排除清单（防止无限循环，C-1 修复）|

---

### 2026-03-21 — 认知域 Subagent 体系批次2（CS-012+CS-013 修复）

| 日期 | 组件 | 版本 | 修改摘要 |
|---|---|---|---|
| 2026-03-21 | cognitive-fragment-integrator.md（新建）| v1.0 | 碎片批量整合器：碎片≥5条时独立context执行「内部居民」视角分析，输出精确整合方案（CS-012）|
| 2026-03-21 | cognitive-task-reflector.md（新建）| v1.0 | 任务认知萃取器：认知类任务后独立context主动萃取，L1.5候选正确路由（CS-013，Loop3→Loop2）|
| 2026-03-21 | cognitive-integrate-fragments | v1.3→v1.4 | 新增 Step 0.5（碎片≥5条时调用 fragment-integrator）|
| 2026-03-21 | write-task-log | v1.0→v1.1 | 废弃步骤四，新增步骤五（cognitive-task-reflector接管，认知类任务自动触发）|

---

### 2026-03-22 — 认知根原则全面落地（D0 步骤 + Gate A/B + 产品定义模板）

| 日期 | 组件 | 版本 | 修改摘要 |
|---|---|---|---|
| 2026-03-22 | role-审核者-用户模拟 | v1.3→v1.4 | D0认知根确认行 + A-11认知根核查 + 闭环第7条（产品核心假设是否有L1产品理论支撑）|
| 2026-03-22 | role-审核者-系统破坏 | v1.2→v1.3 | D0认知根+原则基础行 + B-13 L1.5原则合规 + L1.5原则合规性独立表格 |
| 2026-03-22 | role-产品经理 | v1.6→v1.7 | 知识导航表新增 D0 认知根确认行 |
| 2026-03-22 | role-技术架构师 | +D0 | 知识导航表新增 D0 认知根确认行（L1系统架构思维维度）|
| 2026-03-22 | role-前端开发 | v1.5→v1.6 | 知识导航表新增 D0 认知根确认行（L1.5原则）|
| 2026-03-22 | role-后端开发 | +D0 | 知识导航表新增 D0 认知根确认行（L1.5原则）|
| 2026-03-22 | role-AI工程师 | v1.2→v1.3 | 知识导航表新增 D0 认知根确认行（L1 AI智能体任务分类体系）|
| 2026-03-22 | role-UI设计师 | v1.2→v1.3 | 知识导航表新增 D0 认知根确认行（L1产品理论体验章节）|
| 2026-03-22 | role-数据分析师 | v1.2→v1.3 | 知识导航表新增 D0 认知根确认行（L1产品理论闭环指标）|
| 2026-03-22 | role-测试工程师 | v1.10→v1.11 | 知识导航表新增 D0 认知根确认行（L1 AI智能体任务分类体系五维度）|
| 2026-03-22 | wechat-article-writer | +D0 | 参考文档区域新增 D0 认知根确认（L1文档先读）|
| 2026-03-22 | research-output | +D0 | 新增 D0 章节（调研前先扫 L0 找相关 L1 文档）|
| 2026-03-22 | skill-product-definition-template.md | +认知根字段 | 2.4 依赖声明新增「认知根文档（L1/L1.5）」必填字段 |
| 2026-03-22 | frontend-brand | v1.1→v1.2 | 补充背景适配规则：区分浅色/深色容器配色要求，附 DocTree/ProposalCard 踩坑案例 |

### 2026-03-22 — project-retrospective-20260322 批量沉淀

| 日期 | Skill | 版本 | 修改摘要 |
|---|---|---|---|
| 2026-03-22 | cognitive-input-classifier | v1.0→v1.0.1 | 补充「先按规范记录」触发词识别，区分 CO-BUILD-LOG vs L2碎片路径 |
| 2026-03-22 | frontend-brand | v1.1→v1.2 | 新增背景适配规则（浅色/深色容器配色分层规范，DocTree/ProposalCard踩坑案例）|
| 2026-03-22 | role-产品经理 | v1.5→v1.6 | Step -1 单一真源检查 + Step 2.5 第4条系统行为层检查 |
| 2026-03-22 | role-后端开发 | +Step4.9 | 开发计划任务状态同步门（代码完成后必须更新开发计划）|
| 2026-03-22 | write-task-log | v1.3→v1.4 | 序号生成改为 grep全文取最大序号+1，防多session并发冲突（GAP-CO009-1）|
| 2026-03-22 | role-前端开发 | v1.6→v1.7 | Step 0.2 补 BE修复路由，❌后端字段问题时暂停并路由 role-后端开发（GAP-PD015-1）|
| 2026-03-22 | research-output | v2.1→v2.2 | Phase 9 补 L1矛盾检测提示，D0 找到相关L1时调研完成后询问矛盾检测（GAP-CN009-1）|
| 2026-03-22 | skill-system-health-check | v1.1→v1.2 | P0路由改为触发 project-convention-resolver 而非直接 skill-rule-修改规范（GAP-SK017-1）|
| 2026-03-22 | project-convention-resolver | v1.0→v1.1 | Step 5 E类修复后，若来源为 health-check 报告建议重新运行验证（GAP-SK017-2）|
| 2026-03-22 | wechat-article-writer | v1.4→v1.5 | Step 6.5 前补三层发布前质检架构说明（Layer1内容/Layer2 HTML/Layer3品牌）（GAP-CN008-1）|
| 2026-03-22 | issue-tracker | v1.0→v1.1 | Step 4 补技术-产品冲突后 GATE-A 重触发提醒（GAP-PD014-1）|
| 2026-03-22 | history-auditor | v1.0→v1.1 | 新增 Step 5.5，重复踩坑≥2次时主动提示触发 skill-capture-closure（GAP-CO010-1）|
| 2026-03-22 | cognitive-ask | v1.3→v1.4 | 致命矛盾强化触发，🔴 致命冲突使用「强烈建议立即运行」差异化语气（GAP-CS016-1）|

**已清理**：
- PENDING-EXPERIENCES：F-040/F-041 标记 ✅，DevOps NPC下载3条标记 ✅，cognitive-capture-fragment步骤偏差标记 ✅
- PENDING-EXPERIENCES：3条今日新增（MESSAGE_AGENT认知注入/listPanel空矩形/深浅背景颜色）写入并标记 ✅

| 2026-03-23 | skill-capture-closure | v1.4→v2.0 | 重构主分类轴（现象→B/K对象类型），双向诊断（修复+沉淀），新增完整 K-object ceremony 路径组（K-3-M/C、K-1-M/C、K-0-M、K-F-C、K-2、K-4）|
| 2026-03-23 | skill-capture-closure | v2.0→v2.1 | 新增知识导航表（D0→自进化形式规范 + D3→Skill体系设计原则 + D4→SKILL-INDEX）|
| 2026-03-23 | project-retrospective | v1.3→v1.3.1 | 新增知识导航表（D0/D3/D4 + 核心概念速查）|
| 2026-03-23 | skill-rule-修改规范 | v1.7→v1.7.1 | 新增知识导航表（D0/D3/D4 + 核心概念速查）|
| 2026-03-23 | role-技术架构师 | v1.2→v1.2.1 | 新增知识导航表（D0+①②③④⑤）+ 元认知前置 |
| 2026-03-23 | role-DevOps | v1.3.0→v1.3.1 | 知识导航表新增 D0 认知根行 |
| 2026-03-23 | cognitive-capture-fragment | v1.3→v1.3.1 | 新增知识导航表 |
| 2026-03-23 | cognitive-integrate-fragments | v1.4→v1.4.1 | 新增知识导航表 |
| 2026-03-23 | cognitive-update-knowledge | v1.2→v1.2.1 | 新增知识导航表 |
| 2026-03-23 | cognitive-extract-principle | v1.2→v1.2.1 | 新增知识导航表 |
| 2026-03-23 | cognitive-ask | v1.4→v1.4.1 | 新增知识导航表 |
| 2026-03-23 | cognitive-daily-briefing | v1.1→v1.1.1 | 新增知识导航表 |
| 2026-03-23 | cognitive-consistency-check | v1.0→v1.0.1 | 新增知识导航表 |
| 2026-03-23 | skill-system-health-check | v1.2→v1.2.1 | 新增知识导航表 |
| 2026-03-23 | skill-evolution-planner-meta | v1.0→v1.0.1 | 新增知识导航表 |
| 2026-03-23 | three-loop-health-check | v2.0→v2.0.1 | 新增知识导航表 |
| 2026-03-23 | product-evolution-planner | v1.0→v1.0.1 | 新增知识导航表 |
| 2026-03-23 | issue-tracker | v1.1→v1.1.1 | 新增知识导航表 |
| 2026-03-23 | project-closeout | v1.2→v1.2.1 | 新增知识导航表 |
| 2026-03-23 | codebase-explorer | v1.0→v1.0.1 | 新增知识导航表 |
| 2026-03-23 | document-pipeline | v1.5→v1.5.1 | 新增知识导航表 |
| 2026-03-23 | research-output | v2.2→v2.2.1 | 新增知识导航表 |
| 2026-03-23 | wechat-article-writer | v1.5→v1.5.1 | 非标准导航表升级为标准格式 |
| 2026-03-23 | general-article-writer | v1.0→v1.0.1 | 新增知识导航表 |
| 2026-03-23 | article-proofreading | v1.0→v1.0.1 | 新增知识导航表 |
| 2026-03-23 | role-产品开发协调者 | 新建 v1.0 | 产品开发域团队负责人，5种任务类型，briefing协议，分层治理架构第一个协调者 |
| 2026-03-23 | session-bootstrap（Rule）| v1.9→v2.0 | A1重构：域识别优先路由，产品开发域请求经 role-产品开发协调者 |
