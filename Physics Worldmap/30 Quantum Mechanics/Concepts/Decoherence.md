---
type: "concept"
field: "Quantum Mechanics"
epistemic_status: "established"
level: "advanced"
tags: ["physics", "field/quantum", "status/established", "level/advanced"]
aliases: []
created: 2026-07-30
updated: 2026-07-30
note_maturity: expanded
source_audit: bibliography-present-needs-claim-audit
---

# Decoherence

> [!summary] Core idea
> Environmental entanglement suppresses interference in selected reduced-state bases without by itself selecting a unique experienced outcome.

> [!note] Documentation status
> This expanded note includes a canonical bibliography but has not yet received a claim-by-claim source audit. The epistemic label describes the standing of the underlying physics in its stated regime; it does not certify every sentence or equation in this note.

## Mathematical handle

$\rho_S=\operatorname{Tr}_E\rho_{SE}$

The expression is an orientation point, not a substitute for checking assumptions, sign conventions, units, boundary conditions, and the regime in which it was derived.

## Epistemic status

**Established.** This is a well-established framework or result within its stated domain.

## Place in the world map

- Domain: [[Quantum Mechanics Map]]
- Field-level guiding question (context only): “How do amplitudes encode probabilities and interference?”
- Nearby concepts: [[Physics Worldmap]] · [[Quantum Mechanics Map]] · [[POVMs and Quantum Instruments|← previous]] · [[Open Quantum Systems|next →]]

## Physical content

Decoherence is the process by which a quantum system loses its coherence -- the ability to exhibit interference -- through entanglement with its environment. When a system $S$ interacts with a large number of environmental degrees of freedom $E$, the off-diagonal elements of the system's reduced density matrix $\rho_S = \operatorname{Tr}_E \rho_{SE}$ are suppressed in a basis determined by the nature of the system-environment interaction. This process is extremely rapid for macroscopic objects and explains why quantum superpositions are not observed at everyday scales, even though the underlying dynamics are fully unitary.

The central concept is **einselection** (environment-induced superselection), introduced by Wojciech Zurek. Not all bases of the system Hilbert space are equally robust against decoherence. The interaction Hamiltonian $H_{SE}$ between system and environment singles out a preferred set of states called **pointer states** -- these are the states that become minimally entangled with the environment and thus survive decoherence intact. Formally, pointer states $|s_i\rangle$ satisfy the condition that $H_{SE} |s_i\rangle |\varepsilon_0\rangle \approx |s_i\rangle |\varepsilon_i\rangle$ (the environment records "which pointer state" without disturbing the state itself). For a particle interacting with a thermal photon bath, the pointer states are approximate position eigenstates; for a harmonic oscillator weakly coupled to an environment, they are coherent states. This explains why we observe definite positions of macroscopic objects rather than superpositions of positions.

The **decoherence timescale** $\tau_D$ measures how quickly off-diagonal elements of $\rho_S$ are suppressed. It depends on the system, the environment, and the "distance" in the pointer basis between the superposed states. For a massive particle in a superposition of two positions separated by distance $\Delta x$, interacting with a thermal photon or air-molecule environment, the decoherence time is dramatically shorter than any other relevant timescale:

| System | Environment | $\Delta x$ | $\tau_D$ |
|--------|------------|-------------|----------|
| Dust grain ($10^{-5}$ m) | Air at STP | $10^{-5}$ m | $\sim 10^{-31}$ s |
| Dust grain ($10^{-5}$ m) | Sunlight | $10^{-5}$ m | $\sim 10^{-18}$ s |
| Large molecule (C$_{70}$) | Vacuum, thermal radiation | $10^{-7}$ m | $\sim 10^{-1}$ s |
| Electron | CMB photons | $10^{-2}$ m | $\sim 1$ s |
| Superconducting qubit | Engineered environment | $\sim$ qubit spacing | $\sim 10^{-4}$ s |

These numbers show that for everyday macroscopic objects, decoherence is effectively instantaneous -- it happens on timescales many orders of magnitude shorter than anything we can resolve.

The mathematical framework for describing decoherence is provided by the theory of [[Open Quantum Systems]]. When the environment is Markovian (memoryless), the evolution of $\rho_S$ is governed by the **Lindblad master equation**:

$$\frac{d\rho_S}{dt} = -\frac{i}{\hbar}[H_S, \rho_S] + \sum_k \gamma_k \left(L_k \rho_S L_k^\dagger - \frac{1}{2}\{L_k^\dagger L_k, \rho_S\}\right)$$

where $H_S$ is the system Hamiltonian, $L_k$ are Lindblad (jump) operators determined by the system-environment coupling, and $\gamma_k$ are positive rates. The first term generates unitary evolution; the second causes decoherence and dissipation. For pure dephasing (decoherence without energy exchange), the off-diagonal elements of $\rho_S$ in the pointer basis decay exponentially: $\rho_{ij}(t) = \rho_{ij}(0)\, e^{-t/\tau_D}$.

An important extension is **quantum Darwinism** (Zurek, 2009), which explains not just the loss of coherence but the emergence of objective classical reality. When a system interacts with an environment, many fragments of the environment acquire redundant copies of the information about the system's pointer state. Independent observers who each access only a small fraction of the environment will all agree on the state of the system -- exactly as in classical experience. This redundant proliferation of information is what makes the classical world "objective."

## Mathematical framework

The general decoherence process for a system initially in a superposition $|\psi_S\rangle = \sum_i c_i |s_i\rangle$ (where $|s_i\rangle$ are pointer states) proceeds via:

