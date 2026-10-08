---
type: computational-benchmark
field: Cross-field
epistemic_status: effective
level: advanced
tags: [physics, research, model-checking, response, resonance, reproducibility]
created: 2026-09-04
updated: 2026-09-04
source_audit: explicit-model-derived-with-verified-statistical-method
note_maturity: expanded
---

# Benchmark 004 — Rejecting Inadequate Models

> [!important] Result
> Two established family-rejection checks can now return “none of these models.” With two observation lags and 512 independent pairs, they reject three clearly different omitted systems in every simulated trial. But both usually miss a 5% frequency shift near resonance, despite about 146% response error. Passing an observation-space fit check is not a general response-accuracy certificate.

[[Benchmark 003 — Noisy Measurements and False Confidence]] · [[Research Frontier — Identifiability Before Discovery]] · [[Computational Lab Index]]

## 1. What was fixed before the run?

The [protocol](../62%20Computational%20Labs/family_rejection_protocol.json) was written before generating these results. Its SHA-256 is:

    c108674d1caed27a96bdb04d533dc1c5a7b6eec52d975c8f506424b57fd2cfcb

Candidates remain thermal oscillators with damped frequencies $2\pi j$, $j=1,2,3$, stiffness and thermal energy equal to one, and decay rate 0.2. Each measured position has independent Gaussian sensor noise with standard deviation 0.2.

Compare a single lag 0.17 with two lags, 0.17 and 0.43. The first came from prior development; the second was fixed for this run, not optimized on these outcomes. Total budgets are 32, 128, and 512 independent position pairs, split equally across the chosen lags. Each pair requires two readings. There are no extra observations for the rejection methods.

Fresh alternatives were fixed before simulation:

| Scenario | Change from candidate family |
|---|---|
| Omitted 5 | Damped frequency $10\pi$, same decay |
| Omitted 7 | Damped frequency $14\pi$, same decay |
| Near 1 | Damped frequency $2\pi(1.05)$, same decay |
| Decay shift 2 | Damped frequency $4\pi$, decay 0.35 |
| Hidden pair | A collective coordinate combining independent oscillators 1 and 5 |

The previously inspected omitted oscillator 4 is **not** reused as unseen evidence.

For the hidden pair, $Q=\sqrt{0.65}\,q_1+\sqrt{0.35}\,q_5$, with independent thermal components. Its covariance is $0.65C_1+0.35C_5$. A force conjugate to $Q$ couples to each component with the same square-root weights, giving susceptibility $0.65\chi_1+0.35\chi_5$. This is a linear four-state physical system, not a nonlinear oscillator or a statistical mixture of two populations.

All eight scenarios, including three nominal candidates, are tested with 2,000 independent datasets per scenario/budget/design cell. The 96,000 dataset evaluations support 288,000 method evaluations. Methods and designs share common random numbers; these totals are not mutually independent experiments.

## 2. Three methods, one reading budget

All methods first use the full dataset to construct the fixed-mixture candidate confidence set from Benchmark 003, now at error level 0.025. This common adjustment leaves another 0.025 for family rejection.

- **Discrimination only:** retain the candidate set without a family check.
- **Split-likelihood check:** fit an unrestricted zero-mean Gaussian observation model on half the pairs at each lag, then compare its density with the best candidate density on the other half.
- **Concentration-bound check:** test the candidate-predicted fluctuation magnitudes using all pairs and conservative chi-square tail bounds.

Either rejection check overrides all point claims and returns an empty set, meaning “none of these candidates passed.” It is not an estimate of the correct missing model.

The baseline uses all readings for discrimination. The split test pays for its density fitting from that same budget. Splitting creates independent fitting and testing portions for the likelihood check; the family check and full-data candidate set are **not** mutually independent, nor do the error guarantees require them to be.

## 3. Why the split-likelihood rejection is controlled

Let $D_{\rm fit}$ and $D_{\rm test}$ be the predetermined halves. Fit a zero-mean Gaussian covariance separately at each lag, adding $10^{-6}V I$ for positive definiteness, where $V=1.04$ is the noisy marginal variance. The resulting test-data density $\widehat p$ is normalized conditional on $D_{\rm fit}$. Use

$$
E=\frac{\widehat p(D_{\rm test})}{\max_{j\in\{1,2,3\}}p_j(D_{\rm test})}.
$$

Reject if $E>40$. Under any true listed candidate $j$, the denominator is at least $p_j$. Conditional density normalization and Markov's inequality give

$$
\mathbb E_j[E\mid D_{\rm fit}]\leq1,\qquad
\Pr_j(E>40)\leq0.025.
$$

This instantiates the published split-likelihood test, not a new method. The source's Section 2, equation 9, Theorem 3 and proof were inspected directly. The multi-lag application uses independent product densities. [Wasserman, Ramdas and Balakrishnan, Universal Inference](https://arxiv.org/html/1912.11436v4#S2)

The fitted alternative is a density for checking observations, not a reconstructed physical dynamical model.

## 4. Independent concentration baseline

For each lag, transform the noisy pair $(X,Y)$ into

$$
U_+=(X+Y)/\sqrt2,\qquad U_-=(X-Y)/\sqrt2.
$$

For candidate $j$, the variances are $V+C_j(\tau)$ and $V-C_j(\tau)$. With $n$ independent pairs, each sum of squared standardized components is $\chi_n^2$. For $x>0$, the standard bounds are

$$
\Pr(Z>n+2\sqrt{nx}+2x)\leq e^{-x},\qquad
\Pr(Z<n-2\sqrt{nx})\leq e^{-x}.
$$

