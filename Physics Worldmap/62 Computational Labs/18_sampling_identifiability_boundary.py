"""Thermal aliasing counterexample: exact sampled laws, different forced responses.

This is an illustration of established system aliasing, not a discovery claim.
No stochastic simulation, fitting, or new warning algorithm is performed.
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
PROTOCOL = HERE / "sampling_boundary_protocol.json"
OUT = HERE / "results" / "sampling_boundary"


def oscillator(protocol, alias):
    alpha = protocol["decay_rate"]
    omega = 2*np.pi*alias/protocol["sampling_interval"]
    stiffness = protocol["stiffness"]
    mass = stiffness/(omega**2+alpha**2)
    friction = 2*alpha*mass
    a = np.array([[0., 1.], [-stiffness/mass, -friction/mass]])
    b = np.array([0., 1/mass])
    c = np.array([1., 0.])
    g = np.array([[0.], [np.sqrt(2*friction*protocol["temperature"])/mass]])
    sigma = np.diag([protocol["temperature"]/stiffness, protocol["temperature"]/mass])
    return {"alias": alias, "omega": omega, "mass": mass, "friction": friction,
            "a": a, "b": b, "c": c, "g": g, "sigma": sigma}


def covariance_closed(model, protocol, t):
    t = np.abs(np.asarray(t))
    alpha, omega = protocol["decay_rate"], model["omega"]
    return (protocol["temperature"]/protocol["stiffness"] * np.exp(-alpha*t)
            * (np.cos(omega*t)+alpha/omega*np.sin(omega*t)))


def propagator(model, t):
    eigenvalues, eigenvectors = np.linalg.eig(model["a"])
    value = (eigenvectors*np.exp(eigenvalues*t)) @ np.linalg.inv(eigenvectors)
    return np.real_if_close(value, tol=1000).real


def susceptibility(model, protocol, frequency):
    return 1/(protocol["stiffness"] - model["mass"]*frequency**2
              + 1j*model["friction"]*frequency)


def relative_error(x, y):
    return float(np.linalg.norm(x-y)/np.linalg.norm(y))


def main():
    raw = PROTOCOL.read_bytes()
    p = json.loads(raw)
    models = [oscillator(p, alias) for alias in p["alias_integers"]]
    sample_times = np.arange(p["sample_lag_count"])*p["sampling_interval"]
    fine_times = np.linspace(0, p["fine_time_end"], p["fine_time_count"])
    reference_covariance = (p["temperature"]/p["stiffness"] *
                            np.exp(-p["decay_rate"]*np.abs(
                                sample_times[:, None]-sample_times[None, :])))
    checks = {}
    tol = p["algebra_tolerance"]

    def check(name, error, limit=tol):
        checks[name] = {"error": float(error), "tolerance": float(limit),
                        "passed": bool(error < limit)}

    records = []
    sampled_curves = []
    fine_curves = []
    responses = []
    forced_curves = []
    frequencies = np.linspace(.01, 25., 1001)
    spectra = []
    for model in models:
        key = str(model["alias"])
        a, b, c, g, sigma = (model[name] for name in ("a", "b", "c", "g", "sigma"))
        samples = covariance_closed(model, p, sample_times)
        fine = covariance_closed(model, p, fine_times)
        cov = covariance_closed(model, p, sample_times[:, None]-sample_times[None, :])
        check(key+"_entire_finite_sample_covariance", relative_error(cov, reference_covariance))
        check(key+"_thermal_lyapunov", np.linalg.norm(a@sigma+sigma@a.T+g@g.T)/np.linalg.norm(g@g.T))
        check(key+"_stable_and_positive_mass",
              0. if max(np.linalg.eigvals(a).real) < 0 and model["mass"] > 0 else 1.)
        check(key+"_sample_transition",
              relative_error(propagator(model, p["sampling_interval"]),
                             np.exp(-p["decay_rate"]*p["sampling_interval"])*np.eye(2)))
        matrix_curve = np.array([(propagator(model, t)@sigma)[0, 0]
                                 for t in fine_times[::40]])
        check(key+"_covariance_matrix_vs_formula", relative_error(matrix_curve, fine[::40]))
        target = susceptibility(model, p, p["force_frequency"])
        resolvent = c @ np.linalg.solve(1j*p["force_frequency"]*np.eye(2)-a, b)
        check(key+"_susceptibility_matrix_vs_formula", abs(target-resolvent)/abs(target))
        check(key+"_static_susceptibility",
              abs(susceptibility(model, p, 0.)-1/p["stiffness"]))
        spectrum = np.array([np.sum(np.abs(c@np.linalg.solve(1j*w*np.eye(2)-a, g))**2)
                             for w in frequencies])
        fdt = -2*p["temperature"]*susceptibility(model, p, frequencies).imag/frequencies
        check(key+"_thermal_fdt", relative_error(spectrum, fdt))
        sample_hankel = covariance_closed(model, p, (
            np.arange(5)[:, None]+np.arange(5)[None, :])*p["sampling_interval"])
        singular = np.linalg.svd(sample_hankel, compute_uv=False)
        check(key+"_sampled_hankel_rank_one", singular[1]/singular[0])
        offgrid = float(covariance_closed(model, p, p["jittered_lag"]))
        record = {"alias": model["alias"], "mass": model["mass"], "friction": model["friction"],
                  "damped_angular_frequency": model["omega"],
                  "sample_covariance_relative_error": relative_error(cov, reference_covariance),
                  "offgrid_covariance": offgrid,
                  "susceptibility_real": float(target.real),
                  "susceptibility_imag": float(target.imag),
                  "steady_forcing_amplitude": float(p["force_amplitude"]*abs(target)),
                  "steady_forcing_phase_radians": float(np.angle(target))}
        records.append(record)
        sampled_curves.append(samples)
        fine_curves.append(fine)
        responses.append(target)
        forced_curves.append(np.real(p["force_amplitude"]*target*
                                     np.exp(1j*p["force_frequency"]*fine_times)))
        spectra.append(spectrum)
    distances = np.abs(np.array(responses)[:, None]-np.array(responses)[None, :])
    diameter = float(np.max(distances))
    offgrid = np.array([record["offgrid_covariance"] for record in records])
    gap = min(abs(offgrid[i]-offgrid[j]) for i in range(len(models)) for j in range(i))
    check("chosen_family_separated_by_offgrid_covariance", 0. if gap > .01 else 1.)
    check("forced_response_separation", 0. if diameter > p["response_separation_threshold"] else 1.)
    repeated = oscillator(p, p["alias_integers"][0])
    check("identical_parameters_identical_response",
          abs(susceptibility(repeated, p, p["force_frequency"])-responses[0]))
    # Known m, k and alpha imply a unique positive damped angular frequency.
    check("known_mass_recovers_frequency", max(abs(np.sqrt(p["stiffness"]/m["mass"]-
          p["decay_rate"]**2)-m["omega"]) for m in models))
    report = {
        "protocol_sha256": hashlib.sha256(raw).hexdigest(),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "python": platform.python_version(), "numpy": np.__version__, "matplotlib": matplotlib.__version__,
        "scope": p["scope"], "models": records, "response_diameter": diameter,
        "absolute_susceptibility_minimax_lower_bound": diameter/2,
        "force_scaled_complex_amplitude_lower_bound": p["force_amplitude"]*diameter/2,
        "offgrid_minimum_pair_separation": float(gap),
        "sampled_position_ar1_coefficient": float(np.exp(-p["decay_rate"]*p["sampling_interval"])),
        "checks": checks, "all_checks_passed": all(v["passed"] for v in checks.values()),
        "limits": [
            "Constructed resonant sampling, not a frequency-of-occurrence study.",
            "Only equilibrium position samples are supplied; mass and momentum are unknown.",
            "Entire sampled law equality is analytic for every integer lag, not inferred from this finite grid.",
            "All models satisfy their own thermal fluctuation-dissipation relation.",
            "Off-grid lag distinguishes this finite family only; it is not a universal finite-data guarantee.",
            "The diameter lower bound is absolute complex-response error, not relative trajectory error.",
            "No new aliasing theorem, warning algorithm, nonlinear experiment, or physical discovery is claimed."]}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT/"results.json").write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
    np.savez_compressed(OUT/"arrays.npz", sample_times=sample_times, fine_times=fine_times,
                        sampled_covariances=sampled_curves, fine_covariances=fine_curves,
                        steady_forced_means=forced_curves, frequencies=frequencies,
                        noise_spectra=spectra, sample_covariance_matrix=reference_covariance)
    keys = list(records[0])
    (OUT/"models.csv").write_text(",".join(keys)+"\n"+"\n".join(
        ",".join(str(row[key]) for key in keys) for row in records)+"\n", encoding="utf-8")
    plot(p, models, sample_times, fine_times, sampled_curves, fine_curves, forced_curves, responses)
    print(json.dumps({k: v for k, v in report.items() if k not in ("checks", "limits")}, indent=2))
    print(f"{len(checks)} checks: {report['all_checks_passed']}")
    assert report["all_checks_passed"], "See results.json"


def plot(p, models, sample_times, fine_times, sampled, fine, forced, responses):
    fig, axes = plt.subplots(2, 2, figsize=(11, 8), constrained_layout=True)
    colors = ["#147e79", "#b65338", "#735aaa"]
    for i, model in enumerate(models):
        label = f"Thermal model {model['alias']}"
        axes[0, 0].plot(sample_times, sampled[i], color=colors[i], marker=["o", "x", "+"][i],
                        linestyle=["-", "--", ":"][i], label=label)
        axes[0, 1].plot(fine_times, fine[i], color=colors[i])
        axes[1, 0].plot(fine_times, forced[i], color=colors[i])
        axes[1, 1].scatter(responses[i].real, responses[i].imag, color=colors[i], s=70)
        axes[1, 1].annotate(str(model["alias"]), (responses[i].real, responses[i].imag),
                            xytext=(7, 7), textcoords="offset points")
    axes[0, 0].set(title="Equilibrium samples: identical Gaussian laws",
                    xlabel="Integer lag", ylabel="Position autocovariance")
    axes[0, 0].legend(fontsize=8)
    axes[0, 1].set(title="Between samples: different dynamics",
                    xlabel="Continuous lag", ylabel="Position autocovariance", xlim=(0, 2))
    axes[1, 0].set(title="Same sinusoidal force: different responses",
                    xlabel="Time (periodic steady state)", ylabel="Mean position")
    axes[1, 1].set(title="Response ambiguity at the declared frequency",
                    xlabel="Real susceptibility", ylabel="Imaginary susceptibility",
                    xlim=(.1, 1.5), ylim=(-17, 1.5))
    for ax in axes.flat:
        ax.grid(alpha=.2)
    fig.suptitle("What sampled equilibrium data cannot certify\n"
                 "Position only, fixed sampling interval, unknown mass: an established aliasing obstruction.",
                 fontsize=12)
    fig.savefig(OUT/"sampling_boundary.png", dpi=170)
    plt.close(fig)


if __name__ == "__main__":
    main()
