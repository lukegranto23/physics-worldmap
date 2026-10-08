"""Frozen-protocol, exact linear Gaussian response pilot. NumPy + Matplotlib only.

Run from any directory. Results are separate from core labs 01--13.
No random sampling, finite-data uncertainty, generalization theorem or novelty claim.
"""
from __future__ import annotations

import hashlib
import json
import platform
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
PROTOCOL = HERE / "response_benchmark_protocol.json"
OUT = HERE / "results" / "response_benchmark"


def relative_l2(predicted, truth):
    return float(np.linalg.norm(predicted - truth) / np.linalg.norm(truth))


def covariance(a, diffusion):
    """Solve A S + S A.T + diffusion = 0 using column-vectorization."""
    n = len(a)
    operator = np.kron(np.eye(n), a) + np.kron(a, np.eye(n))
    s = np.linalg.solve(operator, -diffusion.reshape(-1, order="F"))
    s = s.reshape((n, n), order="F")
    return (s + s.T) / 2


def response(model, frequencies):
    a, b, c, _ = model
    return np.array([c @ np.linalg.solve(1j*w*np.eye(len(a))-a, b)
                     for w in frequencies])


def full_model(p, coupling=None):
    coupling = p["coupling"] if coupling is None else coupling
    k = np.array([[p["k1"], coupling], [coupling, p["k2"]]])
    gamma = np.diag([p["gamma1"], p["gamma2"]])
    a = np.block([[np.zeros((2, 2)), np.eye(2)], [-k, -gamma]])
    b = np.array([0., 0., 1., 0.])
    c = np.array([1., 0., 0., 0.])
    g = np.vstack([np.zeros((2, 2)), np.sqrt(2*p["temperature"]*gamma)])
    return (a, b, c, g), k


def reduced_model(p, damping, stiffness):
    a = np.array([[0., 1.], [-stiffness, -damping]])
    b = np.array([0., 1.])
    c = np.array([1., 0.])
    g = np.array([[0.], [np.sqrt(2*damping*p["temperature"])]])
    return a, b, c, g


def balanced_model(model):
    """Classical square-root balancing, full known SISO dynamics, order two."""
    a, b, c, g = model
    pc = covariance(a, np.outer(b, b))
    qo = covariance(a.T, np.outer(c, c))
    rp = np.linalg.cholesky(pc)
    rq = np.linalg.cholesky(qo)
    u, singular, vh = np.linalg.svd(rq.T @ rp)
    t = rp @ vh.T @ np.diag(1 / np.sqrt(singular))
    ti = np.diag(1 / np.sqrt(singular)) @ u.T @ rq.T
    # Use the same projection on thermal noise; do not calibrate to force a match.
    return (ti[:2] @ a @ t[:, :2], ti[:2] @ b, c @ t[:, :2],
            ti[:2] @ g), singular, t, ti


def memory_response(p, w):
    """Schur-complement susceptibility; equivalent hidden state order is four."""
    return 1/(p["k1"] - w*w + 1j*p["gamma1"]*w -
              p["coupling"]**2/(p["k2"] - w*w + 1j*p["gamma2"]*w))


def noise_spectrum(model, frequencies):
    """Two-sided q power spectrum from the independently supplied thermal noise."""
    a, _, c, g = model
    return np.array([np.sum(np.abs(c @ np.linalg.solve(
        1j*w*np.eye(len(a))-a, g))**2) for w in frequencies])


def force(p, name, t):
    if name == "pulse":
        return np.exp(-0.5*((t-p["pulse_center"])/p["pulse_width"])**2)
    start, end = p["chirp_frequency"]
    total = p["time_end"]
    # Angular frequency, not cycles per unit time; phase derivative sweeps linearly.
    return np.sin(np.pi*t/total)**2 * np.sin(start*t + (end-start)*t*t/(2*total))


def trajectory(model, p, name, dt):
    """Ensemble mean from zero-mean equilibrium initial conditions."""
    a, b, c, _ = model
    times = np.linspace(0, p["time_end"], round(p["time_end"]/dt)+1)
    dt = times[1] - times[0]
    state = np.zeros(len(a))
    values = np.zeros(len(times))
    for i, t in enumerate(times[:-1]):
        k1 = a @ state + b*force(p, name, t)
        k2 = a @ (state+dt*k1/2) + b*force(p, name, t+dt/2)
        k3 = a @ (state+dt*k2/2) + b*force(p, name, t+dt/2)
        k4 = a @ (state+dt*k3) + b*force(p, name, t+dt)
        state += dt*(k1+2*k2+2*k3+k4)/6
        values[i+1] = c @ state
    return times, values


