"""Which preparation does each conditional-mean formula describe? Time-domain check; no novelty claim.

For the trapped Basset-Boussinesq sphere, with m including half the displaced fluid mass and units
m = kT = 1,

    x'' + a D^{1/2} x' + g x' + k x = 0,  t > 0,  x(0) = 0, x'(0+) = v0.

The half-derivative's lower limit carries the preparation:
  * impulsive start from rest (fluid quiescent at 0-, velocity jump included): Riemann-Liouville
    D^{1/2} of v on [0, t].  Laplace: X = v0/P(s), i.e. x = v0 * m chi(t).  This equals the
    stationary-equilibrium conditional mean E[X(t) - X(0) | V(0) = v0] by Gaussian regression
    and the classical FDT (Cov(X(t), V(0)) = kT chi(t), Var V = kT/m).
  * steady prior motion (v = v0 for all t < 0, fully developed flow): Caputo D^{1/2} of v, i.e.
    the history integral only over 0 < tau < t.  Laplace: X = v0 (1 + a s^{-1/2})/P(s), i.e.
    x = v0 * (m chi + a m psi), lab 35's model V and the authors' commented-out term.

This script integrates both with a Grunwald-Letnikov implicit scheme, independent of lab 35's
partial-fraction formulas, and compares at lab 35's lags. Two step sizes give an empirical order.

    python 39_conditional_mean_preparations.py
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
OUT = HERE / "results" / "conditional_mean_preparations"
spec = importlib.util.spec_from_file_location("lab35", HERE / "35_gain_free_hydrodynamic_memory.py")
lab35 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lab35)

LAGS = [1, 2, 3, 4, 6, 8, 11, 16, 23, 32, 45, 64, 90, 128, 181, 256]
DT = 7.5e-7


def gl_weights(n, alpha=0.5):
    w = np.empty(n + 1)
    w[0] = 1.0
    for j in range(1, n + 1):
        w[j] = w[j - 1]*(1 - (alpha + 1)/j)
    return w


def integrate(g, a, k, h, t_end, caputo):
    """Implicit Euler in v with GL half-derivative of the smooth part v - v0; x by the trapezoid rule. v0 = 1.

    Both preparations use GL only on v - v0 (no jump). The impulsive start adds the jump's exact
    Riemann-Liouville contribution v0/sqrt(pi t) as a force, averaged exactly over each step.
    """
    n = int(round(t_end/h))
    w = gl_weights(n)
    c = a*h**-0.5
    v = np.empty(n + 1)
    x = np.empty(n + 1)
    v[0], x[0] = 1.0, 0.0
    shift = 1.0                              # GL acts on v - v0 in both cases
    f = np.empty(n + 1)                      # f = v - shift
    f[0] = v[0] - shift
    for i in range(1, n + 1):
        hist = np.dot(w[1:i + 1], f[i - 1::-1])
        # (v_i - v_{i-1})/h = -c (w0 (v_i - shift) + hist) - g v_i - k (x_{i-1} + h (v_{i-1} + v_i)/2)
        jump = 0.0 if caputo else a*2/np.sqrt(np.pi)*(np.sqrt(i*h) - np.sqrt((i - 1)*h))/h
        lhs = 1/h + c*w[0] + g + k*h/2
        rhs = v[i - 1]/h - c*(hist - w[0]*shift) - jump - k*(x[i - 1] + h*v[i - 1]/2)
        v[i] = rhs/lhs
        f[i] = v[i] - shift
        x[i] = x[i - 1] + h*(v[i - 1] + v[i])/2
    return np.arange(n + 1)*h, x


def main():
    g, a, k = lab35.physical_to_scaled(lab35.PUB["r"], lab35.PUB["K"])
    ker = lab35.Kernel(g, a, k)
    t = np.array(LAGS)*DT
    closed = {"impulsive_from_rest": ker.mchi(t), "steady_prior_motion": ker.mchi(t) + a*ker.mpsi(t)}
    res = {}
    for name, caputo in (("impulsive_from_rest", False), ("steady_prior_motion", True)):
        errs = {}
        for h in (DT/40, DT/80):
            tt, x = integrate(g, a, k, h, t[-1], caputo)
            idx = np.rint(t/h).astype(int)
            errs[h] = x[idx]/closed[name] - 1
        h1, h2 = sorted(errs, reverse=True)
        order = np.log2(np.abs(errs[h1])/np.maximum(np.abs(errs[h2]), 1e-300))
        res[name] = {"closed_form_over_t": (closed[name]/t).tolist(),
                     "relative_error_h_dt_over_40": errs[h1].tolist(), "relative_error_h_dt_over_80": errs[h2].tolist(),
                     "empirical_order": order.tolist(),
                     "max_abs_relative_error_finest": float(np.max(np.abs(errs[h2])))}
        print(f"{name:>22}: max |rel err| {np.max(np.abs(errs[h1])):.2e} (h=dt/40), {np.max(np.abs(errs[h2])):.2e} (h=dt/80)")
    sep = closed["steady_prior_motion"]/closed["impulsive_from_rest"] - 1
    res["V_over_E_minus_1_continuum"] = sep.tolist()
    print("V/E - 1 at lab 35 lags:", np.round(sep, 3))
    out = {"meta": {"generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                    "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                    "parameters_scaled": {"gamma_over_m": g, "z_over_m": a, "K_over_m": k}, "lags": LAGS, "dt": DT},
           "results": res}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "results.json").write_text(json.dumps(out, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
