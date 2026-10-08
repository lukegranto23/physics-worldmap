"""Independent read-only recomputation of Lab 33; writes only its audit report.

No Lab 31--33 implementation is imported. Camera variance is recomputed from
the direct velocity-covariance quadratic form of the trapezoidal exposure
weight. Stored Gaussian sufficient statistics are then independently inverted.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from scipy.integrate import quad
from scipy.special import roots_legendre
from scipy.stats import chi2

HERE = Path(__file__).resolve().parent
OUT = HERE / "results" / "camera_response"


def sha(path):
    with Path(path).open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def read_json(path):
    def reject(token):
        raise ValueError("Nonfinite JSON token: " + token)
    return json.loads(Path(path).read_text(encoding="utf-8"), parse_constant=reject)


def covariance(t, kappa, nu, shift):
    """Analytic covariance of the declared underdamped thermal alias."""
    wd2 = kappa - nu * nu / 4
    if wd2 <= 0:
        raise ValueError("This independent implementation targets underdamped cases.")
    wd = np.sqrt(wd2)
    t = np.abs(np.asarray(t))
    return (np.exp(-nu*t/2) * (np.cos(wd*t) + nu*np.sin(wd*t)/(2*wd))
            * np.cos(shift*t))


def camera_quadratic_form(T, h, kappa, nu, shift, order):
    """Half double integral w(s) C(s-t) w(t), not a J-convolution."""
    raw_nodes, raw_weights = roots_legendre(order)
    cuts = sorted(set([0., h, T, T+h]))
    nodes, weights = [], []
    for a, b in zip(cuts[:-1], cuts[1:]):
        t = a + (b-a)*(raw_nodes+1)/2
        exposure_weight = np.maximum(0., np.minimum(h, t)-np.maximum(0., t-T))/h
        nodes.append(t)
        weights.append(raw_weights*(b-a)*exposure_weight/2)
    x, v = np.concatenate(nodes), np.concatenate(weights)
    matrix = covariance(x[:, None]-x[None, :], kappa, nu, shift)
    return float(v@matrix@v/2), float(v.sum())


def interval_from_ss(ss, df, alpha):
    # Survival-function inversion is deliberately separate from Lab 33's ppf.
    return ss / chi2.isf(alpha/2, df), ss / chi2.isf(1-alpha/2, df)


def main():
    protocol_path = HERE / "camera_response_protocol.json"
    result_path = OUT / "results.json"
    arrays_path = OUT / "sufficient_statistics_and_intervals.npz"
    p, r = read_json(protocol_path), read_json(result_path)
    arrays = np.load(arrays_path, allow_pickle=False)
    checks = []

    def check(name, passed, value):
        checks.append({"name": name, "passed": bool(passed), "value": value})
        if not passed:
            raise AssertionError(name + ": " + str(value))

    hash_paths = {
        "script": HERE / "33_camera_response_bounds.py",
        "protocol": protocol_path,
        "source_alias_script": HERE / "32_acceleration_calibration_alias.py",
        "source_spectral_script": HERE / "31_spectral_response_bounds.py",
        "saved_arrays": arrays_path,
    }
    check("all recorded input and source hashes match",
          all(sha(path) == r["hashes"][name] for name, path in hash_paths.items()),
          {name: sha(path) for name, path in hash_paths.items()})

    target, design = p["target"], p["design"]
    T, cmax = target["horizon"], target["known_velocity_variance_upper"]
    kappa, nu = target["kappa"], target["nu"]
    ao, an = p["confidence"]["observation_failure_budget"], p["confidence"]["calibration_failure_budget"]
    repeats = design["replicates_per_cell"]
    truth_audits = []
    j_errors, camera_errors, refinement_errors, weight_errors = [], [], [], []
    for truth in r["truths"]:
        h, q = truth["h"], truth["alias"]
        shift = 2*np.pi*q/target["alias_spacing"]
        true_j, err = quad(lambda t: (T-t)*covariance(t, kappa, nu, shift),
                           0, T, epsabs=1e-12, epsrel=1e-12, limit=300)
        blurred, weight_sum = camera_quadratic_form(T, h, kappa, nu, shift, 240)
        refined, _ = camera_quadratic_form(T, h, kappa, nu, shift, 480)
        j_errors.append(abs(true_j-truth["true_J"]))
        camera_errors.append(abs(refined-truth["camera_J"]))
        refinement_errors.append(abs(refined-blurred))
        weight_errors.append(abs(weight_sum-T))
        truth_audits.append({"alias": q, "h": h, "J_direct_integral": true_j,
                             "J_integral_error_estimate": float(err),
                             "camera_J_direct_covariance": refined,
                             "camera_J_refinement_change": abs(refined-blurred),
                             "camera_weight_integral": weight_sum})
    check("independent unblurred thermal integrals agree", max(j_errors) < 1e-10, max(j_errors))
    check("direct camera covariance quadratic forms agree", max(camera_errors) < 2e-9, max(camera_errors))
    check("direct camera quadrature refinement", max(refinement_errors) < 3e-8, max(refinement_errors))
    check("camera velocity weights integrate to the horizon", max(weight_errors) < 1e-12, max(weight_errors))

    expected_ids = [[q, h, budget, ratio] for q in target["aliases"]
                    for h in p["camera"]["exposures"] for budget in design["total_scalar_readings"]
                    for ratio in design["observed_noise_to_calibration_variance_ratios"]]
    check("all declared cells stored in declared order",
          np.array_equal(arrays["cell_ids"], expected_ids), len(expected_ids))
    check("saved shapes and methods agree with protocol",
          arrays["squared_deviations"].shape == (len(expected_ids), repeats, 2)
          and arrays["intervals"].shape == (len(expected_ids), len(p["methods"]), repeats, 2)
          and arrays["methods"].tolist() == p["methods"],
          {key: list(arrays[key].shape) for key in arrays.files})

    endpoint_error = 0.
    flag_differences = summary_differences = event_differences = 0
    valid_common_violations = invalid_common_successes = 0
    exact_vs_tolerant_coverage_differences = 0
    replay_error = 0.
    per_cell = []
    rng = np.random.default_rng(design["seed"])
    common_count, in_scope_count = 0, 0
    nested_failures = 0
    conditional_cap_tightenings = 0
    withheld_count = 0
    for i, row in enumerate(r["rows"]):
        q, h, budget, ratio = expected_ids[i]
        if [row["alias"], row["h"], row["budget"], row["noise_variance_ratio"]] != expected_ids[i]:
            raise AssertionError("Row-ID disagreement")
        M = row["trajectories"]
        L = row["calibration_pairs"]
        if (2*(M+L) != budget or row["degrees_of_freedom"] != [M-1, L-1]
                or row["exposure_integrated_acquisition_proxy"] != budget*h
                or row["sequential_pair_window_proxy"] != (M+L)*(T+h)):
            raise AssertionError("Acquisition accounting mismatch")
        ss = arrays["squared_deviations"][i]
        o_lo, o_hi = interval_from_ss(ss[:, 0], M-1, ao)
        n_lo, n_hi = interval_from_ss(ss[:, 1], L-1, an)
        v_total, n_cal = row["observed_total_variance"], row["calibration_pair_noise_variance"]
        expected_noise = 2*(p["camera"]["inverse_exposure_coefficient"]/h+p["camera"]["variance_floor"])
        if abs(expected_noise-n_cal) > 1e-14 or abs(v_total-2*row["camera_J"]-ratio*n_cal) > 1e-12:
            raise AssertionError("Noise or total variance normalization mismatch")
        replay_obs = v_total*rng.chisquare(M-1, repeats)
        replay_cal = n_cal*rng.chisquare(L-1, repeats)
        replay_error = max(replay_error, float(np.max(abs(replay_obs-ss[:, 0]))),
                           float(np.max(abs(replay_cal-ss[:, 1]))))
        common = ((o_lo <= v_total) & (v_total <= o_hi) & (n_lo <= n_cal) & (n_cal <= n_hi))
        event_differences += int(np.sum(common != arrays["common_confidence_events"][i]))
        if int(common.sum()) != row["common_confidence_event_count"]:
            summary_differences += 1
        common_count += int(common.sum())
        method_results = []
        recomputed = []
        for j, name in enumerate(p["methods"]):
            delta = design["allowed_transfer_fraction"] if j == 2 else 0.
            blur_aware = j != 0
            jbar_lower = np.maximum(0., o_lo-(1+delta)*n_hi)/2
            raw_upper = (o_hi-(1-delta)*n_lo)/2
            if blur_aware:
                assert T/h == round(T/h), "Current study requires exact declared integer ratios"
                upper = np.minimum.reduce([raw_upper+cmax*h*h/6,
                    T*np.sqrt(cmax*np.maximum(raw_upper, 0.)/2),
                    np.full(repeats, cmax*T*T/2)])
            else:
                upper = np.minimum(raw_upper, cmax*T*T/2)
            valid = (raw_upper >= 0.) & (jbar_lower <= upper)
            cap_tightens = (valid & (T*np.sqrt(cmax*np.maximum(raw_upper, 0.)/2)
                                    < raw_upper+cmax*h*h/6)) if blur_aware else np.zeros(repeats, dtype=bool)
            conditional_cap_tightenings += int(cap_tightens.sum())
            withheld_count += int((~valid).sum())
            interval = np.column_stack([jbar_lower, upper])
            interval[~valid] = np.nan
            stored = arrays["intervals"][i, j]
            flag_differences += int(np.sum(valid != arrays["compatible"][i, j]))
            if not np.array_equal(np.isnan(interval), np.isnan(stored)):
                raise AssertionError("Withheld endpoint mask differs")
            if valid.any():
                endpoint_error = max(endpoint_error, float(np.max(abs(interval[valid]-stored[valid]))))
            truth = row["true_J"]
            contains = valid & (interval[:, 0] <= truth) & (truth <= interval[:, 1])
            tolerant = valid & (interval[:, 0] <= truth+1e-12) & (truth <= interval[:, 1]+1e-12)
            exact_vs_tolerant_coverage_differences += int(np.sum(contains != tolerant))
            assumed = bool(blur_aware and 1-delta <= ratio <= 1+delta)
            reported = row["methods"][j]
            failures = int(np.sum(common & ~contains)) if assumed else None
            if assumed:
                valid_common_violations += failures
                in_scope_count += repeats
            else:
                invalid_common_successes += int(np.sum(common & contains))
            widths = interval[valid, 1]-interval[valid, 0]
            numeric_summaries = {"unconditional_coverage": float(contains.mean()),
                "zero_exclusion_fraction_all_draws": float(np.mean(valid & (jbar_lower > 0))),
                "median_width_returned": float(np.median(widths)) if len(widths) else None,
                "median_relative_width_returned": float(np.median(widths)/truth) if len(widths) else None,
                "median_lower_returned": float(np.median(interval[valid, 0])) if len(widths) else None,
                "median_upper_returned": float(np.median(interval[valid, 1])) if len(widths) else None}
            for key, value in numeric_summaries.items():
                if value is None:
                    summary_differences += int(reported[key] is not None)
                else:
                    summary_differences += int(abs(value-reported[key]) > 1e-10)
            summary_differences += int(reported["truth_inclusion_count"] != int(contains.sum()))
            summary_differences += int(reported["returned_intervals"] != int(valid.sum()))
            summary_differences += int(reported["withheld_incompatible"] != int((~valid).sum()))
            summary_differences += int(reported["assumptions_satisfied"] != assumed)
            method_results.append({"method": name, "in_scope": assumed,
                                   "returned": int(valid.sum()), "truth_inclusions": int(contains.sum()),
                                   "conditional_cap_tightenings": int(cap_tightens.sum()),
                                   "common_event_violations_if_in_scope": failures})
            recomputed.append((interval, valid))
        strict, robust = recomputed[1], recomputed[2]
        both = strict[1] & robust[1]
        nested_failures += int(np.sum(strict[1] & ~robust[1]))
        nested_failures += int(np.sum(both & ((robust[0][:, 0] > strict[0][:, 0]+1e-12)
                                             | (robust[0][:, 1] < strict[0][:, 1]-1e-12))))
        per_cell.append({"id": expected_ids[i], "common_event_count": int(common.sum()), "methods": method_results})

    check("Gaussian sufficient-statistic seed replay exact", replay_error == 0., replay_error)
    check("all stored common confidence events independently recovered", event_differences == 0, event_differences)
    check("all interval endpoints independently recomputed", endpoint_error < 2e-11, endpoint_error)
    check("all compatibility flags independently recovered", flag_differences == 0, flag_differences)
    check("all reported counts medians and scope flags recovered", summary_differences == 0, summary_differences)
    check("coverage does not rely on endpoint tolerance", exact_vs_tolerant_coverage_differences == 0,
          exact_vs_tolerant_coverage_differences)
    check("no in-scope common event loses truth", valid_common_violations == 0,
          {"failures": valid_common_violations, "in_scope_interval_attempts": in_scope_count})
    check("robust intervals nest strict intervals", nested_failures == 0, nested_failures)
    check("exact independent-event probability correctly reported",
          abs(r["summary"]["exact_common_event_probability"]-(1-ao)*(1-an)) < 1e-14,
          (1-ao)*(1-an))
    check("every declared observation and calibration reading is counted", True, len(expected_ids))

    report = {"audit": "Independent camera response recomputation",
              "generated_utc": datetime.now(timezone.utc).isoformat(),
              "status": "All checks passed; no blocking scientific inconsistency found in the declared study.",
              "scope": "Direct covariance quadrature and saved-statistical-output audit, not experimental validation or an exhaustive code proof.",
              "passed_checks": len(checks), "checks": checks, "truth_audits": truth_audits,
              "summary": {"cells": len(expected_ids), "datasets": len(expected_ids)*repeats,
                          "intervals_recomputed": len(expected_ids)*repeats*len(p["methods"]),
                          "common_event_count": common_count, "in_scope_interval_attempts": in_scope_count,
                          "withheld_interval_count": withheld_count,
                          "conditional_cap_tightenings_in_returned_blur_aware_intervals": conditional_cap_tightenings,
                          "in_scope_common_event_failures": valid_common_violations,
                          "out_of_scope_common_event_truth_inclusions": invalid_common_successes,
                          "out_of_scope_interpretation": "Accidental truth inclusion outside assumptions does not validate a method."},
              "nonblocking_scope_notes": [
                  "Integer timing is a declared exact operator property, not experimentally established by a numerical isclose guard.",
                  "The camera functional is passive half-MSD, not the actual blurred camera mean under an ordinary step force.",
                  "Equal scalar-reading counts do not equalize exposure time, photons, total hardware cost or trajectory preparation.",
                  "Confidence is per prechosen cell; the shared method comparisons are dependent and there is no post-selection or simultaneous 48-cell claim.",
                  "Returned-only width medians must remain distinguished from unconditional truth inclusion and withheld counts.",
                  "Formal finite-velocity bounds can be uninformative for ordinary camera/inertial timescale ratios."],
              "cells": per_cell,
              "hashes": {"audit_source": sha(__file__), "main_source": sha(hash_paths["script"]),
                         "protocol": sha(protocol_path), "main_results": sha(result_path), "saved_arrays": sha(arrays_path)}}
    (OUT / "independent_audit.json").write_text(json.dumps(report, indent=2, allow_nan=False)+"\n", encoding="utf-8")
    print(json.dumps({"passed_checks": len(checks), "summary": report["summary"],
                      "largest_endpoint_difference": endpoint_error,
                      "largest_camera_quadrature_difference": max(camera_errors)}, indent=2))


if __name__ == "__main__":
    main()
