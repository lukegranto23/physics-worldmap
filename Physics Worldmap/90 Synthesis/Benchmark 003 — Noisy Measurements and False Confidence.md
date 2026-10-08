---
type: computational-benchmark
field: Cross-field
epistemic_status: effective
level: advanced
tags: [physics, research, sampling, experimental-design, uncertainty, reproducibility]
created: 2026-09-04
updated: 2026-09-04
source_audit: explicit-model-derived-with-method-context
note_maturity: expanded
---

# Benchmark 003 — Noisy Measurements and False Confidence

> [!important] Outcome
> A measurement time selected before seeing simulated data substantially improves identification within a known three-oscillator family. But when the true oscillator is omitted from the candidate list, the same procedure becomes confidently wrong. This is a finite-family demonstration using established design and likelihood-ratio ideas, not a new physical law or a general failure-warning algorithm.

[[Benchmark 002 — The Sampling Boundary of Prediction]] · [[Research Frontier — Identifiability Before Discovery]] · [[Computational Lab Index]] · [[Synthesis Lab]]

## 1. What changed from the exact counterexample?

Benchmark 002 gave exact covariance functions. This study gives the inference procedure finitely many noisy observations. It asks:

1. Can an observation time chosen from the known candidate models improve discrimination?
2. Can an explicit “still ambiguous” answer reduce false reassurance?
3. What happens when none of the candidates is the truth?

This is a simpler, closed-candidate measurement-design control before reconstructing unknown memory kernels. It does **not** complete the roadmap's published thermal-memory-method reproduction or nonlinear study.

The [protocol](../62%20Computational%20Labs/measurement_design_protocol.json) fixes models, lags, noise, budgets, seeds, inference, confidence level, metrics, and omitted-model test before the first run. SHA-256:

    80c51c73ac8e48b2e631b36790226a2b578c6b4235f0b52f13b627b2a3c9d3a4

No design choice or threshold was changed after the outcomes were inspected. This is a local prospective record, not an independently registered study.

## 2. Observations and budget

Use the thermal oscillators of Benchmark 002 with $k=k_BT=\Delta=1$, decay $\alpha=0.2$, and candidate alias labels $j=1,2,3$. Their masses and frictions are completely specified within each candidate. The inference procedure knows this list, but not the true label.

For each independent equilibrium realization, collect two positions separated by lag $\tau$. Add independent Gaussian measurement noise of standard deviation 0.2 to each reading:

$$
X=(q(0)+\epsilon_0,\ q(\tau)+\epsilon_1),\qquad
X\mid j,\tau\sim\mathcal N(0,S_j(\tau)),
$$

$$
S_j(\tau)=
\begin{pmatrix}
V&C_j(\tau)\\
C_j(\tau)&V
\end{pmatrix},\qquad V=1+0.2^2=1.04.
$$

The covariance $C_j$ is derived in Benchmark 002. Independent measurement errors add to the diagonal, not to cross-covariance.

Budgets are 8, 32, and 128 **independent pairs**, respectively 16, 64, and 256 position readings. This does not mean overlapping pairs from a single correlated trajectory. Generating independent equilibrium realizations has a physical cost that is not modeled here. The design comparison matches reading counts, not instrument bandwidth or wall-clock experiment cost.

There are 2,000 independently generated datasets per truth/budget/design cell, totaling 120,000 dataset evaluations over 60 cells. Common random numbers couple designs for the same truth and budget; the 120,000 evaluations are not all mutually independent. Fresh realizations are held out from design selection, but the in-family physical systems themselves are known.

## 3. Five schedules, chosen without the truth label

| Design | Rule | Selected lag |
|---|---|---:|
| Integer | Keep the aliased observation spacing | 1.0 |
| Fixed off-grid | Use the lag already examined in Benchmark 002 | 0.137 |
| Random lag | Uniform choice from the grid, once per dataset | Varies |
| Maximin covariance gap | Maximize the smallest pairwise covariance difference | 0.13 |
| Maximin Gaussian distance | Maximize the smallest pairwise Bhattacharyya distance | 0.17 |

