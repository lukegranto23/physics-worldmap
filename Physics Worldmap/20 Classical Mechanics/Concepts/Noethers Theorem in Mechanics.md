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

# Noethers Theorem in Mechanics

> [!summary] Core idea
> A differentiable continuous variational symmetry gives a conserved charge along solutions. The relevant symmetry is of the action, allowing a boundary term—not merely a visually symmetric trajectory.

## Fixed-time version, with assumptions

Take an infinitesimal transformation $\delta q^i=\epsilon\xi^i(q,t)$, keeping time fixed. Suppose it changes the Lagrangian by
$\delta L=\epsilon\,dB(q,t)/dt$ for arbitrary admissible paths. On solutions,
$$
\frac{\delta L}{\epsilon}
=\frac{\partial L}{\partial q^i}\xi^i+
p_i\frac{d\xi^i}{dt}
=\frac{d}{dt}(p_i\xi^i).
$$
Therefore
$$
Q=p_i\xi^i-B,\qquad \frac{dQ}{dt}=0.
$$
The off-solution symmetry identity and the on-solution conservation law are distinct steps.

When a transformation also changes time by $\delta t=\epsilon\tau$, the charge takes the form $Q=p_i\xi^i-H\tau-B$, where $\xi$ is the change of coordinate at the transformed time and the boundary convention is chosen consistently. Do not mix this $\xi$ with the fixed-time variation $\xi-\dot q\tau$.

## Three reusable examples

For a potential independent of $x$, translation has $\xi_x=1$, $B=0$, so $p_x$ is conserved.

For a central potential in two dimensions, an infinitesimal rotation has $\xi=(-y,x)$. The charge is
$$
Q=xp_y-yp_x=L_z.
$$
For an autonomous Lagrangian, direct differentiation gives
$$
\frac{d}{dt}(p_i\dot q^i-L)=-\partial_tL=0.
$$
This is energy conservation in the regular time-independent mechanical setting. See [[Derivation — Noether Energy from Time Translation]].

## Boundary terms matter: Galilean boost

For a free one-dimensional particle, choose $q\mapsto q+\epsilon t$, where $\epsilon$ has units of velocity. To first order,
$\delta L=\epsilon m\dot q=\epsilon\,d(mq)/dt$.
Thus
$$
Q=pt-mq.
$$
Along $q=q_0+v_0t$, $p=mv_0$, the charge equals $-mq_0$. Omitting $B=mq$ would incorrectly claim that $pt$ is constant. The charge has units kg m because the transformation parameter carries velocity units.

## Broken symmetry gives a balance law

Suppose instead $\delta L/\epsilon=dB/dt+R$. Then the same calculation gives $\dot Q=R$.

For
$V=(k_xx^2+k_yy^2)/2$,
$$
\dot L_z=(k_x-k_y)xy.
$$
At $k_x=4$, $k_y=9$ N m$^{-1}$, $x=0.20$ m, $y=-0.10$ m, the torque is $+0.10$ N m. Rotational symmetry and angular-momentum conservation return when $k_x=k_y$. This makes approximate symmetry quantitatively testable rather than a slogan.

## Scope limits

Discrete symmetries do not generally supply this continuous charge. Gauge redundancies involve Noether identities and constraints; they are not automatically independent observable conserved charges. External driving and dissipation require the full balance accounting. A conserved charge also does not prove integrability: enough independent conserved quantities and their relations are needed.

## Sources and recall

[Tong, Classical Dynamics §2.4](https://davidtong.org/teaching/classical-dynamics/dynhtml/S2) supplies the continuous-symmetry framework. The boundary-term and broken-symmetry examples here can be verified by direct differentiation and by the bundled foundation checks.

Derive the boost charge without memorizing it. Explain why a symmetric-looking orbit does not prove a variational symmetry. Predict the torque sign before substituting numbers.

## Navigation

[[Lagrangian Mechanics]] · [[Hamiltonian Mechanics]] · [[Symmetry Conservation and Noether Map]] · [[Mechanics to Statistical Physics — Foundation Study Route]] · [[Classical Mechanics Map]] · [[Physics Worldmap]]
