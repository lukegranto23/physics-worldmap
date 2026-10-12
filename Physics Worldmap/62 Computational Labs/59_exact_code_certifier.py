"""Generic exact certification of spherical codes from Cohn's table (or any code file).

The identification step is heuristic; the certificate is exact and does not depend on how the guess was made.

For a code X (N unit vectors in R^d):
  1. Contact core: the points touching at mu (|<x_i,x_j> - mu| < 1e-8). Rattlers are set aside.
  2. Class the core inner products into K distinct values (g_K = mu is the maximum). Newton-polish the core so that each
     class is exactly equal (double precision).
  3. Guess: candidate minimal polynomials q of mu (integer relations at double precision, degree <= 8, several coefficient
     bounds and tolerances; double precision admits spurious relations, so every candidate is tried). For each q, every
     g_k is written as a polynomial in mu with rational coefficients (PSLQ on {g_k, 1, mu, ..., mu^(deg-1)}).
  4. Certificate, exact over Q(mu) = Q[x]/(q):
       (a) q is irreducible, and mu is isolated as a real root of q;
       (b) the Gram matrix G (diagonal 1, entries g_k(mu)) has rank exactly d (DomainMatrix over QQ<mu>);
       (c) G is PSD: its d nonzero eigenvalues, evaluated at 60 digits from the exact values, are positive with a margin
           far above the 1e-50 error. Exact rank d means the other eigenvalues are exactly 0;
       (d) all other values g_k (k < K) are < mu, and all are < 1.
     (b)-(d) show that G is the Gram matrix of |core| distinct unit vectors in R^d with cosine of minimal angle exactly mu.
     A candidate polynomial that fails (b)-(d) is rejected; this is how spurious guesses are caught.
  5. Rattlers are not certified exactly. Report their numerical slack, mu - max<rattler, others>, against the exact core.

    python 59_exact_code_certifier.py --table d N [d N ...]     (downloads https://spherical-codes.org/data/d/N)
    python 59_exact_code_certifier.py --file path d N
"""
from __future__ import annotations

import argparse
import json
import urllib.request
from pathlib import Path

import mpmath as mp
import numpy as np
import sympy as sp
from scipy.optimize import least_squares
from sympy.polys.matrices import DomainMatrix

HERE = Path(__file__).resolve().parent
OUT = HERE / "results" / "spherical_codes" / "exact_certificates"
x = sp.symbols("x")


def fetch(d, N):
    with urllib.request.urlopen(f"https://spherical-codes.org/data/{d}/{N}", timeout=60) as r:
        return np.array([[float(v) for v in l.split(",")] for l in r.read().decode().strip().splitlines()])


def polish_equalities(Y, col, K):
    n, d = Y.shape; iu = np.triu_indices(n, 1); c = col[iu]
    def res(v):
        Z = v.reshape(n, d); G = Z @ Z.T; g = G[iu]
        means = np.array([g[c == k].mean() for k in range(K)])
        return np.concatenate([g - means[c], np.diag(G) - 1])
    sol = least_squares(res, Y.ravel(), xtol=1e-15, ftol=1e-15, gtol=1e-15, method="lm")
    Z = sol.x.reshape(n, d); Z /= np.linalg.norm(Z, axis=1, keepdims=True)
    G = Z @ Z.T
    return Z, np.array([G[iu][c == k].mean() for k in range(K)]), float(np.abs(res(sol.x)).max())


