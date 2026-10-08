---
type: computational-benchmark
field: Statistical Physics
epistemic_status: effective
level: advanced
tags: [linear-response, camera-exposure, motion-blur, uncertainty-quantification, calibration]
created: 2026-09-16
updated: 2026-09-16
note_maturity: expanded
source_audit: derived-with-primary-prior-art-and-independent-computational-review
---

# Benchmark 013 — Camera Exposure and Response Uncertainty

A position camera supplies different information from the coarse velocity measurements in [[Benchmark 012 — Acceleration Information and Certified Displacement]]. That change can resolve the earlier response ambiguity over the recorded horizon. But accounting for the camera's exposure and noise is essential: in one tested condition, a 20% increase in noise variance reduces truth inclusion from 100% to 28.33% when the analysis assumes unchanged calibration.

A bound that explicitly permits that transfer error restores coverage in the tested condition, but its median width exceeds the small true response. Reliability and precision are separate requirements.

The positive mathematical result is an acceleration-free exposure bound, plus a sharp special case when the exposure equals the horizon. [[Camera Exposure and Finite-Time Response Bounds]] gives the proofs, attainability examples, and physical limitations. These are checked derivations and a synthetic development study, not a demonstrated breakthrough, a historical originality claim, or a hardware experiment.

## 1. What is actually measured

In normalized thermal units, let

$$
J(T)=\frac12\operatorname{Var}[X(T)-X(0)]
=\int_0^T(T-t)C(t)\,dt.
$$

Under the equilibrium linear-response assumptions, this is displacement per unit weak step force. Its variance interpretation does not require a driven experiment; the response interpretation does require fluctuation–dissipation.

Each trajectory supplies two noisy rectangular averages of **position**, over $[0,h]$ and $[T,T+h]$. Their difference is

$$
Y=\frac1h\int_0^h[X(T+s)-X(s)]\,ds+\epsilon_T-\epsilon_0.
$$

The record therefore extends through $T+h$. Position itself need not be stationary; velocity is stationary and the common position anchor cancels. This is not a measurement of instantaneous acceleration or a rectangular average of velocity. Averaging positions and then differencing applies a convolution of two rectangular filters to velocity.

With signal-independent pair-noise variance $N$,

$$
\operatorname{Var}Y=2\overline J(T,h)+N,\qquad
\overline J=\int_0^\infty g_T(\omega)\operatorname{sinc}^2(\omega h/2)\,\rho(d\omega).
$$

Here $g_T=(1-\cos\omega T)/\omega^2$, continuously extended at zero. The noiseless camera quantity $\overline J$ is not generally the ordinary camera mean response to a force switched on at zero: that driven observable has a single exposure average rather than the squared filter above. We infer the unblurred $J$ from the passive variance instead.

