---
name: paper-deep-review
description: Deeply read and synthesize research papers (especially PDF papers) into structured, high-detail outputs for fast but rigorous understanding. Use when the user asks for paper interpretation, section-wise summarization, baseline analysis, method step-by-step explanation, experiment dissection, strengths/weaknesses, novelty, or differences from prior work.
---

# Paper Deep Review

Follow this workflow to produce high-detail, decision-useful paper analysis.

## Core Outcome
Produce analysis that lets a reader quickly answer:
- What problem is solved and why it matters.
- What exact method is proposed and how it runs step by step.
- Which baselines are used, what they represent, and how fair the comparison is.
- What experiments prove, what remains uncertain, and what the paper's true strengths/limits are.

Favor precision over hype. Keep claims evidence-backed.

## Default Workflow

### 1) Locate Inputs and Define Output Scope
- Identify paper file(s), usually under a user-provided folder.
- Confirm file readability before writing any summary.
- Create a result directory if missing.
- If multiple papers exist, create one subfolder per paper to avoid overwrite.

### 2) Extract Text Robustly
- Prefer visual+text fidelity when available.
- Use one of:
  - `pdftotext`/Poppler when installed.
  - `python` with `pdfplumber`/`pypdf` when Poppler is unavailable.
- Use `scripts/extract_paper_text.py` in this skill for deterministic extraction.
- Save extraction artifacts to a temp location (`tmp/`), not final result files.

### 3) Build Section Map Before Summarizing
- Identify and map at least:
  - `Introduction`
  - `Motivation/Problem Setup`
  - `Method`
  - `Experiments`
  - `Related Work`
  - `Conclusion`
- Detect extraction noise (garbled figure glyphs, missing equations).
- If any critical section is unreadable, state the gap explicitly.

### 4) Analyze Baselines as First-Class Content
For each major baseline in the paper:
- Explain what family it belongs to (centralized, decentralized, compression-based, heterogeneity-aware, etc.).
- Explain what design principle it represents.
- Explain why it is a meaningful comparator for the proposed method.
- State where the new method wins, ties, or loses.
- Flag comparison-risk factors (different training budget, compression ratio, target metric bias, missing variance).

If baseline details are insufficient in the paper text, mark those parts as `inference`.

### 5) Perform Method Step-by-Step Decomposition
- Translate the method into an execution flow:
  - input signals/state
  - decision logic
  - update rules
  - communication/training loop
  - stopping/transition conditions
- Include equations, pseudocode logic, and variable meanings.
- Explain not only "what" but "why this design may work" and "where it may fail".
- Separate paper-stated mechanism from your interpretation.

### 6) Dissect Experiment Evidence
At minimum cover:
- Setup: datasets, models, hardware/system assumptions, data split.
- Baselines and fairness settings.
- Main tables/figures with key numbers.
- Time/accuracy/communication tradeoffs.
- Ablation and scaling results.
- Negative or non-dominant cases.
- Threats to validity and missing tests.

### 7) Write Structured Deliverables
When user asks for the original 5-file format, generate these files in `result/`:
- `memory.md`
- `prompt.md`
- `intro and motivation.md`
- `method.md`
- `experiment.md`

Use templates from:
- `references/output-template.md`
- `references/baseline-analysis-checklist.md`

If baseline depth is heavily requested, optionally add:
- `baselines-and-delta.md`

## Writing Standards

### Evidence Discipline
- Distinguish `paper evidence` from `your inference`.
- Avoid universal claims unless every reported setting supports them.
- If one metric or one task contradicts a broad claim, state that explicitly.

### Detail Allocation
- Keep intro concise but sharp.
- Keep method and baseline analysis deep.
- Keep experiments quantitative and comparative.
- Avoid shallow bullet dumps.

### Quantitative Reporting
- Report concrete numbers when available (accuracy, speedup, time-to-target, communication volume).
- Preserve metric context (IID vs Non-IID, model, dataset, target threshold).

### Review-Oriented Lens
Always include:
- what is strong
- what is weak
- what is unclear
- what extra evidence would change confidence

## Output Checklist (Before Finalizing)
- Confirm file readability was verified.
- Confirm all requested output files were generated.
- Confirm method is explained step by step.
- Confirm baseline families and differences are explicitly analyzed.
- Confirm at least one limitation/risk section is included.
- Confirm no over-claim against contradictory table entries.

## Script
- `scripts/extract_paper_text.py`
  - Extract page text from PDF.
  - Produce `full_text.txt` and per-page text files.
  - Produce a simple section index guess for fast navigation.

