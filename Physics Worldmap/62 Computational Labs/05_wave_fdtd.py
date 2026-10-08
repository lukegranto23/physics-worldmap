#!/usr/bin/env python3
"""Finite-difference time-domain solution of the one-dimensional wave equation.

The ideal string has length 1 m, fixed ends, and wave speed 100 m/s.  Its
transverse displacement u obeys u_tt = c^2 u_xx.  The initial condition is the
fundamental standing-wave shape sin(pi*x/L), with zero velocity.  There is no
damping or dispersion in the continuum model.
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
    parser.add_argument("--grid", type=int, default=801)
    parser.add_argument("--duration", type=float, default=0.025, help="simulation time [s]")
    parser.add_argument("--courant", type=float, default=0.9)
    parser.add_argument("--quick", action="store_true")
    parser.add_argument("--out-dir", type=Path, default=Path("results/wave_fdtd"))
    args = parser.parse_args()
    if args.quick:
        args.grid = 201
    if args.grid < 21 or args.duration <= 0 or not 0 < args.courant <= 1:
        raise ValueError("require grid>=21, duration>0, and 0<Courant<=1")

    length, wave_speed = 1.0, 100.0
    x = np.linspace(0.0, length, args.grid)
    dx = x[1] - x[0]
    requested_dt = args.courant * dx / wave_speed
    steps = int(np.ceil(args.duration / requested_dt))
    dt = args.duration / steps
    courant = wave_speed * dt / dx
    if courant > 1.0 + 1e-14:
        raise AssertionError("FDTD stability condition violated")

    old = np.sin(np.pi * x / length)
    old[[0, -1]] = 0.0
    current = old.copy()
    current[1:-1] += 0.5 * courant**2 * (
        old[2:] - 2 * old[1:-1] + old[:-2]
    )
    current[[0, -1]] = 0.0

    requested_snapshots = np.array([0.0, 0.25, 0.5, 0.75, 1.0])
    snapshot_steps = np.unique(np.rint(requested_snapshots * steps).astype(int))
    snapshots = {0: old.copy()}
    for step in range(1, steps):
        new = np.zeros_like(current)
        new[1:-1] = (
            2 * current[1:-1]
            - old[1:-1]
            + courant**2 * (current[2:] - 2 * current[1:-1] + current[:-2])
        )
        if step in snapshot_steps:
            snapshots[step] = current.copy()
        old, current = current, new
    snapshots[steps] = current.copy()

    exact_final = np.sin(np.pi * x / length) * np.cos(
        np.pi * wave_speed * args.duration / length
    )
    # Normalize by the initial amplitude, not the instantaneous exact field:
    # at quarter-periods the exact displacement vanishes, making a conventional
    # relative error singular even for an accurate phase.
    scaled_l2_error = np.linalg.norm(current - exact_final) / np.linalg.norm(
        np.sin(np.pi * x / length)
    )
    boundary_error = max(abs(current[0]), abs(current[-1]))
    # Second-order convergence gives a generous resolution-scaled acceptance bound.
    error_bound = max(2e-5, 15.0 * dx**2)
    if scaled_l2_error > error_bound or boundary_error > 1e-14:
        raise AssertionError(
            f"wave validation failed: scaled L2={scaled_l2_error:.2e} "
            f"(bound {error_bound:.2e}), boundary={boundary_error:.2e}"
        )

    ordered_steps = np.array(sorted(snapshots))
    snapshot_array = np.array([snapshots[s] for s in ordered_steps])
    args.out_dir.mkdir(parents=True, exist_ok=True)
    np.savez(
        args.out_dir / "wave_solution.npz",
        x_m=x,
        snapshot_time_s=ordered_steps * dt,
        displacement_m=snapshot_array,
        final_exact_m=exact_final,
        courant=courant,
    )
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.4))
    for step, state in zip(ordered_steps, snapshot_array):
        axes[0].plot(x, state, label=f"t={step*dt*1e3:.2f} ms")
    axes[0].set(xlabel="x [m]", ylabel="u [m]", title="String snapshots")
    axes[0].legend(fontsize=8, ncol=2)
    axes[0].grid(alpha=0.25)
    axes[1].plot(x, current - exact_final)
    axes[1].set(
        xlabel="x [m]",
        ylabel="numerical - exact [m]",
        title=f"Final error (initial-amplitude L2 = {scaled_l2_error:.2e})",
    )
    axes[1].grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(args.out_dir / "wave_fdtd.png", dpi=180)
    plt.close(fig)
    print(
        "PASS wave FDTD: "
        f"Courant={courant:.4f}, dx={dx:.3e} m, dt={dt:.3e} s, "
        f"final initial-amplitude-scaled L2 error={scaled_l2_error:.2e}."
    )


if __name__ == "__main__":
    main()
