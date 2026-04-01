#!/usr/bin/env bash
# 将他山 Cursor Skill 体系作为「合集 Skill」发布到他山世界（TopicLab Skill 专区）
# 依赖：topiclab-cli（npm i -g topiclab-cli）
# 规范：topiclab-world-openclaw — CLI 优先，不臆造 API
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CONTENT_FILE="${ROOT}/docs/world-publish/tashan-cursor-skills-bundle.SKILL.md"

BASE_URL="${TOPICLAB_BASE_URL:-https://world.tashan.chat}"
BIND_KEY="${TOPICLAB_BIND_KEY:-}"

if [[ -z "${BIND_KEY}" ]]; then
  echo "请设置环境变量 TOPICLAB_BIND_KEY（他山世界绑定密钥，勿提交到公开仓库）。" >&2
  echo "示例：export TOPICLAB_BIND_KEY='tlos_xxx'" >&2
  exit 1
fi

if ! command -v topiclab &>/dev/null; then
  echo "未找到 topiclab，请先安装: npm install -g topiclab-cli" >&2
  exit 1
fi

if [[ ! -f "${CONTENT_FILE}" ]]; then
  echo "缺少内容文件: ${CONTENT_FILE}" >&2
  exit 1
fi

echo "==> session ensure"
topiclab session ensure --base-url "${BASE_URL}" --bind-key "${BIND_KEY}" --json

echo "==> notifications（心跳：优先续接已有线程）"
topiclab notifications list --json || true

echo "==> skills publish（合集入口）"
# --category：若 API 报错，请 topiclab help ask \"skills publish category 合法取值\" --json 后改此处
topiclab skills publish \
  --name "他山 Cursor Skill 体系" \
  --summary "95 Skills + 32 Rules + 18 SubAgents，全链路 Self-Evolving Agent Harness，支持 npx 一键安装" \
  --description "开源合集：产品开发、认知积累、质量关卡、Skill 自进化。安装见正文；源码 https://github.com/TashanGKD/tashan-cursor-skills" \
  --category "development" \
  --cluster "general" \
  --framework "openclaw" \
  --slug "tashan-cursor-skills" \
  --tags "cursor,openclaw,skills,rules,agents,harness,tashan" \
  --source-url "https://github.com/TashanGKD/tashan-cursor-skills" \
  --source-name "TashanGKD/tashan-cursor-skills" \
  --docs-url "https://github.com/TashanGKD/tashan-cursor-skills#readme" \
  --license "MIT" \
  --install-command "npx ai-agent-skills install TashanGKD/tashan-cursor-skills" \
  --version "0.1.0" \
  --changelog "初始发布：合集入口 SKILL + 安装说明" \
  --content-file "${CONTENT_FILE}" \
  --json

echo "==> 完成。请到 Skill 专区核对条目；若 category 被拒绝，按 CLI 提示修改脚本中的 --category 后重试。"
