#!/usr/bin/env python3
"""
Computational Lab 14 — SYK Entanglement and Memory Diagnostics
==============================================================

Purpose
-------
Explore several finite-size, finite-window diagnostics of entanglement growth
and memory in an SYK Hamiltonian. This lab does not test black-hole evaporation:
the maximum of entropy for one fixed tensor-product bipartition is an
``entropy-peak time``, not a black-hole Page time.

The SYK (Sachdev-Ye-Kitaev) model contains N Majorana fermions with random
all-to-all q-body interactions. Certain large-N, low-energy limits have a
relation to nearly-AdS_2/JT gravity, but this small exact-diagonalization model
does not by itself reproduce an evaporating black hole.

Model
-----
The SYK Hamiltonian with q=4 is:

    H = sum_{i<j<k<l} J_{ijkl} chi_i chi_j chi_k chi_l

where chi_i are Majorana fermion operators satisfying {chi_i, chi_j} = delta_{ij},
and J_{ijkl} are i.i.d. Gaussian random couplings with variance J^2 * 3! / N^3.

Majorana fermions are represented as gamma matrices. For N Majoranas, the
Hilbert space dimension is 2^{N/2} (N must be even).

Protocol
--------
1. Construct the SYK Hamiltonian for N = 8, 10, 12, 14 Majorana fermions.
2. Diagonalize exactly to get eigenvalues and eigenvectors.
3. Compute the thermal density matrix rho(beta) = exp(-beta H) / Z.
4. Bipartition the system into "system" (first N/2 Majoranas) and "bath"
   (remaining N/2 Majoranas).
5. Compute the fixed-bipartition entanglement curve S_A(t) after time evolution
   from a product initial state.
6. Extract the Mori-Zwanzig memory kernel K(t) for the reduced dynamics.
7. Record window- and threshold-dependent memory summaries.
8. Compare those summaries descriptively with the entropy-peak time. Coincident
   times would be a prompt for stronger tests, not evidence of equivalence.

Validation
----------
- Majorana algebra: {chi_i, chi_j} = delta_{ij} checked numerically.
- Trace of H is zero (by antisymmetry of couplings).
- Entropy is bounded: 0 <= S_A <= (N/4) ln 2.
- The finite-size spectral histogram is descriptive only. SYK spectral density
  depends on q, N, normalization, symmetry sector, and energy regime; no
  universal semicircle-law validation is claimed here.

Units: J = 1 (coupling scale), hbar = 1.

Usage
-----
    python 14_syk_mori_zwanzig.py [--quick] [--N 12] [--n-disorder 10]
                                   [--out-dir results/syk_mz] [--seed 2026]

Dependencies: numpy, matplotlib (no scipy required for core computation).
"""

import argparse
import os
import sys
import time

import numpy as np

# ---------------------------------------------------------------------------
# Majorana fermion representation
# ---------------------------------------------------------------------------

def build_majorana_operators(N):
    """
    Build N Majorana operators as 2^{N/2} x 2^{N/2} matrices.

    Uses the Jordan-Wigner transformation. For N Majorana fermions,
    we need N/2 complex fermion modes, giving a Hilbert space of
    dimension d = 2^{N/2}.

    Convention: chi_{2k} = (c_k + c_k^dag), chi_{2k+1} = -i(c_k - c_k^dag)
    where c_k are complex fermion annihilation operators.

    All operators are real and satisfy {chi_i, chi_j} = delta_{ij} * I.
    (We use the convention with a factor of 1/2 absorbed.)
    """
    assert N % 2 == 0, "N must be even for Majorana fermions"
    n_modes = N // 2
    d = 2 ** n_modes

    # Pauli matrices
    sigma_x = np.array([[0, 1], [1, 0]], dtype=np.float64)
    sigma_y = np.array([[0, -1j], [1j, 0]], dtype=np.complex128)
    sigma_z = np.array([[1, 0], [0, -1]], dtype=np.float64)
    eye2 = np.eye(2, dtype=np.float64)

    majoranas = []

    for k in range(n_modes):
        # Jordan-Wigner string: sigma_z on sites 0..k-1
        # sigma_x or sigma_y on site k
        # identity on sites k+1..n_modes-1

        # chi_{2k} corresponds to sigma_x at site k
        op_x = np.array([[1.0]], dtype=np.complex128)
        for j in range(n_modes):
            if j < k:
                op_x = np.kron(op_x, sigma_z)
            elif j == k:
                op_x = np.kron(op_x, sigma_x)
            else:
                op_x = np.kron(op_x, eye2)
        majoranas.append(op_x / np.sqrt(2))

        # chi_{2k+1} corresponds to sigma_y at site k
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


