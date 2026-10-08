---
type: "map-of-content"
field: "Plasma Physics"
epistemic_status: "mixed"
level: "all"
tags: ["physics", "map", "field/plasma"]
aliases: []
created: 2026-07-30
updated: 2026-07-30
---

# Plasma Physics Map

> [!abstract]
> Ionized collective matter governed by fields, particles, waves, collisions, instabilities, and magnetic topology.

## Questions that organize the field

- Which kinetic, fluid, or magnetohydrodynamic description is valid?
- How are charged particles confined, heated, and transported?
- Which microinstabilities drive anomalous transport?
- How can fusion plasmas sustain net energy and robust operation?

## Working principles

- Compare Debye length, gyroradius, mean free path, and system scale.
- Quasineutrality is a scale-dependent approximation, not exact neutrality.
- Distribution functions matter when collisions are weak or resonances dominate.
- Magnetic geometry, invariants, and instabilities govern confinement.

## Canonical mathematical handles

- **Debye length:** $\lambda_D=\sqrt{\epsilon_0k_BT_e/(n_e e^2)}$ — Charge perturbations are screened over a plasma scale.
- **Cyclotron frequency:** $\Omega_c=|q|B/m$ — Particles gyrate around magnetic field lines.
- **Vlasov equation:** $\partial_tf+\mathbf v\cdot\nabla f+(q/m)(\mathbf E+\mathbf v\times\mathbf B)\cdot\nabla_vf=0$ — Collisionless distributions evolve in self-consistent fields.
- **Ideal MHD:** $\partial_t\mathbf B=\nabla\times(\mathbf u\times\mathbf B)$ — Magnetic flux is frozen into an ideal conducting fluid.

## Concept atlas

| Concept | Level | Status | One-line orientation |
|---|---:|---|---|
| [[Plasma State]] | introductory | established | A plasma contains mobile charges whose collective electromagnetic response dominates over many binary interactions. |
| [[Debye Screening]] | intermediate | established | Mobile charges rearrange to screen electrostatic potentials over the Debye length in equilibrium-like regimes. |
| [[Plasma Frequency]] | introductory | established | Electrons displaced from ions oscillate collectively at a characteristic frequency. |
| [[Charged Particle Orbits]] | introductory | established | Uniform magnetic fields produce helical motion with cyclotron frequency and Larmor radius. |
| [[Guiding Center Drifts]] | intermediate | established | Slow field variation and external forces move a particle's gyrocenter across magnetic fields. |
| [[Adiabatic Invariants in Plasmas]] | advanced | established | Slowly varying fields approximately conserve magnetic moment and bounce or drift actions. |
| [[Quasineutrality]] | introductory | effective | At scales much larger than the Debye length, charge densities nearly cancel while currents and fields remain important. |
| [[Fluid Plasma Models]] | intermediate | established | Velocity moments of kinetic equations yield density, momentum, and pressure equations requiring closure. |
| [[Vlasov Equation]] | advanced | established | Collisionless distribution functions are advected in six-dimensional phase space by self-consistent Lorentz forces. |
| [[Landau Damping]] | advanced | established | Resonant particles exchange energy with a wave, causing collisionless damping or growth depending on the velocity-space slope. |
| [[Plasma Waves]] | intermediate | established | Coupled charge, current, pressure, and field perturbations support electrostatic and electromagnetic branches. |
| [[Magnetohydrodynamics]] | intermediate | established | MHD treats a conducting plasma as a fluid coupled to magnetic fields at sufficiently large collisional or collective scales. |
| [[Frozen In Flux]] | advanced | effective | In ideal MHD, magnetic flux through a material loop is conserved, tying field topology to fluid motion. |
| [[Magnetic Pressure and Tension]] | advanced | established | The Lorentz force separates into a magnetic pressure gradient and tension along curved field lines. |
| [[Magnetic Reconnection]] | advanced | active | Nonideal effects change magnetic topology and rapidly convert field energy to particle and bulk energy. |
| [[Plasma Instabilities]] | advanced | active | Free energy in distributions, gradients, currents, or magnetic geometry can amplify perturbations. |
| [[Magnetized Plasma Turbulence]] | advanced | active | Nonlinear interactions transfer energy across anisotropic scales and drive transport far above collisional estimates. |
| [[Magnetic Confinement Fusion]] | intermediate | active | Tokamaks and stellarators use shaped magnetic fields to confine hot deuterium-tritium plasma. |
| [[Tokamaks]] | advanced | active | A tokamak combines toroidal and plasma-current poloidal fields, with stability and steady-current challenges. |
| [[Stellarators]] | advanced | active | Three-dimensional external coils create rotational transform without relying on a large plasma current. |
| [[Inertial Confinement Fusion]] | intermediate | active | Rapid compression confines fusion fuel by inertia for a short burn before disassembly. |
| [[Lawson Criterion]] | intermediate | established | Net fusion requires sufficient density, temperature, and energy confinement time for reaction heating to exceed losses. |
| [[Space Plasmas]] | intermediate | active | Solar wind, magnetospheres, shocks, aurorae, and radiation belts are collisionless plasma systems coupled across scales. |
| [[High Energy Density Physics]] | advanced | active | Matter at extreme pressure and energy density couples plasma, radiation, atomic, and hydrodynamic physics. |

## Frontier queue

- [ ] Burning-plasma control and economically viable fusion
- [ ] First-principles prediction of turbulent transport
- [ ] Magnetic reconnection across collisionality regimes
- [ ] High-energy-density and laser-plasma physics
- [ ] Space-weather forecasting from kinetic to global scales

Current evidence and sources belong in [[Open Problems Dashboard]] and the individual frontier notes. A checked box means “reviewed recently,” never “solved.”

## Neighboring fields

[[Fluid Dynamics Map]] · [[Astrophysics Map]] · [[Electromagnetism Map]] · [[Statistical Physics Map]]

## Suggested study loop

1. Read the field questions, then explain them from memory.
2. Learn the introductory concepts and reproduce their limiting cases.
3. Derive at least one canonical equation from a variational, symmetry, or conservation principle.
4. Reproduce one landmark result computationally or from public data.
5. Audit one frontier claim: known facts, model dependence, discriminating observable, and next experiment.

## Navigation

[[Physics Worldmap]] · [[Learning Paths]] · [[Epistemic Status and Claim Hygiene]] · [[Synthesis Lab]]
