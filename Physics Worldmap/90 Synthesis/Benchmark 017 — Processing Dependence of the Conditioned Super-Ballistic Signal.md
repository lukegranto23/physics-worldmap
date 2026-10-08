---
type: computational-benchmark
field: Statistical Physics
epistemic_status: effective
level: advanced
tags: [brownian-motion, hydrodynamic-memory, conditioning, measurement-operator, detector-noise, reanalysis, preregistration]
created: 2026-10-08
updated: 2026-10-08
note_maturity: expanded
source_audit: digest-verified-public-data-and-notebooks-read-as-text
---

# Benchmark 017 — Processing Dependence of the Conditioned Super-Ballistic Signal

**Status:** a reanalysis result on public data. The hypothesis was formed post hoc and then tested with a confirmatory protocol that was frozen and committed (`c908437`, 2026-10-08T08:39Z) before the confirmatory statistic was computed on the real data. The protocol's synthetic self-test passed.

What it changes is how the published conditioned mean-square displacement should be read. It does **not** challenge Basset–Boussinesq hydrodynamics. [[Benchmark 015 — Gain-Free Test of Hydrodynamic Memory]] finds the published Basset model within 1.6% of a gain-free observable. No new physical effect is claimed.

Lab 41 is `41_processing_dependence_test.py`, with outputs in `results/processing_dependence/`.

## The published reading

Boynewicz, Thumann and Raizen (*Sci. Adv.* 2026) select starts where the measured velocity is within 1% of a standard deviation of zero. The mean-square displacement after those starts grows as $t^{5/2}$, and the conditioned data agree with the continuum theory $2k_BT\int_0^t\chi-k_BTm\chi(t)^2$.

In the authors' `conditioning.ipynb`, read as text, data divided by the fitted gain squared are compared directly with that continuum formula. It contains no measurement operator and no detector-noise term.

## What a measurement-level forward model says

The measured velocity is not the instantaneous velocity. It is an eighth-order stencil spanning ±3 µs, applied to 750 ns box-averaged positions. The derivation in [[Derivation — Equilibrium Conditioning of a Hydrodynamic Brownian Particle]] and the operator of lab 35 apply. Pushing the published Basset model, with no free parameters, through that operator gives these factors:

| lag | 0.75 µs | 1.5 µs | 3 µs | 6 µs | 12 µs | 48 µs |
|---|---:|---:|---:|---:|---:|---:|
| operator ÷ continuum, noise-free | 0.26 | 0.49 | 0.67 | 0.79 | 0.87 | 0.96 |
| detector-noise share of the forward prediction | 71% | 51% | 27% | 16% | 9% | 3% |
| data ÷ continuum curve − 1 | −27% | −2% | +1% | −5% | −5% | −4% |

Noise moments come from the empty-trap traces, which assumes additive, independent noise. The gain is the authors' value. Independently, equipartition through the operator reproduces it to 0.7% (calibration half) and 1.6% (test half). Without the operator the discrepancy would be 8%.

Over 0.75–6 µs the noise-free operator curve has log-log slope **2.93**. Adding measured noise gives **2.42**. The data give **2.52**, and the continuum curve **2.41**. Two large effects nearly cancel at the authors' processing choice.

*This was found post hoc*, after Benchmark 014's results were inspected, so it needed an independent test.

## Confirmatory test (frozen before data)

**Design.**
- Recompute velocity from the same supplied positions with central stencils of order 2, 4 and 8, on positions coarsened by 1, 2 and 4 bins. That gives nine variants; the reference is the published order-8, 750 ns choice.
- At $T=3,6,12,24$ µs, measure $\rho_v(T)$: the conditioned MSD of variant $v$ divided by the reference. The gain cancels.

**Hypotheses.**
- **H_cont** (the continuum reading): the conditioned MSD is the particle's physical quantity, so $\rho=1$.
- **H_fwd** (the forward model): $\rho$ follows the published Basset operator plus each variant's own empty-trap noise.

**Uncertainty.** Paired block bootstrap: the same 2,000-sample blocks are resampled for every variant.

**Decision rule.** H_fwd is favoured if $Z_\text{cont}-Z_\text{fwd}>25$ and the median |log deviation| is below 0.05.

**Self-test.** Synthetic Basset data with white and smooth noise through the lab 38 generator gave $Z_\text{fwd}=21.2$ and $Z_\text{cont}=4202$: H_fwd FAVOURED, as required.

**Result on the Dryad traces: H_fwd FAVOURED.** $Z_\text{fwd}=20.9$ over 32 cells, consistent with noise, against $Z_\text{cont}=4773$. The median |log deviation| from the forward model is 0.024.

