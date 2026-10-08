"""Post hoc audit of lab 36: does stratifying on segment Var(W) move the error without heterogeneity? No novelty claim.

Lab 36's stationary positive control changed the mean signed relative error by
0.0068 under Var(W) stratification (paired bootstrap SE 0.0009), close to the
0.0100 particle shift that produced its SUPPORTED verdict. This audit repeats
the stationary control over fresh seeds and segment lengths for both proxies.
No real data is read.

    python 37_stratification_artifact_audit.py
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
OUT = HERE / "results" / "stratification_artifact_audit"


def load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


lab34 = load("lab34", "34_conditioned_displacement_reproduction.py")
lab36 = load("lab36", "36_stratified_conditioning.py")
SEEDS = list(range(2026100801, 2026100809))   # fresh, not used by labs 34 or 36
SEGMENTS = [1000, 2000, 8000]
BIN = 0.05


def shifts(Ys, Ws, lags, seg):
    rows = lab36.segment_table(Ys, Ws, lags, seg)
    W_all = np.concatenate([r["W"] for r in rows])
    muW = W_all.mean()
    muD = np.concatenate([r["D"] for r in rows], axis=1).mean(axis=1)
    b = BIN*np.sqrt(np.mean((W_all - muW)**2))
    e0 = lab36.evaluate(rows, np.zeros(len(rows), int), 1, b, muW, muD)[2].mean()
    out = {"unstratified": float(e0)}
    for proxy in ("proxy_varW", "proxy_d4"):
        e = lab36.evaluate(rows, lab36.quartile_labels(rows, proxy), 4, b, muW, muD)[2].mean()
        out[proxy] = float(e - e0)
    return out


def main():
    P36 = json.loads(lab36.PROTOCOL.read_text(encoding="utf-8"))
    P34 = json.loads(lab34.PROTOCOL.read_text(encoding="utf-8"))
    lags = P36["design"]["lags_samples"]
    runs = []
    for seed in SEEDS:
        Ys, Ws = lab34.synthetic(P34, False, seed)
        runs.append({"seed": seed, **{str(seg): shifts(Ys, Ws, lags, seg) for seg in SEGMENTS}})
        print(seed, {seg: {k: round(v, 4) for k, v in runs[-1][str(seg)].items()} for seg in SEGMENTS}, flush=True)
    summary = {}
    for seg in SEGMENTS:
        summary[str(seg)] = {}
        for proxy in ("proxy_varW", "proxy_d4"):
            v = np.array([r[str(seg)][proxy] for r in runs])
            summary[str(seg)][proxy] = {"mean_shift": float(v.mean()), "sd": float(v.std(ddof=1)),
                                        "se_of_mean": float(v.std(ddof=1)/np.sqrt(len(v))),
                                        "min": float(v.min()), "max": float(v.max())}
    real = json.loads((HERE / "results" / "stratified_conditioning" / "dryad_v3" / "results.json").read_text(encoding="utf-8"))
    observed = {}
    for r in real["runs"]:
        observed[r["label"]] = {}
        for seg in SEGMENTS:
            e = r["detail"][str(seg)][str(BIN)]
            observed[r["label"]][str(seg)] = {
                "unstratified": e["unstratified_mean_rel"],
                **{p: e[p]["stratified_mean_rel"] - e["unstratified_mean_rel"] for p in ("proxy_varW", "proxy_d4")}}
    # Post hoc reading: lab 36's decision rule applied to the proxy whose stationary shift is consistent with zero.
    d4_rule = {}
    for label, row in observed.items():
        eu = row["2000"]["unstratified"]
        es = eu + row["2000"]["proxy_d4"]
        d4_rule[label] = ("SUPPORTED" if abs(es) <= .5*abs(eu) else "NOT SUPPORTED" if abs(es) > .75*abs(eu) else "PARTIAL")
    out = {"meta": {"generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                    "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                    "lab36_results_sha256": hashlib.sha256((HERE / "results" / "stratified_conditioning" / "dryad_v3" / "results.json").read_bytes()).hexdigest(),
                    "status": "post hoc; synthetic stationary data only; real-data numbers are read from lab 36's saved results"},
           "bin_fraction": BIN, "stationary_runs": runs, "stationary_summary": summary,
           "lab36_observed_shifts": observed, "post_hoc_d4_rule_verdicts": d4_rule}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "results.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps({"stationary_summary": summary, "observed": observed, "d4_rule": d4_rule}, indent=1))


if __name__ == "__main__":
    main()
