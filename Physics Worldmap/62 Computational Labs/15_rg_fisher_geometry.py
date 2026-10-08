#!/usr/bin/env python3
"""
Lab 15 — Exploratory Ising blocking and Fisher-response diagnostics.

Samples a finite square-lattice Ising model, majority-rule blocks its spins,
and records energy variance and neighbor correlations. arctanh(correlation)
is a one-dimensional/high-temperature-inspired COUPLING PROXY, not calibrated
2D inverse inference. Its difference from input K is not a controlled beta
function; even signs and fixed points may be biased.

A potential integrated from that proxy flow is constructed by definition,
not an independently computed c-function. One-dimensional gradient alignment
is tautological. Blocking generates discarded couplings. A genuine RG test
needs calibrated multi-coupling inference, uncertainty, and held-out checks.

Execution and bounds checks test the pipeline only, not a physics hypothesis.
Dependencies: numpy, matplotlib.
"""

import argparse
import os
import time

import numpy as np

# Exact critical coupling for 2D Ising
K_C = np.log(1 + np.sqrt(2)) / 2  # ≈ 0.4407


# ---------------------------------------------------------------------------
# Wolff cluster algorithm
# ---------------------------------------------------------------------------

def wolff_sweep(spins, K, rng):
    """
    One Wolff cluster update step.

    The Wolff algorithm builds a cluster of aligned spins and flips them all.
    The bond activation probability is p = 1 - exp(-2K).
    This is efficient near criticality where Metropolis suffers from critical
    slowing down.
    """
    L = spins.shape[0]
    p_add = 1.0 - np.exp(-2.0 * K)

    # Pick a random seed site
    i0, j0 = rng.integers(0, L, size=2)
    seed_spin = spins[i0, j0]

    # BFS to build cluster
    cluster = set()
    stack = [(i0, j0)]
    cluster.add((i0, j0))

    while stack:
        i, j = stack.pop()
        for di, dj in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            ni, nj = (i + di) % L, (j + dj) % L
            if (ni, nj) not in cluster and spins[ni, nj] == seed_spin:
                if rng.random() < p_add:
                    cluster.add((ni, nj))
                    stack.append((ni, nj))

    # Flip the cluster
    for (i, j) in cluster:
        spins[i, j] *= -1

    return len(cluster)


def total_energy(spins):
    """Compute sum_{<ij>} s_i * s_j (total nearest-neighbor interaction)."""
    return float(np.sum(
        spins * np.roll(spins, 1, axis=0) +
        spins * np.roll(spins, 1, axis=1)
    ))


def nn_correlation(spins):
    """Compute <s_i s_j> for nearest neighbors (averaged over all bonds)."""
    L = spins.shape[0]
    n_bonds = 2 * L * L
    return total_energy(spins) / n_bonds


def magnetization(spins):
    """Compute m = (1/N) sum s_i."""
    return np.mean(spins)


# ---------------------------------------------------------------------------
# Block-spin RG transformation
# ---------------------------------------------------------------------------

def block_spin_rg(spins, rng):
    """
    Perform a 2x2 majority-rule block-spin RG transformation.

    For each 2x2 block, the block spin is:
      +1 if sum >= 0 (with ties broken randomly)
      -1 if sum < 0

    Input: LxL lattice (L must be even)
    Output: (L/2)x(L/2) lattice of block spins
    """
    L = spins.shape[0]
    assert L % 2 == 0, "L must be even for block-spin RG"
    L_new = L // 2
    blocked = np.zeros((L_new, L_new), dtype=np.int8)

    for I in range(L_new):
        for J in range(L_new):
            block_sum = (spins[2*I, 2*J] + spins[2*I+1, 2*J] +
                         spins[2*I, 2*J+1] + spins[2*I+1, 2*J+1])
            if block_sum > 0:
                blocked[I, J] = 1
            elif block_sum < 0:
                blocked[I, J] = -1
            else:
                # Tie: break randomly
                blocked[I, J] = rng.choice([-1, 1])

    return blocked


