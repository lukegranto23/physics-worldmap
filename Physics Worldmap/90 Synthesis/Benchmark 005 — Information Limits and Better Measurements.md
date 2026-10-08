---
type: computational-benchmark
field: Cross-field
epistemic_status: effective
level: advanced
tags: [physics, research, resonance, information, experimental-design, reproducibility]
created: 2026-09-04
updated: 2026-09-04
source_audit: explicit-model-derived-with-primary-method-sources
note_maturity: expanded
---

# Benchmark 005 — Information Limits and Better Measurements

> [!important] Result
> The previous failure has multiple causes. Some observation budgets provably cannot support reliable detection. In other settings, a standard sensitivity-based choice of observation time dramatically improves the existing checks. An information-rich oracle also exposes gaps, but it knows the true alternative and is not a deployable, equally informed competitor.

[[Benchmark 004 — Rejecting Inadequate Models]] · [[Research Frontier — Identifiability Before Discovery]] · [[Computational Lab Index]]

## 1. Fresh test rules

The [protocol](../62%20Computational%20Labs/oracle_detection_protocol.json) was written before the first run. SHA-256:

    a79faec4ceb8949e441ce46db0412db08b3035e1c1a4f2523bf74df73a731c20

Use the same thermal oscillator construction, but replace the previously inspected 5% detuning and sensor-noise level:

- Damped-frequency shifts: **+1.5%, +3.5%, +7.5%** from oscillator 1.
- Sensor-noise standard deviations: **0.1, 0.35, 0.7**.
- Budgets: **64, 256, 1,024 independent position pairs**.
- Schedules: previous lags **0.17 and 0.43**, or one lag chosen from a frozen grid by local Fisher information.
- Rejection level: **2.5%**.

These give 54 alternative/noise/budget/schedule cells. Each has 100,000 separate null calibration replicates and 5,000 independent evaluation datasets under each of the null and alternative: 5.4 million calibration evaluations and 540,000 evaluation datasets.

The oracle is calibrated using simulation, not experimental measurements. Practical checks receive no calibration observations or true-alternative parameters. Observation budgets are equal in number of readings, not elapsed laboratory time; each pair is a fresh equilibrium realization.

## 2. Three references with different meanings

### Mathematical information bound

Let $P_0$ and $P_1$ be the complete noisy-data distributions under oscillator 1 and the specified detuned alternative. Any test with null rejection probability at most $\alpha$ satisfies

$$
\Pr_1(\text{reject})\leq
\alpha+\operatorname{TV}(P_1,P_0).
$$

Using Pinsker's inequality in either direction gives

$$
\Pr_1(\text{reject})\leq
\min\left\{1,\ \alpha+
\sqrt{\frac12\min\left[D_{\rm KL}(P_1\Vert P_0),
D_{\rm KL}(P_0\Vert P_1)\right]}\right\}.
$$

