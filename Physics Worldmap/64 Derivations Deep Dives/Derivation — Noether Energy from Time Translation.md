---
title: "Derivation — Noether Energy from Time Translation"
type: derivation
field: "Foundations of Physics"
epistemic_status: established
level: advanced
tags: [physics, derivation, deep-dive]
created: 2026-07-30
updated: 2026-07-30
note_maturity: worked-derivation
source_audit: canonical-derivation-needs-citation-audit
---

# Derivation — Noether Energy from Time Translation

## Target

Show how time-translation invariance of a mechanical action produces a conserved energy function.

## Direct derivation

For a Lagrangian $L(q_i,\dot q_i,t)$ define generalized momenta

$$p_i=\frac{\partial L}{\partial\dot q_i}.$$

Along an Euler-Lagrange trajectory,

$$
\frac{dL}{dt}
=\frac{\partial L}{\partial q_i}\dot q_i
+\frac{\partial L}{\partial\dot q_i}\ddot q_i
+\frac{\partial L}{\partial t}.
$$

Use $\partial L/\partial q_i=\dot p_i$:

$$
\frac{dL}{dt}
=\dot p_i\dot q_i+p_i\ddot q_i+\frac{\partial L}{\partial t}
=\frac d{dt}(p_i\dot q_i)+\frac{\partial L}{\partial t}.
$$

Therefore

$$
\frac d{dt}\left(p_i\dot q_i-L\right)
=-\frac{\partial L}{\partial t}.
$$

If the Lagrangian has no explicit time dependence, the quantity

$$
\boxed{E=p_i\dot q_i-L}
$$

is conserved.

For $L=T-V$ with a velocity-independent potential and a quadratic kinetic energy, Euler's homogeneous-function theorem gives $p_i\dot q_i=2T$, so $E=T+V$.

## Important qualifications

- Noether's theorem concerns invariance of the **action**, including possible boundary terms.
- A conserved Noether energy need not equal a naive sum of kinetic and potential terms.
- If the system exchanges energy with an unmodeled environment, the reduced subsystem need not conserve energy.
- General relativity replaces simple global time translation with geometry-dependent statements; a global conserved energy may require special spacetime symmetries or asymptotic structure.

## Connected notes

[[Symmetry Conservation and Noether Map]] · [[Conservation Laws]] · [[Noethers Theorem in Mechanics]] · [[Hamiltonian Mechanics]]

## Navigation

[[Derivation Atlas]] · [[Physics Worldmap]]
