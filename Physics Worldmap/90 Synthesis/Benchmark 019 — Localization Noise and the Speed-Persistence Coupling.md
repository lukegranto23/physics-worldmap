---
type: computational-benchmark
field: Biophysics
epistemic_status: effective
level: advanced
tags: [cell-migration, speed-persistence-coupling, localization-noise, measurement-artifact, immune-cells, reanalysis]
created: 2026-10-08
updated: 2026-10-08
note_maturity: expanded
source_audit: public-dataset-provenance-recorded; literature-from-search-summaries
---

# Benchmark 019 — Localization Noise and the Speed-Persistence Coupling

**Status:** theory (lab 48), plus a test on three public in vivo immune-cell track sets (lab 49). The test's final protocol was frozen and committed (`c795361`) before any real-data speed or persistence statistic was computed. Four dated pre-data amendments record the method development on synthetic data. No novelty claim. These are in vivo lymph-node data, so this is a test of how general the "universal" coupling is, not a reanalysis of its original in vitro experiments.

Carries the estimator lesson of [[Derivation — Conditioning on an Estimated Velocity]] from Brownian motion to cell migration.

## The claim and the known critique

Maiuri et al. (*Cell*, 2015) reported a *universal coupling between cell speed and persistence*: faster cells move straighter, across cell types. Ganusov, Zenkov and Majumder (*Phys. Biol.*, 2023) showed that sparse sampling, imaging at intervals comparable to the persistence time, can manufacture such a correlation when cells differ in persistence. As far as a limited search could tell, localization (centroid) error was flagged there as an obstacle at high frame rates but not modelled.

## Theory (lab 48)

Take a 2D Ornstein–Uhlenbeck persistent walk with **no** coupling between speed and persistence, sampled every $\Delta t$, with Gaussian localization error $\sigma$ per coordinate.

Per coordinate, the true steps have variance $V$ and lag-1 covariance $C_1$. The error adds $2\sigma^2$ to the variance and $-\sigma^2$ to the lag-1 covariance, because consecutive steps share a position. So consecutive measured steps have correlation

$$\rho=\frac{C_1-\sigma^2}{V+2\sigma^2},\qquad E[\cos\theta]=\tfrac{\pi}{4}\,\rho\;{}_2F_1\!\left(\tfrac12,\tfrac12;2;\rho^2\right).$$

For fixed persistence, slower cells have smaller $V$ and $C_1$ relative to $\sigma^2$, so they look less persistent. Speed heterogeneity alone therefore produces "faster cells are straighter". The closed form matches Monte Carlo to within 1–2% across five parameter sets.

## Method (lab 49, final protocol)

- **Persistence measure.** Per cell, $r_c=\hat C_{1,c}/\hat V_c$, the lag-1 step correlation. It inverts exactly under the model: $r^*_c=(\hat C_{1,c}+\sigma^2)/(\hat V_c-2\sigma^2)$.
- **Effect size.** The persistence gap $G$ is mean persistence of the fastest third of cells minus that of the slowest third.
- **Attribution.** The fraction of the gap due to noise is $f_\text{noise}(\sigma)=1-G_\text{corr}/G_\text{raw}$.
- **Why a curve, not a single number.** On synthetic data, with the true $\sigma$ the correction attributes 98% of a pure-noise coupling to noise, and 18% of a genuine coupling at $\sigma=0.2$ µm. But $\sigma$ itself is **not reliably identifiable** from tracks this short. A pooled lag-covariance estimator ranged 0.48–1.24 µm over 10 seeds for a true value of 1.0, and fails when persistence is heterogeneous. The primary output is therefore $f_\text{noise}(\sigma)$, together with $\sigma_{1/2}$: the noise level at which noise explains half the coupling.
- **Self-tests.** Both pass: no coupling gives $f_\text{noise}(1.0)=0.98$; genuine coupling gives $f_\text{noise}(0.2)=0.18$.

## Data

