"""Kernel-free displacement confidence bounds: established moment duals applied
to a Gaussian equilibrium example with extra acceleration information.

The continuum correction and tail condition are essential: grid extrema alone
are not confidence bounds over an unbounded continuous-frequency spectrum.
"""
from __future__ import annotations

import hashlib
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
from scipy.linalg import expm, toeplitz
from scipy.optimize import linprog
from scipy.stats import chi2

HERE = Path(__file__).resolve().parent
PROTOCOL = HERE / "spectral_response_protocol.json"
OUT = HERE / "results" / "spectral_response"


def sha256(path):
    with Path(path).open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def covariance(times, kappa=1., nu=1.):
    times = np.asarray(times)
    beta = np.sqrt(complex(kappa-nu*nu/4))
    if abs(beta) < 1e-10:
        return np.exp(-nu*times/2)*(1+nu*times/2)
    values = np.exp(-nu*times/2)*(np.cos(beta*times)+nu/(2*beta)*np.sin(beta*times))
    if np.max(abs(values.imag)) > 1e-11:
        raise ArithmeticError("Complex covariance residual")
    return values.real


def true_displacement(T, kappa=1., nu=1.):
    A = np.array([[0., -1.], [kappa, -nu]])
    e = np.array([1., 0.])
    return float(e@np.linalg.solve(A, np.linalg.solve(A, (expm(A*T)-np.eye(2)-A*T)@e)))


def spectral_integrand(omega, T):
    # np.sinc(x)=sin(pi*x)/(pi*x); avoids cancellation at omega=0.
    return 0.5*T*T*np.sinc(np.asarray(omega)*T/(2*np.pi))**2


def spectral_density(omega, kappa=1., nu=1.):
    return 2*kappa*nu/(np.pi*((kappa-omega*omega)**2+nu*nu*omega*omega))


def wishart_scatter(rng, M, K, count):
    """Exact scatter law of M independent N(0,K) velocity vectors."""
    n = len(K)
    A = np.zeros((count, n, n))
    for i in range(n):
        A[:, i, i] = np.sqrt(rng.chisquare(M-i, count))
        if i:
            A[:, i, :i] = rng.normal(size=(count, i))
    Y = np.linalg.cholesky(K)[None, :, :]@A
    return Y@np.swapaxes(Y, -1, -2)


def covariance_intervals(scatter, M, failure_budget):
    scatter = np.asarray(scatter)
    n = scatter.shape[-1]
    diagonal = np.diagonal(scatter, axis1=-2, axis2=-1)
    common = (diagonal[..., [0]]+diagonal[..., 1:])/2
    cross = scatter[..., 0, 1:]
    tail = failure_budget/(4*(n-1))
    qlo, qhi = chi2.ppf([tail, 1-tail], M)
    plus_lo, plus_hi = (common+cross)/qhi, (common+cross)/qlo
    minus_lo, minus_hi = (common-cross)/qhi, (common-cross)/qlo
    lower = np.maximum.reduce([plus_lo-1, 1-minus_hi, np.full_like(cross, -1.)])
    upper = np.minimum.reduce([plus_hi-1, 1-minus_lo, np.full_like(cross, 1.)])
    return lower, upper


def acceleration_upper(squared_sum, count, failure_budget):
    return np.asarray(squared_sum)/chi2.ppf(failure_budget, count)


def linear_interpolation_bounds(lower, upper, T, delta, kappa_upper):
    m = int(round(T/delta))
    if abs(T/delta-m) > 1e-9 or m > len(lower):
        return None
    coefficients = np.zeros(m+1)
    coefficients[0] = T*delta/2-delta*delta/6
    coefficients[1:m] = delta*(T-delta*np.arange(1, m))
    coefficients[m] = delta*delta/6
    allowance = kappa_upper*T*T*delta*delta/24
    lo = coefficients@np.r_[1., lower[:m]]-allowance
    hi = coefficients@np.r_[1., upper[:m]]+allowance
    return [float(max(0., lo)), float(min(T*T/2, hi))]


