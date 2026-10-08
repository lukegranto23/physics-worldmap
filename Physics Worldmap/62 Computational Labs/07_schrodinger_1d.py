#!/usr/bin/env python3
"""Eigenstates and unitary time evolution in a 1-D infinite square well.

Dimensionless units set hbar = m = L = 1, so the well occupies 0 < x < 1 and
H = -(1/2)d^2/dx^2.  Dirichlet boundary conditions psi(0)=psi(1)=0 represent
infinite walls.  The Hamiltonian is diagonalized on an interior finite-
difference grid; evolution is then exact within that discrete eigenbasis.
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
    parser.add_argument("--grid", type=int, default=280, help="interior grid points")
    parser.add_argument("--quick", action="store_true")
    parser.add_argument("--out-dir", type=Path, default=Path("results/schrodinger"))
    args = parser.parse_args()
    if args.quick:
        args.grid = 100
    if args.grid < 40:
        raise ValueError("grid must contain at least 40 interior points")

    n = args.grid
    dx = 1.0 / (n + 1)
    x_interior = np.arange(1, n + 1) * dx
    hamiltonian = (
        np.diag(np.full(n, 1.0 / dx**2))
        + np.diag(np.full(n - 1, -0.5 / dx**2), 1)
        + np.diag(np.full(n - 1, -0.5 / dx**2), -1)
    )
    energy, eigenvectors = np.linalg.eigh(hamiltonian)
    quantum_number = np.arange(1, 5)
    exact_energy = 0.5 * (quantum_number * np.pi) ** 2
    energy_error = np.max(np.abs(energy[:4] / exact_energy - 1.0))

    x0, sigma, k0 = 0.30, 0.060, 30.0
    psi0 = np.exp(-0.5 * ((x_interior - x0) / sigma) ** 2) * np.exp(
        1j * k0 * x_interior
    )
    psi0 /= np.sqrt(np.sum(np.abs(psi0) ** 2) * dx)
    # q = psi*sqrt(dx) has ordinary Euclidean norm one.
    q0 = psi0 * np.sqrt(dx)
    coefficients = eigenvectors.T.conj() @ q0
    times = np.array([0.0, 0.04, 0.08, 0.12, 0.20])
    q_time = np.array(
        [eigenvectors @ (coefficients * np.exp(-1j * energy * time)) for time in times]
    )
    psi_time = q_time / np.sqrt(dx)
    norms = np.sum(np.abs(psi_time) ** 2, axis=1) * dx
    norm_error = np.max(np.abs(norms - 1.0))
    orthogonality_error = np.max(
        np.abs(eigenvectors[:, :8].T @ eigenvectors[:, :8] - np.eye(8))
    )
    if energy_error > 0.003 or norm_error > 2e-13 or orthogonality_error > 2e-13:
        raise AssertionError(
            f"quantum validation failed: E={energy_error:.2e}, "
            f"norm={norm_error:.2e}, orth={orthogonality_error:.2e}"
        )

    x = np.concatenate(([0.0], x_interior, [1.0]))
    eigenstates = np.zeros((4, n + 2))
    eigenstates[:, 1:-1] = (eigenvectors[:, :4] / np.sqrt(dx)).T
    wavefunctions = np.zeros((len(times), n + 2), dtype=complex)
    wavefunctions[:, 1:-1] = psi_time
    args.out_dir.mkdir(parents=True, exist_ok=True)
    np.savez(
        args.out_dir / "schrodinger_solution.npz",
        x_dimensionless=x,
        energy_dimensionless=energy,
        eigenstates=eigenstates,
        time_dimensionless=times,
        wavefunction=wavefunctions,
        hbar=1.0,
        mass=1.0,
        well_length=1.0,
    )

    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.5))
    for index in range(4):
        state = eigenstates[index]
        if state[np.argmax(np.abs(state))] < 0:
            state = -state
        axes[0].plot(x, state + energy[index], label=f"n={index+1}")
        axes[0].hlines(energy[index], 0, 1, color="0.75", lw=0.5)
    axes[0].set(
        xlabel="x / L",
        ylabel="energy + shifted eigenfunction",
        title="Infinite-well eigenstates",
    )
    axes[0].legend()
    for index, time in enumerate(times):
        axes[1].plot(x, np.abs(wavefunctions[index]) ** 2, label=f"t={time:.2f}")
    axes[1].set(
        xlabel="x / L",
        ylabel=r"$|\psi|^2$",
        title="Unitary wave-packet evolution",
    )
    axes[1].legend(fontsize=8)
    axes[1].grid(alpha=0.2)
    fig.tight_layout()
    fig.savefig(args.out_dir / "schrodinger_1d.png", dpi=180)
    plt.close(fig)
    print(
        "PASS Schrodinger: "
        f"first-four energy max relative error={energy_error:.2e}, "
        f"max norm error={norm_error:.2e}, orthogonality error={orthogonality_error:.2e}."
    )


if __name__ == "__main__":
    main()

