# Baseline Analysis Checklist

Use this checklist to avoid shallow baseline comparison.

## A. Coverage
- Did the paper include centralized, decentralized, and heterogeneity-aware baselines where relevant?
- Did it include both classic and recent strong baselines?

## B. Fairness
- Same training budget?
- Same data split and random seed policy?
- Same or justified optimizer settings?
- Same reporting metric and target threshold?
- Compression ratio and communication settings fairly matched?

## C. Interpretation
For each baseline, explain:
- Method family and core idea.
- Why this baseline matters for this paper.
- Which metric the baseline is naturally good at.
- Whether the proposed method beats it on all, most, or only some settings.

## D. Risk Flags
- Over-claim: text says "consistently best" but table has exceptions.
- Cherry-pick: only favorable metrics highlighted.
- Missing uncertainty: no variance/confidence intervals.
- Hidden cost: better accuracy but much larger communication/time cost.

## E. Delta Statement
Write one concise delta statement per baseline:
- "Compared with <baseline>, this paper adds/removes/changes <mechanism>, yielding <observed effect> under <conditions>."
