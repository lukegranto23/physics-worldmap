#!/usr/bin/env python3
"""Lorentz transformations, invariant intervals, and velocity addition.

Coordinates use ct and x in light-seconds, so c=1 and both coordinates have the
same unit.  The primed inertial frame moves at beta=v/c relative to the lab:
ct' = gamma(ct-beta*x), x' = gamma(x-beta*ct).  Only one spatial dimension is
shown; transverse coordinates would be unchanged.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def lorentz(events: np.ndarray, beta: float) -> np.ndarray:
    if abs(beta) >= 1:
        raise ValueError("a massive inertial frame requires |beta|<1")
    gamma = 1.0 / np.sqrt(1.0 - beta**2)
    ct, x = events[:, 0], events[:, 1]
    return np.column_stack((gamma * (ct - beta * x), gamma * (x - beta * ct)))


def interval_squared(events: np.ndarray) -> np.ndarray:
    return events[:, 0] ** 2 - events[:, 1] ** 2


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--beta", type=float, default=0.8, help="frame speed v/c")
    parser.add_argument("--quick", action="store_true")
    parser.add_argument("--out-dir", type=Path, default=Path("results/relativity"))
    args = parser.parse_args()
    if abs(args.beta) >= 0.99:
        raise ValueError("choose |beta|<0.99 to keep this visualization legible")

    events = np.array(
        [
            [0.0, 0.0],
            [2.0, 0.0],
            [2.0, 1.0],
            [3.0, 3.0],
            [1.0, 2.0],
            [5.0, -1.0],
        ]
    )
    transformed = lorentz(events, args.beta)
    recovered = lorentz(transformed, -args.beta)
    interval_error = np.max(
        np.abs(interval_squared(transformed) - interval_squared(events))
    )
    inverse_error = np.max(np.abs(recovered - events))

    object_velocity = np.array([-0.9, -0.3, 0.0, 0.5, 0.9])
    transformed_velocity = (object_velocity - args.beta) / (
        1.0 - args.beta * object_velocity
    )
    if interval_error > 2e-13 or inverse_error > 2e-13:
        raise AssertionError(
            f"Lorentz invariance failure: interval={interval_error:.2e}, inverse={inverse_error:.2e}"
        )
    if np.any(np.abs(transformed_velocity) >= 1.0 + 1e-14):
        raise AssertionError("subluminal velocity transformed outside the light cone")

    gamma = 1.0 / np.sqrt(1.0 - args.beta**2)
    table = np.column_stack(
        (
            events,
            transformed,
            interval_squared(events),
            interval_squared(transformed),
        )
    )
    args.out_dir.mkdir(parents=True, exist_ok=True)
    np.savetxt(
        args.out_dir / "lorentz_events.csv",
        table,
        delimiter=",",
        header="ct_light_s,x_light_s,ct_prime_light_s,x_prime_light_s,s2_light_s2,s2_prime_light_s2",
        comments="",
    )
    np.savetxt(
        args.out_dir / "velocity_addition.csv",
        np.column_stack((object_velocity, transformed_velocity)),
        delimiter=",",
        header="u_over_c,u_prime_over_c",
        comments="",
    )

    beta_grid = np.linspace(-0.98, 0.98, 600)
    gamma_grid = 1 / np.sqrt(1 - beta_grid**2)
    doppler_grid = np.sqrt((1 + beta_grid) / (1 - beta_grid))
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.7))
    cone_ct = np.linspace(0, 5.5, 100)
    axes[0].plot(cone_ct, cone_ct, "k--", lw=1, label="light cone")
    axes[0].plot(-cone_ct, cone_ct, "k--", lw=1)
    axes[0].scatter(events[:, 1], events[:, 0], label="lab coordinates", s=34)
    axes[0].scatter(
        transformed[:, 1], transformed[:, 0], marker="x", s=46, label="primed coordinates"
    )
    for index, (ct, x) in enumerate(events):
        axes[0].annotate(str(index), (x, ct), xytext=(4, 4), textcoords="offset points")
    axes[0].set(
        xlabel="x [light-second]",
        ylabel="ct [light-second]",
        title=f"Events under a boost beta={args.beta:.2f}",
        aspect="equal",
        xlim=(-5.5, 5.5),
        ylim=(-0.5, 7.0),
    )
    axes[0].legend(fontsize=8)
    axes[0].grid(alpha=0.2)
    axes[1].plot(beta_grid, gamma_grid, label=r"$\gamma$")
    axes[1].plot(beta_grid, doppler_grid, label="longitudinal Doppler factor")
    axes[1].axvline(args.beta, color="k", ls=":", label=f"chosen gamma={gamma:.3f}")
    axes[1].set(
        xlabel=r"$\beta=v/c$",
        ylabel="dimensionless factor",
        title="Relativistic factors",
        ylim=(0, 8),
    )
    axes[1].legend(fontsize=8)
    axes[1].grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(args.out_dir / "special_relativity.png", dpi=180)
    plt.close(fig)
    print(
        "PASS special relativity: "
        f"beta={args.beta:.3f}, gamma={gamma:.6f}, "
        f"max interval error={interval_error:.2e} light-second^2, "
        f"inverse error={inverse_error:.2e} light-second."
    )


if __name__ == "__main__":
    main()

