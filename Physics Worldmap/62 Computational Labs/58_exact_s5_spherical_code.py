"""Exact structure of the improved (d=13, N=59) spherical code: an S5-symmetric 57-point core plus two rattlers.

Pipeline (from lab 56/57's numerical code, results/spherical_codes/codes/sc_13_59.txt):
  1. Contact graph at mu. 57 points are in contact; the other 2 are rattlers.
  2. The 57x57 Gram matrix takes 9 distinct values. A colour-preserving permutation search finds its automorphism
     group: order 120, with the element-order statistics of S5. Orbits have sizes 1, 5, 5, 6, 20, 20.
  3. Characters of the induced orthogonal action: R^13 = 3*1 + sgn + 4 + 5'.
  4. Exact linear relations: G must vanish on the 4', 5 and 6 isotypic components. These relations are integer-coefficient
     equations in the 9 values, and they fix g1 = 2mu-1, g2 = (5mu-2)/3 and g5 = (4mu-1)/3.
  5. The rank conditions on the remaining isotypic blocks (ranks 3, 1, 4 and 5) are solved by Gauss-Newton at 90 digits.
     The solution is isolated: the smallest singular value of the Jacobian is 0.0165.
  6. PSLQ: mu is the root near 0.1714 of 1196x^4 - 1428x^3 + 411x^2 + 18x - 9 (irreducible), and every Gram value lies in
     Q(mu) with small rational coefficients (residuals below 1e-42).
  7. Rigorous existence: the exact Gram matrix over Q(mu) has rank 13 (exact DomainMatrix rank). Its 13 nonzero eigenvalues
     are >= 1.818 at 60 digits (error 1e-60), so it is PSD. All other values are <= 0.1052 < mu. Hence a 57-point code in
     R^13 with cosine of minimal angle exactly mu exists.
  8. The two rattlers are re-attached at 50-digit precision; their max inner product is 0.112 < mu. This gives the 58- and
     59-point codes with cos(minimal angle) = mu = 0.17137828088359479362302865869...

    python 58_exact_s5_spherical_code.py      (about 2 minutes; needs numpy, scipy, mpmath, sympy)
"""
from __future__ import annotations

import collections
import json
import sys
from pathlib import Path

import mpmath as mp
import numpy as np
import sympy as sp
from scipy.optimize import minimize
from sympy.polys.matrices import DomainMatrix

HERE = Path(__file__).resolve().parent
CODES = HERE / "results" / "spherical_codes" / "codes"
OUT = HERE / "results" / "spherical_codes" / "exact_13"
sys.setrecursionlimit(10000)

CHARS = {'1': dict(e=1, t=1, dt=1, c3=1, c4=1, c5=1, c6=1), 'sgn': dict(e=1, t=-1, dt=1, c3=1, c4=-1, c5=1, c6=-1),
         '4': dict(e=4, t=2, dt=0, c3=1, c4=0, c5=-1, c6=-1), "4p": dict(e=4, t=-2, dt=0, c3=1, c4=0, c5=-1, c6=1),
         '5': dict(e=5, t=1, dt=1, c3=-1, c4=-1, c5=0, c6=1), "5p": dict(e=5, t=-1, dt=1, c3=-1, c4=1, c5=0, c6=-1),
         '6': dict(e=6, t=0, dt=-2, c3=0, c4=0, c5=1, c6=0)}


def load_core():
    X = np.loadtxt(CODES / "sc_13_59.txt", delimiter=","); X /= np.linalg.norm(X, axis=1, keepdims=True)
    G = X @ X.T; mu = G[np.triu_indices(len(X), 1)].max()
    C = np.abs(G - mu) < 1e-8; np.fill_diagonal(C, False)
    deg = C.sum(1)
    return X, np.where(deg > 0)[0], np.where(deg == 0)[0]


def automorphisms(col):
    n = len(col); prof = [tuple(sorted(col[i])) for i in range(n)]
    cand = [[j for j in range(n) if prof[j] == prof[i]] for i in range(n)]
    order = sorted(range(n), key=lambda i: len(cand[i])); auts = []
    def bt(k, img, used):
        if k == n: auts.append(img.copy()); return
        v = order[k]
        for w in cand[v]:
            if used[w] or any(col[v, u] != col[w, img[u]] for u in order[:k]): continue
            img[v] = w; used[w] = True; bt(k + 1, img, used); used[w] = False
        img[v] = -1
    bt(0, [-1]*n, [False]*n)
    return np.array(auts)


def elem_order(p):
    q = np.arange(len(p)); k = 0
    while True:
        q = p[q]; k += 1
        if np.all(q == np.arange(len(p))): return k


