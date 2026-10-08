"""Stage-3 diagnostics of lab 35's Basset misfit; post hoc, exploratory, no novelty claim.

Frozen 2026-10-08 after lab 35's first real-data run printed only its main-fit chi2
values (B2 3610, B3 2748, L 9093 on 16 lags) and BEFORE any lag-resolved residual,
fitted parameter, or plot from the real data was seen. The diagnostic list below is
fixed in advance to limit forking paths; every result is reported, none is selected.

Observable and uncertainty are lab 35's: noise-subtracted R_k = Cov(D_k,W)/Var(W) in
seconds, moving-block bootstrap (block 2000, 400 replicates, seed 2026100611), GLS chi2.

  D1 lag localisation: B3 on lags <= 16 (12 us) and on lags >= 16, separately.
  D2 memory exponent:  P(s) = s^2 + a s^beta + g s + k with beta free (Basset: 3/2).
  D3 detector bandwidth: B3 with a single-pole low-pass on the position signal, corner free.
  D4 noise scale: R(alpha) = (r_p - alpha r_e)/(s_p - alpha s_e), alpha free with B3.
  D5 per trace: B3 fitted to each of the six traces (per-trace bootstrap, 200 replicates);
     heterogeneity chi2 of the three parameters about their inverse-variance mean.

Reporting rule (fixed): an extension "accounts for" the misfit only if its SE-corrected
chi2/dof (chi2/1.44/dof) is below 2; Delta chi2 against B3 is reported for every one.
D2-D4 use a frequency-domain operator, validated against lab 35's time-domain operator
at beta = 3/2 before any fit.

    python 40_basset_misfit_diagnostics.py --data <dir with Dryad files>
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from scipy.optimize import minimize
from scipy.stats import chi2 as chi2_dist

HERE = Path(__file__).resolve().parent
OUT = HERE / "results" / "basset_misfit_diagnostics"
spec = importlib.util.spec_from_file_location("lab35", HERE / "35_gain_free_hydrodynamic_memory.py")
lab35 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lab35)
lab34 = lab35.lab34
S8 = lab34.STENCIL8

# frequency grid (rad/s): fine logarithmic core plus a uniform oscillation-resolving band
_W = np.unique(np.concatenate([np.logspace(-1, 4, 20000), np.arange(1e4, 2e6, 25.0), np.arange(2e6, 3e8, 400.0)]))


def chi_scaled(w, a, beta, g, k):
    s = -1j*w
    return 1/(s*s + a*s**beta + g*s + k)


def operator_R_freq(lags, dt, a, beta, g, k, wc=None):
    """R_k = r_k/s from S_x = 2 Im chi / w, box-averaged bins, eighth-order stencil (kT = m = 1)."""
    w = _W
    Sx = 2*np.imag(chi_scaled(w, a, beta, g, k))/w
    B2 = np.sinc(w*dt/(2*np.pi))**2
    if wc is not None:
        B2 = B2/(1 + (w/wc)**2)
    Q = 2*sum(S8[4 + l]*np.sin(w*l*dt) for l in range(1, 5))
    base = Sx*B2*Q/dt
    s = np.trapezoid(base*Q/dt, w)/np.pi
    r = np.array([np.trapezoid(base*np.sin(w*kk*dt), w)/np.pi for kk in lags])
    return r/s


def gls(pred, R, Cinv):
    d = R - pred
    return float(d @ Cinv @ d)


def nm(obj, x0):
    res = minimize(obj, x0, method="Nelder-Mead", options={"xatol": 1e-7, "fatol": 1e-7, "maxiter": 6000, "maxfev": 12000})
    return res.x, float(res.fun)


def safe(f):
    def g(p):
        try:
            v = f(p)
        except (ValueError, FloatingPointError, np.linalg.LinAlgError):
            return 1e30
        return v if np.isfinite(v) else 1e30
    return g


def moments_split(halves, rng=None, L=None):
    return lab35.moments(halves, rng, L)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--data", type=Path, required=True)
    args = ap.parse_args()
    P = json.loads(lab35.PROTOCOL.read_text(encoding="utf-8"))
    P34 = json.loads(lab34.PROTOCOL.read_text(encoding="utf-8"))
    for name, expected in P34["target"]["files_sha256"].items():
        if lab35.sha256(args.data / name) != expected:
            raise lab34.GateFailure(f"{name}: digest mismatch")
    lags = P["observable"]["lags_samples"]
    dt = P["observable"]["sample_time_s"]
    Ys, _ = lab34.load_traces(args.data / "barium_titanate_in_acetone_position.csv")
    Ws, _ = lab34.load_traces(args.data / "barium_titanate_in_acetone_velocity.csv")
    En, _ = lab34.load_traces(args.data / "noise_position.csv")
    Wn, _ = lab34.load_traces(args.data / "noise_velocity.csv")
    halves, empty = lab35.gather(Ys, Ws, lags), lab35.gather(En, Wn, lags)

    g0, a0, k0 = lab35.physical_to_scaled(lab35.PUB["r"], lab35.PUB["K"])
    # validate the frequency-domain operator against lab 35's time-domain operator
    val = {}
    for name, (a, g, k) in {"published": (a0, g0, k0), "langevin": (0.0, g0, k0), "stiff": (a0, g0, 4*k0)}.items():
        tf = operator_R_freq(lags, dt, a, 1.5, g, k)
        tt = lab35.operator_R(lab35.Kernel(g, a, k), lags, dt)
        val[name] = float(np.max(np.abs(tf/tt - 1)))
    print("frequency vs time operator, max rel diff:", val, flush=True)
    if max(val.values()) > 1e-4:
        raise RuntimeError("frequency-domain operator failed validation; no fits run")

    R = lab35.estimate_R(halves, empty)
    rng = np.random.default_rng(2026100611)
    reps = np.array([lab35.estimate_R(halves, empty, rng, 2000) for _ in range(400)])
    cov = np.cov(reps.T)
    Cinv = np.linalg.inv(cov)
    n = len(lags)
    out = {"validation_max_rel_diff": val}

    def b3_fit(Rv, Ci, idx=slice(None), start=(g0, a0, k0)):
        lg = list(np.array(lags)[idx])
        f = safe(lambda p: gls(lab35.operator_R(lab35.Kernel(*np.exp(p)), lg, dt), Rv, Ci))
        x, c2 = nm(f, np.log(start))
        return np.exp(x), c2

    pB3, c2B3 = b3_fit(R, Cinv)
    out["B3"] = {"params_g_a_k": pB3.tolist(), "chi2": c2B3, "dof": n - 3}
    print("B3", pB3, c2B3, flush=True)

    # D1 lag localisation
    d1 = {}
    for label, sel in (("lags_le_16", np.array(lags) <= 16), ("lags_ge_16", np.array(lags) >= 16)):
        idx = np.where(sel)[0]
        Ci = np.linalg.inv(cov[np.ix_(idx, idx)])
        p, c2 = b3_fit(R[idx], Ci, idx, pB3)
        d1[label] = {"params_g_a_k": p.tolist(), "chi2": c2, "dof": len(idx) - 3,
                     "chi2_per_dof_se_corrected": c2/1.44/(len(idx) - 3)}
    out["D1_lag_localisation"] = d1
    print("D1", d1, flush=True)

    # D2 memory exponent
    f2 = safe(lambda p: gls(operator_R_freq(lags, dt, np.exp(p[0]), p[1], np.exp(p[2]), np.exp(p[3])), R, Cinv))
    x2, c22 = nm(f2, [np.log(pB3[1]), 1.5, np.log(pB3[0]), np.log(pB3[2])])
    out["D2_memory_exponent"] = {"a": float(np.exp(x2[0])), "beta": float(x2[1]), "g": float(np.exp(x2[2])),
                                 "k": float(np.exp(x2[3])), "chi2": c22, "dof": n - 4, "delta_chi2_vs_B3": c2B3 - c22}
    print("D2", out["D2_memory_exponent"], flush=True)

    # D3 detector bandwidth
    f3 = safe(lambda p: gls(operator_R_freq(lags, dt, np.exp(p[1]), 1.5, np.exp(p[0]), np.exp(p[2]), np.exp(p[3])), R, Cinv))
    best3 = None
    for wc0 in (2*np.pi*5e6, 2*np.pi*1e6, 2*np.pi*3e5):
        x3, c23 = nm(f3, [np.log(pB3[0]), np.log(pB3[1]), np.log(pB3[2]), np.log(wc0)])
        if best3 is None or c23 < best3[1]:
            best3 = (x3, c23)
    x3, c23 = best3
    out["D3_detector_lowpass"] = {"g": float(np.exp(x3[0])), "a": float(np.exp(x3[1])), "k": float(np.exp(x3[2])),
                                  "corner_hz": float(np.exp(x3[3])/(2*np.pi)), "chi2": c23, "dof": n - 4,
                                  "delta_chi2_vs_B3": c2B3 - c23}
    print("D3", out["D3_detector_lowpass"], flush=True)

    # D4 noise scale
    rp, sp = lab35.moments(halves)
    re, se_ = lab35.moments(empty)
    f4 = safe(lambda p: gls(lab35.operator_R(lab35.Kernel(*np.exp(p[:3])), lags, dt), (rp - p[3]*re)/(sp - p[3]*se_), Cinv))
    x4, c24 = nm(f4, list(np.log(pB3)) + [1.0])
    out["D4_noise_scale"] = {"params_g_a_k": np.exp(x4[:3]).tolist(), "alpha": float(x4[3]), "chi2": c24, "dof": n - 4,
                             "delta_chi2_vs_B3": c2B3 - c24}
    print("D4", out["D4_noise_scale"], flush=True)

    # D5 per trace
    per = []
    for i in range(len(halves)):
        Ri = lab35.estimate_R([halves[i]], empty)
        rr = np.random.default_rng(2026100650 + i)
        repi = np.array([lab35.estimate_R([halves[i]], empty, rr, 2000) for _ in range(200)])
        covi = np.cov(repi.T)
        pi, c2i = b3_fit(Ri, np.linalg.inv(covi), start=pB3)
        boot = []
        for j in range(20):
            pj, _ = b3_fit(repi[j], np.linalg.inv(covi), start=pi)
            boot.append(np.log(pj))
        per.append({"trace": i + 1, "params_g_a_k": pi.tolist(), "chi2": c2i, "dof": n - 3,
                    "log_param_sd_20_refits": np.std(boot, axis=0, ddof=1).tolist(), "R_s": Ri.tolist()})
        print("D5 trace", i + 1, pi, round(c2i, 1), flush=True)
    lp = np.log([p["params_g_a_k"] for p in per])
    sd = np.array([p["log_param_sd_20_refits"] for p in per])
    wts = 1/sd**2
    mean = (wts*lp).sum(0)/wts.sum(0)
    het = ((lp - mean)**2*wts).sum(0)
    out["D5_per_trace"] = {"traces": per, "heterogeneity_chi2_log_g_a_k": het.tolist(), "dof_each": len(per) - 1,
                           "p_each": [float(chi2_dist.sf(h, len(per) - 1)) for h in het]}
    print("D5 heterogeneity", het, flush=True)

    for key in ("D2_memory_exponent", "D3_detector_lowpass", "D4_noise_scale"):
        e = out[key]
        e["accounts_for_misfit"] = bool(e["chi2"]/1.44/e["dof"] < 2)
    out["meta"] = {"generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                   "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                   "status": "stage-3 post hoc diagnostics; list frozen before lab 35 residuals were seen"}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "results.json").write_text(json.dumps(lab34.to_jsonable(out), indent=2), encoding="utf-8")
    print("wrote", OUT / "results.json")


if __name__ == "__main__":
    main()
