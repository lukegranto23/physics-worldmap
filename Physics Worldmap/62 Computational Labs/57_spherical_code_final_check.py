"""Lab 57: independent final check of lab 56 candidates.
The max inner product uses a float64 screen, then 50-digit evaluation of every pair within 1e-9 of the max. Each candidate is compared with the live
table value at the time of checking and must be strictly better after rounding up to 12 decimals (the table's displayed precision). It also tries N-1 by deleting a point."""

import os, sys, glob, json, re, urllib.request, numpy as np, mpmath as mp
import importlib.util
_s = importlib.util.spec_from_file_location("lab56", __import__("pathlib").Path(__file__).resolve().parent / "56_spherical_code_search.py")
_m = importlib.util.module_from_spec(_s); _s.loader.exec_module(_m); make = _m.make
mp.mp.dps = 50
OUT = str(__import__("pathlib").Path(__file__).resolve().parent / "results" / "spherical_codes" / "codes")
def live_mu(d, N):
    try:
        with urllib.request.urlopen(f"https://spherical-codes.org/data/{d}/{N}", timeout=60) as r:
            X = np.array([[float(x) for x in l.split(",")] for l in r.read().decode().strip().splitlines()])
    except Exception:
        return None
    return mu50(X)
def mu50(X):
    """Exact-enough max inner product: float64 screen, then 50-digit evaluation of every pair within 1e-9 of the float max."""
    X = np.asarray(X, float)
    V = [[mp.mpf(repr(float(x))) for x in row] for row in X]
    V = [[x/mp.sqrt(mp.fsum(y*y for y in v)) for x in v] for v in V]
    Xn = X/np.linalg.norm(X, axis=1, keepdims=True); G = Xn @ Xn.T; np.fill_diagonal(G, -2)
    I, J = np.nonzero(np.triu(G > G.max() - 1e-9, 1))
    return max(mp.fsum(a*c for a, c in zip(V[i], V[j])) for i, j in zip(I, J))
def ceil12(x): return mp.ceil(x*10**12)/10**12
def check(d, N, X, tag):
    m = mu50(X); rec = live_mu(d, N)
    ok = rec is not None and ceil12(m) < ceil12(rec)
    row = {"d": d, "N": N, "src": tag, "mu50": mp.nstr(m, 20), "live_record": mp.nstr(rec, 15) if rec is not None else None,
           "improves_at_12dp": bool(ok), "gain": float(rec - m) if rec is not None else None}
    p = f"{OUT}/sc_{d}_{N}.txt"
    if ok and os.path.exists(p) and mu50(np.loadtxt(p, delimiter=",")) <= m:
        ok_save = False
    else:
        ok_save = ok
    if ok_save:
        np.savetxt(f"{OUT}/sc_{d}_{N}.txt", X/np.linalg.norm(X, axis=1, keepdims=True), delimiter=",", fmt="%.17g")
    return row
if __name__ == "__main__":
    import os; os.makedirs(OUT, exist_ok=True)
    rows = []
    for f in sorted(glob.glob(str(__import__("pathlib").Path(__file__).resolve().parent / "results" / "spherical_codes" / "search" / "[0-9]*_[0-9]*.csv"))):
        d, N = map(int, re.findall(r"(\d+)_(\d+)\.csv", f)[0])
        X = np.loadtxt(f, delimiter=","); X /= np.linalg.norm(X, axis=1, keepdims=True)
        assert X.shape == (N, d), (f, X.shape)
        rows.append(check(d, N, X, f))
        # N-1 cascade
        mu, lse, lp = make(N - 1, d)
        G = X @ X.T; np.fill_diagonal(G, -2)
        best = None
        for k in np.argsort(-G.max(axis=1))[:3]:
            Y = lp(np.delete(X, k, axis=0), iters=20, deadline=__import__('time').time() + 60)
            if best is None or mu(Y) < mu(best): best = Y
        if 2*d < N - 1:
            rows.append(check(d, N - 1, best, f + " minus one point"))
        print(json.dumps(rows[-2]), "\n", json.dumps(rows[-1]), flush=True)
    json.dump(rows, open(f"{OUT}/summary.json", "w"), indent=1)
