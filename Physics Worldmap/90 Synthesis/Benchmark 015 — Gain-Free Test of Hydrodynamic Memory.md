---
type: computational-benchmark
field: Statistical Physics
epistemic_status: effective
level: advanced
tags: [brownian-motion, hydrodynamic-memory, basset, calibration-free, public-data, preregistration]
created: 2026-10-08
updated: 2026-10-08
note_maturity: expanded
source_audit: digest-verified-public-data-and-notebooks-read-as-text
---

# Benchmark 015 — Gain-Free Test of Hydrodynamic Memory

> [!warning] Correction after internal review (2026-10-08)
> - **The agreement is within 2.2%, not 1.6%.** Data/E − 1 reaches −1.91% at 96 µs and −2.14% at 135.75 µs.
> - **The pre-committed consistency test rejected the published model:** χ² = 3906 on 16 dof, or 2712 after the SE correction.
> - **The Langevin "rejection" compares two poorly fitting models** (χ²/dof of about 650 vs 260), so it is qualitative only.


**Status:** a preregistered stage-2 analysis of the Dryad traces already used in [[Benchmark 014 — Preregistered Conditioned Brownian Reproduction]]. Hydrodynamic memory is confirmed without the theory-fitted volts-to-metres gain. The published Basset model is within 1.6% of the observable at every lag, yet formally rejected at the observable's 0.04–0.4% precision. No new physical effect is claimed.

| Lab | Role | Files |
|---|---|---|
| 35 | analysis | `35_gain_free_hydrodynamic_memory.py`, `gain_free_hydrodynamics_protocol.json`, `results/gain_free_hydrodynamics/` |
| 38 | synthetic controls | `results/gain_free_selftest/` |
| 40 | frozen post hoc diagnostics | `results/basset_misfit_diagnostics/` |

## Observable

$$
R_k=\frac{\operatorname{Cov}_p(D_k,W)-\operatorname{Cov}_e(D_k,W)}{\operatorname{Var}_p W-\operatorname{Var}_e W}\quad[\text{seconds}],
$$

- $D_k$ is the $k$-lag displacement of the supplied positions and $W$ the supplied velocity.
- $p$ and $e$ denote the particle and empty-trap traces.
- The gain cancels exactly.
- In equilibrium, $R$ is the conditional mean displacement per unit initial velocity, seen through the bin-and-stencil operator. In the continuum limit it is $m\chi(t)$ ([[Derivation — Equilibrium Conditioning of a Hydrodynamic Brownian Particle]]).

The 16 lags run from 0.75 to 192 µs. Uncertainty comes from a moving-block bootstrap (400 replicates), and fits use generalised least squares.

## Protocol history (complete)

1. **Frozen 2026-10-06 (v1.0).** Two amendments followed the same day, both before any model comparison: empty-trap noise subtraction, and quadrature nodes.
2. **Synthetic controls, 2026-10-08, lab 38.** These were added because lab 35 had none.
   - Positions were synthesised exactly from the FDT spectrum on a 25 ns grid and box-averaged.
   - White and smooth detector noise was added at the data's 6% share of $\operatorname{Var}W$.
   - The synthesiser's expected increment variances match lab 35's operator to $10^{-5}$.
3. **Protocol deviation (disclosed).** While reading Benchmark 014's saved ±σ conditional means for noise levels, an approximate lag-1 value of $R/\Delta\approx0.98$ was computed. Shortly afterwards the operator prediction of 0.983 was seen. No other real-data $R$ value was examined before the run, and no decision rule changed.
4. **First real-data run**, after the controls passed. It crashed at the JSON write, having printed only three χ² values.
5. **Serialisation-only fix**, recorded as a dated amendment, and an identical rerun. The rerun reproduced those χ² values exactly.

## Synthetic controls (lab 38)

| Truth | E consistent? | V rejected? | Memory detected? | B3 $z/m$ interval (truth) | Median rel. SE |
|---|---|---|---|---|---:|
| Basset (published) | yes, $p=0.69$ | yes | yes, $\Delta\chi^2=8623$ | [143.5, 147.2] (144.9) | 0.45% |
| Langevin ($z=0$) | correctly no | yes | correctly no, $\Delta\chi^2=-7311$ | [0.3, 1.1] (0) | 0.24% |

The frozen rules are calibrated and have power when their assumptions hold.

## Real-data result

**Preregistered decisions:**

| Decision | Verdict |
|---|---|
| Hydrodynamic memory supported ($\chi^2_L-\chi^2_{B2}>25$) | **YES**, $\Delta\chi^2=5483$ |
| Initial-value variant rejected relative to E | **YES**, $\Delta\chi^2\approx10^7$ |
| Published Basset E consistent ($p>0.01$) | **NO**, $\chi^2=3906$ on 16 dof |
| B3 $z/m$ interval contains the Stokes–Basset value | **NO**: 188 [188.8, 193.7] vs 144.9 |

**Per-lag view of E.** Data ÷ prediction − 1, with relative SE:

| lag | 0.75 µs | 1.5 | 3 | 6 | 12 | 24 | 48 | 96 | 192 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| data/E − 1 | +0.26% | +0.24% | −1.31% | −1.63% | −1.45% | −1.15% | −1.24% | −1.91% | −1.24% |
| rel. SE | 0.04% | 0.10% | 0.15% | 0.23% | 0.37% | 0.63% | 1.1% | 2.0% | 3.3% |