def validate_majorana_algebra(chi_ops, tol=1e-10):
    """Check {chi_i, chi_j} = delta_{ij} * I."""
    N = len(chi_ops)
    d = chi_ops[0].shape[0]
    identity = np.eye(d)
    max_err = 0.0
    for i in range(N):
        for j in range(i, N):
            anticomm = chi_ops[i] @ chi_ops[j] + chi_ops[j] @ chi_ops[i]
            if i == j:
                expected = identity
            else:
                expected = np.zeros((d, d))
            err = np.max(np.abs(anticomm - expected))
            max_err = max(max_err, err)
    return max_err


# ---------------------------------------------------------------------------
# SYK Hamiltonian
# ---------------------------------------------------------------------------

def build_syk_hamiltonian(chi_ops, J_couplings, N):
    """
    Build the SYK_4 Hamiltonian.

    H = sum_{i<j<k<l} J_{ijkl} chi_i chi_j chi_k chi_l

    J_couplings is a dict mapping (i,j,k,l) -> coupling value.
    """
    d = chi_ops[0].shape[0]
    H = np.zeros((d, d), dtype=np.complex128)

    for (i, j, k, l), J_val in J_couplings.items():
        H += J_val * (chi_ops[i] @ chi_ops[j] @ chi_ops[k] @ chi_ops[l])

    # H should be Hermitian
    H = 0.5 * (H + H.conj().T)
    return H


def generate_syk_couplings(N, J=1.0, rng=None):
    """
    Generate random Gaussian couplings for SYK_4.

    Variance: <J_{ijkl}^2> = J^2 * 3! / N^3
    """
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


# ---------------------------------------------------------------------------
# Entanglement entropy
# ---------------------------------------------------------------------------

def entanglement_entropy(psi, d_A, d_B):
    """
    Compute the von Neumann entanglement entropy of subsystem A
    for a pure state psi in a d_A * d_B dimensional Hilbert space.

    Uses the Schmidt decomposition via SVD of the reshaped state vector.
    """
    psi_matrix = psi.reshape(d_A, d_B)
    s = np.linalg.svd(psi_matrix, compute_uv=False)
    s = s[s > 1e-15]  # Remove numerical zeros
    s2 = s**2
    return -np.sum(s2 * np.log(s2))


def random_state_mean_entropy(d_A, d_B):
    """
    Leading Page-formula benchmark for the average entanglement entropy of a
    Haar-random pure state in d_A x d_B dimensions (d_A <= d_B).

    S_Page ~ ln(d_A) - d_A / (2 * d_B)
    """
    if d_A > d_B:
        d_A, d_B = d_B, d_A
    return np.log(d_A) - d_A / (2.0 * d_B)


# ---------------------------------------------------------------------------
# Time evolution and fixed-bipartition entanglement curve
# ---------------------------------------------------------------------------

def compute_entanglement_curve(eigenvalues, eigenvectors, psi0, d_A, d_B, t_array):
    """
    Compute S_A(t) for a pure state evolved under H.

    psi(t) = sum_n <n|psi0> exp(-i E_n t) |n>

    Returns entropy at each time in t_array.
    """
    # Decompose initial state in energy eigenbasis
    coeffs = eigenvectors.conj().T @ psi0  # <n|psi0>

    S_array = np.zeros(len(t_array))
    for idx, t in enumerate(t_array):
        phases = np.exp(-1j * eigenvalues * t)
        psi_t = eigenvectors @ (coeffs * phases)
        S_array[idx] = entanglement_entropy(psi_t, d_A, d_B)

    return S_array


# ---------------------------------------------------------------------------
# Mori-Zwanzig memory kernel extraction
# ---------------------------------------------------------------------------

