"""Spherical codes: basin-hopping search against Henry Cohn's table (spherical-codes.org). No novelty claim for the method.

Objective: for N unit vectors in R^d, minimise mu = max_{i<j} <x_i, x_j> (cosine of the minimal angle).
Start from the table's current coordinates (downloaded live). LP-polish them, then basin-hop: perturb or re-seed a few
points, minimise a log-sum-exp smoothing of mu with L-BFGS at increasing sharpness, and LP-polish near-best results
(trust-region sequential LP on the near-active pairs). The HiGHS time limit and LP deadlines avoid hangs on
highly degenerate codes.

    python 56_spherical_code_search.py targets.json <seconds per entry> <worker id> <n workers>
"""
import sys, time, json, urllib.request, numpy as np
from scipy.optimize import minimize, linprog
from scipy.sparse import coo_matrix
W = str(__import__("pathlib").Path(__file__).resolve().parent / "results" / "spherical_codes" / "search")

def fetch(d, N):
    with urllib.request.urlopen(f"https://spherical-codes.org/data/{d}/{N}", timeout=60) as r:
        return np.array([[float(x) for x in l.split(",")] for l in r.read().decode().strip().splitlines()])

def make(N, d):
    iu = np.triu_indices(N, 1)
    def mu(X): return (X @ X.T)[iu].max()
    def lse(v, beta):
        X = v.reshape(N, d); nr = np.linalg.norm(X, axis=1, keepdims=True); Y = X/nr
        g = (Y @ Y.T)[iu]; m = g.max(); w = np.exp(beta*(g - m)); S = w.sum()
        Wm = np.zeros((N, N)); Wm[iu] = w/S; Wm = Wm + Wm.T
        gY = Wm @ Y; gX = (gY - np.sum(gY*Y, axis=1, keepdims=True)*Y)/nr
        return m + np.log(S)/beta, gX.ravel()
    def lp(X, iters=60, rho=1e-3, deadline=None):
        for _ in range(iters):
            if deadline is not None and time.time() > deadline: break
            G = X @ X.T; np.fill_diagonal(G, -2); m = G.max()
            I, J = np.nonzero(np.triu(G > m - max(4*rho, 1e-10), 1)); K = len(I)
            if K > 4000:
                o = np.argsort(-G[I, J])[:4000]; I, J = I[o], J[o]; K = 4000
            r = np.repeat(np.arange(K), 2*d + 1)
            cols = np.hstack([I[:, None]*d + np.arange(d), J[:, None]*d + np.arange(d), np.full((K, 1), N*d)]).ravel()
            gi = X[J] - G[I, J][:, None]*X[I]; gj = X[I] - G[I, J][:, None]*X[J]   # tangent-projected gradients
            A = coo_matrix((np.hstack([gi, gj, -np.ones((K, 1))]).ravel(), (r, cols)), shape=(K, N*d + 1)).tocsr()
            c = np.zeros(N*d + 1); c[-1] = 1
            res = linprog(c, A_ub=A, b_ub=-G[I, J], bounds=[(-rho, rho)]*(N*d) + [(None, None)], method="highs", options={"time_limit": 10.0})
            if res.status != 0: rho /= 2; continue
            Y = X + res.x[:-1].reshape(N, d); Y /= np.linalg.norm(Y, axis=1, keepdims=True)
            if mu(Y) < m: X = Y; rho = min(rho*2, 1e-2)
            else: rho /= 4
            if rho < 1e-13: break
        return X
    return mu, lse, lp

def run(d, N, T, seed):
    rng = np.random.default_rng(seed)
    X0 = fetch(d, N); X0 /= np.linalg.norm(X0, axis=1, keepdims=True)
    mu, lse, lp = make(N, d)
    rec = mu(X0); best = lp(X0.copy(), iters=15, deadline=time.time() + T/2); mb = mu(best); polish_gain = rec - mb
    t0 = time.time(); hops = 0
    t0 = time.time()
    while time.time() - t0 < T:
        hops += 1; sig = 10**rng.uniform(-3, -0.5)
        X = best + sig*rng.standard_normal(best.shape)
        if rng.random() < 0.3:
            idx = rng.choice(N, max(1, N//20), replace=False); X[idx] = rng.standard_normal((len(idx), d))
        X /= np.linalg.norm(X, axis=1, keepdims=True); v = X.ravel()
        for beta in (100, 1000, 10000):
            v = minimize(lse, v, args=(beta,), jac=True, method="L-BFGS-B", options={"maxiter": 200}).x
        X = v.reshape(N, d); X /= np.linalg.norm(X, axis=1, keepdims=True)
        if mu(X) < mb + 2e-5: X = lp(X, iters=40, deadline=t0 + 1.5*T)
        if mu(X) < mb - 1e-13:
            best, mb = X, mu(X)
    if mb < rec - 1e-11:
        np.savetxt(f"{W}/{d}_{N}.csv", best, delimiter=",", fmt="%.17g")
    return {"d": d, "N": N, "record": float(rec), "best": float(mb), "gain": float(rec - mb), "polish_gain": float(polish_gain), "hops": hops}

if __name__ == "__main__":
    targets = json.load(open(sys.argv[1])); T = float(sys.argv[2]); wid, nw = int(sys.argv[3]), int(sys.argv[4])
    for k, (d, N) in enumerate(targets):
        if k % nw != wid: continue
        try:
            r = run(d, N, T, 1000*d + N)
        except Exception as e:
            r = {"d": d, "N": N, "error": repr(e)}
        with open(f"{W}/results_{wid}.jsonl", "a") as f: f.write(json.dumps(r) + "\n")
