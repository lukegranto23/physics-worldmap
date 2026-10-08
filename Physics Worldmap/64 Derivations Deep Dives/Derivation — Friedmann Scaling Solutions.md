---
title: "Derivation — Friedmann Scaling Solutions"
type: derivation
field: "Cosmology"
epistemic_status: established
level: intermediate
tags: [physics, derivation, deep-dive]
created: 2026-07-30
updated: 2026-07-30
note_maturity: worked-derivation
source_audit: canonical-derivation-needs-citation-audit
---

# Derivation — Friedmann Scaling Solutions

## Energy-density scaling

For a homogeneous component with equation of state

$$p=w\rho c^2,$$

the continuity equation is

$$\dot\rho+3H(\rho+p/c^2)=0.$$

Using $H=\dot a/a$,

$$
\frac{\dot\rho}{\rho}=-3(1+w)\frac{\dot a}{a}.
$$

Integrate:

$$\boxed{\rho(a)\propto a^{-3(1+w)}.}$$

Important cases:

- nonrelativistic matter, $w=0$: $\rho_m\propto a^{-3}$;
- radiation, $w=1/3$: $\rho_r\propto a^{-4}$, with one extra factor from photon redshift;
- cosmological constant, $w=-1$: $\rho_\Lambda=\text{constant}$.

## Flat single-component expansion

For $k=0$ and no cosmological constant other than the component,

$$H^2=\frac{8\pi G}{3}\rho\propto a^{-3(1+w)}.$$

Therefore

$$\dot a\propto a^{-(1+3w)/2}.$$

For $w\ne-1$, integration gives

$$\boxed{a(t)\propto t^{2/[3(1+w)]}.}$$

Thus radiation domination has $a\propto t^{1/2}$ and matter domination $a\propto t^{2/3}$. A pure positive cosmological constant gives

$$a(t)\propto e^{H_\Lambda t}.$$

## Acceleration condition

The acceleration equation gives

$$
\frac{\ddot a}{a}
=-\frac{4\pi G}{3}\rho(1+3w).
$$

Positive-density expansion accelerates when $w<-1/3$.

## Limits

Real cosmology contains multiple components, perturbations, transitions, curvature constraints, neutrino effects, and inferred parameters. These power laws are regime solutions, not a full data analysis.

## Connected notes

[[Friedmann Equations]] · [[Cosmic Expansion]] · [[Thermal History of the Universe]] · [[Dark Energy]] · [[Computational Lab Index]]

## Navigation

[[Derivation Atlas]] · [[Physics Worldmap]]
