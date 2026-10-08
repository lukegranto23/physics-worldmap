#!/usr/bin/env python3
"""
Computational Lab 16 — Exploratory geometry of finite-system thermalization.

This program plots subsystem entropy, purity, successive Bures-angle steps,
and trace distance for one selected pair with the same environment preparation.
It is a diagnostic for a fixed finite SYK bipartition, NOT an evaporating
black-hole model. No Page-time, memory-onset, or bulk-geometry equivalence has
been established by Sessions 002–004.

The Bures/SLD metric is one of infinitely many monotone quantum metrics.
With squared Uhlmann fidelity, ds_B^2 = F_Q dt^2 / 4; the angle and chord
distance have the same infinitesimal metric but differ at finite separation.
Bounded endpoint distance does not imply cumulative path-length saturation.

Entropy-peak, half-speed, and cumulative-fraction times are descriptive,
window-dependent statistics, not hypothesis tests. Positive trace-distance
derivative for this pair is a lower-bound witness under the declared map,
not the optimized BLP measure; one trajectory alone would not define it.
Legacy stored result names have been replaced to prevent misinterpretation.
Dependencies: numpy, matplotlib.
"""

import argparse
import os
import time
import numpy as np

# Import building blocks from SYK lab
import sys

# ---------------------------------------------------------------------------
# Majorana and SYK (copied minimal set from lab 14)
# ---------------------------------------------------------------------------

def build_majorana_operators(N):
    assert N % 2 == 0
    n_modes = N // 2
    sigma_x = np.array([[0, 1], [1, 0]], dtype=np.float64)
    sigma_y = np.array([[0, -1j], [1j, 0]], dtype=np.complex128)
    sigma_z = np.array([[1, 0], [0, -1]], dtype=np.float64)
    eye2 = np.eye(2, dtype=np.float64)
    majoranas = []
    for k in range(n_modes):
        op_x = np.array([[1.0]], dtype=np.complex128)
        for j in range(n_modes):
            if j < k:
                op_x = np.kron(op_x, sigma_z)
            elif j == k:
                op_x = np.kron(op_x, sigma_x)
            else:
                op_x = np.kron(op_x, eye2)
        majoranas.append(op_x / np.sqrt(2))
        op_y = np.array([[1.0]], dtype=np.complex128)
        for j in range(n_modes):
            if j < k:
                op_y = np.kron(op_y, sigma_z)
            elif j == k:
                op_y = np.kron(op_y, sigma_y)
            else:
                op_y = np.kron(op_y, eye2)
        majoranas.append(op_y / np.sqrt(2))
    return majoranas

def generate_syk_couplings(N, J=1.0, rng=None):
    if rng is None:
        rng = np.random.default_rng()
    variance = J**2 * 6.0 / N**3
    std = np.sqrt(variance)
    couplings = {}
    for i in range(N):
        for j in range(i+1, N):
            for k in range(j+1, N):
                for l in range(k+1, N):
                    couplings[(i, j, k, l)] = rng.normal(0, std)
    return couplings

def build_syk_hamiltonian(chi_ops, couplings, N):
    d = chi_ops[0].shape[0]
    H = np.zeros((d, d), dtype=np.complex128)
    for (i, j, k, l), J_val in couplings.items():
        H += J_val * (chi_ops[i] @ chi_ops[j] @ chi_ops[k] @ chi_ops[l])
    H = 0.5 * (H + H.conj().T)
    return H

def entanglement_entropy(psi, d_A, d_B):
    psi_matrix = psi.reshape(d_A, d_B)
    s = np.linalg.svd(psi_matrix, compute_uv=False)
    s = s[s > 1e-15]
    s2 = s**2
    return -np.sum(s2 * np.log(s2))

def reduced_density_matrix(psi, d_A, d_B):
    psi_matrix = psi.reshape(d_A, d_B)
    return psi_matrix @ psi_matrix.conj().T


# ---------------------------------------------------------------------------
# Bures geometry
# ---------------------------------------------------------------------------

def matrix_sqrt(A):
    """Compute the matrix square root of a positive semidefinite Hermitian matrix."""
    eigenvalues, eigenvectors = np.linalg.eigh(A)
    eigenvalues = np.maximum(eigenvalues, 0)  # Clamp numerical negatives
    return eigenvectors @ np.diag(np.sqrt(eigenvalues)) @ eigenvectors.conj().T