def estimate_K_from_correlation(nn_corr):
    """
    Return arctanh(correlation), an uncalibrated 2D coupling proxy.
    Exact for nearest-neighbor correlations of an infinite zero-field 1D
    chain, not for 2D near criticality. Monotonicity of this transformation
    does NOT ensure that proxy_K - input_K preserves true flow signs.
    """
    # Clamp to avoid divergence at |corr| = 1
    c = np.clip(nn_corr, -0.999, 0.999)
    return np.arctanh(c)


# ---------------------------------------------------------------------------
# Fisher information metric
# ---------------------------------------------------------------------------

def compute_fisher_metric(energy_samples, n_bonds):
    """
    Compute the Fisher information metric g_KK.

    For the distribution p(s|K) = (1/Z) exp(K * E_total):
    g_KK = Var(E_total) = <E^2> - <E>^2

    We normalize per bond for comparison across system sizes:
    g_KK_per_bond = Var(E_total) / n_bonds^2 ... no
    Actually, the extensive Fisher metric is Var(E_total).
    The intensive (per bond) Fisher metric is Var(E_total/n_bonds) * n_bonds
    = Var(E_total) / n_bonds.
    """
    return np.var(energy_samples) / n_bonds


# ---------------------------------------------------------------------------
# Main experiment
# ---------------------------------------------------------------------------

def run_at_coupling(K, L, n_thermalize, n_samples, sample_stride, rng, verbose=False):
    """
    Run MC at coupling K, perform block-spin RG, measure observables.

    Returns dict with: K, K_blocked, beta, fisher_metric, nn_corr, nn_corr_blocked,
    magnetization, energy_mean, energy_var, etc.
    """
    spins = rng.choice(np.array([-1, 1], dtype=np.int8), size=(L, L))

    # Thermalize with Wolff
    for _ in range(n_thermalize):
        wolff_sweep(spins, K, rng)

    # Collect samples
    energies = []
    nn_corrs = []
    nn_corrs_blocked = []
    mags = []

    for _ in range(n_samples):
        for _ in range(sample_stride):
            wolff_sweep(spins, K, rng)

        E = total_energy(spins)
        energies.append(E)
        nn_corrs.append(nn_correlation(spins))
        mags.append(abs(magnetization(spins)))

        # Block-spin RG
        blocked = block_spin_rg(spins, rng)
        nn_corrs_blocked.append(nn_correlation(blocked))

    energies = np.array(energies)
    nn_corrs = np.array(nn_corrs)
    nn_corrs_blocked = np.array(nn_corrs_blocked)
    mags = np.array(mags)

    n_bonds = 2 * L * L
    fisher = compute_fisher_metric(energies, n_bonds)

    # Estimate K' from block-spin correlation
    mean_nn_blocked = np.mean(nn_corrs_blocked)
    K_blocked = estimate_K_from_correlation(mean_nn_blocked)

    beta_K = K_blocked - K  # RG "beta function" (change in coupling per RG step)

    if verbose:
        print(f"  K = {K:.4f}: <nn> = {np.mean(nn_corrs):.4f}, "
              f"<nn_block> = {mean_nn_blocked:.4f}, K' = {K_blocked:.4f}, "
              f"beta = {beta_K:.4f}, g_F = {fisher:.4f}, "
              f"|m| = {np.mean(mags):.4f}")

    return {
        'K': K,
        'K_blocked': K_blocked,
        'beta': beta_K,
        'fisher_metric': fisher,
        'nn_corr': np.mean(nn_corrs),
        'nn_corr_blocked': mean_nn_blocked,
        'magnetization': np.mean(mags),
        'energy_mean': np.mean(energies) / n_bonds,
        'energy_var': np.var(energies),
        'n_bonds': n_bonds,
    }


