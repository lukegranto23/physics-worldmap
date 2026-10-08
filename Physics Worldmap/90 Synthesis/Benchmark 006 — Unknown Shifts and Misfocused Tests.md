---
type: computational-benchmark
field: Cross-field
epistemic_status: effective
level: advanced
tags: [physics, research, experimental-design, model-checking, reproducibility]
created: 2026-09-04
updated: 2026-09-04
source_audit: explicit-model-derived-with-primary-method-sources
note_maturity: expanded
---

# Benchmark 006 — Unknown Shifts and Misfocused Tests

> [!important] Outcome
> Range-based timing helps some previously unseen shifts but is not uniformly better. A fixed alternative-mixture test improves some comparisons while missing other physical changes. For one damping-only change, its detection probability tends to zero as the sample size grows, despite a roughly 20% response error. This is a limitation of a specified statistical test, not a new physical law.

[[Benchmark 005 — Information Limits and Better Measurements]] · [[Research Frontier — Identifiability Before Discovery]] · [[When More Data Cannot Rescue a Misfocused Test]]

## Question and frozen rules

Can we improve model checking without telling the detector the exact frequency shift, and does the improvement survive a measurement-time penalty?

The [protocol](../62%20Computational%20Labs/range_design_protocol.json) was saved before the first run. It is a local frozen protocol, not an external preregistration. SHA-256:

    8b29bbf6766e76fc9334ccedcc0d7f7c6ae8d8fc4e66c5ae923ded0653c79973

The thermal oscillator construction and independent noisy position-pair observations are inherited from Benchmarks 002–005. Stiffness and thermal energy are one. The nominal decay is 0.2; the sensor noise standard deviation is 0.35. The three null models have damped-frequency aliases 1, 2, and 3.

For alias $a$ and decay $d$,

$$
C_{a,d}(t)=e^{-d|t|}\left[\cos(2\pi at)+\frac{d}{2\pi a}\sin(2\pi a|t|)\right],
\qquad
\Sigma_{a,d}(t)=
\begin{pmatrix}1+\sigma^2&C_{a,d}(t)\\C_{a,d}(t)&1+\sigma^2\end{pmatrix}.
$$

The detector's design alternatives combine 12 aliases, $1\pm\{0.02,0.04,0.06,0.08,0.10,0.12\}$, with three decays, $\{0.16,0.20,0.24\}$. All 36 models and their uniform weights are fixed before evaluation.

Evaluation includes:

- The three exact nulls.
- Fresh aliases $1\pm\{0.027,0.053,0.093\}$, absent from the design grid.
- Outside-range aliases 0.84 and 1.16.
- Pure damping changes to 0.16 and 0.24 at alias 1, and the same damping changes at alias 1.053.
- A sensor stress: true noise SD 0.45, analyzed as 0.35, with physical dynamics unchanged.

Four schedules, two budget sizes, two budget regimes, and 16 scenarios give **256 cells and 768,000 simulated dataset evaluations**, with 3,000 independent replicates per cell. All three detectors see the same dataset within a cell; different cells use independent random streams. These are simulations of sufficient statistics, not laboratory experiments or continuous trajectories.

## Measurement design and its cost

The finite search considers 19 single lags from 0.05 to 0.95, and all 171 distinct equal-allocation two-lag pairs: **190 options**. Design depends only on declared models and costs, never evaluation outcomes.

For zero-mean Gaussian pair laws, the per-pair Bhattacharyya distance is

$$
B(\Sigma_0,\Sigma_1)
=\frac12\log\det\frac{\Sigma_0+\Sigma_1}{2}
-\frac14\log\det\Sigma_0-\frac14\log\det\Sigma_1.
$$

Distances add for independent pairs. For a schedule $\xi$ with equal lag weights, define $\bar B_\xi$ by averaging the per-lag distances. The two finite-grid objectives are:

$$
J_{\rm discrimination}(\xi)=\min_{i<j}\bar B_\xi(P_i,P_j),
\qquad
J_{\rm range}(\xi)=\min_{k,j}\bar B_\xi(Q_k,P_j).
$$

The first separates the three listed nulls; the second separates every design alternative from every null. These are different questions. The range objective is not standardized by each alternative's own optimum, nor optimized directly for measured rejection probability.

