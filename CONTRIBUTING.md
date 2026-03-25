# 贡献指南

感谢你考虑为他山 Cursor Skill 体系做贡献！

---

## 贡献类型

### 新增 Skill

1. 阅读 [Skill 设计原则](docs/Skill体系设计原则_v1.0.md)，确认是否应该建为 Skill（而不是 Rule 或 Agent）
2. 在 `skills/` 目录创建新文件夹，包含 `SKILL.md`
3. 在 `index/skill-index/SKILL-INDEX.md` 中注册（版本 / 触发词 / 说明）
4. 提交 PR，标题格式：`feat(skills): 新增 [skill名称]`

### 修改 Skill / Rule / Agent

修改前必须执行**三问协议**（在 PR 描述中回答）：

1. **根因**：为什么需要修改？发现了什么问题？
2. **影响范围**：这个修改影响哪些任务场景？是否影响其他 Skill/Rule？
3. **验证方法**：如何验证修改是有效的？用什么场景测试？

### 改进文档

- 改进 README.md / README.en.md：遵循 [README 写作规范]
- 补充 docs/：欢迎添加使用案例、最佳实践

---

## PR 规范

### 标题格式

```
<类型>(<范围>): <简短描述>
```

类型：`feat`（新增）/ `fix`（修复）/ `docs`（文档）/ `refactor`（重构）/ `chore`（维护）

示例：
- `feat(skills): 新增 frontend-qa-agent Skill`
- `fix(rules): 修复 session-bootstrap 阈值判断逻辑`
- `docs(readme): 补充快速开始章节`

### PR 描述模板

```markdown
## 这个 PR 做了什么

（简洁描述变动内容）

## 为什么要做这个变动

根因：
影响范围：
验证方法：

## 变动类型

- [ ] 新增 Skill/Rule/Agent
- [ ] 修复已有 Skill/Rule/Agent
- [ ] 文档更新
- [ ] 重构（不影响功能）

## 测试情况

- [ ] 在真实场景中验证过
- [ ] 已在 SKILL-INDEX.md 中更新版本/状态
```

---

## Commit 规范

遵循 [约定式提交](https://www.conventionalcommits.org/zh-hans/)：

```
feat(skills): 新增 expert-bootstrap Skill，支持按需培养领域专家
fix(rules): session-bootstrap 阈值改为基于模式而非固定数量
docs(readme): 按规范重写中英文 README，补充双语和 Logo
```

---

## 版本号规范

遵循 [Semantic Versioning](https://semver.org/)：`vMAJOR.MINOR.PATCH`

- PATCH：Bug 修复、文档改进（v1.0.1）
- MINOR：新增 Skill/Rule/Agent（v1.1.0）
- MAJOR：不向后兼容的变更（v2.0.0）
