---
type: computational-benchmark
field: Statistical Physics
epistemic_status: effective
level: advanced
tags: [brownian-motion, conditioning, nonstationarity, detector-noise, estimator-bias, post-hoc]
created: 2026-10-08
updated: 2026-10-08
note_maturity: expanded
source_audit: internal-reanalysis-of-digest-verified-public-data
---

# Benchmark 016 — Stratified Conditioning and an Estimator Artifact

**Status:** a stage-2 test on data already inspected in [[Benchmark 014 — Preregistered Conditioned Brownian Reproduction]], plus a post hoc audit of that test. It explains Benchmark 014's empty-trap failure, and it withdraws the particle part of the stage-2 verdict. No new physical effect is claimed.

Labs:
- `36_stratified_conditioning.py` with protocol `stratified_conditioning_protocol.json` (frozen 2026-10-06, run the same day);
- `37_stratification_artifact_audit.py` (post hoc, 2026-10-08, synthetic data only).

Outputs are in `results/stratified_conditioning/` and `results/stratification_artifact_audit/`.

## The question

Benchmark 014 left two anomalies:
- a lag-1–2 failure in the empty trap;
- a systematic particle shortfall of about 3%.

Its working hypothesis was that slowly varying noise power makes small-$|W|$ selection favour quiet stretches, which biases conditional second moments low. Lab 36 tests this hypothesis. It cuts the test halves into segments, groups them into quartiles of a variance proxy, and predicts each stratum from its own moments.

## Preregistered result (lab 36)

Primary settings: 2,000-sample segments, 5% velocity bin, proxy = segment sample variance of $W$. The metric $e$ is the mean signed relative error over 12 lags.

| Role | $e$ unstratified | $e$ stratified | $e$ placebo | Preregistered verdict |
|---|---:|---:|---:|---|
| Particle | −0.83% | +0.17% | −0.78% | SUPPORTED |
| Empty trap | −1.51% | +0.03% | −1.55% | SUPPORTED |

Both self-tests passed under their frozen thresholds:
- **Stationary positive control:** stratification changed $e$ by 0.0068. The threshold was 0.01.
- **Modulated-noise negative control:** $|e|$ fell by 73%, from −22.7% to −6.2%. At least 50% was required.

Rerunning `--selftest` on 2026-10-08 reproduces every number.

## What the positive control was saying

The stationary control has no variance heterogeneity at all, yet stratifying on $\operatorname{Var}W$ still moved its error by 0.0068. The paired bootstrap SE of that change is 0.0009. The protocol's 0.01 tolerance let this through, but the shift is comparable to the effect being tested.

Lab 37 repeats the stationary control on eight fresh seeds, both proxies, and three segment lengths. Real-data shifts are read from lab 36's saved output.

| Segment length | Stationary shift, $\operatorname{Var}W$ proxy | Stationary shift, $d^4$ proxy | Particle, $\operatorname{Var}W$ | Particle, $d^4$ | Empty trap, $d^4$ |
|---:|---:|---:|---:|---:|---:|
| 1,000 | +0.0108 ± 0.0005 | +0.0001 | +0.0187 | +0.0020 | +0.0146 |
| 2,000 | +0.0053 ± 0.0004 | +0.0001 | +0.0100 | +0.0021 | +0.0149 |
| 8,000 | +0.0016 ± 0.0001 | +0.0001 | +0.0016 | +0.0019 | +0.0107 |

(± is the standard error of the mean over seeds.)

**Mechanism.** The $\operatorname{Var}W$ proxy is built from the conditioning variable itself. A 2,000-sample segment holds only about 40 velocity correlation times, so its sample variance fluctuates strongly. Strata defined by that statistic are not Gaussian with the stratum variance, and the Gaussian identity is biased inside them. The bias falls roughly as 1/segment length, as expected for a finite-sample effect.

The $d^4$ proxy is the mean squared fourth difference of $Y$, which is dominated by detector noise. It is not a function of $W$, and its stationary shift is consistent with zero at every length.

## Reading after the audit (post hoc)

Applying lab 36's decision rule to the artifact-free $d^4$ proxy gives:

- **Empty trap: SUPPORTED.**
  - $d^4$ stratification moves $e$ from −1.51% to −0.02%, and the $\operatorname{Var}W$ result agrees.
  - Both agree at all three segment lengths.
  - Together with Benchmark 014's 54% quarter-to-quarter variance drift, the empty-trap failure is attributed to slowly varying detector-noise power.
- **Particle: NOT SUPPORTED.**
  - $d^4$ explains about 0.2 percentage points, roughly 25% of the in-sample deficit. That part is stable across segment lengths and real, since the stationary $d^4$ shift is 0.0001.
  - At 8,000 samples the whole $\operatorname{Var}W$ shift equals the stationary artifact.
  - The preregistered particle SUPPORTED is withdrawn as an estimator artifact.

## Where Benchmark 014's 3% particle shortfall went

This diagnostic is post hoc and uses saved outputs only. Benchmark 014 predicts the test half from the calibration half. Lab 36's unstratified baseline predicts the test half from its own moments. At the shared 5% bin:

| | Mean relative error over 12 lags |
|---|---:|
| Calibration half → test half (Benchmark 014) | −2.7% |
| Test half in-sample (lab 36) | −0.8% ± 1.0% (segment bootstrap) |

The first-half moments predict 1.2–3.8% more than the second half's own moments, most at lag 1. Second-moment conditioning at short lags is a small difference of large terms: $u_k-r_k^2/s$ is a few percent of $u_k$. A change of about 0.1% in moments between halves therefore becomes a percent-level prediction error.

Most of the shortfall is calibration transfer across the trace midpoint, not a failure of the Gaussian identity. The in-sample particle residual is consistent with zero. The comparison is approximate: lab 36 drops a few starts at segment ends, so the two observed values are not quite identical.

## Limits

- All of this runs on data already inspected. Confirmation needs fresh traces.
- The between-half drift is inferred, not measured directly. It could be thermal, optical, or residual high-pass-inversion error.
- The $d^4$ proxy measures high-frequency noise only. Low-frequency noise heterogeneity is not separated.
- The modulated-noise negative control does not include the $\operatorname{Var}W$ self-selection artifact. A stricter future positive-control threshold would compare the shift with its own bootstrap SE, not with a fixed 0.01.

## Next

1. In any future stratified or calibration-transfer protocol, freeze a proxy that is not a function of the conditioning variable. Require the stationary-control shift to be within 2 SE of zero.
2. Measure the between-half drift directly: rolling estimates of $s$ and $u_k-r_k^2/s$ with block-bootstrap bands.
3. Gain-free hydrodynamics: see [[Benchmark 015 — Gain-Free Test of Hydrodynamic Memory]].

[[Benchmark 014 — Preregistered Conditioned Brownian Reproduction]] · [[Public Data Lead — Conditioned Hydrodynamic Brownian Motion]] · [[Research Frontier — Identifiability Before Discovery]] · [[Computational Lab Index]]
