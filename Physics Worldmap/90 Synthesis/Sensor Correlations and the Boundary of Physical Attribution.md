---
type: research-derivation
field: Cross-field
epistemic_status: established
level: advanced
tags: [physics, identifiability, metrology, sensors, response]
created: 2026-09-04
updated: 2026-09-04
source_audit: constructive-gaussian-derivation-with-explicit-assumptions
note_maturity: expanded
---

# Sensor Correlations and the Boundary of Physical Attribution

> [!important] Scope
> A post-hoc, exactly checkable covariance-decomposition example following [[Benchmark 007 — Calibration Before Physical Attribution]]. It illustrates a standard identifiability obstruction, not a novel theorem or new physical law.

## The question

If sensor variance is calibrated perfectly, does a changed measured time correlation prove that physical dynamics changed?

No, not when sensor errors may themselves be correlated. The covariance of a sum of independent signal and sensor error is the sum of their covariances. Knowing the sensor's marginal variance determines its diagonal covariance entries, not its off-diagonal entries.

The need to model the measurement process and its covariance terms is part of ordinary metrology. [NIST TN 1297, Appendix A](https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-appendix-law-propagation-uncertainty) provides that broader context. The exact example below is derived directly, not presented as a result reproduced from that reference.

## Two different mechanisms

Each dynamic trial prepares a fresh equilibrium oscillator and records positions at times 0 and $t$. Different trials are independent. Sensor errors are independent of the physical signal.

Consider:

- **A: changed physics.** Alias 1, decay 0.13, independent sensor errors of variance $s=0.35^2=0.1225$.
- **B: nominal physics.** Alias 1, decay 0.20, sensor errors with the same marginal variance but a specified correlation inside each dynamic pair.

The thermal signal covariance is

$$
C_d(t)=e^{-d|t|}
\left[\cos(2\pi t)+\frac{d}{2\pi}\sin(2\pi|t|)\right].
$$

Set $\delta(t)=C_{0.13}(t)-C_{0.20}(t)$. In mechanism B, choose the sensor pair covariance

$$
R_B(t)=
\begin{pmatrix}s&\delta(t)\\\delta(t)&s\end{pmatrix}.
$$

This is a legitimate positive-definite Gaussian covariance whenever $|\delta(t)|<s$.

| Lag | Required sensor cross covariance $\delta$ | Error correlation $\delta/s$ | Smallest sensor covariance eigenvalue |
|---|---:|---:|---:|
| 0.60 | −0.0254330 | −0.207616 | 0.0970670 |
| 0.85 | +0.0371395 | +0.303179 | 0.0853605 |
| 1.00 | +0.0593647 | +0.484610 | 0.0631353 |

All three are strictly positive-definite. The required noise is therefore mathematically admissible, not a negative-variance artifact.

## Exact agreement of the observations

For mechanism A,

$$
\Sigma_A(t)=
\begin{pmatrix}1+s&C_{0.13}(t)\\C_{0.13}(t)&1+s\end{pmatrix}.
$$

For mechanism B,

$$
\Sigma_B(t)=
\begin{pmatrix}1&C_{0.20}(t)\\C_{0.20}(t)&1\end{pmatrix}
+R_B(t)
=\Sigma_A(t).
$$

Means are zero and both laws are Gaussian, so covariance equality implies equality of the complete observed pair distributions.

Now include arbitrarily many calibration trials, each consisting of **one isolated noise-only observation** with law $N(0,s)$. Their laws are also identical in A and B. They are independent of the dynamic trials and one another.

Consequently, for any number of independently prepared pairs at these three lags and any number of isolated calibration readings, the **entire measured-data law is identical** under A and B. Any randomized or deterministic test based only on those observations has exactly the same rejection probability in both mechanisms.

This argument allows a lag-dependent within-pair error correlation. It constructs valid finite independent-pair experiments, not one stationary colored-noise process on an uninterrupted trajectory. It does not claim indistinguishability under arbitrary new lags, velocity measurements, force interventions, or extra reference channels.

## The responses are not the same

The two physical oscillators have

$$
m_d=\frac1{(2\pi)^2+d^2},\qquad
\chi_d(\nu)=\frac1{1-m_d\nu^2+2idm_d\nu}.
$$

At $\nu=2\pi$, the complex susceptibilities are approximately

$$
\chi_A=0.2500803-24.1738553i,\qquad
\chi_B=0.2501899-15.7198969i.
$$

Predicting B when A is true gives relative error **34.97%**. “Changed decay” here holds damped frequency fixed; the mass also changes through the stated parameterization.

Identical observation laws therefore hide a physically significant response difference. This is an information-level obstruction, unlike the merely weak detector in [[When More Data Cannot Rescue a Misfocused Test]].

## What a response-confidence claim would owe us

Let a data-dependent response set $\mathcal R(D)$ claim at least 97.5% coverage for both mechanisms. Since the observed-data law is the same,

$$
\Pr(\chi_A,\chi_B\in\mathcal R(D))\geq1-0.025-0.025=0.95.
$$

Thus, with probability at least 95%, its diameter must be at least

$$
|\chi_A-\chi_B|\approx8.4539584
$$

in the stated susceptibility units. No amount of the same observation types removes that requirement.

Likewise, for any point estimator with finite expected absolute error, the triangle inequality under the common data law gives

$$
\max\left\{\mathbb E_A|\widehat\chi-\chi_A|,
\mathbb E_B|\widehat\chi-\chi_B|\right\}
\geq\frac12|\chi_A-\chi_B|
\approx4.2269792.
$$

These are elementary two-model lower bounds. They are not claims about all experiments or all sensor models.

## The measurement that breaks this particular ambiguity

Use noise-only **calibration pairs at the same lags and with the same acquisition sequence**. Their cross covariance is zero under A and $\delta(t)$ under B. These calibration pair laws are distinguishable in principle.

The essential additional assumption is transfer: the paired calibration sensor law must describe sensor behavior during physical measurements. Sensor-signal coupling, changed acquisition electronics, or time-varying noise may invalidate it. Independent sensor channels or interventions can provide additional checks, but their error correlations also need measurement.

Lab 25 records 12 passing algebraic checks and the exact numeric covariance matrices in [the counterexample output](../62%20Computational%20Labs/results/sensor_calibration/correlated_sensor_counterexample.json). Finite-sample paired-calibration power has not yet been tested.

[[Benchmark 002 — The Sampling Boundary of Prediction]] · [[Benchmark 007 — Calibration Before Physical Attribution]] · [[Research Frontier — Identifiability Before Discovery]] · [[Synthesis Lab]]