The search grid has 97 lags from 0.02 through 0.98. The random design holds its chosen lag constant across that dataset's pairs; it is not a mixed-lag or adaptive schedule.

For zero-mean Gaussian pairs, the distance used is

$$
D_B(S_i,S_j)=
\frac12\log\det\left(\frac{S_i+S_j}{2}\right)
-\frac14\log\det S_i-\frac14\log\det S_j.
$$

It is minus the logarithm of Gaussian square-root-density overlap. The choice accounts for covariance-dependent distinguishability instead of only raw covariance differences. This is optimal only for the declared maximin score on the finite grid—not a proof of globally minimal model-selection error or cheapest physical experiment.

Information-based design for model discrimination is established; [Daunizeau et al.](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1002280) develop related design criteria and discuss dependence on the candidate set. We use the elementary exact Gaussian distance, not a reproduction of their full neuroimaging method.

## 4. A confidence set with a precise, limited guarantee

For $N$ independent pairs, let $p_j(D)$ be the exact Gaussian likelihood. The point estimate maximizes this likelihood; ties within $10^{-10}$ log-likelihood units select the lowest label.

Separately, define the fixed mixture density and a set of retained models:

$$
p_{\rm mix}(D)=\frac13\sum_{i=1}^3p_i(D),\qquad
\mathcal C(D)=
\left\{j:\frac{p_{\rm mix}(D)}{p_j(D)}\leq\frac1\delta\right\},
\quad\delta=0.05.
$$

For any true listed model $j$, all the Gaussian densities are normalized and positive, so

$$
\mathbb E_j\left[\frac{p_{\rm mix}(D)}{p_j(D)}\right]
=\int p_{\rm mix}(D)\,dD=1.
$$

Markov's inequality therefore implies

$$
\Pr_j\{j\notin\mathcal C(D)\}\leq0.05.
$$

