---
type: computational-benchmark
field: Statistical Physics
epistemic_status: effective
level: advanced
tags: [brownian-motion, hydrodynamic-memory, conditioning, public-data, reproduction, preregistration]
created: 2026-10-06
updated: 2026-10-06
note_maturity: expanded
source_audit: digest-verified-public-data-and-notebooks-read-as-text
---

# Benchmark 014 — Preregistered Conditioned Brownian Reproduction

**Status:** the first external-data result in this vault. It is a **scoped reproduction** of a published conditional-displacement observation. It is not a new physical effect, a test of hydrodynamic theory against alternatives, or an improvement on the published analysis.

Follows [[Public Data Lead — Conditioned Hydrodynamic Brownian Motion]]. Lab 34: `34_conditioned_displacement_reproduction.py`, protocol `conditioned_reproduction_protocol.json`, outputs in `results/conditioned_reproduction/`.

## Sequence and what was frozen when

1. **Protocol frozen** (2026-10-06) after reading only Dryad API metadata: file names, sizes, SHA-256 digests, CC0 licence. The API and web file routes returned HTTP 401/403 to automated requests and were not circumvented.
2. **Self-tests** on synthetic data, before any data content was seen:
   - Gaussian trapped-particle positive control: AGREE on 8/8 fresh seeds.
   - Fluctuating-detector-noise negative control: DISAGREE on 7/8.
   - Pooled positive-control $z$ standard deviation is 1.20, so the bootstrap standard errors are **about 20% too small**. Read every $z$ below with that in mind.
3. **Data acquired** by the vault owner through the Dryad web interface (`doi_10_5061_dryad_pvmcvdnz4__v20260113.zip`). All seven files match the published digests. Data are kept outside the vault in `work/external-data/`.
4. **Notebooks read as text, not executed**, then the frozen analysis was run once. No protocol amendments.

## What the notebooks and files establish

- **Six traces, not five.** Each CSV has columns `Trace 1`–`Trace 6`, 111,848 samples each at 750 ns. That is six $\times$ 83.9 ms. The Dryad README's five-trace listing is wrong; the paper's six is right. This resolves the open discrepancy.
- **Processing chain** (`fitting.ipynb`):
  - 200 MHz detector signal;
  - FFT-domain Tikhonov-regularised inversion of a fitted Sallen–Key high-pass response ($\lambda=|H(40\,\mathrm{Hz})|$);
  - block averaging over 150 samples;
  - velocity from `findiff` with `acc=8`.

  Our least-squares check recovers exactly the eighth-order central stencil divided by 750 ns (cosine 1.0, $R^2=1.0$).
- **Units.** Supplied positions are **detector volts** and velocities volts per second. The volts-to-metres gain ($\sqrt{8.62\times10^{14}}\approx2.94\times10^{7}$ V/m), radius (3.40 µm) and trap stiffness ($7.80\times10^{-5}$ N/m) are **fitted to the hydrodynamic MSD theory**. Metre-scale comparisons with that theory are therefore not independent of it. Lab 34 never uses the gain: its test is internal to the volt-unit signal.
- **Selection** (`conditioning.ipynb`): $|v-v_0|\le0.01\,\sigma_v$ per trace, with $v_0\in\{0,0.5,1,2\}\sigma_v$. Initial position is not conditioned. The theory averages over a Gaussian $x_0$, matching that rule.
- **Open item, not an error claim.** In the authors' analytic function `e_and_f`, a $v_0$-dependent term `z*v0*s_minus_half_b_inverse_form` is commented out. It vanishes at $v_0=0$, so the headline zero-velocity curve is unaffected. Whether the nonzero-speed analytic curves omit a physical contribution has **not** been determined. Settling it requires deriving the conditional mean of the hydrodynamic Langevin equation independently.

## Result

The test: covariances from the first half of each trace predict the held-out second half's conditional displacement second moment. The prediction uses the measurement-level Gaussian identity

$$
\mathbb E[D_k^2\mid |W|\le b]=u_k-\frac{r_k^2}{s}+\frac{r_k^2}{s^2}\,\mathbb E[W^2\mid|W|\le b].
$$

No hydrodynamic model, mass, or gain enters.

