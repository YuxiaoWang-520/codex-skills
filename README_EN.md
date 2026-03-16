<div align="right">

[![Language: English](https://img.shields.io/badge/Language-English-0A66C2)](./README_EN.md)
[![Language: 简体中文](https://img.shields.io/badge/语言-简体中文-2EA44F)](./README.md)

</div>

# Codex Skills

An open-source repository of reusable Codex skills. Each skill is a task capability unit with trigger conditions, execution workflow, references, and optional scripts.

## Overview

- Goal: standardize reusable workflows and reduce repeated context setup.
- Scale: **41** skills (including 2 system skills under `.system`).
- Audience: AI builders, automation engineers, research/content teams, open-source maintainers.

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
```

## How To Use

1. Define the target output clearly (code, docs, report, PR, release).
2. Pick the minimum 1-3 skills that fully cover the task.
3. Read `SKILL.md` first; only load `references/` when needed.
4. Prefer bundled `scripts/` over ad-hoc one-off implementation.
5. Finish with explicit verification and a short execution summary.

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

## Skill Inventory (A-Z)

`api-design`, `article-writing`, `backend-patterns`, `claude-api`, `codex-longrun-dev`, `coding-standards`, `content-engine`, `crosspost`, `deep-research`, `develop-web-game`, `dmux-workflows`, `doc`, `e2e-testing`, `eval-harness`, `exa-search`, `fal-ai-media`, `figma`, `figma-implement-design`, `frontend-patterns`, `frontend-slides`, `gh-address-comments`, `gh-fix-ci`, `investor-materials`, `investor-outreach`, `linear`, `market-research`, `openai-docs`, `paper-deep-review`, `pdf`, `playwright`, `repo-codex-bootstrap`, `screenshot`, `security-review`, `skill-creator`, `skill-installer`, `strategic-compact`, `tdd-workflow`, `verification-loop`, `video-editing`, `x-api`, `yeet`.

## Maintenance Guidelines

- Every skill directory must include `SKILL.md`.
- Keep `name` aligned with folder name; keep `description` trigger-oriented.
- Ensure executable bits for runnable scripts when needed.
- Update skills when external APIs/platform rules change.
- Record major changes in PR descriptions for auditability.

## Contributing

Issues and PRs are welcome. Before submitting, please ensure:

1. Trigger conditions are clear and reusable.
2. `SKILL.md` matches scripts/references behavior.
3. Boundary conditions and fallback behavior are documented.
