"""Frozen range-design comparison: standard mixture e-test, not new physics."""
from __future__ import annotations
import hashlib
import importlib.util
import itertools
import json
import platform
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
PROTOCOL = HERE / "range_design_protocol.json"
OUT = HERE / "results" / "range_design"
DEPENDENCY = HERE / "21_oracle_detection_limits.py"
spec = importlib.util.spec_from_file_location("detection_reference", DEPENDENCY)
ref = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ref)
family = ref.family
METHODS = ("mixture", "split", "concentration")


def logmeanexp(values):
    top = np.max(values, axis=1)
    return top + np.log(np.mean(np.exp(values-top[:, None]), axis=1))


def bhattacharyya(c0, c1, variance):
    """Negative log Gaussian affinity, zero means, shared position variance."""
    average = (c0+c1)/2
    return .5*np.log(variance**2-average**2)-.25*np.log(
        (variance**2-c0**2)*(variance**2-c1**2))


def alternatives(p):
    return list(itertools.product(p["design_aliases"], p["design_decays"]))


def cost(lags, p):
    return float(p["reset_cost"]+np.mean(lags))


def choose_designs(p):
    grid = np.linspace(*p["lag_grid"])
    options = [[float(a)] if i == j else [float(a), float(b)]
               for i, a in enumerate(grid) for j, b in enumerate(grid) if i <= j]
    v = 1+p["measurement_noise_sd"]**2
    nulls = np.array([ref.cov(a, grid, p["decay_rate"]) for a in p["candidate_aliases"]])
    alts = np.array([ref.cov(a, grid, d) for a, d in alternatives(p)])
    # Shape: lag x comparison. Add distances before taking the minimum.
    disc = np.stack([bhattacharyya(nulls[i], nulls[j], v)
                     for i, j in itertools.combinations(range(3), 2)], axis=1)
    robust = bhattacharyya(alts[:, None, :], nulls[None, :, :], v).reshape(-1, len(grid)).T
    curves = []
    for i in range(len(grid)):
        for j in range(i, len(grid)):
            curves.append([float(np.min((disc[i]+disc[j])/2)),
                           float(np.min((robust[i]+robust[j])/2))])
    curves = np.array(curves)
    fg = np.linspace(*p["fisher_grid"])
    fi = ref.information(1, fg, v, p["fisher_derivative_step"], p["decay_rate"])
    selected = {}
    for regime in p["budget_regimes"]:
        timed = regime == "time_proxy"
        scale = np.array([cost(o, p) for o in options]) if timed else np.ones(len(options))
        values = curves/scale[:, None]
        scores = fi/(p["reset_cost"]+fg) if timed else fi
        selected[regime] = {
            "previous": p["previous_lags"],
            "local_fisher": [float(fg[np.argmax(scores)])],
            "null_discrimination": options[int(np.argmax(values[:, 0]))],
            "range_maximin": options[int(np.argmax(values[:, 1]))]}
    return selected, {"options": options, "criteria_per_pair": curves.tolist(),
                      "fisher_grid": fg.tolist(), "fisher_per_pair": fi.tolist()}


def pair_count(reference, lags, regime, p):
    available = reference if regime == "readings" else reference*cost(p["previous_lags"], p)/cost(lags, p)
    multiple = 2*len(lags)
    return multiple*int(np.floor(available/multiple+1e-10))


def likelihoods(data, lags, n, v, models):
    result = np.zeros((len(data[0][0]), len(models)))
    per = n//len(lags)
    for lag, (train, test) in zip(lags, data):
        total = train+test
        for j, (a, d) in enumerate(models):
            result[:, j] += family.ll(v, v, ref.cov(a, lag, d), per, total)
    return result


def mixture_score(data, lags, n, v, p):
    alt = likelihoods(data, lags, n, v, alternatives(p))
    null = likelihoods(data, lags, n, v, [(a, p["decay_rate"]) for a in p["candidate_aliases"]])
    mix = logmeanexp(alt)
    return mix-np.max(null, axis=1), mix, null


