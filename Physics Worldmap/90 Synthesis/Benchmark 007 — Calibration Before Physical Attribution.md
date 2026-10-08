---
type: computational-benchmark
field: Cross-field
epistemic_status: effective
level: advanced
tags: [physics, calibration, model-checking, uncertainty, reproducibility]
created: 2026-09-04
updated: 2026-09-04
source_audit: explicit-model-derived-with-primary-method-sources
note_maturity: expanded
---

# Benchmark 007 — Calibration Before Physical Attribution

> [!important] Result
> Under a stable independent-noise model, independent calibration can improve detection while limiting mistaken physical-family warnings. In one fixed-budget case, damping-change detection rises from 15.10% to 89.83%. Calibration drift breaks that interpretation. A separate exact example shows that correlated sensor errors can mimic changed dynamics even when marginal noise variance is calibrated perfectly.

[[Benchmark 006 — Unknown Shifts and Misfocused Tests]] · [[Sensor Correlations and the Boundary of Physical Attribution]] · [[Research Frontier — Identifiability Before Discovery]]

## 1. Frozen comparison

The [protocol](../62%20Computational%20Labs/sensor_calibration_protocol.json) was fixed before simulation. This is local protocol freezing, not an external preregistration. SHA-256:

    b78c89bb623b6960008ef990c6a7c70560ab0a411fad98cda1d92231a9023da6

The physical family remains the thermal Gaussian oscillator with stiffness and thermal energy one. Its three nominal members have damped-frequency aliases 1, 2, 3 and decay 0.2. Dynamic observations are independent, freshly prepared position pairs with independent zero-mean sensor noise. Unlike earlier tests, the nuisance-aware methods allow its variance $s=\sigma^2$ to be any nonnegative real number, not a finite grid.

Fresh evaluation changes are:

- Frequency shifts ±4.1% and ±11.3%.
- Decay parameters 0.13 and 0.27.
- Sensor noise SDs 0.28, 0.48, 0.65, compared with nominal 0.35.
- Combined changes, and a deliberate transfer failure: calibration noise SD 0.28, dynamic noise SD 0.65.

The three exact nominal cases are included. There are **15 scenarios × 3 reading budgets × 3 calibration allocations × 2 schedules = 270 cells**, each with 3,000 independent simulations: **810,000 dataset evaluations**. Within a cell, methods use the same dynamic data; different cells have independent streams.

“Damping-only” is shorthand for changing the decay parameter while keeping damped frequency fixed. In this constructed family, mass $m=[(2\pi a)^2+d^2]^{-1}$ and friction $2dm$ change accordingly. It is not literally a fixed-mass friction intervention.

## 2. Calibration is an observation, with a cost

Each calibration trial measures noise at a known zero reference:

$$
z_i\sim N(0,s),\qquad Z=\sum_{i=1}^{K}z_i^2,\qquad Z/s\sim\chi^2_K.
$$

The mean is known to be zero, so the degrees of freedom are **$K$**, not $K-1$. For $\beta=0.005$,

$$
I_{\rm cal}=
\left[
\frac{Z}{\chi^2_{1-\beta/2,K}},
\frac{Z}{\chi^2_{\beta/2,K}}
\right]
$$

