"""Scoped reproduction of Bockius et al.'s subdiffusion memory benchmark.

This implements the correlation-to-memory stages listed in
thermal_memory_reproduction_protocol.json.  It is not the authors' code and
does not implement their Riccati/noise factor or final Lanczos sweep.
"""
from __future__ import annotations

import hashlib
import json
import platform
import warnings
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import scipy
from scipy.integrate import quad
from scipy.linalg import expm, logm, solve_continuous_are
from scipy.special import gamma

HERE = Path(__file__).resolve().parent
PROTOCOL = HERE / "thermal_memory_reproduction_protocol.json"
OUT = HERE / "results" / "thermal_memory_reproduction"


def sha256(path: Path) -> str:
    return hashlib.file_digest(path.open("rb"), "sha256").hexdigest()


def mittag_leffler_3_2(t: float) -> float:
    """E_{3/2}(-t^{3/2}) using its pole-plus-branch-cut representation."""
    if t == 0:
        return 1.0
    pole = (4.0 / 3.0) * np.exp(-t / 2.0) * np.cos(np.sqrt(3.0) * t / 2.0)

    def transformed_integrand(x: float) -> float:
        r = x / (1.0 - x)
        density = -np.sqrt(r) / (np.pi * (r**3 + 1.0))
        return density * np.exp(-r * t) / (1.0 - x) ** 2

    branch = quad(transformed_integrand, 0.0, 1.0, epsabs=2e-13,
                  epsrel=2e-13, limit=500)[0]
    return float(pole + branch)


def mittag_leffler_series(t: float) -> float:
    total = 0.0
    for k in range(100):
        term = (-t**1.5) ** k / gamma(1.5 * k + 1.0)
        total += term
        if abs(term) < 1e-17:
            break
    return float(total)


def pad_sum(*polynomials: np.ndarray) -> np.ndarray:
    result = np.zeros(max(len(p) for p in polynomials))
    for polynomial in polynomials:
        result[:len(polynomial)] += polynomial
    return result


def x_times(polynomial: np.ndarray) -> np.ndarray:
    return np.r_[0.0, polynomial]


def phi(polynomial: np.ndarray, moments: np.ndarray) -> float:
    return float(polynomial @ moments[:len(polynomial)])


def dphi(polynomial: np.ndarray) -> float:
    return float(polynomial[1]) if len(polynomial) > 1 else 0.0


