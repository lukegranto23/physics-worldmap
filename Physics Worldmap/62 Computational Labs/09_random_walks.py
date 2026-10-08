#!/usr/bin/env python3
"""Ensemble of unbiased two-dimensional lattice random walks.

Each walker makes one independent unit-length step per unit time, choosing
north, south, east, or west with equal probability.  Therefore
<r^2(n)> = n and the continuum Einstein relation <r^2> = 4 D t gives D = 1/4
in lattice_length^2 per step.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--walkers", type=int, default=20_000)
    parser.add_argument("--steps", type=int, default=1_200)
    parser.add_argument("--seed", type=int, default=20260730)
    parser.add_argument("--quick", action="store_true")
    parser.add_argument("--out-dir", type=Path, default=Path("results/random_walks"))
    args = parser.parse_args()
    if args.quick:
        args.walkers, args.steps = 4_000, 400
    if args.walkers < 500 or args.steps < 50:
        raise ValueError("use at least 500 walkers and 50 steps for an ensemble check")

    rng = np.random.default_rng(args.seed)
    position = np.zeros((args.walkers, 2), dtype=np.int32)
    mean_square_displacement = np.zeros(args.steps + 1)
    mean_position = np.zeros((args.steps + 1, 2))
    directions = np.array([[1, 0], [-1, 0], [0, 1], [0, -1]], dtype=np.int8)
    for step in range(1, args.steps + 1):
        choice = rng.integers(0, 4, size=args.walkers)
        position += directions[choice]
        mean_square_displacement[step] = np.mean(np.sum(position.astype(float) ** 2, axis=1))
        mean_position[step] = np.mean(position, axis=0)

    time = np.arange(args.steps + 1, dtype=float)
    fit_start = max(10, args.steps // 10)
    slope, intercept = np.polyfit(
        time[fit_start:], mean_square_displacement[fit_start:], 1
    )
    diffusion_coefficient = slope / 4.0
    slope_tolerance = 0.12 if args.quick else 0.06
    standard_error_mean_coordinate = np.sqrt(args.steps / (2 * args.walkers))
    drift_z = np.max(np.abs(mean_position[-1]) / standard_error_mean_coordinate)
    if abs(slope - 1.0) > slope_tolerance or drift_z > 4.5:
        raise AssertionError(
            f"random-walk validation failed: MSD slope={slope:.3f}, drift z={drift_z:.2f}"
        )

    args.out_dir.mkdir(parents=True, exist_ok=True)
    np.savez(
        args.out_dir / "random_walks.npz",
        step=time,
        mean_square_displacement=mean_square_displacement,
        mean_position=mean_position,
        final_position=position,
        fitted_slope=slope,
        diffusion_coefficient=diffusion_coefficient,
        seed=args.seed,
    )
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.5))
    axes[0].plot(time, mean_square_displacement, label="simulation")
    axes[0].plot(time, time, "k--", label=r"exact $\langle r^2\rangle=n$")
    axes[0].plot(time, slope * time + intercept, ":", label=f"fit slope={slope:.3f}")
    axes[0].set(
        xlabel="step n",
        ylabel=r"$\langle r^2\rangle$ [lattice units$^2$]",
        title=f"Einstein diffusion: D={diffusion_coefficient:.3f}",
    )
    axes[0].legend()
    axes[0].grid(alpha=0.25)
    subset = min(1500, args.walkers)
    axes[1].scatter(position[:subset, 0], position[:subset, 1], s=4, alpha=0.25)
    extent = 3.5 * np.sqrt(args.steps / 2)
    axes[1].set(
        xlabel="x [lattice units]",
        ylabel="y [lattice units]",
        title=f"{subset} endpoints after {args.steps} steps",
        xlim=(-extent, extent),
        ylim=(-extent, extent),
        aspect="equal",
    )
    axes[1].grid(alpha=0.2)
    fig.tight_layout()
    fig.savefig(args.out_dir / "random_walks.png", dpi=180)
    plt.close(fig)
    print(
        "PASS random walks: "
        f"MSD slope={slope:.4f} (exact 1), D={diffusion_coefficient:.4f} "
        f"(exact 0.25), endpoint drift z={drift_z:.2f}, seed={args.seed}."
    )


if __name__ == "__main__":
    main()