This is a finite-sample marginal coverage statement conditional on the correctly specified family and observation model. The same argument holds conditional on each independent random lag. No asymptotic chi-square likelihood-ratio approximation is needed. This simple likelihood-ratio/e-value construction belongs to existing statistical theory; see [Safe Testing](https://arxiv.org/abs/1906.07801).

This set is not a Bayesian credible set, not a guarantee that any particular answer is 95% likely to be correct, and not a bound on error conditional on choosing a singleton. A non-singleton means “ambiguous among these candidates.”

**Built-in limitation:** $\max_jp_j(D)\geq p_{\rm mix}(D)$, so the maximum-likelihood model is always retained. This procedure can never reject the entire candidate family. It is a discrimination tool, not an absolute goodness-of-fit test.

## 5. Noisy in-family results

At the middle budget of 32 pairs, pooling equal numbers of trials from the three true labels:

| Design | Point-estimate identification errors | Singleton answers | Truth retained in set | Joint false reassurance |
|---|---:|---:|---:|---:|
| Integer | 4,000 / 6,000 | 0 / 6,000 | 6,000 / 6,000 | 0 / 6,000 |
| Fixed off-grid | 35 / 6,000 | 5,755 / 6,000 | 5,997 / 6,000 | 3 / 6,000 |
| Random lag | 691 / 6,000 | 3,445 / 6,000 | 5,993 / 6,000 | 7 / 6,000 |
| Maximin covariance gap | 55 / 6,000 | 5,638 / 6,000 | 5,996 / 6,000 | 4 / 6,000 |
| Maximin Gaussian distance | 7 / 6,000 | 5,926 / 6,000 | 5,999 / 6,000 | 1 / 6,000 |

The designed Gaussian-distance lag identifies the model correctly in 99.883% of these trials. Its point-estimate error is 0.117%, versus 0.583% for the pre-existing fixed off-grid lag. These are descriptive Monte Carlo comparisons, not a claim of universal superiority or a hypothesis test chosen after inspecting results.

At 8 pairs its error is 7.9%; at 128 pairs zero errors were observed in 6,000 trials. Zero observed errors does not prove zero error probability. Integer-lag discrimination remains impossible: the deterministic tie-break always picks label 1, producing exactly one-third accuracy under the balanced label allocation. The confidence set correctly remains all three candidates.

False reassurance is defined before running as **a singleton set and more than 5% relative complex-susceptibility error** at angular frequency $2\pi$. The denominator is the magnitude of the true susceptibility. Reported joint rates count all trials; conditional rates among singleton decisions are separately recorded.

An always-warn baseline retains all candidates and never makes a singleton assertion. A never-warn baseline uses the point estimate on every trial. Their results are included per cell; the former's trivial safety comes with no identification, and the latter can be wrong without warning.

## 6. Omitted-truth stress test: confidence fails

Now the true oscillator is alias $j=4$, but the candidates remain $1,2,3$. The procedure is not told that the list is incomplete. This case was fixed in the protocol before simulation.

At 128 pairs, the Gaussian-distance design returns a singleton in **2,000 / 2,000 trials**, and all 2,000 have response error exceeding the predeclared 5% tolerance. Its mean relative response error is **25.035%**. The per-cell approximate Wilson 95% interval for the joint false-reassurance rate is **99.808%–100%**.

The fixed lag 0.137 and covariance-gap lag also give false reassurance in all 2,000 trials at that budget, but their mean response error is smaller: 5.479%. This matters: a design that discriminates the chosen candidates better need not be more robust to an omitted candidate.

This does not contradict the in-family coverage proof: its central assumption is false. The calculation does not demonstrate that every proposed model list will fail this way, nor that more data generally worsens prediction. It shows a particular failure that an always-nonempty relative comparison cannot diagnose.

![Noisy measurement comparison](../62%20Computational%20Labs/results/measurement_design/measurement_design.png)

## 7. Reproducibility and uncertainty

From the computational-labs directory:

~~~powershell
python 19_noisy_measurement_design.py
~~~

The [source](../62%20Computational%20Labs/19_noisy_measurement_design.py) produces [full results](../62%20Computational%20Labs/results/measurement_design/results.json), [summary scores](../62%20Computational%20Labs/results/measurement_design/summary.csv), and [replicate sufficient statistics, likelihoods and retained sets](../62%20Computational%20Labs/results/measurement_design/replicates.npz). The fixed seed, package versions, protocol hash, and source hash are recorded.

Eleven implementation checks passed: identical integer-lag covariances and likelihoods; positive covariance determinants; zero/symmetric Gaussian distance and valid affinity range; agreement with matrix determinant and direct Gaussian-likelihood formulas; retaining all models for identical likelihoods; nonempty confidence sets; and inclusion of every maximum-likelihood winner.

Passing these checks is not passing a discovery test. Calibration outcomes are reported as measurements, not converted into implementation assertions. Per-cell Wilson intervals describe finite Monte Carlo estimation and are approximate, not simultaneous bounds. Pooled Wilson intervals in the machine-readable summary are descriptive binomial approximations to stratified counts, not exact confidence guarantees for the equal-weight average. No paired significance claim is made between designs, which share underlying standard-normal draws.

The confidence theorem assumes known thermal parameters, known noise, independent pairs, and a listed true model. It does not cover nuisance-parameter fitting, instrument averaging, arbitrary online stopping, omitted dynamics, or nonlinear finite-amplitude forcing.

## 8. Decision: separate discrimination from falsification

This study advances the finite-data measurement control, but does not discover a new design criterion or identify unknown physics.

The next study must give the procedure an explicit **“none of these models”** outcome, evaluated on fresh data and physically distinct omitted-model cases. It should separate:

1. a measurement that distinguishes the candidate models;
2. an independent check of whether any candidate fits the observations;
3. a response prediction conditional on surviving both checks.

A goodness-of-fit check is also established statistics, not automatically a breakthrough. The research opportunity, if any, is a physically meaningful restricted guarantee or a demonstrated tradeoff between discrimination, falsification, and measurement cost beyond existing results. Any follow-up must freeze a new protocol rather than treat this already-inspected fourth oscillator as unseen validation.

## Navigation

[[Research Frontier — Identifiability Before Discovery]] · [[Synthesis Session 001 — Response-Preserving Coarse-Graining]] · [[Release Status and Next Work]] · [[Physics Worldmap]]
