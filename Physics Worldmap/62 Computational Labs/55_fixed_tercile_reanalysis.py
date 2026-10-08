"""Post hoc revision (2026-10-08, after an internal referee report): fixed-tercile and pooled-moment noise attribution.

Lab 49's gaps() re-forms the speed terciles on the cells surviving the low-signal drop rule, and
recomputes G_raw on that subset too. In the regime where it is applied, this biases f_noise
(referee point A3; e.g. in synthetic no-coupling populations at sigma = 0.4, f = 0.83 rather than ~1).
Two corrected attributions:
  FIXED     terciles fixed on all cells by measured speed. Mean r* within each tercile over the cells
            passing the drop rule. G_raw is computed on all cells (the reported gap).
  POOLED    within each fixed tercile, r*_T = (sum C1 + n sigma^2)/(sum V - 2 n sigma^2), the ratio of
            pooled moments. No cell is dropped, and it is unbiased in expectation for white,
            homogeneous error.
f = 1 - G_corr/G_raw. Self-check: synthetic no-coupling and coupled populations (lab 49
generators) at the true sigma, plus the referee's regime (21-frame tracks, sigma 0.4-0.6).

    python 55_fixed_tercile_reanalysis.py --celltrackr <dir> --invitro <dir> --fish <master file>
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
def _m(n, f):
    s = importlib.util.spec_from_file_location(n, HERE / f); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
lab49 = _m("lab49", "49_speed_persistence_noise_test.py")
lab50 = _m("lab50", "50_in_vitro_speed_persistence_test.py")
lab53 = _m("lab53", "53_calibrated_speed_persistence_test.py")
OUT = HERE / "results" / "fixed_tercile_reanalysis.json"
GRID = np.round(np.arange(0, 1.01, 0.1), 2)


def attrib(tracks, sigma):
    sp, V, C1 = lab49.cell_moments(tracks)
    lo, hi = np.quantile(sp, [1/3, 2/3])
    T = {"slow": sp <= lo, "fast": sp >= hi}
    r = C1/V
    g_raw = r[T["fast"]].mean() - r[T["slow"]].mean()
    ok = V - 2*sigma**2 >= 0.2*V
    rs = (C1 + sigma**2)/(V - 2*sigma**2)
    fixed = {k: rs[m & ok].mean() if (m & ok).sum() >= 3 else np.nan for k, m in T.items()}
    pooled = {}
    for k, m in T.items():
        den = V[m].sum() - 2*m.sum()*sigma**2
        pooled[k] = (C1[m].sum() + m.sum()*sigma**2)/den if den > 0 else np.nan
    gf, gp = fixed["fast"] - fixed["slow"], pooled["fast"] - pooled["slow"]
    pr = C1[T["fast"]].sum()/V[T["fast"]].sum() - C1[T["slow"]].sum()/V[T["slow"]].sum()
    return {"G_raw": float(g_raw), "f_fixed": float(1 - gf/g_raw), "G_raw_pooled": float(pr), "f_pooled": float(1 - gp/pr),
            "dropped_slow": int((T["slow"] & ~ok).sum()), "dropped_fast": int((T["fast"] & ~ok).sum())}


def curve(tracks):
    return [attrib(tracks, s) for s in GRID]


def selfcheck(rng):
    rows = []
    for coupled in (False, True):
        tr, sg = lab49.synthetic(coupled, int(rng.integers(1e9)))
        a = attrib(tr, sg); rows.append({"case": f"lab49 synthetic coupled={coupled} sigma={sg}", **a})
    # referee regime: 1000 cells, 21 frames, dt 30 s, no coupling, sigma 0.4 and 0.6
    for sg in (0.4, 0.6):
        res = []
        for _ in range(5):
            vsd = np.exp(rng.normal(np.log(0.03), 0.6, 1000))
            tr = lab49.simulate_tracks([21]*1000, vsd, 150.0, sg, rng)
            res.append(attrib(tr, sg))
        rows.append({"case": f"no coupling, 21 frames, sigma={sg} (5 reps)",
                     "f_fixed_mean": float(np.mean([x["f_fixed"] for x in res])), "f_pooled_mean": float(np.mean([x["f_pooled"] for x in res]))})
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--celltrackr", type=Path, required=True)
    ap.add_argument("--invitro", type=Path, required=True)
    ap.add_argument("--fish", type=Path, required=True)
    a = ap.parse_args()
    rng = np.random.default_rng(2026100855)
    lab49.DT = 30.0
    out = {"status": "post hoc revision", "sigma_grid": GRID.tolist(), "selfcheck": selfcheck(rng), "datasets": {}}
    for row in out["selfcheck"]:
        print(row, flush=True)
    sets = {}
    for n in ("TCells", "BCells", "Neutrophils"):
        sets["LN " + n] = lab49.load_tracks(a.celltrackr / f"{n}.csv")
    for c in ("ICAM", "VCAM"):
        sets["in vitro " + c] = lab50.load_group(a.invitro, c)[0]
    G = lab53.load(a.fish)
    for g in ("fish_T/control", "fish_T/rockout", "fish_T/highfreq_control"):
        sets[g] = G[g]["tracks"]
    sets["fish_T/highfreq_control_x4"] = [r[::4] for r in G["fish_T/highfreq_control"]["tracks"]]
    for name, tr in sets.items():
        c = curve(tr)
        out["datasets"][name] = c
        print(f"{name:30s} G_raw {c[0]['G_raw']:+.3f} | f_fixed " + " ".join(f"{x['f_fixed']:.2f}" for x in c[1:7])
              + " | f_pooled " + " ".join(f"{x['f_pooled']:.2f}" for x in c[1:7]), flush=True)
    OUT.write_text(json.dumps(out, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
