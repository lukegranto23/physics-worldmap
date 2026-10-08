#!/usr/bin/env python3
"""Projectile motion: velocity Verlet (symplectic) versus forward Euler.

Model and units
---------------
Position is in metres, time in seconds, velocity in m/s, and acceleration in
m/s^2.  The only force is constant gravity, g = 9.81 m/s^2; air resistance,
Earth curvature, and rotation are neglected.  The ground is y = 0.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


G = 9.81


def integrate(v0: float, angle_deg: float, dt: float, method: str):
    """Integrate until first passage below the ground."""
    angle = np.deg2rad(angle_deg)
    r = np.array([0.0, 0.0])
    v = v0 * np.array([np.cos(angle), np.sin(angle)])
    acceleration = np.array([0.0, -G])
    times, positions, velocities = [0.0], [r.copy()], [v.copy()]

    for _ in range(1_000_000):
        if method == "verlet":
            r_new = r + v * dt + 0.5 * acceleration * dt**2
            v_new = v + acceleration * dt
        elif method == "euler":
            r_new = r + v * dt
            v_new = v + acceleration * dt
        else:
            raise ValueError(f"unknown method: {method}")
        r, v = r_new, v_new
        times.append(times[-1] + dt)
        positions.append(r.copy())
        velocities.append(v.copy())
        if r[1] < 0.0 and len(times) > 2:
            break
    else:
        raise RuntimeError("projectile did not hit the ground")
    return np.asarray(times), np.asarray(positions), np.asarray(velocities)


def interpolated_range(position: np.ndarray) -> float:
    """Linearly interpolate the final segment to y=0."""
    x0, y0 = position[-2]
    x1, y1 = position[-1]
    fraction = -y0 / (y1 - y0)
    return float(x0 + fraction * (x1 - x0))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--speed", type=float, default=50.0, help="launch speed [m/s]")
    parser.add_argument("--angle", type=float, default=42.0, help="launch angle [degrees]")
    parser.add_argument("--dt", type=float, default=0.01, help="time step [s]")
    parser.add_argument("--quick", action="store_true")
    parser.add_argument("--out-dir", type=Path, default=Path("results/projectile"))
    args = parser.parse_args()
    if args.quick:
        args.dt = max(args.dt, 0.03)
    if args.speed <= 0 or not 0 < args.angle < 90 or args.dt <= 0:
        raise ValueError("require speed>0, 0<angle<90 degrees, and dt>0")

    tv, rv, vv = integrate(args.speed, args.angle, args.dt, "verlet")
    te, re, ve = integrate(args.speed, args.angle, args.dt, "euler")
    theta = np.deg2rad(args.angle)
    exact_range = args.speed**2 * np.sin(2 * theta) / G
    exact_flight = 2 * args.speed * np.sin(theta) / G
    verlet_range = interpolated_range(rv)

    energy_v = 0.5 * np.sum(vv**2, axis=1) + G * rv[:, 1]
    energy_e = 0.5 * np.sum(ve**2, axis=1) + G * re[:, 1]
    # Exclude the interpolated-beyond-ground endpoint only conceptually: the
    # Hamiltonian is still conserved in free flight below y=0.
    verlet_energy_span = np.ptp(energy_v) / energy_v[0]
    range_relative_error = abs(verlet_range - exact_range) / exact_range
    if range_relative_error > 5e-4:
        raise AssertionError(f"trajectory error too large: {range_relative_error:.3e}")
    if verlet_energy_span > 2e-12:
        raise AssertionError(f"Verlet energy drift too large: {verlet_energy_span:.3e}")

    args.out_dir.mkdir(parents=True, exist_ok=True)
    np.savez(
        args.out_dir / "trajectory.npz",
        time_verlet=tv,
        position_verlet=rv,
        velocity_verlet=vv,
        time_euler=te,
        position_euler=re,
        velocity_euler=ve,
        units=np.array(["s", "m", "m/s"]),
    )

    t_exact = np.linspace(0.0, exact_flight, 400)
    x_exact = args.speed * np.cos(theta) * t_exact
    y_exact = args.speed * np.sin(theta) * t_exact - 0.5 * G * t_exact**2
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    axes[0].plot(x_exact, y_exact, "k--", label="analytic")
    axes[0].plot(rv[:, 0], rv[:, 1], label="velocity Verlet")
    axes[0].plot(re[:, 0], re[:, 1], label="forward Euler", alpha=0.8)
    axes[0].set(xlabel="x [m]", ylabel="y [m]", title="Projectile trajectory")
    axes[0].set_ylim(bottom=0)
    axes[0].legend()
    axes[0].grid(alpha=0.25)
    axes[1].plot(tv, energy_v - energy_v[0], label="Verlet")
    axes[1].plot(te, energy_e - energy_e[0], label="Euler")
    axes[1].set(
        xlabel="time [s]",
        ylabel=r"specific energy change [J kg$^{-1}$]",
        title="Numerical energy error",
    )
    axes[1].legend()
    axes[1].grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(args.out_dir / "projectile.png", dpi=180)
    plt.close(fig)

    print(
        "PASS projectile: "
        f"range={verlet_range:.4f} m (analytic {exact_range:.4f} m, "
        f"relative error {range_relative_error:.2e}); "
        f"Verlet energy span={verlet_energy_span:.2e}."
    )


if __name__ == "__main__":
    main()

