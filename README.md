# Codex Skills

Production-grade skills for Codex agents who need to remember your repo, run for hours without losing the plot, and coordinate multiple agents without chaos.

This repository is not a random prompt pack. It is a practical operating layer for serious agent-driven development:

- durable repo memory instead of repeated rediscovery
- long-running execution harnesses instead of fragile one-shot sessions
- accountable multi-agent teamwork instead of parallel confusion
- reusable engineering, research, docs, and delivery skills for real projects

## Why This Repo Exists

Most agent workflows break in the same three places:

1. The agent forgets what it learned about the repo.
2. Long tasks drift, restart badly, or lose verification discipline.
3. Multi-agent work creates overlap, merge conflicts, and shallow review.

This repository is built to solve those problems directly.

If you only try three skills, start here:

- `repo-codex-bootstrap`
- `codex-longrun-dev`
- `agent-team-dev`

Together, they give you a durable memory layer, a long-horizon execution harness, and a safe multi-agent coordination model.

## Install

To use a skill with Codex, place the skill folder under your local Codex skills directory:

```bash
mkdir -p ~/.codex/skills
cp -R skills/repo-codex-bootstrap ~/.codex/skills/
cp -R skills/codex-longrun-dev ~/.codex/skills/
cp -R skills/agent-team-dev ~/.codex/skills/
```

Or install the whole collection by copying the skill directories from this repo into `~/.codex/skills/`.

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

Each skill is self-contained and follows the same pattern:

```text
<skill-name>/
  SKILL.md
  agents/openai.yaml
  scripts/
  references/
  assets/
```

## The 3 Flagship Skills

### 1. `repo-codex-bootstrap`

**Turn Codex into a repo-aware system with durable memory on disk.**

What it solves:

- the agent forgets architecture, decisions, and prior discoveries between sessions
- repo knowledge lives only in chat history
- planning notes, prompt history, and implementation context disappear over time

Why it is different:

- uses `codex/state.json` as a structured source of truth
- continuously re-renders `memory.md`, `prompt.md`, `repowiki.md`, `plan.md`, and `checklist.md`
- preserves rolling knowledge instead of overwriting it with templates
- keeps repo understanding local, inspectable, and recoverable

Architecture:

- `codex/state.json`: machine-readable memory store
- `codex/memory.md`: durable working memory
- `codex/prompt.md`: prompt and intent history
- `codex/repowiki.md`: operational wiki for the repo
- `codex/plan.md`: execution plan
- `codex/checklist.md`: validation and delivery ledger

Why people try it:

Because the fastest way to make an agent feel smarter is to stop making it rediscover the same repo every day.

### 2. `codex-longrun-dev`

**Run long-horizon coding work as a harness, not as a fragile conversation.**

What it solves:

- multi-hour or multi-day tasks lose structure between context windows
- agents claim progress without clean validation
- large projects stall because nobody knows what was done, what is left, and what is currently green

Why it is different:

- bootstraps a deterministic `.codex-longrun/` harness inside the target repo
- enforces one-feature-at-a-time execution
- requires verification evidence before a feature is considered done
- leaves every session with a clean handoff and a commit

Architecture:

- `.codex-longrun/init.sh`: dependency setup and smoke checks
- `.codex-longrun/feature_list.json`: feature queue and pass/fail state
- `.codex-longrun/progress.md`: session-by-session progress log
- `.codex-longrun/session_state.json`: current session state and recovery info

Why people try it:

Because long-running agent work only scales when progress, verification, and handoff are made explicit.

### 3. `agent-team-dev`

**Use multiple agents without turning your codebase into a collision zone.**

What it solves:

- overlapping edits from parallel agents
- weak ownership and unclear handoffs
- shallow or redundant analysis from too many agents doing the same work
- rushed implementation without an independent review pass

Why it is different:

- keeps one Team Lead in the main thread
- limits the team to a compact topology with explicit roles
- assigns disjoint file ownership before delegation
- prioritizes correctness first, efficiency second, token savings third

Architecture:

- Team Lead: contract, integration, verification
- Solution Architect: read-only design and risk brief
- Feature Engineer: production code implementation
- Test Engineer: tests and fixtures
- Reviewer/Verifier: independent risk-ranked review

Why people try it:

Because parallelism is only valuable when ownership, verification, and integration are controlled.

## How These 3 Skills Work Together

This is the recommended operating stack:

1. Start with `repo-codex-bootstrap` to persist repo knowledge locally.
2. Use `codex-longrun-dev` when the task is bigger than one safe session.
3. Use `agent-team-dev` when the task benefits from bounded parallelism.

In practice:

- `repo-codex-bootstrap` makes the agent remember
- `codex-longrun-dev` makes the agent finish
- `agent-team-dev` makes multiple agents collaborate without stepping on each other

That combination is the core value of this repository.

## Recommended Usage Flow

For a serious repo, this is a strong default:

1. Install `repo-codex-bootstrap`, `codex-longrun-dev`, and `agent-team-dev` into `~/.codex/skills/`.
2. Bootstrap repo memory with `repo-codex-bootstrap`.
3. Bootstrap long-run harness files if the task spans many sessions.
4. Delegate with `agent-team-dev` only when there is a real parallelism win.
5. Add domain-specific skills only after the operating layer is in place.

Suggested companion skills:

- build and architecture: `api-design`, `backend-patterns`, `frontend-patterns`, `coding-standards`
- quality: `tdd-workflow`, `e2e-testing`, `verification-loop`, `security-review`
- research and docs: `deep-research`, `openai-docs`, `article-writing`
- delivery: `gh-address-comments`, `gh-fix-ci`, `yeet`

## What Else Is In This Repo

Beyond the three flagship skills, this repo includes a broad set of focused, reusable skills for engineering, testing, research, content, media, fundraising, and delivery.

### Full Skill Inventory

| Skill | Primary Use |
| --- | --- |
| `agent-team-dev` | Coordinate a small sub-agent team with explicit ownership and quality gates |
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
| `market-research` | Analyze markets, competitors, and due diligence targets |
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

- engineers building serious agent workflows
- solo builders who want agents to behave like durable collaborators
- teams that need repeatable AI-assisted implementation, testing, and delivery
- anyone tired of agents forgetting the repo, losing momentum, or creating parallel messes

## Contributing

Contributions are welcome, but the bar is practical usefulness.

A strong skill in this repo should:

- solve a repeatable real-world problem
- have a clear trigger condition
- define a concrete workflow, not just generic advice
- include scripts or references when they materially improve execution
- help the agent produce better outcomes, not just longer outputs

If you want this repository to feel dramatically more capable on day one, start with the flagship trio:

- `repo-codex-bootstrap`
- `codex-longrun-dev`
- `agent-team-dev`
