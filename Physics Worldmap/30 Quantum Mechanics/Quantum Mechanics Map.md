---
type: "map-of-content"
field: "Quantum Mechanics"
epistemic_status: "mixed"
level: "all"
tags: ["physics", "map", "field/quantum"]
aliases: []
created: 2026-07-30
updated: 2026-09-02
---

# Quantum Mechanics Map

> [!abstract]
> States, amplitudes, observables, measurement, entanglement, dynamics, and the structure of microscopic prediction.

## Questions that organize the field

- How do amplitudes encode probabilities and interference?
- Which observables can be jointly sharp, and how do measurements update states?
- How do classical behavior and irreversible records emerge?
- Which quantum resources enable computation, sensing, and communication?

## Working principles

- States are rays or density operators; observables are operators or generalized measurements.
- Evolution of a closed system is unitary; open systems require channels or master equations.
- Composite systems use tensor products and may be entangled.
- Interpretive claims must be separated from operational predictions.

## Canonical mathematical handles

- **Schrodinger:** $i\hbar\partial_t|\psi\rangle=H|\psi\rangle$ — The Hamiltonian generates closed-system evolution.
- **Born rule:** $p(a)=\langle\psi|\Pi_a|\psi\rangle$ — Squared amplitude gives outcome probability.
- **Commutator:** $[A,B]=AB-BA$ — Noncommutativity controls compatibility and dynamics.
- **Density evolution:** $i\hbar\dot\rho=[H,\rho]$ — Mixed and entangled subsystem states use density operators.

## Concept atlas

