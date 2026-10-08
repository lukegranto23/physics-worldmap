"""Preregistered Gaussian prediction of velocity-conditioned displacement; no novelty claim.

Calibration-half covariances predict held-out conditional displacement moments
through the measurement-level Gaussian identity. No hydrodynamic model is fitted.

    python 34_conditioned_displacement_reproduction.py --selftest
    python 34_conditioned_displacement_reproduction.py --data <dir with Dryad files>

Read the protocol's gates first: real data requires digest-verified files and a
prior text reading of the authors' notebooks.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from scipy.linalg import expm, cholesky
from scipy.special import erf

HERE = Path(__file__).resolve().parent
PROTOCOL = HERE / "conditioned_reproduction_protocol.json"
OUT = HERE / "results" / "conditioned_reproduction"
STENCIL8 = np.array([1/280, -4/105, 1/5, -4/5, 0, 4/5, -1/5, 4/105, -1/280])


class GateFailure(RuntimeError):
    pass


def sha256(path):
    with Path(path).open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


# ---------------------------------------------------------------- loading

def load_traces(path):
    with Path(path).open(encoding="utf-8-sig") as handle:
        first = handle.readline()
    delimiter = "," if "," in first else None
    try:
        [float(x) for x in first.replace(",", " ").split()]
        skip = 0
    except ValueError:
        skip = 1
    data = np.loadtxt(path, delimiter=delimiter, skiprows=skip, ndmin=2)
    if not np.all(np.isfinite(data)):
        raise GateFailure(f"{Path(path).name}: non-finite values")
    for layout, arr in (("columns", data), ("rows", data.T)):
        keep = []
        for col in arr.T:
            step = np.diff(col)
            is_time = np.all(step > 0) and np.allclose(step, step[0], rtol=1e-6, atol=0)
            if not is_time:
                keep.append(col)
        if 2 <= len(keep) <= 12 and arr.shape[0] > 10000:
            return [np.asarray(c, float) for c in keep], {"layout": layout, "shape": list(data.shape),
                                                          "traces": len(keep), "time_axis_removed": arr.shape[1] - len(keep),
                                                          "header_skipped": bool(skip)}
    raise GateFailure(f"{Path(path).name}: unrecognised layout {data.shape}")


# ---------------------------------------------------------------- statistics

def m2_truncated(b, s):
    z = b/np.sqrt(s)
    if z < 1e-3:
        return b*b/3*(1 - z*z/5)
    phi = np.exp(-z*z/2)/np.sqrt(2*np.pi)
    return s*(1 - 2*z*phi/erf(z/np.sqrt(2)))


class Half:
    """Cumulative sums over start indices of one trace half, for O(1) block sums."""

    def __init__(self, Y, W, lo, hi, lags):
        j = np.arange(lo, hi - max(lags))
        self.n = len(j)
        self.W = W[j]
        self.D = np.stack([Y[j + k] - Y[j] for k in lags])
        cs = lambda a: np.concatenate([np.zeros(a.shape[:-1] + (1,)), np.cumsum(a, axis=-1)], axis=-1)
        self.cs = cs
        self.cW, self.cW2 = cs(self.W), cs(self.W**2)
        self.cD, self.cD2, self.cDW = cs(self.D), cs(self.D**2), cs(self.D*self.W)

    def block_sums(self, arrays, starts, L):
        if starts is None:
            return [a[..., -1] for a in arrays]
        return [(a[..., starts + L] - a[..., starts]).sum(axis=-1) for a in arrays]


def pooled(halves, which, rng, L):
    """Sums over traces of block-resampled (or full, rng=None) cumulative arrays."""
    totals, count = None, 0
    for h in halves:
        if rng is None:
            starts, n = None, h.n
        else:
            nb = h.n // L
            starts = rng.integers(0, h.n - L + 1, nb)
            n = nb*L
        sums = h.block_sums([getattr(h, a) for a in which], starts, L)
        totals = sums if totals is None else [t + s for t, s in zip(totals, sums)]
        count += n
    return [t/count for t in totals], count


def selection_sums(h, lo_w, hi_w):
    sel = (h.W >= lo_w) & (h.W <= hi_w)
    return {"n": h.cs(sel.astype(float)), "D": h.cs(h.D*sel), "D2": h.cs(h.D**2*sel), "W": h.cs(h.W*sel)}


def evaluate(cal, test, lags, design, rng=None, L=None, bins=None):
    (mW, mW2, mD, mD2, mDW), _ = pooled(cal, ["cW", "cW2", "cD", "cD2", "cDW"], rng, L)
    s = mW2 - mW**2
    u = mD2 - mD**2
    r = mDW - mD*mW
    out = {"s": s, "u": u, "r": r, "muD": mD, "muW": mW}
    for name, (center, b) in bins.items():
        tot = {"n": 0.0, "D": 0.0, "D2": 0.0, "W": 0.0}
        for h, sums in zip(test, design[name]):
            if rng is None:
                starts = None
            else:
                starts = rng.integers(0, h.n - L + 1, h.n // L)
            vals = h.block_sums([sums[k] for k in tot], starts, L)
            for k, v in zip(tot, vals):
                tot[k] = tot[k] + v
        n = tot["n"]
        with np.errstate(invalid="ignore", divide="ignore"):
            ED, ED2, EW = tot["D"]/n, tot["D2"]/n, tot["W"]/n
        obs2 = ED2 - 2*mD*ED + mD**2
        if center == 0:
            pred = u - r**2/s + r**2/s**2*m2_truncated(b, s)
            out[name] = {"n": float(n), "obs": obs2, "pred": pred}
        else:
            out[name] = {"n": float(n), "obs": ED - mD, "pred": r/s*(EW - mW)}
    return out


def kurtosis(x):
    x = x - x.mean()
    return float(np.mean(x**4)/np.mean(x**2)**2 - 3)


def analyse(Ys, Ws, protocol, label):
    lags = protocol["design"]["lags_samples"]
    unc = protocol["uncertainty"]
    if len(Ys) != len(Ws) or any(len(y) != len(w) for y, w in zip(Ys, Ws)):
        raise GateFailure(f"{label}: position/velocity traces do not align")
    cal, test = [], []
    for Y, W in zip(Ys, Ws):
        mid = len(Y)//2
        cal.append(Half(Y, W, 0, mid, lags))
        test.append(Half(Y, W, mid, len(Y), lags))
    (mW, mW2), _ = pooled(cal, ["cW", "cW2"], None, None)
    s0, muW0 = mW2 - mW**2, mW
    sd = np.sqrt(s0)
    d = protocol["design"]
    # Selection windows are fixed from calibration point estimates, then held for every replicate.
    bins = {f"zero_{f}": (0, f*sd) for f in [d["primary_bin_fraction"]] + d["sensitivity_bin_fractions"]}
    fb = d["nonzero_conditioning_bin_fraction"]*sd
    bins.update({"plus_1sd": (1, fb), "minus_1sd": (-1, fb)})
    design = {}
    for name, (center, b) in bins.items():
        c = muW0 + center*sd
        design[name] = [selection_sums(h, c - b, c + b) for h in test]
    point = evaluate(cal, test, lags, design, bins=bins)

    def bootstrap(L, seed):
        rng = np.random.default_rng(seed)
        reps = [evaluate(cal, test, lags, design, rng=rng, L=L, bins=bins) for _ in range(unc["replicates"])]
        res = {}
        for name in bins:
            obs = np.array([r[name]["obs"] for r in reps])
            pred = np.array([r[name]["pred"] for r in reps])
            res[name] = {"se_obs": np.nanstd(obs, axis=0, ddof=1), "se_pred": np.nanstd(pred, axis=0, ddof=1)}
        return res

    boots = {L: bootstrap(L, unc["seed"] + L) for L in [unc["block_samples"]] + unc["block_sensitivity"]}
    primary = f"zero_{d['primary_bin_fraction']}"
    dec = protocol["decision"]

    def summarise(name, L):
        p, bt = point[name], boots[L][name]
        se = np.sqrt(bt["se_obs"]**2 + bt["se_pred"]**2)
        z = (p["obs"] - p["pred"])/se
        rel = (p["obs"] - p["pred"])/np.abs(p["pred"])
        return {"selected_starts": p["n"], "observed": p["obs"].tolist(), "predicted": p["pred"].tolist(),
                "combined_se": se.tolist(), "z": z.tolist(), "relative_error": rel.tolist(),
                "median_abs_relative_error": float(np.median(np.abs(rel))),
                "median_relative_se": float(np.median(se/np.abs(p["pred"]))), "max_abs_z": float(np.max(np.abs(z)))}

    tables = {L: {name: summarise(name, L) for name in bins} for L in boots}
    main = tables[unc["block_samples"]][primary]
    per_trace_min = min(selection_sums(h, muW0 - bins[primary][1], muW0 + bins[primary][1])["n"][-1] for h in test)
    if main["selected_starts"] < 200:
        verdict = "INCONCLUSIVE (too few selected starts)"
    elif main["median_relative_se"] > 0.25:
        verdict = "INCONCLUSIVE (insufficient precision)"
    elif main["max_abs_z"] <= 3 and main["median_abs_relative_error"] <= 0.15:
        verdict = "AGREE"
    else:
        verdict = "DISAGREE"

    loto = []
    if len(cal) > 2:
        for i in range(len(cal)):
            keep = [k for k in range(len(cal)) if k != i]
            sub = evaluate([cal[k] for k in keep], [test[k] for k in keep], lags,
                           {n: [design[n][k] for k in keep] for n in design}, bins={primary: bins[primary]})
            rel = (sub[primary]["obs"] - sub[primary]["pred"])/np.abs(sub[primary]["pred"])
            loto.append(float(np.median(np.abs(rel))))

    # Document, not assume, how the supplied velocity relates to position.
    Y, W = Ys[0], Ws[0]
    j = np.arange(4, min(len(Y) - 4, 200004))
    X = np.stack([Y[j + l] for l in range(-4, 5)], axis=1)
    coef, *_ = np.linalg.lstsq(X, W[j], rcond=None)
    fitted = X @ coef
    stencil_corr = float(np.dot(coef, STENCIL8)/np.linalg.norm(coef)/np.linalg.norm(STENCIL8))

    sel_idx = [l for l in (1, 8, 64) if l in lags]
    T = test[0]
    obs_primary = np.array(main["observed"])
    short = [i for i, l in enumerate(lags) if l <= 8]
    slope = float(np.polyfit(np.log(np.array(lags)[short]), np.log(np.abs(obs_primary[short])), 1)[0])
    quarters = [[float(np.var(w[q*len(w)//4:(q + 1)*len(w)//4])) for q in range(4)] for w in Ws]

    return {
        "label": label, "verdict": verdict, "traces": len(Ys), "samples_per_trace": [len(y) for y in Ys],
        "calibration_velocity_variance": float(s0), "primary_bin": primary, "primary": main,
        "min_selected_starts_single_trace_primary": float(per_trace_min),
        "block_sensitivity": {str(L): {"max_abs_z": tables[L][primary]["max_abs_z"],
                                       "median_relative_se": tables[L][primary]["median_relative_se"]} for L in tables},
        "all_bins": tables[unc["block_samples"]],
        "leave_one_trace_out_median_abs_relative_error": loto,
        "velocity_stencil_fit": {"coefficients_lag_-4_to_4": coef.tolist(), "cosine_with_8th_order_stencil": stencil_corr,
                                 "r2": float(1 - np.var(W[j] - fitted)/np.var(W[j]))},
        "diagnostics": {"excess_kurtosis_W_test_trace0": kurtosis(T.W),
                        "excess_kurtosis_D_test_trace0": {str(lags[i]): kurtosis(T.D[i]) for i in range(len(lags)) if lags[i] in sel_idx},
                        "velocity_variance_by_quarter": quarters,
                        "descriptive_loglog_slope_lags_1_8": slope},
    }


# ---------------------------------------------------------------- self-test data

def synthetic(protocol, modulated, seed):
    rng = np.random.default_rng(seed)
    gamma = 1/15
    K = gamma/44
    A = np.array([[0, 1], [-K, -gamma]])
    F = expm(A)
    S = np.diag([1/K, 1.0])
    Lq = cholesky(S - F @ S @ F.T, lower=True)
    ntr, n = 5, 200000
    state = rng.normal(size=(ntr, 2)) * np.sqrt(np.diag(S))
    x = np.empty((ntr, n))
    for t in range(n):
        x[:, t] = state[:, 0]
        state = state @ F.T + rng.normal(size=(ntr, 2)) @ Lq.T
    amp = 0.5*np.ones((ntr, n))
    if modulated:
        seg = 5000
        factors = np.exp(0.8*rng.normal(size=(ntr, n//seg + 1)))
        amp = 0.5*np.repeat(factors, seg, axis=1)[:, :n]
    y = x + amp*rng.normal(size=(ntr, n))
    w = np.stack([np.convolve(row, STENCIL8[::-1], mode="valid") for row in y])
    y = y[:, 4:-4]
    return list(y), list(w)


def to_jsonable(obj):
    if isinstance(obj, dict):
        return {k: to_jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [to_jsonable(v) for v in obj]
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, (np.floating, np.integer)):
        return obj.item()
    return obj


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--selftest", action="store_true")
    group.add_argument("--data", type=Path)
    args = parser.parse_args()
    protocol = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    meta = {"generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "protocol_sha256": sha256(PROTOCOL), "script_sha256": sha256(__file__),
            "numpy": np.__version__}
    runs = []
    if args.selftest:
        seed = protocol["selftest"]["seed"]
        for label, mod in (("selftest_positive", False), ("selftest_negative", True)):
            Ys, Ws = synthetic(protocol, mod, seed + int(mod))
            runs.append(analyse(Ys, Ws, protocol, label))
        out_dir = OUT / "selftest"
    else:
        digests = {}
        for name, expected in protocol["target"]["files_sha256"].items():
            path = args.data / name
            if not path.exists():
                raise GateFailure(f"missing {name}")
            digests[name] = sha256(path)
            if digests[name] != expected:
                raise GateFailure(f"{name}: digest mismatch")
        meta["data_sha256"] = digests
        for pair in protocol["target"]["pairs"]:
            Ys, ys = load_traces(args.data / pair["position"])
            Ws, ws = load_traces(args.data / pair["velocity"])
            result = analyse(Ys, Ws, protocol, pair["role"])
            result["schema"] = {"position": ys, "velocity": ws}
            runs.append(result)
        out_dir = OUT / "dryad_v3"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "results.json").write_text(json.dumps(to_jsonable({"meta": meta, "runs": runs}), indent=2), encoding="utf-8")
    for r in runs:
        p = r["primary"]
        print(f"{r['label']:>20}: {r['verdict']:<40} max|z|={p['max_abs_z']:.2f} "
              f"median|rel err|={p['median_abs_relative_error']:.3f} median rel SE={p['median_relative_se']:.3f} "
              f"selected={p['selected_starts']:.0f}")
    print(f"wrote {out_dir / 'results.json'}")


if __name__ == "__main__":
    main()
