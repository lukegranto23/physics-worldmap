#!/usr/bin/env python3
"""Background expansion of a homogeneous Friedmann-Lemaitre universe.

The model contains radiation, pressureless matter, and a cosmological constant,
with negligible curvature.  Parameters are illustrative Planck-era-like values:
H0 = 70 km/s/Mpc, Omega_r=9e-5, Omega_m=0.3, Omega_Lambda=0.69991.

The dimensionless expansion rate is
E(a)=H(a)/H0=sqrt(Omega_r/a^4 + Omega_m/a^3 + Omega_Lambda).
Cosmic time follows H0*t = integral da/[a E(a)].  This is a background model:
it does not evolve perturbations, structure formation, or recombination.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


H0 = 70.0  # km s^-1 Mpc^-1
OMEGA_R = 9.0e-5
OMEGA_M = 0.30000
OMEGA_L = 1.0 - OMEGA_R - OMEGA_M
MPC_IN_KM = 3.0856775814913673e19
SECONDS_PER_GYR = 365.25 * 86400.0 * 1e9
C_KM_S = 299_792.458


def expansion_rate(scale_factor: np.ndarray) -> np.ndarray:
    return np.sqrt(
        OMEGA_R / scale_factor**4
        + OMEGA_M / scale_factor**3
        + OMEGA_L
    )


def cumulative_trapezoid(y: np.ndarray, x: np.ndarray) -> np.ndarray:
    result = np.zeros_like(x)
    result[1:] = np.cumsum(0.5 * (y[1:] + y[:-1]) * np.diff(x))
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--grid", type=int, default=40_000)
    parser.add_argument("--quick", action="store_true")
    parser.add_argument("--out-dir", type=Path, default=Path("results/friedmann"))
    args = parser.parse_args()
    if args.quick:
        args.grid = 8_000
    if args.grid < 2_000:
        raise ValueError("grid must be at least 2000 for accurate early-time quadrature")

    scale_factor = np.geomspace(1e-6, 2.0, args.grid)
    e_of_a = expansion_rate(scale_factor)
    dimensionless_time = cumulative_trapezoid(
        1.0 / (scale_factor * e_of_a), scale_factor
    )
    # Radiation-era integral from a=0 to the first grid point.
    dimensionless_time += scale_factor[0] ** 2 / (2 * np.sqrt(OMEGA_R))
    hubble_time_gyr = (MPC_IN_KM / H0) / SECONDS_PER_GYR
    cosmic_time_gyr = dimensionless_time * hubble_time_gyr
    age_gyr = np.interp(1.0, scale_factor, cosmic_time_gyr)

    radiation_fraction = (OMEGA_R / scale_factor**4) / e_of_a**2
    matter_fraction = (OMEGA_M / scale_factor**3) / e_of_a**2
    lambda_fraction = OMEGA_L / e_of_a**2
    closure_error = abs(OMEGA_R + OMEGA_M + OMEGA_L - 1.0)
    present_e_error = abs(float(expansion_rate(np.array([1.0]))[0]) - 1.0)
    monotonic = np.all(np.diff(cosmic_time_gyr) > 0)

    # Independent analytic age for a flat matter+Lambda model (radiation
    # omitted); radiation changes the answer only slightly at this precision.
    analytic_matter_lambda_age = (
        2
        / (3 * np.sqrt(OMEGA_L))
        * np.arcsinh(np.sqrt(OMEGA_L / OMEGA_M))
        * hubble_time_gyr
    )
    analytic_difference = abs(age_gyr - analytic_matter_lambda_age)
    if (
        closure_error > 1e-14
        or present_e_error > 1e-14
        or not monotonic
        or not 12.0 < age_gyr < 15.0
        or analytic_difference > 0.08
    ):
        raise AssertionError(
            "Friedmann validation failed: "
            f"closure={closure_error:.2e}, E1={present_e_error:.2e}, "
            f"age={age_gyr:.3f} Gyr, analytic difference={analytic_difference:.3f} Gyr"
        )

    redshift = np.linspace(0.001, 3.0, 1000)
    integration_redshift = np.concatenate(([0.0], redshift))
    e_of_z = np.sqrt(
        OMEGA_R * (1 + integration_redshift) ** 4
        + OMEGA_M * (1 + integration_redshift) ** 3
        + OMEGA_L
    )
    comoving_integral = cumulative_trapezoid(1.0 / e_of_z, integration_redshift)[1:]
    luminosity_distance_mpc = (1 + redshift) * C_KM_S / H0 * comoving_integral
    distance_modulus = 5 * np.log10(luminosity_distance_mpc) + 25

    args.out_dir.mkdir(parents=True, exist_ok=True)
    np.savez(
        args.out_dir / "friedmann_history.npz",
        scale_factor=scale_factor,
        cosmic_time_gyr=cosmic_time_gyr,
        hubble_over_h0=e_of_a,
        omega_radiation=radiation_fraction,
        omega_matter=matter_fraction,
        omega_lambda=lambda_fraction,
        redshift=redshift,
        luminosity_distance_mpc=luminosity_distance_mpc,
        distance_modulus=distance_modulus,
        H0_km_s_mpc=H0,
    )
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.5))
    axes[0].plot(cosmic_time_gyr, scale_factor)
    axes[0].scatter([age_gyr], [1.0], color="k", s=25, label=f"today: {age_gyr:.2f} Gyr")
    axes[0].set(
        xlabel="cosmic time [Gyr]",
        ylabel="scale factor a",
        title="Expansion history",
        xlim=(0, min(cosmic_time_gyr[-1], 25)),
        ylim=(0, 2),
    )
    axes[0].legend()
    axes[0].grid(alpha=0.25)
    axes[1].loglog(scale_factor, radiation_fraction, label="radiation")
    axes[1].loglog(scale_factor, matter_fraction, label="matter")
    axes[1].loglog(scale_factor, lambda_fraction, label="cosmological constant")
    axes[1].axvline(1.0, color="k", ls=":", lw=1)
    axes[1].set(
        xlabel="scale factor a",
        ylabel="fraction of critical density",
        title="Changing cosmic energy budget",
        xlim=(1e-6, 2),
        ylim=(1e-8, 1.2),
    )
    axes[1].legend()
    axes[1].grid(alpha=0.2, which="both")
    fig.tight_layout()
    fig.savefig(args.out_dir / "friedmann_cosmology.png", dpi=180)
    plt.close(fig)
    print(
        "PASS Friedmann: "
        f"Omega sum={OMEGA_R + OMEGA_M + OMEGA_L:.8f}, E(1)=1, "
        f"age={age_gyr:.3f} Gyr; matter+Lambda analytic comparison differs "
        f"by {analytic_difference:.3f} Gyr."
    )


if __name__ == "__main__":
    main()

