"""Frozen calibration comparison with continuous noise nuisance and safe bounds."""
from __future__ import annotations
from functools import lru_cache
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
PROTOCOL = HERE/"sensor_calibration_protocol.json"
OUT = HERE/"results"/"sensor_calibration"
spec = importlib.util.spec_from_file_location("range_reference", HERE/"22_range_measurement_design.py")
ref = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ref)
family = ref.family
METHODS = ("naive", "plugin", "nuisance_moments", "relaxed_split", "fixed_mixture")


@lru_cache(maxsize=None)
def quantiles(n, tail):
    return float(chi2.ppf(tail, n)), float(chi2.ppf(1-tail, n))


def coordinates(stats):
    return np.column_stack([(stats[:, 0]+stats[:, 1]+2*stats[:, 2])/2,
                            (stats[:, 0]+stats[:, 1]-2*stats[:, 2])/2])


def noise_interval(cal_sum, k, beta):
    if k == 0:
        return np.zeros_like(cal_sum), np.full_like(cal_sum, np.inf)
    low, high = quantiles(k, beta/2)
    return cal_sum/high, cal_sum/low


def moment_candidates(data, lags, n, p, noise_low, noise_high, alpha):
    """Common nuisance-variance interval intersection, not a discretized search."""
    r, per = len(data[0][0]), n//len(lags)
    low_q, high_q = quantiles(per, alpha/(4*len(lags)))
    lower = np.broadcast_to(np.asarray(noise_low)[:, None], (r, 3)).copy()
    upper = np.broadcast_to(np.asarray(noise_high)[:, None], (r, 3)).copy()
    for t, (train, test) in zip(lags, data):
        u = coordinates(train+test)
        c = np.array([ref.ref.cov(a, t, p["decay_rate"]) for a in p["candidate_aliases"]])
        for coord, base in ((0, 1+c), (1, 1-c)):
            lower = np.maximum(lower, u[:, coord, None]/high_q-base[None, :])
            upper = np.minimum(upper, u[:, coord, None]/low_q-base[None, :])
    return lower <= upper


def variance_loglike(sums, n, variance):
    return -.5*(n*np.log(2*np.pi*variance)+sums/variance)


def null_upper_likelihood(data, lags, n, p, noise_low, noise_high):
    """Relax common variance into separate bounded +/- variances per lag."""
    r, half = len(data[0][0]), n//len(lags)//2
    result = np.zeros((r, 3))
    for t, (_, test) in zip(lags, data):
        u = coordinates(test)
        for j, a in enumerate(p["candidate_aliases"]):
            c = ref.ref.cov(a, t, p["decay_rate"])
            for coord, base in ((0, 1+c), (1, 1-c)):
                variance = np.clip(u[:, coord]/half, base+noise_low, base+noise_high)
                result[:, j] += variance_loglike(u[:, coord], half, variance)
    return result


def split_score(data, lags, n, p, noise_low, noise_high):
    half = n//len(lags)//2
    fit = np.zeros(len(data[0][0]))
    for train, test in data:
        ridge = p["ridge_fraction"]*(1+p["measurement_noise_sd"]**2)
        fit += family.ll(train[:, 0]/half+ridge, train[:, 1]/half+ridge,
                         train[:, 2]/half, half, test)
    upper = null_upper_likelihood(data, lags, n, p, noise_low, noise_high)
    return fit-np.max(upper, axis=1), upper


