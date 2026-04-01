---
name: tashan-cursor-skills
description: 他山 Cursor Skill 体系（合集入口）— 95 个 Skills、32 条 Rules、18 个 SubAgents；覆盖产品→架构→开发→测试→上线全链路，含认知积累与 Skill 自进化机制。适用于 Cursor / OpenClaw 工作区一键安装。触发词：他山 skill、Tashan skills、tashan-cursor-skills、安装他山规范、三大闭环、session-bootstrap。
---

# 他山 Cursor Skill 体系（合集）

> **类型**：技能合集 / 安装入口（单条他山世界 Skill 指向完整仓库，非逐文件拆分）。  
> **定位**：Self-Evolving Agent Harness — 执行套具 + 三大闭环（执行层 / 工作层 / 记忆层）+ D5 信号自进化。

## 这是什么

一套面向 **Cursor**（及兼容 OpenClaw 规则的工作区）的规范体系：

| 组件 | 规模 | 作用 |
|---|---|---|
| **Skills** | 95 | 按需加载的执行步骤（角色 / 认知 / 质量关卡 / 元体系等） |
| **Rules** | 32 | `alwaysApply` 约束（含 `session-bootstrap` 对话序列、`role-menu` 触发路由等） |
| **SubAgents** | 18 | 独立 context 的验证者（关卡 A/B/C、fixer、cognitive-* 等） |

完整说明、架构图与 Skill 速查见开源仓库 README。

## 权威来源

- **GitHub**：https://github.com/TashanGKD/tashan-cursor-skills  
- **许可证**：MIT

## 安装方式（推荐）

在项目根目录执行（需 Node / npx）：

```bash
npx ai-agent-skills install TashanGKD/tashan-cursor-skills
```

全局安装（所有项目可用）：

```bash
npx ai-agent-skills install --global TashanGKD/tashan-cursor-skills
```

**手动安装**：克隆仓库后，将 `skills/`、`rules/`、`agents/` 分别复制到目标项目的 `.cursor/skills/`、`.cursor/rules/`、`.cursor/agents/`，重启 Cursor。

## 使用要点

1. 日常只说任务描述即可；`role-menu` 会按触发词路由到对应 Skill。  
2. 产品开发类任务通常先经 **role-产品开发协调者** 再派发到具体角色。  
3. 任务结束后由 **session-bootstrap** 序列 B 驱动经验沉淀（与 PENDING-EXPERIENCES、任务日志等联动）。  
4. 修改任意 Skill/Rule/Agent 前须遵循仓库内 **skill-rule-修改规范**（三问 + 备份 + 变更记录）。

## 与他山世界的关系

本条目在他山世界 **Skill 专区** 作为「合集入口」发布：用户从世界发现后，按上文命令安装到本地 Cursor 工作区即可生效。版本迭代以 GitHub 仓库与 `CHANGELOG.md` 为准；可在本地用 `git pull` 或重新执行 install 同步更新。

## 变更记录（本 SKILL 条目）

| 版本 | 日期 | 摘要 |
|---|---|---|
| 0.1.0 | 2026-04-01 | 初始发布：合集入口 + 安装说明 + 权威链接 |
