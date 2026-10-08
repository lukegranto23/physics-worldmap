#!/usr/bin/env python3
"""Lorenz attractor, sensitivity to initial conditions, and Lyapunov estimate.

The dimensionless Lorenz equations use the classic chaotic parameters
sigma=10, rho=28, beta=8/3.  Fourth-order Runge-Kutta advances the state.  The
largest Lyapunov exponent is estimated by repeatedly evolving and renormalizing
a nearby trajectory after a transient (the Benettin two-trajectory method).
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


SIGMA, RHO, BETA = 10.0, 28.0, 8.0 / 3.0


def derivative(state: np.ndarray) -> np.ndarray:
    x, y, z = state
    return np.array([SIGMA * (y - x), x * (RHO - z) - y, x * y - BETA * z])


def rk4(state: np.ndarray, dt: float) -> np.ndarray:
    k1 = derivative(state)
    k2 = derivative(state + 0.5 * dt * k1)
    k3 = derivative(state + 0.5 * dt * k2)
    k4 = derivative(state + dt * k3)
    return state + dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6.0


def evolve(initial: np.ndarray, duration: float, dt: float):
    steps = int(round(duration / dt))
    states = np.empty((steps + 1, 3))
    states[0] = initial
    for index in range(steps):
        states[index + 1] = rk4(states[index], dt)
    return np.arange(steps + 1) * dt, states


def lyapunov_exponent(initial: np.ndarray, duration: float, dt: float, transient: float):
    epsilon = 1e-8
    block_steps = max(1, int(round(0.1 / dt)))
    base = initial.copy()
    nearby = base + np.array([epsilon, 0.0, 0.0])
    log_growth, measured_time, elapsed = 0.0, 0.0, 0.0
    while elapsed + block_steps * dt <= duration + 1e-14:
        for _ in range(block_steps):
            base = rk4(base, dt)
            nearby = rk4(nearby, dt)
        elapsed += block_steps * dt
        difference = nearby - base
        distance = np.linalg.norm(difference)
        if not np.isfinite(distance) or distance == 0:
            raise FloatingPointError("nearby-trajectory separation became invalid")
        if elapsed > transient:
            log_growth += np.log(distance / epsilon)
            measured_time += block_steps * dt
        nearby = base + epsilon * difference / distance
    return log_growth / measured_time


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--duration", type=float, default=45.0)
    parser.add_argument("--dt", type=float, default=0.005)
    parser.add_argument("--quick", action="store_true")
    parser.add_argument("--out-dir", type=Path, default=Path("results/lorenz"))
    args = parser.parse_args()
    if args.quick:
        args.duration, args.dt = 25.0, 0.01
    if args.duration < 15 or args.dt <= 0 or args.dt > 0.02:
        raise ValueError("require duration>=15 and 0<dt<=0.02")

    initial = np.array([1.0, 1.0, 1.0])
    time, trajectory = evolve(initial, args.duration, args.dt)
    shadow_initial = initial + np.array([1e-8, 0.0, 0.0])
    _, shadow = evolve(shadow_initial, args.duration, args.dt)
    separation = np.linalg.norm(shadow - trajectory, axis=1)
    exponent = lyapunov_exponent(initial, args.duration, args.dt, transient=5.0)

    # A short-time step-halving check remains meaningful before chaos amplifies
    # tiny truncation differences into macroscopically different trajectories.
    _, coarse = evolve(initial, 1.0, args.dt)
    _, fine = evolve(initial, 1.0, args.dt / 2)
    convergence_error = np.linalg.norm(coarse[-1] - fine[-1]) / np.linalg.norm(fine[-1])
    if not np.all(np.isfinite(trajectory)):
        raise AssertionError("Lorenz trajectory contains non-finite values")
    if not 0.45 < exponent < 1.35 or convergence_error > 8e-5:
        raise AssertionError(
            f"Lorenz validation failed: lambda={exponent:.3f}, "
            f"step-halving error={convergence_error:.2e}"
        )

    args.out_dir.mkdir(parents=True, exist_ok=True)
    np.savez(
        args.out_dir / "lorenz_solution.npz",
        time=time,
        trajectory=trajectory,
        shadow_trajectory=shadow,
        separation=separation,
        lyapunov_exponent=exponent,
        parameters=np.array([SIGMA, RHO, BETA]),
    )
    fig = plt.figure(figsize=(11.5, 4.8))
    axis_attractor = fig.add_subplot(1, 2, 1, projection="3d")
    axis_attractor.plot(
        trajectory[:, 0], trajectory[:, 1], trajectory[:, 2], lw=0.55, color="#3a86ff"
    )
    axis_attractor.set(xlabel="x", ylabel="y", zlabel="z", title="Lorenz attractor")
    axis_separation = fig.add_subplot(1, 2, 2)
    axis_separation.semilogy(time, np.maximum(separation, 1e-16))
    axis_separation.set(
        xlabel="dimensionless time",
        ylabel="distance between trajectories",
        title=f"Sensitivity (largest Lyapunov ~ {exponent:.3f})",
    )
    axis_separation.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(args.out_dir / "lorenz_chaos.png", dpi=180)
    plt.close(fig)
    print(
        "PASS Lorenz: "
        f"largest Lyapunov exponent={exponent:.3f} inverse-time "
        f"(reference about 0.91); short-time step-halving error={convergence_error:.2e}."
    )


if __name__ == "__main__":
    main()