**Reading.**
- With no free parameters, E describes the gain-free conditional mean to within 1.6% from 0.75 to 192 µs. A memoryless model misses it by tens of percent.
- The formal rejection reflects a structured residual of about 1–1.6%, measured with extraordinary precision. It is not a gross failure.
- The free fits B3 and B2 are not physical measurements:
  - B3 is itself a poor fit ($\chi^2=2748$/13).
  - Its implied radius, from $z/\gamma$, is about 17 µm.
  - Its bootstrap interval excludes its own point estimate, a sign of an ill-conditioned fit.
  - GLS with strongly correlated lags trades a 30% long-lag error for short-lag agreement.
- Without noise subtraction, E's $\chi^2$ rises to 11,716.

**Independent calibration check.** Equipartition through the operator predicts $\operatorname{Var}W$. With the published radius, it reproduces the authors' MSD-fitted gain to 0.7% using the calibration half, and 1.6% using the test half. Without the operator the discrepancy is 8%.

## Where the residual lives (lab 40)

Lab 40's five diagnostics were frozen and committed (`dfece64`) after lab 35 had printed only three χ² values, before any residual was seen. Its frequency-domain operator agrees with the time-domain one to better than $10^{-6}$.

| Diagnostic | Result | Accounts for the misfit? |
|---|---|---|
| D1 lag split | Lags ≥ 12 µs: B3 fits (SE-corrected χ²/dof 2.4) with near-physical parameters ($\gamma/m$ 23,845, $z/m$ 168, $K/m$ 1.14×10⁸). Lags ≤ 12 µs: χ² = 2,403 on 5 dof | localises it to **0.75–12 µs** |
| D2 free memory exponent | β → 1.85, χ² 2,078 | no |
| D3 detector low-pass | corner → ∞; no change | no |
| D4 noise scale | α = 0.61, χ² 1,730 (Δχ² 1,018) | partly, not fully |
| D5 per-trace B3 | Present in every trace (χ² 732–1,842 on 13 dof). Parameters differ across traces far beyond their refit spread: heterogeneity $p\approx0$, $10^{-92}$ and $10^{-39}$ for $\gamma/m$, $z/m$, $K/m$. Fitted $z/m$ falls from 229 to 94 over traces 2–6 | not a pooling artefact; see note below |

**On D5.** Every per-trace B3 fit is poor, so its parameters compensate rather than measure, and the heterogeneity is a lead, not a result. If the traces are in acquisition order, the falling $z/m$ could indicate a drift during the experiment, such as temperature, viscosity or wall distance. The trace order and timing are not documented in the files.

**Lab 42 (stage 4, post hoc; frozen before running, one dated pre-fit numerical amendment).** It splits the measured empty-trap noise into a short-range part (|n| ≤ 3 bins) and a long-range part, and lets each scale freely in the particle runs, with the published Basset physics kept fixed.
- **Result: NOT EXPLAINED.** χ² = 2,300 on 14 dof, and the best fit needs the long-range noise 8× larger with the particle present, which is implausible.
- With B3 physics also free, χ² = 1,381 on 11 dof.
- So noise transfer, in this two-component form, does not account for the residual.

The sign change between lags 2 and 3 coincides with the reach of white detector noise through the stencil, which spans at most 4 bins. Particle-dependent noise is now established spectrally (lab 45 above). Neither a single scale (D4) nor two components (lab 42) account for the residual, which points to a frequency-dependent change in noise shape, or physics, in the 100–400 kHz band. It stays **open**. The remaining tests need material only the authors hold: raw detector records (to vary the Tikhonov high-pass inversion), the order and timing of the traces, and the detector's linearity calibration.

## Spectral view of the noise assumption (lab 45, descriptive)

Lab 45 (`45_noise_additivity_spectrum.py`; figure `results/noise_additivity/noise_additivity_psd.png`) compares Welch spectra of the supplied 750 ns positions with the published-Basset spectrum, including box averaging and aliasing, at the published gain.

| Band | (particle − empty) ÷ Basset model | particle ÷ empty |
|---|---:|---:|
| 2–100 kHz | 0.96–1.02 | ≫ 1 |
| 100–400 kHz | 1.23 | 13 → 2.8 |
| 400–660 kHz | negative | 0.83 → 0.59 |

Three readings follow:

1. **Theory and calibration agree over four decades in frequency.** From about 200 Hz to 100 kHz the model and gain match the particle spectrum, and to within 1–4% from 2 to 100 kHz.
2. **The noise is not particle-independent.** Above 400 kHz the particle runs are quieter than the empty trap. Their high-frequency noise floor is roughly 0.5–0.7× the empty-trap floor, consistent with D4 (α = 0.61) and lab 42's short-range scale (0.75). Subtracting the empty-trap noise over-subtracts at the shortest lags.
3. **The 2–12 µs residual has a spectral counterpart.** At 100–400 kHz (periods of 2.5–10 µs) the particle spectrum exceeds Basset plus empty-trap noise by about 23% of the model. Noise and particle signal are comparable in that band, so a change in noise shape with the particle present cannot be separated from extra physics using these files alone.

## Limits

- One particle, one dataset. The upstream Tikhonov inversion is shared and was not varied.
- The noise subtraction assumes additive, particle-independent noise. That assumption is the leading suspect for the residual.
- The bootstrap SEs were about 20% too small in Benchmark 014's self-tests. Correcting for that does not change any verdict here.

## Next

1. Model particle-run noise with separate white and smooth components, estimated from a high-frequency proxy in the particle data. Freeze before fitting.
2. Report the gain-free result to the data authors together with [[Benchmark 017 — Processing Dependence of the Conditioned Super-Ballistic Signal]].

[[Benchmark 014 — Preregistered Conditioned Brownian Reproduction]] · [[Benchmark 016 — Stratified Conditioning and an Estimator Artifact]] · [[Benchmark 017 — Processing Dependence of the Conditioned Super-Ballistic Signal]] · [[Computational Lab Index]]
