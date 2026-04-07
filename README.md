<div align="right">

[![Language: English](https://img.shields.io/badge/Language-English-0A66C2)](./README.md)
[![语言: 简体中文](https://img.shields.io/badge/语言-简体中文-2EA44F)](./README_CN.md)

</div>

<div align="center">

# Harness Craft

**Turn agentic coding from a one-off prompt trick into a durable engineering system.**

[![Skills](https://img.shields.io/badge/Skills-46-111111)](./skills)
[![Rules](https://img.shields.io/badge/Rules-15-8B5CF6)](./rules)
[![Flagship](https://img.shields.io/badge/Flagship-4%20Core%20Skills-0A66C2)](#the-4-flagship-skills)
[![Focus](https://img.shields.io/badge/Focus-Persistent%20·%20Verifiable%20·%20Recoverable%20·%20Learnable-2EA44F)](#core-idea)
[![Open Source](https://img.shields.io/badge/Open%20Source-Community%20Ready-F97316)](#contributing)

</div>

---

This repository is built around a simple belief:

> The biggest failure mode in agent-driven development is not intelligence — it is **system instability**.

Most teams don't get blocked because the model "can't write code". They get blocked because:

- the agent understood the repo yesterday and acts like it has amnesia today
- multiple agents look busy, but their changes collide and review quality is weak
- plans, validation status, and handoff context live only inside chat transcripts
- the agent feels done, while the repository is still not in a deliverable state

These are not prompt problems. They are **engineering system problems**.

## Contents

- [Core Idea](#core-idea)
- [Quick Start](#quick-start)
- [The 4 Flagship Skills](#the-4-flagship-skills)
- [How the Stack Fits Together](#how-the-stack-fits-together)
- [Skills vs Rules](#skills-vs-rules)
- [Rules Reference](#rules-reference)
- [Full Skill Inventory](#full-skill-inventory)
- [Who This Is For](#who-this-is-for)
- [Contributing](#contributing)

## Core Idea

The goal is not to add one more clever prompt. The goal is to upgrade agent work into a system that is:

- **Persistent** — repo knowledge survives context-window loss
- **Verifiable** — progress is tied to evidence, not model confidence
- **Collaborative** — multiple agents work with clear boundaries
- **Recoverable** — long tasks resume from stable state, not vague memory
- **Learnable** — agents accumulate knowledge from interactions and get smarter over time

### Prompt Tricks vs. Engineering Systems

| Prompt-First Workflow | System-First Workflow |
| --- | --- |
| Context lives in chat history | Context is written to repo-local artifacts |
| Completion is based on model confidence | Completion is based on evidence and checks |
| Multi-agent work is ad hoc | Roles, ownership, and review gates are explicit |
| Long tasks drift across sessions | Long tasks resume from structured state |
| Handoffs are fragile | Handoffs are built into the workflow |

## Quick Start

### Install Skills

<details>
<summary><strong>Claude Code</strong></summary>

```bash
# Install the 4 flagship skills
mkdir -p ~/.claude/skills
cp -R skills/repo-bootstrap ~/.claude/skills/
cp -R skills/longrun-dev ~/.claude/skills/
cp -R skills/learn ~/.claude/skills/
cp -R skills/agent-team-dev ~/.claude/skills/

# Or install the full collection
cp -R skills/* ~/.claude/skills/
```

Expected structure:

```text
~/.claude/skills/
  repo-bootstrap/
  longrun-dev/
  learn/
  agent-team-dev/
  ...
```

</details>

<details>
<summary><strong>Codex (OpenAI)</strong></summary>

```bash
# Install the 4 flagship skills
mkdir -p ~/.codex/skills
cp -R skills/repo-bootstrap ~/.codex/skills/
cp -R skills/longrun-dev ~/.codex/skills/
cp -R skills/learn ~/.codex/skills/
cp -R skills/agent-team-dev ~/.codex/skills/

# Or install the full collection
cp -R skills/* ~/.codex/skills/
```

Expected structure:

```text
~/.codex/skills/
  repo-bootstrap/
  longrun-dev/
  learn/
  agent-team-dev/
  ...
```

</details>

### Install Rules (Always-On Guardrails)

Rules are auto-injected into every session — no manual invocation needed.

```bash
# User-level (applies to all projects)
mkdir -p ~/.claude/rules
cp -r rules/common ~/.claude/rules/
cp -r rules/python ~/.claude/rules/   # pick your language

# Or project-level (current project only)
mkdir -p .claude/rules
cp -r rules/common .claude/rules/
```

Once installed, the AI agent will automatically:
- use `feat:`/`fix:`/`refactor:` commit format
- check for hardcoded secrets, SQL injection, XSS before every commit
- enforce immutable patterns, functions <50 lines, coverage ≥80%
- add type annotations and frozen dataclass for Python files
- trigger code review proactively after writing code
- load and apply learned knowledge from previous sessions

## The 4 Flagship Skills

If you only try four things from this repo, start here:

| Skill | Layer | Core Problem | Design Lever | Typical Outputs |
| --- | --- | --- | --- | --- |
| `repo-bootstrap` | Context | Repo knowledge gets lost between sessions | Split understanding into durable documents | `.harness/state.json`, `memory.md`, `prompt.md`, `repowiki.md`, `plan.md`, `checklist.md` |
| `longrun-dev` | Execution | Long tasks drift, lose focus, or declare done too early | Stateful harness with evidence-backed completion | `.longrun/init.sh`, `feature_list.json`, `progress.md`, `session_state.json` |
| `agent-team-dev` | Collaboration | Multi-agent work collides without governance | Compact engineering team with explicit ownership | task contract, role packets, `A1/I1/T1/R1` artifacts |
| `learn` | Knowledge | Valuable knowledge from interactions gets lost between sessions | Structured extraction with strength-based evolution | `~/.claude/learned/`, knowledge files with `weak→medium→strong` progression |

---

### `repo-bootstrap`

**Protects context.** The real power of this skill is not generating a few documents — it turns repo understanding from hidden background knowledge into an explicit, persistent workspace.

#### What problem it actually solves

An agent needs more than source code to work effectively. It also needs to know:

- What the user is actually trying to achieve
- What decisions have already been made
- How the repo is actually built, tested, and deployed
- What is still unknown or uncertain
- Whether the current plan still matches execution reality

When this information lives only in chat history, it is extremely fragile. One session switch, one parallel thread, one agent handoff — and facts mix with assumptions.

#### Architecture

This skill splits repo cognition into six durable artifacts:

- `.harness/state.json`: machine-readable single source of truth
- `.harness/memory.md`: ongoing working memory
- `.harness/prompt.md`: user intent, constraints, explanation history
- `.harness/repowiki.md`: repo facts — directories, commands, environment
- `.harness/plan.md`: design approach, assumptions, risks, validation paths
- `.harness/checklist.md`: real execution ledger — file changes, validation status

These responsibilities must stay separated:

| File | What it owns | Why it can't be merged |
| --- | --- | --- |
| `memory.md` | Ongoing working memory | Mixed with repo facts, it becomes an unstructured diary |
| `prompt.md` | User intent and constraints | Task semantics shouldn't couple with repo structure |
| `repowiki.md` | Repo operations, directories, commands | Long-term facts shouldn't be polluted by session noise |
| `plan.md` | Design approach, risks, validation paths | Future actions are not the same as past execution |
| `checklist.md` | Execution ledger, verification status | Real progress shouldn't be rewritten into design prose |

#### Why this design is strong

1. It doesn't pretend automation can replace understanding. Scripts can auto-detect languages, frameworks, commands, config files and directory structure — but that automation only builds the skeleton. It doesn't claim to provide deep understanding.

2. It treats update rules as governance, not suggestions. `memory.md` and `prompt.md` should be updated every session; repo fact changes must be reflected in `repowiki.md`; non-trivial implementations must sync `plan.md` and `checklist.md`.

3. It manages unknowns explicitly. A mature memory system records not only what is known, but also what is still unknown, how to discover it, and what should not be assumed by default.

This makes the system more honest, and much easier to hand off.

---

### `longrun-dev`

**Keeps long tasks on track.** Most agent demos excel at showing how work *starts*. The real difficulty is controlling how work *continues*.

#### Why long tasks fail most often

Once a task spans many sessions, highly predictable failure modes emerge:

- The agent doesn't know where it left off last time
- The baseline is already broken, but it keeps building on top of the damage
- Feature scope drifts silently across rounds
- Progress is narrative only — no structure
- The model *feels* done, but the system has zero completion evidence

These problems can't be solved by adding another paragraph that says "please work carefully." They require state files, recovery entry points, execution order, completion criteria, and scope throttling.

#### Architecture

This skill generates a longrun harness inside the target repo:

- `.longrun/init.sh`: dependency setup and smoke checks
- `.longrun/feature_list.json`: feature definitions with pass/fail status
- `.longrun/progress.md`: append-only session progress log
- `.longrun/session_state.json`: current recovery state and session info

The most important point: **long-task state becomes a repo asset, not a conversation asset.**

#### Control model

| Constraint | Design intent | What it prevents |
| --- | --- | --- |
| One feature per session | Limit scope expansion | Doing too much, drifting, "while I'm here" creep |
| Run `init.sh` first | Restore health before new work | Building on a broken baseline |
| `feature_list.json` status-only updates | Freeze feature definitions | Quietly rewriting the target mid-flight |
| `progress.md` append-only | Preserve traceable history | Overwriting history, making handoff impossible |
| Evidence required for completion | Turn "feels done" into "verified done" | Premature completion based on model confidence |

#### Why it embodies real "systems thinking"

The most powerful idea in this skill is not complexity — it is restraint.

"One feature per session" looks simple, but it is one of the highest-leverage control points for agents. The most common advanced failure mode is not that agents *can't* do the work — it's that they do too much, too broadly, beyond the original task boundary.

This skill cuts long-horizon tasks into a series of verifiable, recoverable, accountable units. At the end of each session, the system can re-evaluate:

- Is the baseline healthy?
- Is the scope stable?
- Is the evidence sufficient?

This is the kind of engineering constraint that long-running autonomous development actually needs.

---

### `agent-team-dev`

**Governs multi-agent collaboration.** The hardest problem in multi-agent systems is not parallel capacity — it is boundary governance.

#### What problem it actually solves

Multi-agent workflows spiral out of control because:

- Multiple agents edit the same files with no clear ownership
- Everyone is analyzing, but nobody owns final integration authority
- Review happens too early, or is too broad
- The main thread loses its role as the single source of truth

Without governance, multi-agent just amplifies single-agent instability.

#### Architecture

This skill deliberately keeps the team in a small, explicit topology:

| Role | Write scope | Responsibility | Why this separation |
| --- | --- | --- | --- |
| Team Lead | Integration & arbitration | Task contract, staffing, conflict resolution, final verification | Must retain the single source of truth |
| Solution Architect | Read-only | Design brief, risk hotspots, file impact map | Design must precede changes |
| Feature Engineer | Production code | Smallest safe implementation patch | Isolate implementation from other concerns |
| Test Engineer | Test code | Test coverage, regression protection | Make verification an independent responsibility |
| Reviewer / Verifier | Read-only | Review the integrated result | Avoid unfocused feedback on half-finished work |

#### Mode selection

| Mode | When to use | Staffing | Design goal |
| --- | --- | --- | --- |
| Mode A | Small change, low risk, single module | 0–1 sub-agents | Lowest coordination overhead |
| Mode B | Implementation and testing can parallelize | 2 sub-agents | Higher throughput without losing control |
| Mode C | High risk, cross-module, independent review needed | 3–4 sub-agents | Correctness-first full protection |

#### How it differs from "role-play" multi-agent

It doesn't indulge in the theatrics of multi-agent — it returns to the fundamentals of engineering organization:

- The main thread must retain a Team Lead
- Parallelism is not the default — it is a risk-driven choice
- Roles exist for responsibility isolation, not for appearances
- Review must be independent, and must happen after integration
- There can only be one source of truth

The point of this skill is not "more agents = smarter" — it's "multiple agents must be governed first."

---

### `learn`

**Makes agents smarter over time.** Every conversation between a developer and an agent contains high-value knowledge: corrections, patterns, facts, preferences. Without a learning system, this knowledge evaporates when the session ends. The agent starts from zero next time, and the user has to teach the same things again.

#### What problem it actually solves

- The agent was corrected last session — "don't mock the database" — and this session it mocks it again
- The user has said "keep responses concise" three times, but the agent is still verbose
- The project has a specific deploy pipeline, and it needs to be re-explained every time
- User coding preferences (naming style, architecture patterns) are never remembered

#### Architecture

This skill is built around one core belief: **conversations are a gold mine of reusable knowledge that gets wasted every time a session ends.** What the user teaches the agent should be systematically preserved.

| Design choice | Why | What it prevents |
| --- | --- | --- |
| Two commands only (`/learn` + `/learn-review`) | Minimal cognitive load | Too many commands that users won't bother to learn |
| Markdown files, not YAML/JSON | Human-readable, directly editable, git-friendly | Black-box knowledge that users can't inspect or correct |
| Three-tier strength (`weak→medium→strong`) | Simple but effective validation model | Floating-point pseudo-precision (0.47 vs 0.52 is meaningless) |
| Project + Global scoping | Keep project knowledge isolated | React habits leaking into a Python project |
| Semi-automatic promotion | User confirms before globalizing | Wrong knowledge polluting all projects — false promotion costs more than missed promotion |
| Quality gate (Save/Merge/Skip) | Filter noise before saving | Knowledge directory becoming a junk drawer |

#### Four knowledge types, prioritized

1. **Corrections** — user corrected the agent's approach (highest value). These represent mistakes the agent made and must never repeat.
2. **Patterns** — repeated workflow or coding convention. E.g., "in this project, always run lint before commit."
3. **Facts** — project/environment-specific truths. E.g., "CI uses Node 20", "deploy requires staging approval."
4. **Preferences** — user's personal style choices. E.g., "keep responses concise", "write comments in Chinese."

#### Strength evolution model

One of the most carefully designed aspects of `learn`. Knowledge is not permanently valid once saved — it needs to be validated, strengthened, and can be overturned:

```
New knowledge created → strength: weak, confirmed: 0
  ↓ Applied once without user correction
strength: weak, confirmed: 1
  ↓ Applied again without correction
strength: medium, confirmed: 2
  ↓ Repeatedly validated
strength: strong, confirmed: 4+
  ↓ User explicitly confirms ("yes, exactly")
strength: strong (immediate jump)
```

User says "no, that's wrong" → downgrade or delete. No automatic decay — knowledge doesn't disappear just because it hasn't been used recently. Stale knowledge is cleaned up through `/learn-review`.

This is more practical than floating-point confidence: `weak/medium/strong` is enough to distinguish "first observation" from "thoroughly validated" without forcing the system to split hairs between 0.47 and 0.52.

#### Scope isolation and promotion

Knowledge is stored at two levels:

- **Project** (`.claude/learned/`): project-specific knowledge, the default destination
- **Global** (`~/.claude/learned/`): cross-project universal knowledge

Promotion rules are deliberately conservative: only when a project-scoped entry reaches `strength = strong` and its content contains no project-specific references will the system **suggest** promotion — but the user always confirms.

Why not auto-promote? Because the cost of false promotion (polluting global scope) far exceeds the cost of missed promotion (teaching it again in another project).

#### User experience design

"Getting smarter over time" can't just be a technical fact — the user must **feel** it:

- Every `/learn` run clearly reports what was learned, what was skipped, and why
- When the agent makes a different decision based on learned knowledge, it says so:
  > "Using real database for integration tests (learned: don't mock DB)"
- `/learn-review` shows cumulative statistics: 23 global entries / 12 project entries
- New sessions announce: "Loaded 8 project entries and 15 global entries"

**Why it works:** Conversations are full of knowledge that agents lose between sessions. This skill turns that loss into lasting growth. Two commands, Markdown files, three strength tiers, and a quality gate — simple enough to actually use, transparent enough to trust, and structured enough to compound over time.

#### How learned knowledge actually takes effect

The `learn` skill only **stores** knowledge — it does not auto-load. To close the loop, install the `learned-knowledge` rule from `rules/common/`. Rules are auto-injected every session, so once installed, the agent will automatically load and apply accumulated knowledge without any manual action. The full pipeline:

```
/learn → saves knowledge files → learned-knowledge rule auto-loads them next session → agent applies and cites
```

Without the rule, `/learn` still extracts knowledge, but future sessions won't use it automatically. See the [Rules Reference](#rules-reference) for installation.

## How the Stack Fits Together

```mermaid
flowchart LR
    A[repo-bootstrap<br/>Persist repo memory] --> B[longrun-dev<br/>Control long-running execution]
    B --> C[agent-team-dev<br/>Coordinate parallel work]
    A --> C
    C --> D[Verified delivery<br/>with evidence and handoff]
    D --> E[learn<br/>Extract & accumulate knowledge]
    E -->|next session| A
```

- `repo-bootstrap` makes the agent **remember** the project
- `longrun-dev` makes the agent **stay on track**
- `agent-team-dev` makes multiple agents **cooperate without chaos**
- `learn` makes the agent **get smarter** over time

## Skills vs Rules

This repo provides two complementary systems:

| | Skills | Rules |
|--|--------|-------|
| **Analogy** | Playbook | Constitution |
| **Loading** | On-demand via `/skill-name` | Auto-injected every session |
| **Context cost** | Full text loaded only when invoked | Always loaded (each is short) |
| **Best for** | Long workflows (TDD, E2E, deep research…) | Short global constraints (style, security, git…) |
| **Activation** | User-triggered | Auto-enforced every turn |

**In short:** Rules are the agent's **instincts**. Skills are the agent's **learned expertise**.

## Rules Reference

> Rules take effect automatically after installation. No manual invocation needed.

### Common Rules (all languages)

| Rule | What It Enforces |
|------|-----------------|
| `coding-style` | Immutable data patterns; functions <50 lines, files <800 lines, nesting <4 levels |
| `security` | Pre-commit checks: no hardcoded secrets, parameterized SQL, XSS/CSRF protection |
| `testing` | TDD (write tests first); coverage ≥80% |
| `git-workflow` | Commit format `<type>: <description>`; PR analyzes full commit history |
| `code-review` | Auto-review after writing code; CRITICAL issues block merge |
| `development-workflow` | Full dev flow: search existing solutions → plan → TDD → review → commit |
| `patterns` | Search for battle-tested skeletons first; Repository Pattern recommended |
| `performance` | Model selection guidance (Haiku / Sonnet / Opus); context window management |
| `agents` | Auto-dispatch sub-agents: complex features → planner, code written → reviewer |
| `learned-knowledge` | Load learned knowledge (`~/.claude/learned/` + `.claude/learned/`) at session start; apply corrections, patterns, facts, preferences; cite sources |
| `hooks` | TodoWrite best practices, permission control guide |

### Python Rules (`.py`/`.pyi` files only)

| Rule | What It Enforces |
|------|-----------------|
| `coding-style` | PEP 8; type annotations required; `frozen=True` dataclass for immutability |
| `patterns` | Protocol duck typing, dataclass DTO, context manager, generator idioms |
| `security` | `os.environ["KEY"]` strict access; bandit static scanning |
| `testing` | pytest + `--cov`; `pytest.mark.unit/integration` categorization |
| `hooks` | Python project hook integration guide |

## Full Skill Inventory

Beyond the flagship quartet, the repo includes a broader reusable library:

<details>
<summary><strong>View all 46 skills</strong></summary>

### Engineering & Quality

| Skill | Purpose |
| --- | --- |
| `⭐⭐ repo-bootstrap` | Persist repo memory with structured context documents |
| `⭐⭐ longrun-dev` | Long-horizon development with stateful harness |
| `⭐⭐ learn` | Extract and accumulate knowledge from interactions |
| `agent-team-dev` | Multi-agent team with explicit ownership and review gates |
| `⭐ api-design` | Production REST API design patterns |
| `⭐ backend-patterns` | Node/Express/Next.js backend architecture |
| `⭐ frontend-patterns` | React/Next.js frontend architecture |
| `⭐ coding-standards` | Unified coding standards for JS/TS/React/Node |
| `⭐ security-review` | Security checklist for sensitive changes |
| `⭐ tdd-workflow` | Test-driven development workflow |
| `e2e-testing` | Playwright E2E testing patterns |
| `⭐ verification-loop` | End-to-end verification before delivery |
| `eval-harness` | Eval-driven development framework |
| `dmux-workflows` | Multi-agent orchestration via dmux/tmux |
| `strategic-compact` | Context compaction at milestone boundaries |

### Frontend, Design & Automation

| Skill | Purpose |
| --- | --- |
| `⭐ canvas-design` | Visual art and poster generation (.png/.pdf) |
| `figma` | Pull design context from Figma MCP |
| `figma-implement-design` | 1:1 Figma-to-code implementation |
| `⭐ frontend-design` | Production-grade frontend UI design |
| `⭐ playwright` | Real-browser automation from terminal |
| `develop-web-game` | Iterative web-game dev + testing loop |
| `frontend-slides` | HTML slide decks and PPT-to-web conversion |
| `screenshot` | OS-level screenshot capture |
| `webapp-testing` | Playwright-based local web app testing |

### Research, Docs & Knowledge

| Skill | Purpose |
| --- | --- |
| `⭐ deep-research` | Multi-source cited deep research |
| `market-research` | Market/competitor/investor diligence |
| `paper-deep-review` | Structured paper dissection |
| `⭐ openai-docs` | Official OpenAI docs lookup with citations |
| `exa-search` | Exa neural web/code/company search |
| `⭐ article-writing` | Long-form writing with voice consistency |
| `doc` | `.docx` authoring/editing with layout checks |
| `pdf` | PDF extraction/generation/review |

### GitHub, Ops & Delivery

| Skill | Purpose |
| --- | --- |
| `⭐ gh-address-comments` | Resolve PR review comments systematically |
| `⭐ gh-fix-ci` | Diagnose and fix failing GitHub Actions |
| `yeet` | Stage/commit/push/open PR in one flow |
| `linear` | Linear issue and project management |

### Content, Media & Growth

| Skill | Purpose |
| --- | --- |
| `content-engine` | Multi-platform content system design |
| `crosspost` | Channel-specific cross-post adaptation |
| `video-editing` | AI-assisted video editing pipeline |
| `fal-ai-media` | Image/video/audio generation via fal.ai |
| `x-api` | X/Twitter API integration |

### Business & Fundraising

| Skill | Purpose |
| --- | --- |
| `investor-materials` | Fundraising decks, memos, and models |
| `investor-outreach` | Investor outreach copywriting |

### Platform Integrations

| Skill | Purpose |
| --- | --- |
| `claude-api` | Claude API integration patterns |
| `⭐ mcp-builder` | Build MCP servers (Python FastMCP / Node SDK) |
| `skill-creator` | Create or refine skills |
| `skill-installer` | Install skills into local environment |

</details>

## Recommended Operating Order

For serious repo work, a strong default is:

1. Install skills and rules (see [Quick Start](#quick-start))
2. Use `repo-bootstrap` to make repo knowledge persistent
3. Use `longrun-dev` when the task will span multiple sessions
4. Use `learn` after productive sessions to accumulate knowledge
5. Use `agent-team-dev` only when bounded parallelism is worth the coordination cost
6. Layer on domain-specific skills after the operating system is in place

Companion skills by category:

- **Architecture:** `api-design`, `backend-patterns`, `frontend-patterns`, `coding-standards`
- **Quality:** `tdd-workflow`, `e2e-testing`, `verification-loop`, `security-review`
- **Research:** `deep-research`, `openai-docs`, `article-writing`
- **Delivery:** `gh-address-comments`, `gh-fix-ci`, `yeet`, `linear`

## Who This Is For

- Builders who want agents to act more like **durable collaborators** than chat assistants
- Teams running multi-step implementation, testing, and delivery through agents
- Engineers who care about **handoff quality**, verification discipline, and controlled autonomy
- Anyone who has felt that agent workflows are impressive in demos but unreliable in production

## Contributing

Contributions are welcome. The standard is practical usefulness.

A good contribution should:

- Solve a recurring real-world problem
- Have clear trigger conditions
- Define a concrete workflow, not generic advice
- Include scripts or references when they materially improve execution
- Rules should stay short (10–50 lines each) — move long workflows to skills

---

<div align="center">

**[Skills](./skills)** · **[Rules](./rules)** · **[Issues](https://github.com/YuxiaoWang-520/harness-craft/issues)** · **[Contributing](#contributing)**

</div>