The measurement framework is established. Savin–Doyle's equations 6–9 give rectangular position exposure and the MSD convolution; Berglund's equations 6–11 include shutter weighting and localization-error correlations. We do not claim those observations as new. [Savin and Doyle (2005)](https://web.mit.edu/doylegroup/pubs/BiophysJ-Savin05.pdf), [Berglund (2010)](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=905460).

## 2. The response certificate

For known finite velocity variance bounded by $C_U$,

$$
0\le J-\overline J\le\frac{C_Uh^2}{6},\qquad J\le\frac{C_UT^2}{2}.
$$

No instantaneous-acceleration variance or physical frequency cutoff is needed. If $T/h$ is a positive integer, an additional bound is

$$
J\le T\sqrt{C_U\overline J/2}.
$$

That refinement is false for general noninteger timing: a spectral line at a shutter zero can be invisible to the camera while contributing to the target displacement. The code retains this counterexample as a check. At $T=h$ and exact variance $C_U$, the conditional range

$$
\overline J\le J\le h\sqrt{C_U\overline J/2}
$$

is sharp over the broad stationary spectral class, and the sharp unconditional blur allowance is $C_Uh^2/8$. The endpoint examples need not be mixing or dissipative thermal free-particle models. Sharpness for that outer class is not sharpness within the particular thermal family below.

For the statistical part, independent trajectory differences give an exact centered Gaussian variance interval $[A,B]$. Independent immobile calibration pairs give an interval $[C,D]$ for $N_{\rm cal}$. With a justified transfer envelope

$$
(1-\delta)N_{\rm cal}\le N_{\rm true}\le(1+\delta)N_{\rm cal},
$$

the camera signal variance is bounded by

$$
\ell=\max\{0,A-(1+\delta)D\},\qquad
u=B-(1-\delta)C.
$$

For integer $T/h$, return

$$
\left[\frac\ell2,
\min\left\{\frac u2+\frac{C_Uh^2}{6},
\frac T2\sqrt{C_Uu},\frac{C_UT^2}{2}\right\}\right].
$$

Negative $u$ or an empty final interval triggers an explicit incompatible-constraints result, not a false claim of zero physical motion. The two chi-square intervals use failure budgets 0.025 each. Their joint event has probability at least 95%; in the independent Gaussian simulation its probability is exactly $0.975^2=0.950625$. This is a per-condition, prechosen-horizon statement, not coverage after selecting the narrowest of many exposures.

## 3. Fixed development design and costs

The written protocol was fixed after analytic development and primary-source reading, before this lab's stochastic run. The integer-ratio refinement was added during that pre-run analytic review and recorded in the protocol. No performance threshold, exposure, noise level, or seed was tuned after seeing the outcomes. This is not external preregistration. The thermal aliases were already known development examples.

| Item | Declared value |
|---|---|
| Physical cases | Base exponential-memory thermal model and its first smooth thermal alias |
| Velocity variance upper bound | $C_U=1$, known, not estimated from the camera |
| Horizon | $T=6$ |
| Position exposure $h$ | 0.075, 0.15, 0.3, 0.6 |
| Total scalar position readings | 8,192 or 32,768 |
| Allocation | 75% trajectory readings, 25% calibration readings |
| Independent pairs | $(M,L)=(3072,1024)$ or $(12288,4096)$ |
| Calibration frame-noise variance | $0.003/h+0.0001$ |
| True/calibration pair-noise variance ratio | 1, 1.2, 1.5 |
| Repetitions | 10,000 independent datasets in each of 48 cells |
| Seed | 2026091603 |

Every pair consumes two scalar readings. Each method uses the same saved sample-variance statistics in a cell. The illustrative inverse-exposure noise law is supplied only to the generator; the inference uses calibration intervals, not the generator's exact noise variance. This law is not a validated camera photon model.

Equal reading counts do not equalize every experimental resource. Total exposure $Bh$ and the sequential pair-window proxy $(B/2)(T+h)$ are also recorded. At $B=32768$, increasing $h$ from 0.075 to 0.6 increases the exposure proxy eightfold. Independent-particle preparation, spatial correlations, photon budget, and actual camera throughput are not modeled. There is no matched-hardware claim against the velocity/acceleration devices in Benchmark 012.

The three analyses are: deliberately ignore blur and assume exact transfer; include blur with exact transfer; include blur with a ±20% variance-transfer allowance. The first is an assumption-violation diagnostic, **not** a competitive state-of-the-art baseline. No superiority over published camera-tracking estimators or spectral optimization is tested.

## 4. Results, including the failures

The base and aliased models have the same sampled velocity law at spacing 0.6, but at $T=6$ their true response functionals are

$$
J_0=6.050892318196411,\qquad
J_1=0.009880356970752622.
$$

Camera position differences do not preserve that identical observation law. For the alias, $\overline J$ decreases from 0.00942017 at $h=0.075$ to 0.000599497 at $h=0.6$. This is why treating the camera variance as the unblurred displacement variance can fail.

The full run evaluates **480,000 synthetic datasets and 1,440,000 interval attempts**. Across conditions where an analysis's assumptions hold, empirical truth inclusion ranges from **97.40% to 100%**. There are zero coverage violations on the common observation/calibration confidence events for the valid methods. The common-event rates range from 94.67% to 95.51%, consistent with finite Monte Carlo variability around 95.0625%; the event is sufficient, not necessary, for coverage. Every attempted interval was returned in this run; the incompatible-draw count is zero.

For the small-response alias, 32,768 readings, and genuinely unchanged noise:

| Exposure | Ignore-blur truth inclusion | Blur-aware truth inclusion | Median width, exact transfer | Median width, ±20% transfer |
|---|---:|---:|---:|---:|
| 0.075 | 99.60% | 99.99% | 0.00774770 | 0.02137751 |
| 0.15 | 52.48% | 100% | 0.00735951 | 0.01541528 |
| 0.3 | 0% | 100% | 0.01683348 | 0.02088012 |
| 0.6 | 0% | 100% | 0.06082941 | 0.06198372 |

The ±20% analysis includes the truth in all 10,000 draws of each row. These empirical rates are not claims of exact 100% population coverage. The report retains Wilson intervals for every rate.

Now increase actual noise variance by 20% while keeping the calibration sample unchanged in law. At $h=0.15$, the blur-aware exact-transfer analysis covers only **28.33%**; the ±20% analysis covers **100%**, but its median width is **0.01564252**, or **158.32% of the true response**. At $h=0.075$, exact-transfer coverage falls to **0.03%**, while the wider analysis covers **99.95%**. At larger exposures the broad blur allowance can mask this mismatch. Apparent good coverage in such a cell does not validate the false transfer assumption.

The 50% drift cells violate even the ±20% allowance and remain in the report. Their behavior is a scope stress, not a failed theorem under its assumptions. Partial cancellation of blur bias and noise bias can make an invalid method look accurate in an individual setting.

![[camera_response_bounds.png]]

The plotted small-response case illustrates both false confidence and the price of protection. The shortest exposure is not automatically best: it reduces blur but, under the declared noise law, worsens localization noise and calibration uncertainty. The displayed finite exposure grid does not identify an optimal shutter.

## 5. What remains uncertain even with infinite repetitions

The population intervals are saved separately from finite-sample intervals. At $h=0.15$ and unchanged noise, the exact-transfer population interval is

$$
[0.008149989854,\;0.011899989854].
$$

Allowing ±20% variance transfer gives

$$
[0.004129989854,\;0.015919989854].
$$

These are nonvanishing uncertainty widths for this bounding procedure. Repeating the same readings cannot remove its systematic blur and transfer allowances. They are **not** proofs that these are the sharp identification intervals or minimax lower bounds; additional constraints or a sharper method may improve them.

The separate sharp $T=h$ result demonstrates an exact identification range only over its explicitly stated broad spectral class. Do not transfer that sharpness claim to the main $T/h=10,20,40,80$ experiment.

The integer-ratio square-root cap never tightens a returned blur-aware interval in this run: the additive blur bound dominates. Its proof and sharp special case are mathematical results, not an observed numerical improvement in this particular experiment.

## 6. Verification and reproducibility

Lab 33 passes 22 verification groups: thermal displacement versus oscillatory integration; equal sampled velocity laws; camera convolution versus an independent spectral integral; quadrature refinement; limiting cases; spectral-line inequality tests; the noninteger-timing counterexample; endpoint-noise telescoping; correct reading budgets and degrees of freedom; interval nesting; common-event coverage; complete attempt accounting; finite returned endpoints; and saved-array round trips.

The simulations generate exact chi-square sufficient statistics for centered Gaussian sample variances. They do not approximate long trajectories by coarse numerical integration. Independent whole trajectories, not overlapping frames from a single movie, provide the degrees of freedom. The deterministic inequalities are proved analytically; numerical frequency grids check implementation but do not replace the proofs.

A separate implementation passes **17 independent audit groups** without importing labs 31–33. It evaluates the camera's trapezoidal velocity-weight covariance directly, agreeing within $6.23\times10^{-10}$, and recomputes all 1,440,000 intervals with a maximum endpoint difference of $8.88\times10^{-16}$. All sufficient statistics replay exactly from the declared seed; confidence-event masks, inclusion counts, scope flags, and width summaries match. No reported coverage depends on the main script's $10^{-12}$ endpoint tolerance.

Portable assets in `62 Computational Labs`:

- `33_camera_response_bounds.py` and `camera_response_protocol.json`;
- `results/camera_response/results.json`, with every condition, confidence rate, interval-width summary, population interval, check, and source hash;
- `results/camera_response/sufficient_statistics_and_intervals.npz`, preserving all squared-deviation sums, interval endpoints, compatibility flags, common-event flags, and cell identifiers;
- `results/camera_response/camera_response_bounds.png`.
- `audit_camera_response.py` and `results/camera_response/independent_audit.json`, containing the independent implementation, per-cell recomputation records, and source/input hashes.

The program requires NumPy, SciPy, and Matplotlib and imports the unchanged thermal helpers from labs 31–32. It is separate from the introductory lab runner. The saved hashes bind the execution record to its protocol, implementation, source helpers, and sufficient statistics.

## 7. Research decision

This checkpoint resolves an observation-model issue, not the problem of predicting unknown physics. The camera measures a functional close to the desired displacement over an already recorded horizon. It does not recover the memory kernel, determine an eventual transport law, establish permanent learning, or forecast beyond that record.

The practical constraint is now explicit. With an inertial relaxation time $\tau_m$ and a long diffusive horizon, the worst-case relative blur allowance scales as $h^2/(6\tau_m T)$. It can be enormous for ordinary camera exposure times, even when the true physical blur is much smaller. Ideal overdamped Brownian motion is outside the finite-velocity-variance theorem.

The next useful gate is **an instrument-feasibility and external-data audit**, not another exposure sweep of the same aliases: identify a primary dataset with exposure metadata, mass/temperature or an independent velocity-variance bound, a matched localization reference, and an independently defensible number of trajectories. First calculate whether these bounds can possibly be informative in its physical units. Reject an unsuitable dataset rather than apply a nominal 95% label to unverified assumptions. For a contribution claim, compare a stronger published instrument-aware baseline and establish either a sharper practically useful guarantee or an externally validated result.

The wider vault still needs foundational derivations and experiment coverage. This narrow research branch does not complete that broader goal.

[[Camera Exposure and Finite-Time Response Bounds]] · [[Benchmark 012 — Acceleration Information and Certified Displacement]] · [[Prior Art — Spectral Bounds and Physical Response]] · [[Research Frontier — Identifiability Before Discovery]] · [[Computational Lab Index]] · [[Synthesis Lab]] · [[Physics Worldmap]]
