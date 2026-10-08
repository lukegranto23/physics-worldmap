---
type: computational-benchmark
field: Statistical Physics
epistemic_status: effective
level: advanced
tags: [linear-response, spectral-measures, uncertainty-quantification, calibration, aliasing, memory-kernel]
created: 2026-09-16
updated: 2026-09-16
note_maturity: expanded
source_audit: derived-with-primary-prior-art-and-independently-reviewed-computation
---

# Benchmark 012 — Acceleration Information and Certified Displacement

Independent information about rapid motion can substantially narrow finite-time displacement predictions without choosing a memory-kernel family. In this development experiment, an additional acceleration calibration reduces the median paired interval-width ratio to **0.228** at the selected horizon: roughly a 77.2% reduction. It does not rescue long extrapolation.

The more important qualification emerged in an adversarial follow-up. A finite-difference estimate of acceleration is not the same observable as instantaneous acceleration. We constructed two free, passive thermal systems that give exactly the same coarse velocity and finite-difference measurements, yet differ by a factor of about 612 in their displacement response at the tested horizon. Substituting the wrong calibration quantity produces false confidence.

These are applications and explicit derivations built on established spectral moment and strict-bounds methods. They are not a new physical law, a new optimization principle, or a demonstrated experimental breakthrough. The genuine research target is now the measurement needed to justify the rapid-motion bound.

[[Acceleration Sum Rules and the Sampling Ambiguity]] supplies the proofs. [[Prior Art — Spectral Bounds and Physical Response]] records the closest existing work. [[Benchmark 011 — Finite Observations and Infinite-Time Claims]] supplies the preceding observation-versus-asymptotics result.

## 1. What is predicted

Use dimensionless units with mass and thermal energy equal to one. For a normalized stationary velocity correlation,

$$
C(t)=\int_0^\infty\cos(\omega t)\,\rho(d\omega),\qquad \rho\ge0,\quad\int\rho=1,
$$

the target functional is

$$
J(T)=\int_0^T(T-t)C(t)\,dt
=\int_0^\infty\frac{1-\cos(\omega T)}{\omega^2}\,\rho(d\omega).
$$

The mean-square displacement is $2J(T)$. In the linear equilibrium target, $J(T)$ also equals the mean displacement under a unit constant force switched on at time zero. In a more general equilibrium model, the force interpretation is a linear-response statement, not a finite-amplitude guarantee.

The bounds concern an **ensemble response or mean-square displacement**, not where an individual future particle will be. The unknown is a whole nonnegative continuous-frequency spectral measure, not a selected finite list of memory kernels. Spectral lines are allowed. This broader class is a conservative relaxation of a particular free-GLE family; every extremizing spectrum need not have that family's realization.

## 2. Physical target and additional information

The generating model has $\gamma(t)=e^{-t}$ and the thermal realization

$$
dV=-Y\,dt,\qquad dY=(V-Y)\,dt+\sqrt2\,dW,
\qquad\operatorname{Cov}(V,Y)=I_2.
$$

Its true acceleration variance is one, and its spectral density is

$$
\rho_*(\omega)=\frac{2/\pi}{(1-\omega^2)^2+\omega^2}.
$$

Three information conditions receive the same sampled velocities:

1. Velocity observations only, with no upper bound on the second spectral moment.
2. An oracle ceiling $\int\omega^2\rho\le1$, supplied from the known generating model. The code uses this as an inequality, not an exact-moment equality.
3. An upper confidence bound on that moment from 256 independent **instantaneous acceleration** observations.

The third condition adds readings and a different observable. It is not a matched-hardware or matched-cost comparison. There is no sensor noise or finite integration time in the valid calibration model. The acceleration prior is not inferred from the fitted memory kernel or from finite differences of the original sampled velocities.

The earlier singular fractional-memory target has infinite acceleration variance and is outside this finite-sum-rule class. Changing the target makes the extra assumption testable; it does not quietly impose it on Benchmark 011.

## 3. A common confidence event

Each dataset consists of $M=512$ or $4096$ independent Gaussian velocity vectors sampled at $0,0.6,\ldots,11.4$. The program generates their exact Wishart scatter law. It preserves all 24 scatter matrices and the independent acceleration sums of squares.

At lag $k$, $(V_0+V_k)/\sqrt2$ and $(V_0-V_k)/\sqrt2$ have variances $1+C_k$ and $1-C_k$. Chi-square intervals for these variances, intersected and transformed, give correlation intervals $[L_k,U_k]$. Allocating 0.025 total failure probability across 38 two-sided variance intervals gives simultaneous covariance coverage of at least 97.5%. Dependence between different lags does not invalidate the union bound.

If $S_a$ is the sum of squares of 256 independent $N(0,\kappa)$ acceleration readings, the one-sided upper limit is

$$
K_U=\frac{S_a}{\chi^2_{256,\,0.025}}.
$$