class SpectralBounds:
    def __init__(self, times, settings):
        self.times = np.asarray(times)
        self.delta = float(times[0])
        if (self.times.ndim != 1 or self.delta <= 0 or not np.all(np.isfinite(self.times))
                or not np.allclose(self.times, self.delta*np.arange(1, len(self.times)+1), rtol=0, atol=1e-12)):
            raise ValueError("Global folding requires the declared equally spaced positive lags")
        self.settings = settings
        self.grids = {}
        for tail_needed in (False, True):
            R = settings["tail_start"] if tail_needed else np.pi/self.delta
            omega = np.linspace(0, R, settings["design_grid_points"])
            self.grids[tail_needed] = (omega, np.cos(omega[:, None]*self.times))

    def upper_functional(self, lower, upper, T, kappa_upper=None, sign=1, refine_factor=1):
        energy = kappa_upper is not None
        if not energy and sign == -1:
            return {"bound": 0., "analytic": "high-frequency alias lower infimum is zero"}
        if abs(T/self.delta-round(T/self.delta)) > 1e-9:
            raise ValueError("Folding certificate requires integer-multiple horizon")
        tail_needed = energy and sign == -1
        omega, cosines = self.grids[tail_needed]
        R = float(omega[-1])
        n = len(self.times)
        # Variables: constant, positive/negative cosine coefficients, energy>=0.
        features = np.column_stack([np.ones(len(omega)), cosines, -cosines])
        objective = np.r_[1., upper, -lower]
        bounds = [(None, None)]+[(0, None)]*(2*n)
        f = sign*spectral_integrand(omega, T)
        if energy:
            features = np.column_stack([features, omega**2])
            objective = np.r_[objective, kappa_upper]
            bounds += [(0, None)]
        if tail_needed:
            tail = np.r_[1., -np.ones(2*n), R*R]
            tail_rhs = 2/(R*R) if sign == 1 else 0.
            A_ub = -np.vstack([features, tail])
            b_ub = -np.r_[f, tail_rhs]
        else:
            A_ub, b_ub = -features, -f
        tolerance = self.settings["dual_feasibility_tolerance"]
        fit = linprog(objective, A_ub=A_ub, b_ub=b_ub, bounds=bounds,
                      method="highs", options={"dual_feasibility_tolerance": tolerance,
                                               "primal_feasibility_tolerance": tolerance})
        if not fit.success:
            raise RuntimeError("Moment dual failed: "+fit.message)
        if not np.all(np.isfinite(fit.x)):
            raise RuntimeError("Nonfinite dual coefficients cannot define a certificate")
        a0 = float(fit.x[0])
        y = fit.x[1:n+1]-fit.x[n+1:2*n+1]
        # Solver feasibility is numerical. Even a tiny negative coefficient
        # would invalidate an infinite-frequency proof; projection upward is
        # safe, and all remainders/objectives below use the projected value.
        lam = max(0., float(fit.x[-1])) if energy else 0.
        curvature = 2*abs(lam)+float(abs(y)@(self.times**2))+T**4/12
        target = self.settings["certificate_curvature_tolerance_per_time"]*max(1., T)/refine_factor**2
        max_h = min(self.settings["certificate_max_spacing"]/refine_factor, np.sqrt(8*target/curvature))
        number = max(2, int(np.ceil(R/max_h))+1)
        if number > self.settings["maximum_certificate_points"]:
            raise RuntimeError("Declared continuum-certificate resource limit exceeded")
        dense = np.linspace(0, R, number)
        h = R/(number-1)
        remainder = a0+lam*dense*dense+np.cos(dense[:, None]*self.times)@y-sign*spectral_integrand(dense, T)
        node_min = float(np.min(remainder))
        curvature_allowance = curvature*h*h/8
        tail_margin = a0+lam*R*R-float(abs(y).sum()) if tail_needed else None
        safety = self.settings["floating_safety_factor"]*(1+abs(a0)+lam*R*R+float(abs(y).sum())+T*T/2)
        shift = max(0., -node_min+curvature_allowance, -tail_margin if tail_needed else 0.)+safety
        repaired_a0 = a0+shift
        bound = repaired_a0+float(np.maximum(y, 0)@upper+np.minimum(y, 0)@lower)
        if energy:
            bound += lam*kappa_upper
        return {"bound": float(bound), "grid_objective": float(fit.fun),
                "constant": float(repaired_a0), "cosine_coefficients": y.tolist(), "energy_coefficient": lam,
                "sign": sign, "finite_interval_end": R, "certificate_nodes": number,
                "minimum_node_remainder_before_repair": node_min,
                "curvature_bound": curvature, "curvature_allowance": curvature_allowance,
                "constant_repair": float(shift), "roundoff_safety_allowance": safety,
                "certified_remainder_floor": float(node_min-curvature_allowance+shift),
                "tail_margin_after_repair": float(tail_margin+shift) if tail_needed else None,
                "extension_to_all_frequencies": "quadratic tail domination" if tail_needed else "integer-horizon folding",
                "grid_solver_iterations": int(fit.nit)}

    def interval(self, lower, upper, T, kappa_upper=None, refine_factor=1):
        high = self.upper_functional(lower, upper, T, kappa_upper, 1, refine_factor)
        negative = self.upper_functional(lower, upper, T, kappa_upper, -1, refine_factor)
        lo, hi = max(0., -negative["bound"]), min(T*T/2, high["bound"])
        if lo > hi+1e-7:
            raise RuntimeError("Empty interval: data or calibration inconsistent with constraints")
        return {"lower": lo, "upper": hi, "width": hi-lo, "upper_certificate": high,
                "negative_certificate": negative}


