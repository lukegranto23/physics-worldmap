"""Post-hoc analytic diagnosis; does not select or change benchmark 006 tests."""
from __future__ import annotations
import hashlib
import importlib.util
import json
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("range_reference", HERE/"22_range_measurement_design.py")
ref = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ref)
SOURCE = HERE/"results"/"range_design"/"results.json"


def kl_pair(v_truth, c_truth, v_model, c_model):
    ratios = np.array([(v_truth+c_truth)/(v_model+c_model),
                       (v_truth-c_truth)/(v_model-c_model)])
    return float(.5*np.sum(ratios-1-np.log(ratios)))


def main():
    p = json.loads(ref.PROTOCOL.read_text(encoding="utf-8"))
    study = json.loads(SOURCE.read_text(encoding="utf-8"))
    models = [(a, p["decay_rate"]) for a in p["candidate_aliases"]]+ref.alternatives(p)
    v = 1+p["measurement_noise_sd"]**2
    rows = []
    for row in study["cells"]:
        s, lags = row["scenario"], row["lags"]
        actual_v = 1+s.get("noise_sd", p["measurement_noise_sd"])**2
        ds = [float(np.mean([kl_pair(actual_v, ref.ref.cov(s["alias"], t, s["decay"]),
                                    v, ref.ref.cov(a, t, d)) for t in lags])) for a, d in models]
        ni, ai = int(np.argmin(ds[:3])), 3+int(np.argmin(ds[3:]))
        rows.append({"regime": row["regime"], "reference_pairs": row["reference_pairs"],
                     "design": row["design"], "scenario": s["name"],
                     "nearest_null": models[ni], "nearest_alternative_component": models[ai],
                     "kl_truth_to_nearest_null_per_pair": ds[ni],
                     "kl_truth_to_nearest_alternative_per_pair": ds[ai],
                     "asymptotic_log_e_per_pair": ds[ni]-ds[ai]})
    a = np.array([[1.3, .2], [.2, 1.3]])
    b = np.array([[1.1, -.4], [-.4, 1.1]])
    direct = .5*(np.trace(np.linalg.solve(b, a))-2+
                 np.linalg.slogdet(b)[1]-np.linalg.slogdet(a)[1])
    errors = {"same_distribution_zero_kl": abs(kl_pair(1.1, .3, 1.1, .3)),
              "unequal_variance_matrix_kl": abs(direct-kl_pair(1.3, .2, 1.1, -.4)),
              "nominal_null_has_zero_min_kl": max(
                  abs(r["kl_truth_to_nearest_null_per_pair"]) for r in rows if r["scenario"].startswith("null_"))}
    report = {
        "analysis_type": "post-hoc explanatory diagnostics, added after benchmark outcomes; no retuning",
        "source_results_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "protocol_sha256": study["protocol_sha256"],
        "definition": "For fixed positive finite mixture weights and fixed lag proportions, log e_N/N tends almost surely to min_j D(Ptruth||Pnull_j)-min_k D(Ptruth||Palt_k). Distances per pair average over scheduled lags.",
        "limits": "Asymptotic growth is not finite-sample detection probability. A negative limit implies power tends to zero; positive implies power tends to one at a fixed threshold. Zero is inconclusive. Nominal false-alarm control remains distinct from power.",
        "checks": {name: {"error": float(error), "tolerance": 1e-9, "passed": bool(error < 1e-9)}
                   for name, error in errors.items()}, "cells": rows}
    report["all_checks_passed"] = all(c["passed"] for c in report["checks"].values())
    (SOURCE.parent/"posthoc_diagnostics.json").write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({"checks": report["checks"], "selected_diagnostics": [
        r for r in rows if r["regime"] == "readings" and r["reference_pairs"] == 1024 and
        ((r["design"] == "local_fisher" and r["scenario"] == "minus_16pct") or
         (r["design"] == "range_maximin" and r["scenario"] in ("damping_only_low", "damping_only_high")))]}, indent=2))
    assert report["all_checks_passed"]


if __name__ == "__main__":
    main()
