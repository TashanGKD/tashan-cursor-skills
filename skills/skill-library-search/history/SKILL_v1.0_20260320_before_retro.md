---
name: skill-library-search
description: 全量搜索外部 Skill/Agent/Rule 仓库，必须执行7维度协议，禁止以少于7维度的搜索声称「全量完成」。触发词：「全量搜索 skill 库」「搜索 GitHub skill 仓库」「找所有 skill 库」「有没有遗漏的 skill 仓库」「更新 skill 参考库」。
---

# Skill 库全量搜索 Skill

> **本 Skill 存在的原因**：2026-03-20 真实事故——AI 仅执行3-4条泛化查询便声称「全量搜索完成」，遗漏了 antfu/skills(⭐4K)、alirezarezvani/claude-skills(⭐5.9K)、mattpocock/skills(⭐4.7K) 等重要仓库。
>
> **核心约束**：未执行全部7个维度，禁止使用「全量」「完整」「没有遗漏」等措辞。

---

## ⚠️ 强制前置声明

执行搜索前，必须声明：
「本次搜索将按 7 维度协议执行，完成全部维度前不声称全量完成。」

---

## 7 维度搜索协议（全部必须执行，缺一不可）

### Dimension 1：官方组织仓库

```
搜索词：github "[platform] skills" official repository 2026
必检查清单（每次都要逐一确认）：
  □ openai/skills
  □ agentskills/agentskills（Anthropic 规范）
  □ vercel-labs/agent-skills
  □ huggingface/skills
  □ microsoft/skills
  □ cloudflare/skills
  □ google-gemini/gemini-skills
```

### Dimension 2：知名开发者个人仓库

```
搜索词：[developer] skills github SKILL.md
必检查清单（每次都要逐一确认）：
  □ antfu/skills（Vue/Vite 生态核心维护者）
  □ mattpocock/skills（TypeScript 教育者，Total TypeScript）
  □ 其他高关注度全栈/工具链开发者
原则：不能只搜「skill library」，知名开发者个人库必须单独检查
```

### Dimension 3：Claude Code 专项搜索

```
搜索词：github "claude code" skills repository stars 2026
搜索词：github "claude-skills" OR "claude-code-skills" stars
必检查：
  □ alirezarezvani/claude-skills（⭐5.9K）
  □ karanb192/awesome-claude-skills
```

### Dimension 4：其他平台专项搜索

```
搜索词：github codex skills SKILL.md repository 2026
搜索词：github gemini skills SKILL.md 2026
搜索词：github cursor skills SKILL.md 2026
```

### Dimension 5：GitHub Topic 直接访问

```
直接搜索以下 topic（不能依赖 AI 摘要，必须搜索）：
  □ "agent-skills" topic：搜索词 github topic:agent-skills
  □ "claude-code" topic：搜索词 github topic:claude-code
  □ "codex-skills" topic：搜索词 github topic:codex-skills
记录每个 topic 下 ⭐100 以上的仓库
```

### Dimension 6：已有仓库的 README 交叉引用

```
检查已克隆仓库的 README 中引用的外部仓库：
  □ 检查 VoltAgent/awesome-agent-skills 的引用列表
  □ 检查 heilcheng/awesome-agent-skills 的引用列表
  □ 检查 philipbankier/awesome-agent-skills 的引用列表
原则：策划列表（awesome lists）往往包含搜索引擎找不到的高质量仓库
```

### Dimension 7：验证步骤（防漏）

```
在声称「全量完成」之前，必须执行：
  □ 搜索词：most starred github SKILL.md agent skills 2026
  □ 搜索词：best agent skills github repository list 2026
  □ 对比当前索引与搜索结果，确认无新发现
  □ 明确输出：「已执行全部7个维度，当前已知 N 个仓库，可能仍有未知遗漏」
```

---

## 数据完整性规则（R2 补丁）

> 对应 `knowledge-integrity-rules.mdc` 的 R2 NO_FABRICATION

1. **引用数字必须有对应实物**：任何分类统计数字（如"806个自动化技能"），必须来自已克隆到本地的仓库。不得引用"搜索摘要里提到的数字"
2. **先克隆，后引用**：发现仓库有用数据，必须先克隆到 `_global-skill-library/_sources/`，再引用其数据
3. **声明来源**：所有数字需标注来源，如「806个（来自 christophacham--agent-skills-library/skills/automation/）」

---

## 搜索结果处理

每发现一个新仓库，执行：
1. 确认仓库真实存在（直接访问 GitHub URL，不凭摘要）
2. `git clone --depth 1 [url] _global-skill-library/_sources/[org]--[repo]`
3. 统计实际 SKILL.md 数量（不依赖文档声称的数量）
4. 更新 `_global-skill-library/_index.md` 和 `README.md`

---

## 完成标准

只有满足以下全部条件，才可声称「全量搜索完成」：

- [ ] 7个维度全部执行，每个维度的检查清单逐项打勾
- [ ] 所有引用的数字均来自已克隆的本地文件
- [ ] 声明：「本次搜索已执行7维度协议，当前已知 [N] 个仓库。受限于搜索引擎覆盖度，仍可能存在未知遗漏，这是已知局限性。」

---

## 变更记录

### 2026-03-20 — 初始创建

**根因**：2026-03-20 真实事故——AI仅执行3-4条泛化查询就声称「全量搜索完成」，遗漏3个高星仓库（antfu/mattpocock/alirezarezvani）。原本将协议写在 `_global-skill-library/全量搜索协议.md` 里，但该文件是参考文档而非可执行约束，不能强制 AI 遵守。本 Skill 将协议提升为可执行层，并在 role-menu 强制规则中注册。

**验证结果**：
- 正向验证：下次执行「全量搜索 skill 库」时，AI 应加载本 Skill，声明7维度并逐一执行（🔵 待验证）
- 负向验证：普通搜索（如"帮我查 React 文档"）不触发本 Skill（🔵 待验证）
