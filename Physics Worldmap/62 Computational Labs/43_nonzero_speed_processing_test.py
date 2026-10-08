"""Does lab 41's processing dependence extend to the published nonzero-speed curves? Frozen; no novelty claim.

Frozen 2026-10-08 after lab 41 (zero-speed: H_fwd FAVOURED) and before this script touched
the real data. Same nine variants (stencil order 2/4/8 x coarsening 1/2/4), times 3, 6, 12,
24 us, reference = order 8, c = 1, paired block bootstrap (2000-sample blocks, 200 replicates,
seed 2026100881).

Selection follows the authors' conditioning.ipynb: |W - v0| <= 0.01 sd(W) with
v0 = q sd(W), q in {0.5, 1, 2}; sd(W) is the variant's own measured velocity sd.
Observable: O_v(T) = E[(D_T - E D_T)^2 | selection] (displacement centred by its global mean).
Forward prediction: u - r^2/s + (r^2/s^2) E[W^2 | bin] with E[W^2 | bin] from the fitted
Gaussian law of W (centred), particle moments from published Basset through the variant
operator plus that variant's empty-trap noise moments, published gain.

For each q: Z_fwd and Z_cont over 8 variants x 4 times, as in lab 41
  (H_cont: rho = 1; H_fwd: rho from the forward model).
  H_fwd FAVOURED if Z_cont - Z_fwd > 25 and median |log dev| < 0.05; H_cont FAVOURED if
  Z_fwd - Z_cont > 25; otherwise UNRESOLVED (expected where ballistic mean terms dominate).
Self-test: lab 41's synthetic Basset records; reported per q, and the real-data verdict for a
q is NOT INTERPRETABLE unless that q's self-test is not H_cont FAVOURED.

    python 43_nonzero_speed_processing_test.py --selftest
    python 43_nonzero_speed_processing_test.py --data <dir with Dryad files>
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from scipy.special import erf

HERE = Path(__file__).resolve().parent
OUT = HERE / "results" / "nonzero_speed_processing"
spec = importlib.util.spec_from_file_location("lab41", HERE / "41_processing_dependence_test.py")
lab41 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lab41)
lab35, lab34, lab38 = lab41.lab35, lab41.lab34, lab41.lab38
SPEEDS = [0.5, 1.0, 2.0]
BIN = 0.01


def m2_window(center, half, s):
    """E[W^2 | center-half <= W <= center+half] for W ~ N(0, s)."""
    sd = np.sqrt(s)
    a, b = (center - half)/sd, (center + half)/sd
    phi = lambda x: np.exp(-x*x/2)/np.sqrt(2*np.pi)
    Z = 0.5*(erf(b/np.sqrt(2)) - erf(a/np.sqrt(2)))
    return s*(1 + (a*phi(a) - b*phi(b))/Z)


def tables(Ys, order, c, q):
    """Per-block selected sums for speed q, using lab 41's construction with a shifted window."""
    lags = [int(round(T*1e-6/(c*lab41.DT))) for T in lab41.TIMES_US]
    d = lab41.STENCILS[order]
    h = len(d)//2
    per = []
    for tr, y in enumerate(Ys):
        yc = lab41.coarsen(np.asarray(y, float), c)
        Yv, Wv = lab41.stencil_velocity(yc, d, c*lab41.DT)
        n = len(Yv) - max(lags)
        D = np.stack([Yv[k:k + n] - Yv[:n] for k in lags])
        per.append((tr, Wv[:n], D, ((np.arange(n) + h)*c)//lab41.BLOCK))
    W = np.concatenate([p[1] for p in per])
    D = np.concatenate([p[2] for p in per], axis=1)
    mW, mD = W.mean(), D.mean(axis=1)
    s = np.mean((W - mW)**2)
    center, half = q*np.sqrt(s), BIN*np.sqrt(s)
    num, cnt = {}, {}
    for tr, Wt, Dt, blk in per:
        sel = np.abs(Wt - mW - center) <= half
        for k in np.unique(blk):
            m = sel & (blk == k)
            num[(tr, int(k))] = np.sum((Dt[:, m] - mD[:, None])**2, axis=1)
            cnt[(tr, int(k))] = int(m.sum())
    return lags, {"s": s, "u": np.mean((D - mD[:, None])**2, axis=1), "r": np.mean((D - mD[:, None])*(W - mW), axis=1)}, num, cnt


def analyse(Yp, Ye, label, n_boot=200):
    vs = lab41.variants()
    out = {}
    for q in SPEEDS:
        pred, tabs = {}, {}
        for v in vs:
            lags, ne, _, _ = tables(Ye, *v, 0.0)
            u, r, s = lab41.theory_moments(v[0], v[1], lags)
            st = lab41.GAIN2_PUB*s + ne["s"]
            rt, ut = lab41.GAIN2_PUB*r + ne["r"], lab41.GAIN2_PUB*u + ne["u"]
            pred[v] = ut - rt**2/st + rt**2/st**2*m2_window(q*np.sqrt(st), BIN*np.sqrt(st), st)
            tabs[v] = tables(Yp, *v, q)
        keys = sorted(set.intersection(*[set(tabs[v][2]) for v in vs]))
        by_trace = {}
        for k in keys:
            by_trace.setdefault(k[0], []).append(k)
        obs = {v: lab41.ratio_obs(tabs[v][2], tabs[v][3], keys)[0] for v in vs}
        nsel = {v: lab41.ratio_obs(tabs[v][2], tabs[v][3], keys)[1] for v in vs}
        rng = np.random.default_rng(2026100881)
        boot = {v: [] for v in vs}
        for _ in range(n_boot):
            draw = [ks[i] for ks in by_trace.values() for i in rng.integers(0, len(ks), len(ks))]
            for v in vs:
                boot[v].append(sum(tabs[v][2][k] for k in draw)/max(sum(tabs[v][3][k] for k in draw), 1))
        boot = {v: np.array(b) for v, b in boot.items()}
        ref = lab41.REF
        Zf = Zc = 0.0
        dev, rows = [], []
        for v in vs:
            if v == ref:
                continue
            lo = np.log(obs[v]/obs[ref])
            lf = np.log(pred[v]/pred[ref])
            se = np.std(np.log(boot[v]/boot[ref]), axis=0, ddof=1)
            Zf += float(np.sum((lo - lf)**2/se**2))
            Zc += float(np.sum(lo**2/se**2))
            dev += list(np.abs(lo - lf))
            rows.append({"variant_order_coarsen": list(v), "rho_obs": np.exp(lo).tolist(), "rho_fwd": np.exp(lf).tolist(),
                         "se_log_rho": se.tolist(), "selected": nsel[v]})
        med = float(np.median(dev))
        verdict = ("H_fwd FAVOURED" if Zc - Zf > 25 and med < 0.05 else
                   "H_cont FAVOURED" if Zf - Zc > 25 else "UNRESOLVED")
        out[str(q)] = {"verdict": verdict, "Z_fwd": Zf, "Z_cont": Zc, "median_abs_log_dev_fwd": med, "rows": rows,
                       "ref_selected": nsel[ref], "ref_obs_over_fwd_minus_1": (obs[ref]/pred[ref] - 1).tolist()}
        print(f"{label} q={q}: {verdict}  Z_fwd={Zf:.1f} Z_cont={Zc:.1f} median|dev|={med:.3f} ref selected={nsel[ref]}", flush=True)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--selftest", action="store_true")
    g.add_argument("--data", type=Path)
    args = ap.parse_args()
    meta = {"generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    if args.selftest:
        res = analyse(*lab41.synthetic_records(2026100872), "selftest_basset")
        out_dir = OUT / "selftest"
    else:
        P34 = json.loads(lab34.PROTOCOL.read_text(encoding="utf-8"))
        for name, expected in P34["target"]["files_sha256"].items():
            if lab35.sha256(args.data / name) != expected:
                raise lab34.GateFailure(f"{name}: digest mismatch")
        st = json.loads((OUT / "selftest" / "results.json").read_text(encoding="utf-8"))
        Yp, _ = lab34.load_traces(args.data / "barium_titanate_in_acetone_position.csv")
        Ye, _ = lab34.load_traces(args.data / "noise_position.csv")
        res = analyse(Yp, Ye, "dryad_v3")
        for q, r in res.items():
            if st["speeds"][q]["verdict"] == "H_cont FAVOURED":
                r["verdict"] = "NOT INTERPRETABLE (self-test favoured H_cont)"
        out_dir = OUT / "dryad_v3"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "results.json").write_text(json.dumps(lab38.jsonable({"meta": meta, "speeds": res}), indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