def main():
    parser = argparse.ArgumentParser(description="Exploratory Ising blocking diagnostics")
    parser.add_argument("--L", type=int, default=64)
    parser.add_argument("--n-K", type=int, default=25)
    parser.add_argument("--K-min", type=float, default=0.20)
    parser.add_argument("--K-max", type=float, default=0.65)
    parser.add_argument("--n-thermalize", type=int, default=500)
    parser.add_argument("--n-samples", type=int, default=800)
    parser.add_argument("--sample-stride", type=int, default=3)
    parser.add_argument("--seed", type=int, default=2026)
    parser.add_argument("--out-dir", default="results/rg_fisher")
    parser.add_argument("--quick", action="store_true")
    args = parser.parse_args()
    if args.quick:
        args.L, args.n_K = 32, 15
        args.n_thermalize, args.n_samples, args.sample_stride = 200, 300, 2
    if (args.L < 4 or args.L % 2 or args.n_K < 3 or
            not 0 < args.K_min < args.K_max or args.n_samples < 2 or
            args.n_thermalize < 1 or args.sample_stride < 1):
        parser.error("require even L >= 4, n-K >= 3, positive ordered couplings and sampling counts")
    rng = np.random.default_rng(args.seed)
    K_arr = np.linspace(args.K_min, args.K_max, args.n_K)
    rows = []
    print("Exploratory Ising blocking: uncalibrated coupling proxy, not an RG theorem", flush=True)
    start = time.perf_counter()
    for index, K in enumerate(K_arr):
        row = run_at_coupling(K, args.L, args.n_thermalize,
                              args.n_samples, args.sample_stride, rng)
        rows.append(row)
        print(f"[{index+1}/{args.n_K}] K={K:.4f}, proxy K'={row['K_blocked']:.4f}, "
              f"Fisher/bond={row['fisher_metric']:.4f}", flush=True)
    proxy = np.array([r["K_blocked"] for r in rows])
    flow = proxy - K_arr
    fisher = np.array([r["fisher_metric"] for r in rows])
    corr = np.array([r["nn_corr"] for r in rows])
    blocked = np.array([r["nn_corr_blocked"] for r in rows])
    integrand = -fisher * flow
    potential = np.zeros_like(K_arr)
    potential[1:] = np.cumsum(0.5 * (integrand[1:] + integrand[:-1]) * np.diff(K_arr))
    assert all(np.all(np.isfinite(x)) for x in (proxy, flow, fisher, corr, blocked, potential))
    assert np.all(fisher >= 0) and np.all(np.abs(corr) <= 1 + 1e-12)
    assert np.all(np.abs(blocked) <= 1 + 1e-12)
    print("PASS finite-output and correlation/variance bounds (pipeline checks only)")
    print("No natural-gradient, c-function, or calibrated fixed-point claim follows.")
    print("arctanh inversion is not valid 2D inference near criticality.")
    print(f"Elapsed {time.perf_counter()-start:.1f} s; seed={args.seed}")
    os.makedirs(args.out_dir, exist_ok=True)
    np.savez(os.path.join(args.out_dir, "rg_fisher_results.npz"),
             K_arr=K_arr, K_proxy=proxy, flow_proxy=flow, fisher_arr=fisher,
             constructed_potential=potential, nn_corr=corr, blocked_corr=blocked,
             L=args.L, seed=args.seed, n_samples=args.n_samples,
             n_thermalize=args.n_thermalize, sample_stride=args.sample_stride)
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    axes[0, 0].plot(K_arr, corr, "o-", label="original")
    axes[0, 0].plot(K_arr, blocked, "o-", label="blocked")
    axes[0, 0].set_title("Measured nearest-neighbor correlations")
    axes[0, 0].legend()
    axes[0, 1].plot(K_arr, fisher, "o-")
    axes[0, 1].set_title("Fisher response per bond")
    axes[1, 0].plot(K_arr, flow, "o-")
    axes[1, 0].axhline(0, color="gray", lw=0.8)
    axes[1, 0].set_title("Uncalibrated coupling displacement proxy")
    axes[1, 1].plot(K_arr, potential, "o-")
    axes[1, 1].set_title("Constructed potential — NOT a c-function")
    for ax in axes.flat:
        ax.set_xlabel("Input K")
        ax.axvline(K_C, color="red", ls="--", alpha=0.5)
        ax.grid(alpha=0.2)
    fig.suptitle("Exploratory Ising diagnostics; dashed line = exact critical K")
    fig.tight_layout()
    fig.savefig(os.path.join(args.out_dir, "rg_fisher_analysis.png"), dpi=150)
    plt.close(fig)
    print(f"Results saved to {args.out_dir}")


if __name__ == "__main__":
    main()
