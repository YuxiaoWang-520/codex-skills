<div align="right">

[![Language: English](https://img.shields.io/badge/Language-English-0A66C2)](./README_EN.md)
[![Language: 简体中文](https://img.shields.io/badge/语言-简体中文-2EA44F)](./README.md)

</div>

# Harness Craft

The craft of harnessing AI coding agents. Skills (on-demand playbooks) + Rules (always-on guardrails) = a stronger, more controllable AI engineering partner.

## Overview

- Goal: standardize reusable skills and rules to reduce repeated context setup and enforce engineering best practices out of the box.
- Scale: **41** skills + **15** rules (10 common + 5 Python-specific).
- Audience: AI builders, automation engineers, research/content teams, open-source maintainers.

## Skills vs Rules

| | Skills | Rules |
|--|--------|-------|
| **Analogy** | Playbook | Constitution |
| **Loading** | On-demand via `/skill-name` | Auto-injected every session |
| **Context cost** | Full text loaded only when invoked | Always loaded (but each is short) |
| **Best for** | Long workflows (TDD, E2E, deep research...) | Short global constraints (coding style, security, git...) |
| **Activation** | User-triggered | Auto-enforced every turn |

**In short**: Rules are the agent's instincts. Skills are the agent's learned expertise.

## Repository Structure

```text
skills/
  .system/
    skill-creator/
    skill-installer/
  <skill-name>/
    SKILL.md              # required: trigger and workflow
    agents/openai.yaml    # optional: UI metadata
    scripts/              # optional: executable helpers
    references/           # optional: load-on-demand docs
    assets/               # optional: templates/assets

rules/
  common/                 # Language-agnostic rules (always active)
    coding-style.md         # Immutability, file org, functions <50 lines
    security.md             # Pre-commit security checklist
    testing.md              # TDD workflow, coverage >=80%
    git-workflow.md         # Commit format, PR standards
    code-review.md          # Review standards, severity levels, merge blocking
    development-workflow.md # Full dev flow: search -> plan -> TDD -> review -> commit
    patterns.md             # Design patterns, skeleton project reuse
    performance.md          # Model selection, context management
    agents.md               # Sub-agent auto-dispatch strategy
    hooks.md                # Hook system and TodoWrite practices
  python/                 # Python-specific rules (only for .py/.pyi files)
    coding-style.md         # PEP 8, type annotations, frozen dataclass
    patterns.md             # Protocol, dataclass DTO, context manager
    security.md             # Env var management, bandit scanning
    testing.md              # pytest, coverage, mark categorization
    hooks.md                # Python project hook integration
```

## How To Use

### Skills

1. Define the target output clearly (code, docs, report, PR, release).
2. Pick the minimum 1-3 skills that fully cover the task.
3. Read `SKILL.md` first; only load `references/` when needed.
4. Prefer bundled `scripts/` over ad-hoc one-off implementation.
5. Finish with explicit verification and a short execution summary.

### Rules

Rules are **zero-config** after installation — they take effect automatically every session:

```bash
# Install at user level (applies to all projects)
mkdir -p ~/.claude/rules
cp -r rules/common ~/.claude/rules/
cp -r rules/python ~/.claude/rules/   # pick your language

# Or install at project level (applies to current project only)
mkdir -p .claude/rules
cp -r rules/common .claude/rules/
```

Once installed, the AI agent will automatically:
- Use `feat:/fix:/refactor:` format for commit messages
- Check for hardcoded secrets, SQL injection, XSS before every commit
- Follow immutable data patterns, functions <50 lines
- Add type annotations and use frozen dataclass for Python files
- Proactively trigger code review after writing code

## Skill Trigger Rules

- Explicit trigger: user names the skill directly (e.g. `$openai-docs`).
- Semantic trigger: user intent strongly matches skill `description`.
- Multi-skill sequencing: research/input -> implementation/output -> verification/delivery.

## Recommended Workflow

1. Context bootstrapping: `repo-codex-bootstrap` + `strategic-compact`
2. Design and implementation: `api-design` / `backend-patterns` / `frontend-patterns`
3. Quality and validation: `tdd-workflow` + `e2e-testing` + `verification-loop`
4. Delivery and collaboration: `gh-address-comments` / `gh-fix-ci` / `yeet`

## Star Rating (Priority Signals)

- `⭐⭐ Core`: foundational skills recommended for most multi-step engineering sessions.
- `⭐ Common`: high-frequency skills that work well across many repositories and workflows.
- No star: specialized skills for narrower task contexts.

### Starred Skills Quick Picks

- `⭐⭐ repo-codex-bootstrap`: baseline context/memory system for cross-session work.
- `⭐⭐ codex-longrun-dev`: stable execution model for long-horizon autonomous development.
- `⭐ backend-patterns`, `⭐ frontend-patterns`, `⭐ coding-standards`, `⭐ security-review`
- `⭐ api-design`, `⭐ tdd-workflow`, `⭐ verification-loop`, `⭐ playwright`
- `⭐ deep-research`, `⭐ openai-docs`, `⭐ article-writing`
- `⭐ gh-address-comments`, `⭐ gh-fix-ci`

## Rules Reference

> Rules take effect automatically after installation. No manual invocation needed.

### Common Rules (all languages)

| Rule | What it enforces |
|------|-----------------|
| `coding-style` | Immutable data patterns; functions <50 lines, files <800 lines, nesting <4 levels |
| `security` | Pre-commit checks: no hardcoded secrets, parameterized SQL, XSS/CSRF protection |
| `testing` | TDD (write tests first); coverage >=80% |
| `git-workflow` | Commit format `<type>: <description>`; PR analyzes full commit history |
| `code-review` | Auto-review after writing code; CRITICAL issues block merge |
| `development-workflow` | Dev flow: search existing solutions -> plan -> TDD -> review -> commit |
| `patterns` | Search for battle-tested skeletons first; Repository Pattern recommended |
| `performance` | Model selection (Haiku for cost / Sonnet for daily / Opus for architecture) |
| `agents` | Auto-dispatch sub-agents: complex features -> planner, code written -> code-reviewer |
| `hooks` | TodoWrite best practices, permission control guide |

### Python Rules (`.py`/`.pyi` files only)

| Rule | What it enforces |
|------|-----------------|
| `coding-style` | PEP 8; type annotations required; `frozen=True` dataclass |
| `patterns` | Protocol duck typing, dataclass DTO, context manager, generator |
| `security` | `os.environ["KEY"]` strict access; bandit static scanning |
| `testing` | pytest + `--cov`; `pytest.mark.unit/integration` categorization |
| `hooks` | Python project hook integration guide |

## Full Skill Reference

> Columns:
> - Purpose: what problem it solves
> - Best timing: when to trigger
> - Recommendation: practical usage advice

### 1) System Skills

| Skill | Purpose | Best timing | Recommendation |
|---|---|---|---|
| `skill-creator` | Create/update skills with consistent structure | Designing a new reusable workflow | Keep `SKILL.md` concise; move details to `references/` |
| `skill-installer` | Install skills from curated list or GitHub | New setup, migration, team sync | Run a smoke test right after installation |

### 2) Engineering & Quality

| Skill | Purpose | Best timing | Recommendation |
|---|---|---|---|
| `⭐ api-design` | Production REST API design patterns | New API or interface refactor | Define resource/error model before endpoints |
| `⭐ backend-patterns` | Backend architecture/performance patterns | Service evolution or performance bottlenecks | Pair with `security-review` early |
| `⭐ frontend-patterns` | Frontend architecture/state/performance patterns | Complex UI state and rendering issues | Design state boundaries first |
| `⭐ coding-standards` | Unified coding standards for JS/TS/React/Node | Team style drift, unstable review quality | Enforce with lint/test gates |
| `⭐ security-review` | Security checklist for sensitive changes | Auth, payments, secrets, untrusted input | Start with threat modeling |
| `⭐ tdd-workflow` | Test-driven development workflow | New features, bug fixes, risky refactors | Write failing tests first |
| `e2e-testing` | Playwright E2E testing patterns | Critical user flow regressions | Prioritize high-value paths |
| `⭐ verification-loop` | End-to-end verification discipline | Multi-module changes before delivery | Use explicit check/test/manual chain |
| `eval-harness` | Eval-driven development framework | Quantitative agent/model evaluation | Freeze metrics and dataset first |
| `⭐⭐ codex-longrun-dev` | Long-horizon autonomous development | Multi-session, long-running tasks | Keep one-feature-per-session cadence |
| `dmux-workflows` | Multi-agent orchestration via dmux/tmux | Parallelizable complex tasks | Assign disjoint ownership upfront |
| `⭐⭐ repo-codex-bootstrap` | Initialize and maintain `codex/` docs | New repo or context-loss risk | Always read/update `memory.md` and `prompt.md` |
| `strategic-compact` | Manual context compaction strategy | Long tasks near context limits | Compact by milestones, not fixed intervals |

### 3) Frontend, Design & Automation

| Skill | Purpose | Best timing | Recommendation |
|---|---|---|---|
| `figma` | Pull context/assets from Figma MCP | Figma-linked implementation tasks | Fetch tokens/variables before coding |
| `figma-implement-design` | 1:1 design-to-code implementation | Pixel-fidelity requirements | Map Figma tokens to project tokens |
| `⭐ playwright` | Real-browser automation from terminal | UI debugging, extraction, scripted flows | Script replayable steps with waits |
| `develop-web-game` | Iterative web-game dev + testing loop | HTML/JS game iteration | Change one mechanic per cycle |
| `frontend-slides` | Rich HTML slides / PPT-to-web conversion | Talks, demos, pitch decks | Lock narrative structure first |
| `screenshot` | OS-level screenshot capture | Full screen/window/region capture needs | Confirm target display/window before capture |

### 4) Research, Docs & Knowledge

| Skill | Purpose | Best timing | Recommendation |
|---|---|---|---|
| `⭐ deep-research` | Multi-source cited deep research | Evidence-heavy analysis tasks | Narrow questions before broad crawl |
| `market-research` | Market/competitor/investor diligence research | Go-to-market or fundraising decisions | Tie outputs to concrete decisions |
| `paper-deep-review` | Structured paper dissection | Fast but rigorous paper understanding | Start from problem and contribution |
| `⭐ openai-docs` | Official OpenAI docs lookup and citation | OpenAI API/features/limits questions | Prefer official sources only |
| `exa-search` | Exa neural web/code/company search | Fast high-relevance retrieval | Validate results before synthesis |
| `⭐ article-writing` | Long-form writing with voice consistency | Articles, tutorials, newsletters, guides | Define audience and tone examples first |
| `doc` | `.docx` authoring/editing with layout checks | Word output with formatting requirements | Validate visual output after generation |
| `pdf` | PDF extraction/generation/review workflow | Reports, contracts, paper PDFs | Separate text extraction from layout QA |

### 5) GitHub, Project Ops & Delivery

| Skill | Purpose | Best timing | Recommendation |
|---|---|---|---|
| `⭐ gh-address-comments` | Resolve PR review/issue comments via `gh` | Comment-driven revision cycles | Triage comments before implementing |
| `⭐ gh-fix-ci` | Diagnose and fix failing GitHub Actions checks | Red CI in PR workflow | Reproduce minimally before patching |
| `yeet` | Stage/commit/push/open PR in one flow | Explicit user request for one-click release | Use only with explicit authorization |
| `linear` | Linear issue/project management workflows | Planning and team coordination | Keep acceptance criteria explicit |

### 6) Content, Media & Growth

| Skill | Purpose | Best timing | Recommendation |
|---|---|---|---|
| `content-engine` | Platform-native content system design | Multi-platform content operations | Define content pillars before adaptation |
| `crosspost` | Channel-specific cross-post adaptation | One idea distributed across platforms | Keep core message, rewrite format/style |
| `video-editing` | AI-assisted video editing pipeline | Vlogs, product videos, short-form batches | Prioritize narrative clarity over effects |
| `fal-ai-media` | Unified image/video/audio generation via fal.ai | Fast media asset generation | Tune prompts/params on small samples first |
| `x-api` | X/Twitter API integration patterns | Programmatic posting/search/analytics | Handle OAuth and rate limits strictly |

### 7) Business & Fundraising

| Skill | Purpose | Best timing | Recommendation |
|---|---|---|---|
| `investor-materials` | Build and maintain fundraising materials | Deck/memo/model preparation | Keep one source of truth for metrics |
| `investor-outreach` | Investor outreach copywriting | Cold emails, intros, follow-ups, updates | Personalize first lines by investor profile |

### 8) Platform Integrations

| Skill | Purpose | Best timing | Recommendation |
|---|---|---|---|
| `claude-api` | Claude API integration patterns | Building Claude-powered apps | Decide call mode before tool orchestration |

## Inventory

**Skills (A-Z):** `api-design`, `article-writing`, `backend-patterns`, `claude-api`, `codex-longrun-dev`, `coding-standards`, `content-engine`, `crosspost`, `deep-research`, `develop-web-game`, `dmux-workflows`, `doc`, `e2e-testing`, `eval-harness`, `exa-search`, `fal-ai-media`, `figma`, `figma-implement-design`, `frontend-patterns`, `frontend-slides`, `gh-address-comments`, `gh-fix-ci`, `investor-materials`, `investor-outreach`, `linear`, `market-research`, `openai-docs`, `paper-deep-review`, `pdf`, `playwright`, `repo-codex-bootstrap`, `screenshot`, `security-review`, `skill-creator`, `skill-installer`, `strategic-compact`, `tdd-workflow`, `verification-loop`, `video-editing`, `x-api`, `yeet`.

**Rules:** `common/coding-style`, `common/security`, `common/testing`, `common/git-workflow`, `common/code-review`, `common/development-workflow`, `common/patterns`, `common/performance`, `common/agents`, `common/hooks`, `python/coding-style`, `python/patterns`, `python/security`, `python/testing`, `python/hooks`.

## Maintenance Guidelines

- Every skill directory must include `SKILL.md`.
- Keep `name` aligned with folder name; keep `description` trigger-oriented.
- Rules should stay short (10-50 lines each); move long workflows to skills.
- Ensure executable bits for runnable scripts when needed.
- Update skills/rules when external APIs/platform rules change.
- Record major changes in PR descriptions for auditability.

## Contributing

Issues and PRs are welcome. Before submitting, please ensure:

1. Trigger conditions are clear and reusable.
2. `SKILL.md` matches scripts/references behavior.
3. Rules follow the "short + global constraint" principle — no detailed workflows.
4. Boundary conditions and fallback behavior are documented.
