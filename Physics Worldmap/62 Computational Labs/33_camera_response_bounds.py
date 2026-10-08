"""Instrument-aware finite-horizon passive response bounds; no novelty claim.

Exact Gaussian sufficient-statistic experiments, with every calibration reading
counted. Camera position averaging is NOT integrated velocity. See the protocol
and proof note for the finite-velocity, equilibrium, and transfer assumptions.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import quad
from scipy.linalg import expm
from scipy.stats import chi2

HERE = Path(__file__).resolve().parent
PROTOCOL = HERE / "camera_response_protocol.json"
OUT = HERE / "results" / "camera_response"
ALIAS_PATH = HERE / "32_acceleration_calibration_alias.py"
spec = importlib.util.spec_from_file_location("thermal_alias_reference", ALIAS_PATH)
alias = importlib.util.module_from_spec(spec)
spec.loader.exec_module(alias)


def sha256(path):
    with Path(path).open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def g(omega, T):
    return .5*T*T*np.sinc(np.asarray(omega)*T/(2*np.pi))**2


def camera_J_time(A, T, h, tolerance=2e-11):
    """Stationary-increment triangular convolution; no position stationarity."""
    J = lambda t: alias.integrated_displacement(A, abs(t))
    value, error = quad(lambda u: (h-u)*(J(T+u)+J(T-u)-2*J(u))/h**2,
                        0, h, epsabs=tolerance, epsrel=tolerance)
    return float(value), float(error)


def camera_J_spectrum(kappa, nu, b, T, h, tolerance=2e-11):
    def density(omega):
        def s2(w):
            return kappa*nu/(np.pi*((kappa-w*w)**2+nu*nu*w*w))
        return s2(omega-b)+s2(omega+b)
    f = lambda w: float(g(w, T)*np.sinc(w*h/(2*np.pi))**2*density(w))
    # Explicit splits resolve both low frequency and the shifted spectral peak.
    edges = sorted(set([0., 1., 2., max(0., b-3), b, b+3, max(40., b+10)]))
    total, error = 0., 0.
    for lo, hi in zip(edges[:-1], edges[1:]):
        value, err = quad(f, lo, hi, epsabs=tolerance, epsrel=tolerance, limit=500)
        total += value
        error += err
    value, err = quad(f, edges[-1], np.inf, epsabs=tolerance, epsrel=tolerance, limit=500)
    return float(total+value), float(error+err)


def variance_interval(squared_deviations, df, alpha):
    return (squared_deviations/chi2.ppf(1-alpha/2, df),
            squared_deviations/chi2.ppf(alpha/2, df))


def response_interval(observed_ci, calibration_ci, T, h, C0, delta, blur):
    """Return endpoints and compatibility; incompatible draws are withheld."""
    ol, ou = observed_ci
    nl, nu = calibration_ci
    low = np.maximum(0., ol-(1+delta)*nu)/2
    signal_high = ou-(1-delta)*nl
    high = signal_high/2
    if blur:
        high = high+C0*h*h/6
        if np.isclose(T/h, round(T/h), rtol=0, atol=1e-10):
            high = np.minimum(high, T*np.sqrt(C0*np.maximum(0., signal_high))/2)
    high = np.minimum(high, C0*T*T/2)
    valid = (signal_high >= 0) & (low <= high)
    return np.stack([np.where(valid, low, np.nan), np.where(valid, high, np.nan)], axis=-1), valid


def wilson(successes, n):
    z = 1.959963984540054
    p = successes/n
    d = 1+z*z/n
    midpoint = (p+z*z/(2*n))/d
    radius = z*np.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
    return [float(midpoint-radius), float(midpoint+radius)]


def main():
    p = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    OUT.mkdir(parents=True, exist_ok=True)
    target, design, cam = p["target"], p["design"], p["camera"]
    T, C0 = target["horizon"], target["known_velocity_variance_upper"]
    kappa, nu, spacing = target["kappa"], target["nu"], target["alias_spacing"]
    exposures = cam["exposures"]
    repeats = design["replicates_per_cell"]
    ao = p["confidence"]["observation_failure_budget"]
    ac = p["confidence"]["calibration_failure_budget"]
    checks = []

    def check(name, passed, value):
        checks.append({"name": name, "passed": bool(passed), "value": value})
        if not passed:
            raise AssertionError(name+": "+str(value))

    check("positive physical parameters and exposures", min(kappa, nu, spacing, T, C0, *exposures) > 0,
          {"T": T, "C0": C0, "exposures": exposures})
    check("all exposure ratios are positive integers", all(abs(T/h-round(T/h)) < 1e-10 for h in exposures), [T/h for h in exposures])
    check("confidence failure budgets sum to five percent", abs(ao+ac-.05) < 1e-14, ao+ac)
    truths, integral_errors, spectrum_errors, refinement_errors = [], [], [], []
    sample_errors, base_variances = [], []
    for q in target["aliases"]:
        b = 2*np.pi*q/spacing
        A = alias.alias_matrix(kappa, nu, b)
        J = alias.integrated_displacement(A, T)
        direct = quad(lambda t: (T-t)*alias.base.covariance(t, kappa, nu), 0, T,
                      weight="cos", wvar=b, epsabs=1e-11, epsrel=1e-11)[0]
        integral_errors.append(abs(J-direct))
        base_variances.append(float(expm(A*0)[0, 0]))
        sample_errors.append(float(max(abs(expm(A*t)[0, 0]-alias.base.covariance(t, kappa, nu))
                                       for t in spacing*np.arange(20))))
        for h in exposures:
            blurred, time_error = camera_J_time(A, T, h)
            spectral, spectral_error = camera_J_spectrum(kappa, nu, b, T, h)
            refined, _ = camera_J_time(A, T, h, 2e-13)
            spectrum_errors.append(abs(blurred-spectral))
            refinement_errors.append(abs(blurred-refined))
            truths.append({"alias": q, "h": h, "true_J": J, "camera_J": blurred,
                           "blur_loss": J-blurred, "additive_blur_allowance": C0*h*h/6,
                           "conditional_population_upper": T*np.sqrt(C0*blurred/2),
                           "time_quadrature_error_estimate": time_error,
                           "spectral_quadrature_error_estimate": spectral_error,
                           "spectral_J": spectral, "frequency_shift": b})
    check("normalized physical velocity variance", max(abs(np.array(base_variances)-C0)) < 1e-13, base_variances)
    check("thermal matrix displacement versus oscillatory integral", max(integral_errors) < 1e-9, max(integral_errors))
    check("same sampled velocity laws for both thermal cases", max(sample_errors) < 1e-10, max(sample_errors))
    check("camera time convolution versus independent spectrum", max(spectrum_errors) < 2e-9, max(spectrum_errors))
    check("camera quadrature refinement", max(refinement_errors) < 2e-10, max(refinement_errors))
    check("true thermal responses obey both blur bounds",
          all(-1e-11 <= r["blur_loss"] <= r["additive_blur_allowance"]+1e-11 and
              r["true_J"] <= r["conditional_population_upper"]+1e-11 for r in truths), len(truths))

    # Test integrand proofs on wide frequency grids, including exact shutter zeros.
    omega = np.r_[0., np.geomspace(1e-6, 1e5, 10000)]
    point_error, conditional_error = [], []
    for h in exposures:
        original = g(omega, T)
        filtered = original*np.sinc(omega*h/(2*np.pi))**2
        point_error.append(float(np.max(original-filtered-C0*h*h/6)))
        conditional_error.append(float(np.max(original**2-.5*T*T*filtered)))
    check("discrete spectral line stress of analytic blur inequalities", max(point_error) < 1e-10 and max(conditional_error) < 1e-8,
          {"additive_max_violation": max(point_error), "conditional_max_violation": max(conditional_error)})
    special_h = 1.
    xx = np.r_[0., np.geomspace(1e-5, 100, 5000)]
    u = np.sinc(xx/np.pi)**2
    special_J, special_blurred = .5*u, .5*u*u
    check("T equals h sharp conditional envelope on spectral lines",
          np.max(abs(special_J-special_h*np.sqrt(special_blurred/2))) < 1e-14 and
          np.max(special_J-special_blurred) <= special_h**2/8+1e-14, float(np.max(special_J-special_blurred)))
    # Noninteger timing: a shutter-zero spectral line invalidates the sqrt bound.
    wzero, noninteger_T = 2*np.pi, .5
    hidden_J = float(g(wzero, noninteger_T))
    invisible_J = float(g(wzero, noninteger_T)*np.sinc(wzero/(2*np.pi))**2)
    check("noninteger shutter-zero counterexample retained", invisible_J < 1e-25 and hidden_J > .04,
          {"T": noninteger_T, "h": 1., "true_J": hidden_J, "camera_J": invisible_J})
    # Position noise telescopes; treating increments as independent is wrong.
    frames = 11
    differencer = np.diff(np.eye(frames), axis=0)
    increment_noise = differencer@differencer.T
    accumulated_noise = np.ones(frames-1)@increment_noise@np.ones(frames-1)
    check("position-noise telescoping leaves exactly two endpoint variances", accumulated_noise == 2,
          {"correct_variance_multiple": float(accumulated_noise), "incorrect_independent_increment_multiple": 2*(frames-1)})
    # Independent general convolution limits, including Brownian motion which is
    # NOT eligible for the finite-instantaneous-velocity blur guarantee.
    hlimit = .3
    def convolved(Jfun):
        return quad(lambda u: (hlimit-u)*(Jfun(T+u)+Jfun(T-u)-2*Jfun(u))/hlimit**2, 0, hlimit)[0]
    check("ballistic and Brownian camera convolution limits",
          abs(convolved(lambda t: .5*t*t)-.5*T*T) < 1e-10 and
          abs(convolved(lambda t: abs(t))-(T-hlimit/3)) < 1e-10,
          {"ballistic": convolved(lambda t: .5*t*t), "Brownian_D1": convolved(lambda t: abs(t))})
    A0 = alias.alias_matrix(kappa, nu, 0.)
    small_exposure, _ = camera_J_time(A0, T, 1e-4)
    check("vanishing exposure recovers instantaneous displacement variance",
          abs(small_exposure-alias.integrated_displacement(A0, T)) < 2e-8,
          abs(small_exposure-alias.integrated_displacement(A0, T)))

    rng = np.random.default_rng(design["seed"])
    rows, ids, saved_sums, saved_intervals, saved_compatible, saved_events = [], [], [], [], [], []
    deterministic_failures, nesting_failures = 0, 0
    for truth in truths:
        q, h, J, Jbar = truth["alias"], truth["h"], truth["true_J"], truth["camera_J"]
        Ncal = 2*(cam["inverse_exposure_coefficient"]/h+cam["variance_floor"])
        for budget in design["total_scalar_readings"]:
            L = int(budget*design["calibration_fraction"]/2)
            M = (budget-2*L)//2
            assert 2*(M+L) == budget and min(M, L) > 1
            for ratio in design["observed_noise_to_calibration_variance_ratios"]:
                Vobs, Nobs = 2*Jbar+ratio*Ncal, ratio*Ncal
                # These are sufficient statistics of centered independent
                # Gaussian differences, exactly, not asymptotic variance draws.
                observed_ss = Vobs*rng.chisquare(M-1, repeats)
                calibration_ss = Ncal*rng.chisquare(L-1, repeats)
                oci = variance_interval(observed_ss, M-1, ao)
                nci = variance_interval(calibration_ss, L-1, ac)
                event = ((oci[0] <= Vobs) & (Vobs <= oci[1]) &
                         (nci[0] <= Ncal) & (Ncal <= nci[1]))
                intervals, compatible, methods = [], [], []
                for name in p["methods"]:
                    delta = design["allowed_transfer_fraction"] if name == "blur_guard_20pct_transfer" else 0.
                    blur = name != "ignore_blur_strict_transfer_INVALID"
                    interval, valid = response_interval(oci, nci, T, h, C0, delta, blur)
                    contains = valid & (interval[:, 0] <= J+1e-12) & (J <= interval[:, 1]+1e-12)
                    assumptions = blur and 1-delta-1e-12 <= ratio <= 1+delta+1e-12
                    if assumptions:
                        deterministic_failures += int(np.sum(event & ~contains))
                    widths = interval[valid, 1]-interval[valid, 0]
                    successes = int(np.sum(contains))
                    methods.append({"name": name, "assumptions_satisfied": bool(assumptions),
                                    "truth_inclusion_count": successes, "unconditional_coverage": successes/repeats,
                                    "coverage_wilson_95": wilson(successes, repeats),
                                    "returned_intervals": int(np.sum(valid)), "withheld_incompatible": int(np.sum(~valid)),
                                    "median_width_returned": float(np.median(widths)) if len(widths) else None,
                                    "median_relative_width_returned": float(np.median(widths)/J) if len(widths) else None,
                                    "median_lower_returned": float(np.median(interval[valid, 0])) if len(widths) else None,
                                    "median_upper_returned": float(np.median(interval[valid, 1])) if len(widths) else None,
                                    "zero_exclusion_fraction_all_draws": float(np.mean(valid & (interval[:, 0] > 0))),
                                    "population_interval": None})
                    pop, pv = response_interval((np.array([Vobs]), np.array([Vobs])),
                                                (np.array([Ncal]), np.array([Ncal])), T, h, C0, delta, blur)
                    if pv[0]:
                        methods[-1]["population_interval"] = pop[0].tolist()
                    intervals.append(interval)
                    compatible.append(valid)
                strict, robust = intervals[1], intervals[2]
                both = compatible[1] & compatible[2]
                nesting_failures += int(np.sum(compatible[1] & ~compatible[2]))
                nesting_failures += int(np.sum(both & ((robust[:, 0] > strict[:, 0]+1e-12) | (robust[:, 1] < strict[:, 1]-1e-12))))
                rows.append({"alias": q, "h": h, "budget": budget, "noise_variance_ratio": ratio,
                             "trajectories": M, "calibration_pairs": L, "degrees_of_freedom": [M-1, L-1],
                             "exposure_integrated_acquisition_proxy": budget*h,
                             "sequential_pair_window_proxy": (M+L)*(T+h),
                             "true_J": J, "camera_J": Jbar, "calibration_pair_noise_variance": Ncal,
                             "observed_pair_noise_variance": Nobs, "observed_total_variance": Vobs,
                             "common_confidence_event_count": int(event.sum()),
                             "common_confidence_event_fraction": float(event.mean()), "methods": methods})
                ids.append([q, h, budget, ratio])
                saved_sums.append(np.stack([observed_ss, calibration_ss], axis=-1))
                saved_intervals.append(np.stack(intervals))
                saved_compatible.append(np.stack(compatible))
                saved_events.append(event)

    check("all declared cells and methods evaluated", len(rows) == len(truths)*len(design["total_scalar_readings"])*len(design["observed_noise_to_calibration_variance_ratios"]) and
          all(len(row["methods"]) == 3 for row in rows), {"cells": len(rows), "datasets": len(rows)*repeats, "interval_attempts": len(rows)*repeats*3})
    check("every observation and calibration reading counted", all(2*(r["trajectories"]+r["calibration_pairs"]) == r["budget"] for r in rows), len(rows))
    check("valid methods cover truth on every common confidence event", deterministic_failures == 0, deterministic_failures)
    check("bounded-transfer intervals contain strict-transfer intervals", nesting_failures == 0, nesting_failures)
    check("every stochastic attempt returned or explicitly withheld", all(m["returned_intervals"]+m["withheld_incompatible"] == repeats for r in rows for m in r["methods"]), len(rows)*3)
    finite_returned = all(np.isfinite(values[flags]).all()
                          for values, flags in zip(saved_intervals, saved_compatible)
                          for values, flags in zip(values, flags))
    check("all returned interval endpoints are finite", finite_returned, finite_returned)
    arrays_path = OUT / "sufficient_statistics_and_intervals.npz"
    np.savez_compressed(arrays_path, cell_ids=np.array(ids), squared_deviations=np.array(saved_sums),
                        intervals=np.array(saved_intervals), compatible=np.array(saved_compatible),
                        common_confidence_events=np.array(saved_events), methods=np.array(p["methods"]))
    loaded = np.load(arrays_path)
    check("saved sufficient statistics and intervals round trip", np.array_equal(loaded["squared_deviations"], np.array(saved_sums)) and
          np.array_equal(loaded["intervals"], np.array(saved_intervals), equal_nan=True), str(loaded["intervals"].shape))
    summary = {"cells": len(rows), "datasets": len(rows)*repeats, "interval_attempts": len(rows)*repeats*3,
               "exact_common_event_probability": (1-ao)*(1-ac),
               "common_event_rate_range": [min(r["common_confidence_event_fraction"] for r in rows), max(r["common_confidence_event_fraction"] for r in rows)],
               "in_scope_coverage_range": [min(m["unconditional_coverage"] for r in rows for m in r["methods"] if m["assumptions_satisfied"]),
                                           max(m["unconditional_coverage"] for r in rows for m in r["methods"] if m["assumptions_satisfied"])],
               "valid_common_event_violations": deterministic_failures}
    result = {"title": p["title"], "status": p["status"], "generated_utc": datetime.now(timezone.utc).isoformat(),
              "scope": p["limits"], "truths": truths, "rows": rows, "summary": summary,
              "checks": checks, "passed_checks": len(checks),
              "hashes": {"script": sha256(__file__), "protocol": sha256(PROTOCOL), "source_alias_script": sha256(ALIAS_PATH),
                         "source_spectral_script": sha256(alias.BASE_PATH), "saved_arrays": sha256(arrays_path)}}
    (OUT/"results.json").write_text(json.dumps(result, indent=2, allow_nan=False)+"\n", encoding="utf-8")
    plot(result, p)
    print(json.dumps({"summary": summary, "truths": truths, "passed_checks": len(checks)}, indent=2))


def plot(result, p):
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.8), constrained_layout=True)
    colors = ["#dc2626", "#0f766e", "#7c3aed"]
    labels = ["Ignores blur (invalid)", "Blur; exact transfer", "Blur; ±20% transfer"]
    selected = [r for r in result["rows"] if r["alias"] == 1 and r["budget"] == 32768]
    for axis, ratio in zip(axes[:2], [1., 1.2]):
        rows = sorted([r for r in selected if r["noise_variance_ratio"] == ratio], key=lambda r: r["h"])
        for j, (color, label) in enumerate(zip(colors, labels)):
            axis.plot([r["h"] for r in rows], [100*r["methods"][j]["unconditional_coverage"] for r in rows],
                      "o-", color=color, label=label)
        axis.axhline(95, color="black", linestyle=":", lw=1)
        axis.set(title="Noise transfer holds" if ratio == 1 else "20% more noise than calibration",
                 xlabel="Position exposure h", ylabel="Truth inclusion (%)", ylim=(-2, 103))
        axis.set_xticks(p["camera"]["exposures"])
    rows = sorted([r for r in selected if r["noise_variance_ratio"] == 1.], key=lambda r: r["h"])
    for j in [1, 2]:
        axes[2].plot([r["h"] for r in rows], [r["methods"][j]["median_relative_width_returned"] for r in rows],
                     "o-", color=colors[j], label=labels[j])
    axes[2].axhline(1, color="black", linestyle=":", lw=1)
    axes[2].set(title="Coverage is not the same as precision", xlabel="Position exposure h",
                ylabel="Median width / true response", yscale="log")
    axes[2].set_xticks(p["camera"]["exposures"])
    for ax in axes:
        ax.grid(alpha=.15)
        ax.legend(fontsize=8, loc="best")
    fig.suptitle("Finite-exposure camera model • thermal alias • 32,768 readings including calibration", fontsize=13)
    fig.savefig(OUT/"camera_response_bounds.png", dpi=180)
    plt.close(fig)


if __name__ == "__main__":
    main()
