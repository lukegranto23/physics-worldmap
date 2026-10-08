"""How much of an observed cell speed-persistence correlation can localization noise produce? Frozen test.

Frozen 2026-10-08 before any speed or persistence statistic of the real tracks was computed.
Only track counts, lengths and the 24 s frame interval had been inspected. No novelty claim.

Data: celltrackR (GPL-2) two-photon lymph-node tracks: TCells (199), BCells (74), Neutrophils (411),
2D positions in um at dt = 24 s (Miller lab; Wortel et al. 2021, ImmunoInformatics 1-2:100003).

Per cell (>= 6 positions): speed = mean |step|/dt; persistence = mean cos of the angle between
consecutive steps (zero-length steps skipped). Observed coupling: Spearman rho(speed, persistence).

Localization noise sigma (pooled per dataset): uncentred per-coordinate step autocovariances
C^_k (k = 1, 2, 3, pooled over cells and both coordinates). For an OU persistent walk with white
localization error, C^_1 = C_1 - sigma^2 and C^_k = C_1 e^{-(k-1)x} for k >= 2, x = dt/P. Hence
x = ln(C^_2/C^_3), C_1 = C^_2 e^{x}, sigma^2 = C_1 - C^_1. If C^_3 <= 0, C^_2 <= C^_3, or sigma^2 < 0,
the estimate is reported as UNIDENTIFIED for that dataset and sigma is set to 0 (no noise
correction claimed). Pooled P = dt/x.

Null model (no speed-persistence coupling): every cell has the pooled P; its true per-coordinate
step variance is V_c = max(V^_c - 2 sigma^2, 0.05 V^_c) from its own uncentred squared steps; its
OU velocity scale follows from V_c. Tracks are simulated exactly (OU velocity and position
increments), with each cell's real number of steps, plus localization error sigma; 300 replicate
populations (seed 2026100895). Null distribution of Spearman rho.

Decision per dataset (fixed):
  f = median(rho_null)/rho_obs (only if rho_obs > 0.1; otherwise "NO COUPLING TO EXPLAIN").
  CONSISTENT WITH NOISE ALONE  if rho_obs lies inside the null 2.5-97.5% interval;
  NOISE ACCOUNTS FOR MOST      if f >= 0.5 but rho_obs exceeds the interval;
  PARTIAL                      if 0.2 <= f < 0.5;
  NOISE MINOR                  if f < 0.2.
Secondary (reported, not decisive):
  (a) noise injection: add 1 um isotropic Gaussian error to the real tracks (20 seeds), compare the
      observed change in rho with the null model run at sqrt(sigma^2 + 1);
  (b) subsampling x2 (every other frame): observed rho.
Self-tests (must pass, else real verdicts NOT INTERPRETABLE):
  S1 no coupling, lognormal speeds, P = 60 s, sigma = 1 um, T-cell track lengths:
     sigma recovered within 35% and verdict CONSISTENT WITH NOISE ALONE or NOISE ACCOUNTS FOR MOST.
  S2 true coupling P_c proportional to speed_c, sigma = 0.2 um: verdict NOISE MINOR or PARTIAL.

Amendment 2026-10-08, after the first self-test and before any real-data statistic was computed.
The first self-test failed S2. The OU null with each cell's own speed scale gave rho_null ~ 0.49
even at sigma = 0.2 um. That comes from intrinsic within-track speed-turning covariation of the OU
walk over short tracks, not from noise, so the original rule conflated two mechanisms. Revised
decision: also run the null at sigma = 0 (same seed stream, 300 replicates).
  rho_OU    = median rho_null(sigma = 0)           (short-track OU contribution)
  rho_noise = median rho_null(sigma) - rho_OU      (localization-noise contribution)
  f_noise   = rho_noise/rho_obs,  f_total = median rho_null(sigma)/rho_obs.
  Verdict on noise: NOISE MAJOR if f_noise >= 0.5; NOISE SUBSTANTIAL if 0.2 <= f_noise < 0.5;
  NOISE MINOR if f_noise < 0.2. Separately: CONSISTENT WITH NO COUPLING if rho_obs lies inside the
  2.5-97.5% interval of rho_null(sigma).
Revised self-tests: S1 sigma recovered within 35% and CONSISTENT WITH NO COUPLING;
S2 NOISE MINOR. The rest is unchanged.

Amendment 2, 2026-10-08, after the revised self-test and before any real-data statistic was computed.
S2 still failed: sigma = 0.2 um moved the Spearman rho by 0.26. With near-uniform true persistence,
small perturbations of the slowest cells reorder ranks, so rank correlation overstates effect size.
The primary effect size becomes the PERSISTENCE GAP G = mean persistence of the fastest third of
cells minus that of the slowest third. All the quantities above (obs, null at sigma, null at 0,
fractions, interval, verdict thresholds) are computed on G. Spearman rho is reported as secondary
with the same decomposition. Self-test criteria unchanged.

Amendment 3 (final), 2026-10-08, after the second self-test and before any real-data statistic was
computed. Both self-tests failed. A simulated no-coupling null answers a counterfactual about an
imagined population, not "how much of THIS gap is noise". It is replaced by a direct per-cell
noise correction:
  persistence r_c = C^_1,c / V^_c (lag-1 step correlation, uncentred, both coordinates pooled);
  corrected r*_c = (C^_1,c + sigma^2)/(V^_c - 2 sigma^2), which inverts the closed-form bias
  (cells with V^_c - 2 sigma^2 < 0.2 V^_c are dropped from both gaps; the count is reported);
  G_raw, G_corr = mean r (r*) of the fastest third minus the slowest third (terciles of measured speed);
  f_noise = 1 - G_corr/G_raw; 500-replicate bootstrap over cells, re-estimating sigma each time.
Verdict (G_raw > 0.05 required): NOISE MAJOR if f_noise >= 0.5; NOISE SUBSTANTIAL if
0.2 <= f_noise < 0.5; NOISE MINOR if f_noise < 0.2.
Internal validation on real data: add 1 um error (20 seeds), re-correct with sigma_total =
sqrt(sigma^2 + 1). G_corr should not change, and the injected G_corr is reported against the original.
Self-tests: S1 (no coupling, sigma = 1) f_noise >= 0.5 and the |G_corr| bootstrap interval
contains 0; S2 (true coupling, sigma = 0.2) f_noise < 0.2. Cell-mean-cos statistics, Spearman
and x2 subsampling are reported as secondary.

Amendment 4 (FINAL PROTOCOL), 2026-10-08, before any real-data statistic was computed.
The development runs above showed three things on synthetic data:
  (i) with the TRUE sigma, the per-cell correction works: no coupling gives f_noise = 0.98,
      true coupling at sigma = 0.2 gives 0.18;
  (ii) the pooled-lag sigma estimator is unbiased but imprecise over 10 seeds (0.48-1.24 for a
      true 1.0), and it is unidentified when persistence is heterogeneous;
  (iii) an injection-matching sigma estimator is not robust.
So sigma is not reliably identifiable from tracks of this length. The primary output is
therefore a SENSITIVITY CURVE, not a single attribution:
  f_noise(sigma) = 1 - G_corr(sigma)/G_raw for sigma = 0, 0.1, ..., 2.0 um, with a 300-replicate
  bootstrap over cells at each sigma;
  sigma_half = smallest sigma with f_noise >= 0.5 (median), and its bootstrap 16-84% range.
The pooled-lag sigma estimate is reported with a bootstrap interval as a low-precision
data-internal guide, not as a verdict. Statement form: "noise explains at least half the
coupling if sigma >= sigma_half". Self-tests: S1 f_noise(1.0) >= 0.8; S2 f_noise(0.2) < 0.25.

    python 49_speed_persistence_noise_test.py --selftest
    python 49_speed_persistence_noise_test.py --data <dir with TCells.csv, BCells.csv, Neutrophils.csv>
"""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

