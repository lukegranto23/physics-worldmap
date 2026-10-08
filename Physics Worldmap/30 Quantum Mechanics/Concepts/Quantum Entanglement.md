---
type: "concept"
field: "Quantum Mechanics"
epistemic_status: "established"
level: "intermediate"
tags: ["physics", "field/quantum", "status/established", "level/intermediate"]
aliases: []
created: 2026-07-30
updated: 2026-09-02
note_maturity: expanded
source_audit: bibliography-present-needs-claim-audit
---

# Quantum Entanglement

> [!summary] Core idea
> An entangled state is not a convex mixture of product states. Entanglement is necessary but not sufficient for Bell nonlocality: some entangled states violate a Bell inequality for suitable measurements, while others admit local models in a given Bell scenario.

> [!note] Documentation status
> This expanded note includes a canonical bibliography but has not yet received a claim-by-claim source audit. The epistemic label describes the standing of the underlying physics in its stated regime; it does not certify every sentence or equation in this note.

## Mathematical handle

$\rho_{AB}\ne\sum_i p_i\rho_A^i\otimes\rho_B^i$

The expression is an orientation point, not a substitute for checking assumptions, sign conventions, units, boundary conditions, and the regime in which it was derived.

## Epistemic status

**Established.** This is a well-established framework or result within its stated domain.

## Place in the world map

- Domain: [[Quantum Mechanics Map]]
- Field-level guiding question (context only): “How do amplitudes encode probabilities and interference?”
- Nearby concepts: [[Physics Worldmap]] · [[Quantum Mechanics Map]] · [[Composite Quantum Systems|← previous]] · [[Bell Theorem|next →]]

## Physical content

Quantum entanglement is the phenomenon in which the state of a composite system is nonseparable: a pure entangled state is not a product state, and a mixed entangled state is not a convex mixture of product states. Entanglement can produce correlations unavailable to separable states. For suitable states and measurement choices, those correlations violate [[Bell Theorem|Bell inequalities]] and rule out local hidden-variable models satisfying the Bell assumptions; entanglement by itself does not guarantee Bell violation in every state or measurement scenario.

The concept originates in the 1935 paper by Einstein, Podolsky, and Rosen (EPR), who argued that quantum mechanics must be incomplete because entangled states appear to allow instantaneous "influence" between distant measurements. Their argument assumed locality and realism (that physical quantities have definite values independent of measurement). John Bell showed in 1964 that any theory satisfying these assumptions must obey certain statistical inequalities, and that quantum mechanics predicts their violation. Experiments by Aspect (1982), and subsequently by many groups with increasing rigor (culminating in loophole-free tests by Hensen et al., 2015, and others), have confirmed the quantum mechanical predictions, establishing that nature is nonlocal in the sense of Bell.

For a bipartite pure state $|\psi\rangle_{AB}$, the **Schmidt decomposition** provides the canonical form for quantifying entanglement. Any such state can be written as $|\psi\rangle_{AB} = \sum_i \lambda_i |a_i\rangle \otimes |b_i\rangle$, where $\lambda_i \geq 0$, $\sum_i \lambda_i^2 = 1$, and $\{|a_i\rangle\}$, $\{|b_i\rangle\}$ are orthonormal bases for the respective subsystems. The state is entangled if and only if more than one Schmidt coefficient is nonzero. The number of nonzero coefficients is the **Schmidt rank**. The four **Bell states** are the maximally entangled states of two qubits:

$$|\Phi^\pm\rangle = \frac{1}{\sqrt{2}}(|00\rangle \pm |11\rangle), \qquad |\Psi^\pm\rangle = \frac{1}{\sqrt{2}}(|01\rangle \pm |10\rangle)$$

These form an orthonormal basis for the two-qubit Hilbert space and are the fundamental resource states for quantum teleportation, superdense coding, and entanglement-based quantum key distribution.

