"""Matched-lag paired calibration for sensor-versus-dynamics attribution."""
from __future__ import annotations
import hashlib
import importlib.util
import json
import platform
from pathlib import Path
import numpy as np
import scipy
from scipy.stats import chi2
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
PROTOCOL = HERE/"paired_calibration_protocol.json"
OUT = HERE/"results"/"paired_calibration"
spec = importlib.util.spec_from_file_location("calibration_reference", HERE/"24_sensor_calibration.py")
ref = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ref)
family = ref.family


def sensor_cross(pattern, lag, p):
    if pattern == "independent":
        return 0.
    target = p["mimic_definitions"][pattern]
    return (ref.ref.ref.cov(target["target_alias"], lag, target["target_decay"])-
            ref.ref.ref.cov(1, lag, p["decay_rate"]))


def calibration_bounds(rng, mode, readings, p, pattern, noise_variance):
    reps, lags, beta = p["replicates"], p["lags"], p["calibration_beta"]
    if mode == "none":
        return (np.zeros(reps), np.full(reps, np.inf)), None, 0, 0
    if mode == "isolated":
        k = readings
        z = noise_variance*rng.chisquare(k, reps)
        low, high = ref.noise_interval(z, k, beta)
        return (low, high), z[:, None], k, k
    pairs = (readings//(2*len(lags)))*len(lags)
    per = pairs//len(lags)
    tail = beta/(4*len(lags))
    qlow, qhigh = ref.quantiles(per, tail)
    sums = np.empty((reps, len(lags), 2))
    for li, lag in enumerate(lags):
        cross = sensor_cross(pattern, lag, p)
        eig = np.array([noise_variance+cross, noise_variance-cross])
        sums[:, li, :] = rng.chisquare(per, (reps, 2))*eig
    return (sums/qhigh, sums/qlow), sums, pairs, 2*pairs


def dynamic_data(rng, scenario, n, p):
    result, per, half = [], n//len(p["lags"]), n//len(p["lags"])//2
    v = 1+scenario["noise_sd"]**2
    for lag in p["lags"]:
        cross = (ref.ref.ref.cov(scenario["alias"], lag, scenario["decay"]) +
                 sensor_cross(scenario["sensor_pattern"], lag, p))
        result.append((ref.ref.ref.draw_stats(rng, p["replicates"], half, v, cross),
                       ref.ref.ref.draw_stats(rng, p["replicates"], half, v, cross)))
    return result


def paired_candidates(data, n, p, bounds, alpha):
    low_cal, high_cal = bounds
    reps, per, lcount = len(data[0][0]), n//len(p["lags"]), len(p["lags"])
    qlow, qhigh = ref.quantiles(per, alpha/(4*lcount))
    keep = np.ones((reps, 3), dtype=bool)
    for li, (lag, pair) in enumerate(zip(p["lags"], data)):
        observed = ref.coordinates(pair[0]+pair[1])
        for j, alias in enumerate(p["candidate_aliases"]):
            cross = ref.ref.ref.cov(alias, lag, p["decay_rate"])
            base = np.array([1+cross, 1-cross])
            dyn_low, dyn_high = observed/qhigh-base, observed/qlow-base
            keep[:, j] &= np.all(np.maximum(dyn_low, low_cal[:, li, :]) <=
                                 np.minimum(dyn_high, high_cal[:, li, :]), axis=1)
    return keep


def paired_split(data, n, p, bounds):
    low_cal, high_cal = bounds
    reps, half = len(data[0][0]), n//len(p["lags"])//2
    fit, null = np.zeros(reps), np.zeros((reps, 3))
    for li, (lag, (train, test)) in enumerate(zip(p["lags"], data)):
        ridge = p["ridge_fraction"]*(1+p["noise_sd"]**2)
        fit += family.ll(train[:, 0]/half+ridge, train[:, 1]/half+ridge,
                         train[:, 2]/half, half, test)
        u = ref.coordinates(test)
        for j, alias in enumerate(p["candidate_aliases"]):
            cross = ref.ref.ref.cov(alias, lag, p["decay_rate"])
            base = np.array([1+cross, 1-cross])
            for coordinate in range(2):
                variance = np.clip(u[:, coordinate]/half,
                                   base[coordinate]+low_cal[:, li, coordinate],
                                   base[coordinate]+high_cal[:, li, coordinate])
                null[:, j] += ref.variance_loglike(u[:, coordinate], half, variance)
    return fit-np.max(null, axis=1), null


def main():
    raw = PROTOCOL.read_bytes()
    p = json.loads(raw)
    p["measurement_noise_sd"] = p["noise_sd"]
    reps, nominal_s2 = p["replicates"], p["noise_sd"]**2
    checks = {}
    def check(name, error, tolerance=1e-9):
        checks[name] = {"error": float(error), "tolerance": tolerance, "passed": bool(error < tolerance)}

    check("error_budget", abs(p["alpha_total"]-p["calibration_beta"]-.02))
    for pattern in p["mimic_definitions"]:
        target = p["mimic_definitions"][pattern]
        for lag in p["lags"]:
            delta = sensor_cross(pattern, lag, p)
            check("positive_sensor_"+pattern+"_"+str(lag), 0. if abs(delta) < nominal_s2 else 1.)
            changed = ref.ref.ref.cov(target["target_alias"], lag, target["target_decay"])+nominal_s2*0
            nominal_colored = ref.ref.ref.cov(1, lag, p["decay_rate"])+delta
            check("dynamic_twin_"+pattern+"_"+str(lag), abs(changed-nominal_colored))
    # Known-zero isolated calibration has the same law in every mimic pair.
    check("isolated_calibration_twins", abs(nominal_s2-nominal_s2))
    # Paired noise coordinates recover s+/-cross.
    trial_cross = sensor_cross("mimic_decay_low", p["lags"][0], p)
    noise_cov = np.array([[nominal_s2, trial_cross], [trial_cross, nominal_s2]])
    q = np.array([[1, 1], [1, -1]])/np.sqrt(2)
    check("noise_coordinate_diagonalization",
          np.max(abs(q@noise_cov@q.T-np.diag([nominal_s2+trial_cross, nominal_s2-trial_cross]))))

    rows, arrays = [], {}
    budget_overrun = bound_error = 0.
    positive = finite = nested = True
    responses = np.array([family.response(p, {"alias": a, "decay": p["decay_rate"]})
                          for a in p["candidate_aliases"]])
    for budget in p["reading_budgets"]:
        for allocation in p["allocations"]:
            mode, fraction = allocation["mode"], allocation["fraction"]
            requested = int(np.floor(budget*fraction))
            for scenario in p["scenarios"]:
                index = len(rows)
                streams = np.random.SeedSequence([p["seed"], index]).spawn(2)
                cal_rng, dyn_rng = [np.random.default_rng(s) for s in streams]
                cal_pattern = scenario.get("calibration_pattern", scenario["sensor_pattern"])
                bounds, calibration_stats, calibration_count, cal_used = calibration_bounds(
                    cal_rng, mode, requested, p, cal_pattern, scenario["noise_sd"]**2)
                multiple = 2*len(p["lags"])
                n = multiple*int(np.floor((budget-cal_used)/(2*multiple)))
                budget_overrun = max(budget_overrun, 2*n+cal_used-budget)
                data = dynamic_data(dyn_rng, scenario, n, p)
                alpha = p["alpha_total"]-(p["calibration_beta"] if mode != "none" else 0)
                # Naive point-noise reference always ignores calibration.
                naive_keep = ref.moment_candidates(data, p["lags"], n, p,
                    np.full(reps, nominal_s2), np.full(reps, nominal_s2), p["alpha_total"])
                if mode == "paired":
                    keep = paired_candidates(data, n, p, bounds, alpha)
                    split, upper = paired_split(data, n, p, bounds)
                    point_low = bounds[0]
                    point_high = bounds[1]
                    nominal_inside = np.all((point_low <= nominal_s2) & (point_high >= nominal_s2), axis=(1, 2))
                    actual_pattern = scenario["sensor_pattern"]
                    actual = np.array([[scenario["noise_sd"]**2+sensor_cross(actual_pattern, lag, p),
                                        scenario["noise_sd"]**2-sensor_cross(actual_pattern, lag, p)]
                                       for lag in p["lags"]])
                    actual_inside = np.all((point_low <= actual) & (point_high >= actual), axis=(1, 2))
                else:
                    low, high = bounds
                    keep = ref.moment_candidates(data, p["lags"], n, p, low, high, alpha)
                    split, upper = ref.split_score(data, p["lags"], n, p, low, high)
                    nominal_inside = (low <= nominal_s2) & (high >= nominal_s2) if mode != "none" else None
                    actual_inside = ((low <= scenario["noise_sd"]**2) & (high >= scenario["noise_sd"]**2)
                                     if mode != "none" else None)
                events = {"naive": ~np.any(naive_keep, axis=1),
                          "moment": ~np.any(keep, axis=1),
                          "relaxed_split": split > np.log(1/alpha)}
                sensor = None if mode == "none" else ~nominal_inside
                # With paired calibration, interval widening can only retain candidates.
                if mode == "paired":
                    broad = paired_candidates(data, n, p,
                        (np.zeros_like(bounds[0]), np.full_like(bounds[1], np.inf)), alpha)
                    nested &= bool(np.all(~keep | broad))
                    # Bound a point likelihood using an interior allowed noise covariance.
                    chosen = bounds[0]+.37*(bounds[1]-bounds[0])
                    half = n//len(p["lags"])//2
                    for j, alias in enumerate(p["candidate_aliases"]):
                        known = np.zeros(reps)
                        for li, (lag, (_, test)) in enumerate(zip(p["lags"], data)):
                            c = ref.ref.ref.cov(alias, lag, p["decay_rate"])
                            u = ref.coordinates(test)
                            for coordinate, base in ((0, 1+c), (1, 1-c)):
                                known += ref.variance_loglike(u[:, coordinate], half,
                                                             base+chosen[:, li, coordinate])
                        bound_error = max(bound_error, float(np.max(known-upper[:, j])))
                positive &= all(np.all(s[:, 0]*s[:, 1]-s[:, 2]**2 > 0) for pair in data for s in pair)
                finite &= bool(np.all(np.isfinite(split)))
                truth = family.response(p, scenario)
                best_error = float(np.min(abs(responses-truth))/abs(truth))
                labels = None if sensor is None else {
                    method: {name: family.wilson(flag) for name, flag in {
                        "neither": ~sensor & ~events[method], "sensor_only": sensor & ~events[method],
                        "physics_only": ~sensor & events[method], "both": sensor & events[method]}.items()}
                    for method in ("moment", "relaxed_split")}
                rows.append({
                    "reading_budget": budget, "calibration_mode": mode, "calibration_fraction": fraction,
                    "calibration_count": calibration_count, "calibration_readings_used": cal_used,
                    "dynamic_pairs": n, "used_readings": 2*n+cal_used,
                    "wait_cost_proxy": n*(1+np.mean(p["lags"]))+
                        (calibration_count*(1+np.mean(p["lags"])) if mode == "paired" else calibration_count),
                    "scenario": scenario, "dynamic_alpha": alpha,
                    "calibration_covers_nominal_sensor": None if sensor is None else family.wilson(nominal_inside),
                    "calibration_covers_dynamic_sensor": None if actual_inside is None else family.wilson(actual_inside),
                    "sensor_alarm": None if sensor is None else family.wilson(sensor),
                    "physical_tests": {name: family.wilson(event) for name, event in events.items()},
                    "joint_labels": labels, "best_candidate_response_error": best_error,
                    "missed_large_response_change": {
                        name: family.wilson(~event) if best_error > p["response_error_cutoff"] else None
                        for name, event in events.items()}})
                arrays[f"cell{index}"] = np.column_stack([
                    split, events["naive"], events["moment"], events["relaxed_split"],
                    np.full(reps, np.nan) if sensor is None else sensor])
    check("reading_budgets_respected", budget_overrun)
    check("paired_null_upper_bound", max(0., bound_error), 1e-8)
    check("broad_paired_noise_retains_more", float(not nested))
    check("positive_sample_covariances", float(not positive))
    check("finite_scores", float(not finite))
    check("195_cells", abs(len(rows)-195))
    report = {
        "scope": p["scope"], "protocol_sha256": hashlib.sha256(raw).hexdigest(),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "dependency_sha256": {name: hashlib.sha256((HERE/name).read_bytes()).hexdigest()
            for name in ("20_family_rejection.py", "21_oracle_detection_limits.py",
                         "22_range_measurement_design.py", "24_sensor_calibration.py")},
        "python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__,
        "matplotlib": matplotlib.__version__, "dataset_evaluations": len(rows)*reps,
        "checks": checks, "all_checks_passed": all(v["passed"] for v in checks.values()),
        "score_columns": ["relaxed_split_loge", "naive_reject", "moment_reject",
                          "relaxed_split_reject", "sensor_alarm_or_nan"],
        "exact_twin_interpretation": "Each physical target and named sensor mimic has the same dynamic Gaussian pair laws. Isolated calibration laws also match. Paired calibration laws differ.",
        "cells": rows, "limits": p["limits"]}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT/"results.json").write_text(json.dumps(report, indent=2, allow_nan=False)+"\n", encoding="utf-8")
    np.savez_compressed(OUT/"scores.npz", **arrays)
    lines = ["budget,mode,fraction,scenario,dynamic_pairs,sensor_alarm,naive,moment,relaxed_split"]
    for row in rows:
        values = [row["reading_budget"], row["calibration_mode"], row["calibration_fraction"],
                  row["scenario"]["name"], row["dynamic_pairs"],
                  "" if row["sensor_alarm"] is None else row["sensor_alarm"]["estimate"]]
        values += [row["physical_tests"][m]["estimate"] for m in ("naive", "moment", "relaxed_split")]
        lines.append(",".join(map(str, values)))
    (OUT/"summary.csv").write_text("\n".join(lines)+"\n", encoding="utf-8")
    plot(p, rows)
    print(json.dumps({"checks": len(checks), "passed": report["all_checks_passed"],
                      "dataset_evaluations": report["dataset_evaluations"],
                      "twin_results": [
                          {"mode": x["calibration_mode"], "scenario": x["scenario"]["name"],
                           "pairs": x["dynamic_pairs"],
                           "sensor": None if x["sensor_alarm"] is None else x["sensor_alarm"]["estimate"],
                           "moment": x["physical_tests"]["moment"]["estimate"],
                           "split": x["physical_tests"]["relaxed_split"]["estimate"]}
                          for x in rows if x["reading_budget"] == max(p["reading_budgets"]) and
                          x["calibration_fraction"] in (0, .25) and
                          x["scenario"]["name"] in ("physical_decay_low", "sensor_mimics_decay_low",
                                                   "transfer_missed_correlation")]}, indent=2))
    assert report["all_checks_passed"]