Its coverage is 97.5%. Combining the two events gives at least **95% coverage of the common spectral information set**. All deterministic functional bounds derived from that same set are valid on this event. The covariance-only and oracle-ceiling conditions have at least 97.5% coverage under their stronger information assumptions; the comparison does not secretly assign them a smaller data budget.

This statistical claim assumes the declared Gaussian, stationary, independent sampling model and known velocity variance. The proof is not supplied by the small collection of plotted intervals.

## 4. How the bounds cover unobserved frequencies

For each sign $\sigma=\pm1$, seek an upper bound for $\sigma g_T(\omega)$ of the form

$$
a+b\omega^2+\sum_{k=1}^{19}y_k\cos(k\Delta\omega),\qquad b\ge0,
$$

where $g_T=(1-\cos\omega T)/\omega^2$. If this majorant is valid for every frequency, integration gives

$$
\sigma J(T)\le a+bK_U
+\sum_{y_k\ge0}y_kU_k+\sum_{y_k<0}y_kL_k.
$$

The quadratic term is omitted when there is no acceleration information. The lower infimum then remains zero because high-frequency aliases preserve sampled velocity laws while reducing displacement.

The optimization follows the established moment-dual strategy. We do not claim its invention. [Karlsson and Georgiou, equations 5–7](https://people.kth.se/~johan79/papers/KGTACversion_2submitted.pdf); [Stark's strict-bounds exposition](https://www.stat.berkeley.edu/~stark/Seminars/nsf-doe-98.htm)

A grid-only optimum is not sufficient. The implementation:

- solves a finite dual linear program;
- checks a refined grid and adds a constant correction using the global bound $|q''|\le2b+\sum|y_k|(k\Delta)^2+T^4/12$;
- uses exact frequency folding to extend the upper certificate beyond the Nyquist interval at the declared lattice-aligned prediction times;
- uses a sufficient quadratic-tail condition for the lower certificate with acceleration information;
- reports the correction, coefficient vector, finite-domain margin, and tail treatment for every returned bound.

The coefficients and margins are evaluated in ordinary floating-point arithmetic with a stated safety allowance, not interval arithmetic. “Certified” refers to the analytic continuum extension conditional on those numerical evaluations; it is not a machine-verified proof of every rounding operation. The bounds are conservative and are not claimed to be sharp continuum optima.

## 5. Structural limit with exact covariance samples

Even before sampling error, velocity observations alone leave a zero lower bound. The extra acceleration ceiling changes this sharply inside the record.

| Horizon $T$ | True $J(T)$ | Velocity-only bounds | Bounds with acceleration ceiling 1 |
|---:|---:|---:|---:|
| 3 | 2.86676 | [0, 2.86736] | [2.86304, 2.86736] |
| 6 | 6.05089 | [0, 6.05230] | [6.03502, 6.05230] |
| 11.4 | 11.40167 | [0, 11.40460] | [11.33615, 11.40460] |
| 30 | 30.00000 | [0, 70.56496] | [0, 70.56496] |

Numbers are rounded display values. The complete unrounded certificates are saved. The pronounced loss at $T=30$ is retained: acceleration information is not a license for arbitrary extrapolation. A wide returned bound alone does not prove that its endpoints are attainable in the narrower physical GLE class.

## 6. Finite-data results

There are 12 inference datasets at each ensemble size and 288 returned intervals in total. The following table shows **median widths**, not the width of an interval made by combining independently computed median endpoints. Values are for $M=4096$.

| Horizon | Velocity-only width | Oracle-ceiling width | Calibrated-acceleration width | Simple interpolation baseline width |
|---:|---:|---:|---:|---:|
| 3 | 2.98885 | 0.24010 | 0.24326 | 0.54762 |
| 6 | 6.81473 | 1.52993 | 1.55358 | 2.75200 |
| 11.4 | 14.95792 | 6.69091 | 6.75127 | 11.19174 |
| 30 | 96.14490 | 96.14490 | 96.14490 | Not applicable |

The baseline integrates a piecewise-linear covariance interpolant and includes its interval uncertainty plus $K_UT^2\Delta^2/24$. It uses the same additional acceleration information and is only defined inside the observed interval.

At $T=6$, the median *paired* ratio of calibrated to velocity-only width is 0.227964. All 12 calibrated intervals have a positive lower endpoint. This passes the development gate fixed before stochastic evaluation: ratio at most 0.5 and at least 90% of all declared datasets excluding zero. It is not a held-out discovery result. With only 12 inference datasets per size, these descriptive medians do not establish general frequency claims or optimality.

All 288 example intervals include the generating target. A separate 20,000-dataset audit of the defining confidence event found joint coverage of 95.71% at $M=512$ and 96.29% at $M=4096$. These are Monte Carlo observations, not replacements for the simultaneous-coverage derivation.

![Spectral response bounds](../62%20Computational%20Labs/results/spectral_response/spectral_response_bounds.png)

The extra information mainly lifts the lower endpoint in this study. The near-equality of upper endpoints is a result for these observations, not a theorem that acceleration information can never lower an upper bound.

## 7. Adversarial follow-up: the wrong acceleration observable

This diagnostic was specified after the main result and changes none of its thresholds. It tests an invalid but tempting substitution: using independent pairs a time $\Delta$ apart to estimate $(V(\Delta)-V(0))/\Delta$, then calling its variance limit an instantaneous acceleration limit.

For the four-dimensional thermal alias family derived in [[Acceleration Sum Rules and the Sampling Ambiguity]],

$$
C_q(t)=C_*(t)\cos(2\pi qt/\Delta),\qquad
\mathbb E[\dot V_q^2]=1+(2\pi q/\Delta)^2.
$$

Every model has the same entire lattice velocity law and the same independent finite-difference calibration law. Every member also has finite acceleration variance, stable thermal dynamics, positive diffusivity, and a passive memory kernel. The latter need not be completely monotone. The free position itself is not stationary; equilibrium refers to velocity and internal variables.

At $\Delta=0.6$ and $T=6$:

| Quantity | Base model $q=0$ | Thermal alias $q=1$ |
|---|---:|---:|
| All sampled velocity covariances | Identical | Identical |
| Finite-difference acceleration variance | 0.803242 | 0.803242 |
| Instantaneous acceleration variance | 1 | 110.662271 |
| Mean displacement per unit step force | 6.050892 | 0.00988036 |

The same measurements hide roughly a 612-fold difference in the response. Gaussianity makes covariance equality equality of the full sampled-data law, not just similarity of one summary statistic.

Reusing the 12 saved $M=4096$ velocity datasets, plus independent synthetic finite-difference calibration pairs, the invalid transfer returned 11 intervals; **all 11 missed the aliased truth**. One case returned no interval because the dual solver reported unboundedness; it is logged separately, not counted as either coverage or a physical detection. The median endpoints among returned invalid intervals were approximately [5.28378, 6.84344], while the true response was 0.00988036. Supplying the correct acceleration ceiling as an explicitly labeled oracle control produced 12 intervals, all containing the aliased truth.

![Invalid calibration transfer](../62%20Computational%20Labs/results/spectral_response/acceleration_alias_diagnostic.png)

The exact family gives a stronger inference limit: an upper confidence bound on instantaneous acceleration variance that is uniformly valid over all these aliases, using only their common observation law, must be infinite with probability at least its claimed coverage. More independent copies of the same lattice readings cannot repair the missing information.

This does **not** invalidate the main experiment's ideal instantaneous-acceleration assumption. It explains why a real instrument must independently justify that observable or a suitable physical spectral-tail bound. The equivalence does not include true displacement increments, off-lattice measurements, or general driven-response observations.

## 8. Verification, provenance, and what remains

The main calculation passed 17 verification groups, including thermal identities, independent correlation/displacement formulas, spectral sum rules, primal–dual weak-duality checks, statistical calibration, continuum and tail margins, and mesh refinement. The post-hoc alias diagnostic passed 14 groups, including full and hidden stability, thermal time reversal, covariance equivalence, finite acceleration, positive diffusivity, and an independent oscillatory quadrature.

An independent mathematical review checked the alias realization and the principal bounds. A September 16 code audit added explicit finite-coefficient and sampling-lattice guards, plus upward projection of the nonnegative quadratic coefficient when numerical solver tolerance could otherwise permit a tiny negative value. Rerunning the fixed study changed none of its 288 interval endpoints. The amendment is documented in protocol version 1.1; the original source, protocol, and results remain in the workspace's `work/spectral-response-v1-2026-09-15` folder outside this portable release.

The method's basic theory is prior art; the present controlled application and counterexample do not establish originality. The next scientifically meaningful target is a **costed, instrument-aware way to justify the acceleration or spectral-tail information**, followed by independent systems and data. Merely deriving finite differences more accurately on the same lattice cannot provide a uniform certificate over the demonstrated family.

Open work includes realistic sensor filtering and noise, systematic calibration-transfer errors, matched acquisition budgets, feasibility witnesses for sharpness claims, broader physical models, and a more exhaustive application-specific literature review. The full noisy Bockius spectral-repair reproduction remains a separate unfinished baseline.

## Reproducible assets

From the computational-lab directory:

~~~powershell
python 31_spectral_response_bounds.py
python 32_acceleration_calibration_alias.py
~~~

[Main protocol](../62%20Computational%20Labs/spectral_response_protocol.json) · [All bounds, certificates, and checks](../62%20Computational%20Labs/results/spectral_response/results.json) · [Saved scatter matrices](../62%20Computational%20Labs/results/spectral_response/input_scatter_matrices.npz) · [Post-hoc diagnostic protocol](../62%20Computational%20Labs/acceleration_alias_diagnostic_protocol.json) · [Alias models and diagnostic outcomes](../62%20Computational%20Labs/results/spectral_response/alias_diagnostic.json)

[[Computational Lab Index]] · [[Research Frontier — Identifiability Before Discovery]] · [[Synthesis Lab]] · [[Release Status and Next Work]] · [[Physics Worldmap]]
