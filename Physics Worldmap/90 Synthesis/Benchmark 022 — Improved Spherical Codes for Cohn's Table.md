---
type: computational-benchmark
field: Discrete Geometry
epistemic_status: effective
level: advanced
tags: [spherical-codes, packing, optimisation, record-table, verified-construction]
created: 2026-10-09
updated: 2026-10-09
note_maturity: expanded
source_audit: live-record-table-compared-and-verified-to-50-digits
---

# Benchmark 022 — Improved Spherical Codes for Cohn's Table

**Status:** 35 entries of Henry Cohn's table of spherical codes (spherical-codes.org) are improved. 13 of them improve by more than 10⁻⁵. Every code was checked independently against the live table value at the time of checking (2026-10-09). The check uses 50-digit evaluation of the maximal inner product, and each code must beat the record strictly after rounding up to 12 decimals. **Submitted on 2026-10-09** through the table's upload form, credited to Luke Granto. The table accepted all 35 entries, which show as "Uploaded by anonymous internet user" until the maintainer reviews them:
- 34 are listed with the new values.
- (15,75) is now omitted as dominated by the improved (15,76) code.
- The (9,73) upload was first not shown, apparently because it ties the new (9,72) value at 12 decimals. It was accepted on re-upload.

**What this is and is not.** These are verifiable constructions: anyone can check a code from its coordinates with a few lines of code. They improve entries that the maintainer marks "needs more optimization". This is a modest, solid contribution, not a breakthrough. No optimality is claimed, and the method (basin hopping plus LP polish) is standard.

## Method

- **Search (lab 56):** `56_spherical_code_search.py`.
  - Start from the table's current coordinates and LP-polish them.
  - Then basin-hop: perturb or re-seed points, and run L-BFGS on a log-sum-exp smoothing of $\mu=\max_{i<j}\langle x_i,x_j\rangle$ at increasing sharpness.
  - Finish with trust-region sequential LP on the near-active pairs.
  - Budget: 3–4 CPU-minutes per entry. The run covered 102 flagged entries with 8 ≤ d ≤ 20 and N ≤ 100, and 33 improved.
- **Final check (lab 57):** `57_spherical_code_final_check.py`.
  - A float64 screen, then 50-digit evaluation of all pairs within 10⁻⁹ of the maximum.
  - Each code is compared with the live table value and must satisfy ⌈μ⌉₁₂ < ⌈record⌉₁₂.
  - The check also tries N−1 by deleting a point and polishing. Three further entries came from this.
- **Coordinates:** `results/spherical_codes/codes/sc_d_N.txt`, one point per line, in the table's upload format.
- **Development:** the first two batch runs stalled on degenerate LPs (lab 56 now caps each solve), and a first survey candidate for (13,59) was superseded.

## Results (cosine of the minimal angle; lower is better)

| d | N | table record (live) | new | gain | note |
|---|---|---|---|---|---|
| 9 | 72 | 0.329461905184 | 0.328681603186 | 7.80e-04 | deleted one point from N+1 |
| 9 | 73 | 0.329478033288 | 0.328681603186 | 7.96e-04 | |
| 10 | 87 | 0.323082807860 | 0.323082764765 | 4.31e-08 | |
| 10 | 88 | 0.324001091518 | 0.324001091468 | 4.97e-11 | |
| 11 | 72 | 0.252505567191 | 0.252505460076 | 1.07e-07 | |
| 11 | 73 | 0.253332726935 | 0.252831335670 | 5.01e-04 | |
| 12 | 71 | 0.230359188910 | 0.230214504053 | 1.45e-04 | |
| 13 | 58 | 0.173434450407 | 0.171378280884 | 2.06e-03 | deleted one point from N+1 |
| 13 | 59 | 0.179765321180 | 0.171378280898 | 8.39e-03 | |
| 13 | 60 | 0.179785851581 | 0.179116681241 | 6.69e-04 | |
| 13 | 71 | 0.205582365853 | 0.204538912177 | 1.04e-03 | |
| 13 | 72 | 0.207220363795 | 0.205810552628 | 1.41e-03 | |
| 13 | 74 | 0.209221450024 | 0.208771442079 | 4.50e-04 | |
| 13 | 90 | 0.241063947559 | 0.241063944443 | 3.12e-09 | |
| 13 | 93 | 0.243747904152 | 0.243720935726 | 2.70e-05 | |
| 13 | 94 | 0.244093461052 | 0.244090157544 | 3.30e-06 | |
| 13 | 95 | 0.244179305989 | 0.244179261698 | 4.43e-08 | |
| 13 | 96 | 0.244269238665 | 0.244267500685 | 1.74e-06 | |
| 13 | 99 | 0.245099135892 | 0.244900175257 | 1.99e-04 | |
| 14 | 76 | 0.189882982066 | 0.189882981571 | 4.95e-10 | |
| 14 | 78 | 0.191435294550 | 0.191435294365 | 1.85e-10 | |
| 15 | 75 | 0.168269066399 | 0.168269065620 | 7.80e-10 | |
| 15 | 76 | 0.168269475595 | 0.168267160236 | 2.32e-06 | deleted one point from N+1 |
| 15 | 77 | 0.168269745715 | 0.168269489188 | 2.57e-07 | |
| 16 | 63 | 0.127282275724 | 0.127282275198 | 5.26e-10 | |
| 16 | 76 | 0.155903738578 | 0.155903629250 | 1.09e-07 | |
| 16 | 78 | 0.156302288104 | 0.156302287276 | 8.28e-10 | |
| 16 | 79 | 0.156684471431 | 0.156684455083 | 1.63e-08 | |
| 17 | 72 | 0.127279887253 | 0.127279802738 | 8.45e-08 | |
| 17 | 82 | 0.149940620385 | 0.149940163547 | 4.57e-07 | |
| 17 | 83 | 0.149986068520 | 0.149985913657 | 1.55e-07 | |
| 17 | 84 | 0.149995515797 | 0.149995475442 | 4.04e-08 | |
| 17 | 94 | 0.167228782108 | 0.167036138529 | 1.93e-04 | |
| 17 | 96 | 0.168028032808 | 0.168027806891 | 2.26e-07 | |
| 19 | 77 | 0.112762651670 | 0.112762651452 | 2.19e-10 | |

## Reading

1. The largest gains are in **13 dimensions** (N = 58–74): the table's 59-point code, for example, is improved by 0.0084. The new 59-point code also gives a 58-point code that beats that record.
2. Gains of 10⁻⁷ to 10⁻¹¹ are real but small. They come from codes that had not fully converged.
3. The improvements are monotone-consistent: each new value sits between its neighbours' records, except where the new code also improves the neighbour (13/58, 9/72, 15/76).

## Limits

- The table changes. Others (ImprovEvolve, Cohn's own re-optimisation) improve entries continually, so each entry must be re-checked just before submission.
- Search effort was small. Larger budgets would likely improve more of the 11,995 flagged entries.

[[Computational Lab Index]] · [[Release Status and Next Work]]
