"""Post hoc: why lab 53's MSD-intercept noise calibration fails on real cells, and a consistent alternative.

Post hoc (2026-10-08), after lab 53's frozen run. With lab 53's calibrated sigma, the 12 s fish
tracks and the Dicty tracks were over-corrected (f_noise 3.5 and 6). That is impossible if sigma
were white localization error: by Cauchy-Schwarz the true lag-1 covariance satisfies C1 <= V, so
    sigma^2 <= (V_hat - C1_hat)/3            (per coordinate; "CS bound").
The slowest third of the 12 s fish tracks have lag-1 step correlation +0.20, where white noise
of 0.49 um would force about -0.5.

Hypothesis: real cells have a fast motion component, decorrelating within about one frame. It adds
to the short-lag MSD but leaves no negative lag-1 dip, and a single-P OU fit then absorbs it into
the intercept. The persistence correction needs only the white-noise part, whose signature is the
lag-1 dip: C1_hat = C1 - sigma^2, while C_k for k >= 2 is untouched.

Estimators:
  OU-MSD    lab 53's estimator (median over tracks).
  lag-dip   per track, sigma_c^2 = C1_ext - C1_hat, with C1_ext = C2^2/C3 if C2 > C3 > 0, else 2 C2 - C3.
            The group value is sqrt(max(median sigma_c^2, 0)). Under convex (mixture) decay this is biased LOW.
  CS split  rank tracks by the first-half V_hat, take the slowest third, and evaluate the CS bound on
            the disjoint second halves (pooled moments). A valid UPPER bound, with no selection bias.
Synthetic validation (lengths from the 12 s fish tracks, dt 12 s): the velocity is OU(P) plus a fast
OU(tau_f = 3 s) component carrying a fraction phi of the velocity variance (phi = 0, 0.3, 0.6). P is
lognormal across cells (median 120 s) and switches within each track between P and P/5. White error
sigma is 0.15, 0.3 or 0.5 um.

    python 54_noise_calibration_consistency.py --data <master_trajectory_file>
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("lab53", HERE / "53_calibrated_speed_persistence_test.py")
lab53 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lab53)
OUT = HERE / "results" / "calibrated_speed_persistence" / "consistency_post_hoc.json"


def moments(r):
    s = np.diff(r, axis=0)
    return np.array([np.mean(s**2)] + [np.mean(s[k:]*s[:-k]) for k in (1, 2, 3)])


def lag_dip(tracks):
    s2 = []
    for r in tracks:
        V, C1, C2, C3 = moments(r)
        ext = C2**2/C3 if (C2 > C3 > 0) else 2*C2 - C3
        s2.append(ext - C1)
    return float(np.sqrt(max(np.median(s2), 0)))


def cs_split(tracks):
    tr = [r for r in tracks if len(r) >= 14]
    h = [len(r)//2 for r in tr]
    V1 = np.array([np.mean(np.diff(r[:k], axis=0)**2) for r, k in zip(tr, h)])
    idx = np.argsort(V1)[:max(3, len(tr)//3)]
    M = np.mean([moments(tr[i][h[i]:]) for i in idx], axis=0)
    return float(np.sqrt(max((M[0] - M[1])/3, 0)))


def synth(lens, dt, sigma, phi, rng, vsd=0.08):
    out = []
    for n in lens:
        P0 = rng.lognormal(np.log(120.0), 0.5); P = P0; tf = 3.0; h = 0.5
        vs, vf = rng.normal(0, vsd*np.sqrt(1 - phi), 2), rng.normal(0, vsd*np.sqrt(phi) + 1e-12, 2)
        pos = np.zeros((n, 2)); sub = int(round(dt/h))
        af = np.exp(-h/tf)
        for i in range(1, n):
            if i % 10 == 0:
                P = P0 if rng.random() < 0.5 else P0/5
            a = np.exp(-h/P); step = np.zeros(2)
            for _ in range(sub):
                vs2 = a*vs + np.sqrt(1 - a*a)*vsd*np.sqrt(1 - phi)*rng.normal(size=2)
                vf2 = af*vf + np.sqrt(1 - af*af)*vsd*np.sqrt(phi)*rng.normal(size=2)
                step += 0.5*(vs + vs2 + vf + vf2)*h
                vs, vf = vs2, vf2
            pos[i] = pos[i-1] + step
        out.append(pos + rng.normal(0, sigma, (n, 2)))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", type=Path, required=True)
    a = ap.parse_args()
    G = lab53.load(a.data)
    rng = np.random.default_rng(2026100854)
    out = {"script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), "status": "post hoc", "synthetic": [], "real": {}}
    hf = G["fish_T/highfreq_control"]
    lens = [len(r) for r in hf["tracks"]]
    for phi in (0.0, 0.3, 0.6):
        for sg in (0.15, 0.3, 0.5):
            syn = synth(lens, hf["dt"], sg, phi, rng)
            long = [r for r in syn if len(r) >= lab53.MIN_CAL]
            row = {"phi": phi, "sigma_true": sg, "ou_msd": float(np.median([lab53.sigma_ou(r) for r in long])),
                   "lag_dip": lag_dip(syn), "cs_split_upper": cs_split(syn)}
            out["synthetic"].append(row)
            print("synthetic", {k: round(v, 3) for k, v in row.items()}, flush=True)
    saved = {r["label"]: r for r in json.loads((HERE / "results/calibrated_speed_persistence/results.json").read_text())["runs"]}
    for g, d in G.items():
        tr = d["tracks"]
        long = [r for r in tr if len(r) >= 30]
        if len(long) < 10:
            continue
        ld = lag_dip(long); cs = cs_split(long)
        bs = np.array([[lag_dip(s), cs_split(s)] for s in ([long[i] for i in rng.integers(0, len(long), len(long))] for _ in range(300))])
        r = saved.get(g)
        f_ld = lab53.f_at(r, ld) if r and r["G_raw"] > 0.05 else None
        f_cs = lab53.f_at(r, cs) if r and r["G_raw"] > 0.05 else None
        out["real"][g] = {"dt": d["dt"], "tracks_ge30": len(long), "lag_dip_sigma": ld, "lag_dip_16_84": np.percentile(bs[:, 0], [16, 84]).tolist(),
                          "cs_split_upper": cs, "cs_split_16_84": np.percentile(bs[:, 1], [16, 84]).tolist(),
                          "f_noise_at_lag_dip": f_ld, "f_noise_at_cs_upper": f_cs}
        print(g, {k: (np.round(v, 3).tolist() if isinstance(v, (list, float)) else v) for k, v in out["real"][g].items()}, flush=True)
    hfr = out["real"]["fish_T/highfreq_control"]
    for g in ("fish_T/control", "fish_T/rockout", "fish_T/highfreq_control_x4"):
        r = saved[g]
        out["real"].setdefault(g, {})["f_noise_at_transferred_highfreq_lag_dip"] = lab53.f_at(r, hfr["lag_dip_sigma"])
        out["real"][g]["f_noise_at_transferred_highfreq_cs_upper"] = lab53.f_at(r, hfr["cs_split_upper"])
        print(g, "transferred 12 s calibration: f at lag-dip", round(out["real"][g]["f_noise_at_transferred_highfreq_lag_dip"], 3),
              "f at CS upper", round(out["real"][g]["f_noise_at_transferred_highfreq_cs_upper"], 3))
    OUT.write_text(json.dumps(out, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
