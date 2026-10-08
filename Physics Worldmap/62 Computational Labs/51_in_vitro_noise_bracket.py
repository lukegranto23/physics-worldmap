"""Post hoc: bracket the localization error of the in vitro T-cell pipeline from near-immobile tracks.

Post hoc (2026-10-08), after lab 50's frozen verdict. For the slowest 5% of tracks by step variance,
true motion contributes C1 >= 0 (persistent walk) and V >= 0. So
    sigma_lo = sqrt(max(-mean C1, 0))   (lower bound)   and   sigma_hi = sqrt(mean V / 2)  (upper bound).
Their lag-1 step correlation near -0.5 is the signature of noise-dominated steps.
Bootstrap over tracks, 1000 replicates, seed 2026100899. f_noise is read off lab 50's saved
sensitivity curve at the bracket ends. Caveat: debris and stuck cells may be localized more
precisely than deforming migrating cells, so the bracket applies to the pipeline's
positional error, not to shape-driven centroid jitter.

Amendment (2026-10-08, same day, after the first run). A synthetic control added afterwards shows
that selecting tracks on the same noisy V used to evaluate them biases BOTH ends low. With true
sigma = 0.25 um and 30% immobile objects, the "upper bound" came out at about 0.19-0.21 um.
sigma_hi from full-track selection is therefore NOT a valid upper bound and is reported only
as "selected-track sigma". A split-half variant is added: select on the first half of each track
(>= 14 positions), evaluate C1 and V on the disjoint second half. Its upper bound is valid but loose.
The full-track lower bound is conservative in every synthetic case. Synthetic controls (lengths from
the real data, OU motile cells, immobile fraction 0.03/0.1/0.3, true sigma 0.25 um) are written to
the output, as is the dependence on the selected fraction.

    python 51_in_vitro_noise_bracket.py --data <dir containing Tracks/...>
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("lab50", HERE / "50_in_vitro_speed_persistence_test.py")
lab50 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lab50)
OUT = HERE / "results" / "in_vitro_speed_persistence" / "noise_bracket_post_hoc.json"


def bracket(tr, frac=0.05):
    V = np.array([np.mean(np.diff(r, axis=0)**2) for r in tr])
    C1 = np.array([np.mean(np.diff(r, axis=0)[1:]*np.diff(r, axis=0)[:-1]) for r in tr])
    idx = np.argsort(V)[:max(10, int(frac*len(V)))]
    return float(np.sqrt(max(-C1[idx].mean(), 0))), float(np.sqrt(V[idx].mean()/2)), float((C1[idx]/V[idx]).mean()), len(idx)


def split_half(tr, frac=0.05):
    tr = [r for r in tr if len(r) >= 14]
    h = [len(r)//2 for r in tr]
    V1 = np.array([np.mean(np.diff(r[:k], axis=0)**2) for r, k in zip(tr, h)])
    idx = np.argsort(V1)[:max(10, int(frac*len(tr)))]
    st = [np.diff(tr[i][h[i]:], axis=0) for i in idx]
    V = np.mean([np.mean(x**2) for x in st]); C = np.mean([np.mean(x[1:]*x[:-1]) for x in st])
    return float(np.sqrt(max(-C, 0))), float(np.sqrt(V/2)), len(tr), len(idx)


def synthetic(lens, p_imm, sigma, rng, dt=30.0):
    tr = []
    for n in lens:
        x = np.zeros((n, 2))
        if rng.random() >= p_imm:
            vsd, P = rng.lognormal(np.log(0.05), 0.8), rng.lognormal(np.log(150), 0.5)
            a = np.exp(-dt/P); v = rng.normal(0, vsd, 2)
            for i in range(1, n):
                v = a*v + np.sqrt(1 - a*a)*vsd*rng.normal(size=2); x[i] = x[i-1] + v*dt
        tr.append(x + rng.normal(0, sigma, (n, 2)))
    return tr


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", type=Path, required=True)
    args = ap.parse_args()
    saved = json.loads((HERE / "results" / "in_vitro_speed_persistence" / "zenodo_8420011" / "results.json").read_text())
    curves = {r["label"]: r for r in saved["runs"]}
    rng = np.random.default_rng(2026100899)
    out = {"script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), "status": "post hoc", "groups": {}}
    groups = {c: lab50.load_group(args.data, c)[0] for c in ("ICAM", "VCAM")}
    groups["ALL"] = groups["ICAM"] + groups["VCAM"]
    for name, tr in groups.items():
        lo, hi, rmean, n = bracket(tr)
        bs = np.array([bracket([tr[i] for i in rng.integers(0, len(tr), len(tr))]) [:2] for _ in range(1000)])
        r = curves[name]
        g = np.array(r["sigma_grid"]); fc = np.array(r["f_noise_curve"], float)
        f_lo, f_hi = float(np.interp(lo, g, fc)), float(np.interp(hi, g, fc))
        sh = split_half(tr)
        bs2 = np.array([split_half([tr[i] for i in rng.integers(0, len(tr), len(tr))])[:2] for _ in range(300)])
        fi = lambda x: float(np.interp(x, g, np.nan_to_num(fc, nan=np.inf)))
        out["groups"][name] = {"tracks_used": n, "mean_lag1_corr_slow": rmean, "sigma_lo": lo, "sigma_hi_selected_INVALID_as_bound": hi,
                               "fraction_dependence": {str(f): bracket(tr, f)[:2] for f in (0.02, 0.05, 0.1, 0.2)},
                               "split_half": {"sigma_lo": sh[0], "sigma_hi_valid": sh[1], "tracks_ge14": sh[2], "selected": sh[3],
                                              "sigma_lo_16_84": np.percentile(bs2[:, 0], [16, 84]).tolist(),
                                              "sigma_hi_16_84": np.percentile(bs2[:, 1], [16, 84]).tolist(),
                                              "f_noise_at_sigma_hi": fi(sh[1])},
                               "sigma_lo_16_84": np.percentile(bs[:, 0], [16, 84]).tolist(),
                               "sigma_hi_selected_16_84": np.percentile(bs[:, 1], [16, 84]).tolist(),
                               "f_noise_at_sigma_lo": f_lo, "f_noise_at_sigma_hi_selected": f_hi}
        print(f"   split-half: sigma in [{sh[0]:.3f}, {sh[1]:.3f}] um, f_noise at upper {fi(sh[1]):.2f}; "
              f"fraction dependence {out['groups'][name]['fraction_dependence']}")
        print(f"{name}: slowest {n} tracks, mean lag-1 corr {rmean:.2f}; lower {lo:.3f}, selected-track {hi:.3f} um "
              f"(16-84%: lo {np.round(out['groups'][name]['sigma_lo_16_84'], 3)}, selected-hi {np.round(out['groups'][name]['sigma_hi_selected_16_84'], 3)}); "
              f"f_noise at lower bound {f_lo:.2f} (at selected-track sigma {f_hi:.2f})")
    lens = [len(r) for r in groups["ALL"]]
    out["synthetic_controls_true_sigma_0.25"] = []
    for p in (0.03, 0.1, 0.3):
        st = synthetic(lens, p, 0.25, rng)
        row = {"p_immobile": p, "full_track": bracket(st)[:2], "split_half": split_half(st)[:2]}
        out["synthetic_controls_true_sigma_0.25"].append(row)
        print("synthetic", row)
    OUT.write_text(json.dumps(out, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