def jacobi_and_derivative(moments: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Appendix C, Algorithm 2, including differentiation with respect to y1."""
    n = len(moments) // 2
    jacobi = np.zeros((n, n))
    derivative = np.zeros_like(jacobi)
    u_minus_two = np.array([0.0])
    du_minus_two = np.array([0.0])
    u_minus_one = np.array([1.0 / np.sqrt(abs(moments[0]))])
    du_minus_one = np.array([0.0])
    alpha = moments[1] / moments[0]
    dalpha = 1.0 / moments[0]
    gamma_i = dgamma = 0.0
    sigma = 1.0
    jacobi[0, 0] = alpha
    derivative[0, 0] = dalpha

    for i in range(1, n):
        raw = pad_sum(x_times(u_minus_one), -alpha * u_minus_one,
                      -sigma * gamma_i * u_minus_two)
        draw = pad_sum(x_times(du_minus_one), -dalpha * u_minus_one,
                       -alpha * du_minus_one, -sigma * dgamma * u_minus_two,
                       -sigma * gamma_i * du_minus_two)
        raw_squared = np.convolve(raw, raw)
        norm_form = phi(raw_squared, moments)
        gamma_i = np.sqrt(abs(norm_form))
        if gamma_i == 0:
            raise RuntimeError("Lanczos polynomial recurrence broke down")
        dgamma = np.sign(norm_form) / (2.0 * gamma_i) * (
            phi(2.0 * np.convolve(raw, draw), moments) + dphi(raw_squared))
        u_i = raw / gamma_i
        du_i = pad_sum(gamma_i * draw, -dgamma * raw) / gamma_i**2
        u_squared = np.convolve(u_i, u_i)
        xu_squared = x_times(u_squared)
        denominator = phi(u_squared, moments)
        numerator = phi(xu_squared, moments)
        alpha = numerator / denominator
        dalpha = (
            denominator * (phi(2.0 * x_times(np.convolve(u_i, du_i)), moments)
                           + dphi(xu_squared))
            - numerator * (phi(2.0 * np.convolve(u_i, du_i), moments)
                           + dphi(u_squared))
        ) / denominator**2
        sigma = denominator / phi(np.convolve(u_minus_one, u_minus_one), moments)
        jacobi[i, i] = alpha
        derivative[i, i] = dalpha
        jacobi[i, i - 1] = sigma * gamma_i
        derivative[i, i - 1] = sigma * dgamma
        jacobi[i - 1, i] = gamma_i
        derivative[i - 1, i] = dgamma
        u_minus_two, u_minus_one = u_minus_one, u_i
        du_minus_two, du_minus_one = du_minus_one, du_i
    return jacobi, derivative


def system_and_frechet(jacobi: np.ndarray, derivative: np.ndarray,
                       tau: float) -> tuple[np.ndarray, np.ndarray]:
    zeros = np.zeros_like(jacobi)
    block = np.block([[jacobi, derivative], [zeros, jacobi]])
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        logged = logm(block) / tau
    n = len(jacobi)
    return logged[:n, :n], logged[:n, n:]


def constrained_realization(original: np.ndarray, tau: float, tolerance: float,
                            maximum: int) -> dict:
    moments = original.copy()
    history = []
    for iteration in range(maximum):
        jacobi, derivative = jacobi_and_derivative(moments)
        system, dsystem = system_and_frechet(jacobi, derivative, tau)
        residual = float(np.real(system[0, 0]))
        slope = float(np.real(dsystem[0, 0]))
        history.append({"iteration": iteration, "y1": float(moments[1]),
                        "residual": residual, "derivative": slope})
        if abs(residual) <= tolerance:
            break
        moments[1] -= residual / slope
    else:
        raise RuntimeError("Newton constraint did not converge")
    jacobi, derivative = jacobi_and_derivative(moments)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        system = logm(jacobi) / tau
    if np.max(abs(np.imag(system))) > 1e-7:
        raise RuntimeError("primary realization was not numerically real")
    return {"moments": moments, "jacobi": jacobi, "system": np.real(system),
            "history": history}


def moment_error(jacobi: np.ndarray, moments: np.ndarray) -> float:
    e1 = np.eye(len(jacobi))[0]
    return float(max(abs(e1 @ np.linalg.matrix_power(jacobi, k) @ e1 - moments[k])
                     for k in range(len(moments))))


def nonsymmetric_lanczos(matrix: np.ndarray) -> dict:
    """Biorthogonal Lanczos sweep initialized with the first basis vector."""
    size = len(matrix)
    right = np.zeros((size, size))
    left = np.zeros((size, size))
    right[:, 0] = left[:, 0] = np.eye(size)[0]
    right_previous = np.zeros(size)
    left_previous = np.zeros(size)
    beta = gamma_i = 0.0
    for j in range(size - 1):
        v, w = right[:, j], left[:, j]
        alpha = float(w @ matrix @ v)
        r = matrix @ v - alpha * v - gamma_i * right_previous
        s = matrix.T @ w - alpha * w - beta * left_previous
        product = float(s @ r)
        if product == 0.0:
            raise RuntimeError("nonsymmetric Lanczos sweep broke down")
        beta_next = np.sign(product) * np.sqrt(abs(product))
        gamma_next = np.sqrt(abs(product))
        right[:, j + 1] = r / beta_next
        left[:, j + 1] = s / gamma_next
        right_previous, left_previous = v, w
        beta, gamma_i = beta_next, gamma_next
    inverse = np.linalg.inv(right)
    tridiagonal = inverse @ matrix @ right
    return {"right": right, "left": left, "inverse": inverse,
            "tridiagonal": tridiagonal}


def main() -> None:
    protocol = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    OUT.mkdir(parents=True, exist_ok=True)
    gates = protocol["regression_gates"]
    evaluation = protocol["evaluation"]
    checks: list[dict] = []

    def check(name: str, condition: bool, value: float | int | str) -> None:
        checks.append({"name": name, "passed": bool(condition), "value": value})
        if not condition:
            raise AssertionError(f"{name}: {value}")

    series_points = np.linspace(0.0, 5.0, 21)
    series_error = max(abs(mittag_leffler_3_2(float(t)) - mittag_leffler_series(float(t)))
                       for t in series_points)
    check("integral target agrees with defining Mittag-Leffler series",
          series_error <= gates["mittag_leffler_series_max_abs_error"], series_error)

    tau, n = 0.6, 10
    original = np.array([mittag_leffler_3_2(k * tau) for k in range(2 * n)])
    fit = constrained_realization(original, tau, evaluation["newton_tolerance"],
                                  evaluation["newton_max_iterations"])
    moments, jacobi, system = fit["moments"], fit["jacobi"], fit["system"]
    eig_j = np.linalg.eigvals(jacobi)
    eig_a = np.linalg.eigvals(system)
    final_constraint = abs(system[0, 0])
    jacobi_moment_error = moment_error(jacobi, moments)
    check("normalized target starts at one", original[0] == 1.0, original[0])
    check("Jacobi moment identities", jacobi_moment_error <= gates["moment_identity_max_abs_error"],
          jacobi_moment_error)
    check("Newton derivative constraint", final_constraint <= gates["newton_constraint_abs_residual"],
          final_constraint)
    check("Newton y1 perturbation remains small", abs(moments[1] - original[1]) <=
          gates["primary_y1_abs_perturbation"], abs(moments[1] - original[1]))
    check("no primary discrete pole lies on or outside unit circle",
          np.max(abs(eig_j)) < 1.0, float(np.max(abs(eig_j))))
    check("no primary discrete pole is negative real",
          not np.any((abs(np.imag(eig_j)) < 1e-10) & (np.real(eig_j) < 0)),
          int(np.sum((abs(np.imag(eig_j)) < 1e-10) & (np.real(eig_j) < 0))))
    max_real_eigenvalue = float(np.max(np.real(eig_a)))
    check("primary continuous realization is stable", max_real_eigenvalue <=
          gates["primary_max_real_system_eigenvalue"], max_real_eigenvalue)

    t_vacf = np.linspace(*evaluation["dense_vacf_interval"],
                         evaluation["dense_vacf_points"])
    e1 = np.eye(n)[0]
    vacf_true = np.array([mittag_leffler_3_2(float(t)) for t in t_vacf])
    vacf_fit = np.array([float(e1 @ expm(t * system) @ e1) for t in t_vacf])
    vacf_rmse = float(np.sqrt(np.mean((vacf_fit - vacf_true) ** 2)))
    check("dense primary VACF reproduction", vacf_rmse <= gates["primary_dense_vacf_rmse"],
          vacf_rmse)
    sample_fit = np.array([float(e1 @ expm(k * tau * system) @ e1) for k in range(2 * n)])
    sample_error_adjusted = float(np.max(abs(sample_fit - moments)))
    check("adjusted samples interpolate", sample_error_adjusted <= 1e-8,
          sample_error_adjusted)

    b = system[0, 1:]
    c = -system[1:, 0]
    a0 = system[1:, 1:]
    t_kernel = np.geomspace(*evaluation["kernel_interval"], evaluation["kernel_points"])
    kernel_true = 1.0 / np.sqrt(np.pi * t_kernel)
    kernel_fit = np.array([float(b @ expm(t * a0) @ c) for t in t_kernel])
    check("reconstructed kernel is positive on evaluation interval",
          np.min(kernel_fit) > 0.0, float(np.min(kernel_fit)))
    kernel_log_rmse = float(np.sqrt(np.mean(np.log(kernel_fit / kernel_true) ** 2)))
    check("kernel shape reproduction", kernel_log_rmse <= gates["primary_kernel_log_rmse"],
          kernel_log_rmse)

    omega = np.geomspace(*evaluation["frequency_interval"],
                         evaluation["frequency_points"])
    identity = np.eye(n - 1)
    positive_real = np.array([float(np.real(b @ np.linalg.solve(1j * w * identity - a0, c)))
                              for w in omega])
    positive_real_min = float(np.min(positive_real))
    check("sampled positive-real diagnostic", positive_real_min >=
          gates["primary_sampled_positive_real_min"], positive_real_min)
    check("auxiliary block is stable", np.max(np.real(np.linalg.eigvals(a0))) < 0.0,
          float(np.max(np.real(np.linalg.eigvals(a0)))))

    # Paper Eq. 62 is an indefinite continuous-time algebraic Riccati equation.
    # In SciPy's convention choose A=B^T and R=-1 so that the quadratic term
    # has the positive sign used by Bockius et al.
    delta = evaluation["regularization_delta_recorded_but_not_used_in_kernel"]
    riccati_b = 2.0 * delta * a0 - np.outer(c, b)
    sigma0 = solve_continuous_are(riccati_b.T, b[:, None], np.outer(c, c),
                                  np.array([[-1.0]]))
    sigma0 = (sigma0 + sigma0.T) / 2.0
    riccati_residual_matrix = (riccati_b @ sigma0 + sigma0 @ riccati_b.T
                               + sigma0 @ np.outer(b, b) @ sigma0 + np.outer(c, c))
    riccati_residual = float(np.linalg.norm(riccati_residual_matrix, ord="fro"))
    sigma0_min_eigenvalue = float(np.min(np.linalg.eigvalsh(sigma0)))
    check("regularized Riccati equation residual", riccati_residual <=
          gates["primary_riccati_residual_frobenius"], riccati_residual)
    check("auxiliary covariance is positive semidefinite", sigma0_min_eigenvalue >=
          gates["primary_covariance_min_eigenvalue"], sigma0_min_eigenvalue)

    regularized_system = system.copy()
    regularized_system[0, 0] = -delta
    covariance = np.zeros_like(system)
    covariance[0, 0] = 1.0
    covariance[1:, 1:] = sigma0
    noise_factor = np.r_[2.0 * delta, c - sigma0 @ b] / np.sqrt(2.0 * delta)
    lyapunov_matrix = (regularized_system @ covariance
                       + covariance @ regularized_system.T
                       + np.outer(noise_factor, noise_factor))
    lyapunov_residual = float(np.linalg.norm(lyapunov_matrix, ord="fro"))
    check("full stationary Lyapunov identity", lyapunov_residual <=
          gates["primary_lyapunov_residual_frobenius"], lyapunov_residual)
    check("stationary covariance has required first column",
          np.max(abs(covariance @ e1 - e1)) <= 1e-12,
          float(np.max(abs(covariance @ e1 - e1))))
    regularized_max_real = float(np.max(np.real(np.linalg.eigvals(regularized_system))))
    check("regularized stochastic realization is stable", regularized_max_real < 0.0,
          regularized_max_real)
    regularized_vacf = np.array([
        float(e1 @ expm(t * regularized_system) @ covariance @ e1) for t in t_vacf])
    regularized_vacf_rmse = float(np.sqrt(np.mean((regularized_vacf - vacf_true) ** 2)))
    check("regularized stationary VACF reproduction", regularized_vacf_rmse <=
          gates["primary_regularized_vacf_rmse"], regularized_vacf_rmse)

    lanczos = nonsymmetric_lanczos(regularized_system)
    transform, inverse, tri = (lanczos["right"], lanczos["inverse"],
                               lanczos["tridiagonal"])
    biorthogonality_error = float(np.max(abs(lanczos["left"].T @ transform
                                               - np.eye(n))))
    similarity_error = float(np.linalg.norm(regularized_system @ transform
                                            - transform @ tri, ord="fro"))
    off_band = abs(np.arange(n)[:, None] - np.arange(n)[None, :]) > 1
    off_tridiagonal_error = float(np.max(abs(tri[off_band])))
    block_structure_error = float(max(np.max(abs(transform[0, 1:])),
                                      np.max(abs(inverse[0, 1:])),
                                      np.max(abs(inverse[1:, 0]))))
    coupling = float(np.sqrt(b @ c))
    coupling_error = float(max(abs(tri[0, 1] - coupling),
                               abs(tri[1, 0] + coupling)))
    check("Lanczos biorthogonality residual", biorthogonality_error <=
          gates["lanczos_biorthogonality_max_abs_error"], biorthogonality_error)
    check("Lanczos similarity residual", similarity_error <=
          gates["lanczos_similarity_frobenius_error"], similarity_error)
    check("Lanczos off-tridiagonal leakage", off_tridiagonal_error <=
          gates["lanczos_off_tridiagonal_max_abs"], off_tridiagonal_error)
    check("Lanczos preserves first-coordinate block structure", block_structure_error <=
          gates["lanczos_block_structure_max_abs_error"], block_structure_error)
    check("Lanczos produces signed first coupling", coupling_error <=
          gates["lanczos_first_coupling_max_abs_error"], coupling_error)
    tri_a0 = tri[1:, 1:]
    tri_kernel = coupling**2 * np.array([
        float(np.eye(n - 1)[0] @ expm(t * tri_a0) @ np.eye(n - 1)[0])
        for t in t_kernel])
    lanczos_kernel_error = float(np.max(abs(tri_kernel - kernel_fit)))
    check("Lanczos similarity preserves memory kernel", lanczos_kernel_error <=
          gates["lanczos_kernel_max_abs_error"], lanczos_kernel_error)
    transformed_covariance = inverse @ covariance @ inverse.T
    transformed_noise = inverse @ noise_factor
    transformed_lyapunov_error = float(np.linalg.norm(
        tri @ transformed_covariance + transformed_covariance @ tri.T
        + np.outer(transformed_noise, transformed_noise), ord="fro"))
    check("Lanczos coordinates preserve Lyapunov identity", transformed_lyapunov_error <=
          gates["lanczos_transformed_lyapunov_frobenius_error"],
          transformed_lyapunov_error)

    coarse_tau, coarse_n = 1.0, 6
    coarse_moments = np.array([mittag_leffler_3_2(k * coarse_tau)
                               for k in range(2 * coarse_n)])
    coarse_jacobi, _ = jacobi_and_derivative(coarse_moments)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        coarse_system = np.real_if_close(logm(coarse_jacobi) / coarse_tau, tol=1000)
    coarse_derivative = float(np.real(coarse_system[0, 0]))
    coarse_target = gates["coarse_unconstrained_derivative_target"]
    check("coarse-grid unconstrained derivative reproduces reported value",
          abs(coarse_derivative - coarse_target) <=
          gates["coarse_unconstrained_derivative_tolerance"], coarse_derivative)
    check("coarse moment identities", moment_error(coarse_jacobi, coarse_moments) <=
          gates["moment_identity_max_abs_error"], moment_error(coarse_jacobi, coarse_moments))

    fig, axes = plt.subplots(2, 2, figsize=(12, 8.2))
    ax = axes[0, 0]
    ax.plot(t_vacf, vacf_true, color="black", lw=2, label="exact VACF")
    ax.plot(t_vacf, vacf_fit, color="#0072B2", lw=1.5, ls="--", label="reconstruction")
    ax.scatter(np.arange(2 * n) * tau, original, s=18, color="#D55E00",
               label="published-grid samples", zorder=3)
    ax.set(xlabel="time", ylabel="normalized VACF", title="Published case: tau=0.6, n=10")
    ax.legend(frameon=False, fontsize=8)
    ax = axes[0, 1]
    near = t_vacf <= 2.0
    ax.plot(t_vacf[near], vacf_true[near], color="black", lw=2)
    ax.plot(t_vacf[near], vacf_fit[near], color="#0072B2", lw=1.5, ls="--")
    ax.scatter(np.arange(4) * tau, original[:4], s=25, color="#D55E00", zorder=3)
    ax.set(xlabel="time", ylabel="normalized VACF", title="Short-time mismatch is visible only on zoom")
    ax = axes[1, 0]
    ax.loglog(t_kernel, kernel_true, color="black", lw=2, label="exact singular kernel")
    ax.loglog(t_kernel, kernel_fit, color="#009E73", lw=1.6, ls="--",
              label="finite-state reconstruction")
    ax.set(xlabel="time", ylabel="memory kernel", title="Kernel recovery (finite model cannot diverge at zero)")
    ax.legend(frameon=False, fontsize=8)
    ax = axes[1, 1]
    ax.semilogx(omega, positive_real, color="#CC79A7", lw=1.6)
    ax.axhline(0.0, color="black", lw=0.8)
    ax.set(xlabel="angular frequency", ylabel="Re kappa(i omega)",
           title="Sampled positive-real diagnostic")
    fig.suptitle("Scoped reproduction of Bockius et al. (2021)", fontsize=14)
    fig.tight_layout()
    fig.savefig(OUT / "thermal_memory_reproduction.png", dpi=180)
    plt.close(fig)

    np.savez_compressed(OUT / "curves.npz", t_vacf=t_vacf, vacf_true=vacf_true,
                        vacf_fit=vacf_fit, t_kernel=t_kernel, kernel_true=kernel_true,
                        kernel_fit=kernel_fit, omega=omega, positive_real=positive_real,
                        original_samples=original, adjusted_samples=moments,
                        jacobi=jacobi, system=system, sigma0=sigma0,
                        covariance=covariance, noise_factor=noise_factor,
                        regularized_system=regularized_system,
                        regularized_vacf=regularized_vacf, transform=transform,
                        inverse_transform=inverse, tridiagonal_system=tri,
                        transformed_covariance=transformed_covariance,
                        transformed_noise=transformed_noise, tri_kernel=tri_kernel)
    result = {
        "study": protocol["title"],
        "protocol_version": protocol["version"],
        "protocol_sha256": sha256(PROTOCOL),
        "script_sha256": sha256(Path(__file__)),
        "environment": {"python": platform.python_version(), "numpy": np.__version__,
                        "scipy": scipy.__version__, "matplotlib": matplotlib.__version__},
        "scope": protocol["implementation_scope"],
        "primary": {
            "tau": tau, "n": n, "newton_history": fit["history"],
            "y1_original": float(original[1]), "y1_adjusted": float(moments[1]),
            "jacobi_moment_max_abs_error": jacobi_moment_error,
            "constraint_abs_residual": final_constraint,
            "max_discrete_pole_modulus": float(np.max(abs(eig_j))),
            "max_real_system_eigenvalue": max_real_eigenvalue,
            "vacf_dense_rmse_0_30": vacf_rmse,
            "vacf_adjusted_sample_max_abs_error": sample_error_adjusted,
            "kernel_log_rmse_0p05_12": kernel_log_rmse,
            "sampled_positive_real_min": positive_real_min,
            "riccati_residual_frobenius": riccati_residual,
            "sigma0_min_eigenvalue": sigma0_min_eigenvalue,
            "lyapunov_residual_frobenius": lyapunov_residual,
            "regularized_max_real_system_eigenvalue": regularized_max_real,
            "regularized_stationary_vacf_rmse_0_30": regularized_vacf_rmse,
            "noise_factor_norm": float(np.linalg.norm(noise_factor)),
            "lanczos_biorthogonality_max_abs_error": biorthogonality_error,
            "lanczos_similarity_frobenius_error": similarity_error,
            "lanczos_off_tridiagonal_max_abs": off_tridiagonal_error,
            "lanczos_block_structure_max_abs_error": block_structure_error,
            "lanczos_coupling_k": coupling,
            "lanczos_first_coupling_max_abs_error": coupling_error,
            "lanczos_kernel_max_abs_error": lanczos_kernel_error,
            "lanczos_transformed_lyapunov_frobenius_error": transformed_lyapunov_error,
            "kernel_at_zero_finite": float(b @ c),
            "exact_kernel_limit_at_zero": "positive infinity"
        },
        "negative_control": {"tau": coarse_tau, "n": coarse_n,
                             "unconstrained_derivative": coarse_derivative,
                             "paper_reported_rounded_value": coarse_target},
        "checks": checks,
        "passed_checks": sum(item["passed"] for item in checks),
        "interpretation": "Method-faithful scoped reproduction, not authors' code or a full Algorithm 1 implementation"
    }
    (OUT / "results.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