| Variant (order, coarsening) | $\rho$ observed at 3 / 6 / 12 / 24 µs | $\rho$ forward model |
|---|---|---|
| 2, ×1 | 0.78 / 0.86 / 0.93 / 0.96 | 0.76 / 0.84 / 0.91 / 0.95 |
| 2, ×2 | 0.48 / 0.67 / 0.80 / 0.91 | 0.46 / 0.65 / 0.79 / 0.88 |
| 8, ×2 | 0.62 / 0.76 / 0.83 / 0.89 | 0.62 / 0.77 / 0.87 / 0.92 |
| 2, ×4 | 0.25 / 0.42 / 0.62 / 0.81 | 0.27 / 0.44 / 0.65 / 0.80 |
| 8, ×4 | 0.29 / 0.57 / 0.72 / 0.87 | 0.31 / 0.56 / 0.75 / 0.86 |

(The remaining three variants are in `results/processing_dependence/dryad_v3/results.json`.)

**Figure.** `results/processing_dependence/processing_dependence_figure.png` (lab 44, descriptive) plots the zero-speed conditioned MSD for the published processing and two coarser alternatives, against the continuum curve and each variant's forward model.

**Descriptive consequence.** Over the same physical window of 3–12 µs, the apparent log-log exponent of the conditioned MSD ranges from **2.29 to 2.96** depending only on processing:
- 2.29–2.42 at 750 ns;
- 2.50–2.66 at 1.5 µs;
- 2.94–2.96 at 3 µs.

The continuum theory itself gives 2.32 there.

## Extension to the nonzero-speed curves (lab 43)

Lab 43 (`43_nonzero_speed_processing_test.py`) applies the same nine-variant test to the published conditioning speeds $v_0=q\,\operatorname{sd}(W)$, using the authors' ±1% window. It was frozen and committed (`f9505f2`) before the real-data run, and the forward prediction now includes the window's $E[W^2]$.

| $q$ | Synthetic self-test | Dryad data | $Z_\text{fwd}$ / $Z_\text{cont}$ (data) | Direction of the effect |
|---:|---|---|---|---|
| 0.5 | H_fwd | **H_fwd FAVOURED** | 44 / 849 | coarser processing suppresses the curve ($\rho\approx0.7$–0.9) |
| 1 | UNRESOLVED | UNRESOLVED | 16 / 28 | crossover: both hypotheses predict $\rho\approx1$ |
| 2 | H_fwd | **H_fwd FAVOURED** | 33 / 114 | coarser processing *enhances* the curve ($\rho$ up to 1.25) |

At larger speeds the mean-displacement term $(r/s)^2E[W^2]$ grows. It responds to processing in the opposite direction to the residual-variance term, so the sign of the effect changes near $q\approx1$. The UNRESOLVED verdict at $q=1$ is that crossover, which the self-test predicted, not a failure. Processing dependence therefore covers every published conditioning speed except the crossover.

## Interpretation

1. **Basset theory is supported.** The published Basset model predicts how the measured statistic changes under nine processing choices, at percent level, with no free parameters. That is further support for the hydrodynamics.
2. **The published conditioned curve is processing-dependent.** It is not a processing-independent display of the physical $t^{5/2}$ law. Its agreement with the continuum curve at 750 ns and order 8 depends on detector noise filling in what the measurement operator suppresses. Neither effect appears in the published comparison.
3. **The physical super-ballistic law can still be inferred.** The physical conditioned MSD is a model-based reconstruction. It can be obtained through a forward model like this one, or from the gain-free observable of Benchmark 015, not read directly off the curve.

## Limits

- **Noise model.** It assumes additive, particle-independent noise statistically equal to the empty trap. The lab 45 spectra in Benchmark 015 show this is only approximate: the particle-run noise floor above 400 kHz is about 0.5–0.7× the empty trap's. The noise shares quoted above (9–71%) are therefore upper estimates; at 0.75 µs a 0.6× floor still gives roughly 60%. The nine-variant test passed regardless, because its ratios are dominated by the operator. [[Benchmark 016 — Stratified Conditioning and an Estimator Artifact]] and lab 40 diagnostic D4 (in Benchmark 015) suggest the noise during particle runs may differ, but only partly.
- **Gain.** The authors' fitted gain is used; equipartition supports it to within 1.6%. Ratios $\rho$ do not depend on it.
- **One dataset.** One particle, six 84 ms traces, one laboratory. The upstream Tikhonov high-pass inversion is shared by all variants and was not varied.
- **No author response.** The authors have not been consulted. A private note to them should come before any public claim.

## Next

1. Review and send [[Draft Technical Note — Processing Dependence for the Data Authors]]: forward model, test, code, digests.
2. Extend the forward model to the authors' metre-unit figures. Nonzero speeds are done (lab 43).
3. Test noise additivity directly, for example from the high-frequency $d^4$ proxy in particle versus empty-trap runs.

[[Benchmark 014 — Preregistered Conditioned Brownian Reproduction]] · [[Benchmark 015 — Gain-Free Test of Hydrodynamic Memory]] · [[Benchmark 016 — Stratified Conditioning and an Estimator Artifact]] · [[Public Data Lead — Conditioned Hydrodynamic Brownian Motion]] · [[Research Frontier — Identifiability Before Discovery]]
