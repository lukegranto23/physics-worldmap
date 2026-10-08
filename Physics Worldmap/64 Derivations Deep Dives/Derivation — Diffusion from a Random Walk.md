---
title: "Derivation — Diffusion from a Random Walk"
type: derivation
field: "Statistical Physics"
epistemic_status: established
level: introductory
tags: [physics, derivation, deep-dive]
created: 2026-07-30
updated: 2026-07-30
note_maturity: worked-derivation
source_audit: canonical-derivation-needs-citation-audit
---

# Derivation — Diffusion from a Random Walk

## Discrete walk

On a one-dimensional lattice with spacing $a$, a walker steps left or right with equal probability every time interval $\tau$:

$$
P_j^{n+1}=\frac12P_{j-1}^n+\frac12P_{j+1}^n.
$$

Write $P_j^n\approx a\,p(x_j,t_n)$ and expand:

$$
p(x,t+\tau)
=p(x,t)+\tau\partial_tp+O(\tau^2),
$$

$$
\frac12[p(x-a,t)+p(x+a,t)]
=p(x,t)+\frac{a^2}{2}\partial_x^2p+O(a^4).
$$

Equating and taking $a,\tau\to0$ while holding

$$D=\frac{a^2}{2\tau}$$

fixed gives

$$\boxed{\partial_tp=D\partial_x^2p.}$$

## Fundamental solution

For an initially localized particle,

$$
p(x,t)=\frac1{\sqrt{4\pi Dt}}
\exp\left(-\frac{x^2}{4Dt}\right).
$$

The mean remains zero and

$$\boxed{\langle x^2\rangle=2Dt.}$$

In $d$ independent spatial dimensions, $\langle r^2\rangle=2dDt$.

## What the limit hides

The diffusion equation has instantaneous nonzero tails, an artifact of the parabolic continuum limit. At short times inertia, finite propagation, persistent steps, correlations, boundaries, drift, reactions, and heterogeneous media matter.

## Connected notes

[[Random Walks and Diffusion]] · [[Brownian Motion]] · [[Fokker Planck Equation]] · [[Diffusion Limited Processes]] · [[Computational Lab Index]]

## Navigation

[[Derivation Atlas]] · [[Physics Worldmap]]
