"""Post-hoc calibration-transfer failure in an exact smooth thermal alias family.

The intentionally misused finite-difference upper bound is NEVER a valid
instantaneous acceleration certificate. This script demonstrates that error;
it does not weaken or retune Lab 31's stated ideal-acceleration assumptions.
"""
from __future__ import annotations

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

HERE = Path(__file__).resolve().parent
PROTOCOL = HERE/"acceleration_alias_diagnostic_protocol.json"
OUT = HERE/"results"/"spectral_response"
BASE_PATH = HERE/"31_spectral_response_bounds.py"
spec = importlib.util.spec_from_file_location("spectral_bound_reference", BASE_PATH)
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)


def alias_matrix(kappa, nu, b):
    generator = np.array([[0., -np.sqrt(kappa)], [np.sqrt(kappa), -nu]])
    rotation = np.array([[0., -b], [b, 0.]])
    return np.kron(generator, np.eye(2))+np.kron(np.eye(2), rotation)


def integrated_displacement(A, T):
    e = np.eye(len(A))[0]
    return float(e@np.linalg.solve(A, np.linalg.solve(A, (expm(A*T)-np.eye(len(A))-T*A)@e)))


def main():
    p = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    original = json.loads(base.PROTOCOL.read_text(encoding="utf-8"))
    source_path = OUT/"input_scatter_matrices.npz"
    data = np.load(source_path)
    kappa, nu, delta, T = p["kappa"], p["nu"], p["sample_spacing"], p["horizon"]
    times = data["sample_times"]
    parity = np.diag([-1., 1., 1., -1.])
    Q = np.diag([0., 0., 2*nu, 2*nu])
    family, checks = [], []

    def check(name, condition, value):
        checks.append({"name": name, "passed": bool(condition), "value": value})
        if not condition:
            raise AssertionError(name+": "+str(value))

    lyapunov_errors, parity_errors, covariance_errors, sample_errors, derivative_errors, diffusion_errors = [], [], [], [], [], []
    integration_errors, full_stability, hidden_stability, positive_real_samples = [], [], [], []
    for q in p["aliases"]:
        b = 2*np.pi*q/delta
        A = alias_matrix(kappa, nu, b)
        hidden = A[1:, 1:]
        coupling = A[1:, 0]
        full_stability.append(float(np.max(np.linalg.eigvals(A).real)))
        hidden_stability.append(float(np.max(np.linalg.eigvals(hidden).real)))
        lyapunov_errors.append(float(np.max(abs(A+A.T+Q))))
        parity_errors.append(float(np.max(abs(parity@A@parity-A.T))))
        fine = np.linspace(0, 3, 71)
        covariance_errors.append(float(max(abs(expm(A*t)[0, 0]-base.covariance(t, kappa, nu)*np.cos(b*t)) for t in fine)))
        sample_errors.append(float(max(abs(expm(A*t)[0, 0]-base.covariance(t, kappa, nu)) for t in times)))
        acceleration = kappa+b*b
        derivative_errors.append(float(abs(-(A@A)[0, 0]-acceleration)))
        D = kappa*nu/((kappa-b*b)**2+nu*nu*b*b)
        diffusion_errors.append(float(abs(np.linalg.solve(-A, np.eye(4)[0])[0]-D)))
        J = integrated_displacement(A, T)
        numerical = quad(lambda t: (T-t)*base.covariance(t, kappa, nu), 0, T,
                         weight="cos", wvar=b, epsabs=1e-11, epsrel=1e-10)[0]
        integration_errors.append(float(abs(J-numerical)))
        for omega in np.r_[0., np.geomspace(1e-4, 1e4, 200)]:
            gamma = coupling@np.linalg.solve(1j*omega*np.eye(3)-hidden, coupling)
            positive_real_samples.append(float(gamma.real))
        family.append({"alias": q, "frequency_shift": b, "instantaneous_acceleration_variance": acceleration,
                       "dc_diffusivity": D, "displacement_at_horizon": J,
                       "drift_matrix": A.tolist(), "full_maximum_eigenvalue_real_part": full_stability[-1],
                       "hidden_maximum_eigenvalue_real_part": hidden_stability[-1]})
    check("all full alias drifts strictly stable", max(full_stability) < 0, max(full_stability))
    # At q=0 the second velocity is still coupled to its damped auxiliary;
    # the hidden block remains stable even though that pair is unobserved.
    check("all hidden alias drifts strictly stable", max(hidden_stability) < 0, max(hidden_stability))
    check("thermal Gibbs Lyapunov identities", max(lyapunov_errors) < 1e-12, max(lyapunov_errors))
    check("generalized time-reversal parity", max(parity_errors) < 1e-12, max(parity_errors))
    check("Kronecker-product VACF identity", max(covariance_errors) < 1e-10, max(covariance_errors))
    check("all measured velocity covariances match", max(sample_errors) < 1e-10, max(sample_errors))
    check("finite acceleration sum rule", max(derivative_errors) < 1e-10, max(derivative_errors))
    check("positive DC diffusion identity", max(diffusion_errors) < 1e-12 and min(row["dc_diffusivity"] for row in family) > 0, max(diffusion_errors))
    check("integrated displacement versus independent oscillatory quadrature", max(integration_errors) < 1e-9, max(integration_errors))
    check("sampled positive-real memory screen", min(positive_real_samples) >= -1e-10, min(positive_real_samples))
    fd_variance = float(2*(1-base.covariance(delta, kappa, nu))/delta**2)
    check("finite-difference acceleration is smaller than every true acceleration variance",
          0 < fd_variance <= min(row["instantaneous_acceleration_variance"] for row in family), fd_variance)
    report31 = json.loads((OUT/"results.json").read_text(encoding="utf-8"))
    check("saved velocity input hash matches source study", base.sha256(source_path) == report31["hashes"]["input_arrays"], base.sha256(source_path))
    selected = next(row for row in family if row["alias"] == p["tested_alias"])
    actual_J, actual_acceleration = selected["displacement_at_horizon"], selected["instantaneous_acceleration_variance"]
    rng = np.random.default_rng(p["calibration_seed"])
    mask = data["input_ids"][:, 0] == p["ensemble_size"]
    scatter = data["scatter_matrices"][mask]
    ids = data["input_ids"][mask]
    sums = fd_variance*rng.chisquare(p["calibration_samples"], len(scatter))
    invalid_uppers = base.acceleration_upper(sums, p["calibration_samples"], original["confidence"]["acceleration_failure_budget"])
    lower, upper = base.covariance_intervals(scatter, p["ensemble_size"], original["confidence"]["covariance_failure_budget"])
    engine = base.SpectralBounds(times[1:], original["optimization"])
    trials, failures = [], []
    for index, (ident, lo, hi, naive) in enumerate(zip(ids, lower, upper, invalid_uppers)):
        trial = {"replicate": int(ident[1]), "finite_difference_squared_sum": float(sums[index]),
                 "invalid_instantaneous_variance_upper": float(naive), "naive_interval": None,
                 "naive_interval_contains_aliased_truth": None,
                 "oracle_correct_acceleration_interval": None, "oracle_interval_contains_aliased_truth": None}
        try:
            invalid = engine.interval(lo, hi, T, float(naive))
            trial.update({"naive_interval": [invalid["lower"], invalid["upper"]],
                          "naive_interval_contains_aliased_truth": bool(invalid["lower"] <= actual_J <= invalid["upper"]),
                          "naive_certificates": [invalid["upper_certificate"], invalid["negative_certificate"]]})
        except RuntimeError as error:
            failures.append({"replicate": int(ident[1]), "stage": "invalid_finite_difference_transfer", "error": str(error)})
        try:
            valid = engine.interval(lo, hi, T, actual_acceleration)
            trial.update({"oracle_correct_acceleration_interval": [valid["lower"], valid["upper"]],
                          "oracle_interval_contains_aliased_truth": bool(valid["lower"] <= actual_J <= valid["upper"]),
                          "oracle_certificates": [valid["upper_certificate"], valid["negative_certificate"]]})
        except RuntimeError as error:
            failures.append({"replicate": int(ident[1]), "stage": "correct_oracle_control", "error": str(error)})
        trials.append(trial)
    invalid_returned = [row for row in trials if row["naive_interval"] is not None]
    check("every post-hoc stage accounted for",
          len(trials) == len(ids) and len(invalid_returned)+sum(row["oracle_correct_acceleration_interval"] is not None for row in trials)+len(failures) == 2*len(ids),
          {"trials": len(trials), "stage_failures": len(failures)})
    check("correctly supplied physical bound control contains truth", all(row["oracle_interval_contains_aliased_truth"] is True for row in trials), len(trials))
    result = {"study": p["title"], "status": p["status"], "generated_utc": datetime.now(timezone.utc).isoformat(),
              "scope": p["scope"], "family": family, "horizon": T,
              "common_finite_difference_acceleration_variance": fd_variance,
              "tested_alias": selected, "trials": trials, "failures": failures,
              "summary": {"declared_trials": len(ids), "invalid_transfer_intervals_returned": len(invalid_returned),
                          "invalid_transfer_excludes_truth_count": sum(row["naive_interval_contains_aliased_truth"] is False for row in trials),
                          "oracle_truth_inclusion_count": sum(row["oracle_interval_contains_aliased_truth"] is True for row in trials),
                          "median_invalid_variance_upper": float(np.median(invalid_uppers)),
                          "median_naive_lower": float(np.median([row["naive_interval"][0] for row in invalid_returned])) if invalid_returned else None,
                          "median_naive_upper": float(np.median([row["naive_interval"][1] for row in invalid_returned])) if invalid_returned else None},
              "checks": checks, "passed_checks": len(checks),
              "hashes": {"script": base.sha256(__file__), "protocol": base.sha256(PROTOCOL),
                         "source_script": base.sha256(BASE_PATH), "source_protocol": base.sha256(base.PROTOCOL),
                         "source_results": base.sha256(OUT/"results.json"), "source_inputs": base.sha256(source_path)}}
    (OUT/"alias_diagnostic.json").write_text(json.dumps(result, indent=2, allow_nan=False)+"\n", encoding="utf-8")
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.7), constrained_layout=True)
    small_times = np.linspace(0, 3, 1600)
    b = selected["frequency_shift"]
    axes[0].plot(small_times, base.covariance(small_times), color="#0f766e", label="Base thermal model")
    axes[0].plot(small_times, base.covariance(small_times)*np.cos(b*small_times), color="#7c3aed", label="Smooth thermal alias")
    observed = times[times <= 3]
    axes[0].plot(observed, base.covariance(observed), "ko", ms=4, label="Identical sampled values")
    axes[0].set(title="Same observations, hidden rapid motion", xlabel="Time lag", ylabel="Velocity correlation")
    tcurve = np.linspace(.1, 11.4, 200)
    alias_A = np.array(selected["drift_matrix"])
    axes[1].semilogy(tcurve, [base.true_displacement(t) for t in tcurve], color="#0f766e", label="Base displacement response")
    axes[1].semilogy(tcurve, [integrated_displacement(alias_A, t) for t in tcurve], color="#7c3aed", label="Actual aliased response")
    if invalid_returned:
        lo, hi = invalid_returned[0]["naive_interval"]
        axes[1].errorbar(T, (lo+hi)/2, yerr=(hi-lo)/2, fmt="s", color="#b91c1c", capsize=6,
                         label="INVALID finite-difference transfer")
    axes[1].set(title="False confidence from the wrong calibration", xlabel="Prediction horizon", ylabel="Mean displacement per unit step force")
    for ax in axes:
        ax.grid(alpha=.15); ax.legend(fontsize=8)
    fig.suptitle("A finite-difference variance bound is not an instantaneous acceleration bound", fontsize=13)
    fig.savefig(OUT/"acceleration_alias_diagnostic.png", dpi=180)
    plt.close(fig)
    print(json.dumps({"summary": result["summary"], "family": family, "passed_checks": len(checks)}, indent=2))


if __name__ == "__main__":
    main()