Robust discrimination design is established literature. [Dette, Melas, and Shpilev, Sections 2–3](https://arxiv.org/html/1309.4652v1#S3) study Bayesian and standardized maximin designs with a different, regression-based criterion. We inspected their motivation and definitions, not reproduced their algorithms or experiments. Our finite Gaussian-distance enumeration does not inherit their optimality theorems.

| Schedule | Selected lags | Pairs at equal-reading budget | Pairs at equal-time-proxy budget |
|---|---|---:|---:|
| Previous | 0.17, 0.43 | 1,024 | 1,024 |
| Local Fisher | 0.89 | 1,024 | 704 |
| Null discrimination | 0.15, 0.50 | 1,024 | 1,004 |
| Range maximin | 0.60, 0.85 | 1,024 | 768 |

The Fisher baseline searches the same finer 97-point grid used in Benchmark 005. Consequently, finite search resolutions are not identical; no continuous global optimum is claimed.

Time cost per pair is **$1+\text{mean lag}$**. A reference budget of $N_0$ pairs gives time budget $1.3N_0$. Affordable counts are rounded down to allow equal train/test halves at each lag. Time-mode design objectives divide information by this cost. The independently optimized schedules happen to be unchanged.

This is a declared cost proxy, not a measured experimental duration. The unit reset cost does **not** establish statistical independence: fresh equilibrium preparation is assumed. A real experiment must price equilibration, sensor readout, and possible parallel acquisition. Equal-reading and time-proxy outcomes are both retained.

## Alternative-blind tests

For the full experiment $D$, write the fixed alternative mixture as

$$
q(D)=\frac1{36}\sum_{k=1}^{36}p_{Q_k}(D),
\qquad
E(D)=\frac{q(D)}{\max_{j=1,2,3}p_{P_j}(D)}.
$$

Reject when $E>40$, corresponding to $\alpha=0.025$. This mixes **whole-experiment likelihoods**. It does not draw a new physical model independently for every pair.

For each true null $P_j$, pointwise $E\leq q/p_{P_j}$, so $\mathbb E_{P_j}E\leq1$. Markov's inequality gives rejection probability at most 2.5%. The true alternative need not lie in the mixture for this null guarantee—but its absence can destroy power.

The mixture/full-likelihood confidence construction and composite-null domination argument are explicitly discussed in [Wasserman, Ramdas, and Balakrishnan, Section 2, Theorem 3 and the following mixture remark](https://arxiv.org/html/1912.11436v4#S2). This is a finite implementation of an established construction, not a new test.

Comparators are the existing split-likelihood and chi-square concentration family checks, each at 2.5%. Unlike the mixture, their alternative fits/checks are not restricted to those 36 oscillators. Their different assumptions are part of the comparison. Always-warn has 100% detection and 100% null rejection; never-warn has zero of both. No calibrated oracle or exact alternative label is supplied.

Guarantees apply separately to each test, not to an unadjusted “reject if any test rejects” combination. Repeatedly inspecting several tests or datasets is not covered by the single-test claim.

## Results: useful tradeoffs, no universal winner

Mixture-test detection at the larger budget:

| Fresh shift | Fisher: equal readings | Range: equal readings | Fisher: time proxy | Range: time proxy |
|---|---:|---:|---:|---:|
| +2.7% | 63.53% | 46.13% | 37.93% | 30.97% |
| −9.3% | 54.67% | 100% observed | 32.90% | 100% observed |

For the −9.3% case at equal readings, the Fisher count is 1,640/3,000, with Wilson 95% interval 52.88–56.44%. The range count is 3,000/3,000, interval 99.87–100%. “100% observed” is not a proof of certain future detection. At +2.7%, Fisher's interval is 61.79–65.24%, and range's is 44.36–47.92%.

The range design therefore fixes an important gap but sacrifices local sensitivity. Its finite-grid worst-distance objective is not a guarantee of better power at every fresh point.

At +5.3% with equal readings, the mixture detects 46.87% on the old schedule and all 3,000 trials on the Fisher schedule. At the time-proxy budget, the range schedule detects 99.10% using 768 pairs. Improvements survive this particular cost assumption, not every possible laboratory cost model.

Across all 48 nominal-null cells and all three tests, the largest observed null-rejection rate is **0.433%**. The mathematical limit is 2.5%; the low observed rates indicate conservatism in this grid, not a stronger universal guarantee. All intervals are per-cell Monte Carlo intervals, not simultaneous statements.

![Fixed-rule detection comparison](../62%20Computational%20Labs/results/range_design/range_design.png)

The horizontal positions enumerate signed shifts by magnitude; connecting lines guide comparison between the discrete tested cases, not interpolation across a continuous parameter sweep.

## Stress tests change the interpretation

**Outside the design range.** At alias 0.84 with lag 0.89 and 1,024 pairs, the mixture detects **0/3,000** cases, versus **70.30%** for split likelihood and **90.33%** for concentration. The mixture's Wilson upper endpoint is 0.128%. This failure is not an information-theoretic impossibility: other checks extract useful evidence from the same observations.

**Damping without a frequency shift.** With alias 1, decay 0.16, and the range schedule, mixture detection is **1/3,000**, despite **19.98% response error** if nominal null 1 is used. Split and concentration each detect 10/3,000. Nonrejection does not certify accurate response.

**Sensor error without changed physics.** On the null-discrimination schedule with 1,024 pairs, changing only sensor noise SD from 0.35 to 0.45 yields **97.83% mixture rejection**. Physical response error relative to null 1 is zero. This is not a violation of the stated type-I guarantee: the observation law is outside the nominal null. It shows why rejecting a joint physics-and-sensor model cannot identify the physical cause.

Response errors above use the complex susceptibility at forcing angular frequency $2\pi$:

$$
m=\frac1{(2\pi a)^2+d^2},\quad
\chi_{a,d}(\nu)=\frac1{1-m\nu^2+2idm\nu},\quad
\epsilon=\frac{|\chi_{1,0.2}-\chi_{a,d}|}{|\chi_{a,d}|}.
$$

This is a declared reference-model discrepancy, not the error of an inferred model. The result file also reports the best response match among the three candidates.

## Post-hoc diagnosis, kept separate from the frozen comparison

After inspecting the failures, lab 23 computed exact Gaussian information distances without altering tests, schedules, weights, or thresholds. [[When More Data Cannot Rescue a Misfocused Test]] gives the derivation.

For fixed finite alternative and null sets, the mixture's asymptotic log evidence per pair is

$$
g=\min_j\bar D(P_*\Vert P_j)-\min_k\bar D(P_*\Vert Q_k).
$$

| Case | Nearest-null KL/pair | Nearest-alternative KL/pair | Growth $g$ |
|---|---:|---:|---:|
| Alias 0.84, lag 0.89 | 0.01432683 | 0.01269096 | +0.00163588 |
| Alias 1, decay 0.16, range schedule | 0.00033845 | 0.00337091 | −0.00303246 |
| Alias 1, decay 0.24, range schedule | 0.00030679 | 0.00277050 | −0.00246371 |

The outside-range case has **small positive** growth, so it is not an asymptotic impossibility for the mixture. Its finite-budget failure is consistent with weak relative evidence: the observed mean log evidence is −1.7065, below the rejection threshold $\log40=3.6889$. The positive asymptotic rate alone does not estimate finite-sample power.

Both pure damping cases have **negative** growth. The alternative grid excludes alias 1 even when its damping is wrong. Every alternative component is further from the observed truth than some null. Under the fixed schedule and model lists, mixture rejection probability therefore tends to zero with more independent pairs. This conclusion is analytic; a separate large-$N$ simulation was not run.

## Verification and next decision

- Lab 22: **21 checks passed**, including scalar/matrix likelihood agreement, Gaussian-distance identities, fixed-mixture algebra, null domination, budget allocations, finite scores, and enumerated design optima.
- Lab 23: **3 additional checks passed**, including unequal-variance Gaussian KL agreement and zero divergence under exact nulls.
- Exact Wishart sufficient-statistic sampling is inherited from the checked lab 21 implementation. Versions, protocol/script/dependency hashes, counts, per-cell Wilson intervals, and raw scores are recorded.
- These checks are implementation evidence, not scientific certification of the entire vault.

Reproduce from the vault's computational-lab directory:

~~~powershell
python 22_range_measurement_design.py
python 23_range_design_diagnostics.py
~~~

[Main results](../62%20Computational%20Labs/results/range_design/results.json) · [Tabulated results](../62%20Computational%20Labs/results/range_design/summary.csv) · [Post-hoc diagnostics](../62%20Computational%20Labs/results/range_design/posthoc_diagnostics.json)

The next useful experiment should separate sensor calibration from physical mismatch, and test a broader alternative fit without losing null control. It should also report uncertainty in response, not merely family rejection. Freeze fresh cases before that comparison. Thermal-memory reconstruction, nonlinear validation, and laboratory-data transfer remain unfinished gates.

[[Computational Lab Index]] · [[Release Status and Next Work]] · [[Physics Worldmap]]
