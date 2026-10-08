---
type: "map-of-content"
field: "Classical Mechanics"
epistemic_status: "mixed"
level: "all"
tags: ["physics", "map", "field/mechanics"]
aliases: []
created: 2026-07-30
updated: 2026-07-30
---

# Classical Mechanics Map

> [!abstract]
> Motion from forces, constraints, action, geometry, symmetry, and phase-space structure.

## Questions that organize the field

- How does a state evolve under forces and constraints?
- Which coordinates expose conserved quantities and integrability?
- When do perturbations, resonances, or chaos destroy simple motion?
- How do classical dynamics emerge from relativistic and quantum theories?

## Working principles

- Begin with degrees of freedom, constraints, and scales.
- Use energy and momentum conservation before solving equations directly.
- Prefer Lagrangian or Hamiltonian structure for symmetry and constrained systems.
- Test stability, resonance, and the sensitivity of long-time predictions.

## Canonical mathematical handles

- **Newton:** $m\ddot{\mathbf r}=\mathbf F$ — Force determines acceleration in an inertial frame.
- **Euler-Lagrange:** $\frac d{dt}\partial_{\dot q_i}L-\partial_{q_i}L=0$ — Stationary action determines generalized motion.
- **Hamilton:** $\dot q_i=\partial_{p_i}H,\ \dot p_i=-\partial_{q_i}H$ — Dynamics is a flow on phase space.
- **Poisson bracket:** $\dot f=\{f,H\}+\partial_t f$ — The Hamiltonian generates time evolution.

## Concept atlas

| Concept | Level | Status | One-line orientation |
|---|---:|---|---|
| [[Kinematics]] | introductory | established | Kinematics describes position, velocity, acceleration, and frames without specifying the forces that cause motion. |
| [[Newtons Laws]] | introductory | established | Newton's laws define inertial motion, relate net force to momentum change, and impose reciprocal interaction forces in their domain. |
| [[Inertial and Noninertial Frames]] | intermediate | established | Accelerating or rotating frames introduce effective inertial forces such as Coriolis and centrifugal terms. |
| [[Work Energy and Power]] | introductory | established | Work transfers energy through force along displacement; power is its rate. |
| [[Linear Momentum and Impulse]] | introductory | established | Momentum is conserved for an isolated translationally invariant system; impulse changes it. |
| [[Angular Momentum and Torque]] | introductory | established | Angular momentum is conserved under rotational symmetry; torque is its rate of change. |
| [[Central Force Motion]] | intermediate | established | A central force confines motion to a plane and reduces two-body dynamics to an effective radial problem. |
| [[Kepler Problem]] | intermediate | established | The inverse-square two-body problem yields conic orbits and hidden symmetry. |
| [[Rigid Body Dynamics]] | intermediate | established | Rigid rotation is governed by the inertia tensor, angular velocity, torque, and Euler equations. |
| [[Moment of Inertia]] | intermediate | established | The inertia tensor measures resistance to angular acceleration about different axes. |
| [[Gyroscopes and Precession]] | intermediate | established | Torque changes the direction of angular momentum and produces precession and nutation. |
| [[Oscillations]] | introductory | established | Near a stable equilibrium, smooth systems reduce at leading order to harmonic oscillators. |
| [[Damping and Driven Oscillators]] | introductory | established | Dissipation and periodic forcing produce transients, phase lag, resonance, and finite response peaks. |
| [[Coupled Oscillators and Normal Modes]] | intermediate | established | Linear coupled systems decompose into independent eigenmodes with characteristic frequencies. |
| [[Lagrangian Mechanics]] | intermediate | established | The Lagrangian encodes dynamics in generalized coordinates and handles constraints and symmetries naturally. |
| [[Constraints and Generalized Coordinates]] | intermediate | established | Holonomic and nonholonomic constraints reduce or restrict accessible configurations and require careful force treatment. |
| [[Noethers Theorem in Mechanics]] | advanced | established | Every differentiable continuous symmetry of the action yields a conserved quantity. |
| [[Hamiltonian Mechanics]] | intermediate | established | Hamiltonian dynamics describes symplectic flow on phase space and supports canonical transformation theory. |
| [[Phase Space]] | intermediate | established | A classical state is a point in position-momentum space; ensembles occupy distributions over it. |
| [[Liouvilles Theorem]] | advanced | established | Hamiltonian flow preserves phase-space volume even as distributions stretch and fold. |
| [[Poisson Brackets]] | advanced | established | Poisson brackets encode the symplectic structure, generators, conserved quantities, and the classical precursor of commutators. |
| [[Canonical Transformations]] | advanced | established | Canonical transformations preserve Hamilton's equations and symplectic form while changing phase-space coordinates. |
| [[Hamilton Jacobi Theory]] | advanced | established | The Hamilton-Jacobi equation converts dynamics into a nonlinear PDE for the action and connects mechanics to waves and optics. |
| [[Action Angle Variables]] | advanced | established | Integrable periodic motion is simplest in actions that remain constant and angles that advance linearly. |
| [[Virial Theorem]] | intermediate | established | Time-averaged kinetic and potential terms obey a scaling relation for bound systems. |
| [[Scattering in Classical Mechanics]] | advanced | established | Impact parameters and deflection angles connect asymptotic trajectories to interaction potentials. |

## Frontier queue

- [ ] Long-time stability and transport in nearly integrable many-body systems
- [ ] Celestial mechanics with relativistic, tidal, and chaotic effects
- [ ] Geometric mechanics of active, robotic, and controlled systems
- [ ] Classical limits of quantum chaos and many-body dynamics

Current evidence and sources belong in [[Open Problems Dashboard]] and the individual frontier notes. A checked box means “reviewed recently,” never “solved.”

## Neighboring fields

[[Continuum Mechanics Map]] · [[Nonlinear Dynamics and Complex Systems Map]] · [[Relativity and Gravitation Map]]

## Suggested study loop

1. Read the field questions, then explain them from memory.
2. Learn the introductory concepts and reproduce their limiting cases.
3. Derive at least one canonical equation from a variational, symmetry, or conservation principle.
4. Reproduce one landmark result computationally or from public data.
5. Audit one frontier claim: known facts, model dependence, discriminating observable, and next experiment.

## Navigation

[[Physics Worldmap]] · [[Learning Paths]] · [[Epistemic Status and Claim Hygiene]] · [[Synthesis Lab]]
