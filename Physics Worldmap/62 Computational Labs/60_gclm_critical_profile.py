"""gCLM (Okamoto-Sakajo-Wunsch) on R: the critical advection a_c where the self-similar focusing exponent c_l vanishes.

Model: w_t + a u w_x = u_x w, u_x = H w (H cos = sin). Self-similar ansatz w = (T-t)^(-1) W(x/(T-t)^{c_l}) gives
    (c_l x + a u) W' = (-1 + u') W,   u' = H W,   u(0) = 0,   W odd,   W'(0) = -1.
At x -> 0 this forces c_l = -1 + (1-a) u'(0). At c_l = 0 the solution is w = W(x)/(T-t), neither focusing nor expanding.
Lushnikov-Silantyev-Siegel (arXiv:2010.01201) found a_c = 0.6890665337007457... numerically. Huang-Qin-Wang-Wei
(arXiv:2305.05895) prove that profiles exist for all a <= 1, but the location of the sign change of c_l is not proved.

Discretisation (Cayley map, which makes the line Hilbert transform exactly the periodic conjugate function):
  x = L tan(phi/2), Theta(x) = int_0^x W, Psi(phi) = Theta - Theta(inf) = sum_{k=0..N} c_k cos(k phi)  (even, Psi(pi) = 0)
  u = H Psi = sum c_k sin(k phi),  W = (2/L) cos^2(phi/2) Psi_phi.
Unknowns c_0..c_N and a (with c_l fixed). Equations: residual at N collocation points phi_j = pi (j - 1/2)/N, plus
Psi(pi) = 0 and W'(0) = -1. Newton's method in mpmath with the exact Jacobian; the system is polynomial in the unknowns.
A double-precision Levenberg-Marquardt solve gives the start, and Newton is then run at the requested precision.

    python 60_gclm_critical_profile.py --N 120 --L 4 --dps 50 [--cl 0]
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import mpmath as mp
import numpy as np
from scipy.optimize import least_squares

HERE = Path(__file__).resolve().parent
OUT = HERE / "results" / "gclm_critical"


def float_start(N, L, cl, a0=0.69):
    M = N; phi = np.pi*(np.arange(1, M + 1) - 0.5)/M; k = np.arange(N + 1)
    C = np.cos(np.outer(phi, k)); S = np.sin(np.outer(phi, k)); g = (2/L)*np.cos(phi/2)**2
    gp = -(2/L)*np.cos(phi/2)*np.sin(phi/2)
    def res(z):
        c, a = z[:-1], z[-1]
        Pp = -(S*k) @ c; Ppp = -(C*k**2) @ c; u = S @ c; up = (C*k) @ c
        w = g*Pp; wp = gp*Pp + g*Ppp
        R = cl*np.sin(phi)*wp + a*g*u*wp - (-1 + g*up)*w
        return np.concatenate([R, [np.sum(c*(-1.0)**k), -(4/L**2)*np.sum(k**2*c) + 1]])
    xx = L*np.tan(phi/2); sig = 4.0
    Psi = -sig**2*(1 - np.exp(-xx**2/(2*sig**2))) + sig**2
    c0 = np.linalg.lstsq(C, Psi, rcond=None)[0]; c0 *= -1/(-(4/L**2)*np.sum(k**2*c0))
    sol = least_squares(res, np.concatenate([c0, [a0]]), xtol=1e-15, ftol=1e-15, gtol=1e-15, max_nfev=4000, method="lm")
    return sol.x, float(np.abs(res(sol.x)).max())


def newton_mp(z0, N, L, cl, dps, iters=12):
    mp.mp.dps = dps
    L = mp.mpf(L); cl = mp.mpf(cl); M = N
    phi = [mp.pi*(j - mp.mpf(1)/2)/M for j in range(1, M + 1)]
    C = [[mp.cos(k*p) for k in range(N + 1)] for p in phi]; S = [[mp.sin(k*p) for k in range(N + 1)] for p in phi]
    g = [2/L*mp.cos(p/2)**2 for p in phi]; gp = [-2/L*mp.cos(p/2)*mp.sin(p/2) for p in phi]; sp_ = [mp.sin(p) for p in phi]
    z = [mp.mpf(float(v)) for v in z0]
    hist = []
    for it in range(iters):
        c, a = z[:-1], z[-1]
        rows = []; F = []
        for j in range(M):
            Pp = -mp.fsum(S[j][k]*k*c[k] for k in range(N + 1)); Ppp = -mp.fsum(C[j][k]*k*k*c[k] for k in range(N + 1))
            u = mp.fsum(S[j][k]*c[k] for k in range(N + 1)); up = mp.fsum(C[j][k]*k*c[k] for k in range(N + 1))
            w = g[j]*Pp; wp = gp[j]*Pp + g[j]*Ppp
            F.append(cl*sp_[j]*wp + a*g[j]*u*wp - (-1 + g[j]*up)*w)
            # derivatives w.r.t. c_k
            row = []
            for k in range(N + 1):
                dPp = -S[j][k]*k; dPpp = -C[j][k]*k*k; du = S[j][k]; dup = C[j][k]*k
                dw = g[j]*dPp; dwp = gp[j]*dPp + g[j]*dPpp
                row.append(cl*sp_[j]*dwp + a*g[j]*(du*wp + u*dwp) - (g[j]*dup*w + (-1 + g[j]*up)*dw))
            row.append(g[j]*u*wp)                                  # d/da
            rows.append(row)
        F.append(mp.fsum(c[k]*(-1)**k for k in range(N + 1))); rows.append([mp.mpf((-1)**k) for k in range(N + 1)] + [0])
        F.append(-4/L**2*mp.fsum(k*k*c[k] for k in range(N + 1)) + 1); rows.append([-4/L**2*k*k for k in range(N + 1)] + [0])
        J = mp.matrix(rows); Fv = mp.matrix(F)
        nr = mp.norm(Fv, mp.inf); hist.append(mp.nstr(nr, 3))
        if nr < mp.mpf(10)**(-(dps - 5)): break
        dz = mp.lu_solve(J, -Fv)
        z = [z[i] + dz[i] for i in range(len(z))]
    return z, hist


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--N", type=int, default=120); ap.add_argument("--L", type=float, default=4.0)
    ap.add_argument("--dps", type=int, default=50); ap.add_argument("--cl", type=float, default=0.0)
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    t = time.time(); z0, r0 = float_start(a.N, a.L, a.cl)
    z, hist = newton_mp(z0, a.N, a.L, a.cl, a.dps)
    rec = {"N": a.N, "L": a.L, "dps": a.dps, "cl": a.cl, "float_a": float(z0[-1]), "float_residual": r0,
           "a": mp.nstr(z[-1], a.dps - 5), "newton_residuals": hist,
           "tail_coeffs": [mp.nstr(abs(v), 3) for v in z[-6:-1]], "seconds": round(time.time() - t, 1)}
    print(json.dumps(rec), flush=True)
    with open(OUT / "runs.jsonl", "a") as f: f.write(json.dumps(rec) + "\n")


if __name__ == "__main__":
    main()