def main():
    raw = PROTOCOL.read_bytes()
    p = json.loads(raw)
    v = 1+p["measurement_noise_sd"]**2
    selected, design_audit = choose_designs(p)
    checks = {}
    def check(name, error, tol=1e-9):
        checks[name] = {"error": float(error), "tolerance": tol, "passed": bool(error < tol)}

    check("36_fixed_alternatives", abs(len(alternatives(p))-36))
    held = [s["alias"] for s in p["scenarios"] if s["class"] in ("fresh_range", "outside_range")]
    check("held_out_aliases_absent_from_grid", float(any(a in p["design_aliases"] for a in held)))
    check("190_lag_options", abs(len(design_audit["options"])-190))
    check("zero_bhattacharyya", abs(bhattacharyya(.3, .3, v)))
    c0, c1 = .3, -.6
    s0 = np.array([[v, c0], [c0, v]])
    s1 = np.array([[v, c1], [c1, v]])
    direct = .5*np.linalg.slogdet((s0+s1)/2)[1]-.25*(
        np.linalg.slogdet(s0)[1]+np.linalg.slogdet(s1)[1])
    check("bhattacharyya_matrix_formula", abs(direct-bhattacharyya(c0, c1, v)))
    check("bhattacharyya_symmetry", abs(bhattacharyya(c0, c1, v)-bhattacharyya(c1, c0, v)))
    check("logmeanexp_stability", abs(logmeanexp(np.array([[10000., 10000.]]))[0]-10000.))
    check("logmeanexp_scalar_reference", abs(logmeanexp(np.array([[1., 2., 3.]]))[0]-
                                           np.log((np.exp(1)+np.exp(2)+np.exp(3))/3)))
    # Finite-space audit of the domination argument, independent of Gaussian code.
    null_mass = np.array([[.1, .3, .6], [.5, .25, .25]])
    mixed_mass = np.mean([[.2, .7, .1], [.6, .1, .3]], axis=0)
    e = mixed_mass/null_mass.max(axis=0)
    check("discrete_mixture_normalized", abs(sum(mixed_mass)-1))
    check("discrete_null_expectations_bounded", max(0., float(np.max(null_mass@e))-1))
    # Compare matrix likelihood on raw points to sufficient-statistic evaluation.
    points = np.array([[.1, -.4], [.7, .2], [-.2, .3], [.6, -.1]])
    stats = np.array([[sum(points[:, 0]**2), sum(points[:, 1]**2), sum(points[:, 0]*points[:, 1])]])
    direct_ll = -len(points)*np.log(2*np.pi)-len(points)/2*np.linalg.slogdet(s0)[1]-.5*np.sum(
        (points@np.linalg.inv(s0))*points)
    check("raw_points_matrix_likelihood", abs(direct_ll-family.ll(v, v, c0, len(points), stats)[0]))
    rows, arrays = [], {}
    max_domination = max_swap = max_cost_overrun = 0.
    all_finite = positive = allocations = True
    for regime in p["budget_regimes"]:
        for budget in p["reference_pair_budgets"]:
            for design in p["designs"]:
                lags = selected[regime][design]
                n = pair_count(budget, lags, regime, p)
                if regime == "time_proxy":
                    max_cost_overrun = max(max_cost_overrun, n*cost(lags, p)-budget*cost(p["previous_lags"], p))
                allocations &= n >= 4*len(lags) and n % (2*len(lags)) == 0
                for scenario in p["scenarios"]:
                    index = len(rows)
                    rng = np.random.default_rng(np.random.SeedSequence([p["seed"], index]))
                    actual_v = 1+scenario.get("noise_sd", p["measurement_noise_sd"])**2
                    actual_p = {**p, "decay_rate": scenario["decay"]}
                    data = ref.datasets(rng, p["replicates"], n, lags, actual_v, scenario["alias"], actual_p)
                    score, mix, null = mixture_score(data, lags, n, v, p)
                    split, concentration = ref.practical_scores(data, lags, n, v, p)
                    max_domination = max(max_domination, float(np.max(score[:, None]-(mix[:, None]-null))))
                    if index == 0:
                        swapped = [(b, a) for a, b in data]
                        max_swap = float(np.max(abs(score-mixture_score(swapped, lags, n, v, p)[0])))
                    all_finite &= bool(np.all(np.isfinite(score)) and np.all(np.isfinite(split)))
                    positive &= all(np.all(t[:, 0]*t[:, 1]-t[:, 2]**2 > 0) for pair in data for t in pair)
                    decisions = {"mixture": score > np.log(1/p["alpha"]),
                                 "split": split > np.log(1/p["alpha"]),
                                 "concentration": concentration}
                    truth_response = family.response(p, scenario)
                    errors = [abs(family.response(p, {"alias": a, "decay": p["decay_rate"]})-
                                  truth_response)/abs(truth_response) for a in p["candidate_aliases"]]
                    rows.append({"regime": regime, "reference_pairs": budget, "design": design,
                                 "lags": lags, "pairs": n, "readings": 2*n,
                                 "time_proxy": n*cost(lags, p), "scenario": scenario,
                                 "response_error_if_null1": float(errors[0]),
                                 "best_candidate_response_error": float(min(errors)),
                                 "tests": {m: family.wilson(d) for m, d in decisions.items()}})
                    arrays[f"cell{index}"] = np.column_stack([score, split, concentration])
    check("evalue_pointwise_domination", max_domination)
    check("mixture_train_test_swap_invariant", max_swap)
    check("time_budgets_respected", max_cost_overrun)
    check("valid_equal_half_allocations", float(not allocations))
    check("finite_scores", float(not all_finite))
    check("sample_covariances_positive", float(not positive))
    # Verify selected finite-grid optima independently against stored objective table.
    for regime in p["budget_regimes"]:
        for col, name in enumerate(("null_discrimination", "range_maximin")):
            vals = np.array(design_audit["criteria_per_pair"])[:, col]
            if regime == "time_proxy":
                vals = vals/np.array([cost(o, p) for o in design_audit["options"]])
            ix = design_audit["options"].index(selected[regime][name])
            check(regime+"_"+name+"_grid_optimal", max(0., float(max(vals)-vals[ix])))
    report = {"protocol_sha256": hashlib.sha256(raw).hexdigest(),
              "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "dependency_sha256": {f.name: hashlib.sha256(f.read_bytes()).hexdigest()
                                    for f in (DEPENDENCY, HERE/"20_family_rejection.py")},
              "python": platform.python_version(), "numpy": np.__version__, "matplotlib": matplotlib.__version__,
              "scope": p["scope"], "selected_designs": selected, "design_audit": design_audit,
              "checks": checks, "all_checks_passed": all(c["passed"] for c in checks.values()),
              "dataset_evaluations": len(rows)*p["replicates"], "cells": rows,
              "trivial_baselines": {"always_warn": {"null_rejection": 1, "alternative_detection": 1},
                                    "never_warn": {"null_rejection": 0, "alternative_detection": 0}},
              "interpretation": p["interpretation"], "time_assumption": p["time_rule"]}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT/"results.json").write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
    np.savez_compressed(OUT/"scores.npz", **arrays)
    lines = ["regime,reference_pairs,design,pairs,time_proxy,scenario,class,response_error_if_null1,"+
             ",".join(METHODS)]
    for r in rows:
        fields = [r["regime"], r["reference_pairs"], r["design"], r["pairs"], r["time_proxy"],
                  r["scenario"]["name"], r["scenario"]["class"], r["response_error_if_null1"]]
        lines.append(",".join(map(str, fields+[r["tests"][m]["estimate"] for m in METHODS])))
    (OUT/"summary.csv").write_text("\n".join(lines)+"\n", encoding="utf-8")
    plot(p, rows)
    print(json.dumps({"checks": len(checks), "all_passed": report["all_checks_passed"],
                      "dataset_evaluations": report["dataset_evaluations"], "selected_designs": selected,
                      "largest_budget_results": [
                          {"regime": r["regime"], "design": r["design"], "pairs": r["pairs"],
                           "scenario": r["scenario"]["name"],
                           **{m: r["tests"][m]["estimate"] for m in METHODS}}
                          for r in rows if r["reference_pairs"] == max(p["reference_pair_budgets"])
                          and r["scenario"]["class"] != "null"]}, indent=2))
    assert report["all_checks_passed"]