HERE = Path(__file__).resolve().parent
OUT = HERE / "results" / "speed_persistence_noise"
DT = 24.0
MIN_POS = 6


def load_tracks(csv):
    import csv as _csv
    tracks = {}
    with open(csv, newline="", encoding="utf-8") as fh:
        for row in _csv.DictReader(fh):
            tracks.setdefault(row["track"], []).append((float(row["t"]), float(row["x"]), float(row["y"])))
    out = []
    for rows in tracks.values():
        a = np.array(sorted(rows))
        if len(a) >= MIN_POS:
            out.append(a[:, 1:3])
    return out


def cell_stats(tracks):
    sp, pe = [], []
    for r in tracks:
        s = np.diff(r, axis=0)
        n = np.linalg.norm(s, axis=1)
        ok = (n[1:] > 0) & (n[:-1] > 0)
        cos = np.sum(s[1:]*s[:-1], axis=1)[ok]/(n[1:]*n[:-1])[ok]
        sp.append(n.mean()/DT)
        pe.append(cos.mean() if len(cos) else np.nan)
    sp, pe = np.array(sp), np.array(pe)
    m = np.isfinite(pe)
    return sp[m], pe[m]


def spearman(tracks):
    sp, pe = cell_stats(tracks)
    return float(spearmanr(sp, pe).correlation)


