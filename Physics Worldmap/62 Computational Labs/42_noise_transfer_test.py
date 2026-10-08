"""Stage-4 post hoc test: does two-component noise transfer explain lab 35's residual? No novelty claim.

Frozen 2026-10-08 after labs 35 and 40 (lab 40 D4: one noise scale alpha = 0.61 leaves
chi2 1730/12). Motivation: empty-trap increment variances jump from lag 1 to lag 2 and then
grow slowly, so the bin-level noise is not white; a short-range part (shot/electronic) and a
long-range part (pointing/drift) may change differently when a particle scatters light.

Model: empty-trap bin autocovariance gamma(n) is measured directly (all six traces, centred).
  gamma_long(n): quadratic in n fitted over 4 <= |n| <= 12 and extended to |n| <= 3;
                 equal to gamma(n) for |n| > 3.
  gamma_short(n) = gamma(n) - gamma_long(n), nonzero only for |n| <= 3.
  Particle-run noise covariance = a_s gamma_short + a_l gamma_long; its r_k and s follow from
  the eighth-order stencil exactly as for the particle operator.
  Observable R_k(a_s, a_l) = (r_p - r_noise)/(s_p - s_noise), lab 35's 16 lags.
  Check before fitting: gamma-based (a_s = a_l = 1) R reproduces lab 35's subtracted R to 2e-3 relative.
Fits (GLS, lab 35 bootstrap covariance at a_s = a_l = 1: block 2000, 400 replicates, seed 2026100611):
  N2: published Basset (no physical parameter free) with (a_s, a_l) free.
  N5: B3 (g, a, k free) with (a_s, a_l) free.
Decision (fixed): noise transfer ACCOUNTS for the residual if N2 has SE-corrected chi2/dof
  (chi2/1.44/14) < 2 with both scales in [0.5, 2]; PARTIAL if N2 improves on lab 35's E chi2
  (3906) by more than half; otherwise NOT EXPLAINED. N5 is reported, not decisive.

Amendment 2026-10-08, before any fit: the first run stopped at the decomposition check
(max rel diff 0.019 > 2e-3; no fits run). Cause: autocovariances with lag-dependent
normalisation do not cancel the large slow-drift variance exactly in the stencil sums.
Replaced gamma(n) by half increment variances V(n) = E[(Y_{j+n} - Y_j)^2]/2 (gamma(n) =
gamma(0) - V(n); the constant drops out because the stencil sums to zero). The short/long
split, check, fits and decision are otherwise unchanged; the split is applied to V.

    python 42_noise_transfer_test.py --data <dir with Dryad files>
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
OUT = HERE / "results" / "noise_transfer"
spec = importlib.util.spec_from_file_location("lab35", HERE / "35_gain_free_hydrodynamic_memory.py")
lab35 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lab35)
lab34 = lab35.lab34
S8 = lab34.STENCIL8
N0 = 3


def half_increment_var(traces, nmax):
    """V(n) = E[(Y_{j+n} - Y_j)^2]/2, pooled over traces with increments centred."""
    num = np.zeros(nmax + 1)
    cnt = np.zeros(nmax + 1)
    for n in range(1, nmax + 1):
        d = np.concatenate([np.asarray(y, float)[n:] - np.asarray(y, float)[:-n] for y in traces])
        num[n] = np.sum((d - d.mean())**2)/2
        cnt[n] = len(d)
    cnt[0] = 1
    return num/cnt


def split(gamma):
    n = np.arange(len(gamma))
    fit = (n >= N0 + 1) & (n <= 12)
    coef = np.polyfit(n[fit], gamma[fit], 2)
    long = gamma.copy()
    long[: N0 + 1] = np.polyval(coef, n[: N0 + 1])
    return gamma - long, long


def stencil_moments(V, lags, dt):
    g = lambda n: -V[abs(n)]          # gamma(n) up to a constant that the zero-sum stencil removes
    ls = range(-4, 5)
    s = sum(S8[a + 4]*S8[b + 4]*g(a - b) for a in ls for b in ls)/dt**2
    r = np.array([sum(S8[a + 4]*g(k - a) for a in ls)/dt for k in lags])
    return r, s


def gls(pred, R, Ci):
    d = R - pred
    return float(d @ Ci @ d)


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
    rp, sp = lab35.moments(halves)
    R35 = lab35.estimate_R(halves, empty)

    gamma = half_increment_var(En, max(lags) + 8)   # V(n); name kept for the split helper
    gs, gl = split(gamma)
    rs, ss = stencil_moments(gs, lags, dt)
    rl, sl = stencil_moments(gl, lags, dt)
    R11 = (rp - rs - rl)/(sp - ss - sl)
    check = float(np.max(np.abs(R11/R35 - 1)))
    print("gamma-based vs lab 35 subtracted R, max rel diff:", check, flush=True)
    if check > 2e-3:
        raise RuntimeError("noise decomposition does not reproduce lab 35's subtraction; no fits run")

    rng = np.random.default_rng(2026100611)
    reps = np.array([lab35.estimate_R(halves, empty, rng, 2000) for _ in range(400)])
    Ci = np.linalg.inv(np.cov(reps.T))
    Rof = lambda a_s, a_l: (rp - a_s*rs - a_l*rl)/(sp - a_s*ss - a_l*sl)
    g0, a0, k0 = lab35.physical_to_scaled(lab35.PUB["r"], lab35.PUB["K"])
    RE = lab35.operator_R(lab35.Kernel(g0, a0, k0), lags, dt)

    def safe(f):
        def h(p):
            try:
                v = f(p)
            except (ValueError, FloatingPointError, np.linalg.LinAlgError):
                return 1e30
            return v if np.isfinite(v) else 1e30
        return h

    opts = {"xatol": 1e-8, "fatol": 1e-8, "maxiter": 8000, "maxfev": 16000}
    best2 = None
    for start in ([1, 1], [0.6, 1], [1, 0.6], [1.5, 0.5], [0.5, 1.5]):
        res = minimize(safe(lambda p: gls(RE, Rof(*p), Ci)), start, method="Nelder-Mead", options=opts)
        if best2 is None or res.fun < best2.fun:
            best2 = res
    a_s, a_l = best2.x
    c2 = float(best2.fun)
    dof2 = len(lags) - 2
    res5 = minimize(safe(lambda p: gls(lab35.operator_R(lab35.Kernel(*np.exp(p[:3])), lags, dt), Rof(p[3], p[4]), Ci)),
                    [np.log(g0), np.log(a0), np.log(k0), a_s, a_l], method="Nelder-Mead", options=opts)
    Rfit = Rof(a_s, a_l)
    E1 = gls(RE, R35, Ci)
    if c2/1.44/dof2 < 2 and 0.5 <= a_s <= 2 and 0.5 <= a_l <= 2:
        verdict = "ACCOUNTS"
    elif c2 < E1/2:
        verdict = "PARTIAL"
    else:
        verdict = "NOT EXPLAINED"
    out = {"meta": {"generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                    "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                    "status": "stage-4 post hoc; frozen before running"},
           "decomposition_check_max_rel": check,
           "empty_trap_half_increment_var_0_to_8": gamma[:9].tolist(), "V_short_0_to_3": gs[:4].tolist(),
           "E_chi2_lab35_subtraction": E1,
           "N2": {"a_short": float(a_s), "a_long": float(a_l), "chi2": c2, "dof": dof2, "p": float(chi2_dist.sf(c2, dof2)),
                  "chi2_per_dof_se_corrected": c2/1.44/dof2,
                  "data_over_E_minus_1": (Rfit/RE - 1).tolist()},
           "N5": {"g_a_k": np.exp(res5.x[:3]).tolist(), "a_short": float(res5.x[3]), "a_long": float(res5.x[4]),
                  "chi2": float(res5.fun), "dof": len(lags) - 5},
           "verdict": verdict}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "results.json").write_text(json.dumps(lab34.to_jsonable(out), indent=2), encoding="utf-8")
    print(json.dumps({k: out[k] for k in ("E_chi2_lab35_subtraction", "N2", "N5", "verdict")}, indent=1))


if __name__ == "__main__":
    main()
