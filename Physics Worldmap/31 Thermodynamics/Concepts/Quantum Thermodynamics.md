---
type: "concept"
field: "Thermodynamics"
epistemic_status: "active"
level: "advanced"
tags: ["physics", "field/thermodynamics", "status/active", "level/advanced"]
aliases: ["quantum heat engines", "fluctuation theorems", "thermodynamic resource theory"]
created: 2026-07-30
updated: 2026-09-04
note_maturity: expanded
source_audit: bibliography-present-needs-claim-audit
---

# Quantum Thermodynamics

> [!summary] Core idea
> Quantum thermodynamics studies energy, entropy, work, and heat in quantum systems, including small devices, coherence, fluctuations, and system–bath correlations. It refines the assumptions of macroscopic thermodynamics; it does not abolish the second law at small scales.

> [!note] Documentation status
> Expanded orientation with canonical references; operational assumptions determine which statements apply.

## Work and fluctuation relations

For an initially Gibbs-distributed system and the usual driven protocol,
$$
\langle e^{-\beta W}\rangle=e^{-\beta\Delta F},
\qquad \beta=(k_BT)^{-1}.
$$
This Jarzynski relation concerns an ensemble average of exponentiated trajectory work, not an equality for each trajectory. The final driven state need not be in equilibrium; $\Delta F$ compares equilibrium states of the endpoint Hamiltonians.

In the closed quantum two-projective-measurement protocol, $W=E_m^{\rm final}-E_n^{\rm initial}$. Initial coherence, measurements, open dynamics, and strong coupling require explicit treatment. Under microscopic reversibility and the appropriate reverse protocol, Crooks' relation reads
$$
P_F(W)/P_R(-W)=e^{\beta(W-\Delta F)}.
$$
[Jarzynski](https://doi.org/10.1103/PhysRevLett.78.2690), [Crooks](https://doi.org/10.1103/PhysRevE.60.2721)

## Information erasure

Resetting an initially unbiased classical bit with no exploitable side information, using an equilibrium bath at $T$ under the standard cyclic-memory assumptions, costs at least $k_BT\ln2$ of heat to the bath in the reversible limit. Biased memories, correlations, quantum side information, finite baths, and finite-time operation alter the operational bound. Erasure is not necessarily one bit of entropy reduction for every memory state.

## Thermal operations and coherence

A standard resource theory permits appending Gibbs ancillas, applying a unitary that conserves total energy, and discarding subsystems. For states diagonal in energy and a fixed Hamiltonian, thermomajorization characterizes transitions under ideal thermal operations, with the usual closure/approximation qualifications.

Catalytic transformations introduce additional assumptions about the catalyst and correlations. Families of Rényi free energies belong to these specific formulations; they should not be conflated with one universal necessary-and-sufficient test for arbitrary coherent states. [Brandão et al.](https://arxiv.org/abs/1305.5278)

Energy coherence is constrained by time-translation symmetry. A battery, phase reference, control apparatus, and correlations must be included when claiming an advantage. Thermal operations cannot create asymmetry from an initially symmetric preparation without an additional resource.

## Engines and batteries

For an ideal qubit Otto cycle with population-preserving adiabatic strokes and gaps $\hbar\omega_h>\hbar\omega_c$, the efficiency is
$$
\eta=1-\omega_c/\omega_h
$$
in the engine regime. The Carnot bound applies to engines using only equilibrium thermal reservoirs when all resource costs are counted. Squeezed or otherwise nonthermal reservoirs carry extra resources and cannot be compared using temperature alone.

Collective battery charging advantages depend on fair constraints on interaction strength, locality, control power, and stored energy. There is no universal $1/n$ charging-time law for unrestricted comparisons.

## Open questions and a useful benchmark

Strong coupling, non-Markovian dynamics, autonomous clocks, fluctuation precision, and resource-accounted quantum advantages remain active subjects. Start with a two-level working medium: track its Hamiltonian, density matrix, bath energy, drive work, and full entropy production through one cycle. Verify energy balance before discussing efficiency.

## Reading and recall

[Goold et al., quantum information in thermodynamics](https://arxiv.org/abs/1505.07835); [Vinjanampathy and Anders](https://arxiv.org/abs/1508.06099). Derive the average-work inequality from Jensen's inequality; explain the TPM coherence issue; identify every resource in a proposed quantum engine.

## Navigation

[[Thermodynamics Map]] · [[Thermodynamics of Information]] · [[Second Law of Thermodynamics]] · [[Entropy Production]] · [[Open Quantum Systems]] · [[Quantum Information]] · [[Physics Worldmap]]
