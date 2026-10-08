---
title: "Deep Dive — Renormalization Group and Universality"
type: derivation
field: "Statistical Physics"
epistemic_status: established
level: advanced
tags: [physics, derivation, deep-dive]
created: 2026-07-30
updated: 2026-07-30
note_maturity: worked-derivation
source_audit: canonical-derivation-needs-citation-audit
---

# Deep Dive — Renormalization Group and Universality

## Core operation

A renormalization-group step has three conceptual parts:

1. integrate or average over short-distance degrees of freedom;
2. rescale lengths and fields to restore the comparison scale;
3. read off new couplings.

If the Hamiltonian or action has couplings $g_i$, repeated coarse-graining defines a flow

$$\frac{dg_i}{d\ln b}=\beta_i(\mathbf g).$$

A fixed point obeys $\beta_i(\mathbf g_*)=0$.

## Linearized flow

Near a fixed point,

$$
\frac{d\,\delta g_i}{d\ln b}=M_{ij}\delta g_j.
$$

For an eigenvector with eigenvalue $y$,

$$\delta g(b)=b^y\delta g(1).$$

- $y>0$: relevant perturbation grows at long distance.
- $y<0$: irrelevant perturbation fades.
- $y=0$: marginal; nonlinear terms decide.

Microscopic models that flow to the same fixed point share long-distance exponents and scaling functions: a universality class.

## Correlation-length exponent

Let reduced temperature $t$ be the single relevant thermal variable with eigenvalue $y_t$. Coarse-graining by $b$ transforms $t\to b^{y_t}t$. The correlation length must obey

$$\xi(t)=b\,\xi(b^{y_t}t).$$

Choose $b=|t|^{-1/y_t}$ so the transformed argument is order one:

$$
\boxed{\xi\propto|t|^{-\nu}},\qquad \nu=\frac1{y_t}.
$$

## Quantum-field connection

In QFT, changing the renormalization scale changes couplings while physical observables remain scale-consistent. Ultraviolet divergences are one technical entry point; the deeper content is that effective descriptions live on scale-dependent theory space.

## Boundaries of the analogy to compression

RG is not arbitrary information loss. Locality, symmetry, scale composition, and preservation of selected long-distance observables constrain the map.

## Connected notes

[[Renormalization Group]] · [[Critical Phenomena]] · [[Effective Field Theory]] · [[Theory Space]] · [[Renormalization as Compression Across Scales]]

## Navigation

[[Derivation Atlas]] · [[Physics Worldmap]]
