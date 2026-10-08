---
type: "concept"
field: "Condensed Matter Physics"
epistemic_status: "mixed"
level: "advanced"
tags: ["physics", "field/condensed", "status/mixed", "level/advanced"]
aliases: ["Sachdev-Ye-Kitaev model", "SYK"]
created: 2026-07-30
updated: 2026-09-04
note_maturity: expanded
source_audit: bibliography-present-needs-claim-audit
---

# SYK Model

> [!summary] Core idea
> Random all-to-all interactions of many Majorana fermions give a tractable large-$N$ model of strongly interacting quantum matter. Its low-energy Schwarzian sector shares important structure with nearly-AdS$_2$/JT gravity; this is not an exact identification of every finite SYK Hamiltonian with a black hole.

> [!note] Documentation status
> Expanded orientation with canonical sources and targeted precision checks; not a complete claim-by-claim literature audit.

## Definition and conventions

For even $N$ and even interaction order $q$,
$$
H=i^{q/2}\sum_{i_1<\cdots<i_q}J_{i_1\cdots i_q}\chi_{i_1}\cdots\chi_{i_q},
\qquad \{\chi_i,\chi_j\}=\delta_{ij},
$$
with independent zero-mean real Gaussian couplings
$$
\overline{J_{i_1\cdots i_q}^2}=\frac{(q-1)!J^2}{N^{q-1}}.
$$
The Hilbert-space dimension is $2^{N/2}$ before resolving fermion-parity sectors. The phase ensures Hermiticity. For $q=4$, changing its overall sign is distributionally equivalent for symmetric random couplings, but comparisons of individual realizations must use the same convention.

## Controlled large-$N$ structure

Disorder-averaged two-point functions obey self-consistent Schwinger–Dyson equations. With a compatible Euclidean convention,
$$
G(i\omega_n)^{-1}=-i\omega_n-\Sigma(i\omega_n),\qquad
\Sigma(\tau)=J^2G(\tau)^{q-1}.
$$
For interacting $q>2$, the strong-coupling infrared solution behaves as
$G(\tau)\propto\operatorname{sgn}(\tau)/|J\tau|^{2/q}$.
This describes the absence of a sharp quasiparticle pole, not the absence of every physical excitation. Large-$N$ tractability means controlled equations and expansions, not closed forms for all observables at finite $N$. [Maldacena and Stanford](https://arxiv.org/abs/1604.07818)

## Gravity connection and its boundary

The soft reparametrization mode has a Schwarzian effective action. Nearly-AdS$_2$ JT gravity has the same low-energy boundary structure. Matching this sector is powerful, but additional SYK modes, finite coupling, finite size, the disorder ensemble, and ultraviolet completion matter. The shared action is not proof of a full microscopic duality between arbitrary finite SYK and pure JT gravity. [JT gravity review](https://link.springer.com/article/10.1007/s41114-023-00046-1)

## Chaos, thermodynamics, and spectra

- In the appropriate large-$N$, strong-coupling thermal regime, a regularized out-of-time-order correlator has a growth exponent approaching $\lambda_L=2\pi k_BT/\hbar$. Finite-coupling corrections and finite-size saturation matter. The chaos bound assumes analyticity and factorization properties; unitarity alone is not enough. [Maldacena, Shenker, and Stanford](https://arxiv.org/abs/1503.01409)
- In the order of limits $N\to\infty$ before $T\to0$, low-temperature thermodynamics has residual entropy density and linear specific heat. A convenient parametrization is $F=E_0-TS_0-\tfrac12\gamma T^2+\cdots$, so $S=S_0+\gamma T$ and $C=\gamma T$. This must not be confused with extensive exact degeneracy of a generic finite realization.
- Many-body density of states is not generically a Wigner semicircle. Q-Hermite approximations capture important SYK spectral features. Local random-matrix level statistics and the global density of states are distinct questions. [García-García and Verbaarschot](https://doi.org/10.1103/PhysRevD.96.066012)
- Spectral-statistics comparisons require resolving symmetries and choosing the appropriate random-matrix class; there is no universal class for all SYK variants.

## Numerical checks

1. Verify the Majorana anticommutation relations and Hamiltonian Hermiticity.
2. Resolve parity and other relevant symmetry sectors before testing level repulsion.
3. Check norm, reduced-state trace/positivity, and $0\le S_A\le\ln d_A$.
4. Vary disorder samples, size, temperature, and time resolution.
5. Distinguish correlation functions, kernel-inversion diagnostics, and reduced dynamical maps.

A fixed bipartition of a closed SYK system is not an evaporating radiation subsystem. An entropy peak is not automatically a black-hole Page time. See [[Synthesis Session 002 — Holographic Coarse-Graining and the Memory of Spacetime]].

## What remains open

Which features survive realistic locality, sparse couplings, finite sizes, and experimental errors? Which proposed gravity observables are specific to holographic structure rather than generic chaotic finite systems? Experimental simulation of a small engineered model tests that model, not the existence of a physical gravitational wormhole.

## Recall checks

Explain the order-of-limits issue for residual entropy; distinguish spectral density from level statistics; identify the assumptions behind maximal chaos; state exactly which sector is compared with JT gravity.

## Navigation

[[Condensed Matter Physics Map]] · [[Non Fermi Liquids]] · [[Quantum Phase Transitions]] · [[AdS-CFT Correspondence]] · [[Eigenstate Thermalization Hypothesis]] · [[Computational Lab Index]] · [[Physics Worldmap]]