def plot(p, rows):
    fig, axes = plt.subplots(2, 3, figsize=(14, 8), constrained_layout=True)
    names = [s["name"] for s in p["scenarios"] if s["class"] == "fresh_range"]
    colors = ["#64748b", "#187e83", "#b27732", "#7054a0"]
    for row, regime in enumerate(p["budget_regimes"]):
        for col, method in enumerate(METHODS):
            ax = axes[row, col]
            for design, color in zip(p["designs"], colors):
                subset = [r for r in rows if r["regime"] == regime and r["design"] == design and
                          r["reference_pairs"] == max(p["reference_pair_budgets"]) and
                          r["scenario"]["class"] == "fresh_range"]
                vals = [next(r["tests"][method] for r in subset if r["scenario"]["name"] == s) for s in names]
                y = np.array([r["estimate"] for r in vals])
                ci = np.array([r["wilson95"] for r in vals])
                ax.errorbar(np.arange(len(names)), y, yerr=[y-ci[:, 0], ci[:, 1]-y],
                            marker="o", markersize=3, capsize=2, label=design.replace("_", " "), color=color)
            ax.set_xticks(range(len(names)), ["-2.7", "+2.7", "-5.3", "+5.3", "-9.3", "+9.3"])
            ax.set(title=method+" / "+regime.replace("_", " "), ylim=(-.03, 1.03),
                   xlabel="Frequency shift (%)", ylabel="Rejection probability")
            ax.grid(alpha=.2)
    axes[0, 0].legend(fontsize=7, loc="lower right")
    fig.suptitle("Unknown-shift detection: fixed rules, fresh evaluation aliases\n"
                 "1,024 reference pairs; time proxy includes an assumed reset cost, not measured preparation time")
    fig.savefig(OUT/"range_design.png", dpi=170)
    plt.close(fig)


if __name__ == "__main__":
    main()
