---
type: computational-benchmark
field: Biophysics
epistemic_status: effective
level: advanced
tags: [cell-migration, speed-persistence-coupling, localization-noise, in-vitro, t-cells, reanalysis]
created: 2026-10-08
updated: 2026-10-08
note_maturity: expanded
source_audit: public-dataset-provenance-and-checksum-recorded
---

# Benchmark 020 — In Vitro T Cells and the Noise Margin of Speed-Persistence Coupling

**Status:** lab 50 (`50_in_vitro_speed_persistence_test.py`) applies the final protocol of [[Benchmark 019 — Localization Noise and the Speed-Persistence Coupling]], unchanged. It was frozen and committed (`849616a`) before any statistic of these tracks was computed, and its self-tests were rerun at 30 s. No novelty claim.

## Data

The data are Zenodo record 10.5281/zenodo.8420011 (CC-BY 4.0), "T cell dataset for CellTracksColab – 2" (file MD5 verified). They show T cells migrating **in vitro** on ICAM-1 or VCAM-1. Imaging was 10× phase contrast, every **30 s for 10 min**, giving 21 frames. Segmentation used StarDist and tracking used TrackMate, with **645 nm pixels** (source record 10.5281/zenodo.4034929).

Coordinates are calibrated µm, which was checked against the image size: X max 865 against 1344 px × 0.645 µm, and Y max 658 against 1024 px × 0.645 µm. There are 10 movies over 3 replicates per condition. Tracks with gaps (122) were excluded, as were tracks with fewer than 6 positions. The data are not redistributed.

## Results

| Group | Cells | $G_\text{raw}$ | Spearman (speed, mean cos) | ×2-subsampled Spearman | $f_\text{noise}$ at 0.19 µm (quantization floor) | at 0.3 µm | at 0.645 µm (1 px) | $\sigma_{1/2}$ |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| ICAM-1 | 820 | 0.93 | 0.83 | 0.80 | 0.05 | 0.16 | 0.62 | 0.6 µm |
| VCAM-1 | 1083 | 0.73 | 0.76 | 0.72 | 0.13 | 0.42 | >1 | 0.4 µm |
| All | 1903 | 0.87 | 0.80 | 0.76 | 0.09 | 0.28 | 0.97 | 0.5 µm |

**Frozen verdict, for all three groups: NOT ROBUST TO LOCALIZATION NOISE.** That is, $\sigma_{1/2}\le$ one pixel. On synthetic data, a genuinely coupled population can also receive this verdict. It means the coupling **cannot be distinguished from a noise artefact without knowing σ**. It does not mean the coupling is an artefact.

## Reading

1. **In vitro, the coupling is strong.** The gap is 0.73–0.93 and Spearman is 0.76–0.83, far stronger than in the in vivo lymph-node data of Benchmark 019. There, T cells and neutrophils showed no noise-correctable gap.
2. **It is probably mostly real, but the margin is under one pixel.** At σ ≈ 0.2 µm (about ⅓ px), which is plausible for StarDist centroids of ~10 µm cells at this pixel size, noise explains 6–15%. At 0.3 µm it explains 16–42%. At 0.4–0.6 µm, still below one pixel, it explains half or more. The data-internal lag estimate (0.0–0.16 µm, upper 84% ≤ 0.32 µm) points to the low end. That estimator is biased low when persistence is heterogeneous (see the Benchmark 019 self-tests), so it is not relied on.
3. **Sparse sampling is not the driver here.** Halving the frame rate slightly lowers the correlation, unlike the in vivo case.
4. **What would settle it** is an independent localization-error measurement for this pipeline: fixed cells, beads, or repeated segmentation of the same frames.

## Limits

These are 2D tracks of 10 minutes (21 frames). The OU walk is a null model. The persistence measure (lag-1 step correlation) is not the measure used by Maiuri et al. The speed thirds are formed after excluding low-signal cells at each σ. ICAM and VCAM are pooled across replicates.

[[Benchmark 019 — Localization Noise and the Speed-Persistence Coupling]] · [[Derivation — Conditioning on an Estimated Velocity]] · [[Biophysics Map]] · [[Computational Lab Index]]