Set $x=\log(4L/0.025)$ for $L$ observation lags. The $4L$ accounts for two coordinates and two tails at each lag. A candidate fails if any bound fails; the **family** is rejected only if every candidate fails. If a candidate is true, family rejection implies its failure, so no additional factor of three is required.

The chi-square inequalities are established concentration results, attributed to [Laurent and Massart, Lemma 1 and its chi-square specialization](https://doi.org/10.1214/aos/1015957395). Their role here is a conservative known-Gaussian comparator, not a novel test.

## 5. What the guarantee does and does not say

For either check, a correctly specified listed family is rejected with probability at most 2.5%. Combining this with the 2.5% candidate-set exclusion bound gives, by the union bound, at most 5% probability of losing the true listed model from the final set.

Neither bound supplies a minimum detection probability against omitted models. Nor does it mean that a nonempty final set certifies response accuracy. Its guarantee depends on the exact independent Gaussian observation model and correctly specified candidate family under the null.

False reassurance is an accepted singleton whose complex susceptibility has more than 5% relative error at the declared angular frequency $2\pi$. Rejection and ambiguity make no point assertion. Conditional errors among accepted singleton decisions and unconditional false-reassurance rates are recorded separately.

## 6. Results: two lags, 512 total pairs

Each scenario/method entry represents 2,000 trials. Rejection percentages are:

| True scenario | Split-likelihood rejection | Concentration rejection | Ungated model's mean response error |
|---|---:|---:|---:|
| Nominal 1 | 0.15% | 0.05% | 0% |
| Nominal 2 | 0.15% | 0.05% | 0% |
| Nominal 3 | 0.25% | 0.15% | 0% |
| Omitted 5 | 100% | 100% | 28.04% |
| Omitted 7 | 100% | 100% | 30.66% |
| Near 1 | 7.45% | 11.85% | 146.18% |
| Decay shift 2 | 0.70% | 0.60% | 1.59% |
| Hidden pair | 100% | 100% | 53.83% |

For omitted 5, omitted 7, and the hidden pair, the two-lag checks reject in all 2,000 trials and eliminate the observed false singleton assertions. An observed 100% detection rate is not proof of detection probability one.

Across all tested nominal scenarios, designs, and budgets, the largest observed family false-rejection rate is 0.3%. This is an empirical observation; the mathematical upper bound remains 2.5%.

### Measurement diversity matters here

At the same 512-pair budget, the one-lag split check detects omitted 5 in 5.35% of trials and the hidden pair in only 0.25%. The corresponding two-lag rates are both 100%. For the concentration check, one-lag rates are 10.3% and 0.45%, again rising to 100% with two lags.

This is evidence for these cases that a second observation time adds information that many repetitions at the original time miss. It does not establish the chosen pair of lags as optimal.

### The important unresolved failure

For the 5% frequency-shift case, false singleton reassurance remains **92.55%** with the split check and **88.15%** with the concentration check. Accepted predictions have about **146.18%** relative complex-response error.

This is a small damped-frequency detuning, not a 5% change in every physical parameter. The mass and friction follow the thermal oscillator construction. The force frequency lies near the original model's resonance; its susceptibility is highly sensitive to detuning.

The exact transfer functions explain how nearby dynamics can have very different forced responses. The present study does **not** prove that no other test could detect this case with the same data. It has not yet separated insufficient information from conservatism or inefficiency of these particular tests.

The decay-shift case provides the opposite caution: it is outside the listed family but has only 1.59% response error at the selected frequency, below the 5% tolerance. Detecting every parameter mismatch and detecting every operationally harmful error are different objectives.

![Family rejection study](../62%20Computational%20Labs/results/family_rejection/family_rejection.png)

The figure averages scenarios equally to show broad trends. The table and per-scenario outputs are essential: averages hide the difficult near-resonance case.

## 7. Reproduce and inspect

From the computational-labs directory:

~~~powershell
python 20_family_rejection.py
~~~

The [source](../62%20Computational%20Labs/20_family_rejection.py) writes [results and checks](../62%20Computational%20Labs/results/family_rejection/results.json), [scores](../62%20Computational%20Labs/results/family_rejection/summary.csv), [replicate sufficient statistics, fitted covariances and likelihoods](../62%20Computational%20Labs/results/family_rejection/replicates.npz), and the figure.

All 18 implementation checks passed. They cover direct Gaussian likelihood agreement, orthogonal sum/difference statistics, component weight normalization, stationary position variance for each scenario, fitted positive definiteness, the likelihood-denominator inequality, and rejection overriding candidate claims. They do not turn observed detection power into a theorem.

Per-scenario Wilson intervals are approximate Monte Carlo intervals, not simultaneous bounds. The fixed seed and source/protocol hashes are recorded. All covariance and response data arise from exact Gaussian models; there is no time-step approximation. The simulations assume independent equilibrium pairs, not overlapping windows from a trajectory.

## 8. Research decision

The requested “none of these models” capability is implemented, with a published statistical construction and an independent concentration baseline. It fixes some of the previous study's failures but is not a trustworthy universal warning.

The next discriminating question is:

> Is the near-resonance failure due to a weak test, insufficient observations, or a measurement design that ignores response sensitivity?

Before building a new method, compare achievable discrimination under a known-alternative oracle with the two practical checks; examine information distances and response sensitivity together. A fresh protocol must use new detunings and noise settings. This already-inspected 1.05 case is now a development example.

Thermal-memory-method reproduction and nonlinear response tests remain unfinished. Nothing in this study establishes a new physical law or a novel general statistical method.

## Navigation

[[Research Frontier — Identifiability Before Discovery]] · [[Synthesis Session 001 — Response-Preserving Coarse-Graining]] · [[Synthesis Lab]] · [[Release Status and Next Work]] · [[Physics Worldmap]]
