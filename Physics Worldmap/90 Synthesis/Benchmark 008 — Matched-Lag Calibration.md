---
type: computational-benchmark
field: Cross-field
epistemic_status: effective
level: advanced
tags: [physics, calibration, identifiability, sensors, reproducibility]
created: 2026-09-05
updated: 2026-09-05
source_audit: explicit-model-derived-with-primary-method-sources
note_maturity: expanded
---

# Benchmark 008 — Matched-Lag Calibration

> [!important] Outcome
> Dynamic measurements plus isolated noise-variance calibration cannot separate constructed changes in physical dynamics from correlated sensor errors. Noise-only calibration pairs at the same lags resolve those controls when their error law transfers. This exchanges detection power for valid attribution under a broader sensor model.

[[Benchmark 007 — Calibration Before Physical Attribution]] · [[Matched-Condition Calibration]] · [[Sensor Correlations and the Boundary of Physical Attribution]]

## 1. Exact challenge

Benchmark 007 constructed pairs of mechanisms with identical dynamic observations and identical isolated calibration observations:

- **Physical target:** changed oscillator parameters with independent sensor errors.
- **Sensor twin:** nominal oscillator parameters with correlated errors chosen to reproduce the target covariance.

The three target/twin pairs change decay from 0.20 to 0.145, change decay to 0.255, or shift damped frequency by +2.9%. All use the fixed lags 0.60, 0.85, 1.00.

The [protocol](../62%20Computational%20Labs/paired_calibration_protocol.json) was frozen before the first attempted execution. The first execution correctly failed validation: a proposed +6.7% sensor twin required an error cross covariance exceeding its variance at two lags, so its Gaussian noise covariance was not positive.

Before accepting results, protocol version 1.1 replaced only that malformed control with +2.9%, which satisfies positivity. Other printed outcomes were not used to tune tests, allocations, schedules, or thresholds. This amendment and its reason are stored in the protocol. Accepted-protocol SHA-256:

    c76ddf227ba0d0da507be89c6f8863ce934c222a96729d13566fc41649213dac

This is transparent local protocol control, not an external preregistration.

## 2. What paired calibration measures

Let the within-pair sensor covariance at lag $t_\ell$ be

$$
R_\ell=
\begin{pmatrix}
s_\ell&r_\ell\\r_\ell&s_\ell
\end{pmatrix}.
$$

In sum/difference coordinates its eigenvariances are

$$
\eta_{\ell,+}=s_\ell+r_\ell,\qquad
\eta_{\ell,-}=s_\ell-r_\ell.
$$

An isolated calibration reading samples only marginal variance $s$. It cannot observe $r_\ell$. A noise-only pair acquired with the same ordering and lag samples both eigenvariances.

For $K_\ell$ calibration pairs, the two coordinate sums of squares obey

$$
\frac{Z_{\ell,\pm}}{\eta_{\ell,\pm}}\sim\chi^2_{K_\ell}.
$$

The paired method gives each of the $2L$ eigenvariances a two-sided chi-square interval with per-tail error $\beta/(4L)$. Their simultaneous calibration error is at most $\beta=0.005$ by the union bound. It imposes no equality of noise variance or covariance across coordinates or lags.

For physical candidate $j$, dynamic coordinate variance is

$$
\Lambda_{j,\ell,\pm}=1\pm C_j(t_\ell)+\eta_{\ell,\pm}.
$$

Dynamic chi-square intervals use total error $\alpha_d=0.020$. Candidate $j$ survives when its implied noise-eigenvariance interval intersects the paired calibration interval at every lag and coordinate. Reject the physical family only if all three candidates fail.

When the true physical model is listed and the paired calibration law transfers,

$$
\Pr(\text{physical-family warning})\leq
\alpha_d+\beta=0.025.
$$

The isolated method uses one common variance interval and assumes $r_\ell=0$. Without calibration it permits any common nonnegative independent-noise variance. The naive reference fixes SD at 0.35.

## 3. A broader split-likelihood comparator

A second nuisance-aware method fits an arbitrary zero-mean Gaussian covariance from half of each dynamic dataset and evaluates its likelihood on the other half. For every null candidate, each test-coordinate variance is maximized independently over the paired calibration interval. This enlarges the null family and therefore upper-bounds its likelihood.

Dividing by that upper bound gives a conservative split likelihood ratio. Conditional on valid calibration coverage, the same 2% dynamic error bound applies; adding 0.5% calibration error gives 2.5%.

