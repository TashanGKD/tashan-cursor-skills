<!-- Logo -->
<p align="center">
  <a href="https://tashan.ac.cn" target="_blank" rel="noopener noreferrer">
    <img src="docs/assets/tashan.svg" alt="Tashan Logo" width="280" />
  </a>
</p>

<!-- Title -->
<p align="center">
  <strong>Tashan Cursor Skill System</strong><br>
  <em>Self-Evolving AI Execution Framework for Cursor</em>
</p>

<!-- Navigation -->
<p align="center">
  <a href="#overview">Overview</a> •
  <a href="#features">Features</a> •
  <a href="#quick-start">Quick Start</a> •
  <a href="#structure">Structure</a> •
  <a href="#ecosystem">Ecosystem</a> •
  <a href="#contributing">Contributing</a> •
  <a href="README.md">中文</a>
</p>

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Skills](https://img.shields.io/badge/Skills-95-blue)](#features)
[![Rules](https://img.shields.io/badge/Rules-32-green)](#features)
[![Agents](https://img.shields.io/badge/SubAgents-18-purple)](#features)

> A self-evolving AI execution framework for Cursor: 95 Skills, 32 Rules, 18 SubAgents — enabling AI to autonomously judge tasks, follow standards, and evolve from experience.

---

## Overview

This project provides the **Skill layer** of Tashan's "Human-Agent Digital World" ecosystem. It solves three fundamental problems in AI-assisted product development: AI starting from scratch every session, repeating past mistakes, and requiring users to manually specify every workflow step.

Without this system, AI relies purely on training knowledge — no standards, no accumulation, no evolution. With this system, AI has a complete framework for "how to do things," can autonomously identify task types, execute full workflows, and automatically convert lessons learned into updated standards.

**Core Ideas**

- **Self-Evolution**: Automatically capture failure signals (types A-G) during execution, identify root causes across multiple occurrences, update Skills/Rules, and avoid repeating mistakes
- **Three-Layer Architecture**: Rules (constraint guards) → Skills (step sequences) → SubAgents (independent perspective verification)
- **Universal Quality Loop**: Create → Verify independently (clean context) → Respond → Second review → Close — applicable to all quality assurance scenarios

**Who This Is For**

- Cursor AI developers and teams who want standardized development workflows
- AI engineers researching self-evolving agent systems
- Product managers and tech leads wanting AI coverage across design → architecture → development → testing → deployment
- Developers studying Cursor Skill system design principles

---

## Features

**Full Product Development Automation**
- **Automatic task classification**: Describe your need, AI identifies whether it's "new feature / bug fix / config change" and plans the execution sequence
- **Complete gate system**: Gate A (product spec review) → Gate B (architecture review) → Gate C (functional verification), each gate uses an independent perspective and cannot be bypassed
- **Bug fix loop**: Discover → TDD fix (write failing test first) → regression verification → tracker update, fully documented

**Self-Evolution Mechanism**
- **Signal A-G auto-capture**: 6 signal types (pitfall/blind spot/gap/insight/expectation mismatch/unexpected behavior/root cause) auto-routed after task completion
- **Pattern recognition**: Multiple similar signals trigger `project-retrospective` for batch Skill/Rule updates, solving root causes rather than patching symptoms
- **Three-question change protocol**: Before modifying any Skill/Rule/Agent, must answer: root cause / impact scope / verification method

**Document Management Automation**
- **Territory setup**: Each project role automatically creates/maintains the standard document structure when activated
- **Version tracking**: Project documents are automatically backed up before modification, with change records appended
- **Path resolution**: Resolves document paths from `project-config.md`, adapting to different project directory structures

**Knowledge Accumulation**
- **Fragment capture**: Insights during work are automatically recorded as cognitive fragments
- **Knowledge elevation**: Fragments integrate into L1 systematic documents, reusable across projects
- **Principle extraction**: Cross-domain patterns are distilled into foundational principles for all tasks

---

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/TashanGKD/tashan-cursor-skills.git
```

### 2. Copy to your project

```bash
# Full installation (recommended)
cp -r tashan-cursor-skills/skills/* your-project/.cursor/skills/
cp -r tashan-cursor-skills/rules/* your-project/.cursor/rules/
cp -r tashan-cursor-skills/agents/* your-project/.cursor/agents/
```

### 3. Restart Cursor

Close and reopen Cursor. All Skills and Rules take effect automatically.

### 4. Create project config (recommended)

Create `.cursor/project-config.md` in your project root:

```markdown
# Project Configuration

## Basic Info
Project name: [your project name]
Project path: [root directory path]

## Core Document Paths
Product docs: [project]/product-manager/
Architecture docs: [project]/architect/
Test docs: [project]/dev-plan/
```

### 5. Start using

Just describe your needs — AI automatically identifies the task type and executes:

```
"Build a user login feature"
→ AI auto-executes: Product design → Gate A review → Architecture → Gate B review → Development → Testing → Deployment

"Login API returning 500"
→ AI auto-executes: Issue classification → TDD fix → Regression → Tracker update
```

### Selective installation

When you only need specific Skills, copy at minimum the core routing Rules:

```bash
# Core routing Rules (required)
cp tashan-cursor-skills/rules/role-menu.mdc your-project/.cursor/rules/
cp tashan-cursor-skills/rules/session-bootstrap.mdc your-project/.cursor/rules/

# Add specific Skills as needed
cp -r tashan-cursor-skills/skills/role-产品经理 your-project/.cursor/skills/
cp -r tashan-cursor-skills/skills/role-技术架构师 your-project/.cursor/skills/
```

---

## Structure

```
tashan-cursor-skills/
├── README.md                    # Chinese documentation
├── README.en.md                 # English documentation (this file)
├── CHANGELOG.md                 # Version history
├── CONTRIBUTING.md              # Contribution guide
├── LICENSE                      # MIT License
├── docs/
│   ├── assets/
│   │   └── tashan.svg           # Tashan Logo
│   ├── overview.md              # Complete system documentation
│   ├── Skill体系设计原则_v1.0.md # Design philosophy (Chinese)
│   └── SYSTEM-BLUEPRINT.md     # System blueprint
├── skills/                      # 95 Skills (each with SKILL.md)
│   ├── role-产品开发协调者/     # Domain coordinator: task type identification
│   ├── role-产品经理/           # Product definition + development planning
│   ├── role-技术架构师/         # Technical architecture + API specs
│   ├── role-前端开发/           # React + TypeScript + Vite
│   ├── role-后端开发/           # Python + FastAPI + PostgreSQL
│   ├── role-AI工程师/           # Prompt design + Agent building
│   ├── role-测试工程师/         # Gate C: full verification
│   ├── role-DevOps/             # Deployment + operations
│   ├── role-审核者-用户模拟/    # Gate A: product spec review
│   ├── role-审核者-系统破坏/    # Gate B: architecture security review
│   ├── bug-fix-loop-coordinator/ # Bug fix loop
│   ├── issue-tracker/           # Issue classification and tracking
│   ├── project-backlog/         # Unified inbox for external feedback
│   ├── expert-bootstrap/        # On-demand domain expert Agent cultivation
│   ├── project-retrospective/   # Project retrospective + Skill evolution
│   ├── cognitive-*/             # Knowledge accumulation series
│   └── ...（full list in index/skill-index/SKILL-INDEX.md）
├── rules/                       # 32 Rules (.mdc files, alwaysApply)
│   ├── session-bootstrap.mdc    # ★ Core: session execution protocol
│   ├── role-menu.mdc            # ★ Core: trigger word routing table
│   ├── comprehensive-change-guard.mdc  # Multi-layer change ordering
│   ├── bug-fix-tdd-guard.mdc   # Enforce TDD for bug fixes
│   ├── test-coverage-guard.mdc # Test completion verification
│   ├── document-lifecycle-guard.mdc    # Document version management
│   ├── product-alignment-guard.mdc     # Fixes must align with product intent
│   └── ...（full list in rules/ directory）
├── agents/                      # 18 SubAgent definitions
│   ├── verifier.md              # Independent functional verification (readonly)
│   ├── fixer.md                 # TDD fix executor (writable)
│   ├── arch-destroyer.md        # Architecture destruction reviewer (readonly)
│   ├── user-simulator.md        # User perspective simulation (readonly)
│   ├── ai-evaluator.md          # AI output quality evaluator (readonly)
│   └── ...（full list in agents/ directory）
└── index/
    └── skill-index/
        ├── SKILL-INDEX.md       # Complete index of all Skills
        └── SYSTEM-BLUEPRINT.md  # System design blueprint
```

---

## Ecosystem

This project provides the AI execution standards layer for the Tashan ecosystem.

```
Tashan Ecosystem
│
├── Resonnet                    ← Multi-agent cognitive collaboration backend
│   └── tashan-openbrain        ← Cognitive twin application (powered by Resonnet)
│
├── Tashan-TopicLab             ← Multi-expert roundtable discussion platform
│
├── tashan-cursor-skills ★     ← This repo: AI execution standards (Skill/Rule/Agent)
│   └── Provides AI execution standards for all product development
│
└── world-axiom-framework       ← Axiomatic framework for Human-Agent Digital Worlds
```

### Related Repositories

| Repository | Role | Link |
|-----------|------|------|
| Resonnet | Multi-agent cognitive collaboration backend | [TashanGKD/Resonnet](https://github.com/TashanGKD/Resonnet) |
| Tashan-TopicLab | Multi-expert roundtable discussion platform | [TashanGKD/Tashan-TopicLab](https://github.com/TashanGKD/Tashan-TopicLab) |
| world-axiom-framework | Axiomatic framework for digital worlds | [TashanGKD/world-axiom-framework](https://github.com/TashanGKD/world-axiom-framework) |
| tashan-cursor-skills | This repo (AI execution standards) | Current page |

---

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

- **New Skill**: Follow [design principles](docs/Skill体系设计原则_v1.0.md) and register in `index/skill-index/SKILL-INDEX.md`
- **Modifying Skill/Rule/Agent**: Must read `skills/skill-rule-修改规范/SKILL.md` and follow the three-question protocol (root cause / impact / verification)
- **Documentation**: Improvements to README or `docs/` are welcome

---

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

---

## License

MIT License. See [LICENSE](LICENSE) for details.
