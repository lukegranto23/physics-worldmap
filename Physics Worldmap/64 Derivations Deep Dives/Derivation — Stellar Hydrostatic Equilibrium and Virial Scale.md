---
title: "Derivation — Stellar Hydrostatic Equilibrium and Virial Scale"
type: derivation
field: "Astrophysics"
epistemic_status: established
level: intermediate
tags: [physics, derivation, deep-dive]
created: 2026-07-30
updated: 2026-07-30
note_maturity: worked-derivation
source_audit: canonical-derivation-needs-citation-audit
---

# Derivation — Stellar Hydrostatic Equilibrium and Virial Scale

## Hydrostatic equilibrium

Consider a spherical shell of radius $r$, thickness $dr$, density $\rho$, and enclosed mass $m(r)$. Pressure forces across the shell balance gravity:

$$
\boxed{\frac{dP}{dr}=-\frac{Gm(r)\rho(r)}{r^2}}.
$$

Mass continuity is

$$
\boxed{\frac{dm}{dr}=4\pi r^2\rho(r)}.
$$

An equation of state and energy-transport/generation equations are needed to close stellar structure.

## Order-of-magnitude central pressure

Take $m\sim M$, $\rho\sim M/R^3$, and $dP/dr\sim P_c/R$:

$$
P_c\sim\frac{GM^2}{R^4}.
$$

For an ideal-gas-supported star, $P\sim\rho k_BT/(\mu m_p)$, so

$$
k_BT_c\sim\frac{GM\mu m_p}{R}.
$$

This is the virial temperature scale.

## Virial theorem

For a bound self-gravitating idealized star in equilibrium,

$$2K+U=0.$$

Total energy $E=K+U=U/2=-K<0$. If the star loses energy, it can heat up as it contracts: a negative heat-capacity behavior of self-gravitating systems.

## Failure and extensions

Radiation pressure, degeneracy, rotation, magnetic fields, relativistic structure, mass loss, convection, and composition gradients matter in different stars. Compact stars require the Tolman-Oppenheimer-Volkoff equation rather than Newtonian balance.

## Connected notes

[[Stellar Structure Equations]] · [[Virial Theorem]] · [[Stellar Evolution]] · [[White Dwarfs]] · [[Neutron Stars]]

## Navigation

[[Derivation Atlas]] · [[Physics Worldmap]]