def main():
    raw = PROTOCOL.read_bytes()
    p = json.loads(raw)
    # Reference model list is inherited; it is not tuned to calibration outcomes.
    mixture_p = json.loads(ref.PROTOCOL.read_text(encoding="utf-8"))
    r = p["replicates"]
    nominal_s2 = p["measurement_noise_sd"]**2
    checks = {}
    def check(name, error, tol=1e-9):
        checks[name] = {"error": float(error), "tolerance": tol, "passed": bool(error < tol)}

    check("error_budget", abs(p["alpha_total"]-p["calibration_beta"]-.02))
    ql, qu = quantiles(128, p["calibration_beta"]/2)
    check("chi_square_tail_inversion", max(abs(chi2.cdf(ql, 128)-.0025), abs(chi2.sf(qu, 128)-.0025)))
    zl, zu = noise_interval(np.array([16.]), 128, p["calibration_beta"])
    check("calibration_interval_order", float(not (0 < zl[0] < zu[0])))
    lo0, hi0 = noise_interval(np.zeros(3), 0, p["calibration_beta"])
    check("no_calibration_full_noise_range", float(not (np.all(lo0 == 0) and np.all(np.isposinf(hi0)))))
    known_stats = np.array([[2., 3., .4]])
    eig = coordinates(known_stats)[0]
    check("orthogonal_coordinate_sum", abs(sum(eig)-5))
    check("orthogonal_coordinate_difference", abs(eig[0]-eig[1]-0.8))
    check("eigen_likelihood_matches_matrix", abs(
        sum(variance_loglike(eig, 4, np.array([1.4, 1.])))-
        family.ll(1.2, 1.2, .2, 4, known_stats)[0]))
    # Check bounded scalar maximum against a dense independent grid.
    dense = np.linspace(.2, 2., 10001)
    for i, sums in enumerate((.1, 4., 40.)):
        opt = np.clip(sums/4, .2, 2.)
        check("clipped_variance_optimum_"+str(i), max(0., float(
            np.max(variance_loglike(sums, 4, dense))-variance_loglike(sums, 4, opt))))
    rows, arrays = [], {}
    budget_overrun = bound_error = quantile_error = 0.
    nested = finite = positive = True
    responses = np.array([family.response(p, {"alias": a, "decay": p["decay_rate"]})
                          for a in p["candidate_aliases"]])
    distances = abs(responses[:, None]-responses[None, :])
    for b in p["reading_budgets"]:
        for fraction in p["calibration_fractions"]:
            k = int(np.floor(b*fraction))
            alpha = p["alpha_total"]-(p["calibration_beta"] if k else 0)
            for design, lags in p["designs"].items():
                multiple = 2*len(lags)
                n = multiple*int(np.floor((b-k)/(2*multiple)))
                budget_overrun = max(budget_overrun, 2*n+k-b)
                for scenario in p["scenarios"]:
                    index = len(rows)
                    streams = np.random.SeedSequence([p["seed"], index]).spawn(2)
                    rng, cal_rng = [np.random.default_rng(s) for s in streams]
                    actual_s2 = scenario["noise_sd"]**2
                    cal_s2 = scenario.get("calibration_noise_sd", scenario["noise_sd"])**2
                    z = cal_s2*cal_rng.chisquare(k, r) if k else np.zeros(r)
                    lo, hi = noise_interval(z, k, p["calibration_beta"])
                    data = ref.ref.datasets(rng, r, n, lags, 1+actual_s2, scenario["alias"],
                                            {**p, "decay_rate": scenario["decay"]})
                    naive_keep = moment_candidates(data, lags, n, p,
                        np.full(r, nominal_s2), np.full(r, nominal_s2), p["alpha_total"])
                    aware_keep = moment_candidates(data, lags, n, p, lo, hi, alpha)
                    split, upper = split_score(data, lags, n, p, lo, hi)
                    mix, _, _ = ref.mixture_score(data, lags, n, 1+nominal_s2, mixture_p)
                    events = {"naive": ~np.any(naive_keep, axis=1),
                              "nuisance_moments": ~np.any(aware_keep, axis=1),
                              "relaxed_split": split > np.log(1/alpha),
                              "fixed_mixture": mix > np.log(1/p["alpha_total"])}
                    sensor = (nominal_s2 < lo) | (nominal_s2 > hi) if k else None
                    if k:
                        point = z/k
                        plugin_keep = moment_candidates(data, lags, n, p, point, point, p["alpha_total"])
                        events["plugin"] = ~np.any(plugin_keep, axis=1)
                    # For the same alpha, widening calibration intervals cannot increase rejection.
                    broad = moment_candidates(data, lags, n, p, np.zeros(r), np.full(r, np.inf), alpha)
                    nested &= bool(np.all(~aware_keep | broad))
                    # Upper denominator must dominate every null likelihood at an included variance.
                    trial_s2 = lo+.37*np.where(np.isfinite(hi), hi-lo, 1.)
                    half = n//len(lags)//2
                    for j, a in enumerate(p["candidate_aliases"]):
                        known_ll = np.zeros(r)
                        for t, (_, test) in zip(lags, data):
                            c = ref.ref.cov(a, t, p["decay_rate"])
                            known_ll += family.ll(1+trial_s2, 1+trial_s2, c, half, test)
                        bound_error = max(bound_error, float(np.max(known_ll-upper[:, j])))
                    finite &= bool(np.all(np.isfinite(split)) and np.all(np.isfinite(mix)))
                    positive &= all(np.all(s[:, 0]*s[:, 1]-s[:, 2]**2 > 0) for pair in data for s in pair)
                    truth_chi = family.response(p, scenario)
                    best_error = float(np.min(abs(responses-truth_chi))/abs(truth_chi))
                    retained = np.sum(aware_keep, axis=1)
                    mask = aware_keep[:, :, None] & aware_keep[:, None, :]
                    diameter = np.max(np.where(mask, distances, 0.), axis=(1, 2))
                    joint = None if sensor is None else {
                        method: {name: family.wilson(flag) for name, flag in {
                            "neither": ~sensor & ~events[method],
                            "sensor_only": sensor & ~events[method],
                            "physics_only": ~sensor & events[method],
                            "both": sensor & events[method]}.items()}
                        for method in ("nuisance_moments", "relaxed_split")}
                    rows.append({
                        "reading_budget": b, "calibration_fraction": fraction, "calibration_readings": k,
                        "dynamic_pairs": n, "used_readings": k+2*n, "design": design, "lags": lags,
                        "wait_cost_proxy": n*(1+np.mean(lags))+k,
                        "scenario": scenario, "dynamic_alpha": alpha,
                        "calibration_coverage": None if not k else family.wilson((lo <= cal_s2) & (hi >= cal_s2)),
                        "dynamic_noise_covered": None if not k else family.wilson((lo <= actual_s2) & (hi >= actual_s2)),
                        "sensor_alarm": None if sensor is None else family.wilson(sensor),
                        "tests": {m: family.wilson(ev) for m, ev in events.items()},
                        "joint_labels": joint, "best_candidate_response_error": best_error,
                        "missed_large_response_deviation": {
                            m: family.wilson(~ev) if best_error > p["response_error_cutoff"] else None
                            for m, ev in events.items()},
                        "nominal_response_set": {
                            "singleton_rate": family.wilson(retained == 1),
                            "mean_diameter_absolute_nonempty": float(np.mean(diameter[retained > 0])) if np.any(retained > 0) else None,
                            "scope": "Only the three nominal responses; not a continuum response certificate."}})
                    arrays[f"cell{index}"] = np.column_stack([
                        z, split, mix, events["naive"], events.get("plugin", np.full(r, np.nan)),
                        events["nuisance_moments"], events["relaxed_split"],
                        np.full(r, np.nan) if sensor is None else sensor, aware_keep.astype(int)])
    check("reading_budgets_respected", budget_overrun)
    check("null_relaxation_pointwise_dominates", max(0., bound_error), 1e-8)
    check("wider_noise_range_retains_more_models", float(not nested))
    check("finite_test_scores", float(not finite))
    check("positive_sample_covariances", float(not positive))
    check("270_cells", abs(len(rows)-270))
    report = {"scope": p["scope"], "protocol_sha256": hashlib.sha256(raw).hexdigest(),
              "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "dependency_sha256": {name: hashlib.sha256((HERE/name).read_bytes()).hexdigest()
                  for name in ("20_family_rejection.py", "21_oracle_detection_limits.py",
                               "22_range_measurement_design.py", "range_design_protocol.json")},
              "python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__,
              "matplotlib": matplotlib.__version__, "dataset_evaluations": len(rows)*r,
              "score_columns": ["calibration_sum_squares", "split_loge", "mixture_loge", "naive_reject",
                                "plugin_reject_or_nan", "nuisance_moments_reject", "split_reject",
                                "sensor_alarm_or_nan", "retained_alias1", "retained_alias2", "retained_alias3"],
              "checks": checks, "all_checks_passed": all(c["passed"] for c in checks.values()),
              "cells": rows, "limits": p["limits"]}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT/"results.json").write_text(json.dumps(report, indent=2, allow_nan=False)+"\n", encoding="utf-8")
    np.savez_compressed(OUT/"scores.npz", **arrays)
    lines = ["budget,calibration_fraction,design,scenario,dynamic_pairs,sensor_alarm,"+",".join(METHODS)]
    for row in rows:
        values = [row["reading_budget"], row["calibration_fraction"], row["design"], row["scenario"]["name"],
                  row["dynamic_pairs"], "" if row["sensor_alarm"] is None else row["sensor_alarm"]["estimate"]]
        values += [row["tests"][m]["estimate"] if m in row["tests"] else "" for m in METHODS]
        lines.append(",".join(map(str, values)))
    (OUT/"summary.csv").write_text("\n".join(lines)+"\n", encoding="utf-8")
    plot(p, rows)
    print(json.dumps({"checks": len(checks), "all_checks_passed": report["all_checks_passed"],
                      "dataset_evaluations": report["dataset_evaluations"],
                      "selected_results": [
                          {"budget": row["reading_budget"], "fraction": row["calibration_fraction"],
                           "scenario": row["scenario"]["name"],
                           **{m: ev["estimate"] for m, ev in row["tests"].items()}}
                          for row in rows if row["design"] == "range_plus_integer" and
                          row["reading_budget"] == 8192 and row["calibration_fraction"] in (0., .25) and
                          row["scenario"]["name"] in ("sensor_high", "damping_low", "frequency_plus_4.1pct",
                                                      "calibration_transfer_failure")]}, indent=2))
    assert report["all_checks_passed"]