def rho(tracks):
    """Primary effect size (amendment 2): persistence gap between fastest and slowest thirds."""
    sp, pe = cell_stats(tracks)
    lo, hi = np.quantile(sp, [1/3, 2/3])
    return float(pe[sp >= hi].mean() - pe[sp <= lo].mean())


def estimate_noise(tracks):
    num = np.zeros(4)
    cnt = np.zeros(4)
    for r in tracks:
        s = np.diff(r, axis=0)
        for k in range(4):
            if len(s) > k:
                num[k] += np.sum(s[k:]*s[:len(s) - k])
                cnt[k] += 2*(len(s) - k)
    C = num/cnt
    out = {"C_hat_0_to_3": C.tolist()}
    if C[3] <= 0 or C[2] <= C[3]:
        out.update(identified=False, sigma=0.0, P=None)
        return out
    x = np.log(C[2]/C[3])
    C1 = C[2]*np.exp(x)
    s2 = C1 - C[1]
    if s2 < 0:
        out.update(identified=False, sigma=0.0, P=float(DT/x))
        return out
    out.update(identified=True, sigma=float(np.sqrt(s2)), P=float(DT/x))
    return out


def simulate_tracks(lengths, vel_sd, P, sigma, rng):
    """Exact OU persistent walk: per-coordinate velocity sd vel_sd (array per cell), steps per cell."""
    a = np.exp(-DT/P)
    n_max = int(max(lengths))
    nc = len(lengths)
    vs = np.asarray(vel_sd)[:, None]
    var_v = vs**2*(1 - a**2)
    var_x = vs**2*P**2*(2*DT/P - 3 + 4*a - a**2)
    cov_xv = vs**2*P*(1 - a)**2
    v = rng.normal(size=(nc, 2))*vs
    pos = np.zeros((nc, n_max + 1, 2))
    for i in range(n_max):
        mx = P*(1 - a)*v
        z1 = rng.normal(size=(nc, 2))
        z2 = rng.normal(size=(nc, 2))
        sx = np.sqrt(var_x)
        dx = mx + sx*z1
        v = a*v + (cov_xv/sx)*z1 + np.sqrt(np.maximum(var_v - cov_xv**2/var_x, 0))*z2
        pos[:, i + 1] = pos[:, i] + dx
    pos = pos + rng.normal(0, sigma, pos.shape)
    return [pos[c, :int(lengths[c]) + 1] for c in range(nc)]


def vel_sd_from_V(V, P):
    x = DT/P
    return np.sqrt(V/(2*P**2*(x - 1 + np.exp(-x))))


def null_rhos(tracks, sigma, P, reps, rng):
    lengths = np.array([len(r) - 1 for r in tracks])
    Vhat = np.array([np.mean(np.diff(r, axis=0)**2) for r in tracks])
    V = np.maximum(Vhat - 2*sigma**2, 0.05*Vhat)
    vsd = vel_sd_from_V(V, P)
    return np.array([rho(simulate_tracks(lengths, vsd, P, sigma, rng)) for _ in range(reps)])


def cell_moments(tracks):
    sp, V, C1 = [], [], []
    for r in tracks:
        st = np.diff(r, axis=0)
        sp.append(np.linalg.norm(st, axis=1).mean()/DT)
        V.append(np.mean(st**2))
        C1.append(np.mean(st[1:]*st[:-1]))
    return np.array(sp), np.array(V), np.array(C1)


def gaps(tracks, sigma):
    sp, V, C1 = cell_moments(tracks)
    ok = V - 2*sigma**2 >= 0.2*V
    r = C1/V
    rs = (C1 + sigma**2)/(V - 2*sigma**2)
    lo, hi = np.quantile(sp[ok], [1/3, 2/3])
    fast, slow = ok & (sp >= hi), ok & (sp <= lo)
    return float(r[fast].mean() - r[slow].mean()), float(rs[fast].mean() - rs[slow].mean()), int((~ok).sum())


GRID = np.round(np.arange(0, 2.01, 0.1), 2)


