---
type: "concept"
field: "Classical Mechanics"
epistemic_status: "established"
level: "advanced"
tags: ["physics", "field/mechanics", "status/established", "level/advanced"]
aliases: []
created: 2026-07-30
updated: 2026-09-04
note_maturity: expanded
source_audit: bibliography-present-needs-claim-audit
---

# Liouvilles Theorem

> [!summary] Core idea
> Hamiltonian evolution preserves canonical phase-space volume. A probability density carried by that flow remains constant along trajectories, even while its shape stretches and folds.

## Derivation from Hamilton's equations

In $z=(q^i,p_i)$ coordinates and for a twice-differentiable Hamiltonian,
$$
\nabla_z\cdot\dot z
=\sum_i\left(\frac{\partial^2H}{\partial q^i\partial p_i}
-\frac{\partial^2H}{\partial p_i\partial q^i}\right)=0.
$$
For the flow Jacobian $M(t)=\partial z(t)/\partial z(0)$,
$$
\frac{d}{dt}\ln\det M=\nabla_z\cdot\dot z=0,\qquad \det M(0)=1.
$$
Hence $\det M(t)=1$. Explicit time dependence in $H$ does not spoil this argument. Energy conservation is a separate issue.

## Probability transport

Probability conservation is
$\partial_t\rho+\nabla_z\cdot(\rho\dot z)=0$.
Combining it with zero divergence yields
$$
\partial_t\rho+\{\rho,H\}=0,\qquad
\frac{d\rho(z(t),t)}{dt}=0.
$$
A stationary density additionally obeys $\{\rho,H\}=0$. A moving nonequilibrium distribution need not satisfy that extra condition.

For noncanonical coordinates the invariant volume measure may carry a Jacobian. “Volume preservation” does not mean the ordinary coordinate-box volume is invariant in every arbitrary parameterization.

## Numerical example: oscillator integrators

For a unit-mass, unit-frequency oscillator, explicit Euler gives
$$
\begin{pmatrix}q'\\p'\end{pmatrix}
=\begin{pmatrix}1&h\\-h&1\end{pmatrix}
\begin{pmatrix}q\\p\end{pmatrix},\qquad\det M_E=1+h^2.
$$
At $h=0.1$, a phase-space patch grows by $1.01^{100}=2.7048$ after 100 steps. This is numerical expansion, not physical entropy production.

A kick-then-drift symplectic Euler step is
$$
p'=p-hq,\qquad q'=q+hp',\qquad
M_S=\begin{pmatrix}1-h^2&h\\-h&1\end{pmatrix}.
$$
Its determinant is exactly one. For this oscillator it is linearly stable for $0<h<2$; area preservation alone does not guarantee stability or accurate phase.

## Dissipative counterexample

For $\dot q=p/m$, $\dot p=-kq-\gamma p$, phase-space divergence is $-\gamma$ and an area element shrinks as $e^{-\gamma t}$. This reduced damped model is not a canonical closed Hamiltonian flow in $(q,p)$. A larger system including the environment may still evolve Hamiltonianly.

## Entropy bridge—and its missing assumptions

With a fixed invariant reference measure and suitable boundary behavior,
$$
S_{\rm fine}=-k_B\int\rho\ln\rho\,d\mu
$$
is constant under Hamiltonian flow. This does not show that thermodynamic entropy never increases. Coarse-graining, subsystem restriction, special initial conditions, and operational resolution alter the description. Replacing a fine density by cell averages increases its entropy at that instant by concavity, but does not guarantee monotonic increase at every future time in a finite closed system.

See [[Gibbs Entropy]] for an explicit coarse-graining calculation.

## Sources and recall

[Tong, Classical Dynamics §4.2](https://davidtong.org/teaching/classical-dynamics/dynhtml/S4) is the canonical reference for the invariant-volume and continuity-equation statements. The integrator counterexample is reproduced in [[Mechanics to Statistical Physics — Foundation Study Route]].

Explain why time-dependent $H$ can preserve volume while changing energy. Compare a density moving with the flow to a density stationary at fixed coordinates.

## Navigation

[[Hamiltonian Mechanics]] · [[Phase Space]] · [[Poisson Brackets]] · [[Gibbs Entropy]] · [[Classical Mechanics Map]] · [[Physics Worldmap]]
