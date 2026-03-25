# Agent 统一任务信封（Agent I/O Contract）

> 来源：基于 closure-orchestration-package 的 agent-task-envelope.yaml 本地化
> 用途：新建子智能体时，必须按此格式定义其输入/输出契约
> 位置：保存到 skill-designer/ 目录，作为设计新 Agent 时的参考模板

---

## 为什么需要统一信封

没有统一任务信封时：
1. 主控（主 Agent）无法可靠续跑——不知道子智能体的状态
2. branch 无法被自动接手——缺少 case_id / branch_id 追踪
3. 验证结果无法稳定回流——输出是自由文本，无法解析
4. repair branch 无法自动触发——没有 failure_evidence 结构

---

## 输入信封格式（调用子智能体时必须提供）

```yaml
task_id: "<TASK-YYYYMMDD-NN>"          # 唯一任务标识
case_id: "<case-name>"                  # 所属闭环 case（如 project-retrospective-20260319）
branch_id: "<branch-name>"             # 当前分支（如 skill-update-role-后端开发）
goal: "<一句话说明本次任务目标>"
scope: "<明确的处理范围，越窄越好>"
allowed_write_set:                      # 允许写入的文件列表（严格限制）
  - "<文件路径1>"
  - "<文件路径2>"
required_outputs:                       # 期望产出的结构化输出
  - "<产出物1描述>"
done_criteria:                          # 完成标准（可验证的条件）
  - "<条件1>"
  - "<条件2>"
upstream_artifacts:                     # 上游产出物（前序步骤的结果）
  - "<引用说明>"
relevant_rules:                         # 适用的规则（如 skill-rule-修改规范）
  - "<规则名>"
preferred_skill: "<优先使用的 Skill>"
```

---

## 输出信封格式（子智能体必须返回）

```yaml
status: "done | blocked | needs_split | failed | partial"
produced_artifacts:                    # 实际产出物列表
  - path: "<文件路径>"
    summary: "<一句话描述>"
summary: "<本次执行的整体摘要>"
evidence: "<支持结论的证据，具体到行/节点>"
new_risks:                             # 执行中发现的新风险
  - "<风险描述>"
suggested_next_branches:               # 建议的后续分支（失败时自动触发 repair）
  - branch_type: "repair | verify | implement | merge"
    goal: "<建议目标>"
    reason: "<为什么建议这个分支>"
gate_recommendation: "pass | fail | needs_review"
```

---

## 现有子智能体的信封状态

| 子智能体 | 当前状态 | 升级优先级 |
|---|---|---|
| skill-updater | 接收自由文本，无结构化 I/O | 🔴 高（影响 project-retrospective 可靠性）|
| verifier | 输出结构化报告，但无 suggested_next_branches | 🟠 中（repair 回路缺失）|
| arch-destroyer | 输出结构化报告，无 gate_recommendation 字段 | 🟡 低 |
| user-simulator | 输出结构化报告，无 suggested_next_branches | 🟡 低 |
| experience-logger | 极轻量，后台模式，暂不需要信封 | ✅ 暂缓 |
| co-build-logger | 极轻量，后台模式，暂不需要信封 | ✅ 暂缓 |
| wechat-scraper | 已有结构化输出（文件路径列表）| ✅ 基本满足 |