def main():
    OUT.mkdir(parents=True, exist_ok=True); rep = {}
    X, core, ratt = load_core(); Y = X[core]; Gc = Y @ Y.T; n = len(core)
    vals = np.unique(np.round(Gc[np.triu_indices(n, 1)], 4)); col = np.searchsorted(vals, np.round(Gc, 4)); np.fill_diagonal(col, -1)
    K = len(vals); gnum = np.array([Gc[col == k].mean() for k in range(K)])
    P = automorphisms(col)
    orders = collections.Counter(elem_order(p) for p in P)
    rep.update(core=n, rattlers=len(ratt), distinct_values=K, group_order=len(P), element_orders=dict(sorted(orders.items())))
    assert len(P) == 120 and orders == {1: 1, 2: 25, 3: 20, 4: 30, 5: 24, 6: 20}, "not S5"
    cls = {(1, n): 'e', (2, 7): 't', (2, 13): 'dt', (3, 9): 'c3', (4, 5): 'c4', (5, 2): 'c5', (6, 1): 'c6'}
    key = [cls[(elem_order(p), int((p == np.arange(n)).sum()))] for p in P]
    Pm = [np.eye(n, dtype=np.int64)[p] for p in P]
    S = {nm: sum(chi[k]*M for k, M in zip(key, Pm)) for nm, chi in CHARS.items()}
    A = [(col == k).astype(np.int64) for k in range(K)]
    # exact linear relations from the absent isotypic components
    eqs = set()
    for nm in ("4p", "5", "6"):
        Ms = [Ak @ S[nm] for Ak in A]
        for i in range(n):
            for j in range(n):
                row = tuple(int(Mk[i, j]) for Mk in Ms) + (int(S[nm][i, j]),)
                if any(row):
                    gcd = np.gcd.reduce([abs(v) for v in row if v]); row = tuple(v//gcd for v in row)
                    if row[next(i for i, v in enumerate(row) if v)] < 0: row = tuple(-v for v in row)
                    eqs.add(row)
    R, piv = sp.Matrix([list(r) for r in eqs]).rref()
    g = sp.symbols('g0:%d' % K)
    rep["linear_relations"] = [str(sp.expand(sum(R[r, k]*g[k] for k in range(K)) + R[r, K])) + " = 0" for r in range(len(piv))]
    # high-precision solve of the rank conditions (unknowns g0, g3, g4, g6, g7, mu)
    mp.mp.dps = 90
    targets = {'1': 3, 'sgn': 1, '4': 4, '5p': 5}
    Bmp = {nm: mp.matrix(sp.Matrix.hstack(*sp.Matrix(S[nm]).columnspace()).tolist()) for nm in targets}
    Wih = {}
    for nm, V in Bmp.items():
        Lw, Uw = mp.eigsy(V.T*V); Wih[nm] = Uw*mp.diag([1/mp.sqrt(v) for v in Lw])*Uw.T
    Amp = [mp.matrix(a.tolist()) for a in A]
    def gfull(z):
        gg = [None]*K
        for i, k in enumerate([0, 3, 4, 6, 7]): gg[k] = z[i]
        mu = z[5]; gg[8] = mu; gg[1] = 2*mu - 1; gg[2] = (5*mu - 2)/3; gg[5] = (4*mu - 1)/3
        return gg
    def resid(z):
        G = mp.eye(n)
        for k, v in enumerate(gfull(z)): G += v*Amp[k]
        r = []
        for nm, t in targets.items():
            V = Bmp[nm]; Lb, _ = mp.eigsy(Wih[nm]*(V.T*G*V)*Wih[nm]); r += sorted(Lb, key=abs)[:V.cols - t]
        return r
    z = [mp.mpf(gnum[k]) for k in (0, 3, 4, 6, 7, 8)]
    for _ in range(6):
        r = mp.matrix(resid(z)); h = mp.mpf(10)**-45; J = mp.matrix(len(r), 6)
        for j in range(6):
            y = list(z); y[j] += h; J[:, j] = (mp.matrix(resid(y)) - r)/h
        U, Sv, Vt = mp.svd_r(J)
        dx = -(Vt.T*mp.diag([1/s if s > mp.mpf(10)**-30 else 0 for s in Sv])*(U.T*r)); z = [z[j] + dx[j] for j in range(6)]
    print("newton residual", mp.nstr(mp.norm(mp.matrix(resid(z))), 3), "mu", mp.nstr(z[5], 45), flush=True)
    rep["newton_residual"] = mp.nstr(mp.norm(mp.matrix(resid(z))), 3); rep["jacobian_min_singular_value"] = mp.nstr(min(Sv), 4)
    ghp = gfull(z); mu = z[5]
    mp.mp.dps = 45                     # identification precision (the solve is accurate to about 1e-42)
    ghp = [+v for v in ghp]; mu = +mu
    poly = mp.findpoly(mu, 4, maxcoeff=10**6, tol=mp.mpf(10)**-36)
    x = sp.symbols('x'); q = sp.Poly([int(c) for c in poly], x)
    if q.LC() < 0: q = -q
    rep["minimal_polynomial"] = str(q.as_expr()); rep["irreducible"] = bool(q.is_irreducible)
    # refine the other unknowns at the exact root (mu fixed), then identify each value in Q(mu)
    mp.mp.dps = 90
    qc = [int(c) for c in q.all_coeffs()]
    mu = mp.findroot(lambda t: sum(c*t**(len(qc) - 1 - i) for i, c in enumerate(qc)), mp.mpf(str(z[5])))
    w = [mp.mpf(str(v)) for v in z[:5]]
    for _ in range(4):
        r = mp.matrix(resid(w + [mu])); h = mp.mpf(10)**-45; J = mp.matrix(len(r), 5)
        for j in range(5):
            y = list(w); y[j] += h; J[:, j] = (mp.matrix(resid(y + [mu])) - r)/h
        U, Sv, Vt = mp.svd_r(J)
        dx = -(Vt.T*mp.diag([1/s_ if s_ > mp.mpf(10)**-30 else 0 for s_ in Sv])*(U.T*r)); w = [w[j] + dx[j] for j in range(5)]
    rep["fixed_mu_residual"] = mp.nstr(mp.norm(mp.matrix(resid(w + [mu]))), 3)
    ghp = gfull(w + [mu])
    mp.mp.dps = 60
    basis = [mp.mpf(1), +mu, mu**2, mu**3]; exact = []
    for v in ghp:
        rel = mp.pslq([+v] + basis, maxcoeff=10**8, maxsteps=10**6, tol=mp.mpf(10)**-40)
        if rel is None: raise RuntimeError(f"PSLQ failed for {mp.nstr(v, 30)}")
        exact.append(sum(sp.Rational(-c, rel[0])*x**i for i, c in enumerate(rel[1:])))
    rep["gram_values_in_Q(mu)"] = [str(e) for e in exact]
    # exact rank over Q(mu)
    root = [rt for rt in sp.Poly(q, x).all_roots() if abs(sp.N(rt) - float(mu)) < 1e-9][0]
    F = sp.QQ.algebraic_field(root); el = [F.from_sympy(e.subs(x, root)) for e in exact]
    M = DomainMatrix([[F.one if i == j else el[col[i, j]] for j in range(n)] for i in range(n)], (n, n), F)
    rep["exact_rank"] = int(M.rank())
    # PSD and coordinates at 60 digits
    mp.mp.dps = 60
    mu60 = mp.findroot(lambda t: sum(int(c)*t**(4 - i) for i, c in enumerate(q.all_coeffs())), mp.mpf(str(mu)))
    gv = [sp.lambdify(x, e, "mpmath")(mu60) for e in exact]
    G = mp.eye(n)
    for k in range(K): G += gv[k]*mp.matrix(A[k].tolist())
    Lg, Ug = mp.eigsy(G)
    nz = [i for i in range(n) if abs(Lg[i]) > mp.mpf(10)**-30]
    rep["nonzero_eigenvalues"] = len(nz); rep["min_nonzero_eigenvalue"] = mp.nstr(min(Lg[i] for i in nz), 8)
    rep["max_other_gram_value"] = mp.nstr(max(gv[:8]), 10); rep["mu"] = mp.nstr(mu60, 50)
    assert rep["exact_rank"] == 13 and len(nz) == 13 and min(Lg[i] for i in nz) > 1 and max(gv[:8]) < mu60
    Yhp = [[Ug[r, i]*mp.sqrt(Lg[i]) for i in nz] for r in range(n)]
    # re-attach rattlers
    Yf = np.array([[float(v) for v in row] for row in Yhp])
    Uq, _, Vq = np.linalg.svd(X[core].T @ Yf); Rt = X[ratt] @ (Uq @ Vq)
    def obj(v):
        Pp = v.reshape(-1, 13); Pp = Pp/np.linalg.norm(Pp, axis=1, keepdims=True)
        ips = np.concatenate([(Pp @ Yf.T).ravel(), [Pp[0] @ Pp[1]]]); return np.log(np.exp(200*ips).sum())/200
    Rt = minimize(obj, Rt.ravel(), method="L-BFGS-B").x.reshape(-1, 13); Rt /= np.linalg.norm(Rt, axis=1, keepdims=True)
    def tomp(v):
        w = [mp.mpf(repr(float(t))) for t in v]; s = mp.sqrt(mp.fsum(t*t for t in w)); return [t/s for t in w]
    Rmp = [tomp(r) for r in Rt]
    for N, pts in ((57, Yhp), (58, Yhp + Rmp[:1]), (59, Yhp + Rmp)):
        m = max(mp.fsum(a*b for a, b in zip(pts[i], pts[j])) for i in range(N) for j in range(i + 1, N))
        rep[f"mu_{N}"] = mp.nstr(m, 40)
        (OUT / f"exact_13_{N}.txt").write_text("\n".join(",".join(mp.nstr(t, 40) for t in p) for p in pts) + "\n")
    (OUT / "report.json").write_text(json.dumps(rep, indent=2))
    print(json.dumps(rep, indent=2))


if __name__ == "__main__":
    main()