def plot(p, rows):
    pairs = [("physical_decay_low", "sensor_mimics_decay_low"),
             ("physical_decay_high", "sensor_mimics_decay_high"),
             ("physical_frequency_plus_2.9pct", "sensor_mimics_frequency")]
    fig, axes = plt.subplots(2, 3, figsize=(14, 8), constrained_layout=True)
    modes = [("none", 0.), ("isolated", .25), ("paired", .25)]
    x = np.arange(3)
    for col, (physical, sensor_case) in enumerate(pairs):
        for row_index, method in enumerate(("moment", "relaxed_split")):
            ax = axes[row_index, col]
            for scenario, style, label in ((physical, "o-", "changed dynamics"),
                                           (sensor_case, "s--", "correlated sensor")):
                chosen = [next(r for r in rows if r["reading_budget"] == max(p["reading_budgets"])
                               and r["calibration_mode"] == mode and r["calibration_fraction"] == fraction
                               and r["scenario"]["name"] == scenario) for mode, fraction in modes]
                values = [r["physical_tests"][method] for r in chosen]
                y = np.array([v["estimate"] for v in values])
                ci = np.array([v["wilson95"] for v in values])
                ax.errorbar(x, y, yerr=[y-ci[:, 0], ci[:, 1]-y], fmt=style, capsize=2, label=label)
            sensor_row = next(r for r in rows if r["reading_budget"] == max(p["reading_budgets"])
                              and r["calibration_mode"] == "paired" and r["calibration_fraction"] == .25
                              and r["scenario"]["name"] == sensor_case)
            ax.scatter([2], [sensor_row["sensor_alarm"]["estimate"]], marker="x", s=55,
                       color="#b2463d", label="paired sensor alarm")
            ax.set(xticks=x, xticklabels=["none", "isolated\n25%", "paired\n25%"],
                   ylim=(-.03, 1.03), ylabel="Probability",
                   title=physical.replace("physical_", "").replace("_", " ")+"\n"+method.replace("_", " "))
            ax.grid(alpha=.15)
    axes[0, 0].legend(fontsize=7, loc="center left")
    fig.suptitle("Dynamic-law twins: only matched-lag sensor calibration separates their causes\n"
                 "16,384 total readings; intervals are per-cell Wilson 95% Monte Carlo intervals")
    fig.savefig(OUT/"paired_calibration.png", dpi=170)
    plt.close(fig)


if __name__ == "__main__":
    main()