A striking property of entanglement is **monogamy**: if qubit $A$ is maximally entangled with qubit $B$, it cannot be entangled at all with a third qubit $C$. Quantitatively, for the squared concurrence, the Coffman-Kundu-Wootters inequality states $C^2_{A|BC} \geq C^2_{AB} + C^2_{AC}$. This constraint has deep implications for [[Black Hole Thermodynamics|black hole physics]] (the firewall argument relies on monogamy) and for the security of quantum cryptography.

In many-body quantum systems, entanglement structure reveals the nature of quantum phases. Ground states of gapped, local Hamiltonians typically satisfy an **area law**: the entanglement entropy of a region scales as the area of its boundary, $S \sim L^{d-1}$, rather than its volume. Critical systems and certain exotic phases violate this with logarithmic corrections. The distinction between area-law and volume-law entanglement is central to the efficiency of [[Tensor Networks and Physics|tensor network]] methods such as matrix product states and MERA, which exploit the limited entanglement of physically relevant states.

## Mathematical framework

For a bipartite pure state, the **von Neumann entanglement entropy** is the primary measure:

$$S(\rho_A) = -\operatorname{Tr}(\rho_A \ln \rho_A) = -\sum_i \lambda_i^2 \ln \lambda_i^2$$

where $\rho_A = \operatorname{Tr}_B |\psi\rangle\langle\psi|$ is the reduced density matrix of subsystem $A$, and $\lambda_i$ are the Schmidt coefficients. For a maximally entangled state of two $d$-dimensional systems, $S = \ln d$.

For mixed states, several entanglement measures are used since $S(\rho_A)$ no longer quantifies entanglement alone:

- **Concurrence** (Wootters, 1998): For two qubits with density matrix $\rho$, define the spin-flipped state $\tilde{\rho} = (\sigma_y \otimes \sigma_y)\rho^*(\sigma_y \otimes \sigma_y)$. The concurrence is $C(\rho) = \max(0, \sqrt{\lambda_1} - \sqrt{\lambda_2} - \sqrt{\lambda_3} - \sqrt{\lambda_4})$, where $\lambda_i$ are the eigenvalues of $\rho\tilde{\rho}$ in decreasing order.
- **Negativity**: $\mathcal{N}(\rho) = \frac{\|\rho^{T_A}\|_1 - 1}{2}$, where $\rho^{T_A}$ is the partial transpose of $\rho$ with respect to subsystem $A$, and $\|\cdot\|_1$ is the trace norm. A nonzero negativity is a sufficient (but not necessary, for dimensions $>2 \times 3$) condition for entanglement.
- **Entanglement of formation**: $E_F(\rho) = \min_{\{p_i, |\psi_i\rangle\}} \sum_i p_i\, S(\operatorname{Tr}_B |\psi_i\rangle\langle\psi_i|)$, minimized over all pure-state decompositions $\rho = \sum_i p_i |\psi_i\rangle\langle\psi_i|$.

The **CHSH inequality** provides the standard Bell test. For observables $A_1, A_2$ on Alice's side and $B_1, B_2$ on Bob's side (each with outcomes $\pm 1$):

$$|E(A_1, B_1) + E(A_1, B_2) + E(A_2, B_1) - E(A_2, B_2)| \leq 2 \quad \text{(classical)}$$

Quantum mechanics allows violation up to the Tsirelson bound $2\sqrt{2} \approx 2.83$, achieved by the Bell state $|\Phi^+\rangle$ with appropriate measurement settings.

The **Ryu-Takayanagi formula** connects entanglement to geometry in the [[AdS-CFT Correspondence|AdS/CFT]] context:

$$S(\rho_A) = \frac{\text{Area}(\gamma_A)}{4 G_N \hbar}$$

where $\gamma_A$ is the minimal-area surface in the bulk AdS spacetime that is homologous to the boundary region $A$. This remarkable formula, and the related ER=EPR conjecture (Maldacena and Susskind, 2013), suggests that [[Quantum Entanglement|entanglement]] may be the fundamental building block of spacetime geometry itself.

## Key results and implications

