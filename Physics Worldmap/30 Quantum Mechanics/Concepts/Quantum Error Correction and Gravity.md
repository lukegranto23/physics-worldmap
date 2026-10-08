---
type: "concept"
field: "Quantum Mechanics"
epistemic_status: "active"
level: "advanced"
tags: ["physics", "field/quantum", "status/active", "level/advanced"]
aliases: ["holographic quantum error correction", "bulk reconstruction as QEC", "ADH code"]
created: 2026-07-30
updated: 2026-09-04
note_maturity: expanded
source_audit: bibliography-present-needs-claim-audit
---

# Quantum Error Correction and Gravity

> [!summary] Core idea
> In semiclassical code-subspace descriptions of AdS/CFT, bulk reconstruction has the structure of operator-algebra quantum error correction. Different boundary representatives can implement the same logical action without making independent copies of an arbitrary quantum state.

> [!note] Documentation status
> Expanded orientation with canonical sources; gravitational interpretation is conditional on the duality and approximation regime.

## Encoding and recoverable algebras

Let $V:\mathcal H_{\rm code}\to\mathcal H_{\rm boundary}$ be an encoding isometry. An operator $\phi$ is recoverable from region $A$ if a representative $O_A$ satisfies
$$
(O_A\otimes I_{\bar A})V=V\phi
$$
on the chosen code subspace, exactly in an ideal code or approximately in the physical application. Operator-algebra correction protects a selected logical algebra acting within a code, not necessarily every logical operator.

For ordinary subspace correction, the Knill–Laflamme condition is
$$
P E_a^\dagger E_b P=c_{ab}P.
$$
For an operator algebra, the compressed error products must commute with the protected logical algebra. This distinction matters for gravitational centers and area operators. [Almheiri, Dong, and Harlow](https://doi.org/10.1007/JHEP04(2015)163)

## Entanglement wedge and entropy

Within the appropriate holographic code subspace, operators in the entanglement wedge of $A$ can be represented on $A$. The code subspace, dressing, quantum corrections, and reconstruction error must be specified.

Codes with complementary recovery can exhibit an entropy decomposition into a central area-like contribution plus logical bulk entropy. In holography this motivates
$$
S(A)=\frac{\langle\operatorname{Area}\rangle}{4G_N}+S_{\rm bulk}+\cdots.
$$
It is not a property of every arbitrary QEC code. [Harlow, RT from QEC](https://arxiv.org/abs/1607.03901)

## HaPPY as a toy example

Perfect tensors on a hyperbolic network define bulk-to-boundary encoding maps. The perfect-tensor property concerns bipartitions of an individual tensor; it does not imply that tracing out any less-than-half boundary subset leaves a maximally mixed remainder.

A greedy reconstruction algorithm gives a sufficient recoverable region for a specified erasure pattern. Its success is location-dependent and need not characterize every possible reconstruction. RT-like minimal-cut formulas hold in stated cases and depend on bond dimensions and bulk states. These are static toy codes, not dynamical solutions of quantum gravity. [Pastawski et al.](https://arxiv.org/abs/1503.06237)

## No-cloning and redundancy

Boundary representatives agree on encoded states while differing outside the code. Overlapping recovery regions or reconstructable commuting subalgebras do not supply two freely accessible copies of a full unknown quantum state. Compare this with [[Quantum Darwinism and Holographic Encoding]] only after distinguishing quantum information from classical pointer records.

## Information problem and open questions

Islands and entanglement-wedge reconstruction explain entropy and recoverability in controlled models; they do not by themselves give an efficient decoding algorithm or complete microscopic evaporation dynamics. Open questions include finite-$N$ errors, state-dependent code choices, dynamical geometries, complexity, and extensions beyond AdS.

A universal correction scale such as $e^{-S_{\rm BH}}$ should not be assumed for every observable or code regime.

## Recall checks

Specify a logical algebra, a correctable erasure, and an encoding. Explain why two boundary representatives can agree on the code without being identical everywhere. Separate a minimal-cut theorem in a toy network from an empirical statement about spacetime.

## Navigation

[[Quantum Mechanics Map]] · [[Quantum Error Correction]] · [[AdS-CFT Correspondence]] · [[Holographic Principle]] · [[Black Hole Information Problem]] · [[Tensor Networks and Physics]] · [[Physics Worldmap]]