def compute_autocorrelation(eigenvalues, eigenvectors, A_op, beta, t_array):
    """
    Compute the thermal autocorrelation function:

    C(t) = <A(t) A(0)>_beta = Tr[rho_beta A(t) A(0)]

    where A(t) = e^{iHt} A e^{-iHt} and rho_beta = e^{-beta H} / Z.

    In the energy eigenbasis:
    C(t) = (1/Z) sum_{m,n} e^{-beta E_m} |A_{mn}|^2 e^{i(E_m - E_n)t}
    """
    d = len(eigenvalues)
    Z = np.sum(np.exp(-beta * eigenvalues))
    rho_diag = np.exp(-beta * eigenvalues) / Z

    # Matrix elements of A in energy eigenbasis
    A_eig = eigenvectors.conj().T @ A_op @ eigenvectors
    A_mn_sq = np.abs(A_eig)**2  # |<m|A|n>|^2

    C_array = np.zeros(len(t_array), dtype=np.complex128)
    for idx, t in enumerate(t_array):
        # Sum over m, n
        phase_matrix = np.exp(1j * np.subtract.outer(eigenvalues, eigenvalues) * t)
        C_array[idx] = np.sum(rho_diag[:, None] * A_mn_sq * phase_matrix)

    return C_array


def extract_memory_kernel(C_array, t_array):
    """
    Extract the Mori-Zwanzig memory kernel K(t) from the autocorrelation
    function C(t) using the generalized Langevin equation:

    dC/dt = -Omega^2 * integral_0^t K(t-s) C(s) ds + noise

    In the frequency domain:
    K(omega) = [Omega^2 - omega^2 * C_hat(omega)] / (omega * C_hat(omega))

    For simplicity, we use a time-domain deconvolution:
    K(t) is extracted iteratively from the Volterra equation.

    We discretize:
    C'(t_n) = -Omega^2 * dt * sum_{k=0}^{n} K(t_{n-k}) C(t_k)

    Solving for K(t_n) at each step (trapezoidal rule).
    """
    dt = t_array[1] - t_array[0]
    n_t = len(t_array)

    # Compute C'(t) numerically
    C_dot = np.gradient(np.real(C_array), dt)

    # Frequency matrix (static susceptibility)
    C0 = np.real(C_array[0])
    if abs(C0) < 1e-15:
        return np.zeros(n_t)

    # Omega^2 = -C''(0)/C(0) (initial curvature)
    if n_t > 2:
        C_ddot_0 = (np.real(C_array[2]) - 2*np.real(C_array[1]) + np.real(C_array[0])) / dt**2
        Omega_sq = -C_ddot_0 / C0
    else:
        Omega_sq = 1.0

    if Omega_sq <= 0:
        Omega_sq = abs(Omega_sq) + 1e-10

    # Solve Volterra equation iteratively
    K = np.zeros(n_t)

    for n in range(n_t):
        # C'(t_n) = -Omega^2 * dt * [0.5*K(0)*C(t_n) + sum_{k=1}^{n-1} K(t_k)*C(t_{n-k}) + 0.5*K(t_n)*C(0)]
        rhs = C_dot[n]
        conv_sum = 0.0
        for k in range(1, n):
            conv_sum += K[k] * np.real(C_array[n - k])

        # Trapezoidal: 0.5*dt*(K[0]*C[n] + K[n]*C[0]) + dt*conv_sum = -C_dot[n]/Omega^2
        # Solve for K[n]:
        denominator = 0.5 * dt * Omega_sq * C0
        if abs(denominator) < 1e-20:
            K[n] = 0.0
        else:
            numerator = -rhs - Omega_sq * dt * (0.5 * K[0] * np.real(C_array[n]) + conv_sum)
            K[n] = numerator / denominator

    return K


def memory_onset_time(K, t_array, threshold=0.1):
    """
    Find the time at which the memory kernel K(t) first exceeds
    a threshold fraction of its initial value (normalized).
    This is the old method, kept for comparison.
    """
    K_abs = np.abs(K)
    dt = t_array[1] - t_array[0]
    cumulative = np.cumsum(K_abs) * dt
    total = cumulative[-1]
    if total < 1e-15:
        return t_array[-1]
    tail_integral = total - cumulative
    for idx in range(1, len(t_array)):
        if tail_integral[idx] / total < (1.0 - threshold):
            return t_array[idx]
    return t_array[-1]