def main():
    p = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    observation, confidence, target = p["observation"], p["confidence"], p["physical_target"]
    kappa, nu = target["kappa"], target["nu"]
    delta, n = observation["sample_spacing"], observation["samples_per_trajectory"]
    times = delta*np.arange(n)
    c = covariance(times, kappa, nu)
    K = toeplitz(c)
    engine = SpectralBounds(times[1:], p["optimization"])
    truth = {str(T): true_displacement(T, kappa, nu) for T in p["horizons"]}
    checks = []

    def check(name, condition, value):
        checks.append({"name": name, "passed": bool(condition), "value": value})
        if not condition:
            raise AssertionError(name+": "+str(value))

    A = np.array([[0., -1.], [kappa, -nu]])
    Sigma = np.diag([1., kappa])
    Q = np.diag([0., 2*kappa*nu])
    residual = float(np.max(abs(A@Sigma+Sigma@A.T+Q)))
    check("thermal realization Lyapunov identity", residual < 1e-12, residual)
    matrix_error = float(max(abs(covariance(t, kappa, nu)-expm(A*t)[0, 0]) for t in times))
    check("closed-form VACF versus matrix dynamics", matrix_error < 1e-12, matrix_error)
    check("sampled velocity covariance is positive definite", float(np.linalg.eigvalsh(K)[0]) > 0,
          float(np.linalg.eigvalsh(K)[0]))
    spectral_moments = [quad(lambda w: spectral_density(w, kappa, nu)*w**power,
                             0, np.inf, epsabs=1e-10, epsrel=1e-10)[0] for power in [0, 2]]
    check("spectrum normalization and acceleration sum rule", max(abs(np.array(spectral_moments)-[1., kappa])) < 1e-9,
          spectral_moments)
    displacement_error = max(abs(quad(lambda t: (T-t)*covariance(t, kappa, nu), 0, T,
                                      epsabs=1e-10)[0]-truth[str(T)]) for T in p["horizons"])
    check("displacement matrix integral versus time quadrature", displacement_error < 1e-9, float(displacement_error))
    # Explicit passive alias pair; validates sampling identity, not new physics.
    alias_lags = np.arange(60)*delta
    alias_error = float(np.max(abs(np.exp(-alias_lags)*np.cos(2*np.pi/delta*alias_lags)-np.exp(-alias_lags))))
    check("unit-variance passive alias sample identity", alias_error < 1e-12, alias_error)
    wtest = np.linspace(0, np.pi/delta, 300)
    folding_gap = min(float(np.min(spectral_integrand(wtest, T)-spectral_integrand(wtest+2*np.pi/delta, T)))
                      for T in p["horizons"])
    check("sampled check of analytic integer-horizon folding inequality", folding_gap > -1e-12, folding_gap)

    population = []
    for mode, kap in [("no_acceleration_information", None), ("known_acceleration_variance", kappa)]:
        for T in p["horizons"]:
            interval = engine.interval(c[1:], c[1:], T, kap)
            baseline = linear_interpolation_bounds(c[1:], c[1:], T, delta, kap) if kap is not None else None
            population.append({"mode": mode, "horizon": T, "truth": truth[str(T)],
                               "interpolation_baseline": baseline, **interval})
    check("noiseless continuum-corrected bounds include truth",
          all(row["lower"] <= row["truth"] <= row["upper"] for row in population),
          len(population))
    check("noiseless interpolation baseline includes truth",
          all(row["interpolation_baseline"] is None or row["interpolation_baseline"][0] <= row["truth"] <= row["interpolation_baseline"][1]
              for row in population), len(population))
    # Independent finite-grid primal: weak duality must hold even though the
    # repaired continuum bound need not achieve the exact infinite LP optimum.
    primal_omega = np.linspace(0, p["optimization"]["tail_start"], 4001)
    moment_matrix = np.cos(times[1:, None]*primal_omega)
    primal_features = np.vstack([moment_matrix, -moment_matrix, primal_omega**2])
    primal_limits = np.r_[c[1:], -c[1:], kappa]
    weak_duality = []
    for sign in [-1, 1]:
        primal = linprog(-sign*spectral_integrand(primal_omega, 6.), A_ub=primal_features,
                         b_ub=primal_limits, A_eq=np.ones((1, len(primal_omega))), b_eq=[1.],
                         bounds=(0, None), method="highs")
        if not primal.success:
            raise AssertionError("Independent finite-grid primal infeasible")
        dual = engine.upper_functional(c[1:], c[1:], 6., kappa, sign)
        weak_duality.append(float(dual["bound"]+primal.fun))
    check("independent finite-grid primal versus continuum upper dual", min(weak_duality) > -1e-7, weak_duality)

    calibration_rng = np.random.default_rng(p["calibration_seed"])
    calibration = []
    M_acc = observation["independent_acceleration_samples"]
    count = p["calibration_replicates_per_ensemble_size"]
    for M in observation["ensemble_sizes"]:
        scatter = wishart_scatter(calibration_rng, M, K, count)
        lower, upper = covariance_intervals(scatter, M, confidence["covariance_failure_budget"])
        acc = kappa*calibration_rng.chisquare(M_acc, count)
        kap = acceleration_upper(acc, M_acc, confidence["acceleration_failure_budget"])
        covariance_ok = np.all((lower <= c[1:]) & (c[1:] <= upper), axis=1)
        acceleration_ok = kap >= kappa
        joint = covariance_ok & acceleration_ok
        calibration.append({"ensemble_size": M, "replicates": count,
                            "covariance_coverage_count": int(covariance_ok.sum()),
                            "acceleration_coverage_count": int(acceleration_ok.sum()),
                            "joint_coverage_count": int(joint.sum()),
                            "joint_coverage_rate": float(joint.mean()),
                            "covariance_coverage_rate": float(covariance_ok.mean()),
                            "acceleration_coverage_rate": float(acceleration_ok.mean())})
        del scatter
    # Diagnostic threshold is looser than nominal coverage; finite Monte Carlo
    # cannot establish the theoretical coverage claim.
    check("Monte Carlo audit of simultaneous confidence event", min(row["joint_coverage_rate"] for row in calibration) > .93,
          [row["joint_coverage_rate"] for row in calibration])

    rng = np.random.default_rng(p["inference_seed"])
    saved_scatter, saved_acc, input_ids, inputs, rows, failures = [], [], [], [], [], []
    reps = observation["inference_datasets_per_size"]
    for M in observation["ensemble_sizes"]:
        scatters = wishart_scatter(rng, M, K, reps)
        acceleration_sums = kappa*rng.chisquare(M_acc, reps)
        lowers, uppers = covariance_intervals(scatters, M, confidence["covariance_failure_budget"])
        kappas = acceleration_upper(acceleration_sums, M_acc, confidence["acceleration_failure_budget"])
        for rep, (scatter, acc, lower, upper, kap) in enumerate(zip(scatters, acceleration_sums, lowers, uppers, kappas)):
            saved_scatter.append(scatter); saved_acc.append(acc); input_ids.append([M, rep])
            inputs.append({"ensemble_size": M, "replicate": rep, "covariance_lower": lower.tolist(),
                           "covariance_upper": upper.tolist(), "acceleration_upper": float(kap),
                           "covariance_event_contains_truth": bool(np.all((lower <= c[1:]) & (c[1:] <= upper))),
                           "acceleration_event_contains_truth": bool(kap >= kappa)})
            for mode in p["modes"]:
                energy = None if mode == "no_acceleration_information" else kappa if mode == "known_acceleration_variance" else float(kap)
                for T in p["horizons"]:
                    base = {"ensemble_size": M, "replicate": rep, "mode": mode, "horizon": T,
                            "truth": truth[str(T)], "acceleration_upper_used": energy}
                    try:
                        interval = engine.interval(lower, upper, T, energy)
                        baseline = linear_interpolation_bounds(lower, upper, T, delta, energy) if energy is not None else None
                        row = {**base, **interval, "interpolation_baseline": baseline,
                               "contains_truth": bool(interval["lower"] <= truth[str(T)] <= interval["upper"])}
                        rows.append(row)
                    except RuntimeError as error:
                        failures.append({**base, "error": str(error)})
            print(f"Finished M={M}, dataset {rep+1}/{reps}", flush=True)
    input_map = {(r["ensemble_size"], r["replicate"]): r for r in inputs}
    event_rows = [row for row in rows if input_map[(row["ensemble_size"], row["replicate"])]["covariance_event_contains_truth"]
                  and (row["mode"] != "calibrated_acceleration_upper_bound" or input_map[(row["ensemble_size"], row["replicate"])]["acceleration_event_contains_truth"])]
    check("functional coverage whenever defining confidence event holds", all(row["contains_truth"] for row in event_rows), len(event_rows))
    check("all requested inference attempts accounted for", len(rows)+len(failures) == len(inputs)*len(p["modes"])*len(p["horizons"]),
          {"successful_intervals": len(rows), "reported_failures": len(failures)})
    certificates = [r[key] for r in rows+population for key in ["upper_certificate", "negative_certificate"] if "constant" in r[key]]
    check("every stored quadratic coefficient is nonnegative and finite",
          all(np.isfinite(cert["energy_coefficient"]) and cert["energy_coefficient"] >= 0 for cert in certificates), len(certificates))
    minimum_floor = min(cert["certified_remainder_floor"] for cert in certificates)
    tail_margins = [cert["tail_margin_after_repair"] for cert in certificates if cert["tail_margin_after_repair"] is not None]
    check("every returned certificate has nonnegative finite-domain floor", minimum_floor >= -1e-12, minimum_floor)
    check("every required tail certificate is nonnegative", min(tail_margins) >= -1e-12, min(tail_margins))

    # Refine the finite-domain check without changing the original optimized
    # dual or fitting to truth. This detects a too-coarse reported correction.
    refinements = []
    for M in observation["ensemble_sizes"]:
        item = input_map[(M, 0)]
        fine = engine.interval(np.array(item["covariance_lower"]), np.array(item["covariance_upper"]),
                               6., item["acceleration_upper"], refine_factor=2)
        coarse = next(r for r in rows if r["ensemble_size"] == M and r["replicate"] == 0
                      and r["horizon"] == 6. and r["mode"] == "calibrated_acceleration_upper_bound")
        refinements.append({"ensemble_size": M, "coarse": [coarse["lower"], coarse["upper"]],
                            "refined": [fine["lower"], fine["upper"]],
                            "maximum_endpoint_change": max(abs(fine["lower"]-coarse["lower"]), abs(fine["upper"]-coarse["upper"]))})
    check("continuum-check mesh refinement changes endpoints by less than 0.002",
          max(r["maximum_endpoint_change"] for r in refinements) < .002, refinements)
    summary = []
    for M in observation["ensemble_sizes"]:
        for mode in p["modes"]:
            for T in p["horizons"]:
                group = [r for r in rows if r["ensemble_size"] == M and r["mode"] == mode and r["horizon"] == T]
                widths = np.array([r["width"] for r in group])
                baseline_widths = [r["interpolation_baseline"][1]-r["interpolation_baseline"][0] for r in group if r["interpolation_baseline"] is not None]
                summary.append({"ensemble_size": M, "mode": mode, "horizon": T, "successful_intervals": len(group),
                                "truth_inclusion_count": sum(r["contains_truth"] for r in group),
                                "strictly_positive_lower_count": sum(r["lower"] > 0 for r in group),
                                "median_lower": float(np.median([r["lower"] for r in group])) if group else None,
                                "median_upper": float(np.median([r["upper"] for r in group])) if group else None,
                                "median_width": float(np.median(widths)) if group else None,
                                "median_relative_width": float(np.median(widths)/truth[str(T)]) if group else None,
                                "width_10_90_percentiles": np.quantile(widths, [.1, .9]).tolist() if group else None,
                                "median_interpolation_baseline_width": float(np.median(baseline_widths)) if baseline_widths else None})
    gate = p["development_gate"]
    relevant = [r for r in rows if r["ensemble_size"] == gate["ensemble_size"] and r["horizon"] == gate["horizon"]]
    plain = {r["replicate"]: r for r in relevant if r["mode"] == "no_acceleration_information"}
    measured = {r["replicate"]: r for r in relevant if r["mode"] == "calibrated_acceleration_upper_bound"}
    paired = sorted(plain.keys() & measured.keys())
    ratio = float(np.median([measured[i]["width"]/plain[i]["width"] for i in paired])) if paired else None
    positive_fraction = sum(measured[i]["lower"] > 0 for i in measured)/reps
    gate_result = {"paired_successes": len(paired), "required_datasets": reps,
                   "median_calibrated_to_no_acceleration_width_ratio": ratio,
                   "fraction_of_all_declared_datasets_excluding_zero": positive_fraction,
                   "passed": bool(len(paired) == reps and ratio <= gate["median_calibrated_to_no_acceleration_width_ratio_maximum"]
                                  and positive_fraction >= gate["fraction_calibrated_intervals_excluding_zero_minimum"]),
                   "scope": gate["interpretation"]}
    OUT.mkdir(parents=True, exist_ok=True)
    array_path = OUT / "input_scatter_matrices.npz"
    np.savez_compressed(array_path, input_ids=input_ids, scatter_matrices=saved_scatter,
                        acceleration_squared_sums=saved_acc, sample_times=times, true_covariance=K)
    report = {"study": p["title"], "status": p["status"], "generated_utc": datetime.now(timezone.utc).isoformat(),
              "population_results": population, "calibration_audit": calibration, "inputs": inputs,
              "inference_results": rows, "failures": failures, "summary": summary,
              "development_gate": gate_result, "checks": checks, "passed_checks": len(checks),
              "hashes": {"script": sha256(__file__), "protocol": sha256(PROTOCOL), "input_arrays": sha256(array_path)},
              "environment": {"python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__, "matplotlib": matplotlib.__version__},
              "cost_scope": p["cost_scope"], "limits": p["limits"]}
    (OUT / "results.json").write_text(json.dumps(report, indent=2, allow_nan=False)+"\n", encoding="utf-8")
    plot_results(report, p, truth)
    print(json.dumps({"passed_checks": len(checks), "development_gate": gate_result, "failures": failures,
                      "summary": summary, "calibration_audit": calibration}, indent=2, allow_nan=False))


def plot_results(report, p, truth):
    colors = {"no_acceleration_information": "#64748b", "known_acceleration_variance": "#0f766e",
              "calibrated_acceleration_upper_bound": "#7c3aed"}
    labels = {"no_acceleration_information": "Velocity samples only",
              "known_acceleration_variance": "Plus exact acceleration variance",
              "calibrated_acceleration_upper_bound": "Plus measured acceleration bound"}
    plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.4), constrained_layout=True)
    for mode in p["modes"][:2]:
        rows = [r for r in report["population_results"] if r["mode"] == mode]
        axes[0].plot([r["horizon"] for r in rows], [r["width"]/r["truth"] for r in rows], "o-", color=colors[mode], label=labels[mode])
    for mode in p["modes"]:
        rows = [r for r in report["summary"] if r["ensemble_size"] == 4096 and r["mode"] == mode]
        axes[1].plot([r["horizon"] for r in rows], [r["median_relative_width"] for r in rows], "o-", color=colors[mode], label=labels[mode])
    baseline = [r for r in report["summary"] if r["ensemble_size"] == 4096 and r["mode"] == "calibrated_acceleration_upper_bound"
                and r["median_interpolation_baseline_width"] is not None]
    axes[1].plot([r["horizon"] for r in baseline], [r["median_interpolation_baseline_width"]/truth[str(r["horizon"])] for r in baseline],
                 "s--", color="#d97706", label="Simple interpolation baseline")
    for ax in axes:
        ax.axvline(11.4, color="#b91c1c", ls=":", label="End of observation window")
        ax.set(xlabel="Prediction horizon", ylabel="Interval width / true mean displacement", xscale="log", yscale="log")
        ax.grid(alpha=.15)
        ax.legend(fontsize=8)
    axes[0].set_title("Structural ambiguity with exact covariance samples")
    axes[1].set_title("Noisy data: median over 12 independent datasets")
    fig.suptitle("Extra acceleration information narrows finite-time predictions\n"
                 "Established spectral bounds; continuous-frequency corrections; 4,096 trajectories", fontsize=13)
    fig.savefig(OUT / "spectral_response_bounds.png", dpi=180)
    plt.close(fig)


if __name__ == "__main__":
    main()
