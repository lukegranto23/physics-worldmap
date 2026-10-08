---
type: "concept"
field: "Condensed Matter Physics"
epistemic_status: "established"
level: "advanced"
tags: ["physics", "field/condensed", "status/established", "level/advanced"]
aliases: ["Magnetic Frustration", "Geometric Frustration"]
created: 2026-07-30
updated: 2026-09-04
note_maturity: expanded
source_audit: bibliography-present-needs-claim-audit
---

# Frustrated Magnets

> [!summary] Core idea
> Frustration occurs when competing local energetic preferences cannot all be satisfied. It can suppress ordering or favor unusual phases, but does not universally imply macroscopic degeneracy, a spin liquid, or computational hardness.

> [!note] Documentation status
> Expanded orientation; material-specific and thermodynamic-limit conclusions need dedicated source audits.

## Geometric example

For three classical fixed-length spins with antiferromagnetic coupling $J>0$,
$$
H_\triangle=J(\mathbf S_1\cdot\mathbf S_2+\mathbf S_2\cdot\mathbf S_3+
\mathbf S_3\cdot\mathbf S_1)
=\frac J2|\mathbf S_1+\mathbf S_2+\mathbf S_3|^2-\frac{3JS^2}{2}.
$$
A zero vector sum minimizes the energy, giving coplanar $120^\circ$ angles and energy $-JS^2/2$ per bond. The triangular-lattice nearest-neighbor classical Heisenberg ground states have this ordered structure; global rotations do not constitute extensive degeneracy. Triangular-lattice triangles share edges, unlike the corner-sharing triangles of kagome.

Kagome and pyrochlore constraints permit larger low-energy manifolds. Spin ice involves local Ising axes and particular interactions; it is not the generic consequence of putting Ising antiferromagnets on pyrochlore.

## Exchange frustration

The square-lattice model
$$
H=J_1\sum_{\langle ij\rangle}\mathbf S_i\cdot\mathbf S_j
+J_2\sum_{\langle\!\langle ij\rangle\!\rangle}\mathbf S_i\cdot\mathbf S_j
$$
competes between nearest- and next-nearest-neighbor antiferromagnetism. Ordered regimes and an intermediate strongly frustrated region occur, but phase boundaries depend on spin, geometry, and method. Whether a specified intermediate interval is a valence-bond solid or a spin liquid must be established, not built into the label.

## Consequences that must be tested

Fluctuations can select order from a degenerate classical manifold (“order by disorder”). Other models retain residual entropy, develop fractionalized excitations, or exhibit emergent gauge descriptions. No one outcome follows solely from frustration.

The ratio $|\Theta_{\rm CW}|/T_{\rm order}$ is a screening statistic, not a universal frustration measure: dimensionality, disorder, and anisotropy can also suppress ordering.

## Computational boundary

QMC sign severity depends on basis, representation, and algorithm. Frustrated models often cause cancellations, but some admit sign-free formulations. The generic complexity result does not prove that every frustrated instance is hard. [Troyer and Wiese](https://doi.org/10.1103/PhysRevLett.94.170201)

Exact diagonalization provides finite-cluster anchors; tensor networks, variational states, series expansions, and suitable QMC methods supply complementary approximations. Compare size, geometry, variational bias, and competing states before extrapolating.

## Evidence checklist

Measure structure factors and order parameters, energy gaps, correlations, heat capacity, and sensitivity to disorder. Absence of observed order down to a finite temperature is not proof of a zero-temperature spin liquid. A broad scattering continuum alone is not unique evidence of fractionalization.

## References and recall

Balents, “Spin liquids in frustrated magnets,” *Nature* **464**, 199 (2010); [Zhou, Kanoda, and Ng](https://arxiv.org/abs/1607.03228). Derive the triangle identity; compare Ising and Heisenberg spins; give a frustrated ordered counterexample.

## Navigation

[[Condensed Matter Physics Map]] · [[Quantum Spin Liquids]] · [[Quantum Phase Transitions]] · [[Frustrated Systems and Computational Hardness]] · [[Physics Worldmap]]