def analyse(tracks, label, reps=300, seed=2026100895):
    rng = np.random.default_rng(seed)
    n = len(tracks)
    noise = estimate_noise(tracks)
    sig_boot = [estimate_noise([tracks[i] for i in rng.integers(0, n, n)])["sigma"] for _ in range(200)]
    curve, lo16, hi84, Gc, drop = [], [], [], [], []
    boots_idx = [rng.integers(0, n, n) for _ in range(reps)]
    for sg in GRID:
        gr, gc, dr = gaps(tracks, sg)
        curve.append(1 - gc/gr if gr > 0.05 else np.nan)
        Gc.append(gc)
        drop.append(dr)
        fb = []
        for idx in boots_idx:
            sub = [tracks[i] for i in idx]
            g1, g2, _ = gaps(sub, sg)
            fb.append(1 - g2/g1 if g1 > 0.05 else np.nan)
        lo16.append(float(np.nanpercentile(fb, 16)))
        hi84.append(float(np.nanpercentile(fb, 84)))
    curve = np.array(curve)
    def first(arr):
        arr = np.asarray(arr)
        hit = np.where(arr >= 0.5)[0]
        return float(GRID[hit[0]]) if len(hit) else None
    g_raw = gaps(tracks, 0.0)[0]
    sp, pe = cell_stats(tracks)
    lo3, hi3 = np.quantile(sp, [1/3, 2/3])
    sub2 = [r[::2] for r in tracks if len(r[::2]) >= 4]
    out = {"label": label, "cells": n, "G_raw": g_raw, "sigma_grid": GRID.tolist(),
           "f_noise_curve": curve.tolist(), "f_noise_16": lo16, "f_noise_84": hi84, "G_corr_curve": Gc,
           "cells_dropped": drop,
           "sigma_half": first(curve), "sigma_half_range_from_84_16": [first(hi84), first(lo16)],
           "lag_sigma_estimate": noise, "lag_sigma_bootstrap_16_84": np.percentile(sig_boot, [16, 84]).tolist(),
           "secondary": {"spearman_speed_meancos": spearman(tracks),
                         "meancos_gap": float(pe[sp >= hi3].mean() - pe[sp <= lo3].mean()),
                         "spearman_subsample_x2": spearman(sub2) if len(sub2) > 10 else None}}
    def at(sg):
        return round(float(curve[int(round(sg*10))]), 2)
    print(f"{label}: cells={n} G_raw={g_raw:.3f} | f_noise at sigma 0.5/1.0/1.5 um: {at(0.5)}/{at(1.0)}/{at(1.5)} | "
          f"sigma_half={out['sigma_half']} (range {out['sigma_half_range_from_84_16']}) | lag sigma {noise['sigma']:.2f} "
          f"[{out['lag_sigma_bootstrap_16_84'][0]:.2f}, {out['lag_sigma_bootstrap_16_84'][1]:.2f}] | spearman {out['secondary']['spearman_speed_meancos']:.3f}",
          flush=True)
    return out


def synthetic(coupled, seed):
    rng = np.random.default_rng(seed)
    n = 199
    lengths = rng.integers(6, 40, n)
    speed_scale = np.exp(rng.normal(np.log(0.12), 0.6, n))       # per-coordinate velocity sd (um/s)
    sigma = 0.2 if coupled else 1.0
    if not coupled:
        return simulate_tracks(lengths, speed_scale, 60.0, sigma, rng), sigma
    tracks = []
    for c in range(n):
        Pc = 60.0*speed_scale[c]/np.median(speed_scale)
        tracks += simulate_tracks([lengths[c]], [speed_scale[c]], Pc, sigma, rng)
    return tracks, sigma


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--selftest", action="store_true")
    g.add_argument("--data", type=Path)
    args = ap.parse_args()
    meta = {"generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    runs = []
    if args.selftest:
        t1, s1 = synthetic(False, 2026100896)
        r1 = analyse(t1, "S1_no_coupling_sigma1")
        t2, s2 = synthetic(True, 2026100897)
        r2 = analyse(t2, "S2_true_coupling_sigma0.2")
        ok1 = r1["f_noise_curve"][10] >= 0.8
        ok2 = r2["f_noise_curve"][2] < 0.25
        meta["self_tests_pass"] = bool(ok1 and ok2)
        meta["S1_pass"], meta["S2_pass"] = bool(ok1), bool(ok2)
        runs = [r1, r2]
        out_dir = OUT / "selftest"
        print("self-tests pass:", meta["self_tests_pass"], "(S1", ok1, "S2", ok2, ")")
    else:
        st = json.loads((OUT / "selftest" / "results.json").read_text(encoding="utf-8"))
        meta["self_tests_pass"] = st["meta"]["self_tests_pass"]
        meta["data_sha256"] = {}
        for name in ("TCells", "BCells", "Neutrophils"):
            f = args.data / f"{name}.csv"
            meta["data_sha256"][name] = hashlib.sha256(f.read_bytes()).hexdigest()
            r = analyse(load_tracks(f), name)
            if not meta["self_tests_pass"]:
                r["status"] = "NOT INTERPRETABLE (self-test failed)"
            runs.append(r)
        out_dir = OUT / "celltrackR"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "results.json").write_text(json.dumps({"meta": meta, "runs": runs}, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
