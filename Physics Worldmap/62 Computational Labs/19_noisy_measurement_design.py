"""Known-candidate Gaussian experiment design and finite-sample confidence pilot.

All methods are standard constructions. No new theory or general certificate.
Independent equilibrium position pairs are drawn exactly; no time integrator.
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
PROTOCOL = HERE / "measurement_design_protocol.json"
OUT = HERE / "results" / "measurement_design"


def covariance(p, alias, lag):
    omega = 2*np.pi*alias/p["sampling_interval"]
    alpha = p["decay_rate"]
    lag = np.asarray(lag)
    result = (p["temperature"]/p["stiffness"] * np.exp(-alpha*np.abs(lag)) *
              (np.cos(omega*lag)+alpha/omega*np.sin(omega*np.abs(lag))))
    # Exactly equal on integer lags for this integer-alias family; avoid fake information.
    integer = np.isclose(lag/p["sampling_interval"], np.round(lag/p["sampling_interval"]),
                         atol=1e-13, rtol=0)
    return np.where(integer, p["temperature"]/p["stiffness"]*np.exp(-alpha*np.abs(lag)), result)


def susceptibility(p, alias):
    omega = 2*np.pi*alias/p["sampling_interval"]
    mass = p["stiffness"]/(omega**2+p["decay_rate"]**2)
    nu = p["force_frequency"]
    return 1/(p["stiffness"]-mass*nu**2+2j*p["decay_rate"]*mass*nu)


def bhattacharyya(variance, c1, c2):
    """Distance for zero-mean Gaussian pairs with shared marginal variance."""
    return .5*np.log(variance**2-((c1+c2)/2)**2) - .25*(
        np.log(variance**2-c1**2)+np.log(variance**2-c2**2))


def log_likelihood(variance, cross_covariance, n, s00, s11, s01):
    det = variance**2-cross_covariance**2
    return (-n*np.log(2*np.pi)-n/2*np.log(det)-
            (variance*(s00+s11)-2*cross_covariance*s01)/(2*det))


def confidence_set(loglikes, alpha):
    top = np.max(loglikes, axis=1, keepdims=True)
    logmix = top[:, 0]+np.log(np.mean(np.exp(loglikes-top), axis=1))
    return logmix[:, None]-loglikes <= np.log(1/alpha)


def wilson(successes, total):
    if total == 0:
        return None
    z = 1.959963984540054
    estimate = successes/total
    denom = 1+z*z/total
    center = (estimate+z*z/(2*total))/denom
    half = z*np.sqrt(estimate*(1-estimate)/total+z*z/(4*total**2))/denom
    return {"estimate": float(estimate), "count": int(successes), "total": int(total),
            "wilson95": [float(max(0, center-half)), float(min(1, center+half))]}


def main():
    raw = PROTOCOL.read_bytes()
    p = json.loads(raw)
    variance = p["temperature"]/p["stiffness"]+p["measurement_noise_sd"]**2
    aliases = p["candidate_aliases"]
    m = len(aliases)
    grid = np.linspace(*p["lag_grid"][:2], int(p["lag_grid"][2]))
    curves = np.array([covariance(p, alias, grid) for alias in aliases])
    pairs = [(i, j) for i in range(m) for j in range(i)]
    distances = np.array([bhattacharyya(variance, curves[i], curves[j]) for i, j in pairs])
    gaps = np.array([abs(curves[i]-curves[j]) for i, j in pairs])
    chosen = {
        "integer": p["sampling_interval"],
        "fixed_offgrid": p["fixed_offgrid_lag"],
        "maximin_covariance_gap": float(grid[np.argmax(np.min(gaps, axis=0))]),
        "maximin_bhattacharyya": float(grid[np.argmax(np.min(distances, axis=0))])}
    responses = np.array([susceptibility(p, alias) for alias in aliases])
    response_distances = abs(responses[:, None]-responses[None, :])
    checks = {}

    def check(name, error, tol=1e-9):
        checks[name] = {"error": float(error), "tolerance": tol, "passed": bool(error < tol)}

    check("integer_covariances_identical",
          np.ptp([covariance(p, a, p["sampling_interval"]) for a in aliases]))
    check("distance_zero_for_identical_models",
          np.max(abs(bhattacharyya(variance, curves[0], curves[0]))))
    check("distance_symmetric", np.max(abs(
        bhattacharyya(variance, curves[0], curves[1])-
        bhattacharyya(variance, curves[1], curves[0]))))
    check("affinity_in_unit_interval", 0. if np.min(distances) >= -1e-12 else 1.)
    check("positive_covariance_determinants", 0. if np.min(variance**2-curves**2)>0 else 1.)
    a = np.array([[variance, curves[0, 13]], [curves[0, 13], variance]])
    b = np.array([[variance, curves[1, 13]], [curves[1, 13], variance]])
    independent_distance = (.5*np.linalg.slogdet((a+b)/2)[1]-
                            .25*(np.linalg.slogdet(a)[1]+np.linalg.slogdet(b)[1]))
    check("distance_matches_matrix_determinants",
          abs(independent_distance-bhattacharyya(variance, a[0, 1], b[0, 1])))
    # Direct Gaussian likelihood versus sufficient-statistic implementation.
    example = np.array([[.1, -.2], [.5, .8], [-.9, .4]])
    direct = (-len(example)*np.log(2*np.pi)-len(example)/2*np.linalg.slogdet(a)[1]-
              .5*np.einsum("ni,ij,nj->", example, np.linalg.inv(a), example))
    indirect = log_likelihood(variance, a[0, 1], len(example),
                              sum(example[:, 0]**2), sum(example[:, 1]**2),
                              sum(example[:, 0]*example[:, 1]))
    check("likelihood_matches_direct_matrix_formula", abs(direct-indirect))
    check("equal_likelihood_retains_all_candidates",
          0. if np.all(confidence_set(np.zeros((4, m)), p["confidence_error"])) else 1.)
    rows = []
    arrays = {"lag_grid": grid, "pairwise_distances": distances, "pairwise_covariance_gaps": gaps}
    count = p["replicates_per_truth_budget_design"]
    max_integer_ll_spread = 0.
    all_nonempty = True
    all_mle_included = True
    for truth in aliases+[p["omitted_truth_alias"]]:
        for n in p["pair_budgets"]:
            rng = np.random.default_rng(np.random.SeedSequence([p["seed"], truth, n]))
            # Common standard normals across designs; independent datasets within each cell.
            normals = rng.standard_normal((count, n, 2))
            random_lags = grid[rng.integers(0, len(grid), count)]
            for design in p["designs"]:
                lags = random_lags if design == "uniform_random_lag" else np.full(count, chosen[design])
                rho = covariance(p, truth, lags)/variance
                x = np.sqrt(variance)*normals[:, :, 0]
                y = np.sqrt(variance)*(rho[:, None]*normals[:, :, 0]+
                    np.sqrt(1-rho[:, None]**2)*normals[:, :, 1])
                s00, s11, s01 = (np.sum(value, axis=1) for value in (x*x, y*y, x*y))
                ll = np.array([log_likelihood(variance, covariance(p, alias, lags),
                               n, s00, s11, s01) for alias in aliases]).T
                if design == "integer":
                    max_integer_ll_spread = max(max_integer_ll_spread, float(np.max(np.ptp(ll, axis=1))))
                # Frozen deterministic tie break; integer-lag average accuracy is only 1/3.
                winners = np.argmax(ll >= np.max(ll, axis=1, keepdims=True)-1e-10, axis=1)
                accepted = confidence_set(ll, p["confidence_error"])
                sizes = np.sum(accepted, axis=1)
                all_nonempty &= bool(np.all(sizes > 0))
                all_mle_included &= bool(np.all(accepted[np.arange(count), winners]))
                singleton = sizes == 1
                errors = abs(responses[winners]-susceptibility(p, truth))/abs(susceptibility(p, truth))
                wrong_response = errors > p["response_error_tolerance"]
                false_safe = singleton & wrong_response
                in_family = truth in aliases
                cover = accepted[:, aliases.index(truth)] if in_family else np.zeros(count, dtype=bool)
                diameter = np.max(np.where(accepted[:, :, None]&accepted[:, None, :],
                                           response_distances, 0), axis=(1, 2))
                row = {
                    "truth_alias": truth, "in_candidate_family": in_family, "pairs": n, "design": design,
                    "lag": None if design == "uniform_random_lag" else chosen[design],
                    "classification_error": wilson(np.sum(np.array(aliases)[winners] != truth), count),
                    "coverage": wilson(np.sum(cover), count) if in_family else None,
                    "singleton_rate": wilson(np.sum(singleton), count),
                    "joint_false_reassurance": wilson(np.sum(false_safe), count),
                    "conditional_false_reassurance": wilson(np.sum(false_safe), np.sum(singleton)),
                    "mean_set_size": float(np.mean(sizes)),
                    "mean_response_diameter": float(np.mean(diameter)),
                    "mean_relative_response_error": float(np.mean(errors)),
                    "always_warn": {"singleton_rate": 0., "mean_set_size": m,
                                    "coverage": 1. if in_family else None, "joint_false_reassurance": 0.},
                    "never_warn": {"singleton_rate": 1.,
                                   "joint_false_reassurance": wilson(np.sum(wrong_response), count)}}
                rows.append(row)
                key = f"truth{truth}_n{n}_{design}"
                arrays[key+"_sufficient_statistics"] = np.column_stack([s00, s11, s01, lags])
                arrays[key+"_log_likelihoods"] = ll
                arrays[key+"_accepted"] = accepted
                arrays[key+"_winner"] = winners
    check("all_integer_likelihoods_identical", max_integer_ll_spread)
    check("all_confidence_sets_nonempty", 0. if all_nonempty else 1.)
    check("all_mle_models_in_confidence_set", 0. if all_mle_included else 1.)
    summary = []
    for n in p["pair_budgets"]:
        for design in p["designs"]:
            group = [r for r in rows if r["in_candidate_family"] and r["pairs"]==n and r["design"]==design]
            item = {"pairs": n, "design": design}
            for metric in ("classification_error", "coverage", "singleton_rate", "joint_false_reassurance"):
                item[metric] = wilson(sum(r[metric]["count"] for r in group), count*m)
            item["conditional_false_reassurance"] = wilson(
                sum(r["joint_false_reassurance"]["count"] for r in group),
                sum(r["singleton_rate"]["count"] for r in group))
            item["mean_set_size"] = float(np.mean([r["mean_set_size"] for r in group]))
            item["mean_relative_response_error"] = float(np.mean([r["mean_relative_response_error"] for r in group]))
            summary.append(item)
    report = {"protocol_sha256": hashlib.sha256(raw).hexdigest(),
              "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "python": platform.python_version(), "numpy": np.__version__, "matplotlib": matplotlib.__version__,
              "scope": p["scope"], "chosen_lags": chosen,
              "total_simulated_datasets": len(rows)*count, "observations_per_dataset": "2 * pair budget",
              "checks": checks, "all_checks_passed": all(c["passed"] for c in checks.values()),
              "in_family_summary": summary, "cells": rows,
              "limits": [
                  "Known finite candidate family, known noise and thermal parameters; not hidden-model identification.",
                  "Fresh data realizations are held out; candidate physical systems are not held out.",
                  "Common random numbers couple designs; 120000 evaluations are not 120000 independent datasets.",
                  "Per-cell Wilson intervals are approximate Monte Carlo intervals. Pooled Wilson intervals are descriptive binomial approximations to stratified totals, not exact mixture or simultaneous coverage.",
                  "Independent equilibrium pairs, not correlated overlapping trajectory pairs.",
                  "Design objective uses candidate knowledge before simulated data, not the hidden truth label.",
                  "Confidence guarantee requires the true distribution to be a listed candidate.",
                  "Marginal coverage is not conditional accuracy among singleton decisions.",
                  "No guaranteed full-function band, adaptive stopping, nonlinear transfer, or novelty claim.",
                  "No formal paper-algorithm reproduction or thermal-memory reconstruction is claimed."]}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT/"results.json").write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
    np.savez_compressed(OUT/"replicates.npz", **arrays)
    fields = ["pairs", "design", "classification_error", "coverage", "singleton_rate",
              "joint_false_reassurance", "mean_set_size", "mean_relative_response_error"]
    lines = [",".join(fields)]
    for row in summary:
        lines.append(",".join(str(row[f]["estimate"] if isinstance(row[f], dict) else row[f]) for f in fields))
    (OUT/"summary.csv").write_text("\n".join(lines)+"\n", encoding="utf-8")
    plot(p, grid, distances, chosen, summary, rows)
    print(json.dumps({"chosen_lags": chosen, "datasets": len(rows)*count,
          "checks_passed": report["all_checks_passed"], "check_count": len(checks),
          "n32": [s for s in summary if s["pairs"]==32],
          "omitted_truth_n128": [r for r in rows if not r["in_candidate_family"] and r["pairs"]==128]},
          indent=2))
    assert report["all_checks_passed"], "Implementation checks failed"


def plot(p, grid, distances, chosen, summary, rows):
    fig, axes = plt.subplots(2, 2, figsize=(12, 8), constrained_layout=True)
    labels = {"integer": "Integer lag", "fixed_offgrid": "Fixed lag 0.137",
              "uniform_random_lag": "Random lag", "maximin_covariance_gap": "Maximin covariance gap",
              "maximin_bhattacharyya": "Maximin Gaussian distance"}
    colors = ["#87909b", "#c0723c", "#765aaa", "#3685ad", "#147e79"]
    axes[0, 0].plot(grid, np.min(distances, axis=0), color="#172c4c")
    axes[0, 0].axvline(chosen["maximin_bhattacharyya"], color="#147e79", linestyle="--")
    axes[0, 0].set(title="Design score before seeing data", xlabel="Observation lag",
                    ylabel="Minimum pairwise Gaussian distance")
    for color, design in zip(colors, p["designs"]):
        series = [r for r in summary if r["design"]==design]
        axes[0, 1].plot(p["pair_budgets"], [r["classification_error"]["estimate"] for r in series],
                        "o-", label=labels[design], color=color)
        axes[1, 0].plot(p["pair_budgets"], [r["singleton_rate"]["estimate"] for r in series],
                        "o-", color=color)
        missing = [r for r in rows if not r["in_candidate_family"] and r["design"]==design]
        axes[1, 1].plot(p["pair_budgets"], [r["joint_false_reassurance"]["estimate"] for r in missing],
                        "o-", color=color)
    axes[0, 1].set(title="Known family: identification error", ylabel="Error fraction")
    axes[0, 1].legend(fontsize=8)
    axes[1, 0].set(title="Known family: fraction giving one answer", ylabel="Singleton fraction")
    axes[1, 1].set(title="Omitted true model: false reassurance", ylabel="Singleton AND >5% response error")
    for ax in (axes[0, 1], axes[1, 0], axes[1, 1]):
        ax.set(xlabel="Independent pairs (two readings per pair)", xscale="log", ylim=(-.03, 1.03))
        ax.set_xticks(p["pair_budgets"], [str(n) for n in p["pair_budgets"]])
    for ax in axes.flat:
        ax.grid(alpha=.2)
    fig.suptitle("Noisy measurement design: what it resolves and what it cannot certify\n"
                 "2,000 independent datasets per cell; points are Monte Carlo estimates, intervals in results.json.",
                 fontsize=12)
    fig.savefig(OUT/"measurement_design.png", dpi=170)
    plt.close(fig)


if __name__ == "__main__":
    main()
