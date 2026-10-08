---
title: "Derivation — Plasma Oscillation and Debye Length"
type: derivation
field: "Plasma Physics"
epistemic_status: established
level: intermediate
tags: [physics, derivation, deep-dive]
created: 2026-07-30
updated: 2026-07-30
note_maturity: worked-derivation
source_audit: canonical-derivation-needs-citation-audit
---

# Derivation — Plasma Oscillation and Debye Length

## Electron plasma oscillation

Treat ions as a fixed uniform background and displace the electron fluid by a small distance $x$. A slab displacement produces charge separation and an electric restoring field. Equivalently combine linearized electron momentum,

$$m_e\partial_t\mathbf u_e=-e\mathbf E,$$

continuity,

$$\partial_t n_1+n_0\nabla\cdot\mathbf u_e=0,$$

and Poisson,

$$\nabla\cdot\mathbf E=-\frac{e n_1}{\epsilon_0}.$$

Differentiate continuity in time and substitute:

$$
\partial_t^2n_1+\frac{n_0e^2}{m_e\epsilon_0}n_1=0.
$$

Thus

$$\boxed{\omega_{pe}=\sqrt{\frac{n_0e^2}{m_e\epsilon_0}}.}$$

## Debye screening

For a weak electrostatic potential in an isothermal equilibrium electron population,

$$n_e\simeq n_0e^{e\phi/(k_BT_e)}
\approx n_0\left(1+\frac{e\phi}{k_BT_e}\right).
$$

Poisson's equation around a test charge becomes

$$
(\nabla^2-\lambda_D^{-2})\phi
=-\frac{q\delta(\mathbf r)}{\epsilon_0},
$$

with

$$\boxed{\lambda_D=\sqrt{\frac{\epsilon_0k_BT_e}{n_0e^2}}.}$$

The screened potential is Yukawa-like:

$$\phi(r)=\frac{q}{4\pi\epsilon_0r}e^{-r/\lambda_D}.$$

## Assumptions

Small potential, near-Maxwellian equilibrium response, suitable scale separation, and weak coupling. Strongly coupled, magnetized, flowing, quantum-degenerate, or nonneutral plasmas require modification.

## Connected notes

[[Plasma Frequency]] · [[Debye Screening]] · [[Quasineutrality]] · [[Vlasov Equation]]

## Navigation

[[Derivation Atlas]] · [[Physics Worldmap]]
