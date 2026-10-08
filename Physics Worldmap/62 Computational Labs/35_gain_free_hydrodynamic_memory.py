"""Gain-free test of hydrodynamic memory from conditioned mean displacement; no novelty claim.

R_k = Cov(D_k, W)/Var(W) is in seconds and independent of the volts-to-metres
gain. Equilibrium Basset theory, an initial-value variant, and a memoryless
Langevin model are compared through the measured bin-and-stencil operator.

    python 35_gain_free_hydrodynamic_memory.py --data <dir with Dryad files>
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from multiprocessing import Pool
from datetime import datetime, timezone
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import mpmath as mp
import numpy as np
from scipy.optimize import minimize
from scipy.special import erfcx
from scipy.stats import chi2 as chi2_dist

HERE = Path(__file__).resolve().parent
PROTOCOL = HERE / "gain_free_hydrodynamics_protocol.json"
OUT = HERE / "results" / "gain_free_hydrodynamics"
spec = importlib.util.spec_from_file_location("lab34", HERE / "34_conditioned_displacement_reproduction.py")
lab34 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lab34)
STENCIL8 = lab34.STENCIL8

KB = 1.380649e-23
PUB = {"r": 3.398436499688567e-06, "K": 7.79518420309616e-05, "rho_p": 4200.0, "rho_f": 790.0, "eta": 0.32e-3, "T": 293.0}


def physical_to_scaled(r, K, rho_p=PUB["rho_p"], rho_f=PUB["rho_f"], eta=PUB["eta"]):
    """(gamma/m, z/m, K/m) for a sphere including half the displaced fluid mass."""
    m = 4/3*np.pi*r**3*rho_p + 2/3*np.pi*r**3*rho_f
    return 6*np.pi*r*eta/m, 6*np.pi*r**2*np.sqrt(rho_f*eta)/m, K/m


class Kernel:
    """Partial-fraction inverse Laplace transforms for 1/(s^2 + a s^{3/2} + g s + k), u = -sqrt(s)."""

    def __init__(self, g, a, k):
        self.g, self.a, self.k = g, a, k
        self.q = np.roots([1, -a, g, 0, k]).astype(complex)
        self.den = np.array([np.prod([qi - qj for j, qj in enumerate(self.q) if j != i]) for i, qi in enumerate(self.q)])

    def _sum(self, t, power):
        x = np.sqrt(np.abs(np.asarray(t, float)))[..., None]
        return np.real(np.sum(self.q**power*erfcx(self.q*x)/self.den, axis=-1))

    def mchi(self, t):           # m * chi(t): conditional mean displacement per unit initial velocity
        return self._sum(t, 1)

    def int_mchi_minus_limit(self, t):   # int_0^t m chi - 1/k; equals -m C_x(t)/kT, constant cancels in operators
        return self._sum(t, -1)

    def mpsi(self, t):           # m * L^{-1}[s^{-1/2}/P(s)]
        return -self._sum(t, 0)

    def talbot(self, t, which):
        mp.mp.dps = 30
        P = lambda s: s**2 + self.a*s**mp.mpf(1.5) + self.g*s + self.k
        F = {"mchi": lambda s: 1/P(s), "int": lambda s: 1/(s*P(s)), "mpsi": lambda s: s**mp.mpf(-0.5)/P(s)}[which]
        return float(mp.invertlaplace(F, t, method="talbot"))


def operator_R(kernel, lags, dt, nodes=12):
    """Bin-averaged positions and 8th-order stencil velocity: R_k = r_k/s (seconds)."""
    x, w = np.polynomial.legendre.leggauss(nodes)
    u = 0.5*dt*(x + 1)
    wu = 0.5*dt*w*(1 - u/dt)/dt
    nmax = max(lags) + 9
    n = np.arange(-nmax, nmax + 1)
    Cx = lambda t: -kernel.int_mchi_minus_limit(t)   # m C_x / kT up to an additive constant
    tn = n[:, None]*dt
    G = (Cx(tn + u) + Cx(tn - u)) @ wu
    Gat = lambda i: G[i + nmax]
    ls = np.arange(-4, 5)
    s = sum(STENCIL8[a]*STENCIL8[b]*Gat(ls[a] - ls[b]) for a in range(9) for b in range(9))/dt**2
    r = np.array([sum(STENCIL8[a]*Gat(k - ls[a]) for a in range(9))/dt for k in lags])
    return r/s


def gather(Ys, Ws, lags):
    halves = [lab34.Half(Y, W, 0, len(Y), lags) for Y, W in zip(Ys, Ws)]
    return halves


def moments(halves, rng=None, L=None):
    (mW, mW2, mD, mDW), _ = lab34.pooled(halves, ["cW", "cW2", "cD", "cDW"], rng, L)
    return mDW - mD*mW, mW2 - mW**2


def estimate_R(particle, empty=None, rng=None, L=None):
    """Noise-subtracted when an empty-trap reference is given; volt units cancel either way."""
    r, s = moments(particle, rng, L)
    if empty is not None:
        re, se_ = moments(empty, rng, L)
        r, s = r - re, s - se_
    return r/s


def gls(pred, R, Cinv):
    d = R - pred
    return float(d @ Cinv @ d)


def fit(model, R, Cinv, lags, dt, start):
    def predict(p):
        if model == "B2":
            return operator_R(Kernel(*physical_to_scaled(*np.exp(p))), lags, dt)
        if model == "B3":
            return operator_R(Kernel(*np.exp(p)), lags, dt)
        g, k = np.exp(p)
        return operator_R(Kernel(g, 0.0, k), lags, dt)

    def objective(p):
        try:
            v = gls(predict(p), R, Cinv)
        except (ValueError, np.linalg.LinAlgError, FloatingPointError):
            return 1e30
        return v if np.isfinite(v) else 1e30

    res = minimize(objective, np.log(start), method="Nelder-Mead",
                   options={"xatol": 1e-7, "fatol": 1e-7, "maxiter": 4000, "maxfev": 8000})
    return np.exp(res.x), float(res.fun), predict(res.x)


_REFIT = {}


def _refit(i):
    s = _REFIT
    return {m: fit(m, s["reps"][i], s["Cinv"], s["lags"], s["dt"], s["start"][m])[0] for m in s["start"]}


def sha256(path):
    with Path(path).open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, required=True)
    args = parser.parse_args()
    P = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    P34 = json.loads(lab34.PROTOCOL.read_text(encoding="utf-8"))
    for name, expected in P34["target"]["files_sha256"].items():
        if sha256(args.data / name) != expected:
            raise lab34.GateFailure(f"{name}: digest mismatch")
    lags = P["observable"]["lags_samples"]
    dt = P["observable"]["sample_time_s"]
    unc = P["inference"]["uncertainty"]

    Ys, _ = lab34.load_traces(args.data / "barium_titanate_in_acetone_position.csv")
    Ws, _ = lab34.load_traces(args.data / "barium_titanate_in_acetone_velocity.csv")
    halves = gather(Ys, Ws, lags)
    En, Wn = lab34.load_traces(args.data / "noise_position.csv")[0], lab34.load_traces(args.data / "noise_velocity.csv")[0]
    empty = gather(En, Wn, lags)
    R_raw = estimate_R(halves)
    R = estimate_R(halves, empty)
    R_empty = estimate_R(empty)
    noise_fraction_varW = moments(empty)[1]/moments(halves)[1]
    rng = np.random.default_rng(2026100611)
    reps = np.array([estimate_R(halves, empty, rng, 2000) for _ in range(400)])
    rng_raw = np.random.default_rng(2026100613)
    reps_raw = np.array([estimate_R(halves, None, rng_raw, 2000) for _ in range(400)])
    cov = np.cov(reps.T)
    Cinv = np.linalg.inv(cov)
    se = np.sqrt(np.diag(cov))
    cov_raw = np.cov(reps_raw.T)

    g0, a0, k0 = physical_to_scaled(PUB["r"], PUB["K"])
    kE = Kernel(g0, a0, k0)
    t = np.array(lags)*dt
    R_E = operator_R(kE, lags, dt)
    cont_E = kE.mchi(t)
    R_V = R_E*(1 + a0*kE.mpsi(t)/cont_E)

    fits = {}
    for model, start in (("B2", [PUB["r"], PUB["K"]]), ("B3", [g0, a0, k0]), ("L", [g0, k0])):
        p, c2, pred = fit(model, R, Cinv, lags, dt, start)
        fits[model] = {"params": p, "chi2": c2, "pred": pred}

    print("main fits done:", {m: round(v["chi2"], 2) for m, v in fits.items()}, flush=True)
    boot_params = {m: [] for m in fits}
    brng = np.random.default_rng(2026100612)
    _REFIT.update(reps=reps, Cinv=Cinv, lags=lags, dt=dt, start={m: fits[m]["params"] for m in fits})
    with Pool(min(16, os.cpu_count() or 1)) as pool:
        for done, res in enumerate(pool.imap(_refit, brng.choice(len(reps), 100, replace=False)), 1):
            for model in fits:
                boot_params[model].append(res[model])
            if done % 20 == 0:
                print(f"bootstrap refits {done}/100", flush=True)

    def interval(model, idx):
        v = np.array(boot_params[model])[:, idx]
        return [float(np.percentile(v, 16)), float(np.percentile(v, 84))]

    n = len(lags)
    models = {
        "E_published": (R_E, 0, gls(R_E, R, Cinv)),
        "V_initial_value_variant": (R_V, 0, gls(R_V, R, Cinv)),
        "B2_fit": (fits["B2"]["pred"], 2, fits["B2"]["chi2"]),
        "B3_fit": (fits["B3"]["pred"], 3, fits["B3"]["chi2"]),
        "L_fit": (fits["L"]["pred"], 2, fits["L"]["chi2"]),
    }
    table = {}
    for name, (pred, npar, c2) in models.items():
        dof = n - npar
        table[name] = {"chi2": c2, "dof": dof, "p": float(chi2_dist.sf(c2, dof)),
                       "chi2_se_corrected": c2/1.44, "p_se_corrected": float(chi2_dist.sf(c2/1.44, dof)),
                       "prediction_s": pred.tolist(), "z": ((R - pred)/se).tolist()}

    Craw_inv = np.linalg.inv(cov_raw)
    secondary = {}
    for name in ("E_published", "V_initial_value_variant"):
        pred = models[name][0]
        c2 = gls(pred, R_raw, Craw_inv)
        secondary[name] = {"chi2": c2, "dof": n, "p": float(chi2_dist.sf(c2, n))}
    for model in ("B2", "B3", "L"):
        p, c2, _ = fit(model, R_raw, Craw_inv, lags, dt, fits[model]["params"])
        secondary[model + "_fit"] = {"params": p, "chi2": c2, "dof": n - (3 if model == "B3" else 2)}

    gB3, aB3, kB3 = fits["B3"]["params"]
    r_ratio = aB3/gB3*np.sqrt(PUB["eta"]/PUB["rho_f"])
    r_ratio_int = [float(np.percentile(np.array(boot_params["B3"])[:, 1]/np.array(boot_params["B3"])[:, 0], q))*np.sqrt(PUB["eta"]/PUB["rho_f"]) for q in (16, 84)]

    verification = {}
    for name, ker in (("E", kE), ("B3", Kernel(*fits["B3"]["params"])), ("L", Kernel(fits["L"]["params"][0], 0, fits["L"]["params"][1]))):
        errs = []
        for tt in (1e-7, 3e-6, 4e-5, 1.9e-4):
            for which, f in (("mchi", ker.mchi), ("int", lambda x: ker.int_mchi_minus_limit(x) + 1/ker.k), ("mpsi", ker.mpsi)):
                exact = ker.talbot(tt, which)
                errs.append(abs(float(f(tt)) - exact)/max(abs(exact), 1e-300))
        verification[name] = max(errs)
    nodes_check = float(np.max(np.abs(operator_R(kE, lags, dt, 96)/R_E - 1)))  # 12-node default vs 96

    dec = {
        "E_published_consistent": table["E_published"]["p"] > 0.01,
        "V_rejected_vs_E": table["V_initial_value_variant"]["chi2"] - table["E_published"]["chi2"] > 25,
        "memory_supported_L_minus_B2": table["L_fit"]["chi2"] - table["B2_fit"]["chi2"],
        "z_over_m_B3": [float(aB3), interval("B3", 1)],
        "z_over_m_stokes_basset_at_published_radius": float(a0),
    }
    dec["memory_supported"] = dec["memory_supported_L_minus_B2"] > 25
    dec["z_interval_contains_stokes_basset"] = bool(dec["z_over_m_B3"][1][0] <= a0 <= dec["z_over_m_B3"][1][1])

    out = {
        "meta": {"generated": datetime.now(timezone.utc).isoformat(timespec="seconds"), "protocol_sha256": sha256(PROTOCOL),
                 "script_sha256": sha256(__file__)},
        "lags": lags, "R_data_s": R.tolist(), "R_raw_s": R_raw.tolist(), "noise_fraction_of_varW": float(noise_fraction_varW),
        "secondary_raw": secondary, "R_se_s": se.tolist(), "R_empty_trap_s": R_empty.tolist(),
        "continuum_E_mchi_s": cont_E.tolist(), "operator_correction_E": (R_E/cont_E).tolist(),
        "models": table,
        "fits": {
            "B2": {"radius_m": float(fits["B2"]["params"][0]), "radius_16_84": interval("B2", 0),
                   "K_N_per_m": float(fits["B2"]["params"][1]), "K_16_84": interval("B2", 1)},
            "B3": {"gamma_over_m": float(gB3), "gamma_over_m_16_84": interval("B3", 0), "z_over_m": float(aB3),
                   "z_over_m_16_84": interval("B3", 1), "K_over_m": float(kB3), "K_over_m_16_84": interval("B3", 2),
                   "radius_from_z_over_gamma_m": float(r_ratio), "radius_from_z_over_gamma_16_84": r_ratio_int},
            "L": {"gamma_over_m": float(fits["L"]["params"][0]), "K_over_m": float(fits["L"]["params"][1])},
            "published_scaled": {"gamma_over_m": float(g0), "z_over_m": float(a0), "K_over_m": float(k0)},
        },
        "decision": dec,
        "verification": {"max_rel_error_root_form_vs_talbot": verification, "quadrature_48_vs_96_nodes_max_rel": nodes_check},
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "results.json").write_text(json.dumps(lab34.to_jsonable(out), indent=2), encoding="utf-8")

    fig, ax = plt.subplots(2, 1, figsize=(7, 7), sharex=True, gridspec_kw={"height_ratios": [3, 2]})
    ax[0].errorbar(t*1e6, R*1e6, yerr=se*1e6, fmt="o", ms=3, color="k", label="data (gain-free)")
    styles = {"E_published": "-", "V_initial_value_variant": "--", "B3_fit": ":", "L_fit": "-."}
    for name, ls in styles.items():
        ax[0].plot(t*1e6, np.array(table[name]["prediction_s"])*1e6, ls, label=name)
        ax[1].plot(t*1e6, table[name]["z"], ls, marker=".", label=name)
    ax[0].set_ylabel("Cov(D,W)/Var(W)  [µs]")
    ax[0].set_xscale("log"); ax[0].set_yscale("log"); ax[0].legend(fontsize=8)
    ax[1].axhline(0, color="k", lw=.5); ax[1].set_ylabel("z = (data - model)/SE"); ax[1].set_xlabel("lag [µs]")
    ax[1].set_ylim(-15, 15)
    fig.tight_layout(); fig.savefig(OUT / "gain_free_regression.png", dpi=150)

    for name, row in table.items():
        print(f"{name:>26}: chi2={row['chi2']:9.2f} dof={row['dof']:2d} p={row['p']:.3g}  (SE-corrected p={row['p_se_corrected']:.3g})")
    print(f"noise fraction of Var(W): {noise_fraction_varW:.4f}")
    print("secondary (raw, no noise subtraction):", json.dumps(lab34.to_jsonable(secondary)))
    print(json.dumps(lab34.to_jsonable({"fits": out["fits"], "decision": dec, "verification": out["verification"]}), indent=1))


if __name__ == "__main__":
    main()
