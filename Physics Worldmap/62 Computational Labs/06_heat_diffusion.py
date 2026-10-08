#!/usr/bin/env python3
"""Explicit finite-difference solution of heat diffusion in a rod.

The rod is 1 m long with thermal diffusivity alpha = 1e-4 m^2/s.  Its ends are
held at 0 degC, while the initial excess temperature is
100*sin(pi*x/L) degC.  With constant material properties this single Fourier
mode decays exactly as exp[-alpha*(pi/L)^2*t].
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def integrate_profile(values: np.ndarray, coordinate: np.ndarray) -> float:
    """Composite trapezoid rule, compatible with both NumPy 1.x and 2.x."""
    return float(
        np.sum(0.5 * (values[1:] + values[:-1]) * np.diff(coordinate))
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--grid", type=int, default=301)
    parser.add_argument("--duration", type=float, default=400.0, help="seconds")
    parser.add_argument("--stability", type=float, default=0.45, help="alpha*dt/dx^2")
    parser.add_argument("--quick", action="store_true")
    parser.add_argument("--out-dir", type=Path, default=Path("results/heat_diffusion"))
    args = parser.parse_args()
    if args.quick:
        args.grid = 101
    if args.grid < 21 or args.duration <= 0 or not 0 < args.stability <= 0.5:
        raise ValueError("require grid>=21, duration>0, and 0<alpha*dt/dx^2<=0.5")

    length, diffusivity, amplitude = 1.0, 1e-4, 100.0
    x = np.linspace(0.0, length, args.grid)
    dx = x[1] - x[0]
    dt_requested = args.stability * dx**2 / diffusivity
    steps = int(np.ceil(args.duration / dt_requested))
    dt = args.duration / steps
    ratio = diffusivity * dt / dx**2
    if ratio > 0.5 + 1e-14:
        raise AssertionError("FTCS diffusion stability condition violated")

    temperature = amplitude * np.sin(np.pi * x / length)
    targets = np.unique(np.rint(np.linspace(0, steps, 5)).astype(int))
    snapshots = {0: temperature.copy()}
    heat_content = [integrate_profile(temperature, x)]
    heat_time = [0.0]
    for step in range(1, steps + 1):
        updated = temperature.copy()
        updated[1:-1] += ratio * (
            temperature[2:] - 2 * temperature[1:-1] + temperature[:-2]
        )
        updated[[0, -1]] = 0.0
        temperature = updated
        if step in targets:
            snapshots[step] = temperature.copy()
        if step % max(1, steps // 250) == 0:
            heat_time.append(step * dt)
            heat_content.append(integrate_profile(temperature, x))

    exact = amplitude * np.sin(np.pi * x / length) * np.exp(
        -diffusivity * (np.pi / length) ** 2 * args.duration
    )
    relative_l2_error = np.linalg.norm(temperature - exact) / np.linalg.norm(exact)
    maximum_principle_ok = np.min(temperature) >= -1e-12 and np.max(temperature) <= amplitude + 1e-12
    if relative_l2_error > max(3e-5, 2.0 * dx**2) or not maximum_principle_ok:
        raise AssertionError(
            f"heat validation failed: L2={relative_l2_error:.2e}, "
            f"maximum principle={maximum_principle_ok}"
        )

    ordered_steps = np.array(sorted(snapshots))
    snapshot_array = np.array([snapshots[s] for s in ordered_steps])
    args.out_dir.mkdir(parents=True, exist_ok=True)
    np.savez(
        args.out_dir / "heat_solution.npz",
        x_m=x,
        snapshot_time_s=ordered_steps * dt,
        temperature_c=snapshot_array,
        final_exact_c=exact,
        heat_time_s=np.asarray(heat_time),
        integrated_temperature_c_m=np.asarray(heat_content),
        alpha_m2_s=diffusivity,
    )
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.3))
    for step, state in zip(ordered_steps, snapshot_array):
        axes[0].plot(x, state, label=f"{step*dt:.0f} s")
    axes[0].set(xlabel="x [m]", ylabel="temperature [degC]", title="Diffusion of a Fourier mode")
    axes[0].legend()
    axes[0].grid(alpha=0.25)
    axes[1].plot(x, temperature - exact)
    axes[1].set(
        xlabel="x [m]",
        ylabel="numerical - exact [degC]",
        title=f"Final error (relative L2 = {relative_l2_error:.2e})",
    )
    axes[1].grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(args.out_dir / "heat_diffusion.png", dpi=180)
    plt.close(fig)
    print(
        "PASS heat diffusion: "
        f"alpha*dt/dx^2={ratio:.4f}, steps={steps}, "
        f"final relative L2 error={relative_l2_error:.2e}; maximum principle holds."
    )


if __name__ == "__main__":
    main()