def main():
    raw = PROTOCOL.read_bytes()
    p = json.loads(raw)
    full, k = full_model(p)
    keff = p["k1"] - p["coupling"]**2/p["k2"]
    train = np.linspace(*p["train_frequency"][:2], int(p["train_frequency"][2]))
    interpolation = (train[1:] + train[:-1])/2
    extrapolation = np.linspace(*p["extrapolation_frequency"][:2],
                                int(p["extrapolation_frequency"][2]))
    search = np.geomspace(*p["damping_search"][:2], int(p["damping_search"][2]))
    target_train = response(full, train)
    losses = np.array([relative_l2(response(reduced_model(p, g, keff), train),
                                  target_train) for g in search])
    index = int(np.argmin(losses))
    best = float(search[index])
    balanced, hsv, transform, inverse = balanced_model(full)
    models = {"full": full,
              "equilibrium": reduced_model(p, p["gamma1"], keff),
              "response_fit": reduced_model(p, best, keff),
              "balanced_reference": balanced}
    full_sigma = np.block([[p["temperature"]*np.linalg.inv(k), np.zeros((2, 2))],
                           [np.zeros((2, 2)), p["temperature"]*np.eye(2)]])
    observe = np.array([[1., 0., 0., 0.], [0., 0., 1., 0.]])
    target_sigma = observe @ full_sigma @ observe.T
    metrics = {}
    sigmas = {}
    validation = {}
    tol = p["algebra_tolerance"]

    def check(name, error, tolerance=tol):
        validation[name] = {"error": float(error), "tolerance": float(tolerance),
                            "passed": bool(error < tolerance)}

    check("positive_stiffness", 0. if np.min(np.linalg.eigvalsh(k)) > 0 else 1.)
    check("balancing_inverse", np.linalg.norm(inverse @ transform-np.eye(4)))
    check("controllability_gramian_balanced",
          relative_l2(inverse @ covariance(full[0], np.outer(full[1], full[1]))
                      @ inverse.T, np.diag(hsv)))
    check("observability_gramian_balanced",
          relative_l2(transform.T @ covariance(full[0].T, np.outer(full[2], full[2]))
                      @ transform, np.diag(hsv)))
    check("canonical_vs_lyapunov_covariance",
          relative_l2(covariance(full[0], full[3]@full[3].T), full_sigma))
    check("schur_complement_vs_resolvent",
          relative_l2(memory_response(p, extrapolation), response(full, extrapolation)))
    uncoupled, _ = full_model(p, coupling=0.)
    check("zero_coupling_reduction",
          relative_l2(response(reduced_model(p, p["gamma1"], p["k1"]), extrapolation),
                      response(uncoupled, extrapolation)))
    check("static_susceptibility",
          abs(response(full, [0])[0] - 1/keff))
    check("fit_not_on_search_boundary", 0. if index not in (0, len(search)-1) else 1.)

    for name, model in models.items():
        a, _, _, g = model
        sigma = covariance(a, g@g.T)
        retained = (observe if name == "full" else
                    observe @ transform[:, :2] if name == "balanced_reference" else np.eye(2))
        observed_sigma = retained @ sigma @ retained.T
        sigmas[name] = observed_sigma.tolist()
        metrics[name] = {
            "states": len(a),
            "stationary_qp_covariance_relative_error": relative_l2(observed_sigma, target_sigma),
            "stationary_q_variance_relative_error": float(abs(observed_sigma[0, 0]/target_sigma[0, 0]-1)),
            "max_real_eigenvalue": float(np.max(np.linalg.eigvals(a).real))}
        check(name+"_stability", 0. if metrics[name]["max_real_eigenvalue"] < 0 else 1.)
        check(name+"_lyapunov_residual",
              np.linalg.norm(a@sigma+sigma@a.T+g@g.T)/np.linalg.norm(g@g.T))
        for band, grid in (("train", train), ("interpolation", interpolation),
                           ("extrapolation", extrapolation)):
            metrics[name][band+"_relative_l2"] = relative_l2(response(model, grid), response(full, grid))
    for name in ("equilibrium", "response_fit"):
        check(name+"_exact_stationary_marginal",
              metrics[name]["stationary_qp_covariance_relative_error"])

    # Added as a post-run implementation audit, not a new model-selection criterion.
    # With exp(+i omega t), the classical FDT has a minus sign before Im chi.
    for name in ("full", "equilibrium", "response_fit"):
        predicted_psd = -2*p["temperature"]*response(models[name], extrapolation).imag/extrapolation
        check(name+"_fluctuation_dissipation_identity",
              relative_l2(noise_spectrum(models[name], extrapolation), predicted_psd))

    # Independent tied damping control: equilibrium agreement alone permits distinct responses.
    tied = reduced_model(p, 1., keff)
    check("alternative_damping_same_stationary_covariance",
          relative_l2(covariance(tied[0], tied[3]@tied[3].T), target_sigma))
    difference = relative_l2(response(tied, extrapolation), response(models["equilibrium"], extrapolation))
    check("alternative_damping_different_response", 0. if difference > .1 else 1.)
    trajectories = {}
    for forcing in ("pulse", "chirp"):
        for name, model in models.items():
            times, coarse = trajectory(model, p, forcing, p["time_step"])
            _, fine = trajectory(model, p, forcing, p["time_step"]/2)
            check(forcing+"_"+name+"_time_refinement", relative_l2(coarse, fine[::2]),
                  p["time_convergence_tolerance"])
            trajectories[forcing+"_"+name] = coarse
        for name in models:
            metrics[name][forcing+"_relative_l2"] = relative_l2(
                trajectories[forcing+"_"+name], trajectories[forcing+"_full"])

    report = {
        "protocol_sha256": hashlib.sha256(raw).hexdigest(),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "python": platform.python_version(), "numpy": np.__version__,
        "matplotlib": matplotlib.__version__,
        "scope": p["scope"], "effective_stiffness": keff,
        "fitted_damping": best, "equilibrium_baseline_damping": p["gamma1"],
        "hankel_singular_values": hsv.tolist(),
        "training_grid_index": index,
        "training_objective": float(losses[index]),
        "metrics": metrics, "retained_qp_covariances": sigmas,
        "validation": validation,
        "all_checks_passed": all(x["passed"] for x in validation.values()),
        "interpretation_limits": [
            "One analytic linear system; not Session 001's four-system study.",
            "Response fit uses noiseless forced data; equilibrium objective does not identify damping.",
            "Balanced reference has full model information and a more flexible two-state realization.",
            "Equilibrium means a one-time Gaussian marginal, not multi-time correlations.",
            "Exact memory susceptibility is four-state-equivalent, not an equal-budget reduction.",
            "No novelty, statistical confidence interval or experimental physics claim."]}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT/"results.json").write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
    np.savez_compressed(OUT/"arrays.npz", times=times, train=train, interpolation=interpolation,
                        extrapolation=extrapolation, damping_grid=search, training_losses=losses,
                        **trajectories,
                        **{name+"_extrapolation": response(model, extrapolation)
                           for name, model in models.items()})
    columns = ["model", "stationary_qp_covariance_relative_error", "train_relative_l2",
               "interpolation_relative_l2", "extrapolation_relative_l2",
               "pulse_relative_l2", "chirp_relative_l2"]
    rows = [",".join(columns)] + [",".join([name]+[format(metrics[name][key], ".12g")
                                                  for key in columns[1:]]) for name in models]
    (OUT/"metrics.csv").write_text("\n".join(rows)+"\n", encoding="utf-8")
    plot(models, p, train, metrics, times, trajectories)
    print(json.dumps({"fitted_damping": best, "metrics": metrics,
                      "checks": len(validation), "all_checks_passed": report["all_checks_passed"]},
                     indent=2))
    assert report["all_checks_passed"], "Validation failure: inspect results.json"


