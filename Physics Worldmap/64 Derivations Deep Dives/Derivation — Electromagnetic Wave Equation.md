---
title: "Derivation — Electromagnetic Wave Equation"
type: derivation
field: "Electromagnetism"
epistemic_status: established
level: intermediate
tags: [physics, derivation, deep-dive]
created: 2026-07-30
updated: 2026-07-30
note_maturity: worked-derivation
source_audit: canonical-derivation-needs-citation-audit
---

# Derivation — Electromagnetic Wave Equation

## Target

Derive vacuum electromagnetic waves from Maxwell's equations.

## Source-free region

Set $\rho=0$ and $\mathbf J=0$:

$$
\nabla\cdot\mathbf E=0,\quad
\nabla\cdot\mathbf B=0,\quad
\nabla\times\mathbf E=-\partial_t\mathbf B,\quad
\nabla\times\mathbf B=\mu_0\epsilon_0\partial_t\mathbf E.
$$

Take the curl of Faraday's law:

$$
\nabla\times(\nabla\times\mathbf E)
=-\partial_t(\nabla\times\mathbf B)
=-\mu_0\epsilon_0\partial_t^2\mathbf E.
$$

Use

$$\nabla\times(\nabla\times\mathbf E)=\nabla(\nabla\cdot\mathbf E)-\nabla^2\mathbf E=-\nabla^2\mathbf E.$$

Thus

$$
\boxed{\nabla^2\mathbf E-\mu_0\epsilon_0\partial_t^2\mathbf E=0.}
$$

The same steps give

$$
\boxed{\nabla^2\mathbf B-\mu_0\epsilon_0\partial_t^2\mathbf B=0.}
$$

The propagation speed is

$$c=\frac1{\sqrt{\mu_0\epsilon_0}}.$$

## Plane-wave constraints

For $\mathbf E=\mathbf E_0e^{i(\mathbf k\cdot\mathbf r-\omega t)}$,

$$\omega=c|\mathbf k|,\qquad \mathbf k\cdot\mathbf E_0=0.$$

Faraday's law gives

$$\mathbf B_0=\frac1\omega\mathbf k\times\mathbf E_0,$$

so $\mathbf E$, $\mathbf B$, and $\mathbf k$ are mutually transverse in a vacuum plane wave.

## What changes in matter

Polarization, magnetization, conductivity, dispersion, absorption, nonlinearity, and spatial nonlocality alter the constitutive relations. Maxwell's equations remain, but the simple wave speed and transverse structure need not.

## Connected notes

[[Maxwell Equations]] · [[Electromagnetic Waves]] · [[Dispersion Relations]] · [[Poynting Theorem]]

## Navigation

[[Derivation Atlas]] · [[Physics Worldmap]]