# ---------------------------------------------------------------------------
# Selected-pair trace-distance revival proxy
# ---------------------------------------------------------------------------

def reduced_density_matrix(psi, d_A, d_B):
    """Compute reduced density matrix of subsystem A from a pure state."""
    psi_matrix = psi.reshape(d_A, d_B)
    return psi_matrix @ psi_matrix.conj().T


def trace_distance(rho, sigma):
    """Compute trace distance D(rho, sigma) = 0.5 * Tr|rho - sigma|."""
    diff = rho - sigma
    eigenvalues = np.linalg.eigvalsh(diff)
    return 0.5 * np.sum(np.abs(eigenvalues))


def compute_selected_pair_trace_distance(
        eigenvalues, eigenvectors, d_A, d_B, t_array, rng):
    """
    Compute a BLP-inspired trace-distance curve for one selected state pair.

    Prepare two initial product states that differ only in subsystem A.
    Evolve both under the full Hamiltonian.
    Track the trace distance D(rho_A(t), rho_A'(t)) between the
    reduced density matrices.

    A trace-distance revival for this pair is a useful proxy for information
    backflow. It is not the optimized BLP measure, which requires maximizing
    over admissible initial-state pairs (and specifying a dynamical map).

    Returns:
    - D_array: trace distance at each time
    - sigma_array: dD/dt at each time (positive = selected-pair revival)
    - t_revival: first resolved increase after an initial decrease
    """
    d = d_A * d_B

    # Initial state 1: |0>_A |0>_B
    psi_A_1 = np.zeros(d_A, dtype=np.complex128)
    psi_A_1[0] = 1.0

    # Initial state 2: random pure state for A
    psi_A_2 = rng.standard_normal(d_A) + 1j * rng.standard_normal(d_A)
    psi_A_2 /= np.linalg.norm(psi_A_2)
    # Ensure it's not too close to state 1
    overlap = abs(np.vdot(psi_A_1, psi_A_2))
    if overlap > 0.95:
        psi_A_2 = np.zeros(d_A, dtype=np.complex128)
        psi_A_2[1] = 1.0

    # Same B state for both
    psi_B = np.zeros(d_B, dtype=np.complex128)
    psi_B[0] = 1.0

    psi0_1 = np.kron(psi_A_1, psi_B)
    psi0_2 = np.kron(psi_A_2, psi_B)

    # Decompose in energy eigenbasis
    coeffs_1 = eigenvectors.conj().T @ psi0_1
    coeffs_2 = eigenvectors.conj().T @ psi0_2

    D_array = np.zeros(len(t_array))
    for idx, t in enumerate(t_array):
        phases = np.exp(-1j * eigenvalues * t)
        psi_t_1 = eigenvectors @ (coeffs_1 * phases)
        psi_t_2 = eigenvectors @ (coeffs_2 * phases)

        rho_A_1 = reduced_density_matrix(psi_t_1, d_A, d_B)
        rho_A_2 = reduced_density_matrix(psi_t_2, d_A, d_B)

        D_array[idx] = trace_distance(rho_A_1, rho_A_2)

    # Compute derivative (positive = revival for this selected pair)
    dt = t_array[1] - t_array[0]
    sigma_array = np.gradient(D_array, dt)

    # Find the first selected-pair revival:
    # Look for the first time after an initial decrease where D increases
    # (i.e., first positive sigma after initial negative period)
    t_revival = t_array[-1]  # default: no revival detected in this window
    found_decrease = False
    for idx in range(1, len(t_array)):
        if sigma_array[idx] < -1e-8:
            found_decrease = True
        if found_decrease and sigma_array[idx] > 1e-8:
            t_revival = t_array[idx]
            break

    return D_array, sigma_array, t_revival


