"""Exploratory information limit for a known tempered fractional-memory family.

Deterministic population calculations, not simulated test outcomes or new physics.
The exact Gaussian experiment is more informative than the normalized VACF used
by Lab 28: no fitting, estimator compression, or measurement noise is involved.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import platform
from datetime import datetime, timezone
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import scipy
from scipy.integrate import quad
from scipy.linalg import eigvalsh, solve_triangular, toeplitz
from scipy.special import erfcx

HERE = Path(__file__).resolve().parent
PROTOCOL = HERE / "tempered_memory_boundary_protocol.json"
OUT = HERE / "results" / "tempered_memory_boundary"


def sha256(path):
    with Path(path).open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


class Correlation:
    """Exact inverse transform on the declared small-cutoff domain.

    Put z=sqrt(s+epsilon). Ctilde=z/(z^3-epsilon*z+1).
    If r_j are its simple cubic roots and a_j=r_j/(3*r_j^2-epsilon),
    then C(t)=exp(-epsilon*t)*sum_j a_j*r_j*erfcx(-r_j*sqrt(t)).
    The 1/sqrt(pi*t) partial-fraction terms cancel because sum_j a_j=0.
    """

    def __init__(self, epsilon):
        self.epsilon = float(epsilon)
        if not 0 <= self.epsilon <= 0.1:
            raise ValueError("Validated implementation domain is 0 <= epsilon <= 0.1")
        self.roots = np.roots([1.0, 0.0, -self.epsilon, 1.0]).astype(complex)
        self.weights = self.roots / (3*self.roots**2-self.epsilon)

    def complex_value(self, times):
        t = np.asarray(times, dtype=float)
        if np.any(t < 0):
            raise ValueError("Use nonnegative time lags")
        r = self.roots
        return np.exp(-self.epsilon*t) * np.sum(
            self.weights*r*erfcx(-np.sqrt(t)[..., None]*r), axis=-1)

    def __call__(self, times):
        value = self.complex_value(times)
        if not np.all(np.isfinite(value)) or np.max(np.abs(value.imag)) > 1e-10:
            raise ArithmeticError("Nonfinite or nonreal analytic covariance")
        real = value.real
        return float(real) if real.ndim == 0 else real

    def derivative(self, time):
        # The 1/sqrt(t) derivative terms cancel: sum_j a_j*r_j^2=0.
        r = self.roots
        value = np.exp(-self.epsilon*time) * np.sum(
            self.weights*r*(r*r-self.epsilon)*erfcx(-r*np.sqrt(time)))
        if not np.isfinite(value) or abs(value.imag) > 1e-10:
            raise ArithmeticError("Nonfinite or nonreal analytic derivative")
        return float(value.real)

    def transform(self, s):
        return 1/(s+1/np.sqrt(s+self.epsilon))


def stable_log_remainder(a):
    """Compute a-log(1+a) without subtracting two nearly equal numbers."""
    a = np.asarray(a)
    out = a-np.log1p(a)
    small = np.abs(a) < 1e-4
    out[small] = sum((-1)**k * a[small]**k/k for k in range(2, 13))
    return out


def gaussian_kl(K_alt, K_null):
    """KL(N(0,K_alt) || N(0,K_null)), and whitened difference spectrum."""
    L = np.linalg.cholesky(K_null)
    left = solve_triangular(L, K_alt-K_null, lower=True)
    whitened = solve_triangular(L, left.T, lower=True).T
    whitened = (whitened+whitened.T)/2
    shifts = np.linalg.eigvalsh(whitened)
    if np.min(shifts) <= -1:
        raise ValueError("Alternative covariance is not positive definite")
    return float(0.5*np.sum(stable_log_remainder(shifts))), shifts


def main():
    p = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    reference_path = HERE / "27_thermal_memory_reproduction.py"
    spec = importlib.util.spec_from_file_location("clean_memory_reference", reference_path)
    reference = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(reference)
    checks = []

    def check(name, condition, value):
        checks.append({"name": name, "passed": bool(condition), "value": value})
        if not condition:
            raise AssertionError(f"{name}: {value}")

    n = p["samples_per_trajectory"]
    sample_times = p["sample_spacing"]*np.arange(n)
    T = float(sample_times[-1])
    curve_times = np.linspace(0, T, p["curve_points"])
    cutoffs = [p["null_cutoff"]]+p["cutoffs"]
    correlations = {eps: Correlation(eps) for eps in cutoffs}
    C0 = correlations[0.0]
    null_covariance = toeplitz(C0(sample_times))
    min_eigenvalue = float(eigvalsh(null_covariance)[0])
    check("strictly positive null sampled covariance", min_eigenvalue > 0.09, min_eigenvalue)

    root_residual = max(float(np.max(abs(c.roots**3-eps*c.roots+1)))
                        for eps, c in correlations.items())
    check("cubic root residuals", root_residual < 1e-12, root_residual)
    initial_error = max(abs(c(0)-1)+abs(c.derivative(0)) for c in correlations.values())
    check("unit initial variance and zero initial VACF derivative", initial_error < 1e-12, initial_error)
    imaginary_error = max(float(np.max(abs(c.complex_value(curve_times).imag)))
                          for c in correlations.values())
    check("conjugate cancellation on evaluation curves", imaginary_error < 1e-12, imaginary_error)
    reference_times = np.unique(np.r_[sample_times, [.05, .1, 1, 5, 20, 50]])
    reference_error = float(max(abs(C0(t)-reference.mittag_leffler_3_2(float(t)))
                                for t in reference_times))
    check("zero cutoff versus independent pole-and-cut reference", reference_error < 1e-10, reference_error)

    volterra_errors, laplace_errors, derivative_errors = [], [], []
    for eps in p["validation_cutoffs"]:
        c = correlations[eps]
        for t in p["validation_times"]:
            # u=x^2 removes the integrable square-root singularity in gamma.
            integral = 2/np.sqrt(np.pi)*quad(
                lambda x: np.exp(-eps*x*x)*c(max(0., t-x*x)),
                0, np.sqrt(t), epsabs=1e-11, epsrel=1e-11)[0]
            volterra_errors.append(abs(c.derivative(t)+integral))
            h = 1e-5*min(t, 1.)
            derivative_errors.append(abs(c.derivative(t)-(c(t+h)-c(t-h))/(2*h)))
        for s in p["validation_laplace_arguments"]:
            numeric = quad(lambda t: np.exp(-s*t)*c(t), 0, np.inf,
                           epsabs=1e-11, epsrel=1e-11)[0]
            laplace_errors.append(abs(numeric-c.transform(s)))
    check("independent smooth Volterra convolution residual", max(volterra_errors) < 1e-9, max(volterra_errors))
    check("analytic derivative versus centered differences", max(derivative_errors) < 1e-8, max(derivative_errors))
    check("quadrature Laplace transform versus declared mobility", max(laplace_errors) < 1e-9, max(laplace_errors))

    identical_kl, _ = gaussian_kl(null_covariance, null_covariance)
    check("zero KL for identical covariance", identical_kl == 0, identical_kl)
    rows, covariances, curves, mobilities = [], [], [], []
    fg = p["frequency_grid"]
    omega = np.geomspace(fg["minimum"], fg["maximum"], fg["points"])
    direct_errors, generalized_errors, bound_ratios, min_eigenvalues = [], [], [], []
    b = 4/(15*np.sqrt(np.pi))
    for eps, c in correlations.items():
        K = toeplitz(c(sample_times))
        values = c(curve_times)
        response = c.transform(1j*omega)
        covariances.append(K)
        curves.append(values)
        mobilities.append(response)
        min_eigenvalues.append(float(eigvalsh(K)[0]))
        if eps == 0:
            continue
        kl, shifts = gaussian_kl(K, null_covariance)
        direct = .5*(np.trace(np.linalg.solve(null_covariance, K))-n
                     +np.linalg.slogdet(null_covariance)[1]-np.linalg.slogdet(K)[1])
        generalized = .5*np.sum(stable_log_remainder(eigvalsh(K, null_covariance)-1))
        direct_errors.append(abs(kl-direct))
        generalized_errors.append(abs(kl-generalized))
        bound = b*eps*curve_times[1:]**2.5
        bound_ratios.append(float(np.max(abs(values[1:]-C0(curve_times[1:]))/bound)))
        power_bounds = {str(M): min(1., p["test_size"]+np.sqrt(M*kl/2))
                        for M in p["ensemble_sizes"]}
        rows.append({"cutoff": eps, "memory_cutoff_timescale": 1/eps,
                     "asymptotic_msd_exponent": 1.0, "diffusivity": np.sqrt(eps),
                     "maximum_sampled_covariance_difference": float(np.max(abs(K-null_covariance))),
                     "kl_per_trajectory": kl,
                     "whitened_difference_eigenvalues": shifts.tolist(),
                     "power_upper_bound_by_independent_trajectories": power_bounds})
    check("all alternative sampled covariances positive definite", min(min_eigenvalues) > 0, min(min_eigenvalues))
    check("stable KL versus direct trace-logdet formula", max(direct_errors) < 1e-12, max(direct_errors))
    check("stable KL versus generalized covariance eigenvalues", max(generalized_errors) < 1e-12, max(generalized_errors))
    check("positive KL for every positive declared cutoff", min(row["kl_per_trajectory"] for row in rows) > 0,
          min(row["kl_per_trajectory"] for row in rows))
    check("sampled verification of proved finite-window bound", max(bound_ratios) <= 1+1e-6, max(bound_ratios))
    dc_error = max(abs(c.transform(0)-np.sqrt(eps)) for eps, c in correlations.items() if eps > 0)
    check("finite-cutoff DC mobility identity", dc_error < 1e-15, dc_error)
    null_dc_ratio = abs(C0.transform(1j*1e-12))/np.sqrt(1e-12)
    check("zero-cutoff low-frequency square-root response", abs(null_dc_ratio-1) < 1e-10, null_dc_ratio)

    OUT.mkdir(parents=True, exist_ok=True)
    array_path = OUT / "curves_and_covariances.npz"
    np.savez_compressed(array_path, cutoffs=cutoffs, sample_times=sample_times,
                        curve_times=curve_times, covariances=covariances, correlations=curves,
                        frequencies=omega, mobilities=mobilities)
    report = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "status": p["status"], "observation_model": p["observation_model"],
        "bound_interpretation": p["bound"], "null_cutoff": 0.0,
        "null_asymptotic_msd_exponent": 0.5, "null_diffusivity": 0.0,
        "sample_times": sample_times.tolist(), "test_size": p["test_size"],
        "null_minimum_covariance_eigenvalue": min_eigenvalue,
        "finite_window_bound_coefficient": b, "cases": rows, "checks": checks,
        "hashes": {"script": sha256(__file__), "protocol": sha256(PROTOCOL),
                   "independent_reference_script": sha256(reference_path),
                   "saved_arrays": sha256(array_path)},
        "environment": {"python": platform.python_version(), "numpy": np.__version__,
                        "scipy": scipy.__version__, "matplotlib": matplotlib.__version__},
        "scope_limits": p["scope_limits"]}
    (OUT / "results.json").write_text(json.dumps(report, indent=2, allow_nan=False)+"\n", encoding="utf-8")

    plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
    fig, axes = plt.subplots(2, 2, figsize=(12.5, 8.8), constrained_layout=True)
    selected = p["plot_cutoffs"]
    palette = ["#d97706", "#0f766e", "#7c3aed"]
    axes[0, 0].plot(curve_times, C0(curve_times), color="#172554", lw=2.4, label="No cutoff")
    axes[1, 1].loglog(omega, abs(C0.transform(1j*omega)), color="#172554", lw=2.4, label="No cutoff")
    for eps, color in zip(selected, palette):
        c = correlations[eps]
        label = f"cutoff {eps:g}"
        axes[0, 0].plot(curve_times, c(curve_times), color=color, ls="--", lw=1.4, label=label)
        axes[0, 1].semilogy(curve_times[1:], abs(c(curve_times[1:])-C0(curve_times[1:])), color=color, label=label)
        axes[1, 1].loglog(omega, abs(c.transform(1j*omega)), color=color, label=label)
    eps_values = [row["cutoff"] for row in rows]
    for M, color in zip(p["ensemble_sizes"], ["#94a3b8", "#0284c7", "#0f766e", "#172554"]):
        bounds = [row["power_upper_bound_by_independent_trajectories"][str(M)] for row in rows]
        axes[1, 0].semilogx(eps_values, bounds, "o-", color=color, label=f"{M:,} trajectories")
    axes[1, 0].axhline(p["test_size"], color="#b91c1c", ls=":", label="5% false-positive limit")
    axes[0, 0].set(title="Almost overlapping measured correlations", xlabel="Time lag", ylabel="Normalized velocity correlation")
    axes[0, 1].set(title="Small but nonzero differences", xlabel="Time lag", ylabel="Absolute correlation difference")
    axes[1, 0].set(title="Upper bound on any test's detection power", xlabel="Positive memory cutoff", ylabel="Power bound (not achieved power)", ylim=(0, 1.04))
    axes[1, 1].set(title="Different zero-frequency behavior", xlabel="Angular frequency", ylabel="Velocity mobility magnitude")
    for ax in axes.flat:
        ax.grid(alpha=.16)
        ax.legend(fontsize=8, loc="best")
    fig.suptitle("Finite observations do not uniformly determine the infinite-time diffusion class\n"
                 "20 equilibrium velocity samples per independent trajectory; dimensionless Gaussian model", fontsize=14)
    fig.savefig(OUT / "tempered_memory_boundary.png", dpi=175)
    plt.close(fig)
    print(json.dumps({"checks_passed": len(checks), "cases": rows}, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