def hp_refine(g0, col, n, d, K, dps=90, iters=8):
    """Gauss-Newton on the K Gram values so that G(g) has rank d (the n-d smallest |eigenvalues| vanish)."""
    mp.mp.dps = dps
    A = [mp.matrix((col == k).astype(int).tolist()) for k in range(K)]
    def res(g):
        G = mp.eye(n)
        for k in range(K): G += g[k]*A[k]
        L, _ = mp.eigsy(G); return sorted(L, key=abs)[:n - d]
    g = [mp.mpf(float(v)) for v in g0]; h = mp.mpf(10)**(-(dps//2))
    for _ in range(iters):
        r = mp.matrix(res(g))
        if mp.norm(r) < mp.mpf(10)**(-(dps - 8)): break
        J = mp.matrix(len(r), K)
        for j in range(K):
            y = list(g); y[j] += h; J[:, j] = (mp.matrix(res(y)) - r)/h
        U, S, Vt = mp.svd_r(J)
        dx = -(Vt.T*mp.diag([1/s_ if s_ > mp.mpf(10)**(-(dps//3)) else 0 for s_ in S])*(U.T*r))
        g = [g[j] + dx[j] for j in range(K)]
    return g, mp.norm(mp.matrix(res(g))), min(S)


def candidate_polys(mu):
    mp.mp.dps = 50; out = []
    for deg in range(1, 9):
        for mc in (10**3, 10**5, 10**7):
            for tol in (mp.mpf(10)**-34, mp.mpf(10)**-30):
                p = mp.findpoly(mu, deg, maxcoeff=mc, tol=tol)
                if not p: continue
                q = sp.Poly([int(c) for c in p], x)
                for f, _ in sp.factor_list(q.as_expr())[1]:     # keep the irreducible factor that vanishes at mu
                    P = sp.Poly(f, x)
                    if P.degree() >= 1 and abs(sp.N(P.as_expr().subs(x, sp.Float(mp.nstr(mu, 45), 45)), 50)) < 1e-25*max(abs(int(c)) for c in P.all_coeffs()):
                        if P.LC() < 0: P = -P
                        if P not in out: out.append(P)
    return out


def attempt(q, g, mu, col, n, d, K):
    rep = {"minimal_polynomial": str(q.as_expr())}
    deg = q.degree(); mp.mp.dps = 50
    exprs = []
    for k, v in enumerate(g):
        if k == K - 1 and deg > 1:
            exprs.append(x); continue
        if deg == 1:
            rel = mp.pslq([v, mp.mpf(1)], maxcoeff=10**9, maxsteps=10**6, tol=mp.mpf(10)**-30)
            if rel is None or rel[0] == 0:
                rep["status"] = "value not rational"; return rep
            exprs.append(sp.Rational(-rel[1], rel[0])); continue
        rel = mp.pslq([v] + [mu**i for i in range(deg)], maxcoeff=10**9, maxsteps=10**6, tol=mp.mpf(10)**-30)
        if rel is None or rel[0] == 0:
            rep["status"] = f"could not express {float(v):.12f} in Q(mu)"; return rep
        exprs.append(sum(sp.Rational(-c, rel[0])*x**i for i, c in enumerate(rel[1:])))
    rep["gram_values"] = [str(e) for e in exprs]
    roots = [r for r in q.real_roots() if abs(float(r) - float(mu)) < 1e-10]
    if len(roots) != 1:
        rep["status"] = "root isolation failed"; return rep
    root = roots[0]
    if deg == 1:
        F = sp.QQ; el = [sp.QQ(sp.Rational(e)) for e in exprs]; one = sp.QQ(1)
    else:
        F = sp.QQ.algebraic_field(root); el = [F.from_sympy(sp.sympify(e).subs(x, root)) for e in exprs]; one = F.one
    M = DomainMatrix([[one if i == j else el[col[i, j]] for j in range(n)] for i in range(n)], (n, n), F)
    rank = int(M.rank()); rep["exact_rank"] = rank
    if rank != d:
        rep["status"] = "rank != d"; return rep
    mp.mp.dps = 60
    if deg == 1:
        gv = [mp.mpf(sp.Rational(e).p)/sp.Rational(e).q for e in exprs]
    else:
        cf = [int(c) for c in q.all_coeffs()]
        r60 = mp.findroot(lambda t: sum(c*t**(deg - i) for i, c in enumerate(cf)), mu)
        gv = [sp.lambdify(x, sp.sympify(e), "mpmath")(r60) for e in exprs]
    Gm = mp.matrix(n, n)
    for i in range(n):
        for j in range(n): Gm[i, j] = 1 if i == j else gv[col[i, j]]
    L, U = mp.eigsy(Gm)
    nz = sorted(L[i] for i in range(n) if abs(L[i]) > mp.mpf(10)**-30)
    others = max(gv[:-1]) if K > 1 else mp.mpf(-2)
    rep.update(nonzero_eigenvalues=len(nz), min_nonzero_eigenvalue=mp.nstr(nz[0], 6) if nz else None,
               max_other_value=mp.nstr(others, 10), mu=mp.nstr(gv[-1], 40))
    ok = len(nz) == d and nz[0] > mp.mpf(10)**-20 and others < gv[-1] and max(gv) < 1
    rep["certified_core"] = bool(ok); rep["status"] = "CERTIFIED" if ok else "PSD/ordering check failed"
    if ok:
        idx = [i for i in range(n) if abs(L[i]) > mp.mpf(10)**-30]
        rep["_Yhp"] = np.array([[float(U[r, i]*mp.sqrt(L[i])) for i in idx] for r in range(n)])
        rep["_mu"] = gv[-1]
    return rep


def certify(X, d, N, label):
    rep = {"d": d, "N": N, "source": label}
    X = X/np.linalg.norm(X, axis=1, keepdims=True); G = X @ X.T; np.fill_diagonal(G, -2); mu0 = G.max()
    C = np.abs(G - mu0) < 1e-8; core = np.where(C.sum(1) > 0)[0]; ratt = np.where(C.sum(1) == 0)[0]
    Y = X[core]; n = len(core); Gc = Y @ Y.T
    vals = np.unique(np.round(Gc[np.triu_indices(n, 1)], 6)); K = len(vals)
    col = np.searchsorted(vals, np.round(Gc, 6)); np.fill_diagonal(col, -1)
    rep.update(core=n, rattlers=len(ratt), distinct=K)
    if K > 40:
        rep["status"] = "too many distinct values"; return rep
    Y, g, err = polish_equalities(Y, col, K); rep["polish_residual"] = err
    if err > 1e-12:
        rep["status"] = "classes not exactly equalisable (not a rigid exact structure)"; return rep
    ghp, rres, smin = hp_refine(g, col, n, d, K); rep["hp_residual"] = mp.nstr(rres, 3); rep["hp_min_singular"] = mp.nstr(smin, 3)
    if rres > mp.mpf(10)**-35:
        rep["status"] = "high-precision refinement did not converge"; return rep
    g = ghp; mu = g[-1]; tried = []; best = None
    for q in candidate_polys(mu):
        sub = attempt(q, g, mu, col, n, d, K)
        tried.append({k: sub.get(k) for k in ("minimal_polynomial", "exact_rank", "status")})
        if sub.get("certified_core"):
            best = sub; break
    rep["candidates_tried"] = tried
    if best is None:
        rep["status"] = "no candidate certified"; return rep
    Yhp = best.pop("_Yhp"); mu_ex = best.pop("_mu"); rep.update(best)
    if len(ratt):
        Uq, _, Vq = np.linalg.svd(X[core].T @ Yhp); R = X[ratt] @ (Uq @ Vq)
        allp = np.vstack([Yhp, R]); Ga = allp @ allp.T; np.fill_diagonal(Ga, -2)
        rep["rattler_slack"] = float(mu_ex - Ga[n:].max())
    return rep


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--table", nargs="*", type=int)
    ap.add_argument("--file", nargs=3)
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    jobs = [(a.table[i], a.table[i + 1], None) for i in range(0, len(a.table or []), 2)]
    if a.file:
        jobs.append((int(a.file[1]), int(a.file[2]), a.file[0]))
    for d, N, f in jobs:
        try:
            X = np.loadtxt(f, delimiter=",") if f else fetch(d, N)
            rep = certify(X, d, N, f or "spherical-codes.org")
        except Exception as e:
            rep = {"d": d, "N": N, "status": "error: " + repr(e)}
        print(json.dumps(rep), flush=True)
        with open(OUT / "certificates.jsonl", "a") as fh: fh.write(json.dumps(rep) + "\n")


if __name__ == "__main__":
    main()
