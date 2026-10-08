#!/usr/bin/env python3
"""Metropolis Monte Carlo for the two-dimensional ferromagnetic Ising model.

The dimensionless Hamiltonian is H/J = -sum_<ij> s_i s_j with s_i = +/-1,
periodic boundaries, zero magnetic field, and k_B = J = 1.  A checkerboard
Metropolis update is used on an even L by L square lattice.  Reported heat
capacity and susceptibility are per spin.

Near the critical temperature, T_c = 2/ln(1+sqrt(2)) ~= 2.269, samples are
autocorrelated.  This compact lab demonstrates the phase trend but is not a
precision finite-size-scaling calculation.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


TC_EXACT = 2.0 / np.log(1.0 + np.sqrt(2.0))


def energy_magnetization(spins: np.ndarray):
    neighbors = (
        np.roll(spins, 1, axis=0)
        + np.roll(spins, -1, axis=0)
        + np.roll(spins, 1, axis=1)
        + np.roll(spins, -1, axis=1)
    )
    n_spins = spins.size
    energy_per_spin = -0.5 * np.sum(spins * neighbors) / n_spins
    magnetization_per_spin = np.sum(spins) / n_spins
    return float(energy_per_spin), float(magnetization_per_spin)


def sweep(spins: np.ndarray, beta: float, parity: np.ndarray, rng: np.random.Generator):
    accepted = 0
    for sublattice in (0, 1):
        neighbors = (
            np.roll(spins, 1, axis=0)
            + np.roll(spins, -1, axis=0)
            + np.roll(spins, 1, axis=1)
            + np.roll(spins, -1, axis=1)
        )
        delta_energy = 2 * spins * neighbors
        trial = rng.random(spins.shape)
        flip = (parity == sublattice) & (
            (delta_energy <= 0) | (trial < np.exp(-beta * delta_energy))
        )
        accepted += int(np.count_nonzero(flip))
        spins[flip] *= -1
    return accepted / spins.size


def sample_temperature(
    spins: np.ndarray,
    temperature: float,
    parity: np.ndarray,
    rng: np.random.Generator,
    burn_sweeps: int,
    samples: int,
    stride: int,
):
    beta = 1.0 / temperature
    for _ in range(burn_sweeps):
        sweep(spins, beta, parity, rng)
    energies, magnetizations, acceptances = [], [], []
    for _ in range(samples):
        acceptance = 0.0
        for _ in range(stride):
            acceptance += sweep(spins, beta, parity, rng)
        energy, magnetization = energy_magnetization(spins)
        energies.append(energy)
        magnetizations.append(magnetization)
        acceptances.append(acceptance / stride)
    energy = np.asarray(energies)
    magnetization = np.asarray(magnetizations)
    n_spins = spins.size
    return {
        "energy": np.mean(energy),
        "abs_magnetization": np.mean(np.abs(magnetization)),
        "heat_capacity": beta**2 * n_spins * np.var(energy, ddof=1),
        "susceptibility": beta
        * n_spins
        * (np.mean(magnetization**2) - np.mean(np.abs(magnetization)) ** 2),
        "acceptance": np.mean(acceptances),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--size", type=int, default=28, help="even lattice side length")
    parser.add_argument("--seed", type=int, default=20260730)
    parser.add_argument("--quick", action="store_true")
    parser.add_argument("--out-dir", type=Path, default=Path("results/ising"))
    args = parser.parse_args()
    if args.quick:
        args.size = 16
        temperature_count, burn_sweeps, samples, stride = 10, 160, 260, 1
    else:
        temperature_count, burn_sweeps, samples, stride = 17, 600, 900, 2
    if args.size < 8 or args.size % 2:
        raise ValueError("checkerboard updates require an even lattice size >= 8")

    rng = np.random.default_rng(args.seed)
    spins = rng.choice(np.array([-1, 1], dtype=np.int8), size=(args.size, args.size))
    rows, columns = np.indices(spins.shape)
    parity = (rows + columns) % 2
    # Cool gradually from the disordered phase; each point still receives burn-in.
    descending_temperature = np.linspace(3.5, 1.5, temperature_count)
    records = []
    final_low_temperature_spins = None
    for temperature in descending_temperature:
        result = sample_temperature(
            spins, temperature, parity, rng, burn_sweeps, samples, stride
        )
        records.append(
            [
                temperature,
                result["energy"],
                result["abs_magnetization"],
                result["heat_capacity"],
                result["susceptibility"],
                result["acceptance"],
            ]
        )
        final_low_temperature_spins = spins.copy()
    data = np.asarray(records)[::-1]

    energy, magnetization, acceptance = data[:, 1], data[:, 2], data[:, 5]
    energy_in_bounds = np.all((-2.0 - 1e-12 <= energy) & (energy <= 2.0 + 1e-12))
    ordered_trend = magnetization[0] > magnetization[-1] + 0.35
    acceptance_valid = np.all((0.0 <= acceptance) & (acceptance <= 1.0))
    if not (energy_in_bounds and ordered_trend and acceptance_valid):
        raise AssertionError(
            "Ising validation failed: "
            f"energy_bounds={energy_in_bounds}, phase_trend={ordered_trend}, "
            f"acceptance={acceptance_valid}"
        )

    args.out_dir.mkdir(parents=True, exist_ok=True)
    header = (
        "temperature,energy_per_spin,abs_magnetization,"
        "heat_capacity_per_spin,susceptibility_per_spin,acceptance"
    )
    np.savetxt(args.out_dir / "ising_scan.csv", data, delimiter=",", header=header, comments="")
    np.save(args.out_dir / "low_temperature_spins.npy", final_low_temperature_spins)

    fig, axes = plt.subplots(2, 2, figsize=(10.5, 8), sharex=True)
    axes[0, 0].plot(data[:, 0], data[:, 1], "o-")
    axes[0, 0].set(ylabel="<E>/N", title="Energy")
    axes[0, 1].plot(data[:, 0], data[:, 2], "o-")
    axes[0, 1].set(ylabel="<|M|>/N", title="Order parameter")
    axes[1, 0].plot(data[:, 0], data[:, 3], "o-")
    axes[1, 0].set(xlabel="T [J/kB]", ylabel="C/N", title="Heat capacity")
    axes[1, 1].plot(data[:, 0], data[:, 4], "o-")
    axes[1, 1].set(xlabel="T [J/kB]", ylabel="chi/N", title="Susceptibility")
    for axis in axes.flat:
        axis.axvline(TC_EXACT, color="k", ls="--", lw=1, label=f"Tc={TC_EXACT:.3f}")
        axis.grid(alpha=0.2)
    axes[0, 0].legend(fontsize=8)
    fig.suptitle(f"2-D Ising Metropolis simulation ({args.size}x{args.size})")
    fig.tight_layout()
    fig.savefig(args.out_dir / "ising_monte_carlo.png", dpi=180)
    plt.close(fig)
    print(
        "PASS Ising: "
        f"|M|/N rises from {magnetization[-1]:.3f} at T={data[-1,0]:.2f} "
        f"to {magnetization[0]:.3f} at T={data[0,0]:.2f}; "
        f"energy and acceptance bounds hold (seed={args.seed})."
    )


if __name__ == "__main__":
    main()