$$\left(\sum_i c_i |s_i\rangle\right) \otimes |\varepsilon_0\rangle \xrightarrow{H_{SE}} \sum_i c_i |s_i\rangle \otimes |\varepsilon_i(t)\rangle$$

Taking the partial trace over the environment:

$$\rho_S(t) = \operatorname{Tr}_E |\Psi_{SE}(t)\rangle\langle\Psi_{SE}(t)| = \sum_{i,j} c_i c_j^* |s_i\rangle\langle s_j| \langle \varepsilon_j(t)|\varepsilon_i(t)\rangle$$

As the environment states $|\varepsilon_i(t)\rangle$ become orthogonal over time ($\langle \varepsilon_j(t)|\varepsilon_i(t)\rangle \to \delta_{ij}$ for $t \gg \tau_D$), the off-diagonal terms vanish:

$$\rho_S(t \gg \tau_D) \approx \sum_i |c_i|^2 |s_i\rangle\langle s_i|$$

This is a **proper mixture** mathematically, but its interpretation differs from a classical probability distribution -- this is the core subtlety.

For a particle in a superposition of positions coupled to a thermal environment, the **decoherence rate** scales as:

$$\frac{1}{\tau_D} \sim \Lambda (\Delta x)^2$$

where $\Lambda$ is the **localization rate** that depends on the scattering cross-section and flux of environmental particles. For thermal photon scattering, $\Lambda \sim 10^{36}\ \text{cm}^{-2}\text{s}^{-1}$ at room temperature, explaining the fantastically short decoherence times for macroscopic superpositions.

The **predictability sieve** (Zurek) provides a criterion for identifying pointer states: they are the states that maximize the predictability of the system (minimize the entropy production rate). Equivalently, pointer states are eigenstates of observables that commute with the system-environment interaction Hamiltonian: $[|s_i\rangle\langle s_i|, H_{SE}] \approx 0$.

## Key results and implications

- Decoherence explains the **quantum-to-classical transition** in practice: it shows why macroscopic objects appear to be in definite states rather than superpositions, why certain observables (like position for massive objects) are "preferred," and why classical probability theory is an effective description of everyday phenomena.
- The pointer basis selected by decoherence corresponds to the observables that appear classical. For massive objects interacting via short-range forces, the pointer states are localized wave packets; this explains the classicality of position.
- Decoherence is the primary obstacle to building large-scale [[Quantum Computing Hardware|quantum computers]]: maintaining coherence across many qubits requires isolating them from the environment while still allowing controlled interactions. Quantum error correction is designed to combat decoherence.
- **Environment-induced superselection** (einselection) effectively restricts the observable algebra of the system to block-diagonal form in the pointer basis, mimicking a classical superselection rule without postulating one.

## Failure modes and limitations

- Decoherence does **not** solve the [[Interpretations of Quantum Mechanics|measurement problem]] by itself. After decoherence, the system-plus-environment is still in a superposition $\sum_i c_i |s_i\rangle |\varepsilon_i\rangle$ -- the global state is pure. Decoherence explains why we do not observe interference between branches, but it does not explain why one particular outcome is experienced. Within the Everett (many-worlds) interpretation, decoherence defines the branching structure; within collapse interpretations, decoherence must be supplemented by an additional collapse mechanism.
- A common error is claiming that decoherence "causes collapse." It does not. It produces a reduced density matrix that looks like a classical mixture, but the total state remains a pure superposition. The diagonal form of $\rho_S$ is consistent with both "one outcome occurred and we do not know which" and "all outcomes occurred in different branches."
- The Markovian (Lindblad) description breaks down when the environment has long correlation times or when system-environment correlations persist (non-Markovian dynamics). In such cases, coherence can partially revive.
- Decoherence times are model-dependent: the precise $\tau_D$ depends on detailed knowledge of the system-environment coupling, which is often known only approximately.

## Experimental evidence

- **Matter-wave interferometry**: Experiments with C$_{60}$ and larger molecules (Arndt and Zeilinger groups, Vienna) observe a gradual loss of interference fringe visibility as the molecules are heated or exposed to gas, in quantitative agreement with decoherence theory. These experiments demonstrate the transition from quantum to classical behavior as the effective coupling to the environment increases.
- **Superconducting qubits**: Decoherence times ($T_1$ for energy relaxation, $T_2$ for phase coherence) are directly measured in superconducting circuits. Modern transmon qubits achieve $T_2 \sim 100\ \mu\text{s}$ or more, and the decoherence mechanisms (photon loss, quasiparticle tunneling, TLS defects) are identified and systematically suppressed.
- **Quantum Darwinism tests**: Experiments with photonic systems (Ciampini et al., 2018) have verified that multiple observers accessing independent fragments of the environment obtain consistent information about the system state, as predicted by quantum Darwinism.
- **Cavity QED**: Haroche and colleagues (Nobel Prize 2012) tracked the decoherence of mesoscopic superposition states ("Schrodinger cat states") of the electromagnetic field in a high-Q microwave cavity, observing the progressive loss of coherence in real time in agreement with theory.

## Sources

- W. H. Zurek, "Decoherence, einselection, and the quantum origins of the classical," *Reviews of Modern Physics* **75**, 715 (2003).
- M. Schlosshauer, *Decoherence and the Quantum-to-Classical Transition*, Springer, 2007.
- E. Joos, H. D. Zeh, C. Kiefer, D. Giulini, J. Kupsch, and I.-O. Stamatescu, *Decoherence and the Appearance of a Classical World in Quantum Theory*, 2nd ed., Springer, 2003.

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

[[Physics Worldmap]] · [[Quantum Mechanics Map]] · [[POVMs and Quantum Instruments|← previous]] · [[Open Quantum Systems|next →]]
