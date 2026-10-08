"""General theory: conditioning on an estimated velocity distorts the short-time exponent; no novelty claim.

For a stationary Gaussian process with velocity covariance C_v(tau) = c - a|tau|^alpha + ...,
measured as bin averages Y_n (width Delta) with velocity W = sum_l d_l Y_{n+l}/Delta from a
central stencil d (sum d = 0, sum l d_l = 1), the zero-velocity conditioned MSD of D_k = Y_k - Y_0
is, to first order in a and with independent white position noise sigma^2,

    M_k = a Delta^{alpha+2} Phi_alpha(k)  +  2 sigma^2  +  [eps/(1+eps)] c (k Delta)^2  + ...

* Phi_alpha(k) = Var(Y_k - Y_0 - k sum_l d_l Y_l) under the generalised position covariance
  gamma(tau) = |tau|^{alpha+2}/((alpha+1)(alpha+2)), bin-averaged. The weights annihilate
  constant and linear motion, so the ballistic c-term cancels exactly. Continuum limit:
  Phi -> 2 k^{alpha+2}/(alpha+2).
* eps = sigma_W^2 / Var_signal(W): noise in W attenuates the regression slope, so a fraction
  eps/(1+eps) of the ballistic term leaks back (exact for k beyond the stencil reach).

Checks: (1) Phi -> continuum at large k; (2) first-order prediction vs the full published
Basset operator (lab 41 theory_moments, noise-free) at short lags; (3) the noise-leak formula
vs the exact Gaussian expression with white noise. Output: universal suppression factors,
local apparent exponents, and the minimum lag k_min(alpha, stencil) at which the operator
alone keeps the exponent within 0.05 and 0.1 of alpha+2.

    python 46_estimated_velocity_conditioning_theory.py
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
OUT = HERE / "results" / "estimated_velocity_theory"
spec = importlib.util.spec_from_file_location("lab41", HERE / "41_processing_dependence_test.py")
lab41 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lab41)
lab35 = lab41.lab35
STENCILS = lab41.STENCILS
_X, _WQ = np.polynomial.legendre.leggauss(64)


def gamma_bin(n, alpha):
    """Bin-averaged generalised covariance (Delta = 1): integral of triangle(u) gamma(n + u), u in [-1, 1]."""
    u = 0.5*(_X + 1)               # [0, 1]
    w = 0.5*_WQ*(1 - u)
    g = lambda t: np.abs(t)**(alpha + 2)/((alpha + 1)*(alpha + 2))
    return float(np.sum(w*(g(n + u) + g(n - u))))


def phi(alpha, order, k):
    d = STENCILS[order]
    h = len(d)//2
    w = {}
    w[k] = w.get(k, 0) + 1.0
    w[0] = w.get(0, 0) - 1.0
    for i, l in enumerate(range(-h, h + 1)):
        w[l] = w.get(l, 0) - k*d[i]
    keys = list(w)
    return float(sum(w[i]*w[j]*gamma_bin(i - j, alpha) for i in keys for j in keys))


def phi_cont(alpha, k):
    return 2*k**(alpha + 2)/(alpha + 2)


def main():
    alphas = [0.25, 0.5, 0.75, 1.0]
    ks = np.unique(np.round(np.logspace(0, np.log10(256), 40)).astype(int))
    table = {}
    for a in alphas:
        for o in STENCILS:
            p = np.array([phi(a, o, int(k)) for k in ks])
            ratio = p/phi_cont(a, ks)
            slope = np.gradient(np.log(p), np.log(ks))
            kmin = {}
            for tol in (0.05, 0.1):
                ok = np.abs(slope - (a + 2)) <= tol
                bad = np.where(~ok)[0]
                kmin[str(tol)] = int(ks[bad[-1] + 1]) if len(bad) and bad[-1] + 1 < len(ks) else (int(ks[0]) if not len(bad) else None)
            table[f"alpha={a},order={o}"] = {"k": ks.tolist(), "suppression_vs_continuum": ratio.tolist(),
                                             "local_exponent": slope.tolist(), "k_min": kmin}
            print(f"alpha={a:4} order={o}: suppression k=1 {ratio[0]:.3f}, k=4 {ratio[np.searchsorted(ks, 4)]:.3f}, "
                  f"k=16 {ratio[np.searchsorted(ks, 16)]:.3f}; local exponent k=1 {slope[0]:.2f}; "
                  f"k_min(0.05)={kmin['0.05']} k_min(0.1)={kmin['0.1']}", flush=True)

    # check 1: continuum limit
    big = phi(0.5, 8, 2000)/phi_cont(0.5, 2000)
    # check 2: first-order formula vs full published Basset operator (noise-free), alpha = 1/2
    g0, a0, k0 = lab35.physical_to_scaled(lab35.PUB["r"], lab35.PUB["K"])
    a_cusp = 2*a0/np.sqrt(np.pi)                # C_v = 1 - (2 z/(m sqrt(pi))) t^{1/2} + ... (kT = m = 1)
    dt = lab41.DT
    lags = [1, 2, 3, 4, 6, 8, 11, 16, 23, 32]
    u, r, s = lab41.theory_moments(8, 1, lags)
    r_ = lab35.PUB["r"]
    mass = 4/3*np.pi*r_**3*lab35.PUB["rho_p"] + 2/3*np.pi*r_**3*lab35.PUB["rho_f"]
    kTm = lab35.KB*lab35.PUB["T"]/mass
    full = (u - r**2/s)/kTm
    first = np.array([a_cusp*dt**2.5*phi(0.5, 8, k) for k in lags])
    check2 = (first/full - 1).tolist()
    # check 3: noise leak formula vs exact Gaussian (white position noise), k beyond stencil reach
    sig2 = 0.01*kTm*dt**2               # arbitrary white-noise level in m^2
    sW = sig2*np.sum(STENCILS[8]**2)/dt**2
    eps = sW/s
    exact_add = 2*sig2 + r**2/s - r**2/(s + sW)
    formula_add = 2*sig2 + eps/(1 + eps)*r**2/s            # exact identity for k beyond the stencil reach
    ballistic_add = 2*sig2 + eps/(1 + eps)*kTm*(np.array(lags)*dt)**2   # leading-order (r ~ c t) form
    sel = np.array(lags) > 4
    check3 = (formula_add[sel]/exact_add[sel] - 1).tolist()
    ballistic_err = (ballistic_add/exact_add - 1).tolist()
    print("check 1 continuum limit ratio at k=2000:", round(big, 4))
    print("check 2 first-order/full Basset - 1:", np.round(check2, 3))
    print("check 3 noise-leak formula/exact - 1 (k>4):", np.round(check3, 6))
    print("ballistic c t^2 approximation error:", np.round(ballistic_err, 3))

    # experiment-specific blend for the Dryad case (published parameters, measured eps ~ 0.06)
    eps_data = 0.0604
    ks2 = np.array(lags)
    leak = eps_data/(1 + eps_data)*(r**2/s)/kTm           # in units of c = kT/m
    cusp = full
    out = {"meta": {"generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                    "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
           "table": table, "check_continuum_k2000": big, "check_first_order_vs_full_basset": check2,
           "check_noise_leak_formula": check3, "ballistic_leak_approx_error_all_lags": ballistic_err,
           "dryad_case_leak_over_cusp": (leak/cusp).tolist(), "dryad_lags": lags,
           "a_cusp_scaled": a_cusp}
    print("Dryad case: velocity-noise ballistic leak / operator cusp term:", np.round(leak/cusp, 2))
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "results.json").write_text(json.dumps(out, indent=2), encoding="utf-8")

    fig, ax = plt.subplots(1, 2, figsize=(10, 4))
    for a, ls in zip((0.5, 1.0), ("-", "--")):
        for o, col in zip((2, 4, 8), ("C2", "C1", "C0")):
            e = table[f"alpha={a},order={o}"]
            ax[0].semilogx(e["k"], e["suppression_vs_continuum"], ls, color=col, label=f"α={a}, order {o}")
            ax[1].semilogx(e["k"], e["local_exponent"], ls, color=col, label=f"α={a}, order {o}")
        ax[1].axhline(a + 2, color="k", lw=0.6, ls=ls)
    ax[0].set_xlabel("lag after selection (bins)"); ax[0].set_ylabel("measured ÷ continuum (cusp term)")
    ax[1].set_xlabel("lag after selection (bins)"); ax[1].set_ylabel("apparent local exponent")
    ax[0].legend(fontsize=7); ax[0].set_title("Operator suppression is universal in k", fontsize=9)
    ax[1].set_title("Apparent exponent overshoots α+2 at short lags", fontsize=9)
    fig.tight_layout(); fig.savefig(OUT / "universal_operator_curves.png", dpi=150)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
