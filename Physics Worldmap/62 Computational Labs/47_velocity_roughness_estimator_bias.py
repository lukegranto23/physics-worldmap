"""Is the apparent velocity roughness exponent H_v processing-dependent? Theory + data; no novelty claim.

Context: 2026 preprints (arXiv:2605.16252, 2605.16247) discuss a velocity fractal dimension
d_v = 2 - H_v = 7/4 (H_v = 1/4) for Brownian motion with fluid inertia, from velocity increments.
With C_v(tau) = c - a|tau|^alpha, the true increment variance is Var(v(t) - v(0)) = 2a t^alpha,
so 2 H_v = alpha (= 1/2 for Basset memory).

Measured velocities are stencils on bin averages: W_n = sum_l d_l Y_{n+l}/Delta. To first order in a,
    Var(W_k - W_0) = a Delta^alpha Psi_alpha(k),
with Psi computed from the bin-averaged generalised covariance |tau|^{alpha+2}/((alpha+1)(alpha+2))
and weights d_{l-k} - d_l (which annihilate constant and linear motion). Psi -> 2 k^alpha in the
continuum. Its local log-slope is the APPARENT 2 H_v.

Theory part: Psi_alpha(k) and apparent H_v for alpha in {1/4, 1/2, 3/4, 1}, stencils 2/4/8,
and the full published-Basset operator (noise-free) for the Dryad geometry.
Data part (descriptive, if --data is given): noise-subtracted increment variance of W recomputed
from the supplied positions for stencils 2/4/8 at 750 ns, Var_p - Var_e, local slopes vs lag,
compared with the forward model. No decision rule; post hoc description.

    python 47_velocity_roughness_estimator_bias.py [--data <dir with Dryad files>]
"""
from __future__ import annotations

import argparse
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
OUT = HERE / "results" / "velocity_roughness"
spec = importlib.util.spec_from_file_location("lab46", HERE / "46_estimated_velocity_conditioning_theory.py")
lab46 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lab46)
lab41, lab35 = lab46.lab41, lab46.lab35
lab34 = lab35.lab34
STENCILS = lab41.STENCILS
DT = lab41.DT


def psi(alpha, order, k):
    d = STENCILS[order]
    h = len(d)//2
    w = {}
    for i, l in enumerate(range(-h, h + 1)):
        w[l + k] = w.get(l + k, 0) + d[i]
        w[l] = w.get(l, 0) - d[i]
    keys = list(w)
    return float(sum(w[i]*w[j]*lab46.gamma_bin(i - j, alpha) for i in keys for j in keys))


def basset_W_increment_var(order, lags):
    """Noise-free Var(W_k - W_0)/(kT/m) for published Basset through the order-`order` stencil at 750 ns."""
    g0, a0, k0 = lab35.physical_to_scaled(lab35.PUB["r"], lab35.PUB["K"])
    ker = lab35.Kernel(g0, a0, k0)
    x, wq = np.polynomial.legendre.leggauss(24)
    u = 0.5*DT*(x + 1)
    wu = 0.5*DT*wq*(1 - u/DT)/DT
    Cx = lambda tt: -ker.int_mchi_minus_limit(np.abs(tt))
    G = lambda n: (Cx(n*DT + u) + Cx(n*DT - u)) @ wu
    d = STENCILS[order]
    h = len(d)//2
    ls = range(-h, h + 1)
    covW = lambda k: sum(d[i]*d[j]*G(k + li - lj) for i, li in enumerate(ls) for j, lj in enumerate(ls))/DT**2
    s = covW(0)
    return np.array([2*(s - covW(k)) for k in lags])


