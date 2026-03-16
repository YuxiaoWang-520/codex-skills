# Output Template for Paper Deep Review

Use this template when generating result files.

## 1) memory.md

Recommended sections:
- Paper snapshot (title, venue/status, task domain)
- Core claim and contribution summary
- Method memory (core variables, equations, control flow)
- Baseline map (method family -> role)
- Experiment memory (main metrics, strongest evidence, non-dominant cases)
- Review risk notes (consistency issues, missing evidence)

## 2) prompt.md

Include reusable prompts for:
- Full technical review
- Baseline fairness audit
- Method failure-mode stress test
- Rebuttal drafting
- Minimal revision plan

Each prompt must require concrete evidence and avoid generic wording.

## 3) intro and motivation.md

Required content:
- One-line paper positioning
- Intro argument chain (problem -> gap -> proposal)
- Motivation strength assessment
- What is convincing vs what still needs stronger proof

## 4) method.md

Required content:
- Objective and system architecture
- Variables and equations with plain-language meaning
- Algorithm flow (step-by-step)
- Pseudocode-level decomposition
- Why it may work
- Where it may fail
- Difference vs major baseline categories

## 5) experiment.md

Required content:
- Full setup (dataset/model/distribution/system assumptions)
- Baselines and fairness controls
- Main quantitative outcomes (not just best-case)
- Time/accuracy/communication tradeoff interpretation
- Scaling and ablation conclusions
- Contradictory or non-dominant cases
- Threats to validity and missing tests

## Optional 6) baselines-and-delta.md

Use when baseline depth is requested.

For each baseline:
- what it optimizes
- what assumptions it makes
- where it is strong
- where the target paper improves or regresses
- fairness caveats