def selected_pair_backflow_quantile_time(
        sigma_array, t_array, quantile=0.5):
    """
    Return a quantile time for cumulative positive selected-pair slope.

    This is explicitly relative to the chosen [0, t_max] analysis window and
    selected initial-state pair. At quantile=0.5 it is merely the within-window
    median of accumulated positive slope; it is not a window-independent
    transition, a memory-onset time, or the optimized BLP measure.
    """
    dt = t_array[1] - t_array[0]
    backflow = np.maximum(sigma_array, 0.0)
    cumulative = np.cumsum(backflow) * dt
    total = cumulative[-1]

    if total < 1e-15:
        return t_array[-1]

    for idx in range(len(t_array)):
        if cumulative[idx] >= quantile * total:
            return t_array[idx]

    return t_array[-1]


# ---------------------------------------------------------------------------
# Main experiment
# ---------------------------------------------------------------------------

def run_single_realization(N, beta, t_max, n_t, rng, verbose=False):
    """
    Run one disorder realization of the SYK model and extract:
    - The fixed-bipartition entanglement curve S_A(t)
    - The Mori-Zwanzig memory kernel K(t)
    - A finite-window entropy-peak time
    - Threshold- and window-dependent memory diagnostics
    """
    if verbose:
        print(f"  Building {N} Majorana operators...", flush=True)
    chi_ops = build_majorana_operators(N)

    if verbose:
        print(f"  Generating SYK couplings...", flush=True)
    couplings = generate_syk_couplings(N, J=1.0, rng=rng)

    if verbose:
        print(f"  Building Hamiltonian...", flush=True)
    H = build_syk_hamiltonian(chi_ops, couplings, N)

    # Check: Tr(H) should be zero
    tr_H = np.trace(H)
    assert abs(tr_H) < 1e-8 * np.sqrt(H.shape[0]), f"Tr(H) = {tr_H}, expected ~0"

    if verbose:
        print(f"  Diagonalizing (d = {H.shape[0]})...", flush=True)
    eigenvalues, eigenvectors = np.linalg.eigh(H)

    # Subsystem dimensions
    n_A = N // 4  # Half the Majoranas -> d_A = 2^{N/4}
    n_B = N // 2 - n_A
    # But the Hilbert space factorizes into 2^{N/2} = 2^{n_A+n_B}
    # Actually for Majorana fermions, we need N/2 modes total
    # Subsystem A: first N/4 modes, subsystem B: remaining N/4 modes
    n_modes_A = N // 4
    n_modes_B = N // 2 - n_modes_A
    d_A = 2 ** n_modes_A
    d_B = 2 ** n_modes_B
    d = d_A * d_B
    assert d == H.shape[0], f"Dimension mismatch: {d} vs {H.shape[0]}"

    # Time array
    t_array = np.linspace(0, t_max, n_t)

    # Initial state: product state (ground state of subsystem A) x (ground state of subsystem B)
    # For simplicity, use a random product state
    psi_A = np.zeros(d_A, dtype=np.complex128)
    psi_A[0] = 1.0
    psi_B = np.zeros(d_B, dtype=np.complex128)
    psi_B[0] = 1.0
    psi0 = np.kron(psi_A, psi_B)

    if verbose:
        print(f"  Computing fixed-bipartition entanglement curve...", flush=True)
    S_array = compute_entanglement_curve(
        eigenvalues, eigenvectors, psi0, d_A, d_B, t_array)

    # Smoothed entropy peak within the chosen observation window. This is not
    # a black-hole Page time, and its value can move with smoothing/window size.
    window = max(3, n_t // 50)
    S_smooth = np.convolve(S_array, np.ones(window)/window, mode='same')
    idx_max = np.argmax(S_smooth[window:-window]) + window if n_t > 2*window else np.argmax(S_array)
    t_entropy_peak = t_array[idx_max]
    S_entropy_peak = S_array[idx_max]
    S_random_state_benchmark = random_state_mean_entropy(d_A, d_B)

    if verbose:
        print(f"  Entropy-peak time = {t_entropy_peak:.3f}, "
              f"S_peak = {S_entropy_peak:.4f} "
              f"(Haar-random benchmark = {S_random_state_benchmark:.4f})",
              flush=True)

    # Mori-Zwanzig analysis
    # A = i chi_0 chi_1 is a Hermitian, nonzero Majorana bilinear.
    A_op = 1j * chi_ops[0] @ chi_ops[1]
    assert np.allclose(A_op, A_op.conj().T, atol=1e-12), \
        "Majorana bilinear observable must be Hermitian"
    assert np.linalg.norm(A_op) > 1e-12, \
        "Majorana bilinear observable must be nonzero"

    if verbose:
        print(f"  Computing autocorrelation function...", flush=True)
    C_array = compute_autocorrelation(eigenvalues, eigenvectors, A_op, beta, t_array)

    if verbose:
        print(f"  Extracting memory kernel...", flush=True)
    K_array = extract_memory_kernel(C_array, t_array)

    # Memory onset time (old method, from Volterra deconvolution)
    t_memory_volterra = memory_onset_time(K_array, t_array, threshold=0.1)

    # Selected-pair, BLP-inspired trace-distance proxy (not optimized BLP)
    if verbose:
        print(f"  Computing selected-pair trace-distance proxy...", flush=True)
    D_array, sigma_array, t_pair_revival = compute_selected_pair_trace_distance(
        eigenvalues, eigenvectors, d_A, d_B, t_array, rng)

    # Window-relative median time of cumulative positive selected-pair slope.
    t_pair_backflow_median = selected_pair_backflow_quantile_time(
        sigma_array, t_array, quantile=0.5)

    if verbose:
        print(f"  First selected-pair revival = {t_pair_revival:.3f}", flush=True)
        print(f"  Within-window backflow median = {t_pair_backflow_median:.3f}",
              flush=True)
        print(f"  Volterra threshold time = {t_memory_volterra:.3f}", flush=True)
        print("  These times depend on the pair, threshold, smoothing, and time window.",
              flush=True)

    return {
        't_array': t_array,
        'S_array': S_array,
        'C_array': np.real(C_array),
        'K_array': K_array,
        'D_array': D_array,
        'sigma_array': sigma_array,
        't_entropy_peak': t_entropy_peak,
        't_pair_revival': t_pair_revival,
        't_pair_backflow_median': t_pair_backflow_median,
        't_memory_volterra': t_memory_volterra,
        'S_entropy_peak': S_entropy_peak,
        'S_random_state_benchmark': S_random_state_benchmark,
        'eigenvalues': eigenvalues,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Exploratory SYK entanglement and memory diagnostics")
    parser.add_argument("--N", type=int, default=12,
                        help="Number of Majorana fermions (default: 12)")
    parser.add_argument("--n-disorder", type=int, default=10,
                        help="Number of disorder realizations (default: 10)")
    parser.add_argument("--beta", type=float, default=0.5,
                        help="Inverse temperature for MZ analysis (default: 0.5)")
    parser.add_argument("--t-max", type=float, default=20.0,
                        help="Maximum time for evolution (default: 20.0)")
    parser.add_argument("--n-t", type=int, default=200,
                        help="Number of time points (default: 200)")
    parser.add_argument("--seed", type=int, default=2026,
                        help="Random seed (default: 2026)")
    parser.add_argument("--out-dir", type=str, default="results/syk_mz",
                        help="Output directory")
    parser.add_argument("--quick", action="store_true",
                        help="Quick smoke test with small parameters")
    args = parser.parse_args()

    if args.quick:
        args.N = 8
        args.n_disorder = 3
        args.n_t = 100
        args.t_max = 10.0

    print("=" * 70)
    print("SYK Entanglement and Memory Diagnostics (exploratory)")
    print("=" * 70)
    print(f"  N = {args.N} Majorana fermions")
    print(f"  Hilbert space dimension = {2**(args.N//2)}")
    print(f"  Subsystem dimensions = {2**(args.N//4)} x {2**(args.N//2 - args.N//4)}")
    print(f"  Disorder realizations = {args.n_disorder}")
    print(f"  beta = {args.beta}")
    print(f"  t_max = {args.t_max}, n_t = {args.n_t}")
    print(f"  Seed = {args.seed}")
    print()

    rng = np.random.default_rng(args.seed)

    # Validate Majorana algebra
    print("Validating Majorana algebra...", flush=True)
    chi_test = build_majorana_operators(args.N)
    algebra_err = validate_majorana_algebra(chi_test)
    print(f"  Max anticommutator error: {algebra_err:.2e}")
    assert algebra_err < 1e-10, f"Majorana algebra check FAILED (err = {algebra_err})"
    print("  PASSED")
    print()

    # Run disorder realizations
    results = []
    t_entropy_peaks = []
    t_backflow_medians = []

    for r in range(args.n_disorder):
        print(f"Realization {r+1}/{args.n_disorder}:", flush=True)
        t0 = time.time()
        result = run_single_realization(
            args.N, args.beta, args.t_max, args.n_t, rng, verbose=True)
        elapsed = time.time() - t0
        print(f"  Elapsed: {elapsed:.1f} s")
        print()
        results.append(result)
        t_entropy_peaks.append(result['t_entropy_peak'])
        t_backflow_medians.append(result['t_pair_backflow_median'])

    # Summary statistics
    t_entropy_peaks = np.array(t_entropy_peaks)
    t_backflow_medians = np.array(t_backflow_medians)

    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"  Entropy-peak time: mean = {np.mean(t_entropy_peaks):.3f} "
          f"+/- {np.std(t_entropy_peaks):.3f}")
    print(f"  Window-relative selected-pair backflow median: "
          f"mean = {np.mean(t_backflow_medians):.3f} "
          f"+/- {np.std(t_backflow_medians):.3f}")
    print()

    print("INTERPRETATION LIMIT:")
    print("  The entropy peak is not a black-hole Page time, and the trace-distance")
    print("  curve is a selected-pair proxy rather than an optimized BLP measure.")
    print("  Numerical proximity of these window-dependent times does not establish")
    print("  a Markovianity transition or an equivalence between the diagnostics.")
    print()

    # Validation checks
    print("VALIDATION CHECKS:")
    S_maxes = [r['S_entropy_peak'] for r in results]
    S_theories = [r['S_random_state_benchmark'] for r in results]
    print(f"  Max entropy achieved: {np.mean(S_maxes):.4f} +/- {np.std(S_maxes):.4f}")
    print(f"  Haar-random benchmark:{S_theories[0]:.4f}")
    print(f"  Entropy bound check:  ", end="")
    n_modes_A = args.N // 4
    S_bound = n_modes_A * np.log(2)
    all_bounded = all(r['S_entropy_peak'] <= S_bound + 0.01 for r in results)
    print("PASSED" if all_bounded else "FAILED")
    print()

    # Save results
    os.makedirs(args.out_dir, exist_ok=True)

    # Save numerical data
    np.savez(os.path.join(args.out_dir, "syk_mz_results.npz"),
             N=args.N,
             n_disorder=args.n_disorder,
             beta=args.beta,
             t_array=results[0]['t_array'],
             t_entropy_peaks=t_entropy_peaks,
             t_pair_backflow_medians=t_backflow_medians,
             # Store last realization's curves for plotting
             S_array=results[-1]['S_array'],
             C_array=results[-1]['C_array'],
             K_array=results[-1]['K_array'],
             D_array=results[-1]['D_array'],
             sigma_array=results[-1]['sigma_array'],
             eigenvalues_last=results[-1]['eigenvalues'])

    # Plot
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(2, 3, figsize=(18, 10))
        fig.suptitle(f"SYK Model (N={args.N}): Exploratory Entanglement and Memory",
                     fontsize=14)

        # Panel 1: fixed-bipartition entanglement curve (all realizations)
        ax = axes[0, 0]
        for r in results:
            ax.plot(r['t_array'], r['S_array'], alpha=0.3, color='steelblue')
        ax.axhline(S_theories[0], color='red', linestyle='--',
                   label='Haar-random mean benchmark')
        ax.set_xlabel('Time (J=1)')
        ax.set_ylabel(r'$S_A(t)$')
        ax.set_title('Fixed-Bipartition Entanglement Entropy')
        ax.legend()

        # Panel 2: Memory kernel (last realization)
        ax = axes[0, 1]
        r = results[-1]
        ax.plot(r['t_array'], r['K_array'], color='darkgreen')
        ax.axvline(r['t_entropy_peak'], color='red', linestyle='--',
                   label=f'entropy peak = {r["t_entropy_peak"]:.2f}')
        ax.axvline(r['t_memory_volterra'], color='orange', linestyle=':',
                   label=f'$t_M^{{\\mathrm{{Volt}}}} = {r["t_memory_volterra"]:.2f}$')
        ax.set_xlabel('Time (J=1)')
        ax.set_ylabel(r'$K(t)$')
        ax.set_title('Mori-Zwanzig Memory Kernel')
        ax.legend(fontsize=8)

        # Panel 3: selected-pair trace distance (last realization)
        ax = axes[0, 2]
        ax.plot(r['t_array'], r['D_array'], color='teal', label='Trace distance')
        ax.axvline(r['t_entropy_peak'], color='red', linestyle='--',
                   label=f'entropy peak = {r["t_entropy_peak"]:.2f}')
        ax.axvline(r['t_pair_revival'], color='blue', linestyle=':',
                   label=f'first selected-pair revival = {r["t_pair_revival"]:.2f}')
        ax.set_xlabel('Time (J=1)')
        ax.set_ylabel(r'$D(\rho_A, \rho_A^\prime)$')
        ax.set_title('Selected-Pair Trace-Distance Proxy')
        ax.legend(fontsize=8)

        # Panel 4: Autocorrelation function
        ax = axes[1, 0]
        ax.plot(r['t_array'], r['C_array'], color='purple')
        ax.axvline(r['t_entropy_peak'], color='red', linestyle='--', alpha=0.5)
        ax.set_xlabel('Time (J=1)')
        ax.set_ylabel(r'$C(t) = \langle A(t) A(0) \rangle_\beta$')
        ax.set_title(f'Thermal Autocorrelation ($\\beta = {args.beta}$)')

        # Panel 5: derivative of selected-pair trace distance
        ax = axes[1, 1]
        ax.plot(r['t_array'], r['sigma_array'], color='darkorange')
        ax.axhline(0, color='gray', linestyle='-', linewidth=0.5)
        ax.fill_between(r['t_array'], 0, r['sigma_array'],
                        where=np.array(r['sigma_array']) > 0,
                        alpha=0.3, color='red', label='Selected-pair revival')
        ax.axvline(r['t_entropy_peak'], color='red', linestyle='--', alpha=0.5)
        ax.set_xlabel('Time (J=1)')
        ax.set_ylabel(r'$\sigma(t) = dD/dt$')
        ax.set_title('Selected-Pair Positive-Slope Proxy')
        ax.legend(fontsize=8)

        # Panel 6: distributions of window-dependent diagnostic times
        ax = axes[1, 2]
        bins = max(5, args.n_disorder // 2)
        ax.hist(t_entropy_peaks, bins=bins, color='steelblue', alpha=0.6,
                label='entropy peak')
        ax.hist(t_backflow_medians, bins=bins, color='coral', alpha=0.6,
                label='selected-pair backflow median')
        ax.set_xlabel('Time within selected analysis window')
        ax.set_ylabel('Count')
        ax.set_title('Diagnostic-Time Distributions')
        ax.legend()

        plt.tight_layout()
        fig_path = os.path.join(args.out_dir, "syk_mz_analysis.png")
        plt.savefig(fig_path, dpi=150)
        print(f"Figure saved: {fig_path}")

        # Additional figure: descriptive finite-size spectral histogram
        fig2, ax2 = plt.subplots(figsize=(7, 5))
        for r in results:
            ax2.hist(r['eigenvalues'], bins=50, density=True, alpha=0.15,
                     color='steelblue', edgecolor='none')
        ax2.set_xlabel('Energy')
        ax2.set_ylabel('Density of states')
        ax2.set_title(f'Finite-Size SYK Spectral Histogram (N={args.N}; descriptive)')
        fig2_path = os.path.join(args.out_dir, "syk_spectral_density.png")
        fig2.savefig(fig2_path, dpi=150)
        print(f"Figure saved: {fig2_path}")

    except ImportError:
        print("matplotlib not available; skipping figures.")

    print()
    print("Done. Results saved to:", args.out_dir)


if __name__ == "__main__":
    main()