has 99.5% coverage. Without calibration, use $I_{\rm cal}=[0,\infty)$. The usual chi-square variance interval is described by [NIST](https://www.itl.nist.gov/div898/handbook/prc/section2/prc231.htm); that page estimates the mean and therefore uses $N-1$. The known-zero variant above follows directly from a sum of squared standard normals.

Total reading budgets are 512, 2,048, and 8,192. Calibration uses 0%, 12.5%, or 25%. Each dynamic pair costs two readings; each calibration observation costs one. Counts are rounded down for equal train/test halves at every lag.

Two schedules are frozen: **(0.60, 0.85)** and **(0.60, 0.85, 1.00)**. The integer lag is a damping-sensitive complement: for the nominal integer aliases, $C_{a,d}(1)=e^{-d}$. It is not a new global design optimum.

For the 8,192-reading three-lag comparison:

| Calibration allocation | Calibration readings | Dynamic pairs | Used readings |
|---|---:|---:|---:|
| 0% | 0 | 4,092 | 8,184 |
| 25% | 2,048 | 3,072 | 8,192 |

Unused readings arise only from equal-allocation rounding. A lag-wait proxy is also recorded, but the comparison is **reading-budget matched**, not actual laboratory-time matched. Preparation, locking a zero reference, drift monitoring, and parallel acquisition have not been priced experimentally.

## 3. A physical-family check with an unknown noise variance

At lag $t$, the sum and difference coordinates have variances

$$
\lambda_{j,\pm}(t)=1+s\pm C_j(t).
$$

For $n_t$ independent pairs, let $U_{t,\pm}$ be the sums of squared normalized sum/difference coordinates. Under a true candidate,

$$
\frac{U_{t,\pm}}{\lambda_{j,\pm}(t)}\sim\chi^2_{n_t}.
$$

With $L$ lags and dynamic error budget $\alpha_d$, take chi-square quantiles $q_{\rm lo},q_{\rm hi}$ at tail probabilities $\alpha_d/(4L)$ and $1-\alpha_d/(4L)$. Each coordinate implies an interval for the same nuisance parameter:

$$
s\in
\left[
\frac{U_{t,\pm}}{q_{\rm hi}}-(1\pm C_j(t)),
\frac{U_{t,\pm}}{q_{\rm lo}}-(1\pm C_j(t))
\right].
$$

Candidate $j$ survives if all these intervals intersect $I_{\rm cal}$ and $[0,\infty)$. Reject the physical family only when no candidate survives. This is an exact interval intersection, not numerical maximization over a noise grid.

For calibrated methods, $\alpha_d=0.020$ and $\beta=0.005$. If the true physical model is a candidate and the calibration law transfers to dynamics, a union bound gives

$$
\Pr(\text{physical-family rejection})\leq\alpha_d+\beta=0.025.
$$

There is no additional factor for the three null candidates: when one is true, its survival suffices to prevent rejecting the family. Without calibration, the full nuisance range always includes the true variance, and $\alpha_d=0.025$.

## 4. Comparators and the broader alternative fit

| Method | Sensor treatment | Relevant limitation |
|---|---|---|
| Naive exact moment check | Fixes SD at 0.35 | No false-physical-warning guarantee under other noise |
| Plug-in moment check | Fixes variance at $Z/K$ | Ignores calibration uncertainty; unavailable without calibration |
| Nuisance moment check | Intersects noise intervals | Coverage requires Gaussian pair law and calibration transfer |
| Relaxed split likelihood | Fits arbitrary Gaussian covariance on half the data; bounds the null likelihood on the other half | Safe relaxation can discard useful null constraints and lose power |
| Previous fixed mixture | Retains Benchmark 006's 36 alternatives and nominal SD 0.35 | Ignores calibration; both model-list and noise limitations remain |

The split numerator is a normalized, zero-mean, positive-definite Gaussian fit at each lag, not restricted to oscillators on the old alternative grid. This directly addresses the fixed-support failure from [[When More Data Cannot Rescue a Misfocused Test]].

For a null candidate, calibration bounds each coordinate variance between $1+s_{\rm lo}\pm C_j$ and $1+s_{\rm hi}\pm C_j$. The maximum coordinate log likelihood occurs at the sample second moment clipped to those limits. Maximizing each coordinate and lag separately enlarges the allowed null family, hence upper-bounds its likelihood. Using that bound in the denominator preserves split-test validity, conditional on calibration coverage, at the expense of power.

The split construction and the validity of an upper-bounded null denominator are established methods. We inspected [Wasserman, Ramdas, and Balakrishnan, Section 6](https://arxiv.org/html/1912.11436v4#S6). This study implements a simple analytic relaxation; it does not reproduce all that paper's experiments.

Each method has its own threshold. The 2.5% claim does not cover choosing whichever test rejects, repeated peeking, or an unadjusted combination of methods.

## 5. Main outcome: calibration and timing complement each other

For true alias 1, decay 0.13, nominal sensor noise, and the 8,192-reading budget, nuisance-moment detection is:

| Schedule | No calibration | 25% calibration |
|---|---:|---:|
| Two range lags | 3.70% | 10.83% |
| Range lags plus integer lag | 15.10% | **89.83%** |

For the three-lag comparison, counts are 453/3,000 and 2,695/3,000. Wilson 95% intervals are **13.86–16.43%** and **88.70–90.86%**. The best nominal-candidate susceptibility differs from truth by **34.97%** at forcing angular frequency $2\pi$.

The gain survives spending one quarter of the reading budget on calibration, but it is not a general 90% detector. At the smaller 2,048-reading budget, the same three-lag comparison is 2.47% versus 11.40%.

The calibrated broader split fit reaches **20.67%** in the large-budget damping case, compared with **25.67%** for the fixed mixture and 89.83% for nuisance moments. Broadening the alternative does not guarantee a finite-sample improvement when a loose denominator and sample splitting consume power. Without calibration, the relaxed split fit detects none of these 3,000 damping trials.

## 6. Sensor warnings are separate from physical-family warnings

The calibration sensor alarm asks whether nominal variance $0.35^2$ lies outside $I_{\rm cal}$. Under nominal calibration noise its error probability is at most 0.5%. It says nothing by itself about whether calibration remains valid during dynamic acquisition.

For unchanged alias-1 dynamics, sensor SD 0.48, the three-lag schedule, 8,192 readings, and 25% calibration:

- Sensor alarm: **3,000/3,000**.
- Nuisance-moment physical-family warning: **24/3,000 = 0.80%**, Wilson interval 0.54–1.19%.
- Joint “sensor only” label: **99.20%**.
- Naive physical-family warning: **3,000/3,000**.

Under the experiment's assumptions, the separated warnings are useful. They are not causal proof. In particular, the sensor alarm tests only the noise sampled in calibration trials.

Across the 108 cells with unchanged physical dynamics and valid calibration transfer, the largest observed physical-family rejection rates are **1.367%** for nuisance moments and **0.133%** for relaxed split. These descriptive maxima do not strengthen their analytic 2.5% guarantee.

Plug-in calibration reaches **5.833%** mistaken physical-family rejection in one sensor-only cell: 2,048 readings, 12.5% calibration, alias 2, SD 0.65, three lags. Its per-cell Wilson interval is 5.05–6.73%. Reporting the largest inspected cell is descriptive, not a simultaneous inference. Treating a calibration estimate as exact did not preserve the desired control.

Observed calibration coverage across calibrated cells ranges from 99.13% to 99.80%; the analytic coverage is 99.5%. Monte Carlo variation around the stated level is expected.

## 7. Deliberate failure: calibration does not transfer

Keep nominal physical dynamics, but let calibration SD be 0.28 and dynamic SD 0.65. At the large budget and 25% calibration, both nuisance methods produce **3,000/3,000 physical-family warnings** and label all trials “both.”

Without calibration, the nuisance-moment method gives just **0.333%** physical-family rejection in the three-lag setting. Tight but irrelevant calibration can therefore be worse than honestly allowing a broad noise range.

This does not contradict the theorem: its transfer assumption is false. It falsifies an unrestricted interpretation of the warning as evidence that the physical dynamics changed.

![Calibration tradeoffs and transfer failure](../62%20Computational%20Labs/results/sensor_calibration/sensor_calibration.png)

The dotted 2.5% line is a reference for methods and cases satisfying the appropriate null assumptions, not a guarantee for the transfer-failure column.

## 8. Response uncertainty is still conditional

The result file records the response diameter of surviving nominal candidates, singleton frequency, and missed cases whose best nominal response differs by more than 5%. It does **not** claim coverage over an unknown continuum of physical systems.

In the large-budget calibrated three-lag damping example, 10.17% of trials retain a singleton response. Every nonempty set has diameter zero, although the true response differs from the candidate by 34.97%. A narrow set over the wrong physical family remains misleading.

The post-hoc note [[Sensor Correlations and the Boundary of Physical Attribution]] strengthens this warning: isolated variance calibration can leave exact sensor-versus-dynamics ambiguity. It also derives the nonzero response-set diameter required if coverage is demanded over both indistinguishable mechanisms.

## 9. Verification, provenance, and next step

Lab 24 passed **16 implementation checks**: variance-pivot quantiles, coordinate/matrix likelihood agreement, clipped scalar optima, interval nesting, pointwise null domination, budget constraints, finite scores, and positive sample covariance.

Lab 25 adds **12 checks** for the separately labeled post-hoc correlated-sensor example. It does not alter the frozen protocol or its outcomes.

Stored outputs include versions, hashes of protocols/scripts/dependencies, all cell results, per-cell Wilson intervals, and sufficient score arrays. Missing plug-in or sensor decisions without calibration are explicitly marked unavailable, not counted as negative results.

From the computational-lab directory:

~~~powershell
python 24_sensor_calibration.py
python 25_sensor_dynamics_ambiguity.py
~~~

[Main results](../62%20Computational%20Labs/results/sensor_calibration/results.json) · [Table](../62%20Computational%20Labs/results/sensor_calibration/summary.csv) · [Exact counterexample](../62%20Computational%20Labs/results/sensor_calibration/correlated_sensor_counterexample.json)

Next: use noise-only **pairs at the actual dynamic lags**, not just isolated variance calibration, and test whether their correlation law transfers. A response certificate must admit sensor uncertainty explicitly. Freeze fresh parameters before testing; thermal-memory reconstruction and nonlinear validation remain separate unfinished requirements.

[[Computational Lab Index]] · [[Release Status and Next Work]] · [[Physics Worldmap]]
