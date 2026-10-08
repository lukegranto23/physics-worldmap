---
title: "Derivation — Navier-Stokes Nondimensionalization"
type: derivation
field: "Fluid Dynamics"
epistemic_status: established
level: intermediate
tags: [physics, derivation, deep-dive]
created: 2026-07-30
updated: 2026-07-30
note_maturity: worked-derivation
source_audit: canonical-derivation-needs-citation-audit
---

# Derivation — Navier-Stokes Nondimensionalization

## Starting equation

For an incompressible Newtonian fluid,

$$
\rho(\partial_t\mathbf u+\mathbf u\cdot\nabla\mathbf u)
=-\nabla p+\mu\nabla^2\mathbf u+\rho\mathbf f,
\qquad\nabla\cdot\mathbf u=0.
$$

Choose characteristic length $L$, speed $U$, time $L/U$, and dynamic pressure $\rho U^2$:

$$
\mathbf x=L\mathbf x^*,\quad
t=\frac LU t^*,\quad
\mathbf u=U\mathbf u^*,\quad
p=\rho U^2p^*.
$$

Substitution and division by $\rho U^2/L$ gives

$$
\partial_{t^*}\mathbf u^*
+\mathbf u^*\cdot\nabla^*\mathbf u^*
=-\nabla^*p^*
+\frac1{Re}\nabla^{*2}\mathbf u^*
+\mathbf f^*,
$$

where

$$\boxed{Re=\frac{\rho UL}{\mu}=\frac{UL}{\nu}.}$$

## Interpretation

$Re$ compares inertial advection with viscous diffusion:

$$
\frac{\text{inertia}}{\text{viscosity}}
\sim
\frac{\rho U^2/L}{\mu U/L^2}
=Re.
$$

- $Re\ll1$: Stokes flow, reversible linear equations in the ideal limit, no inertial wake.
- $Re\gg1$: viscosity may be small in the bulk but remains decisive in boundary layers, dissipation scales, and topology change.

## Singular limit warning

Setting $1/Re=0$ everywhere can destroy the no-slip boundary condition. Thin boundary layers reconcile an inviscid outer solution with viscous walls. “Small coefficient” does not imply “small effect” when it multiplies the highest derivative.

## Connected notes

[[Navier Stokes Equations]] · [[Reynolds Number]] · [[Boundary Layers]] · [[Turbulence]] · [[Dimensional Analysis in Fluids]]

## Navigation

[[Derivation Atlas]] · [[Physics Worldmap]]
