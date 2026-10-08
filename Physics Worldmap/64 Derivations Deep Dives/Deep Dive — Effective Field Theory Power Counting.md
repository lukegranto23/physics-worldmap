---
title: "Deep Dive — Effective Field Theory Power Counting"
type: derivation
field: "Quantum Field Theory and Particle Physics"
epistemic_status: established
level: advanced
tags: [physics, derivation, deep-dive]
created: 2026-07-30
updated: 2026-07-30
note_maturity: worked-derivation
source_audit: canonical-derivation-needs-citation-audit
---

# Deep Dive — Effective Field Theory Power Counting

## Core idea

At energies $E$ far below a heavy scale $\Lambda$, unresolved physics is represented by local operators consistent with the low-energy symmetries:

$$
\mathcal L_{\rm EFT}
=\mathcal L_{\rm light}
+\sum_i\frac{c_i}{\Lambda^{d_i-4}}\mathcal O_i.
$$

In four spacetime dimensions, operator $\mathcal O_i$ has mass dimension $d_i$.

## Power counting

A contribution from an operator of dimension $d$ typically scales as

$$
\mathcal A_d\sim c_d\left(\frac E\Lambda\right)^{d-4}
$$

relative to dimension-four interactions, with additional coupling, loop, symmetry, and kinematic factors.

This ordering converts ignorance into a controlled expansion: compute all terms through a chosen order and estimate the omitted remainder.

## Matching

Suppose a heavy field of mass $M$ mediates an interaction with propagator

$$\frac1{p^2-M^2}.$$

For $p^2\ll M^2$,

$$
\frac1{p^2-M^2}
=-\frac1{M^2}\left(1+\frac{p^2}{M^2}+\cdots\right).
$$

The low-energy theory contains contact operators with coefficients determined by matching amplitudes or observables to the full theory.

## Running

Loops within the EFT make coefficients depend on renormalization scale. Running sums logarithms and preserves scale independence of physical predictions order by order:

$$\mu\frac{dc_i}{d\mu}=\gamma_{ij}c_j.$$

## What EFT does and does not say

- It explains why low-energy predictions can be insensitive to unknown ultraviolet details.
- It does not identify the ultraviolet completion unless coefficient patterns are sufficiently diagnostic.
- Symmetries can forbid or suppress operators.
- A breakdown appears when $E/\Lambda$ is not small, new states become accessible, or unitarity/analyticity signals demand completion.

## Connected notes

[[Effective Field Theory]] · [[Effective Theories]] · [[Renormalization]] · [[Renormalization Group in QFT]] · [[Approximation and Regime Map]]

## Navigation

[[Derivation Atlas]] · [[Physics Worldmap]]
