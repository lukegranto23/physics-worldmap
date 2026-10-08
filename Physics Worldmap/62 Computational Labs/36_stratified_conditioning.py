"""Stage-2 stratified test of variance heterogeneity in conditioned moments; no novelty claim.

    python 36_stratified_conditioning.py --selftest
    python 36_stratified_conditioning.py --data <dir with Dryad files>
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
PROTOCOL = HERE / "stratified_conditioning_protocol.json"
OUT = HERE / "results" / "stratified_conditioning"
spec = importlib.util.spec_from_file_location("lab34", HERE / "34_conditioned_displacement_reproduction.py")
lab34 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lab34)


def sha256(path):
    with Path(path).open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def segment_table(Ys, Ws, lags, seg):
    """Per-segment sums over test-half start indices: counts, moments, and both proxies."""
    rows = []
    kmax = max(lags)
    for tr, (Y, W) in enumerate(zip(Ys, Ws)):
        lo, hi = len(Y)//2, len(Y) - kmax
        for a in range(lo, hi - seg + 1, seg):
            j = np.arange(a, a + seg)
            D = np.stack([Y[j + k] - Y[j] for k in lags])
            d4 = np.diff(Y[a:a + seg + 4], 4)
            rows.append({"trace": tr, "W": W[j], "D": D, "proxy_varW": float(np.var(W[j])),
                         "proxy_d4": float(np.mean(d4**2)/70)})
    return rows


def evaluate(rows, labels, nstrata, b, muW, muD):
    obs_num = 0.0
    obs_den = 0.0
    pred_num = 0.0
    for s in range(nstrata):
        group = [r for r, l in zip(rows, labels) if l == s]
        if not group:
            continue
        W = np.concatenate([g["W"] for g in group]) - muW
        D = np.concatenate([g["D"] for g in group], axis=1) - muD[:, None]
        sv = np.mean(W**2)
        u = np.mean(D**2, axis=1)
        r = np.mean(D*W, axis=1)
        sel = np.abs(W) <= b
        n = sel.sum()
        if n == 0:
            continue
        pred = u - r**2/sv + r**2/sv**2*lab34.m2_truncated(b, sv)
        obs_num = obs_num + np.sum(D[:, sel]**2, axis=1)
        obs_den += n
        pred_num = pred_num + n*pred
    obs = obs_num/obs_den
    pred = pred_num/obs_den
    return obs, pred, (obs - pred)/np.abs(pred)


def quartile_labels(rows, proxy):
    v = np.array([r[proxy] for r in rows])
    edges = np.quantile(v, [.25, .5, .75])
    return np.searchsorted(edges, v)


def analyse(Ys, Ws, P, label):
    d = P["design"]
    lags = d["lags_samples"]
    out = {}
    for seg in [d["segments_samples"]] + d["segment_sensitivity"]:
        rows = segment_table(Ys, Ws, lags, seg)
        W_all = np.concatenate([r["W"] for r in rows])
        muW = W_all.mean()
        muD = np.concatenate([r["D"] for r in rows], axis=1).mean(axis=1)
        sd = np.sqrt(np.mean((W_all - muW)**2))
        res = {}
        for frac in [d["bin_fractions"]["primary"]] + d["bin_fractions"]["secondary"]:
            b = frac*sd
            base = evaluate(rows, np.zeros(len(rows), int), 1, b, muW, muD)
            entry = {"unstratified_mean_rel": float(base[2].mean()), "unstratified_rel": base[2].tolist()}
            for proxy in ("proxy_varW", "proxy_d4"):
                lab = quartile_labels(rows, proxy)
                st = evaluate(rows, lab, 4, b, muW, muD)
                perm = np.random.default_rng(2026100621).permutation(lab)
                pl = evaluate(rows, perm, 4, b, muW, muD)
                entry[proxy] = {"stratified_mean_rel": float(st[2].mean()), "stratified_rel": st[2].tolist(),
                                "placebo_mean_rel": float(pl[2].mean())}
            if seg == d["segments_samples"] and frac == d["bin_fractions"]["primary"]:
                rng = np.random.default_rng(2026100622)
                by_trace = {}
                for i, r in enumerate(rows):
                    by_trace.setdefault(r["trace"], []).append(i)
                lab = quartile_labels(rows, "proxy_varW")
                boots_u, boots_s = [], []
                for _ in range(300):
                    idx = np.concatenate([rng.choice(v, len(v)) for v in by_trace.values()])
                    sub = [rows[i] for i in idx]
                    boots_u.append(evaluate(sub, np.zeros(len(sub), int), 1, b, muW, muD)[2].mean())
                    boots_s.append(evaluate(sub, lab[idx], 4, b, muW, muD)[2].mean())
                entry["bootstrap_se"] = {"unstratified": float(np.std(boots_u, ddof=1)),
                                         "stratified_varW": float(np.std(boots_s, ddof=1)),
                                         "difference": float(np.std(np.array(boots_s) - np.array(boots_u), ddof=1))}
            res[str(frac)] = entry
        quart_var = np.array([r["proxy_varW"] for r in rows])
        res["proxy_spread_varW_q90_over_q10"] = float(np.quantile(quart_var, .9)/np.quantile(quart_var, .1))
        out[str(seg)] = res
    prim = out[str(d["segments_samples"])][str(d["bin_fractions"]["primary"])]
    eu = prim["unstratified_mean_rel"]
    es = prim["proxy_varW"]["stratified_mean_rel"]
    ep = prim["proxy_varW"]["placebo_mean_rel"]
    if abs(es) <= .5*abs(eu) and abs(ep) >= .75*abs(eu):
        verdict = "SUPPORTED"
    elif abs(es) > .75*abs(eu):
        verdict = "NOT SUPPORTED"
    else:
        verdict = "PARTIAL"
    return {"label": label, "verdict": verdict, "e_unstrat": eu, "e_strat": es, "e_placebo": ep, "detail": out}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--selftest", action="store_true")
    group.add_argument("--data", type=Path)
    args = parser.parse_args()
    P = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    P34 = json.loads(lab34.PROTOCOL.read_text(encoding="utf-8"))
    meta = {"generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "protocol_sha256": sha256(PROTOCOL), "script_sha256": sha256(__file__)}
    runs = []
    if args.selftest:
        seed = P34["selftest"]["seed"]
        for label, mod in (("selftest_positive", False), ("selftest_negative", True)):
            runs.append(analyse(*lab34.synthetic(P34, mod, seed + int(mod)), P, label))
        pos, neg = runs
        meta["self_tests_pass"] = bool(abs(pos["e_strat"] - pos["e_unstrat"]) < .01 and abs(neg["e_strat"]) <= .5*abs(neg["e_unstrat"]))
        out_dir = OUT / "selftest"
    else:
        for name, expected in P34["target"]["files_sha256"].items():
            if sha256(args.data / name) != expected:
                raise lab34.GateFailure(f"{name}: digest mismatch")
        st = json.loads((OUT / "selftest" / "results.json").read_text(encoding="utf-8"))
        meta["self_tests_pass"] = st["meta"]["self_tests_pass"]
        for pair in P34["target"]["pairs"]:
            Ys, _ = lab34.load_traces(args.data / pair["position"])
            Ws, _ = lab34.load_traces(args.data / pair["velocity"])
            r = analyse(Ys, Ws, P, pair["role"])
            if not meta["self_tests_pass"]:
                r["verdict"] = "NOT INTERPRETABLE (self-test failed)"
            runs.append(r)
        out_dir = OUT / "dryad_v3"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "results.json").write_text(json.dumps(lab34.to_jsonable({"meta": meta, "runs": runs}), indent=2), encoding="utf-8")
    for r in runs:
        print(f"{r['label']:>20}: {r['verdict']:<14} e_unstrat={r['e_unstrat']:+.4f} e_strat={r['e_strat']:+.4f} e_placebo={r['e_placebo']:+.4f}")
    print("self-tests pass:", meta["self_tests_pass"])


if __name__ == "__main__":
    main()
