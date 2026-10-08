"""Post hoc: bracket the localization error of the in vitro T-cell pipeline from near-immobile tracks.

Post hoc (2026-10-08), after lab 50's frozen verdict. For the slowest 5% of tracks by step variance,
true motion contributes C1 >= 0 (persistent walk) and V >= 0. So
    sigma_lo = sqrt(max(-mean C1, 0))   (lower bound)   and   sigma_hi = sqrt(mean V / 2)  (upper bound).
Their lag-1 step correlation near -0.5 is the signature of noise-dominated steps.
Bootstrap over tracks, 1000 replicates, seed 2026100899. f_noise is read off lab 50's saved
sensitivity curve at the bracket ends. Caveat: debris and stuck cells may be localized more
precisely than deforming migrating cells, so the bracket applies to the pipeline's
positional error, not to shape-driven centroid jitter.

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
        out["groups"][name] = {"tracks_used": n, "mean_lag1_corr_slow": rmean, "sigma_lo": lo, "sigma_hi": hi,
                               "sigma_lo_16_84": np.percentile(bs[:, 0], [16, 84]).tolist(),
                               "sigma_hi_16_84": np.percentile(bs[:, 1], [16, 84]).tolist(),
                               "f_noise_at_sigma_lo": f_lo, "f_noise_at_sigma_hi": f_hi}
        print(f"{name}: slowest {n} tracks, mean lag-1 corr {rmean:.2f}; sigma in [{lo:.3f}, {hi:.3f}] um "
              f"(16-84%: lo {np.round(out['groups'][name]['sigma_lo_16_84'], 3)}, hi {np.round(out['groups'][name]['sigma_hi_16_84'], 3)}); "
              f"f_noise in [{f_lo:.2f}, {f_hi:.2f}]")
    OUT.write_text(json.dumps(out, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
