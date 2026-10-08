---
title: "Deep Dive — Density Matrices Partial Trace and Entanglement"
type: derivation
field: "Quantum Mechanics"
epistemic_status: established
level: advanced
tags: [physics, derivation, deep-dive]
created: 2026-07-30
updated: 2026-07-30
note_maturity: worked-derivation
source_audit: canonical-derivation-needs-citation-audit
---

# Deep Dive — Density Matrices Partial Trace and Entanglement

## Why density operators are needed

A preparation that yields $|\psi_i\rangle$ with classical probability $p_i$ is represented by

$$\rho=\sum_ip_i|\psi_i\rangle\langle\psi_i|.$$

Every measurement effect $E_a$ has probability

$$p(a)=\operatorname{Tr}(\rho E_a).$$

Different ensemble decompositions can generate the same $\rho$ and are then operationally indistinguishable on that system.

## Reduced state

For a composite state $\rho_{AB}$, predictions for measurements on $A$ alone use

$$\rho_A=\operatorname{Tr}_B\rho_{AB}.$$

Choose a basis $|j\rangle_B$:

$$
\rho_A=\sum_j {}_B\langle j|\rho_{AB}|j\rangle_B.
$$

This operation is basis-independent even though the formula uses a basis.

## Bell-pair example

Let

$$|\Phi^+\rangle=\frac{|00\rangle+|11\rangle}{\sqrt2}.$$

The total state is pure:

$$\rho_{AB}=|\Phi^+\rangle\langle\Phi^+|,\qquad
\operatorname{Tr}\rho_{AB}^2=1.
$$

Tracing out $B$ gives

$$\rho_A=\frac12(|0\rangle\langle0|+|1\rangle\langle1|)=I/2.$$

Thus a subsystem can be mixed even when the joint system is pure. The missing local purity is stored in correlations.

## Entropies

The von Neumann entropy is

$$S(\rho)=-\operatorname{Tr}(\rho\ln\rho).$$

For a bipartite pure state, $S(\rho_A)=S(\rho_B)$ is an entanglement entropy. For mixed states, entropy also includes classical uncertainty and is not by itself an entanglement measure.

## Connected notes

[[Density Matrices]] · [[Composite Quantum Systems]] · [[Quantum Entanglement]] · [[Decoherence]] · [[Open Quantum Systems]]

## Navigation

[[Derivation Atlas]] · [[Physics Worldmap]]