This is an upper bound, not an estimate of attainable power. It may become uninformative at one. The total-variation convention is half the density $L_1$ difference; KL uses natural logarithms. [Canonne, Section 1 and Lemma 2](https://arxiv.org/html/2202.07198#S1)

For each lag, the Gaussian covariance eigenvalues are $\lambda_\pm=V\pm C(\tau)$, where $V=1+\sigma_{\rm noise}^2$. With eigenvalue ratios $r_\pm=\lambda_{\pm,1}/\lambda_{\pm,0}$, the exact divergence per independent pair is

$$
D_{\rm KL}(P_{1,\tau}\Vert P_{0,\tau})
=\frac12\sum_{\pm}(r_\pm-1-\log r_\pm).
$$

Independent-pair divergences add across the declared lag allocation. This calculation uses the full observation distribution, not an estimated warning statistic.

### Known-alternative oracle

The oracle uses the exact likelihood ratio $p_1(D)/p_0(D)$. With the exact population threshold, this is the most powerful level-$\alpha$ test of the specified simple null against the specified simple alternative. [Neyman–Pearson lemma, Berkeley theoretical-statistics notes](https://stat210a.berkeley.edu/fall-2024/reader/hypothesis-testing.html)

Here its threshold is approximated with independent null simulations. For $M=100{,}000$, choose the $k$th ordered score, where

$$
k=\lceil(M+1)(1-\alpha)\rceil=97{,}501.
$$

Exchangeability of a fresh continuous null score with the calibration scores gives marginal rejection probability $(M+1-k)/(M+1)=2500/100001<0.025$. This is marginal over calibration randomness; conditional on a particular threshold, null size can vary.

Consequently the plotted oracle power is a numerical approximation to the ideal Neyman–Pearson reference, **not a rigorously computed power ceiling**. Evaluation intervals do not include threshold-calibration uncertainty.

### Practical checks

Reuse the split-likelihood and concentration-bound family-rejection checks from Benchmark 004. They still test the entire listed family, oscillators 1, 2, and 3, without knowing the true detuning.

The oracle only needs to control null 1 and knows the exact alternative. Its theoretical optimality makes it a useful upper reference for family-valid tests, but the information and null constraints are different. A large gap cannot be attributed uniquely to a poor implementation or one conservative threshold. Power loss in universal split tests is already studied, for example in [Gaussian Universal Likelihood Ratio Testing](https://arxiv.org/abs/2104.14676).

## 3. Choose the measurement before seeing the alternatives' data

For an observation pair at lag $\tau$, compute the scalar Fisher information for the alias parameter $a$ at the known null $a=1$:

$$
I_a(\tau)=\frac12\left(\frac{\partial C_a(\tau)}{\partial a}\right)^2
\left[\frac{1}{(V+C_a(\tau))^2}
+\frac{1}{(V-C_a(\tau))^2}\right]_{a=1}.
$$

Maximize it over 97 lags from 0.02 to 0.98. The derivative is calculated by centered differences; halving the step is checked. No alternative labels or simulated outcomes enter the design.

| Sensor-noise SD | Selected lag |
|---:|---:|
| 0.10 | 0.91 |
| 0.35 | 0.89 |
| 0.70 | 0.84 |

This is a standard local parameter-sensitivity criterion. It is not optimal for every alternative, a robust worst-case design, or a direct optimization of response error. The longer lag may cost more waiting time; the comparison matches pair counts only.

## 4. A concrete improvement

For a **3.5% frequency shift**, sensor-noise SD **0.35**, and **1,024 pairs**:

| Detector | Earlier two-lag schedule | Fisher-selected lag 0.89 |
|---|---:|---:|
| Known-alternative oracle | 58.36% | 99.92% |
| Split-likelihood family check | 2.52% | 59.16% |
| Concentration family check | 4.24% | 93.12% |

The concentration check improves from **212/5,000** detections to **4,656/5,000**. Its approximate per-cell Wilson 95% intervals are 3.72–4.83% and 92.38–93.79%, respectively.

The original oscillator's relative complex-response error for this alternative is **104.54%** at the fixed force frequency $2\pi$. The changed measurement schedule helps detect a mismatch that matters physically; it does not repair the model or estimate the corrected response.

This addresses one cause of the previous failure: at equal reading count, an observation time sensitive to local detuning can reveal much more than the earlier candidate-discrimination schedule. It is a successful controlled example, not a general design breakthrough.

## 5. A genuine information-limited example

For a **1.5% frequency shift**, noise SD **0.35**, **64 pairs**, and the earlier two-lag schedule:

- Using the original oscillator would give **46.13% response error**.
- The known-alternative oracle detects the mismatch in **3.66%** of evaluation trials.
- The analytic upper bound is **14.54% detection probability** for any test restricted to these observations and a 2.5% null-rejection level.

The bound rules out a 90%-power detector in this exact information setting, even one with unlimited computation. It does not rule out better sensors, more observations, a different schedule, or forcing experiments.

Across the frozen grid, **17 of 54 cells** have an analytic power bound below 50%. That count depends on the declared grid and criterion; it is not a prevalence estimate for physical systems.

## 6. What remains between the bound and a useful method?

The protocol also flagged cells with oracle power above 80% but both practical checks below 40%; **seven cells** meet this descriptive criterion. The flag was fixed before evaluation.

These gaps point to available information under the oracle's stronger knowledge and weaker null constraints. They do not show that an alternative-blind family test can automatically attain oracle power. The next comparison needs a detector with a declared continuous alternative range and uniform control over the candidate null family.

The two failure categories can coexist: the practical checks may discard information in a setting where even the optimal test still has limited power. A high upper bound does not establish detectability; a low practical detection rate alone does not establish impossibility.

![Detection limits and measurement timing](../62%20Computational%20Labs/results/oracle_detection/oracle_detection.png)

The figure shows the predeclared middle noise level. All noise levels and per-cell null rejection rates are preserved in the results.

## 7. Reproducibility and validation

From the computational-labs directory:

~~~powershell
python 21_oracle_detection_limits.py
~~~

The [source](../62%20Computational%20Labs/21_oracle_detection_limits.py) reuses the checked rejection functions in lab 20. It saves the dependency hash as well as its own source and protocol hashes.

Outputs: [full results](../62%20Computational%20Labs/results/oracle_detection/results.json), [scores by case](../62%20Computational%20Labs/results/oracle_detection/summary.csv), [evaluation detection scores and design curves](../62%20Computational%20Labs/results/oracle_detection/scores.npz), and the plot.

Gaussian pair sufficient statistics are generated exactly using a two-dimensional Wishart/Bartlett construction; raw time trajectories are not simulated. Calibration scores need not be stored because the protocol, seeds, and threshold rule reproduce them. Scores preserve evaluation-level outcomes for audit.

All **10 implementation checks** passed: derivative refinement at three noise levels, calibration-rank validity and marginal size, zero KL for identical models, matrix versus diagonal KL, matrix versus scalar Fisher information, and Wishart mean/positive-definiteness checks. The mean check is a finite sampling audit, not a proof.

Per-cell Wilson intervals are approximate Monte Carlo intervals and are not simultaneous. Oracle null rejection is evaluated independently; observed finite-sample rates can lie above 2.5% without contradicting the marginal rank-calibration guarantee. Practical checks retain their stated null bounds under the known Gaussian family; no unknown-noise or correlated-trajectory guarantee is added.

## 8. Next research decision

We now have an explicit distinction between provably insufficient observations and settings in which sensitivity-based timing greatly improves detection. The next target is **response-sensitive experimental design that remains valid over a range of possible detunings**, not a detector supplied with the true alternative.

Before claiming a contribution, compare such a design with established local-Fisher, model-discrimination, robust-design, and likelihood methods, including acquisition-time cost. These newly inspected detunings are now development cases. A subsequent protocol must reserve new alternatives.

No new physical law, universal detector, nonlinear validation, or thermal-memory-method reproduction is claimed.

## Navigation

[[Research Frontier — Identifiability Before Discovery]] · [[Synthesis Lab]] · [[Release Status and Next Work]] · [[Physics Worldmap]]
