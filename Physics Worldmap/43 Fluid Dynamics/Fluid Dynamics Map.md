---
type: "map-of-content"
field: "Fluid Dynamics"
epistemic_status: "mixed"
level: "all"
tags: ["physics", "map", "field/fluids"]
aliases: []
created: 2026-07-30
updated: 2026-07-30
---

# Fluid Dynamics Map

> [!abstract]
> Flow of liquids and gases across laminar, turbulent, compressible, geophysical, and multiphase regimes.

## Questions that organize the field

- Which balances dominate at the relevant Reynolds, Mach, Froude, and Weber numbers?
- When does smooth flow become unstable or turbulent?
- How are momentum, heat, species, and vorticity transported?
- Can singular behavior or universal turbulent statistics be characterized?

## Working principles

- Nondimensionalize before solving.
- Conservation equations require constitutive closure and boundary data.
- Vorticity and circulation expose rotational structure.
- Turbulence requires statistical observables and resolution-aware computation.

## Canonical mathematical handles

- **Continuity:** $\partial_t\rho+\nabla\cdot(\rho\mathbf u)=0$ — Fluid mass is conserved.
- **Navier-Stokes:** $\rho D_t\mathbf u=-\nabla p+\mu\nabla^2\mathbf u+\rho\mathbf f$ — Momentum balance for a Newtonian fluid.
- **Reynolds number:** $Re=UL/\nu$ — Inertia relative to viscosity controls many flow regimes.
- **Vorticity:** $\boldsymbol\omega=\nabla\times\mathbf u$ — Local rotation and vortex stretching organize flow.

## Concept atlas

| Concept | Level | Status | One-line orientation |
|---|---:|---|---|
| [[Fluid Kinematics]] | introductory | established | A velocity field defines trajectories, streamlines, strain rate, rotation, and material transport. |
| [[Mass Conservation in Fluids]] | introductory | established | Local density change plus mass flux divergence vanishes in the absence of sources. |
| [[Euler Equations]] | intermediate | established | Inviscid fluid momentum changes through pressure gradients and body forces. |
| [[Navier Stokes Equations]] | intermediate | established | Newtonian viscous momentum balance combines inertia, pressure, stress diffusion, and forcing. |
| [[Incompressible Flow]] | introductory | established | When density changes are negligible, velocity is divergence-free and pressure enforces the constraint. |
| [[Bernoulli Equation]] | introductory | established | Along a steady inviscid streamline, pressure, kinetic, and potential energy per volume are conserved under stated assumptions. |
| [[Viscosity]] | introductory | established | Viscosity converts velocity gradients into shear stress and dissipates mechanical energy into heat. |
| [[Boundary Layers]] | intermediate | established | At high Reynolds number, viscous effects concentrate near no-slip boundaries and may separate. |
| [[Vorticity]] | intermediate | established | Vorticity is the curl of velocity and evolves through advection, stretching, baroclinicity, and diffusion. |
| [[Kelvin Circulation Theorem]] | advanced | established | For an inviscid barotropic fluid with conservative body forces, circulation around a material loop is conserved. |
| [[Potential Flow]] | intermediate | effective | Incompressible irrotational flow reduces to a harmonic velocity potential, useful outside boundary layers. |
| [[Dimensional Analysis in Fluids]] | introductory | established | Dimensionless groups identify dominant balances and enable similarity laws and scaled experiments. |
| [[Reynolds Number]] | introductory | established | Reynolds number compares inertial advection with viscous diffusion. |
| [[Flow Instability]] | advanced | established | Perturbations grow when energy extraction from a base flow overcomes restoring and dissipative effects. |
| [[Turbulence]] | intermediate | active | Turbulence is multiscale irregular flow with strong mixing, nonlinear transfer, intermittency, and sensitive dynamics. |
| [[Kolmogorov Turbulence]] | advanced | established | Under ideal assumptions, inertial-range energy transfer yields scale laws based on the dissipation rate. |
| [[Reynolds Averaging and Closure]] | advanced | active | Averaging turbulent equations creates unknown correlation stresses that require models or additional dynamics. |
| [[Compressible Flow]] | intermediate | established | Density, pressure, temperature, and velocity couple through conservation laws and an equation of state. |
| [[Shocks]] | advanced | established | Compressible nonlinear waves steepen into discontinuities satisfying conservation jump conditions and increasing entropy. |
| [[Surface Waves]] | advanced | established | Gravity and surface tension restore interface disturbances, producing wavelength-dependent dispersion. |
| [[Multiphase Flow]] | advanced | active | Distinct phases couple through interfaces, surface tension, phase change, and complex topology. |
| [[Convection]] | intermediate | established | Buoyancy can destabilize a temperature gradient and organize heat transport into rolls or turbulence. |
| [[Rotating Fluids]] | advanced | established | Coriolis effects constrain large-scale flow and create geostrophic balance, inertial waves, and columns. |
| [[Stratified Fluids]] | advanced | established | Stable density gradients support internal waves and inhibit vertical motion. |

## Frontier queue

- [ ] Three-dimensional Navier-Stokes regularity
- [ ] Predictive theory and control of turbulence
- [ ] Multiphase, reactive, and interfacial flow across scales
- [ ] Data-assisted closure that respects conservation and uncertainty
- [ ] Extreme geophysical and astrophysical fluid regimes

Current evidence and sources belong in [[Open Problems Dashboard]] and the individual frontier notes. A checked box means “reviewed recently,” never “solved.”

## Neighboring fields

[[Continuum Mechanics Map]] · [[Plasma Physics Map]] · [[Geophysics and Climate Map]] · [[Nonlinear Dynamics and Complex Systems Map]]

## Suggested study loop

1. Read the field questions, then explain them from memory.
2. Learn the introductory concepts and reproduce their limiting cases.
3. Derive at least one canonical equation from a variational, symmetry, or conservation principle.
4. Reproduce one landmark result computationally or from public data.
5. Audit one frontier claim: known facts, model dependence, discriminating observable, and next experiment.

## Navigation

[[Physics Worldmap]] · [[Learning Paths]] · [[Epistemic Status and Claim Hygiene]] · [[Synthesis Lab]]