def plot(models, p, train, metrics, times, trajectories):
    fig, axes = plt.subplots(2, 2, figsize=(12, 8), constrained_layout=True)
    colors = {"full": "#172c4c", "equilibrium": "#ba4b32",
              "response_fit": "#147e79", "balanced_reference": "#8a61a8"}
    labels = {"full": "Full system (4 states)", "equilibrium": "Equilibrium-only (2)",
              "response_fit": "Response-fitted (2)", "balanced_reference": "Balanced reference (2)*"}
    w = np.linspace(0, 3, 601)
    for name, model in models.items():
        h = response(model, w)
        axes[0, 0].plot(w, np.abs(h), color=colors[name], label=labels[name])
        if name != "full":
            axes[0, 1].plot(w, np.abs(h-response(models["full"], w)),
                            color=colors[name], label=labels[name])
        axes[1, 0].plot(times, trajectories["pulse_"+name], color=colors[name])
        axes[1, 1].plot(times, trajectories["chirp_"+name], color=colors[name])
    axes[0, 0].set(title="Same equilibrium can hide different response", ylabel="Susceptibility magnitude")
    axes[0, 1].set(title="Response mismatch outside the fitted band", ylabel="Absolute complex-response error")
    for ax in axes[0]:
        ax.axvspan(train[0], train[-1], color="#aaaaaa", alpha=.2, label="Training band")
        ax.set_xlabel("Angular frequency (nondimensional)")
    axes[0, 0].legend(fontsize=8)
    axes[1, 0].set(title="Held-out Gaussian pulse", xlabel="Time", ylabel="Mean observed displacement", xlim=(0, 35))
    axes[1, 1].set(title="Held-out chirped forcing", xlabel="Time", ylabel="Mean observed displacement")
    for ax in axes.flat:
        ax.grid(alpha=.2)
    fig.suptitle("Response-preserving reduction: exact linear pilot\n"
                 "*Balanced reference uses the full known model; not an information-matched competitor.",
                 fontsize=12)
    fig.savefig(OUT/"response_comparison.png", dpi=170)
    plt.close(fig)


if __name__ == "__main__":
    main()
