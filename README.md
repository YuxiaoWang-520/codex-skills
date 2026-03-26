<div align="right">

[![Language: English](https://img.shields.io/badge/Language-English-0A66C2)](./README.md)
[![语言: 简体中文](https://img.shields.io/badge/语言-简体中文-2EA44F)](./README_CN.md)

</div>

# Codex Skills

Turn Agentic Coding from a one-off prompt trick into a durable engineering system.

This repository is built around a simple belief:

> The biggest failure mode in agent-driven development is usually not intelligence. It is system instability.

Most teams do not get blocked because the model "cannot write code".
They get blocked because the workflow is fragile:

- the agent understood the repo yesterday and acts like it has amnesia today
- multiple agents look busy, but their changes collide and review quality is weak
- plans, validation status, and handoff context live only inside chat transcripts
- the agent feels done, while the repository is still not in a deliverable state

This repo is designed to solve those problems directly.

## Core Idea

The goal is not to add one more clever prompt.

The goal is to upgrade agent work into a system that is:

- **persistent**: repo knowledge survives context-window loss
- **verifiable**: progress is tied to evidence, not confidence
- **collaborative**: multiple agents can work without stepping on each other
- **recoverable**: long tasks can resume from stable state instead of vague memory

That is the design center of this repository.

## The 3 Flagship Skills

If you only try three skills from this repo, start with these:

- `repo-codex-bootstrap`
- `codex-longrun-dev`
- `agent-team-dev`

Together, they cover the three layers where serious agent workflows usually fail:

| Skill | Layer | Core Problem | Design Lever | Most Important Control Points | Typical Outputs |
| --- | --- | --- | --- | --- | --- |
| `repo-codex-bootstrap` | Context layer | Repo knowledge gets lost between sessions | Split project understanding into durable documents backed by structured state | responsibility separation, continuous updates, explicit unknowns | `codex/state.json`, `memory.md`, `prompt.md`, `repowiki.md`, `plan.md`, `checklist.md` |
| `codex-longrun-dev` | Execution continuity layer | Long tasks drift, lose focus, or get declared done too early | Turn long-running development into a stateful harness | one feature per session, baseline recovery first, required evidence | `.codex-longrun/init.sh`, `feature_list.json`, `progress.md`, `session_state.json` |
| `agent-team-dev` | Collaboration orchestration layer | Multi-agent work becomes noisy, overlapping, and hard to trust | Treat multi-agent work like a compact engineering team | ownership, role boundaries, independent review, round caps | task contract, role packets, `A1/I1/T1/R1` artifacts |

These three skills are the core differentiator of the repository.

## Why These Skills Matter

### `repo-codex-bootstrap`

**This skill is about protecting context.**

The key insight is not "generate five markdown files".
The real value is that it turns repo understanding from hidden background knowledge into an explicit workspace.

#### What problem it solves

A capable agent needs more than source code:

- what the user is actually trying to achieve
- what decisions were already made
- how the repo is run, tested, and validated
- which gaps are still unresolved
- whether the plan still matches execution reality

If that information lives only in chat history, it is fragile.
As soon as sessions change, parallel threads multiply, or another agent takes over, facts and assumptions blur together.

#### Architecture

This skill separates repo cognition into six persistent artifacts:

- `codex/state.json`: canonical machine-readable source of truth
- `codex/memory.md`: durable working memory
- `codex/prompt.md`: user intent, constraints, and interpretation history
- `codex/repowiki.md`: repository facts, commands, structure, and environment notes
- `codex/plan.md`: execution design, assumptions, risks, and validation strategy
- `codex/checklist.md`: real execution ledger, file changes, and validation state

That separation matters because these concerns should not be mixed:

| File | Responsibility | Why It Must Stay Separate |
| --- | --- | --- |
| `memory.md` | Ongoing working memory | Mixing it with repo facts turns it into an unstructured diary |
| `prompt.md` | User intent and evolving constraints | Task semantics should not be buried inside repo structure notes |
| `repowiki.md` | Stable operational repo knowledge | Long-term facts should not be polluted by session noise |
| `plan.md` | Intended path forward | Plans are not the same as executed reality |
| `checklist.md` | Real execution and validation status | Actual progress should not be rewritten into design prose |

#### Why the design is strong

There are three design decisions here that matter:

1. It does not pretend automation can replace understanding.
   The bootstrap script can detect languages, frameworks, commands, config files, and top-level structure. That gives the agent a scaffold, not false certainty.

2. It treats update rules as governance, not suggestions.
   `memory.md` and `prompt.md` are supposed to be updated every turn. `repowiki.md` should reflect repo fact changes. `plan.md` and `checklist.md` should move together when non-trivial implementation starts.

3. It manages unknowns explicitly.
   A good memory system does not only store what is known. It also stores what is still missing, how to discover it, and what should not be assumed.

That makes the system more honest, easier to hand off, and much harder to silently drift.

### `codex-longrun-dev`

**This skill is about keeping long tasks from wandering off course.**

Short demos usually show how an agent starts.
Real engineering systems need to control how an agent continues.

#### What problem it solves

Once a task spans many sessions, the common failure modes are predictable:

- the agent no longer knows where it left off
- baseline is already broken, but more changes keep piling on top
- feature scope drifts quietly across sessions
- progress is narrated, but not structured
- the model decides that something is "basically done" without objective evidence

These are not prompt wording problems.
They are state-management and execution-discipline problems.

#### Architecture

`codex-longrun-dev` bootstraps a harness inside the target repository:

- `.codex-longrun/init.sh`: dependency setup and smoke checks
- `.codex-longrun/feature_list.json`: feature definitions and pass/fail status
- `.codex-longrun/progress.md`: append-only session log
- `.codex-longrun/session_state.json`: current recovery and session state

This is the critical move: long-running task state becomes a **repo asset**, not a chat artifact.

#### The control model

The most important constraints are intentionally strict:

| Constraint | Why It Exists | What It Prevents |
| --- | --- | --- |
| One feature per session | Limits scope expansion | "While I'm here" drift, opportunistic refactors, hidden scope creep |
| Run `init.sh` first | Restore health before adding new work | Building new changes on top of a broken baseline |
| Keep `feature_list.json` mostly status-only | Freeze feature definitions | Quietly rewriting the target problem mid-flight |
| Keep `progress.md` append-only | Preserve traceability | History loss and weak handoff |
| Require evidence for completion | Tie done-ness to validation | Premature "done" declarations based on model confidence |

#### Why this is unusually valuable

The strongest idea in this skill is not complexity. It is restraint.

"One feature per session" looks simple, but it is one of the highest-leverage control points for agents. Agents do not only fail by being incapable. They also fail by doing too much, too broadly, and too early.

This skill forces long tasks to behave like a sequence of local, recoverable, evidence-backed units.

That is what makes long-running autonomous development practical rather than theatrical.

### `agent-team-dev`

**This skill is about governed multi-agent collaboration.**

The point of multi-agent systems is not "more minds".
The point is better decomposition with stronger boundaries.

#### What problem it solves

Multi-agent workflows usually break because:

- multiple agents touch overlapping files without clear ownership
- everyone produces analysis, but nobody owns final integration
- review happens too early or too vaguely
- the main thread loses its role as the single source of truth

Without governance, multi-agent work often amplifies the instability of single-agent work.

#### Architecture

This skill deliberately keeps the team small and explicit:

| Role | Write Scope | Responsibility | Why It Is Split This Way |
| --- | --- | --- | --- |
| Team Lead | integration and arbitration | task contract, staffing, conflict resolution, final verification | there must be one final source of truth |
| Solution Architect | read-only | design brief, risk hotspots, file impact map | design should precede edits |
| Feature Engineer | production code | smallest safe implementation patch | implementation should be isolated |
| Test Engineer | tests and fixtures | coverage, regression protection, test evidence | validation should be a first-class role |
| Reviewer / Verifier | read-only | independent review of integrated result | review should happen on real integrated state |

#### Mode-based orchestration

Instead of treating parallelism as the default, this skill treats it as a risk-based decision:

| Mode | When To Use It | Staffing | Optimization Goal |
| --- | --- | --- | --- |
| Mode A | small, low-risk, single-module changes | 0-1 sub-agents | lowest coordination overhead |
| Mode B | implementation and testing can proceed in parallel | 2 sub-agents | throughput without losing control |
| Mode C | high-risk, cross-module work, independent review required | 3-4 sub-agents | correctness-first protection |

#### What makes it different

This skill is intentionally unromantic about multi-agent work.

It does not try to simulate an entire company.
It does not optimize for theatrical roleplay.
It optimizes for:

- explicit file ownership
- clear role packets
- independent review after integration
- round caps and stop conditions
- a single arbitration point in the Team Lead

That is why it tends to hold up better in real engineering tasks than looser "everyone collaborates with everyone" patterns.

## How To Use This Repo

### Install Into Codex

Place the skill folders under your local Codex skills directory.

Use either:

- `~/.codex/skills/`
- or `$CODEX_HOME/skills/`

Example:

```bash
mkdir -p ~/.codex/skills
cp -R skills/repo-codex-bootstrap ~/.codex/skills/
cp -R skills/codex-longrun-dev ~/.codex/skills/
cp -R skills/agent-team-dev ~/.codex/skills/
```

To install the whole collection:

```bash
mkdir -p ~/.codex/skills
cp -R skills/* ~/.codex/skills/
```

Expected structure:

```text
~/.codex/skills/
  repo-codex-bootstrap/
    SKILL.md
  codex-longrun-dev/
    SKILL.md
  agent-team-dev/
    SKILL.md
```

### Recommended Operating Order

For serious repo work, a strong default is:

1. Install the skills into `~/.codex/skills/`.
2. Use `repo-codex-bootstrap` to make repo knowledge persistent.
3. Use `codex-longrun-dev` when the task will span many sessions.
4. Use `agent-team-dev` only when bounded parallelism is worth the coordination cost.
5. Layer on domain-specific skills after the operating system is in place.

In short:

- `repo-codex-bootstrap` makes the agent remember
- `codex-longrun-dev` makes the agent stay on track
- `agent-team-dev` makes multiple agents cooperate without chaos

## Full Skill Inventory

The flagship trio is the main entry point, but the repo also includes a broader skill library.

| Skill | Primary Use |
| --- | --- |
| `agent-team-dev` | Coordinate a compact sub-agent team with explicit ownership and verification gates |
| `api-design` | Design production-grade REST APIs |
| `article-writing` | Write polished long-form articles, guides, and newsletters |
| `backend-patterns` | Structure and optimize Node.js, Express, and Next.js backend systems |
| `claude-api` | Build apps with the Anthropic Claude API |
| `codex-longrun-dev` | Run long-horizon development with persistent harness artifacts |
| `coding-standards` | Apply shared coding standards across TS, JS, React, and Node |
| `content-engine` | Turn one idea into a multi-platform content system |
| `crosspost` | Adapt one message across X, LinkedIn, Threads, and Bluesky |
| `deep-research` | Run multi-source research with citations and synthesis |
| `develop-web-game` | Iterate on HTML/JS games with a tight test loop |
| `dmux-workflows` | Orchestrate multi-agent work through dmux/tmux workflows |
| `doc` | Create and edit `.docx` documents with layout checks |
| `e2e-testing` | Build and maintain Playwright end-to-end test suites |
| `eval-harness` | Evaluate agent behavior with a formal harness |
| `exa-search` | Use Exa for neural web, code, and company search |
| `fal-ai-media` | Generate image, video, and audio assets via fal.ai |
| `figma` | Pull design context and assets from Figma |
| `figma-implement-design` | Translate Figma nodes into production-ready UI |
| `frontend-patterns` | Build scalable React and Next.js frontend systems |
| `frontend-slides` | Create high-impact slide decks in HTML |
| `gh-address-comments` | Resolve GitHub PR review comments systematically |
| `gh-fix-ci` | Diagnose and fix failing GitHub Actions checks |
| `investor-materials` | Produce investor-facing fundraising materials |
| `investor-outreach` | Write investor outreach and follow-up messages |
| `linear` | Manage issues and workflow in Linear |
| `market-research` | Analyze markets, competitors, and diligence targets |
| `openai-docs` | Use current official OpenAI docs with citations |
| `paper-deep-review` | Read and explain research papers deeply |
| `pdf` | Parse, generate, and inspect PDFs |
| `playwright` | Automate a real browser from the terminal |
| `repo-codex-bootstrap` | Persist repo memory and regenerate structured codex docs |
| `screenshot` | Capture desktop or app screenshots |
| `security-review` | Review auth, secrets, input handling, and sensitive flows |
| `skill-creator` | Create or refine Codex skills |
| `skill-installer` | Install skills into your local Codex environment |
| `strategic-compact` | Compress context intentionally at milestone boundaries |
| `tdd-workflow` | Drive implementation through tests first |
| `verification-loop` | Run a structured verification pass before delivery |
| `video-editing` | Edit and structure videos with AI-assisted workflows |
| `x-api` | Integrate with the X/Twitter API |
| `yeet` | Stage, commit, push, and open a PR in one flow |

## Who This Repo Is For

- builders who want agents to act more like durable collaborators than chat assistants
- teams running multi-step implementation, testing, and delivery through agents
- engineers who care about handoff quality, verification discipline, and controlled autonomy
- anyone who has felt that agent workflows are impressive in demos but unreliable in production

## Contributing

Contributions are welcome, but the standard is practical usefulness.

A good skill in this repo should:

- solve a recurring real-world problem
- have clear trigger conditions
- define an actual workflow, not generic advice
- include scripts or references when they materially improve execution
- improve repeatability, correctness, or recoverability
