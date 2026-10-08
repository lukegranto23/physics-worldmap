"""Can localization noise manufacture a speed-persistence coupling? Theory + simulation; no novelty claim.

Model: 2D persistent random walk with Ornstein-Uhlenbeck velocity (speed scale v, persistence
time P) and NO coupling between v and P. Positions sampled every dt, each coordinate observed
with independent Gaussian localization error sigma. Measured steps s_i = r_{i+1} - r_i.

Per coordinate, true steps are stationary Gaussian with
    V  = Var(step)          = 2 v^2 P^2 (dt/P - 1 + e^{-dt/P})
    C1 = Cov(step_i, step_{i+1}) = v^2 P^2 (1 - e^{-dt/P})^2
(v^2 = per-coordinate velocity variance). Localization error adds 2 sigma^2 to the variance and
-sigma^2 to the lag-1 covariance. Consecutive measured steps are therefore isotropic bivariate
Gaussian vectors with correlation
    rho = (C1 - sigma^2) / (V + 2 sigma^2),
and the mean turning cosine has the closed form (2D isotropic Gaussian, correlation rho)
    E[cos theta] = (pi/4) rho 2F1(1/2, 1/2; 2; rho^2).
The measured mean speed is E|s|/dt = sqrt(pi (V + 2 sigma^2)/2)/dt.

Consequence: for fixed P, slower cells (smaller v) have smaller V and C1 relative to sigma^2,
so their apparent persistence E[cos theta] falls. Population heterogeneity in v alone then
produces a positive speed-persistence correlation with no biological coupling.
Also reported: the sparse-sampling regime (dt >~ P) of Ganusov et al., where heterogeneity in
P alone produces the correlation; together they bound an artefact-light window, if any.

Checks: closed form vs Monte Carlo for several (v, P, dt, sigma).
    python 48_speed_persistence_noise_theory.py
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.special import hyp2f1

HERE = Path(__file__).resolve().parent
OUT = HERE / "results" / "speed_persistence_theory"


def step_moments(v, P, dt):
    x = dt/P
    V = 2*v**2*P**2*(x - 1 + np.exp(-x))
    C1 = v**2*P**2*(1 - np.exp(-x))**2
    return V, C1


def mean_cos(rho):
    rho = np.clip(rho, -0.999999, 0.999999)
    return np.pi/4*rho*hyp2f1(0.5, 0.5, 2.0, rho**2)


def apparent(v, P, dt, sigma):
    V, C1 = step_moments(v, P, dt)
    rho = (C1 - sigma**2)/(V + 2*sigma**2)
    speed = np.sqrt(np.pi*(V + 2*sigma**2)/2)/dt
    return speed, mean_cos(rho), rho


def simulate(v, P, dt, sigma, n_steps, n_tracks, rng, sub=200):
    """Exact OU velocity integration on a fine grid, sampled every dt, plus localization noise."""
    h = dt/sub
    a = np.exp(-h/P)
    # exact joint (position increment, velocity) update for OU per coordinate
    q = v**2*(1 - a**2)
    vel = rng.normal(0, v, (n_tracks, 2))
    pos = np.zeros((n_tracks, 2))
    out = np.empty((n_tracks, n_steps + 1, 2))
    out[:, 0] = pos
    for i in range(1, n_steps + 1):
        for _ in range(sub):
            vn = a*vel + np.sqrt(q)*rng.normal(size=vel.shape)
            pos = pos + 0.5*h*(vel + vn)      # trapezoid; fine grid makes the error negligible
            vel = vn
        out[:, i] = pos
    out = out + rng.normal(0, sigma, out.shape)
    s = np.diff(out, axis=1)
    sp = np.linalg.norm(s, axis=2)
    cos = np.sum(s[:, 1:]*s[:, :-1], axis=2)/(sp[:, 1:]*sp[:, :-1])
    return sp.mean()/dt, cos.mean()


def main():
    rng = np.random.default_rng(2026100891)
    checks = []
    for v, P, dt, sigma in [(1.0, 60, 24, 0.0), (1.0, 60, 24, 3.0), (0.3, 60, 24, 3.0), (0.3, 200, 24, 1.0), (2.0, 30, 24, 2.0)]:
        sp_t, c_t, rho = apparent(v, P, dt, sigma)
        sp_m, c_m = simulate(v, P, dt, sigma, 60, 400, rng, sub=60)
        checks.append({"v": v, "P": P, "dt": dt, "sigma": sigma, "speed_theory": float(sp_t), "speed_mc": float(sp_m),
                       "cos_theory": float(c_t), "cos_mc": float(c_m)})
        print(f"v={v} P={P} dt={dt} sigma={sigma}: speed {sp_t:.4f} vs MC {sp_m:.4f}; <cos> {c_t:.4f} vs MC {c_m:.4f}", flush=True)

    # population with heterogeneous speed, identical persistence: apparent coupling vs noise
    vs = np.exp(np.linspace(np.log(0.05), np.log(1.0), 60))      # per-coordinate velocity sd, um/s
    P, dt = 60.0, 24.0
    curves = {}
    for sigma in (0.0, 0.5, 1.0, 2.0):
        sp, c, _ = apparent(vs, P, dt, sigma)
        curves[str(sigma)] = {"speed": sp.tolist(), "mean_cos": c.tolist()}
    # sparse-sampling regime for comparison: heterogeneous P, identical v, no noise
    Ps = np.exp(np.linspace(np.log(5), np.log(600), 60))
    sp2, c2, _ = apparent(0.3, Ps, dt, 0.0)

    out = {"meta": {"generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                    "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
           "checks": checks, "speed_heterogeneity_curves_P60_dt24": curves,
           "persistence_heterogeneity_v0.3_dt24": {"P": Ps.tolist(), "speed": sp2.tolist(), "mean_cos": c2.tolist()}}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "results.json").write_text(json.dumps(out, indent=2), encoding="utf-8")

    fig, ax = plt.subplots(1, 2, figsize=(10, 4))
    for sigma, col in zip(("0.0", "0.5", "1.0", "2.0"), ("k", "C0", "C1", "C3")):
        ax[0].semilogx(curves[sigma]["speed"], curves[sigma]["mean_cos"], color=col, label=f"σ = {sigma} µm")
    ax[0].set_xlabel("measured mean speed (µm/s)"); ax[0].set_ylabel("apparent persistence ⟨cos θ⟩")
    ax[0].set_title("Same persistence (P = 60 s) for every cell;\nlocalization noise alone makes slow cells look less persistent", fontsize=9)
    ax[0].legend(fontsize=8)
    ax[1].semilogx(sp2, c2, "C2")
    ax[1].set_xlabel("measured mean speed (µm/s)"); ax[1].set_ylabel("apparent persistence ⟨cos θ⟩")
    ax[1].set_title("Same speed, varying persistence, no noise:\nthe sparse-sampling mechanism (Ganusov et al.)", fontsize=9)
    fig.tight_layout(); fig.savefig(OUT / "noise_made_coupling.png", dpi=150)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
