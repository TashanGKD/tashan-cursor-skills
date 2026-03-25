# [项目名] · Bug 修复记录

> **性质**：append-only（只追加，不修改历史记录）
> **维护者**：各开发角色（通过 bug-fix-tdd-guard Rule 约束写入）
> **目的**：作为所有 Bug 修复的 TDD 证据汇总，支持 Postmortem 和回归测试

---

## 修复记录模板（每次修复追加以下格式）

```markdown
## [TC-XXX] [Bug描述一句话] — Round N — YYYY-MM-DD

**优先级**：P0 / P1 / P2
**项目**：tashan-openbrain_v2 / [其他项目名]
**修复角色**：role-后端开发 / role-前端开发 / role-AI工程师

**根因（5 Whys 第1-2层）**：
[Bug 发生的根本原因，不是「某人写错了」而是「哪里的系统/流程没有防护」]

**修复内容**：
- 文件：[修改的文件路径]
- 改动：[一句话说明改了什么逻辑]

**TDD 证据**：
- 失败测试（Red）：`tests/xxx/test_yyy.py::test_fix_TC_XXX`
  → 修复前运行：❌ 失败（证明测试捕获了 Bug）
- 修复后运行：✅ 通过（Green）
- 全量 CI：✅ 通过（Layer 0: Xs, Layer 1: Xs）

**影响半径分析**：
- 直接影响：[修改的模块]
- 可能波及：[依赖此模块的其他地方]
- 验证范围：[哪些测试用例被重新跑]

**回归验证**：
- 针对性回归：✅ [测试用例ID]
- 全量回归：✅ / ⏳待下轮

**合并记录**：[commit hash 或 PR 描述]

**Postmortem 触发**：[是（P0）/ 否（P1/P2）]
```

---

## 示例

## [TC-001] 并发对话 session 串话 — Round 1 — 2026-03-24

**优先级**：P0
**项目**：tashan-openbrain_v2
**修复角色**：role-后端开发

**根因**：
ContextVar `_request_workspace` 在请求结束后没有被清理，导致相邻请求复用了上一次的 workspace 路径，多用户并发时出现串话。

**修复内容**：
- 文件：`backend/app/deps.py`
- 改动：在请求结束的 finally 块中添加 ContextVar 重置逻辑

**TDD 证据**：
- 失败测试（Red）：`tests/integration/test_concurrent_session.py::test_session_isolation_concurrent`
  → 修复前运行：❌ 失败（用户A的上下文出现在用户B的响应中）
- 修复后运行：✅ 通过（Green）
- 全量 CI：✅ 通过（Layer 0: 3s, Layer 1: 45s）

**影响半径分析**：
- 直接影响：所有 HTTP 请求的 workspace 注入
- 可能波及：/chat、/proxy/chat、/messages/* 路由
- 验证范围：并发测试组 + 路由测试组

**回归验证**：
- 针对性回归：✅ test_concurrent_session_isolation（新增）
- 全量回归：✅ Round 2 全量通过

**合并记录**：fix/TC-001-session-isolation

**Postmortem 触发**：是（P0）→ 见 内部总控/Postmortem-session串话-20260324.md
