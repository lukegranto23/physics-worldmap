#!/usr/bin/env python3
"""Solve the two-dimensional electrostatic Laplace equation by relaxation.

A 1 m by 1 m grounded conducting box contains two thin vertical electrodes at
+1 V and -1 V.  The space between is homogeneous vacuum with no free volume
charge, so nabla^2 V = 0 away from the fixed-potential conductors.  The model is
two-dimensional and ignores fringing in the suppressed third dimension.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def solve_laplace(n: int, tolerance: float, max_iterations: int):
    potential = np.zeros((n, n), dtype=float)
    fixed = np.zeros_like(potential, dtype=bool)
    fixed[[0, -1], :] = True
    fixed[:, [0, -1]] = True
    y0, y1 = int(0.25 * (n - 1)), int(0.75 * (n - 1))
    left, right = int(0.35 * (n - 1)), int(0.65 * (n - 1))
    fixed[y0 : y1 + 1, left] = True
    fixed[y0 : y1 + 1, right] = True
    potential[y0 : y1 + 1, left] = 1.0
    potential[y0 : y1 + 1, right] = -1.0

    for iteration in range(1, max_iterations + 1):
        updated = potential.copy()
        updated[1:-1, 1:-1] = 0.25 * (
            potential[2:, 1:-1]
            + potential[:-2, 1:-1]
            + potential[1:-1, 2:]
            + potential[1:-1, :-2]
        )
        updated[fixed] = potential[fixed]
        change = np.max(np.abs(updated - potential))
        potential = updated
        if change < tolerance:
            break
    else:
        raise RuntimeError(f"Jacobi relaxation did not converge in {max_iterations} iterations")
    return potential, fixed, iteration, change


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--grid", type=int, default=101, help="points along each direction")
    parser.add_argument("--tolerance", type=float, default=2e-6, help="maximum update [V]")
    parser.add_argument("--quick", action="store_true")
    parser.add_argument("--out-dir", type=Path, default=Path("results/laplace"))
    args = parser.parse_args()
    if args.quick:
        args.grid, args.tolerance = 61, 1e-5
    if args.grid < 31 or args.tolerance <= 0:
        raise ValueError("grid must be at least 31 and tolerance positive")

    potential, fixed, iterations, final_change = solve_laplace(
        args.grid, args.tolerance, 100_000
    )
    spacing = 1.0 / (args.grid - 1)
    stencil_residual = (
        potential[2:, 1:-1]
        + potential[:-2, 1:-1]
        + potential[1:-1, 2:]
        + potential[1:-1, :-2]
        - 4 * potential[1:-1, 1:-1]
    )
    free_interior = ~fixed[1:-1, 1:-1]
    max_stencil_residual = np.max(np.abs(stencil_residual[free_interior]))
    symmetry_error = np.max(np.abs(potential + np.fliplr(potential)))
    fixed_error = max(
        np.max(np.abs(potential[fixed & (potential > 0)] - 1.0), initial=0.0),
        np.max(np.abs(potential[fixed & (potential < 0)] + 1.0), initial=0.0),
    )
    if max_stencil_residual > 4.1 * args.tolerance:
        raise AssertionError(f"Laplace stencil residual too large: {max_stencil_residual:.3e}")
    if symmetry_error > 3e-13 or fixed_error > 1e-14:
        raise AssertionError(
            f"boundary/symmetry failure: symmetry={symmetry_error:.2e}, fixed={fixed_error:.2e}"
        )

    edge_order = 2 if args.grid >= 3 else 1
    d_v_dy, d_v_dx = np.gradient(potential, spacing, spacing, edge_order=edge_order)
    electric_x, electric_y = -d_v_dx, -d_v_dy
    coordinate = np.linspace(0.0, 1.0, args.grid)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    np.savez(
        args.out_dir / "laplace_solution.npz",
        x_m=coordinate,
        y_m=coordinate,
        potential_v=potential,
        electric_x_v_m=electric_x,
        electric_y_v_m=electric_y,
        fixed_mask=fixed,
    )

    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.8), constrained_layout=True)
    levels = np.linspace(-1, 1, 31)
    contour = axes[0].contourf(coordinate, coordinate, potential, levels=levels, cmap="coolwarm")
    axes[0].contour(coordinate, coordinate, potential, levels=11, colors="k", linewidths=0.35)
    axes[0].set(xlabel="x [m]", ylabel="y [m]", title="Potential V(x,y) [V]", aspect="equal")
    fig.colorbar(contour, ax=axes[0], label="V [volt]")
    magnitude = np.hypot(electric_x, electric_y)
    axes[1].streamplot(
        coordinate,
        coordinate,
        electric_x,
        electric_y,
        color=np.log10(magnitude + 1e-6),
        cmap="viridis",
        density=1.1,
        linewidth=0.8,
    )
    axes[1].set(xlabel="x [m]", ylabel="y [m]", title="Electric-field lines", aspect="equal")
    axes[1].plot([], [], alpha=0, label=f"grid spacing = {spacing:.3g} m")
    axes[1].legend(loc="lower right", fontsize=8)
    fig.savefig(args.out_dir / "laplace_electrostatics.png", dpi=180)
    plt.close(fig)
    print(
        "PASS Laplace: "
        f"{iterations} iterations, final update={final_change:.2e} V, "
        f"max stencil residual={max_stencil_residual:.2e} V, "
        f"antisymmetry error={symmetry_error:.2e} V."
    )


if __name__ == "__main__":
    main()