This uses the split-likelihood and null-upper-bound construction described by [Wasserman, Ramdas, and Balakrishnan, Sections 2 and 6](https://arxiv.org/html/1912.11436v4#S6). It is a specialized implementation, not a new statistical method or a reproduction of their empirical work.

## 4. Matched reading budgets

A dynamic pair or paired calibration pair costs two readings. An isolated calibration reading costs one. Paired observations are equally distributed across three lags; counts are rounded down to preserve equal allocation and train/test halves.

At the largest 16,384-reading budget:

| Mode | Calibration use | Dynamic pairs | Total readings used |
|---|---:|---:|---:|
| None | 0 | 8,190 | 16,380 |
| Isolated 25% | 4,096 isolated readings | 6,144 | 16,384 |
| Paired 25% | 2,046 pairs (682/lag) | 6,144 | 16,380 |

Thus the isolated and paired 25% modes have the same dynamic-pair count and essentially the same total reading cost. A wait-time proxy is recorded separately; no actual equilibration or instrument-switching duration was measured.

The accepted study includes **13 scenarios × 5 calibration allocations × 3 budgets = 195 cells**, with 3,000 independent simulations per cell: **585,000 dataset evaluations**.

## 5. Main result: twins separate only after matched-lag calibration

Physical-family warning rates for the exact low-decay twins at the largest budget:

| Calibration | Actual changed dynamics | Correlated-sensor twin |
|---|---:|---:|
| None | 17.70% | 17.77% |
| Isolated 25% | 93.17% | 93.53% |
| Paired 25% | **56.30%** | **0.43%** |

The no-calibration and isolated rates agree within Monte Carlo uncertainty because those observation laws are exactly identical. Isolated calibration becomes confident about marginal variance but still cannot locate the covariance change, so it calls both mechanisms physical.

With paired calibration, the sensor alarm fires in **3,000/3,000** sensor-twin trials. Joint labels are:

- Changed-physics target: **56.03% “physics only”**, 0.20% “sensor only,” 0.27% “both,” and 43.50% neither.
- Sensor twin: **99.57% “sensor only”**, 0.43% “both,” and no physics-only labels.

The physical target changes the candidate response by **27.47%** at forcing angular frequency $2\pi$. Paired calibration gives materially better attribution but lower physical detection than isolated calibration, because it admits a much broader sensor covariance.

The same pattern occurs in the other twins:

| Target | Paired moment physical detection | Twin physical warning | Twin sensor alarm |
|---|---:|---:|---:|
| Decay 0.145 | 56.30% | 0.43% | 100% observed |
| Decay 0.255 | 19.67% | 0.43% | 100% observed |
| Frequency +2.9% | 96.67% | 0.33% | 100% observed |

The corresponding best-candidate response discrepancies are 27.47%, 27.43%, and 87.37%. “100% observed” has Wilson 95% lower endpoint 99.87%, not certainty.

The relaxed split method remains much less powerful: 5.73%, 1.00%, and 38.60% target detection in these three cases. Its twin physical-warning rates are at most 0.033%. The comparison shows the price of sample splitting and the deliberately loose null likelihood; broad support alone did not produce a strong finite-sample detector.

![Paired calibration separates dynamic-law twins](../62%20Computational%20Labs/results/paired_calibration/paired_calibration.png)

Intervals in the figure are per-cell Wilson 95% Monte Carlo intervals, not simultaneous confidence bands.

## 6. Control behavior and failure of transfer

Across paired-calibration cells with exact nominal physical dynamics, the largest observed moment physical-warning rate is 0.367%. Across transferred sensor-only cases it is 0.567%. The analytic bound remains 2.5%; descriptive maxima do not strengthen it.

The largest observed sensor alarm under nominal independent noise is 0.733%. Its target probability is at most 0.5%; inspecting a maximum across many cells can exceed that level through Monte Carlo and selection variation. No simultaneous claim is made.

Two stress cases deliberately violate transfer:

1. Dynamic sensor errors mimic lower decay, but paired calibration errors are independent. At the largest 25% allocation, the method raises a physical warning in **56.93%** and a sensor alarm in 0.47%. The cause is sensor correlation, yet calibration says otherwise.
2. Dynamic sensor errors are independent, but calibration pairs have the mimic correlation. The method raises both sensor and physical warnings in **100%** and **68.60%**, respectively, despite nominal physical dynamics.

These are not failures of the conditional guarantee. They show that “same lags” is insufficient if calibration does not reproduce the acquisition conditions relevant to the physical measurement.

## 7. What has and has not been learned

This study resolves the exact finite-pair ambiguity from [[Sensor Correlations and the Boundary of Physical Attribution]] under a stronger measurement. It supports four restricted conclusions:

1. Calibration must target covariance structure, not merely marginal variance.
2. Matching calibration to measurement lags enables attribution in the constructed controls.
3. Allowing richer sensor error lowers physical-detection power at fixed cost.
4. Calibration transfer is itself an empirical hypothesis, not a bookkeeping assumption.

It does **not** show that real sensors have these correlations, that paired calibration always transfers, or that a warning identifies novel dynamics. It does not create a continuum response-confidence set. It assumes zero-mean Gaussian errors, known equilibrium variance, independent freshly prepared trials, and access to a zero reference.

NIST's uncertainty guidance emphasizes that the measurement process should include significant sources of variability and covariance terms; see [NIST TN 1297, Appendix A](https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-appendix-law-propagation-uncertainty). Our paired construction is an explicit controlled example, not a reproduction of that general guidance.

## 8. Verification and next experiment

Lab 26 passed **27 checks**, including:

- positive-definite sensor covariances for all amended mimic controls;
- exact covariance equality of every physical target and sensor twin;
- orthogonal noise-coordinate diagonalization;
- paired calibration interval nesting;
- pointwise domination by the relaxed null likelihood;
- budget, finite-score, and positive-covariance checks.

All cell results, source hashes, per-cell intervals, classifications, and score arrays are stored. The failed validation attempt is disclosed in the amended protocol rather than erased from the study history.

From the computational-lab directory:

~~~powershell
python 26_paired_sensor_calibration.py
~~~

[Protocol](../62%20Computational%20Labs/paired_calibration_protocol.json) · [Results](../62%20Computational%20Labs/results/paired_calibration/results.json) · [Table](../62%20Computational%20Labs/results/paired_calibration/summary.csv)

Next, leave the constructed Gaussian world: use a published experimental or synthetic instrument-noise dataset with drift and colored-noise diagnostics, then reproduce a thermal-memory identification baseline. Paired calibration should be treated as one measurement-design control, not as the endpoint of the research program.

[[Computational Lab Index]] · [[Release Status and Next Work]] · [[Physics Worldmap]]
