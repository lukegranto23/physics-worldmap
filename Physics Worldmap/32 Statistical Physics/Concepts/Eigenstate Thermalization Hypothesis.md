---
type: "concept"
field: "Statistical Physics"
epistemic_status: "active"
level: "advanced"
tags: ["physics", "field/statistical", "status/active", "level/advanced"]
aliases: ["ETH"]
created: 2026-07-31
updated: 2026-09-04
note_maturity: expanded
source_audit: bibliography-present-needs-claim-audit
---

# Eigenstate Thermalization Hypothesis

> [!summary] Core idea
> ETH proposes that suitably simple observables in typical chaotic many-body energy eigenstates agree with thermal predictions within a resolved symmetry sector. It explains a broad mechanism for local thermalization, not a theorem for every nonintegrable system.

> [!note] Documentation status
> Expanded orientation with a canonical review; generality and exceptions remain research questions.

## Matrix-element ansatz

For a few-body observable $O$,
$$
O_{mn}=O(\bar E)\delta_{mn}
+e^{-S(\bar E)/2}f_O(\bar E,\omega)R_{mn},
\qquad
\bar E=(E_m+E_n)/2,\quad\omega=E_m-E_n,
$$
using $\hbar=1$. Here $S$ is the thermodynamic entropy in the chosen sector and energy window, $O(\bar E)$ is smooth, and the fluctuating factors $R_{mn}$ have roughly zero mean and unit variance. Their detailed correlations cannot always be replaced by independent random numbers. [D’Alessio et al.](https://arxiv.org/abs/1509.06411)

## Why it can lead to thermalization

For $|\psi_0\rangle=\sum_n c_n|E_n\rangle$,
$$
\langle O(t)\rangle=\sum_{mn}c_m^*c_n
e^{i(E_m-E_n)t}O_{mn}.
$$
If the initial energy distribution is narrow and the relevant diagonal elements vary smoothly, the diagonal ensemble $\sum_n|c_n|^2O_{nn}$ approximates the microcanonical answer. Off-diagonal terms dephase for most sufficiently late times under suitable spectral conditions. They do not disappear permanently: finite systems can recur.

A pure global state stays pure. Thermalization concerns local observables or reduced states, not convergence of the full wavefunction to a mixed Gibbs state.

## Strong, weak, and subsystem ETH

Strong ETH concerns all eigenstates in a specified regime; weak ETH permits a vanishing fraction of exceptions. Subsystem ETH asks for agreement of reduced density matrices and requires constraints on subsystem fraction and energy. These versions are not interchangeable.

The ansatz alone does not supply one universal relaxation time. Initial states, conservation laws, transport, rare states, and spectral functions influence the approach to equilibrium. [Deutsch review](https://arxiv.org/abs/1805.01616)

## Counterexamples and qualifications

Integrable systems require additional conserved quantities and can relax to generalized ensembles. Many-body-localized regimes and quantum scars challenge strong ETH; their stability and scope must be stated model by model. Nonintegrability is not by itself a guarantee that every initial state thermalizes.

## What ETH does not imply

- It does not fix a universal finite-subsystem entropy correction.
- It does not turn a quench entropy maximum into a black-hole Page time.
- It does not identify an MZ memory kernel with off-diagonal matrix elements without specifying a projection and inner product.
- It does not prove that all local reduced evolution is Markovian.

## A controlled computational test

Resolve symmetry sectors; choose a narrow energy window; plot diagonal-observable variation versus system size; compare nearby eigenstates; examine off-diagonal statistics; and test time evolution from several energy-matched states. Include an integrable control. Distinguish evidence of finite-size ETH scaling from a thermodynamic-limit proof.

## Recall checks

Derive the diagonal-ensemble prediction under nondegeneracy assumptions. Explain why a broad energy distribution may fail to look like one thermal ensemble. Construct a conserved observable that must be treated separately.

## Navigation

[[Statistical Physics Map]] · Quantum Thermalization · [[SYK Model]] · [[Open Quantum Systems]] · [[Synthesis Session 002 — Holographic Coarse-Graining and the Memory of Spacetime]] · [[Physics Worldmap]]
