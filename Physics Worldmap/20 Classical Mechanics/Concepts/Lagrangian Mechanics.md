---
type: "concept"
field: "Classical Mechanics"
epistemic_status: "established"
level: "intermediate"
tags: ["physics", "field/mechanics", "status/established", "level/intermediate"]
aliases: []
created: 2026-07-30
updated: 2026-09-04
note_maturity: expanded
source_audit: bibliography-present-needs-claim-audit
---

# Lagrangian Mechanics

> [!summary] Core idea
> Specify a scalar function of configuration and velocity, vary its time integral, and obtain equations valid in generalized coordinates. The stationary-action principle concerns an entire trial path; it does not mean a particle consciously chooses a future.

## Objects, units, and assumptions

Let $q^i(t)$ be independent coordinates and $L(q,\dot q,t)$ the Lagrangian. Its units are energy; the action $\mathcal A=\int_{t_a}^{t_b}L\,dt$ has units J s. For ordinary conservative particles, $L=T-V$. Velocity-dependent interactions require a more general expression.

The elementary derivation assumes differentiable paths and $L$, fixed endpoint times and positions, and admissible variations respecting the chosen configuration space. Holonomic ideal constraints can be eliminated by coordinates. General nonholonomic constraints require additional care.

## Derivation to reconstruct

For $q^i\mapsto q^i+\epsilon\eta^i$ with $\eta^i(t_a)=\eta^i(t_b)=0$,
$$
\delta\mathcal A=\int\left(\frac{\partial L}{\partial q^i}\eta^i+
\frac{\partial L}{\partial\dot q^i}\dot\eta^i\right)dt
=\int\left[\frac{\partial L}{\partial q^i}
-\frac{d}{dt}\frac{\partial L}{\partial\dot q^i}\right]\eta^i\,dt.
$$
Arbitrary interior variations imply the Euler–Lagrange equations:
$$
\frac{d}{dt}\frac{\partial L}{\partial\dot q^i}
-\frac{\partial L}{\partial q^i}=0.
$$
The integration-by-parts boundary term vanishes because of the endpoint condition—not because momentum vanishes. See [[Derivation — Euler-Lagrange Equations]].

## Worked example: a vertical pendulum

For a mass $m$ on a rigid massless rod of length $\ell$, with $\theta$ measured from downward vertical,
$$
L=\tfrac12m\ell^2\dot\theta^2-mg\ell(1-\cos\theta).
$$
Hence $m\ell^2\ddot\theta+mg\ell\sin\theta=0$. Both terms have units of torque. Only after deriving the exact equation do we approximate $\sin\theta\simeq\theta$.

At $\ell=0.75$ m and $g=9.81$ m s$^{-2}$, $\omega_0=\sqrt{g/\ell}=3.6166$ s$^{-1}$ and the small-amplitude period is $1.7373$ s. The mass cancels. The relative leading finite-amplitude correction is $\theta_0^2/16$: about $0.0625\%$ at $\theta_0=0.10$ rad. Air drag, rod flexure, and pivot friction are excluded.

## Why “stationary,” not always “least”

For the unit oscillator $L=(\dot q^2-q^2)/2$, the path $q=0$ with zero endpoints has quadratic action change
$$
\mathcal A[\epsilon\sin(n\pi t/T)]-\mathcal A[0]
=\frac{\epsilon^2T}{4}\left[(n\pi/T)^2-1\right].
$$
If $T>\pi$, the $n=1$ direction lowers the action while sufficiently large $n$ raises it. The physical path is a saddle. This explicit counterexample is checked in [[Mechanics to Statistical Physics — Foundation Study Route]].

## Gauge freedom and failure modes

Adding $dF(q,t)/dt$ changes the action only by endpoint data and leaves these equations unchanged. It can shift canonical momentum and the Hamiltonian representation.

Dissipation does not generally fit a simple closed-system $T-V$ model. A generalized force or enlarged system may be needed. Choosing coordinates that already impose a nonholonomic velocity constraint and varying as though they were independent can produce incorrect equations.

## Sources and recall

Targeted reference check: [Tong, Classical Dynamics §2.1–2.3](https://davidtong.org/teaching/classical-dynamics/dynhtml/S2). This note's numerical examples and counterexample are explicitly reconstructed here; a full claim-level audit is still pending.

Without looking: derive the pendulum equation, identify the discarded boundary term, and explain why $L+dF/dt$ has the same dynamics.

## Navigation

[[Classical Mechanics Map]] · [[Constraints and Generalized Coordinates]] · [[Noethers Theorem in Mechanics]] · [[Hamiltonian Mechanics]] · [[Mechanics to Statistical Physics — Foundation Study Route]] · [[Physics Worldmap]]
