---
title: "Derivation — Bloch Theorem"
type: derivation
field: "Condensed Matter Physics"
epistemic_status: established
level: advanced
tags: [physics, derivation, deep-dive]
created: 2026-07-30
updated: 2026-07-30
note_maturity: worked-derivation
source_audit: canonical-derivation-needs-citation-audit
---

# Derivation — Bloch Theorem

## Statement

For a single-particle Hamiltonian periodic under every lattice translation,

$$V(\mathbf r+\mathbf R)=V(\mathbf r),$$

energy eigenstates can be chosen as

$$
\boxed{\psi_{n\mathbf k}(\mathbf r)
=e^{i\mathbf k\cdot\mathbf r}u_{n\mathbf k}(\mathbf r)}
$$

where $u_{n\mathbf k}(\mathbf r+\mathbf R)=u_{n\mathbf k}(\mathbf r)$.

## Derivation from commuting translations

Define a lattice translation operator

$$T_{\mathbf R}\psi(\mathbf r)=\psi(\mathbf r+\mathbf R).$$

Periodicity implies

$$[H,T_{\mathbf R}]=0.$$

All lattice translations commute with each other, so energy eigenstates can be chosen as their simultaneous eigenstates:

$$T_{\mathbf R}\psi=\lambda(\mathbf R)\psi.$$

Unitarity gives $|\lambda|=1$, and the group rule

$$T_{\mathbf R_1}T_{\mathbf R_2}=T_{\mathbf R_1+\mathbf R_2}$$

requires a one-dimensional character

$$\lambda(\mathbf R)=e^{i\mathbf k\cdot\mathbf R}.$$

Define

$$u_{\mathbf k}(\mathbf r)=e^{-i\mathbf k\cdot\mathbf r}\psi_{\mathbf k}(\mathbf r).$$

Then

$$
u_{\mathbf k}(\mathbf r+\mathbf R)
=e^{-i\mathbf k\cdot(\mathbf r+\mathbf R)}
e^{i\mathbf k\cdot\mathbf R}\psi_{\mathbf k}(\mathbf r)
=u_{\mathbf k}(\mathbf r).
$$

## Reciprocal equivalence

$\mathbf k$ and $\mathbf k+\mathbf G$ describe equivalent translation eigenvalues when $\mathbf G\cdot\mathbf R=2\pi n$. This motivates restriction to one Brillouin zone.

## Extensions and limits

Interactions may preserve crystal momentum for many-body states, while disorder breaks exact translation symmetry. Magnetic fields, nonsymmorphic symmetries, topology, and quasiperiodicity require generalized formulations.

## Connected notes

[[Bloch Theorem]] · [[Crystal Lattices]] · [[Reciprocal Lattice]] · [[Brillouin Zones]] · [[Electronic Band Structure]]

## Navigation

[[Derivation Atlas]] · [[Physics Worldmap]]
