---
type: computational-benchmark
field: Discrete Geometry
epistemic_status: effective
level: advanced
tags: [spherical-codes, symmetry, exact-construction, algebraic-numbers, verified-construction]
created: 2026-10-09
updated: 2026-10-09
note_maturity: expanded
source_audit: exact-rank-certificate-and-high-precision-numerics
---

# Benchmark 023 — An Exact S5-Symmetric Spherical Code in 13 Dimensions

**Status:** lab 58 (`58_exact_s5_spherical_code.py`) reproduces every claim below in about two minutes. No claim of optimality, and no claim that this structure is new to the literature (not yet searched).

## Finding

The improved 59-point code in $\mathbb R^{13}$ from [[Benchmark 022 — Improved Spherical Codes for Cohn's Table]] is a **57-point configuration with symmetry group $S_5$, plus two rattlers**.

**Structure of the 57-point core.**
- **Orbits.** Under $S_5$ (order 120) the 57 points fall into orbits of sizes 1, 5, 5, 6, 20 and 20.
- **Gram matrix.** It takes only 9 distinct values.
- **Representation.** $\mathbb R^{13}$ decomposes as $3\cdot\mathbf 1\oplus\mathrm{sgn}\oplus\mathbf 4\oplus\mathbf 5'$.

**The minimal angle is exact.** Its cosine is
$$\mu = 0.17137828088359479362302865869\ldots,$$
the root near 0.171 of the irreducible quartic
$$1196x^4-1428x^3+411x^2+18x-9=0.$$
The quartic's discriminant is $2^{20}\cdot3^8\cdot23\cdot431$. All nine Gram values lie in $\mathbb Q(\mu)$. Three of them are linear in $\mu$:
- $2\mu-1$;
- $(5\mu-2)/3$;
- $(4\mu-1)/3$.

These three are forced by exact vanishing on the $\mathbf 4'$, $\mathbf 5$ and $\mathbf 6$ isotypic components.

## Why the existence is rigorous

Let $G$ be the 57×57 Gram matrix with entries in $\mathbb Q(\mu)$.
1. **Rank.** Exact computation over $\mathbb Q(\mu)$ gives rank 13.
2. **Positive semidefinite.** At 60 digits its 13 nonzero eigenvalues are all at least 1.818, against a numerical error of $10^{-60}$. So $G$ is PSD, and it is the Gram matrix of 57 unit vectors in $\mathbb R^{13}$.
3. **Minimal angle.** The largest other value is $0.1051<\mu$, so the cosine of the minimal angle is exactly $\mu$.
4. **Rattlers.** Two rattlers fit with largest inner product $0.112<\mu$, giving 58- and 59-point codes with the same $\mu$.

What is *not* proved: optimality of $\mu$, or that the rattler coordinates are exact. They are explicit floating-point vectors whose inner products are checked at 50 digits.

## Effect on Cohn's table

| d | N | before (table) | now |
|---|---|---|---|
| 13 | 58 | 0.173434450407 (2026 table) → 0.171378280885 (Benchmark 022 upload) | **0.171378280884** (exact μ) |
| 13 | 59 | 0.179765321180 → 0.171378280898 | **0.171378280884** (exact μ) |
| 13 | 71 | 0.205582365853 → 0.204538912177 | 0.204507858381 (further polish) |
| 13 | 72 | 0.207220363795 → 0.205810552628 | 0.205422831761 (further polish) |

The 71 and 72 rows are numerical improvements only, not exact constructions. All four were **uploaded on 2026-10-09** and accepted. The live table shows 0.171378280884, 0.171378280884, 0.204507858382 and 0.205422831761. The upload note gave the maintainer the minimal polynomial, the S5 structure, and a permalink to lab 58 at commit `ee67bc0`. No separate email was sent. Exact 40-digit coordinates are in `results/spherical_codes/exact_13/`.

## How it was found

The structure surfaced when the inner products were inspected. The automorphism group was then computed as the group of colour-preserving permutations of the Gram matrix. Projectors built from exact characters turned the rank-13 condition into integer linear equations plus small rank conditions. A 90-digit Gauss–Newton solve followed: the solution is isolated, and the smallest singular value of the Jacobian is 0.0165. PSLQ identified the values, and an exact rank certificate closed the argument.

[[Benchmark 022 — Improved Spherical Codes for Cohn's Table]] · [[Computational Lab Index]] · [[Release Status and Next Work]]
