#!/usr/bin/env python3
"""Symplectic Sun-Earth-Jupiter integration in astronomical units.

Units are AU, Julian years, and solar masses.  In these units
G = 4*pi^2 AU^3 / (solar_mass year^2).  Bodies are point masses in a planar,
isolated Newtonian system; relativity, other planets, and collisions are absent.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


G = 4.0 * np.pi**2


def accelerations(r: np.ndarray, masses: np.ndarray) -> np.ndarray:
    delta = r[np.newaxis, :, :] - r[:, np.newaxis, :]
    distance2 = np.sum(delta**2, axis=2)
    np.fill_diagonal(distance2, np.inf)
    inverse_r3 = distance2 ** (-1.5)
    return G * np.sum(delta * inverse_r3[:, :, None] * masses[None, :, None], axis=1)


def invariants(r: np.ndarray, v: np.ndarray, masses: np.ndarray):
    kinetic = 0.5 * np.sum(masses[:, None] * v**2)
    potential = 0.0
    for i in range(len(masses)):
        for j in range(i + 1, len(masses)):
            potential -= G * masses[i] * masses[j] / np.linalg.norm(r[j] - r[i])
    momentum = np.sum(masses[:, None] * v, axis=0)
    angular_momentum = np.sum(masses * (r[:, 0] * v[:, 1] - r[:, 1] * v[:, 0]))
    return kinetic + potential, momentum, angular_momentum


def initial_conditions():
    masses = np.array([1.0, 3.003e-6, 9.545e-4])
    radii = np.array([0.0, 1.0, 5.2044])
    r = np.column_stack((radii, np.zeros(3)))
    v = np.zeros((3, 2))
    v[1:, 1] = np.sqrt(G * (masses[0] + masses[1:]) / radii[1:])
    # Move to the centre-of-mass frame exactly.
    r[0] = -np.sum(masses[1:, None] * r[1:], axis=0) / masses[0]
    v[0] = -np.sum(masses[1:, None] * v[1:], axis=0) / masses[0]
    r -= np.sum(masses[:, None] * r, axis=0) / np.sum(masses)
    return masses, r, v


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--years", type=float, default=24.0)
    parser.add_argument("--dt", type=float, default=0.002, help="time step [year]")
    parser.add_argument("--quick", action="store_true")
    parser.add_argument("--out-dir", type=Path, default=Path("results/nbody"))
    args = parser.parse_args()
    if args.quick:
        args.years, args.dt = 3.0, 0.004
    if args.years <= 0 or args.dt <= 0:
        raise ValueError("years and dt must be positive")

    masses, r, v = initial_conditions()
    steps = int(np.ceil(args.years / args.dt))
    keep_every = max(1, steps // 6000)
    time_history, r_history, energy_history, lz_history, p_history = [], [], [], [], []
    a = accelerations(r, masses)
    for step in range(steps + 1):
        if step % keep_every == 0 or step == steps:
            energy, momentum, lz = invariants(r, v, masses)
            time_history.append(step * args.dt)
            r_history.append(r.copy())
            energy_history.append(energy)
            lz_history.append(lz)
            p_history.append(momentum)
        if step == steps:
            break
        r_new = r + v * args.dt + 0.5 * a * args.dt**2
        a_new = accelerations(r_new, masses)
        v_new = v + 0.5 * (a + a_new) * args.dt
        r, v, a = r_new, v_new, a_new

    time_history = np.asarray(time_history)
    r_history = np.asarray(r_history)
    energy_history = np.asarray(energy_history)
    lz_history = np.asarray(lz_history)
    p_history = np.asarray(p_history)
    energy_error = np.max(np.abs(energy_history / energy_history[0] - 1.0))
    lz_error = np.max(np.abs(lz_history / lz_history[0] - 1.0))
    momentum_norm = np.max(np.linalg.norm(p_history, axis=1))
    if energy_error > 2e-4 or lz_error > 2e-11 or momentum_norm > 2e-14:
        raise AssertionError(
            f"invariant failure: dE={energy_error:.2e}, dL={lz_error:.2e}, |P|={momentum_norm:.2e}"
        )

    args.out_dir.mkdir(parents=True, exist_ok=True)
    np.savez(
        args.out_dir / "orbits.npz",
        time_year=time_history,
        position_au=r_history,
        energy=energy_history,
        angular_momentum=lz_history,
        momentum=p_history,
        mass_solar=masses,
        names=np.array(["Sun", "Earth", "Jupiter"]),
    )
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 5))
    colors = ["#f4a261", "#277da1", "#9c6644"]
    for index, name in enumerate(("Sun", "Earth", "Jupiter")):
        axes[0].plot(
            r_history[:, index, 0],
            r_history[:, index, 1],
            color=colors[index],
            label=name,
            lw=1.2,
        )
        axes[0].scatter(*r_history[0, index], color=colors[index], s=18)
    axes[0].set(
        xlabel="x [AU]", ylabel="y [AU]", title="Barycentric Newtonian orbits", aspect="equal"
    )
    axes[0].legend()
    axes[0].grid(alpha=0.2)
    axes[1].plot(time_history, energy_history / energy_history[0] - 1, label="energy")
    axes[1].plot(time_history, lz_history / lz_history[0] - 1, label=r"$L_z$")
    axes[1].set(xlabel="time [year]", ylabel="fractional change", title="Conservation diagnostics")
    axes[1].legend()
    axes[1].grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(args.out_dir / "nbody_orbits.png", dpi=180)
    plt.close(fig)
    print(
        "PASS N-body: "
        f"max |Delta E/E|={energy_error:.2e}, "
        f"max |Delta L/L|={lz_error:.2e}, max |P|={momentum_norm:.2e} "
        "[solar_mass AU/year]."
    )


if __name__ == "__main__":
    main()

