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

# Hamiltonian Mechanics

> [!summary] Core idea
> A regular Legendre transformation replaces velocities with canonical momenta. Dynamics then becomes a first-order flow preserving symplectic structure.

## From Lagrangian to Hamiltonian

Define $p_i=\partial L/\partial\dot q^i$. If the velocity Hessian
$W_{ij}=\partial^2L/(\partial\dot q^i\partial\dot q^j)$ is nonsingular locally, solve for $\dot q(q,p,t)$ and set
$$
H(q,p,t)=p_i\dot q^i-L.
$$
Taking a differential and cancelling $p_i\,d\dot q^i$ gives
$$
dH=\dot q^i\,dp_i-\frac{\partial L}{\partial q^i}dq^i
-\frac{\partial L}{\partial t}dt.
$$
Using Euler–Lagrange yields
$$
\dot q^i=\frac{\partial H}{\partial p_i},\qquad
\dot p_i=-\frac{\partial H}{\partial q^i},\qquad
\frac{\partial H}{\partial t}=-\frac{\partial L}{\partial t}.
$$
Partial derivatives hold the appropriate independent variables fixed. A singular Hessian signals constraints; it is not permission to invert a zero matrix.

## Worked example and units

For $L=\tfrac12m\dot q^2-\tfrac12kq^2$,
$$
p=m\dot q,\qquad H=\frac{p^2}{2m}+\frac{kq^2}{2}.
$$
With $m=2$ kg, $k=18$ N m$^{-1}$, $q_0=0.10$ m, and $p_0=0.60$ kg m s$^{-1}$, the energy is $0.18$ J and $\omega=3$ s$^{-1}$.

The exact solution is
$$
q(t)=q_0\cos\omega t+\frac{p_0}{m\omega}\sin\omega t,\quad
p(t)=p_0\cos\omega t-m\omega q_0\sin\omega t.
$$
It separately satisfies both first-order equations. A numerical solver should reproduce phase as well as energy: a trajectory may conserve a modified energy while accumulating timing error.

## Poisson brackets and symplectic flow

Using $\{f,g\}=\partial_{q^i}f\,\partial_{p_i}g-\partial_{p_i}f\,\partial_{q^i}g$,
$$
\frac{df}{dt}=\{f,H\}+\partial_t f.
$$
In canonical coordinates, $\dot z=J\nabla H$ with
$J=\begin{pmatrix}0&I\\-I&0\end{pmatrix}$.
The exact flow Jacobian $M$ obeys $M^TJM=J$ and therefore preserves volume. In more than one degree of freedom, preserving volume alone does not guarantee symplecticity.

## Counterexample: canonical momentum is not always mechanical momentum

For a charge $e$ in electromagnetic potentials in SI units,
$$
L=\tfrac12m v^2+e\mathbf A\cdot\mathbf v-e\phi,\quad
\mathbf p=m\mathbf v+e\mathbf A,\quad
H=\frac{|\mathbf p-e\mathbf A|^2}{2m}+e\phi.
$$
The canonical momentum depends on gauge. Equating it automatically with $m\mathbf v$ loses the magnetic interaction.

Likewise, a Hamiltonian in time-dependent coordinates need not be the laboratory energy. Conservation follows from $\partial_tH=0$ in the chosen canonical description, not merely from naming a function “Hamiltonian.”

## What this solves—and does not

It supplies an equivalent local formulation for regular mechanical systems, powerful conservation tests, and structure-preserving numerical methods. It does not make a generic many-body trajectory analytically solvable, establish ergodicity, or eliminate chaos.

## Sources and recall

Targeted reference: [Tong, Classical Dynamics §4.1 and §4.3](https://davidtong.org/teaching/classical-dynamics/dynhtml/S4). The numerical oscillator and Jacobian checks are bundled in [[Mechanics to Statistical Physics — Foundation Study Route]].

Derive the Legendre differential, distinguish canonical from mechanical momentum, and construct a time-dependent $H$ whose flow still preserves volume.

## Navigation

[[Lagrangian Mechanics]] · [[Poisson Brackets]] · [[Phase Space]] · [[Liouvilles Theorem]] · [[Classical Mechanics Map]] · [[Physics Worldmap]]
