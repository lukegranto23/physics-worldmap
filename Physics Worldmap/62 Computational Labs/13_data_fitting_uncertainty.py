#!/usr/bin/env python3
"""Weighted fitting and uncertainty propagation for a pendulum experiment.

For small angles, T^2 = b + (4*pi^2/g)L.  The optional intercept b absorbs a
small timing offset.  Synthetic periods have independent Gaussian uncertainty
sigma_T=0.003 s; length uncertainty is neglected.  Weighted linear least
squares estimates b and the slope, whose covariance is propagated to g.

A repeated-experiment Monte Carlo checks whether the analytic one-sigma
uncertainty has approximately the advertised 68% coverage.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


G_TRUE = 9.80665
SIGMA_PERIOD = 0.003
INTERCEPT_TRUE = 0.002


def weighted_fit(length: np.ndarray, measured_period: np.ndarray):
    y = measured_period**2
    sigma_y = 2 * measured_period * SIGMA_PERIOD
    design = np.column_stack((np.ones_like(length), length))
    weights = 1.0 / sigma_y**2
    normal_matrix = design.T @ (weights[:, None] * design)
    covariance = np.linalg.inv(normal_matrix)
    parameters = covariance @ (design.T @ (weights * y))
    residual = y - design @ parameters
    chi_square = np.sum((residual / sigma_y) ** 2)
    intercept, slope = parameters
    g = 4 * np.pi**2 / slope
    sigma_g = 4 * np.pi**2 / slope**2 * np.sqrt(covariance[1, 1])
    return {
        "parameters": parameters,
        "covariance": covariance,
        "sigma_y": sigma_y,
        "residual": residual,
        "chi_square": chi_square,
        "g": g,
        "sigma_g": sigma_g,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=20260730)
    parser.add_argument("--trials", type=int, default=5_000)
    parser.add_argument("--quick", action="store_true")
    parser.add_argument("--out-dir", type=Path, default=Path("results/data_fitting"))
    args = parser.parse_args()
    if args.quick:
        args.trials = 1_000
    if args.trials < 500:
        raise ValueError("use at least 500 trials for the coverage check")

    rng = np.random.default_rng(args.seed)
    length = np.linspace(0.20, 1.20, 16)
    slope_true = 4 * np.pi**2 / G_TRUE
    true_period = np.sqrt(INTERCEPT_TRUE + slope_true * length)
    measured_period = true_period + rng.normal(0.0, SIGMA_PERIOD, size=length.size)
    fit = weighted_fit(length, measured_period)
    degrees_of_freedom = length.size - 2
    reduced_chi_square = fit["chi_square"] / degrees_of_freedom
    pull = (fit["g"] - G_TRUE) / fit["sigma_g"]

    trial_g = np.empty(args.trials)
    trial_sigma_g = np.empty(args.trials)
    for trial in range(args.trials):
        trial_period = true_period + rng.normal(0.0, SIGMA_PERIOD, size=length.size)
        trial_fit = weighted_fit(length, trial_period)
        trial_g[trial] = trial_fit["g"]
        trial_sigma_g[trial] = trial_fit["sigma_g"]
    coverage = np.mean(np.abs(trial_g - G_TRUE) <= trial_sigma_g)
    empirical_to_reported = np.std(trial_g, ddof=1) / np.mean(trial_sigma_g)

    covariance_eigenvalues = np.linalg.eigvalsh(fit["covariance"])
    if np.any(covariance_eigenvalues <= 0):
        raise AssertionError("fit covariance is not positive definite")
    if abs(pull) > 3.5 or not 0.61 < coverage < 0.75 or not 0.80 < empirical_to_reported < 1.20:
        raise AssertionError(
            f"uncertainty validation failed: pull={pull:.2f}, "
            f"coverage={coverage:.3f}, sigma ratio={empirical_to_reported:.3f}"
        )

    args.out_dir.mkdir(parents=True, exist_ok=True)
    measurement_table = np.column_stack(
        (
            length,
            measured_period,
            measured_period**2,
            fit["sigma_y"],
            fit["residual"],
        )
    )
    np.savetxt(
        args.out_dir / "pendulum_measurements.csv",
        measurement_table,
        delimiter=",",
        header="length_m,period_s,period_squared_s2,sigma_period_squared_s2,residual_s2",
        comments="",
    )
    summary = {
        "model": "T^2 = intercept + slope*L",
        "seed": args.seed,
        "intercept_s2": float(fit["parameters"][0]),
        "slope_s2_per_m": float(fit["parameters"][1]),
        "covariance": fit["covariance"].tolist(),
        "g_m_per_s2": float(fit["g"]),
        "sigma_g_m_per_s2": float(fit["sigma_g"]),
        "chi_square": float(fit["chi_square"]),
        "degrees_of_freedom": degrees_of_freedom,
        "monte_carlo_trials": args.trials,
        "one_sigma_coverage": float(coverage),
        "empirical_to_reported_sigma": float(empirical_to_reported),
    }
    with (args.out_dir / "fit_summary.json").open("w", encoding="utf-8") as stream:
        json.dump(summary, stream, indent=2)
        stream.write("\n")

    length_line = np.linspace(0.15, 1.25, 300)
    y_line = fit["parameters"][0] + fit["parameters"][1] * length_line
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.5))
    axes[0].errorbar(
        length,
        measured_period**2,
        yerr=fit["sigma_y"],
        fmt="o",
        capsize=2,
        label="synthetic measurement",
    )
    axes[0].plot(length_line, y_line, label="weighted fit")
    axes[0].set(
        xlabel="pendulum length L [m]",
        ylabel=r"$T^2$ [s$^2$]",
        title=f"g = {fit['g']:.4f} +/- {fit['sigma_g']:.4f} m/s^2",
    )
    axes[0].legend()
    axes[0].grid(alpha=0.25)
    axes[1].hist(trial_g, bins=45, density=True, alpha=0.75)
    axes[1].axvline(G_TRUE, color="k", ls="--", label="true g")
    axes[1].axvspan(
        G_TRUE - np.mean(trial_sigma_g),
        G_TRUE + np.mean(trial_sigma_g),
        color="k",
        alpha=0.12,
        label=f"mean reported 1 sigma; coverage={coverage:.3f}",
    )
    axes[1].set(
        xlabel="fitted g [m/s^2]",
        ylabel="probability density",
        title=f"{args.trials} repeated experiments",
    )
    axes[1].legend(fontsize=8)
    axes[1].grid(alpha=0.2)
    fig.tight_layout()
    fig.savefig(args.out_dir / "data_fitting_uncertainty.png", dpi=180)
    plt.close(fig)
    print(
        "PASS data fitting: "
        f"g={fit['g']:.5f} +/- {fit['sigma_g']:.5f} m/s^2 "
        f"(pull={pull:.2f}), chi2/dof={reduced_chi_square:.2f}, "
        f"Monte Carlo 1-sigma coverage={coverage:.3f}, seed={args.seed}."
    )


if __name__ == "__main__":
    main()

