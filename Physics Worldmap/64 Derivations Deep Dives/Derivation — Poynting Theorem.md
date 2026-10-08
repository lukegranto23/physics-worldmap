---
title: "Derivation — Poynting Theorem"
type: derivation
field: "Electromagnetism"
epistemic_status: established
level: advanced
tags: [physics, derivation, deep-dive]
created: 2026-07-30
updated: 2026-07-30
note_maturity: worked-derivation
source_audit: canonical-derivation-needs-citation-audit
---

# Derivation — Poynting Theorem

## Target

Derive local energy conservation for electromagnetic fields and charged matter.

Start with Ampere-Maxwell and Faraday:

$$
\nabla\times\mathbf B=\mu_0\mathbf J+\mu_0\epsilon_0\partial_t\mathbf E,
\qquad
\nabla\times\mathbf E=-\partial_t\mathbf B.
$$

Dot the first with $\mathbf E/\mu_0$ and the second with $\mathbf B/\mu_0$, then use

$$
\nabla\cdot(\mathbf E\times\mathbf B)
=\mathbf B\cdot(\nabla\times\mathbf E)
-\mathbf E\cdot(\nabla\times\mathbf B).
$$

Rearrangement gives

$$
\frac{\partial}{\partial t}
\left(
\frac{\epsilon_0E^2}{2}+\frac{B^2}{2\mu_0}
\right)
+\nabla\cdot\left(\frac{\mathbf E\times\mathbf B}{\mu_0}\right)
=-\mathbf J\cdot\mathbf E.
$$

Define field energy density

$$u_{\rm EM}=\frac{\epsilon_0E^2}{2}+\frac{B^2}{2\mu_0}$$

and Poynting vector

$$\mathbf S=\frac1{\mu_0}\mathbf E\times\mathbf B.$$

Then

$$\boxed{\partial_tu_{\rm EM}+\nabla\cdot\mathbf S=-\mathbf J\cdot\mathbf E.}$$

The right side is the rate per volume at which fields do work on charge. When matter's mechanical and internal energy balance is included, total energy is locally conserved.

## Integral form

$$
\frac d{dt}\int_Vu_{\rm EM}dV
=-\oint_{\partial V}\mathbf S\cdot d\mathbf A
-\int_V\mathbf J\cdot\mathbf E\,dV.
$$

Energy in a volume changes because energy flows through its boundary or is transferred to matter.

## Interpretive caution

Energy density and flux can be rearranged by convention in material media, while the total conservation statement and measurable transfer remain. In circuits, energy often flows through surrounding fields rather than “inside the wire” in a naive particle-only picture.

## Connected notes

[[Poynting Theorem]] · [[Electromagnetic Momentum]] · [[Conservation Laws]] · [[Theory Experiment Computation Loop]]

## Navigation

[[Derivation Atlas]] · [[Physics Worldmap]]
