---
type: "map-of-content"
field: "Continuum Mechanics"
epistemic_status: "mixed"
level: "all"
tags: ["physics", "map", "field/continuum"]
aliases: []
created: 2026-07-30
updated: 2026-07-30
---

# Continuum Mechanics Map

> [!abstract]
> Macroscopic matter treated as continuous fields of density, deformation, stress, strain, and flow.

## Questions that organize the field

- How do conservation laws constrain continuous media?
- Which constitutive relation is valid for a given material and timescale?
- When do singularities, shocks, fractures, or instabilities arise?
- How do microstructure and defects determine macroscopic response?

## Working principles

- Conservation laws are universal; constitutive laws are material- and regime-dependent.
- Distinguish Eulerian and Lagrangian descriptions.
- Track objective tensors, boundary conditions, and dimensionless control parameters.
- Check continuum validity against microscopic length and time scales.

## Canonical mathematical handles

- **Mass balance:** $\partial_t\rho+\nabla\cdot(\rho\mathbf v)=0$ — Matter is locally conserved.
- **Momentum balance:** $\rho D_t\mathbf v=\nabla\cdot\boldsymbol\sigma+\rho\mathbf b$ — Stress and body forces change momentum.
- **Linear elasticity:** $\sigma_{ij}=C_{ijkl}\epsilon_{kl}$ — A constitutive relation closes elastic dynamics.
- **Strain:** $\epsilon_{ij}=(\partial_i u_j+\partial_j u_i)/2$ — Small deformation is the symmetric displacement gradient.

## Concept atlas

| Concept | Level | Status | One-line orientation |
|---|---:|---|---|
| [[Continuum Hypothesis]] | introductory | established | A medium is approximated by smooth fields when observation scales greatly exceed microscopic structure. |
| [[Material and Spatial Descriptions]] | intermediate | established | Lagrangian coordinates follow material parcels while Eulerian coordinates describe fields at fixed spatial locations. |
| [[Deformation Gradient]] | advanced | established | The deformation gradient maps infinitesimal reference line elements into the current configuration. |
| [[Strain Tensors]] | advanced | established | Strain measures deformation independent of rigid motion; different tensors suit small or finite deformations. |
| [[Cauchy Stress Tensor]] | intermediate | established | Stress maps a surface normal to the traction exerted across that surface. |
| [[Balance Laws]] | intermediate | established | Mass, momentum, angular momentum, and energy balances provide universal field equations before constitutive closure. |
| [[Constitutive Relations]] | intermediate | established | Constitutive laws relate stress, flux, and internal variables to deformation and history within a material regime. |
| [[Linear Elasticity]] | intermediate | established | Small reversible deformations of solids obey a linear stress-strain relation constrained by material symmetry. |
| [[Isotropic Elasticity]] | intermediate | established | An isotropic linear solid is characterized by two independent elastic constants. |
| [[Elastic Waves]] | intermediate | established | Momentum balance plus elasticity supports longitudinal and transverse waves in solids. |
| [[Viscoelasticity]] | intermediate | established | Viscoelastic materials combine storage and dissipation with time-dependent stress-strain response. |
| [[Plasticity]] | advanced | active | Plastic deformation is irreversible and often governed by yield surfaces, flow rules, and evolving internal variables. |
| [[Dislocations]] | advanced | established | Line defects carry quantized lattice mismatch and mediate crystal plasticity. |
| [[Fracture Mechanics]] | advanced | active | Crack growth depends on stress intensity, energy release rate, toughness, geometry, and dynamics. |
| [[Contact Mechanics]] | advanced | established | Contact forces and deformations depend on geometry, elasticity, adhesion, friction, and surface roughness. |
| [[Friction]] | introductory | active | Friction emerges from asperity contact, adhesion, deformation, wear, and state-dependent interfaces. |
| [[Granular Matter]] | advanced | active | Grains form force networks and exhibit jamming, avalanches, segregation, and nonthermal statistics. |
| [[Poroelasticity]] | advanced | established | Fluid pressure and solid deformation are coupled in porous media. |
| [[Homogenization]] | advanced | established | Homogenization derives effective continuum properties from heterogeneous microstructure under scale separation. |
| [[Metamaterials]] | advanced | active | Engineered microstructure produces effective mechanical response unavailable in ordinary homogeneous materials. |

## Frontier queue

- [ ] Fracture nucleation and multiscale crack dynamics
- [ ] Metamaterials with programmable nonlinear and topological response
- [ ] Plasticity from dislocation networks and amorphous rearrangements
- [ ] Granular constitutive laws across jamming and flow

Current evidence and sources belong in [[Open Problems Dashboard]] and the individual frontier notes. A checked box means “reviewed recently,” never “solved.”

## Neighboring fields

[[Classical Mechanics Map]] · [[Fluid Dynamics Map]] · [[Soft Matter Map]] · [[Geophysics and Climate Map]]

## Suggested study loop

1. Read the field questions, then explain them from memory.
2. Learn the introductory concepts and reproduce their limiting cases.
3. Derive at least one canonical equation from a variational, symmetry, or conservation principle.
4. Reproduce one landmark result computationally or from public data.
5. Audit one frontier claim: known facts, model dependence, discriminating observable, and next experiment.

## Navigation

[[Physics Worldmap]] · [[Learning Paths]] · [[Epistemic Status and Claim Hygiene]] · [[Synthesis Lab]]
