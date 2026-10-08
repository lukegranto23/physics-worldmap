#!/usr/bin/env python3
"""Normal modes of a one-dimensional fixed-end mass-spring chain.

All N masses are identical (m = 1 kg), all springs have k = 25 N/m, and the
end springs connect to fixed walls.  Displacements are small, so Hooke's law is
linear.  Damping and driving are omitted.
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
    parser.add_argument("--masses", type=int, default=8)
    parser.add_argument("--duration", type=float, default=8.0, help="seconds")
    parser.add_argument("--quick", action="store_true")
    parser.add_argument("--out-dir", type=Path, default=Path("results/normal_modes"))
    args = parser.parse_args()
    if args.quick:
        args.duration = 3.0
    if args.masses < 2 or args.duration <= 0:
        raise ValueError("require at least two masses and positive duration")

    n, mass, spring = args.masses, 1.0, 25.0
    stiffness = spring * (
        2 * np.eye(n) - np.eye(n, k=1) - np.eye(n, k=-1)
    )
    eigenvalue, modes = np.linalg.eigh(stiffness / mass)
    omega = np.sqrt(eigenvalue)
    mode_number = np.arange(1, n + 1)
    omega_exact = 2 * np.sqrt(spring / mass) * np.sin(
        mode_number * np.pi / (2 * (n + 1))
    )
    frequency_error = np.max(np.abs(omega - omega_exact) / omega_exact)
    orthogonality_error = np.max(np.abs(modes.T @ modes - np.eye(n)))

    # Pull the leftmost mass aside by 5 cm and release it.
    displacement0 = np.zeros(n)
    displacement0[0] = 0.05
    velocity0 = np.zeros(n)
    q0 = modes.T @ displacement0
    qdot0 = modes.T @ velocity0
    time = np.linspace(0.0, args.duration, 1200 if not args.quick else 350)
    q = q0[:, None] * np.cos(omega[:, None] * time)
    q += qdot0[:, None] / omega[:, None] * np.sin(omega[:, None] * time)
    qdot = -q0[:, None] * omega[:, None] * np.sin(omega[:, None] * time)
    qdot += qdot0[:, None] * np.cos(omega[:, None] * time)
    displacement = modes @ q
    velocity = modes @ qdot
    energy = 0.5 * mass * np.sum(velocity**2, axis=0)
    energy += 0.5 * np.einsum("it,ij,jt->t", displacement, stiffness, displacement)
    energy_span = np.ptp(energy) / np.mean(energy)

    if frequency_error > 2e-13 or orthogonality_error > 2e-13 or energy_span > 2e-12:
        raise AssertionError(
            f"mode validation failed: freq={frequency_error:.2e}, "
            f"orth={orthogonality_error:.2e}, energy={energy_span:.2e}"
        )

    args.out_dir.mkdir(parents=True, exist_ok=True)
    np.savez(
        args.out_dir / "normal_modes.npz",
        time_s=time,
        displacement_m=displacement,
        velocity_m_s=velocity,
        omega_rad_s=omega,
        eigenvectors=modes,
        energy_joule=energy,
    )
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.5))
    sites = np.arange(1, n + 1)
    for j in range(min(4, n)):
        shape = modes[:, j]
        if shape[np.argmax(np.abs(shape))] < 0:
            shape = -shape
        axes[0].plot(sites, shape, marker="o", label=f"mode {j+1}: {omega[j]:.2f} rad/s")
    axes[0].set(xlabel="mass index", ylabel="normalized displacement", title="Lowest normal modes")
    axes[0].legend(fontsize=8)
    axes[0].grid(alpha=0.25)
    image = axes[1].imshow(
        displacement,
        origin="lower",
        aspect="auto",
        extent=[time[0], time[-1], 1, n],
        cmap="RdBu_r",
    )
    axes[1].set(xlabel="time [s]", ylabel="mass index", title="Motion after local displacement")
    fig.colorbar(image, ax=axes[1], label="displacement [m]")
    fig.tight_layout()
    fig.savefig(args.out_dir / "coupled_oscillators.png", dpi=180)
    plt.close(fig)
    print(
        "PASS normal modes: "
        f"max frequency error={frequency_error:.2e}, "
        f"orthogonality error={orthogonality_error:.2e}, "
        f"energy span={energy_span:.2e}."
    )


if __name__ == "__main__":
    main()

