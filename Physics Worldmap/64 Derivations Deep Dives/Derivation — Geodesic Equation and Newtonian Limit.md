---
title: "Derivation — Geodesic Equation and Newtonian Limit"
type: derivation
field: "Relativity and Gravitation"
epistemic_status: established
level: advanced
tags: [physics, derivation, deep-dive]
created: 2026-07-30
updated: 2026-07-30
note_maturity: worked-derivation
source_audit: canonical-derivation-needs-citation-audit
---

# Derivation — Geodesic Equation and Newtonian Limit

## Geodesic equation from proper time

For a massive free particle, extremize

$$S=-mc\int ds.$$

An equivalent affine-parameter Lagrangian is

$$L=\frac12g_{\mu\nu}(x)\dot x^\mu\dot x^\nu.$$

Applying the Euler-Lagrange equation and combining metric derivatives gives

$$
\boxed{
\ddot x^\rho+\Gamma^\rho_{\mu\nu}\dot x^\mu\dot x^\nu=0
}
$$

with

$$
\Gamma^\rho_{\mu\nu}
=\frac12g^{\rho\sigma}
(\partial_\mu g_{\sigma\nu}+\partial_\nu g_{\sigma\mu}-\partial_\sigma g_{\mu\nu}).
$$

The connection coefficients can vanish at one point in a freely falling coordinate system; curvature, built from derivatives and products of connections, cannot generally be removed over a region.

## Newtonian weak-field limit

Assume:

- slow motion $|\mathbf v|\ll c$;
- a stationary weak field;
- metric component $g_{00}\approx-(1+2\Phi/c^2)$;
- spatial metric approximately Euclidean.

The dominant spatial geodesic term is

$$\frac{d^2x^i}{dt^2}\approx-c^2\Gamma^i_{00}.$$

To first order,

$$\Gamma^i_{00}\approx\frac1{c^2}\partial_i\Phi,$$

so

$$\boxed{\ddot{\mathbf x}=-\nabla\Phi.}$$

Einstein's equation reduces to $\nabla^2\Phi=4\pi G\rho$ under the same regime, recovering Newtonian gravity.

## Lesson

The correspondence is a controlled limit, not an assertion that gravity is “just a force” or “just curvature” in every calculation. Different representations are useful at different scales.

## Connected notes

[[Metric and Proper Time]] · [[Covariant Derivatives and Connection]] · [[Curvature]] · [[Einstein Field Equations]] · [[Correspondence Principle]]

## Navigation

[[Derivation Atlas]] · [[Physics Worldmap]]