def fidelity(rho, sigma):
    """
    Compute the Uhlmann fidelity F(rho, sigma) = (Tr sqrt(sqrt(rho) sigma sqrt(rho)))^2.

    Uses the equivalent formula: F = (sum sqrt(lambda_i))^2
    where lambda_i are eigenvalues of sqrt(rho) sigma sqrt(rho).
    """
    sqrt_rho = matrix_sqrt(rho)
    M = sqrt_rho @ sigma @ sqrt_rho
    eigenvalues = np.linalg.eigvalsh(M)
    eigenvalues = np.maximum(eigenvalues, 0)
    return (np.sum(np.sqrt(eigenvalues)))**2

def bures_distance(rho, sigma):
    """
    Bures distance: D_B(rho, sigma) = sqrt(2(1 - sqrt(F(rho, sigma)))).

    This is a proper metric on the space of density matrices.
    """
    F = fidelity(rho, sigma)
    F = min(F, 1.0)  # Clamp numerical overshoots
    return np.sqrt(2.0 * (1.0 - np.sqrt(F)))

def bures_angle(rho, sigma):
    """
    Bures angle (quantum angle): theta = arccos(sqrt(F)).

    This is the geodesic distance on the Bures manifold.
    """
    F = fidelity(rho, sigma)
    F = np.clip(F, 0.0, 1.0)
    return np.arccos(np.sqrt(F))

def quantum_fisher_speed(rho_t, rho_tdt, dt):
    """
    Compute the instantaneous quantum Fisher information "speed" of the
    trajectory rho(t) at time t.

    ds/dt ≈ bures_angle(rho(t), rho(t+dt)) / dt

    This is the quantum analogue of the Fisher information metric applied
    to the time direction.
    """
    return bures_angle(rho_t, rho_tdt) / dt


# ---------------------------------------------------------------------------
# Trace distance (for BLP comparison)
# ---------------------------------------------------------------------------

def trace_distance(rho, sigma):
    diff = rho - sigma
    eigenvalues = np.linalg.eigvalsh(diff)
    return 0.5 * np.sum(np.abs(eigenvalues))


# ---------------------------------------------------------------------------
# Main computation
# ---------------------------------------------------------------------------