def slopes(k, y):
    return np.gradient(np.log(y), np.log(k))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--data", type=Path)
    args = ap.parse_args()
    ks = np.unique(np.round(np.logspace(0, np.log10(256), 32)).astype(int))
    theory = {}
    for a in (0.25, 0.5, 0.75, 1.0):
        for o in STENCILS:
            p = np.array([psi(a, o, int(k)) for k in ks])
            sl = slopes(ks, p)/2
            theory[f"alpha={a},order={o}"] = {"k": ks.tolist(), "suppression_vs_continuum": (p/(2*ks**a)).tolist(),
                                              "apparent_H_v": sl.tolist()}
            print(f"alpha={a:4} order={o}: true H_v={a/2:.3f}; apparent H_v at k=1,2,4,8,16: "
                  + ", ".join(f"{sl[np.searchsorted(ks, kk)]:.3f}" for kk in (1, 2, 4, 8, 16)), flush=True)
    big = psi(0.5, 8, 2000)/(2*2000**0.5)
    print("continuum check alpha=1/2 order 8, k=2000:", round(big, 4))

    lags = [1, 2, 3, 4, 6, 8, 11, 16, 23, 32, 45, 64]
    basset = {o: basset_W_increment_var(o, lags) for o in STENCILS}
    out = {"meta": {"generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                    "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                    "status": "theory plus post hoc descriptive data comparison; no decision rule"},
           "theory": theory, "continuum_check": big, "lags": lags,
           "basset_apparent_H_v": {str(o): (slopes(np.array(lags), basset[o])/2).tolist() for o in STENCILS}}
    for o in STENCILS:
        print(f"published Basset (noise-free), order {o}: apparent H_v at lags 1..64:",
              np.round(slopes(np.array(lags), basset[o])/2, 3))

    if args.data:
        P34 = json.loads(lab34.PROTOCOL.read_text(encoding="utf-8"))
        for name, expected in P34["target"]["files_sha256"].items():
            if lab35.sha256(args.data / name) != expected:
                raise lab34.GateFailure(f"{name}: digest mismatch")
        Yp, _ = lab34.load_traces(args.data / "barium_titanate_in_acetone_position.csv")
        Ye, _ = lab34.load_traces(args.data / "noise_position.csv")
        r_ = lab35.PUB["r"]
        mass = 4/3*np.pi*r_**3*lab35.PUB["rho_p"] + 2/3*np.pi*r_**3*lab35.PUB["rho_f"]
        kTm = lab35.KB*lab35.PUB["T"]/mass
        data = {}
        for o in STENCILS:
            def incvar(Ys):
                tot = np.zeros(len(lags))
                n = np.zeros(len(lags))
                for y in Ys:
                    _, W = lab41.stencil_velocity(np.asarray(y, float), STENCILS[o], DT)
                    for i, k in enumerate(lags):
                        dW = W[k:] - W[:-k]
                        tot[i] += np.sum((dW - dW.mean())**2)
                        n[i] += len(dW)
                return tot/n
            vp, ve = incvar(Yp), incvar(Ye)
            sub = (vp - ve)/lab41.GAIN2_PUB/kTm
            raw = vp/lab41.GAIN2_PUB/kTm
            data[str(o)] = {"apparent_H_v_noise_subtracted": (slopes(np.array(lags), sub)/2).tolist(),
                            "apparent_H_v_raw": (slopes(np.array(lags), raw)/2).tolist(),
                            "subtracted_over_basset_minus_1": (sub/basset[o] - 1).tolist()}
            print(f"data order {o}: apparent H_v (noise-subtracted):", np.round(slopes(np.array(lags), sub)/2, 3),
                  "\n               raw:", np.round(slopes(np.array(lags), raw)/2, 3),
                  "\n               subtracted/Basset-1:", np.round(sub/basset[o] - 1, 3), flush=True)
        out["data"] = data

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "results.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    for o, col in zip((2, 4, 8), ("C2", "C1", "C0")):
        e = theory[f"alpha=0.5,order={o}"]
        ax.semilogx(e["k"], e["apparent_H_v"], color=col, lw=0.8, ls=":", label=f"pure-cusp theory, α=½, order {o}")
        if args.data:
            ax.semilogx(lags, out["data"][str(o)]["apparent_H_v_noise_subtracted"], "o", color=col, ms=4,
                        label=f"Dryad data, order {o} (noise-subtracted)")
    ax.semilogx(lags, out["basset_apparent_H_v"]["8"], "k-", lw=1.2, label="full published Basset, order 8 (noise-free)")
    if args.data:
        ax.semilogx(lags, out["data"]["8"]["apparent_H_v_raw"], "x", color="C3", ms=6,
                    label="Dryad data, order 8, raw (no noise subtraction)")
    ax.axhline(0.25, color="k", lw=0.8, ls="--", label="$H_v=1/4$ (Basset short-time value)")
    ax.set_xlabel("velocity-increment lag (750 ns bins)")
    ax.set_ylabel("apparent $H_v$ (half the local log-slope)")
    ax.legend(fontsize=7)
    ax.set_title("Stencil velocities make Brownian velocity look smoother at short lags", fontsize=9)
    fig.tight_layout()
    fig.savefig(OUT / "apparent_velocity_roughness.png", dpi=150)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
