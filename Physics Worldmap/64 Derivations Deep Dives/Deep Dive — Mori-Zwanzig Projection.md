---
type: deep-dive
field: Statistical Physics
epistemic_status: established
level: advanced
tags: [physics, derivation, coarse-graining, memory]
created: 2026-07-30
updated: 2026-07-30
---

# Mori-Zwanzig Projection

## Purpose

Projection-operator methods derive an exact equation for selected resolved variables while exposing how unresolved variables return as memory and fluctuating forcing.

Let the full dynamics act on observables through a Liouville operator $L$:

$$\frac d{dt}A(t)=LA(t),\qquad A(t)=e^{tL}A(0).$$

Choose a projection $P$ onto functions of resolved variables and let $Q=1-P$. The Dyson identity separates resolved and orthogonal evolution. Applied to the resolved dynamics, it yields the generalized Langevin structure

$$
\frac d{dt}PA(t)
=PLPA(t)
+\int_0^tPL\,e^{(t-s)QL}QL\,PA(s)\,ds
+PL\,e^{tQL}QA(0).
$$

Schematically:

$$
\boxed{\dot Z(t)=F[Z(t)]+\int_0^tK(t-s;Z(s))\,ds+\eta(t).}
$$

## Meaning of the terms

- **drift $F$:** instantaneous projected dynamics;
- **memory kernel $K$:** delayed feedback carried through unresolved degrees of freedom;
- **orthogonal force $\eta$:** dependence on unresolved initial conditions and dynamics.

The formula is exact for a specified projection. Approximation enters when the drift, memory, or noise is truncated or modeled.

## Equilibrium relation

For suitable equilibrium projections, noise correlations and memory are related by a fluctuation-dissipation relation. Away from equilibrium, with nonlinear projections, or under finite-data inference, that relation may change or fail.

## Practical tests for a Markov closure

1. residuals are uncorrelated beyond the resolved time step;
2. held-out impulse responses are reproduced;
3. increasing resolved dimension shrinks inferred memory;
4. conservation and stationary statistics remain correct;
5. prediction error is stable when the observation interval changes.

## Connected notes

[[Renormalization Group|Coarse-graining]] · [[Open Quantum Systems]] · [[Langevin Equation]] · [[Linear Response Theory]] · [[Synthesis Session 001 — Response-Preserving Coarse-Graining]] · [[Derivation Atlas]]
