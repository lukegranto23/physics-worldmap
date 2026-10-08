"""Does the conditioned MSD depend on how velocity is estimated? A frozen confirmatory test; no novelty claim.

Background (post hoc, 2026-10-08): under the published Basset model the bin-and-stencil
measurement operator suppresses the zero-velocity conditioned MSD to 0.26-0.87 of the
continuum curve over 0.75-12 us and steepens its log-log slope to about 2.93, while
detector noise supplies 9-71% of the measured value. Their near cancellation would explain
the published agreement of the data with the continuum t^{5/2} curve.

Frozen test (this docstring and the code were committed before --data was run):
  Variants: velocity stencils of order 2, 4, 8 (central differences) on positions coarsened
  by c = 1, 2, 4 bins (box averages; spacing c*750 ns). Nine variants; reference = order 8, c = 1
  (the published processing). Common physical times T = 3, 6, 12, 24 us.
  Observable: O_v(T) = E[(D_T - E D_T)^2 | |W - E W| <= 0.01 sd(W)], pooled over all six full
  traces, W recomputed from the coarsened positions with the variant stencil.
  Statistic: rho_v(T) = O_v(T)/O_ref(T); gain and most shared systematics cancel.
  Predictions:
    H_cont (continuum reading): rho = 1 for every variant.
    H_fwd  (forward model): rho from published Basset theory through each variant's operator,
           plus that variant's empty-trap noise moments, with the published gain.
  Uncertainty: non-overlapping 2000-base-sample blocks resampled within traces, the same blocks
  for every variant (paired), 200 replicates, seed 2026100871; SE of log rho per (v, T).
  Decision: over the 8 non-reference variants x 4 times, compute
    Z_fwd = sum (log rho_obs - log rho_fwd)^2 / se^2 and Z_cont likewise.
    H_fwd FAVOURED if Z_cont - Z_fwd > 25 and the median |log rho_obs - log rho_fwd| < 0.05;
    H_cont FAVOURED if Z_fwd - Z_cont > 25; otherwise UNRESOLVED.
  Self-test (synthetic, lab 38 generator, Basset truth plus white and smooth noise; empty-trap
  noise records synthesised independently): the decision must return H_fwd FAVOURED. If not,
  the real-data result is reported as NOT INTERPRETABLE.

    python 41_processing_dependence_test.py --selftest
    python 41_processing_dependence_test.py --data <dir with Dryad files>
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
OUT = HERE / "results" / "processing_dependence"


def load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


lab38 = load("lab38", "38_gain_free_selftest.py")
lab35 = lab38.lab35
lab34 = lab35.lab34

DT = 7.5e-7
STENCILS = {2: np.array([-1/2, 0, 1/2]),
            4: np.array([1/12, -2/3, 0, 2/3, -1/12]),
            8: lab34.STENCIL8}
COARSE = [1, 2, 4]
TIMES_US = [3, 6, 12, 24]
REF = (8, 1)
GAIN2_PUB = 861966767682287.1
BIN = 0.01


def variants():
    return [(o, c) for c in COARSE for o in STENCILS]


def coarsen(y, c):
    n = len(y)//c*c
    return y[:n].reshape(-1, c).mean(axis=1)


def stencil_velocity(y, d, dt):
    h = len(d)//2
    return y[h:-h], np.convolve(y, d[::-1], mode="valid")/dt


def theory_moments(order, c, lags):
    """Particle u, r, s (m^2 units) for the variant operator under published Basset."""
    g0, a0, k0 = lab35.physical_to_scaled(lab35.PUB["r"], lab35.PUB["K"])
    ker = lab35.Kernel(g0, a0, k0)
    r_ = lab35.PUB["r"]
    mass = 4/3*np.pi*r_**3*lab35.PUB["rho_p"] + 2/3*np.pi*r_**3*lab35.PUB["rho_f"]
    kTm = lab35.KB*lab35.PUB["T"]/mass
    x, w = np.polynomial.legendre.leggauss(24)
    u = 0.5*DT*(x + 1)
    wu = 0.5*DT*w*(1 - u/DT)/DT
    Cx = lambda tt: -ker.int_mchi_minus_limit(np.abs(tt))
    G1 = lambda n: (Cx(n*DT + u) + Cx(n*DT - u)) @ wu
    cache = {}

    def Gc(n):      # covariance of c-bin averages, n in coarse samples
        if n not in cache:
            cache[n] = sum(G1(c*n + i - j) for i in range(c) for j in range(c))/c**2
        return cache[n]

    d = STENCILS[order]
    h = len(d)//2
    ls = np.arange(-h, h + 1)
    dtc = c*DT
    s = kTm*sum(d[i]*d[j]*Gc(ls[i] - ls[j]) for i in range(len(d)) for j in range(len(d)))/dtc**2
    r = kTm*np.array([sum(d[i]*Gc(k - ls[i]) for i in range(len(d)))/dtc for k in lags])
    uu = kTm*np.array([2*(Gc(0) - Gc(k)) for k in lags])
    return uu, r, s


def cond(u, r, s, b):
    return u - r**2/s + r**2/s**2*lab34.m2_truncated(b, s)


BLOCK = 2000   # base samples per bootstrap block, shared by all variants (paired resampling)


def block_table(Ys, order, c):
    """Per-block sums of the selected squared displacement and selection counts, with global centring."""
    lags = [int(round(T*1e-6/(c*DT))) for T in TIMES_US]
    d = STENCILS[order]
    h = len(d)//2
    per = []
    for tr, y in enumerate(Ys):
        yc = coarsen(np.asarray(y, float), c)
        Yv, Wv = stencil_velocity(yc, d, c*DT)
        n = len(Yv) - max(lags)
        D = np.stack([Yv[k:k + n] - Yv[:n] for k in lags])
        base = (np.arange(n) + h)*c                 # base-sample index of each start
        per.append((tr, Wv[:n], D, base // BLOCK))
    W = np.concatenate([p[1] for p in per])
    D = np.concatenate([p[2] for p in per], axis=1)
    mW, mD = W.mean(), D.mean(axis=1)
    s = np.mean((W - mW)**2)
    mom = {"u": np.mean((D - mD[:, None])**2, axis=1), "r": np.mean((D - mD[:, None])*(W - mW), axis=1), "s": s}
    b = BIN*np.sqrt(s)
    num, cnt = {}, {}
    for tr, Wt, Dt, blk in per:
        sel = np.abs(Wt - mW) <= b
        for k in np.unique(blk):
            m = sel & (blk == k)
            num[(tr, int(k))] = np.sum((Dt[:, m] - mD[:, None])**2, axis=1)
            cnt[(tr, int(k))] = int(m.sum())
    return lags, mom, num, cnt


def ratio_obs(num, cnt, keys):
    tot = sum(num[k] for k in keys if k in num)
    n = sum(cnt[k] for k in keys if k in cnt)
    return tot/n, n


def analyse(Yp, Ye, label, n_boot=200):
    vs = variants()
    pred_fwd, tabs = {}, {}
    for v in vs:
        lags, _, _, _ = block_table(Ye[:1], *v)
        _, ne, _, _ = block_table(Ye, *v)
        u, r, s = theory_moments(v[0], v[1], lags)
        st = GAIN2_PUB*s + ne["s"]
        pred_fwd[v] = cond(GAIN2_PUB*u + ne["u"], GAIN2_PUB*r + ne["r"], st, BIN*np.sqrt(st))
        tabs[v] = block_table(Yp, *v)
        print(label, v, "selected", ratio_obs(tabs[v][2], tabs[v][3], tabs[v][2].keys())[1], flush=True)
    ref = REF
    keys = sorted(set.intersection(*[set(tabs[v][2]) for v in vs]))
    by_trace = {}
    for k in keys:
        by_trace.setdefault(k[0], []).append(k)
    obs = {v: ratio_obs(tabs[v][2], tabs[v][3], keys)[0] for v in vs}
    rng = np.random.default_rng(2026100871)
    boot = {v: [] for v in vs}
    for _ in range(n_boot):
        draw = [ks[i] for ks in by_trace.values() for i in rng.integers(0, len(ks), len(ks))]
        for v in vs:
            tot = sum(tabs[v][2][k] for k in draw)
            n = sum(tabs[v][3][k] for k in draw)
            boot[v].append(tot/n)
    boot = {v: np.array(b) for v, b in boot.items()}
    rows = []
    Zf = Zc = 0.0
    dev_f = []
    for v in vs:
        if v == ref:
            continue
        lr_obs = np.log(obs[v]/obs[ref])
        lr_fwd = np.log(pred_fwd[v]/pred_fwd[ref])
        se = np.std(np.log(boot[v]/boot[ref]), axis=0, ddof=1)
        Zf += float(np.sum((lr_obs - lr_fwd)**2/se**2))
        Zc += float(np.sum(lr_obs**2/se**2))
        dev_f += list(np.abs(lr_obs - lr_fwd))
        rows.append({"variant_order_coarsen": list(v), "times_us": TIMES_US, "rho_obs": np.exp(lr_obs).tolist(),
                     "rho_fwd": np.exp(lr_fwd).tolist(), "se_log_rho": se.tolist(),
                     "abs_obs_over_fwd_minus_1": (obs[v]/pred_fwd[v] - 1).tolist()})
    med = float(np.median(dev_f))
    if Zc - Zf > 25 and med < 0.05:
        verdict = "H_fwd FAVOURED"
    elif Zf - Zc > 25:
        verdict = "H_cont FAVOURED"
    else:
        verdict = "UNRESOLVED"
    return {"label": label, "verdict": verdict, "Z_fwd": Zf, "Z_cont": Zc, "median_abs_log_dev_fwd": med, "rows": rows,
            "ref_obs_over_fwd_minus_1": (obs[ref]/pred_fwd[ref] - 1).tolist(), "blocks": len(keys)}


def synthetic_records(seed):
    """Basset truth through the lab 38 generator, scaled to volts with the published gain."""
    rng = np.random.default_rng(seed)
    g0, a0, k0 = lab35.physical_to_scaled(lab35.PUB["r"], lab35.PUB["K"])
    Yp, _, Ye, _ = lab38.make_records(rng, (g0, a0, k0), DT)
    r_ = lab35.PUB["r"]
    mass = 4/3*np.pi*r_**3*lab35.PUB["rho_p"] + 2/3*np.pi*r_**3*lab35.PUB["rho_f"]
    scale = np.sqrt(GAIN2_PUB*lab35.KB*lab35.PUB["T"]/mass)   # scaled units (kT = m = 1) -> volts
    return [y*scale for y in Yp], [y*scale for y in Ye]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--selftest", action="store_true")
    g.add_argument("--data", type=Path)
    args = ap.parse_args()
    meta = {"generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    if args.selftest:
        res = analyse(*synthetic_records(2026100872), "selftest_basset")
        meta["self_test_pass"] = res["verdict"] == "H_fwd FAVOURED"
        out_dir = OUT / "selftest"
    else:
        P34 = json.loads(lab34.PROTOCOL.read_text(encoding="utf-8"))
        for name, expected in P34["target"]["files_sha256"].items():
            if lab35.sha256(args.data / name) != expected:
                raise lab34.GateFailure(f"{name}: digest mismatch")
        st = json.loads((OUT / "selftest" / "results.json").read_text(encoding="utf-8"))
        meta["self_test_pass"] = st["meta"]["self_test_pass"]
        Yp, _ = lab34.load_traces(args.data / "barium_titanate_in_acetone_position.csv")
        Ye, _ = lab34.load_traces(args.data / "noise_position.csv")
        res = analyse(Yp, Ye, "dryad_v3")
        if not meta["self_test_pass"]:
            res["verdict"] = "NOT INTERPRETABLE (self-test failed)"
        out_dir = OUT / "dryad_v3"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "results.json").write_text(json.dumps(lab38.jsonable({"meta": meta, **res}), indent=2), encoding="utf-8")
    print(f"{res['label']}: {res['verdict']}  Z_fwd={res['Z_fwd']:.1f}  Z_cont={res['Z_cont']:.1f}  "
          f"median|dev|={res['median_abs_log_dev_fwd']:.3f}")
    for row in res["rows"]:
        print(row["variant_order_coarsen"], "rho_obs", np.round(row["rho_obs"], 3), "rho_fwd", np.round(row["rho_fwd"], 3))


if __name__ == "__main__":
    main()
