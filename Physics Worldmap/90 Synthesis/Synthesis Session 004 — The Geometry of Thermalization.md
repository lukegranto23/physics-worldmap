---
title: "Synthesis Session 004 — The Geometry of Thermalization"
type: synthesis
field: "Cross-domain"
epistemic_status: "conjectural"
level: "advanced"
tags: [physics, synthesis, information-geometry, thermalization, holography]
created: 2026-08-01
updated: 2026-09-02
prior_art_audit: initial-not-exhaustive
---

# Synthesis Session 004 — The Geometry of Thermalization

> [!warning] Research status
> Density-matrix trajectories can be studied geometrically. No Page-time/Bures-transition equivalence has been established. The current finite closed-system calculation is an exploratory diagnostic, not a black-hole evaporation model and not evidence for a bulk-geometric interpretation.

[[Synthesis Lab]] · [[Information Geometry]] · [[Open Quantum Systems]] · [[Synthesis Session 002 — Holographic Coarse-Graining and the Memory of Spacetime]]

## 1. Geometry that is actually defined

Choose the squared fidelity convention

$$
F(\rho,\sigma)=\left[\operatorname{Tr}\sqrt{\sqrt\rho\,\sigma\sqrt\rho}\right]^2,
$$

and Bures distance

$$
D_B^2(\rho,\sigma)=2\left(1-\sqrt{F(\rho,\sigma)}\right).
$$

For a differentiable one-parameter family $\rho(\theta)$, define the symmetric logarithmic derivative $L_\theta$ by

$$
\partial_\theta\rho=\frac12(\rho L_\theta+L_\theta\rho).
$$

The SLD quantum Fisher information is

$$
F_Q(\theta)=\operatorname{Tr}(\rho L_\theta^2),
$$

and, with these conventions, the infinitesimal Bures line element is

$$
ds_B^2=\frac14F_Q(\theta)d\theta^2.
$$

Petz’s classification contains an **infinite family** of monotone quantum metrics. The Bures/SLD choice is operationally central and contractive under quantum channels, but it is not the unique quantum monotone metric.

For time evolution, the instantaneous Bures speed is

$$
v_B(t)=\lim_{\delta t\to0}
\frac{D_B(\rho(t),\rho(t+\delta t))}{|\delta t|}.
$$

This quantity depends on the chosen subsystem, initial state, Hamiltonian or channel, and time parametrization.

## 2. Useful questions without overclaiming

A thermalizing subsystem suggests several measurable comparisons:

- Does $v_B(t)$ track local relaxation, entropy production, or distance to a declared stationary ensemble?
- Which geometric statistic is robust to time resolution and smoothing?
- Do integrable, many-body-localized, and chaotic systems show distinguishable trajectory geometry at matched size and energy density?
- Does a fitted Markovian channel reproduce held-out Bures distances and response functions?
- How do different monotone metrics change the conclusion?

These are descriptive and discriminating questions. None requires calling an entropy maximum a phase transition.

## 3. Three traps

### Finite diameter does not bound path length

The Bures distance between two endpoints is bounded in finite dimension, but a trajectory can loop or fluctuate indefinitely. Therefore

$$
s(t)=\int_0^t v_B(t')dt'
$$

need not saturate. A bounded manifold can contain curves of arbitrarily long arc length. Endpoint distance, cumulative path length, and distance to equilibrium are different observables.

### A single trajectory is not a BLP test

The Breuer–Laine–Piilo criterion concerns trace-distance distinguishability for pairs of initial system states under the **same reduced dynamical map**, optimized or bounded over legitimate pairs with a fixed environment preparation. A reversal of one trajectory or an increase in distance from its initial point is not equivalent to BLP information backflow.

### Entanglement peak is not automatically Page time

For a fixed finite bipartition evolved by a time-independent closed Hamiltonian, subsystem entropy commonly rises and fluctuates. The first smoothed maximum depends on the state, size, window, and smoothing. A black-hole Page time instead refers to radiation entropy during evaporation, where the radiation subsystem grows and a gravitational generalized-entropy calculation supplies an independent saddle transition.

## 4. What Computational Lab 16 establishes

`62 Computational Labs/16_bures_thermalization_geometry.py` constructs small SYK matrices, evolves a product state, computes a reduced density matrix, and plots entropy, purity, pairwise Bures steps, and selected trace-distance diagnostics. It is useful for checking numerical definitions and generating hypotheses.

It does not validate a “Bures speed transition near the Page time.” Its ratio thresholds are broad exploratory diagnostics; the entropy-peak time is not a black-hole Page time; cumulative path-length saturation is not theoretically required; and small systems have strong recurrences. Any apparent alignment must be treated as a finite-size correlation discovered in the same data used to define the statistic.

## 5. A controlled benchmark

1. Predeclare endpoint distance, speed, curvature, and distance-to-stationary-state estimators.
2. Use independent training and held-out time windows; never define a threshold from the curve and then test it on the same curve.
3. Compare chaotic, integrable, and random-matrix controls at matched Hilbert-space dimension and spectral bandwidth.
4. Vary initial states and subsystem fractions.
5. Quantify time-step, eigenvalue-regularization, smoothing, and finite-size errors.
6. For non-Markovianity, reconstruct or otherwise specify a legitimate family of reduced maps and state pairs.
7. If testing a Page-time relation, use an actual system–bath evaporation model with an independently calculated radiation-entropy/QES transition.

### Falsifiers

The proposed unification is disfavored if the extracted time follows observation-window length, recurrence time, arbitrary smoothing, or generic equilibration in non-holographic controls; if different monotone metrics give incompatible transitions; or if no feature survives finite-size scaling.

## 6. Holographic boundary

Bures geometry is a geometry on a family of density matrices. A bulk metric is a spacetime geometry. Ryu–Takayanagi relates a boundary entropy to a bulk extremal-area functional in a controlled limit, but it does not identify the Bures speed of a subsystem with radial bulk velocity, nor the Page time with a geodesic turning point. Such a dictionary would require a derivation with declared states, regions, coordinates, and approximation order.

## 7. Sources

- [Petz, “Monotone metrics on matrix spaces”](https://doi.org/10.1016/0024-3795(94)00211-8)
- D. Bures, *Transactions of the American Mathematical Society* **135**, 199 (1969)
- A. Uhlmann, *Reports on Mathematical Physics* **9**, 273 (1976)
- [[Synthesis Session 002 — Holographic Coarse-Graining and the Memory of Spacetime]] for the corrected Page-time boundary

## Navigation

[[Synthesis Lab]] · [[Connection Ledger]] · [[Synthesis Session 002 — Holographic Coarse-Graining and the Memory of Spacetime]] · [[Synthesis Session 003 — RG Flow as Information Geometry and the Shape of Scale]] · [[Physics Worldmap]]