The data are celltrackR (GPL-2) two-photon tracks of cells in mouse lymph nodes (Miller lab; Wortel et al., *ImmunoInformatics* 2021). They are 2D, with a 24 s frame interval, and only tracks with at least 6 positions are used. The CSV exports are not redistributed; their SHA-256 digests are in `results/speed_persistence_noise/celltrackR/results.json`.

## Results

| Dataset | Cells | $G_\text{raw}$ (noise-correctable $r$) | Mean-cos gap | Spearman (speed, mean cos) | ×2-subsampled Spearman | $\sigma_{1/2}$ |
|---|---:|---:|---:|---:|---:|---|
| T cells | 199 | **−0.035** | 0.20 | 0.28 | 0.39 | none (no gap) |
| B cells | 74 | **0.214** | 0.32 | 0.61 | 0.69 | **0.4 µm** (0.3–0.4) |
| Neutrophils | 363 | **−0.108** | 0.02 | 0.02 | 0.25 | none (no gap) |

The pooled-lag $\sigma$ estimate is a low-precision guide only: 0.78 µm [0.52, 0.98] for T cells, unidentified for B cells, and 1.07 µm for neutrophils.

## Reading

1. **No universal coupling in these data.** In the noise-correctable persistence measure, T cells and neutrophils show no positive speed–persistence gap. Only B cells do.
2. **The B-cell coupling is fragile.** A localization error of only 0.3–0.4 µm would explain between half and all of it: $f_\text{noise}=0.48$ at 0.3 µm and over-correction ($>1$) at 0.4 µm. For centroid tracking of roughly 7 µm cells in two-photon stacks, that is plausible but unmeasured. Whether the B-cell coupling is biological cannot be settled from the tracks alone. It needs an independent noise calibration, for example the apparent motion of fixed or stationary objects.
3. **The common metric is the noise-sensitive one.** For T cells the standard turning-angle (mean cos) metric shows a positive gap of 0.20 and Spearman 0.28, where the noise-robust measure shows none. This is the direction the theory predicts.
4. **Sparse sampling pushes the same way.** Halving the frame rate raises the Spearman correlation in every dataset (0.28→0.39, 0.61→0.69, 0.02→0.25). This is consistent with the Ganusov et al. mechanism. Noise biases at fast frame rates and sparse sampling biases at slow ones, so for these data there may be **no frame interval free of artefact**. That is the cell-migration analogue of the "no clean window" result in [[Benchmark 017 — Processing Dependence of the Conditioned Super-Ballistic Signal]].

## Limits

- The data are 2D projections of 3D motion. The OU persistent walk is a null model, not a description of lymphocyte motility. Track lengths are short (median 11–38 frames).
- The noise-correctable measure $r_c$ is not the persistence measure used by Maiuri et al. The mean-cos statistics are given for comparison.
- In vivo lymph-node data differ from the in vitro assays behind the original claim. No conclusion is drawn about those experiments.
- Literature status comes from search summaries; the full texts of Maiuri et al. and Ganusov et al. were not read here.

## Next

1. Obtain an independent localization-error estimate, from fixed beads or stationary cells, for any dataset where the coupling is claimed.
2. **Done for one in vitro dataset:** [[Benchmark 020 — In Vitro T Cells and the Noise Margin of Speed-Persistence Coupling]]. In vitro T cells on ICAM-1 and VCAM-1 show a strong coupling. σ ≤ 0.6 µm (under one pixel) would explain half of it. A post hoc lower bound from near-immobile tracks (σ ≳ 0.2 µm) shows that noise explains at least 12–14% of it. The upper end cannot be bounded from the tracks.
3. **Done for zebrafish T cells:** [[Benchmark 021 — Calibrating Localization Error in Zebrafish T-Cell Tracks]] gives a data-internal noise bound. That coupling is robust (at most about 13–23% from noise at 45–48 s).
4. Extend the closed form to the mean-cos metric, so that published cos-based results can be corrected directly.

[[Derivation — Conditioning on an Estimated Velocity]] · [[Biophysics Map]] · [[Computational Lab Index]]
