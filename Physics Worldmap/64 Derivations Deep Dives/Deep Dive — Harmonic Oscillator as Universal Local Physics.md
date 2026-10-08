---
title: "Deep Dive — Harmonic Oscillator as Universal Local Physics"
type: derivation
field: "Classical Mechanics"
epistemic_status: established
level: intermediate
tags: [physics, derivation, deep-dive]
created: 2026-07-30
updated: 2026-07-30
note_maturity: worked-derivation
source_audit: canonical-derivation-needs-citation-audit
---

# Deep Dive — Harmonic Oscillator as Universal Local Physics

## Why it recurs

Let a one-dimensional system have a smooth, nondegenerate stable equilibrium at $x_0$. Expand its potential:

$$
V(x_0+\xi)=V(x_0)+V'(x_0)\xi+\frac12V''(x_0)\xi^2+O(\xi^3).
$$

At a nondegenerate stable equilibrium, $V'(x_0)=0$ and $k=V''(x_0)>0$. To leading order,

$$m\ddot\xi+k\xi=0,\qquad \omega_0=\sqrt{k/m}.$$

The oscillator is universal because every smooth **nondegenerate** stable minimum looks quadratic sufficiently close to equilibrium. A degenerate minimum such as $V\propto x^4$ has $V''(0)=0$ and is governed by its leading nonzero higher-order term instead.

## Three representations

### Time-domain trajectory

$$\xi(t)=A\cos(\omega_0t+\phi).$$

### Phase space

With $p=m\dot\xi$,

$$H=\frac{p^2}{2m}+\frac12m\omega_0^2\xi^2=E,$$

so constant-energy trajectories are ellipses. Hamiltonian flow preserves their enclosed phase-space area.

### Complex amplitude

$$z=\xi+i\frac{\dot\xi}{\omega_0},\qquad \dot z=-i\omega_0z.$$

Time evolution is a rotation. This representation anticipates Fourier modes, ladder operators, and normal-mode amplitudes.

## Driven and damped response

For

$$\ddot x+2\gamma\dot x+\omega_0^2x=\frac{F_0}{m}\cos\omega t,$$

the steady-state complex susceptibility is

$$\chi(\omega)=\frac{1/m}{\omega_0^2-\omega^2-2i\gamma\omega}.$$

Its real and imaginary parts encode dispersion and dissipation. Resonance position, linewidth, ringdown time, and phase lag are different views of the same poles.

## Limits

Large amplitude exposes anharmonic terms, mode coupling, frequency shift, bistability, or chaos. Degenerate equilibria with vanishing quadratic curvature are not harmonic even at leading order. Quantum mechanics replaces continuous energy with $E_n=\hbar\omega_0(n+\tfrac12)$ while retaining the same algebraic core for a quadratic potential.

## Connected notes

[[Oscillations]] · [[Damping and Driven Oscillators]] · [[Coupled Oscillators and Normal Modes]] · [[Quantum Harmonic Oscillator]] · [[Linear Response Theory]]

## Navigation

[[Derivation Atlas]] · [[Physics Worldmap]]
