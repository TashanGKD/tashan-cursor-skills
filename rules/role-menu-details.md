# role-menu 配套知识库与变更记录

> 关系类型：references（被 role-menu.mdc alwaysApply Rule 引用，详细内容存于此）
> 本文件不参与 alwaysApply 注入，供需要时主动读取

---

## 配套模板与知识库

| 文件 | 用途 |
|---|---|
| `.cursor/rules/document-reference-guard.mdc` | **文档引用留痕与级联更新约束（F-033/F-034）**：被引用文档追踪其引用方，文档变动时传播到所有引用方（2026-03-20 新建）|
| `.cursor/rules/tech-discovery-capture.mdc` | **开发中技术发现捕捉**：不确定先搜索（信号一）；高价值方案调用子智能体写带图文档（信号二）|
| `.cursor/rules/frontend-brand-guard.mdc` | **前端品牌约束层（alwaysApply）**：禁止清单 + 场景触发 + 规范文档索引；与 frontend-brand Skill 配套 |
| `.cursor/skills/frontend-brand/SKILL.md` | **前端品牌设计系统（知识层）**：技术框架/设计令牌/组件模板/配色/圆角/动画/a11y 完整可复用手册 |
| `_内部总控/认知结构/L1_系统性文档/技术架构思维维度/知识库/_技术发现文档_TEMPLATE.md` | **技术发现文档模板**（REF-EXT）：含必填架构图/流程图节，产出存入认知结构技术架构思维维度知识库 |
| `.cursor/skills/role-产品经理/templates/产品定义模板.md` | 新项目产品定义标准格式 |
| `.cursor/skills/role-产品经理/templates/开发计划任务条目模板.md` | 开发计划任务条目格式 |
| `.cursor/skills/role-技术架构师/templates/技术架构模板.md` | 技术架构文档标准格式 |
| `.cursor/skills/role-前端开发/knowledge/前端踩坑速查.md` | 8条真实前端踩坑 |
| `.cursor/skills/role-后端开发/knowledge/后端踩坑速查.md` | 10条真实后端踩坑 |
| `.cursor/skills/role-DevOps/knowledge/部署踩坑速查.md` | 10条真实部署踩坑 |
| `.cursor/skills/role-测试工程师/templates/Bug报告模板.md` | Bug/产品偏差报告格式 |
| `.cursor/skills/skill-rule-修改规范/SKILL.md` | **修改任何 Skill/Rule/Agent 前必读**（含复杂度分级 Step 0）|
| `.cursor/skills/skill-index/SKILL-INDEX.md` | **Skill 总索引**：所有 Skill/Agent/Rule 的状态、版本、触发词一览 |
| `.cursor/skills/skill-index/PENDING-SKILLS.md` | **Skill 需求池**：待开发的 Skill 清单，含优先级和复杂度级别 |
| `.cursor/skills/skill-index/SYSTEM-BLUEPRINT.md` | **系统蓝图**：基于历史对话的全量任务类型/闭环/子智能体编排分析 |
| `.cursor/skills/skill-index/CO-BUILD-LOG.md` | **协作建设日志**：人机协作过程中的决策轨迹记录（过程层）|
| `.cursor/skills/skill-index/PENDING-EXPERIENCES.md` | **经验暂存区**：任务执行中 AI 自动感知的踩坑/发现（结果层）|
| `.cursor/skills/skill-designer/skill-product-definition-template.md` | **Skill 产品定义模板**：新建 Skill 前填写的双层设计卡片 |
| `.cursor/skills/project-retrospective/SKILL.md` | **项目复盘入口**：项目结束后批量沉淀 Skill 经验 |
| `_内部总控/AGENT_RULES.md` | **项目治理文档**：代码提交/关联声明/理论体系/格式标准等（AI 在相关任务时参考）|
| `.cursor/rules/knowledge-integrity-rules.mdc` | **认知完整性护栏**：R1-R13（禁止捏造/证据优先/先读后析/记忆边界等），alwaysApply 全局生效 |
| `.cursor/skills/skill-designer/agent-io-contract.md` | **子智能体 I/O 契约**：统一任务信封格式（含递归保护字段）|
| `_内部总控/skill-system-design/DOMAIN-REGISTRY.md` | **五域节点图**：产品开发/认知结构/公司运营/内容宣传/Skill体系的触发链路形式化描述 |
| `_内部总控/skill-system-design/NODE-IO-CONTRACTS.md` | **节点I/O契约**：40个节点的输入/处理/输出/触发下游精确定义 |
| `_内部总控/skill-system-design/SANDBOX-FORMAT.md` | **沙盘格式规范**：两阶段验证场景的标准格式（供元验证器使用）|
| `_内部总控/skill-system-design/sandboxes/` | **沙盘库**：35+个已写沙盘，目标100个，按域存放 |
| `_global-skill-library/` | **全量外部 Skill 参考库**：18仓库/3568个SKILL.md，M0-M5分类体系，Phase 2 吸收来源（`skill-library-harvester` 待建）|
| `_global-skill-library/全量搜索协议.md` | **Skill库搜索规范**：7维度搜索+R2数据完整性规则，防止系统性遗漏 |

---

## 变更记录

### 2026-03-19 — 新增 research-output + write-guard 知识库路径例外

**根因**：新建 research-output（系统调研输出 Skill），需注册到 role-menu；同时关卡B发现 write-guard 需新增 知识库/ 路径例外条款。

**修改内容**：
- 新增：research-output 角色条目 + 触发词示例

### 2026-03-19 — 注册4个写作类 Skill（writing system 补全）

**根因**：写作类 Skill（wechat-article-writer / general-article-writer / academic-si-writer / article-proofreading）均未在 role-menu 中注册，违反 SK-001 规定。

**修改内容**：
- 新增：4个写作类 Skill 的角色一览条目
- 新增：4条使用方式触发词示例

### 2026-03-19 — 新增规则11：指令上下文优先级（IDE 状态劫持安全修复）

**根因**：2026-03-19 真实事件——用户在认知文档保存完毕后说「按规范执行」，AI 因 IDE 当前打开技术架构文件便路由至后端开发 Skill，写了数百行代码。

### 2026-03-20 — 注册 frontend-brand Skill + 全量 Skill 参考库 + 规则13

- 注册 frontend-brand Skill、_global-skill-library 到配套知识库
- 新增规则13：Skill触发词强制前置拦截

### 2026-03-20 — P0-2：配套知识库 + 变更记录移出主文件（减少 alwaysApply 注入体量）

**根因**：role-menu.mdc 的「配套知识库」表格和「变更记录」是文档性内容，非行为约束，alwaysApply 注入属于纯浪费。迁移到本文件（role-menu-details.md），role-menu.mdc 中保留路由表+触发词+规则，减少约 40% 注入体量。