def plot(p, rows):
    fig, axes = plt.subplots(2, 3, figsize=(14, 8), constrained_layout=True)
    names = ["sensor_high", "damping_low", "calibration_transfer_failure"]
    colors = {"naive": "#ad6638", "plugin": "#a18431", "nuisance_moments": "#187d83",
              "relaxed_split": "#7951a0", "fixed_mixture": "#6e7786"}
    for row_index, design in enumerate(p["designs"]):
        for col, scenario in enumerate(names):
            ax = axes[row_index, col]
            subset = [r for r in rows if r["design"] == design and r["scenario"]["name"] == scenario
                      and r["reading_budget"] == 8192]
            for method in METHODS:
                chosen = [r for r in subset if method in r["tests"]]
                rates = [r["tests"][method] for r in chosen]
                estimates = np.array([t["estimate"] for t in rates])
                ci = np.array([t["wilson95"] for t in rates])
                ax.errorbar([100*r["calibration_fraction"] for r in chosen], estimates,
                            yerr=[estimates-ci[:, 0], ci[:, 1]-estimates], marker="o", capsize=2,
                            label=method.replace("_", " "), color=colors[method])
            ax.axhline(.025, color="#aaa", linestyle=":", linewidth=1)
            ax.set(title=scenario.replace("_", " ")+"\n"+design.replace("_", " "),
                   xlabel="Reading budget spent on calibration (%)",
                   ylabel="Physical-family rejection", ylim=(-.03, 1.03))
            ax.set_xticks([0, 12.5, 25])
            ax.grid(alpha=.15)
    axes[0, 1].legend(fontsize=7, loc="upper left")
    fig.suptitle("Independent calibration: useful uncertainty, real cost, limited transfer\n"
                 "8,192 total readings; transfer-failure column deliberately violates the guarantee")
    fig.savefig(OUT/"sensor_calibration.png", dpi=170)
    plt.close(fig)


if __name__ == "__main__":
    main()