| Run | Verdict (preregistered) | max $\lvert z\rvert$ | median $\lvert$rel. error$\rvert$ | selected starts |
|---|---|---:|---:|---:|
| Particle, 1% bin | **AGREE** | 1.62 | 3.2% | 2,750 |
| Empty trap, 1% bin | DISAGREE | 3.26 | 3.4% | 2,844 |

**Particle.**
- **Exponent:** the descriptive log-log slope of the observed zero-velocity second moment over lags 1–8 (0.75–6 µs) is **2.517**. That is the published super-ballistic $t^{5/2}$ regime.
- **Robustness:**
  - leave-one-trace-out median errors 2.5–4.7%;
  - block-length sensitivity max $|z|$ 1.62–1.95;
  - conditional means at $\pm\sigma_v$ predicted to 0.3–1.3%.
- **Interpretation:** the conditioned $t^{5/2}$ is fully accounted for, to a few percent, by the second-order Gaussian structure of the measured signal. That is what [[Public Data Lead — Conditioned Hydrodynamic Brownian Motion]] derives for a velocity covariance with a square-root cusp ($\alpha=1/2$). It supports the paper's Gaussian-conditioning account. It does not independently confirm Basset hydrodynamics, because any process with the same measured covariance would pass.

**Systematic shortfall (post hoc).** All twelve particle lags fall 0.6–4.7% below prediction. Lags share data, so these are not twelve independent signs. Over the 5% and 20% bins the shortfall persists at about 3%; with more selected starts it becomes nominally significant (max $|z|$ 2.5 and 4.1).

**Empty trap.**
- The disagreement is confined to lags 1–2: −9.8% and −7.0%.
- Velocity variance changes by up to 54% between quarters of a trace, versus at most 13% with the particle present.
- $D_{64}$ is strongly platykurtic, with excess kurtosis −0.78.

**Working hypothesis** (generated after seeing the data and **untested**): slowly varying detector-noise power makes small-$|W|$ selection favour quieter stretches. That biases observed short-lag moments low, which is the mechanism planted in the negative control. It would explain both the empty-trap failure and part of the particle shortfall. A frozen follow-up would have to test it, for example by conditioning within locally variance-normalised segments, or by modelling noise power as a covariate. Positive particle excess kurtosis (0.09–0.17) is small and has not been separated from this mechanism.

## Limits

- **Shared processing.** Calibration and test halves share the authors' deconvolution and block averaging. The split guards against tuning on test statistics, not against processing artefacts common to both halves.
- **Few independent traces.** Six traces of 84 ms; overlapping start windows are handled only by block resampling.
- **Error bars too small.** Bootstrap standard errors are about 20% too small in self-tests. The particle verdict survives the correction; the empty-trap $z=3.26$ would drop to about 2.7.
- **Short lags only.** 64 lags (48 µs) and below. The trap-dominated regime was not examined.

## Next

> [!note] Update 2026-10-08
> - **Item 1 is settled.** [[Derivation — Equilibrium Conditioning of a Hydrodynamic Brownian Particle]] shows that omitting the term is correct for the equilibrium ensemble. Lab 39 checks this in the time domain: the extra term is the mean motion after release from steady dragging.
> - **Item 2 is done**, in [[Benchmark 016 — Stratified Conditioning and an Estimator Artifact]]. Noise-power drift explains the empty-trap failure. Most of the particle shortfall is calibration transfer between trace halves; the in-sample residual is −0.8% ± 1.0%.
> - **The gain-free test** is [[Benchmark 015 — Gain-Free Test of Hydrodynamic Memory]]. Its synthetic controls are done; the real-data run is pending.

1. Independently derive the hydrodynamic conditional mean for $v_0\neq0$ and settle the commented-out term.
2. Freeze and run a nonstationary-noise-aware conditioning protocol (see the hypothesis above) on the same files, labelled as a second-stage analysis on already-inspected data.
3. Compare the metre-unit curves with the authors' theory only alongside an explicit note that the gain is theory-fitted.

[[Public Data Lead — Conditioned Hydrodynamic Brownian Motion]] · [[Research Frontier — Identifiability Before Discovery]] · [[Computational Lab Index]] · [[Synthesis Lab]]