def run_geometry_analysis(N, t_max, n_t, rng, verbose=True):
    """
    Run a single SYK realization and compute the full thermalization geometry:
    - Subsystem entropy curve S_A(t)
    - Bures speed ds/dt along rho_A(t)
    - Cumulative Bures distance s(t)
    - Selected-pair trace distance D(t) between two initial states
    - Selected-pair trace-distance derivative (information backflow rate)
    """
    chi_ops = build_majorana_operators(N)
    couplings = generate_syk_couplings(N, J=1.0, rng=rng)
    H = build_syk_hamiltonian(chi_ops, couplings, N)
    H = 0.5 * (H + H.conj().T)

    eigenvalues, eigenvectors = np.linalg.eigh(H)

    n_modes_A = N // 4
    n_modes_B = N // 2 - n_modes_A
    d_A = 2 ** n_modes_A
    d_B = 2 ** n_modes_B
    d = d_A * d_B

    t_array = np.linspace(0, t_max, n_t)
    dt = t_array[1] - t_array[0]

    # Initial product state
    psi_A = np.zeros(d_A, dtype=np.complex128)
    psi_A[0] = 1.0
    psi_B = np.zeros(d_B, dtype=np.complex128)
    psi_B[0] = 1.0
    psi0 = np.kron(psi_A, psi_B)

    # Second system state; same environment preparation
    psi_A_2 = np.zeros(d_A, dtype=np.complex128)
    psi_A_2[1 % d_A] = 1.0
    psi0_2 = np.kron(psi_A_2, psi_B)

    coeffs = eigenvectors.conj().T @ psi0
    coeffs_2 = eigenvectors.conj().T @ psi0_2

    # Arrays
    S_array = np.zeros(n_t)
    bures_speed = np.zeros(n_t)
    bures_dist_cumul = np.zeros(n_t)
    D_array = np.zeros(n_t)  # Selected-pair trace distance
    purity_array = np.zeros(n_t)
    von_neumann_rate = np.zeros(n_t)

    # Compute at each time step
    rho_A_prev = None
    for idx, t in enumerate(t_array):
        if verbose and idx % (n_t // 10) == 0:
            print(f"  t = {t:.2f} ({idx}/{n_t})", flush=True)

        phases = np.exp(-1j * eigenvalues * t)

        # State 1
        psi_t = eigenvectors @ (coeffs * phases)
        rho_A = reduced_density_matrix(psi_t, d_A, d_B)

        # Entropy
        S_array[idx] = entanglement_entropy(psi_t, d_A, d_B)

        # Purity
        purity_array[idx] = np.real(np.trace(rho_A @ rho_A))

        # Bures geometry
        if rho_A_prev is not None:
            angle = bures_angle(rho_A_prev, rho_A)
            bures_speed[idx] = angle / dt
            bures_dist_cumul[idx] = bures_dist_cumul[idx-1] + angle

        # Selected-pair trace distance
        psi_t_2 = eigenvectors @ (coeffs_2 * phases)
        rho_A_2 = reduced_density_matrix(psi_t_2, d_A, d_B)
        D_array[idx] = trace_distance(rho_A, rho_A_2)

        rho_A_prev = rho_A.copy()

    assert np.all(np.isfinite(S_array)) and np.all(np.isfinite(bures_speed))
    assert np.min(S_array) >= -1e-10 and np.max(S_array) <= np.log(d_A) + 1e-9
    assert np.min(purity_array) >= 1 / d_A - 1e-9 and np.max(purity_array) <= 1 + 1e-9
    assert np.min(D_array) >= -1e-10 and np.max(D_array) <= 1 + 1e-9

    # Von Neumann entropy rate
    von_neumann_rate = np.gradient(S_array, dt)

    # Selected-pair trace-distance derivative
    sigma_array = np.gradient(D_array, dt)

    # Entropy-peak time
    window = max(3, n_t // 50)
    S_smooth = np.convolve(S_array, np.ones(window)/window, mode='same')
    idx_entropy_peak = np.argmax(S_smooth[window:-window]) + window
    t_entropy_peak = t_array[idx_entropy_peak]

    # Window-dependent 50% cumulative backflow time
    backflow = np.maximum(sigma_array, 0.0)
    cumulative = np.cumsum(backflow) * dt
    total = cumulative[-1]
    t_backflow50 = t_array[-1]
    if total > 1e-15:
        for i in range(len(t_array)):
            if cumulative[i] >= 0.5 * total:
                t_backflow50 = t_array[i]
                break

    # Exploratory half-speed time: find where speed drops to 50% of initial
    speed_smooth = np.convolve(bures_speed, np.ones(window)/window, mode='same')
    initial_speed = np.mean(speed_smooth[window:2*window])
    t_bures_half = t_array[-1]
    if initial_speed > 1e-10:
        for i in range(window, len(t_array)):
            if speed_smooth[i] < 0.5 * initial_speed:
                t_bures_half = t_array[i]
                break

    # Window-dependent cumulative path fraction: where cumulative distance reaches 80% of total
    total_bures = bures_dist_cumul[-1]
    t_path80 = t_array[-1]
    if total_bures > 1e-10:
        for i in range(len(t_array)):
            if bures_dist_cumul[i] >= 0.8 * total_bures:
                t_path80 = t_array[i]
                break

    if verbose:
        print(f"\n  RESULTS:")
        print(f"    Entropy-peak time t_E = {t_entropy_peak:.3f}")
        print(f"    50% window backflow t_F = {t_backflow50:.3f}")
        print(f"    Bures speed half-life t_B = {t_bures_half:.3f}")
        print(f"    80% window path time = {t_path80:.3f}")
        print(f"    t_F / t_E = {t_backflow50 / t_entropy_peak:.3f}" if t_entropy_peak > 0 else "")
        print(f"    t_B / t_E = {t_bures_half / t_entropy_peak:.3f}" if t_entropy_peak > 0 else "")

    return {
        't_array': t_array,
        'S_array': S_array,
        'bures_speed': bures_speed,
        'bures_dist_cumul': bures_dist_cumul,
        'D_array': D_array,
        'sigma_array': sigma_array,
        'purity_array': purity_array,
        'von_neumann_rate': von_neumann_rate,
        't_entropy_peak': t_entropy_peak,
        't_backflow50': t_backflow50,
        't_bures_half': t_bures_half,
        't_path80': t_path80,
        'eigenvalues': eigenvalues,
        'N': N,
        'd_A': d_A,
        'd_B': d_B,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Bures Geometry of SYK Thermalization")
    parser.add_argument("--N", type=int, default=12,
                        help="Number of Majorana fermions (default: 12)")
    parser.add_argument("--n-disorder", type=int, default=5,
                        help="Number of disorder realizations (default: 5)")
    parser.add_argument("--t-max", type=float, default=30.0,
                        help="Maximum time (default: 30.0)")
    parser.add_argument("--n-t", type=int, default=300,
                        help="Number of time points (default: 300)")
    parser.add_argument("--seed", type=int, default=2026,
                        help="Random seed (default: 2026)")
    parser.add_argument("--out-dir", type=str, default="results/bures_geometry",
                        help="Output directory")
    parser.add_argument("--quick", action="store_true")
    args = parser.parse_args()

    if args.quick:
        args.N = 10
        args.n_disorder = 2
        args.n_t = 150
        args.t_max = 15.0

    if args.N < 4 or args.N % 2 or args.n_t < 20 or args.t_max <= 0 or args.n_disorder < 1:
        parser.error("require even N >= 4, n-t >= 20, positive t-max and n-disorder")
    pure0 = np.diag([1.0, 0.0])
    pure1 = np.diag([0.0, 1.0])
    assert abs(bures_distance(pure0, pure0)) < 1e-7
    assert np.isclose(bures_distance(pure0, pure1), np.sqrt(2.0))
    assert np.isclose(bures_angle(pure0, pure1), np.pi / 2)
    print("PASS basic fidelity/Bures identities (not a research hypothesis test)")
    print("=" * 70)
    print("Bures Geometry of SYK Thermalization")
    print("=" * 70)
    print(f"  N = {args.N}, d = {2**(args.N//2)}")
    print(f"  d_A = {2**(args.N//4)}, d_B = {2**(args.N//2 - args.N//4)}")
    print(f"  t_max = {args.t_max}, n_t = {args.n_t}")
    print(f"  Disorder realizations = {args.n_disorder}")
    print()

    rng = np.random.default_rng(args.seed)

    results = []
    t_entropy_peaks = []
    t_backflow50s = []
    t_bures_halves = []
    t_path80s = []

    for r in range(args.n_disorder):
        print(f"Realization {r+1}/{args.n_disorder}:")
        t0 = time.time()
        result = run_geometry_analysis(args.N, args.t_max, args.n_t, rng)
        elapsed = time.time() - t0
        print(f"  Elapsed: {elapsed:.1f} s\n")
        results.append(result)
        t_entropy_peaks.append(result['t_entropy_peak'])
        t_backflow50s.append(result['t_backflow50'])
        t_bures_halves.append(result['t_bures_half'])
        t_path80s.append(result['t_path80'])

    t_entropy_peaks = np.array(t_entropy_peaks)
    t_backflow50s = np.array(t_backflow50s)
    t_bures_halves = np.array(t_bures_halves)
    t_path80s = np.array(t_path80s)

    # Summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"  Entropy-peak time t_E:          {np.mean(t_entropy_peaks):.3f} +/- {np.std(t_entropy_peaks):.3f}")
    print(f"  50% window backflow t_F:   {np.mean(t_backflow50s):.3f} +/- {np.std(t_backflow50s):.3f}")
    print(f"  Bures half-speed t_B:   {np.mean(t_bures_halves):.3f} +/- {np.std(t_bures_halves):.3f}")
    print(f"  80% window path time:   {np.mean(t_path80s):.3f} +/- {np.std(t_path80s):.3f}")

    ratio_dom = t_backflow50s / np.where(t_entropy_peaks > 0, t_entropy_peaks, 1)
    ratio_bures = t_bures_halves / np.where(t_entropy_peaks > 0, t_entropy_peaks, 1)
    ratio_sat = t_path80s / np.where(t_entropy_peaks > 0, t_entropy_peaks, 1)

    print()
    print(f"  t_F / t_E:  {np.mean(ratio_dom):.3f} +/- {np.std(ratio_dom):.3f}")
    print(f"  t_B / t_E:  {np.mean(ratio_bures):.3f} +/- {np.std(ratio_bures):.3f}")
    print(f"  t_sat / t_E: {np.mean(ratio_sat):.3f} +/- {np.std(ratio_sat):.3f}")

    print()
    print("EXPLORATORY DIAGNOSTICS ONLY:")
    print("  These window-dependent ratios are not hypothesis-validation tests.")
    print("  No Page-time, memory-onset, or gravitational equivalence follows.")

    # Save
    os.makedirs(args.out_dir, exist_ok=True)
    np.savez(os.path.join(args.out_dir, "bures_geometry_results.npz"),
             N=args.N,
             t_entropy_peaks=t_entropy_peaks,
             t_backflow50s=t_backflow50s,
             t_bures_halves=t_bures_halves,
             t_path80s=t_path80s,
             t_array=results[0]['t_array'],
             # Last realization for plotting
             S_array=results[-1]['S_array'],
             bures_speed=results[-1]['bures_speed'],
             bures_dist_cumul=results[-1]['bures_dist_cumul'],
             D_array=results[-1]['D_array'],
             sigma_array=results[-1]['sigma_array'],
             purity_array=results[-1]['purity_array'],
             von_neumann_rate=results[-1]['von_neumann_rate'])

    # Plot
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(2, 3, figsize=(18, 10))
        fig.suptitle(f"Bures Geometry of SYK Thermalization (N={args.N})", fontsize=14)

        r = results[-1]
        t = r['t_array']
        t_E = r['t_entropy_peak']
        t_F = r['t_backflow50']
        t_B = r['t_bures_half']

        # Panel 1: Subsystem entropy curve
        ax = axes[0, 0]
        for res in results:
            ax.plot(res['t_array'], res['S_array'], alpha=0.3, color='steelblue')
        ax.axvline(t_E, color='red', linestyle='--', alpha=0.7, label=f'$t_E = {t_E:.1f}$')
        ax.set_xlabel('Time')
        ax.set_ylabel(r'$S_A(t)$')
        ax.set_title('Entanglement Entropy (Fixed Bipartition)')
        ax.legend(fontsize=8)
        ax.grid(alpha=0.2)

        # Panel 2: Bures speed
        ax = axes[0, 1]
        window = max(3, len(t) // 50)
        speed_smooth = np.convolve(r['bures_speed'], np.ones(window)/window, mode='same')
        for res in results:
            ss = np.convolve(res['bures_speed'], np.ones(window)/window, mode='same')
            ax.plot(res['t_array'], ss, alpha=0.3, color='purple')
        ax.axvline(t_E, color='red', linestyle='--', alpha=0.7, label=f'$t_E$')
        ax.axvline(t_B, color='green', linestyle=':', alpha=0.7, label=f'$t_B = {t_B:.1f}$')
        ax.set_xlabel('Time')
        ax.set_ylabel(r'$ds/dt$ (Bures speed)')
        ax.set_title('Quantum Fisher Speed')
        ax.legend(fontsize=8)
        ax.grid(alpha=0.2)

        # Panel 3: Cumulative Bures distance
        ax = axes[0, 2]
        for res in results:
            ax.plot(res['t_array'], res['bures_dist_cumul'], alpha=0.3, color='teal')
        ax.axvline(t_E, color='red', linestyle='--', alpha=0.7)
        ax.set_xlabel('Time')
        ax.set_ylabel(r'$s(t) = \int_0^t ds/dt\, dt$')
        ax.set_title('Cumulative Bures Path Length')
        ax.grid(alpha=0.2)

        # Panel 4: Selected-pair trace distance
        ax = axes[1, 0]
        ax.plot(t, r['D_array'], color='teal')
        ax.axvline(t_E, color='red', linestyle='--', alpha=0.5)
        ax.axvline(t_F, color='blue', linestyle=':', label=f'$t_F = {t_F:.1f}$')
        ax.set_xlabel('Time')
        ax.set_ylabel(r'$D(\rho_A, \rho_A^\prime)$')
        ax.set_title('Selected-pair trace distance')
        ax.legend(fontsize=8)
        ax.grid(alpha=0.2)

        # Panel 5: Entropy rate vs Bures speed
        ax = axes[1, 1]
        ax2 = ax.twinx()
        vn_rate_smooth = np.convolve(r['von_neumann_rate'], np.ones(window)/window, mode='same')
        ax.plot(t, vn_rate_smooth, color='steelblue', label='$dS/dt$')
        ax2.plot(t, speed_smooth, color='purple', alpha=0.7, label='$ds_{Bures}/dt$')
        ax.axvline(t_E, color='red', linestyle='--', alpha=0.5)
        ax.set_xlabel('Time')
        ax.set_ylabel(r'$dS/dt$', color='steelblue')
        ax2.set_ylabel(r'$ds/dt$ (Bures)', color='purple')
        ax.set_title('Entropy Rate vs Bures Speed')
        ax.grid(alpha=0.2)

        # Panel 6: Purity
        ax = axes[1, 2]
        for res in results:
            ax.plot(res['t_array'], res['purity_array'], alpha=0.3, color='coral')
        ax.axhline(1.0/2**(args.N//4), color='gray', linestyle=':',
                    label=f'max mixed ($1/d_A$)')
        ax.axvline(t_E, color='red', linestyle='--', alpha=0.5)
        ax.set_xlabel('Time')
        ax.set_ylabel(r'$\mathrm{Tr}(\rho_A^2)$')
        ax.set_title('Subsystem Purity')
        ax.legend(fontsize=8)
        ax.grid(alpha=0.2)

        plt.tight_layout()
        fig_path = os.path.join(args.out_dir, "bures_geometry_analysis.png")
        plt.savefig(fig_path, dpi=150)
        print(f"\nFigure saved: {fig_path}")

    except ImportError:
        print("\nmatplotlib not available; skipping figures.")

    print(f"\nDone. Results saved to: {args.out_dir}")


if __name__ == "__main__":
    main()
