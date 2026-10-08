---
type: research-principle
field: Cross-field
epistemic_status: established
level: advanced
tags: [calibration, sensors, experimental-design, identifiability]
created: 2026-09-05
updated: 2026-09-05
source_audit: derived-principle-with-explicit-controlled-example
note_maturity: expanded
---

# Matched-Condition Calibration

> [!important] Principle
> Calibration identifies only those features of the measurement process that it excites and observes under conditions that transfer to the target measurement.

[[Benchmark 007 — Calibration Before Physical Attribution]] · [[Benchmark 008 — Matched-Lag Calibration]] · [[Sensor Correlations and the Boundary of Physical Attribution]]

## Variance calibration is not covariance calibration

Suppose a measured two-time vector is

$$
Y=(X_0+\epsilon_0,\ X_t+\epsilon_t).
$$

If signal and sensor error are independent,

$$
\operatorname{Cov}(Y)=\operatorname{Cov}(X)+\operatorname{Cov}(\epsilon).
$$

Isolated zero-reference readings estimate $\operatorname{Var}(\epsilon)$. They do not estimate $\operatorname{Cov}(\epsilon_0,\epsilon_t)$. A change in measured time covariance can therefore be assigned to the signal or to the sensor unless another observation constrains that decomposition.

Noise-only calibration pairs at the same separation $t$ directly observe the missing covariance. This is the intervention used in Benchmark 008.

## Matching has several dimensions

“Same calibration” can fail along distinct axes:

- **Time separation:** white-noise behavior at one lag does not imply white noise at another.
- **Acquisition order and electronics:** triggering, filtering, digitization, and shared references can create correlations.
- **Operating state:** temperature, gain, load, bias, and vibration may differ between zero-reference and dynamic runs.
- **Time:** drift can make yesterday's calibration irrelevant.
- **Signal coupling:** sensor noise may depend on the physical state, violating additive independence.
- **Channel structure:** two nominally independent sensors can share clocks, power, processing, or environmental noise.

A matched calibration need not reproduce every condition. It must reproduce or bound those aspects that materially enter the claim.

NIST's general measurement-uncertainty guidance makes the same high-level point: a measurement model should include significant variability and covariance contributions. [NIST TN 1297, Appendix A](https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-appendix-law-propagation-uncertainty)

## Transfer is testable only with additional structure

Let $R_{\rm cal}(t)$ and $R_{\rm dyn}(t)$ be sensor covariance during calibration and dynamic measurement. Assuming

$$
R_{\rm cal}(t)=R_{\rm dyn}(t)
$$

is a transport assumption. Calibration data alone sample the left side; target data mix physical covariance with the right side.

Ways to probe transfer include:

- interleaving calibration and target trials;
- randomizing their order;
- using paired zero-reference acquisitions at every target lag;
- adding an independent reference channel;
- varying signal amplitude while holding acquisition settings fixed;
- checking residual cross spectra and Allan-type drift diagnostics;
- deliberately changing environmental or electronic conditions.

Each option adds assumptions. For example, an “independent” reference channel helps only to the extent that its shared-error structure is measured.

## The power–attribution tradeoff

A narrow sensor model gives a physical test more power because fewer observation patterns can be blamed on the instrument. If that model is wrong, the same power becomes false attribution.

A broader sensor model protects against this error but makes more physical alternatives observationally compatible. Benchmark 008 shows both sides at one reading budget: isolated calibration warns on both exact twins at about 93%, whereas paired calibration separates the causes but detects the true physical change only 56%.

This is not a defect that threshold tuning can erase. It reflects a larger null family. More discriminating observations—not more confidence in an untested sensor assumption—are the principled remedy.

## Consequence for response certificates

A response-confidence set must include uncertainty in every observation component capable of imitating response-relevant physics. If two physical/sensor decompositions generate the same measurements, uniform response coverage must include both responses with high probability. [[Sensor Correlations and the Boundary of Physical Attribution]] derives this requirement for one exact Gaussian pair.

Accordingly, a complete claim should state:

1. the physical model class;
2. the sensor and calibration model class;
3. which conditions are shared between calibration and target runs;
4. the allowed failure probability for calibration transfer;
5. the intervention and response family;
6. reading, time, and perturbation cost;
7. what observation would falsify the transfer assumption.

Without these, “the data reject the physical model” may mean only “the combined physical-plus-instrument story is incomplete.”

## Limits

The paired Gaussian construction is a clean teaching and verification case. Real instruments may have nonstationary, non-Gaussian, nonlinear, state-dependent, or adversarial errors. Matched-condition calibration reduces ambiguity; it does not make the instrument transparent.

[[Experiment Atlas]] · [[Uncertainty Quantification]] · [[Research Frontier — Identifiability Before Discovery]] · [[Synthesis Lab]]