| Concept | Level | Status | One-line orientation |
|---|---:|---|---|
| [[Quantum States]] | introductory | established | A quantum state assigns probabilities to all allowed measurements and is represented by a ray or density operator. |
| [[Hilbert Space]] | intermediate | established | Quantum pure states inhabit a complex inner-product space whose dimension and tensor structure encode degrees of freedom. |
| [[Superposition Principle]] | introductory | established | Linear combinations of state vectors are possible states and produce interference when alternatives remain coherent. |
| [[Born Rule]] | introductory | established | Measurement probabilities are given by expectation values of positive effects, reducing to squared amplitudes for projectors. |
| [[Observables and Operators]] | intermediate | established | Ideal observables correspond to self-adjoint operators whose spectra give possible values. |
| [[Compatible Observables]] | intermediate | established | Commuting observables can share an eigenbasis and admit a joint sharp measurement in the idealized projective setting. |
| [[Uncertainty Relations]] | intermediate | established | Noncommuting observables have state-dependent lower bounds on joint dispersion and information tradeoffs. |
| [[Schrodinger Equation]] | introductory | established | The Hamiltonian generates continuous unitary time evolution for a closed nonrelativistic quantum system. |
| [[Stationary States]] | introductory | established | Hamiltonian eigenstates acquire only a phase in time and define quantized energy levels for bound systems. |
| [[Position and Momentum]] | introductory | established | Position and momentum are Fourier-conjugate operators with a canonical commutation relation. |
| [[Wave Packets and Quantum Spreading]] | intermediate | established | Localized states combine momentum components that dephase, generally causing free-particle spreading. |
| [[Quantum Harmonic Oscillator]] | introductory | established | Ladder operators solve an exactly spaced spectrum and form the local approximation near stable minima. |
| [[Infinite and Finite Square Wells]] | introductory | established | Boundary conditions quantize standing-wave momenta and energies in confined regions. |
| [[Quantum Tunneling]] | intermediate | established | Wave amplitudes penetrate classically forbidden regions, enabling barrier transmission and level splitting. |
| [[Angular Momentum in Quantum Mechanics]] | intermediate | established | Rotation generators obey a noncommutative algebra with quantized total and projected angular momentum. |
| [[Spin]] | intermediate | established | Spin is intrinsic angular momentum classified by rotation-group representations and has no classical rigid-body analogue. |
| [[Identical Particles]] | intermediate | established | Indistinguishable particles require symmetric bosonic or antisymmetric fermionic states, with observable consequences. |
| [[Pauli Exclusion Principle]] | introductory | established | No two identical fermions can occupy the same single-particle state in an antisymmetrized description. |
| [[Density Matrices]] | intermediate | established | Density operators represent classical uncertainty, subsystems of entangled states, and general quantum ensembles. |
| [[Composite Quantum Systems]] | intermediate | established | The state space of distinguishable subsystems is a tensor product, permitting correlations stronger than classical mixtures. |
| [[Quantum Entanglement]] | intermediate | established | Entangled states are nonseparable; entanglement is necessary but not sufficient for Bell nonlocality, and some entangled states violate Bell inequalities for suitable measurements. |
| [[Bell Theorem]] | advanced | established | No local hidden-variable model satisfying the Bell assumptions reproduces all quantum correlations. |
| [[Quantum Measurement]] | intermediate | established | A measurement is described operationally by outcomes, probabilities, and post-measurement transformations. |
| [[POVMs and Quantum Instruments]] | advanced | established | Generalized measurements use positive effects for statistics and completely positive maps for state updates. |
| [[Decoherence]] | advanced | established | Environmental entanglement suppresses interference in selected reduced-state bases without by itself selecting a unique experienced outcome. |
| [[Open Quantum Systems]] | advanced | established | Subsystem evolution includes dissipation, noise, memory, and information exchange with an environment. |
| [[Lindblad Master Equation]] | advanced | established | Markovian completely positive trace-preserving dynamics has a generator of Gorini-Kossakowski-Sudarshan-Lindblad form. |
| [[Path Integrals]] | advanced | established | Quantum amplitudes can be expressed as a coherent sum over histories weighted by the classical action phase. |
| [[WKB Approximation]] | advanced | established | Slowly varying potentials permit a semiclassical phase-amplitude expansion with turning-point matching. |
| [[Time Independent Perturbation Theory]] | intermediate | established | Weak changes to a solvable Hamiltonian produce order-by-order corrections to eigenvalues and eigenstates. |
| [[Time Dependent Perturbation Theory]] | advanced | established | Weak time-dependent interactions generate transition amplitudes and response rates. |
| [[Adiabatic Theorem]] | advanced | established | Slow parameter change can keep a gapped system in its instantaneous eigenstate up to phases and controlled corrections. |
| [[Berry Phase]] | advanced | established | Adiabatic cyclic evolution produces a geometric phase determined by the path in parameter space. |
| [[Scattering in Quantum Mechanics]] | advanced | established | Asymptotic incoming and outgoing waves encode cross sections, phase shifts, resonances, and bound states. |
| [[Quantum Information]] | intermediate | active | Quantum information studies states, channels, entropies, resources, computation, sensing, and communication. |
| [[Quantum Error Correction]] | advanced | active | Logical quantum information is encoded nonlocally so syndromes reveal correctable errors without measuring the logical state. |
| [[Interpretations of Quantum Mechanics]] | advanced | open | Interpretations provide different accounts of states, probabilities, outcomes, and observers while generally sharing standard predictions. |
| [[Quantum Error Correction and Gravity]] | advanced | active | Bulk reconstruction in semiclassical holographic code subspaces has operator-algebra QEC structure, conditional on the duality and regime. |
| [[Tensor Networks and Physics]] | advanced | mixed | Structured tensor decompositions efficiently represent some entanglement patterns; generic states and late-time dynamics can remain expensive. |

## Frontier queue

- [ ] Scalable fault-tolerant quantum computation
- [ ] Quantum simulation of strongly correlated and gauge systems
- [ ] Measurement problem and experimentally distinguishable modifications
- [ ] Quantum thermodynamics far from equilibrium
- [ ] Macroscopic quantum states and gravity-mediated entanglement tests

Current evidence and sources belong in [[Open Problems Dashboard]] and the individual frontier notes. A checked box means “reviewed recently,” never “solved.”

## Neighboring fields

[[Atomic Molecular and Optical Physics Map]] · [[Condensed Matter Physics Map]] · [[Quantum Field Theory and Particle Physics Map]] · [[Thermodynamics Map]]

## Suggested study loop

1. Read the field questions, then explain them from memory.
2. Learn the introductory concepts and reproduce their limiting cases.
3. Derive at least one canonical equation from a variational, symmetry, or conservation principle.
4. Reproduce one landmark result computationally or from public data.
5. Audit one frontier claim: known facts, model dependence, discriminating observable, and next experiment.

## Navigation

[[Physics Worldmap]] · [[Learning Paths]] · [[Epistemic Status and Claim Hygiene]] · [[Synthesis Lab]]
