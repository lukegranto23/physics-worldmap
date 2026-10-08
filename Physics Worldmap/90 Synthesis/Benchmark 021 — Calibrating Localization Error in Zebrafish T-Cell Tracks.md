---
type: computational-benchmark
field: Biophysics
epistemic_status: effective
level: advanced
tags: [cell-migration, speed-persistence-coupling, localization-noise, calibration, zebrafish, t-cells, reanalysis]
created: 2026-10-08
updated: 2026-10-08
note_maturity: expanded
source_audit: public-dataset-provenance-and-checksum-recorded
---

# Benchmark 021 — Calibrating Localization Error in Zebrafish T-Cell Tracks

**Status:** a frozen test (lab 53, committed as `4028d77` before any real-data statistic was computed, with one pre-data code fix) and a post hoc consistency analysis (lab 54). No novelty claim.

**Data:** the tracks of Jerison and Quake, *eLife* 9:e53933 (2020), from github.com/erjerison/TCellMigration. These are 2D tracks in µm:

| Group | Tracks | Frame interval |
|---|---|---|
| Zebrafish T cells, control | 712 | 45 s |
| Zebrafish T cells, rockout | 236 | 45 s |
| Zebrafish T cells, high frequency | 29 | 12 s, about 830 frames each |
| Mouse T cells (Gérard) | 42 + 123 | 30 s |
| *Dictyostelium* (Gautreau) | 3 × ~40 | 5 s |

This is the dataset at the centre of the speed–turning debate (Ganusov, Zenkov & Majumder 2023). The authors' own artefact check simulated a single assumed noise level, about 0.45 µm.

## Frozen result (lab 53)

The calibration estimator fits each long track's MSD with an OU-walk-plus-white-noise form. Its synthetic self-test passed for the 12 s fish and Dicty groups. It gave σ = 0.49 µm (12 s fish), 0.77 µm (rockout) and 0.12–0.22 µm (Dicty). The frozen verdicts were:

| Group | $G_\text{raw}$ | $f_\text{noise}$ at calibrated σ | Verdict |
|---|---:|---:|---|
| Fish control (45 s) | 0.58 | 0.21 (12 s calibration transferred) | NOISE SUBSTANTIAL |
| Fish rockout | 0.52 | 0.91 | NOISE MAJOR |
| Fish 12 s | 0.44 | **3.46** | NOISE MAJOR |
| Fish 12 s, coarsened to 48 s | 0.49 | 0.34 | NOISE SUBSTANTIAL |
| Mouse T control / KO | 0.67 / 0.45 | — | SIGMA UNIDENTIFIED |
| Dicty WT / Arp rescue / Arp KO | 0.19 / 0.26 / −0.03 | **6.1** / ∞ / — | MAJOR / UNDEFINED / NO COUPLING |

## Post hoc: the calibration is inconsistent (lab 54)

An attribution above 1 is impossible if σ is white localization error. By Cauchy–Schwarz, the true lag-1 step covariance satisfies $C_1\le V$, which gives
$$\sigma^2\le(\hat V-\hat C_1)/3.$$
Evaluated without selection bias, this is a valid upper bound. The slowest third of tracks is chosen by the first half of each track, and the bound is computed on the disjoint second halves ("CS split"). For the 12 s fish tracks the slowest third have lag-1 step correlation **+0.20**; 0.49 µm of white noise would force about −0.5.

**Mechanism, confirmed on synthetic data.** Suppose cells have a fast motion component that decorrelates within about a frame. It raises the short-lag MSD but leaves no negative lag-1 dip, and a single-P OU fit absorbs it into the noise intercept. Synthetic tracks with the 12 s fish lengths show this:

| True σ | Fast-component share | OU-MSD | Lag-dip | CS split (upper) |
|---|---|---|---|---|
| 0.15 | 0 / 0.3 / 0.6 | 0.18 / 0.24 / 0.29 | 0.11 / 0 / 0 | 0.27 / 0.29 / 0.31 |
| 0.30 | 0 / 0.3 / 0.6 | 0.31 / 0.36 / 0.39 | 0.26 / 0.25 / 0.24 | 0.36 / 0.39 / 0.41 |
| 0.50 | 0 / 0.3 / 0.6 | 0.51 / 0.54 / 0.56 | 0.48 / 0.49 / 0.46 | 0.55 / 0.56 / 0.58 |

- **OU-MSD** is biased high by the fast component.
- **Lag-dip** reads the white-noise signature, the dip in lag-1 covariance. It is biased low and blind below about 0.2 µm.
- **CS split** is a valid upper bound in all nine cases.

**Real data:**

| Group | Lag-dip σ (16–84%) | CS split upper σ (16–84%) | $f_\text{noise}$ at the upper bound |
|---|---|---|---|
| Fish 12 s | 0.06 (0–0.20) | **0.40** (0.37–0.46) | 1.8 at 12 s; **0.23 when coarsened to 48 s** |
| Fish control (45 s) | 0 | 1.2 (loose) | **0.13** with the 12 s upper bound transferred |
| Fish rockout | 0.38 (0.33–0.40) | 0.71 (0.66–0.78) | 0.34–0.76 with its own bounds; 0.39 transferred |
| Mouse T control | 0 | 0.35 (0.24–0.42) | ≤ 0.42 |
| Dicty WT / rescue | 0 (0–0.05) | 0.15 / 0.13 | indeterminate: at 5 s even σ = 0.1 µm over-corrects |

The 0.49 µm calibration lies above the valid 12 s upper bound (0.40, with 84% bound 0.46), so it is excluded.

## Reading

1. **The fish T-cell coupling is robust to localization error at the authors' sampling.** Observed at 48 s, the same 29 high-frequency cells have $f_\text{noise}\le0.23$ (0.30 at the bootstrap 84% bound). With the 12 s bound transferred to the 45 s control movies, $f_\text{noise}\le0.13$. This agrees with the authors' own noise check, and here it rests on a data-internal calibration rather than an assumed σ. It does not address the sparse-sampling mechanism. Coarsening 12 s to 48 s raises $G$ only from 0.44 to 0.49.
2. **The standard MSD-intercept calibration is wrong for cells.** It mistakes fast real motion for localization error. It passed a synthetic self-test that lacked such a component, then failed a consistency check on real data. The persistence correction needs the white-noise part only, which is bounded by the lag-1 structure.
3. **The frame interval decides.** The same fish cells are noise-sensitive at 12 s (an upper-bound σ could explain everything) and robust at 48 s. Noise and sparse sampling bias opposite ends of the frame-interval range (Benchmark 019).
4. **Rockout** cells are slower and more noise-sensitive: between a third and three quarters of their gap is attributable to noise within the bounds. **Dicty** at 5 s cannot be decided from the tracks.
5. **In vitro** (Benchmark 020, 21-frame tracks): the CS split bound is too loose to help (0.5–0.8 µm). Long tracks are what make the calibration possible.

## Limits

Transferring the 12 s calibration to the 45 s movies assumes similar imaging settings. The coarsened result does not need that assumption, but it rests on 29 cells. The data are 2D projections, and motion blur is ignored. The OU walk is a null model. The lag-dip and CS-split estimators were developed after the frozen run, so the results above are post hoc.

[[Benchmark 019 — Localization Noise and the Speed-Persistence Coupling]] · [[Benchmark 020 — In Vitro T Cells and the Noise Margin of Speed-Persistence Coupling]] · [[Biophysics Map]] · [[Computational Lab Index]]