- Bell inequality violations have been confirmed experimentally in loophole-free settings, establishing that local realism is incompatible with nature. The 2022 Nobel Prize in Physics was awarded to Aspect, Clauser, and Zeilinger for this line of work.
- Entanglement is the essential resource for **quantum computation**: algorithms like Shor's factoring and quantum error-correcting codes require entangled states that span many qubits.
- **Quantum teleportation** (Bennett et al., 1993) uses a shared Bell pair and two bits of classical communication to transfer an unknown quantum state, demonstrating that entanglement can be "spent" as a communication resource.
- In condensed matter, entanglement entropy distinguishes [[Topological Order|topological phases]]: topologically ordered states have a universal correction $-\gamma$ (the topological entanglement entropy) to the area law, $S = \alpha L - \gamma$.
- The ER=EPR conjecture and Ryu-Takayanagi formula suggest that entanglement may be the microscopic mechanism underlying the emergence of spacetime in [[Quantum Gravity]].

## Failure modes and limitations

- Entanglement does **not** permit faster-than-light signaling. The reduced density matrix of one subsystem is independent of any operation performed on the other, so no information can be transmitted through entanglement alone without a classical channel.
- A widespread misconception is to identify entanglement with Bell nonlocality. Separable correlations can be generated by shared classical randomness. Entangled states are nonseparable, but only a subset display Bell-nonlocal correlations in a specified measurement scenario; some mixed entangled states admit local hidden-variable models for broad classes of measurements.
- For mixed states, determining whether a given density matrix is entangled is computationally hard (NP-hard for general multipartite systems). The partial transpose criterion (Peres-Horodecki) is necessary and sufficient only for $2 \times 2$ and $2 \times 3$ dimensional systems; for higher dimensions, bound entangled states exist that are entangled but have positive partial transpose.
- Entanglement is fragile: interaction with the environment causes [[Decoherence]], which can destroy entanglement on timescales much shorter than the decoherence time of individual qubits (a phenomenon called **entanglement sudden death**).

## Experimental evidence

- **Photon pair experiments**: Spontaneous parametric down-conversion produces entangled photon pairs that have been used in Bell tests since Aspect's pioneering experiments (1981-82). Modern loophole-free tests (Delft, 2015; NIST, 2015; Vienna, 2015) close the locality, detection, and freedom-of-choice loopholes simultaneously.
- **Trapped ions**: Entangled states of up to $\sim 20$ ions have been generated deterministically using laser-driven gate operations (Blatt group, Innsbruck; Monroe group, Maryland). These systems achieve the highest-fidelity Bell states.
- **Superconducting qubits**: Multi-qubit entangled states are routinely generated in superconducting circuits, forming the basis of current quantum computing platforms (Google, IBM, etc.). Google's 2019 quantum supremacy experiment involved a 53-qubit entangled state.
- **Satellite-based entanglement distribution**: The Micius satellite (Pan group, 2017) distributed entangled photon pairs over 1200 km, demonstrating Bell violation at unprecedented distances.

## Sources

- M. A. Nielsen and I. L. Chuang, *Quantum Computation and Quantum Information*, Cambridge University Press, 2000.
- R. Horodecki, P. Horodecki, M. Horodecki, and K. Horodecki, "Quantum entanglement," *Reviews of Modern Physics* **81**, 865 (2009).
- J. S. Bell, *Speakable and Unspeakable in Quantum Mechanics*, 2nd ed., Cambridge University Press, 2004.

## Reasoning checks

1. State the physical objects and observables without using the displayed equation.
2. Check dimensions and identify every limiting assumption.
3. Give one regime where this description succeeds and one where it needs correction.
4. Name an experiment, simulation, or observation that could determine its parameters.
5. Explain how this idea changes when the dominant length, time, energy, or particle-number scale changes.

## Expansion queue

- [x] Add a derivation from the nearest prerequisite principles.
- [x] Add a worked example with units.
- [x] Add a primary or canonical source.
- [x] Add a failure case, misconception, or counterexample.

## Navigation

[[Physics Worldmap]] · [[Quantum Mechanics Map]] · [[Composite Quantum Systems|← previous]] · [[Bell Theorem|next →]]
