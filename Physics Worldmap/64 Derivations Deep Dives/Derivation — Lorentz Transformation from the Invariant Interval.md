---
title: "Derivation — Lorentz Transformation from the Invariant Interval"
type: derivation
field: "Relativity and Gravitation"
epistemic_status: established
level: intermediate
tags: [physics, derivation, deep-dive]
created: 2026-07-30
updated: 2026-07-30
note_maturity: worked-derivation
source_audit: canonical-derivation-needs-citation-audit
---

# Derivation — Lorentz Transformation from the Invariant Interval

## Target

Find the linear transformation between inertial coordinates that preserves the spacetime interval.

Consider one spatial dimension and define $x^\mu=(ct,x)$. Homogeneity makes the transformation between inertial frames linear. Require

$$-(ct')^2+x'^2=-(ct)^2+x^2.$$

A hyperbolic rotation satisfies this automatically:

$$
\begin{pmatrix}ct'\\x'\end{pmatrix}
=
\begin{pmatrix}
\cosh\eta&-\sinh\eta\\
-\sinh\eta&\cosh\eta
\end{pmatrix}
\begin{pmatrix}ct\\x\end{pmatrix}.
$$

The origin of the primed frame follows $x=vt$ and has $x'=0$:

$$0=-ct\sinh\eta+vt\cosh\eta,$$

so $\tanh\eta=v/c\equiv\beta$. Then

$$\cosh\eta=\gamma=\frac1{\sqrt{1-\beta^2}},\qquad \sinh\eta=\gamma\beta.$$

Therefore

$$
\boxed{x'=\gamma(x-vt),\qquad
t'=\gamma\left(t-\frac{vx}{c^2}\right).}
$$

## Immediate consequences

- Light rays $x=\pm ct$ remain light rays.
- Events at the same place in one frame but separated by proper time obey $\Delta t=\gamma\Delta\tau$.
- Simultaneous separated events transform with $\Delta t'=-\gamma v\Delta x/c^2$.
- Rapidity adds linearly, which gives the relativistic velocity-addition rule.

## Do not say

“Moving clocks physically malfunction.” A clock records proper time along its worldline. Coordinate-time comparisons depend on the paths and reunion events being compared.

## Connected notes

[[Lorentz Transformations]] · [[Spacetime Events and Intervals]] · [[Time Dilation]] · [[Relativity of Simultaneity]] · [[Four Vectors]]

## Navigation

[[Derivation Atlas]] · [[Physics Worldmap]]
