---
type: research-derivation
field: Cross-field
epistemic_status: established
level: advanced
tags: [statistics, model-checking, information, research-limits]
created: 2026-09-04
updated: 2026-09-04
source_audit: elementary-derivation-with-explicit-assumptions
note_maturity: expanded
---

# When More Data Cannot Rescue a Misfocused Test

> [!important] Claim status
> An elementary consequence of likelihood asymptotics for fixed finite model lists—not a new theorem claim. Its application here explains a failure in [[Benchmark 006 — Unknown Shifts and Misfocused Tests]].

## The distinction

A test may control false alarms rigorously while having almost no ability to detect a particular error. A finite alternative mixture can even become **less willing to reject as data accumulates** when all its alternatives fit worse than a wrong null model.

This is not the same as insufficient information in the observations. It is a mismatch between what the test is designed to recognize and what actually changed.

## Assumptions

1. A fixed finite set of measurement lags has fixed positive sampling proportions $w_\ell$ as total pair count $N$ grows.
2. Pairs are independent within and across lag groups, with true density $p_{*,\ell}$.
3. Null models $P_j$ and alternative models $Q_k$ form fixed finite lists. Every alternative weight $\pi_k$ is fixed and positive, with sum one.
4. Densities are positive on the true support, and their log densities have finite absolute expectations under the truth. All Gaussian models used in Benchmark 006 satisfy these assumptions.
5. The threshold $1/\alpha$ stays fixed. The lists, weights, and schedule are not adaptively changed.

Write $\bar D(P_*\Vert M)=\sum_\ell w_\ell D(p_{*,\ell}\Vert p_{M,\ell})$ and let $\bar H_*$ be the corresponding average true differential entropy.

## Derivation

The strong law applied to each lag group gives, for every model $M$,

$$
\frac1N\log L_M(D_N)\ \longrightarrow\
-\bar H_*-\bar D(P_*\Vert M)
\qquad\text{almost surely}.
$$

Since the lists are finite, limits commute with their maxima. Also,

$$
\pi_{\min}\max_k L_{Q_k}
\leq \sum_k\pi_kL_{Q_k}
\leq\max_kL_{Q_k}.
$$

After taking logs and dividing by $N$, the discrepancy between the mixture and the best alternative vanishes: $|\log\pi_{\min}|/N\to0$. Thus, for

$$
E_N=\frac{\sum_k\pi_kL_{Q_k}(D_N)}{\max_jL_{P_j}(D_N)},
$$

we obtain

$$
\boxed{\frac{\log E_N}{N}\longrightarrow
\min_j\bar D(P_*\Vert P_j)-\min_k\bar D(P_*\Vert Q_k)=g.}
$$

If $g<0$, $E_N\to0$ almost surely; the fixed-threshold rejection probability tends to zero by bounded convergence of the rejection indicator. If $g>0$, rejection probability tends to one. If $g=0$, the displayed limit alone does not decide power.

This argument is a direct derivation using the strong law and finite log-sum bounds. The finite-mixture testing construction belongs to established universal-inference methodology; see the full-likelihood mixture remark in [Wasserman, Ramdas, and Balakrishnan, Section 2](https://arxiv.org/html/1912.11436v4#S2).

## Concrete thermal example

Take the true alias-1 oscillator with decay 0.16, nominal sensor noise SD 0.35, and equally allocated lags 0.60 and 0.85. The null list contains aliases 1, 2, 3, all with decay 0.20. The alternative list contains aliases $1\pm\{0.02,0.04,0.06,0.08,0.10,0.12\}$ and decays 0.16, 0.20, 0.24.

The exact Gaussian pair divergences give

$$
\min_j\bar D(P_*\Vert P_j)=0.0003384524,\qquad
\min_k\bar D(P_*\Vert Q_k)=0.0033709102.
$$

So $g=-0.0030324578<0$. The nearest null has alias 1, decay 0.20; the nearest mixture component has alias 1.02, decay 0.20. The list omits the pure damping alternative.

At 1,024 pairs, the frozen study saw 1 rejection in 3,000 trials. More importantly, the derivation predicts asymptotic failure for this unchanged test. Yet the nominal alias-1 susceptibility is wrong by about 19.98% at the declared forcing frequency.

The positive null divergence means the observations are not exactly identical to every candidate. A different consistent goodness-of-fit procedure can in principle detect the discrepancy with growing data. The problem here is not a universal observational impossibility.

## What changes the conclusion?

Adding the true model, or a closer alternative, can make $g$ positive. So can changing the observations. Data-dependent alternative fitting requires a valid separation or predictive construction to preserve null control; simply fitting and testing on the same observations does not retain the elementary guarantee.

Changing mixture weights alone cannot change the asymptotic rate when all weights remain fixed and positive and the support is unchanged. It can change finite-sample performance. This distinction prevents attempting to repair a missing alternative solely by retuning fixed weights.

The result says nothing about every possible test, growing model lists, continuous mixtures, sequentially changing designs, unknown noise calibration, or nonlinear systems without checking their additional assumptions.

## Research consequence

Track three separate questions: whether the data distinguish the physical change, whether the test can recognize it, and whether rejection identifies its cause. A model-checking alarm is not a response certificate or a discovery diagnosis.

[[Benchmark 005 — Information Limits and Better Measurements]] · [[Research Frontier — Identifiability Before Discovery]] · [[Synthesis Lab]]
