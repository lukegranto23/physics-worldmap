---
type: "concept"
field: "Condensed Matter Physics"
epistemic_status: "active"
level: "advanced"
tags: ["physics", "field/condensed", "status/active", "level/advanced"]
aliases: ["Topologically Ordered Phase"]
created: 2026-07-30
updated: 2026-07-31
note_maturity: expanded
source_audit: bibliography-present-needs-claim-audit
---

# Topological Order

> [!summary] Core idea
> Long-range entanglement, fractional excitations, and topology-dependent degeneracy characterize phases beyond local symmetry breaking.

> [!note] Documentation status
> This expanded note includes a canonical bibliography but has not yet received a claim-by-claim source audit. The epistemic label describes the standing of the underlying physics in its stated regime; it does not certify every sentence or equation in this note.

## Mathematical handle

$\gamma_{\rm topo} = \ln \mathcal{D}$ in the entanglement entropy $S = \alpha L - \gamma_{\rm topo}$

The expression is an orientation point, not a substitute for checking assumptions, sign conventions, units, boundary conditions, and the regime in which it was derived.

## Epistemic status

**Active.** The core framework is established, while mechanisms, regimes, or quantitative closure remain active research.

## Place in the world map

- Domain: [[Condensed Matter Physics Map]]
- Field-level guiding question (context only): "How do symmetry, interactions, topology, and disorder determine phases?"
- Nearby concepts: [[Physics Worldmap]] · [[Condensed Matter Physics Map]] · [[Topological Insulators|← previous]] · [[Strongly Correlated Electrons|next →]]

## Physical content

### Wen's definition

Topological order, as defined by Wen (1990), characterizes quantum phases of matter that cannot be described by Landau's symmetry-breaking paradigm. A topologically ordered state has the following defining properties:

1. **Topology-dependent ground-state degeneracy.** The number of degenerate ground states depends on the topology of the spatial manifold -- for example, a $\mathbb{Z}_2$ topologically ordered state has a 4-fold degenerate ground state on a torus but a unique ground state on a sphere. This degeneracy is exact in the thermodynamic limit and cannot be lifted by any local perturbation.
2. **Robustness to local perturbations.** The ground-state degeneracy and the low-energy properties are stable against arbitrary local perturbations of the Hamiltonian, as long as the perturbation does not close the bulk gap. This robustness is the hallmark that distinguishes topological order from accidental degeneracies.
3. **No local order parameter.** No local observable can distinguish between the degenerate ground states. The different ground states on a torus are related by non-contractible loop operators -- global, topological operations -- and all local correlation functions are identical across the degenerate sectors.

These properties make topological order fundamentally invisible to the Landau-Ginzburg-Wilson framework, which diagnoses phases by local order parameters and their symmetries.

### Why no local order parameter works

The deep reason is that topologically ordered states are **long-range entangled** (LRE): they cannot be transformed into a product state by any finite-depth local unitary circuit. A conventional symmetry-breaking state (e.g. a ferromagnet) is short-range entangled -- a local unitary rotation can map it to a product state. Because no local measurement can detect the global entanglement pattern, no local order parameter can identify the phase.

### Topological entanglement entropy

The operational diagnostic for topological order is the **topological entanglement entropy** (Kitaev and Preskill, 2006; Levin and Wen, 2006). For a region $A$ with smooth boundary of length $L$ in a gapped, topologically ordered 2D ground state:

$$S(A) = \alpha L - \gamma + O(1/L)$$

where $\alpha$ is a non-universal area-law coefficient and $\gamma = \ln \mathcal{D}$ is a universal constant. The **total quantum dimension** $\mathcal{D} = \sqrt{\sum_a d_a^2}$ encodes the full anyon content of the phase, with $d_a$ the quantum dimension of anyon type $a$. For the toric code, $\mathcal{D} = 2$ (four anyons: $\{1, e, m, \epsilon = e \times m\}$, all with $d_a = 1$), giving $\gamma = \ln 2$. For the $\nu = 1/3$ Laughlin state, $\mathcal{D} = \sqrt{3}$.

The topological entanglement entropy $\gamma$ is a universal, quantitative fingerprint of topological order that can be extracted from numerical wave functions (exact diagonalization, DMRG, tensor networks) via the Kitaev-Preskill or Levin-Wen construction.

### Anyonic excitations

The elementary excitations of a topologically ordered phase are **anyons** -- quasiparticles with exchange statistics that are neither bosonic nor fermionic.

- **Abelian anyons**: exchanging two identical anyons multiplies the wave function by a phase $e^{i\theta}$ with $\theta \neq 0, \pi$. In the $\nu = 1/3$ Laughlin state, the quasiholes carry charge $e/3$ and exchange phase $\theta = \pi/3$. The outcome of exchanges depends only on the topology of the worldlines (which particle went around which), not on geometric details.
- **Non-Abelian anyons**: exchanging two anyons applies a unitary matrix to a degenerate state space. The dimension of this space grows exponentially with the number of anyons, and the matrix depends on the order of exchanges (braiding). Ising anyons (realized in the gapped phase of the Kitaev honeycomb model with time-reversal breaking, and predicted at $\nu = 5/2$) and Fibonacci anyons are the most studied cases. Fibonacci anyons are **universal** for quantum computation: any unitary gate can be approximated to arbitrary precision by braiding operations alone.

### Paradigmatic example: fractional quantum Hall effect

The fractional quantum Hall effect (FQHE) is the original and best-established realization of topological order. At Landau-level filling fraction $\nu = 1/3$, the ground state is described by the **Laughlin wave function**:

$$\Psi_{\rm Laughlin}(z_1, \ldots, z_N) = \prod_{i < j} (z_i - z_j)^3\, e^{-\sum_k |z_k|^2 / 4\ell_B^2}$$

where $z_k = x_k + iy_k$ are complex coordinates and $\ell_B = \sqrt{\hbar/eB}$ is the magnetic length. This state has all the hallmarks of topological order: 3-fold ground-state degeneracy on a torus, charge-$e/3$ quasihole excitations with fractional statistics, a quantized Hall conductance $\sigma_{xy} = \frac{1}{3}\frac{e^2}{h}$ robust to disorder, and topological entanglement entropy $\gamma = \frac{1}{2}\ln 3$. The FQHE at $\nu = 5/2$ is believed to host non-Abelian anyons described by the Moore-Read (Pfaffian) state.

### Toric code

Kitaev's toric code (2003) is the simplest exactly solvable lattice model with topological order. Spin-$1/2$ degrees of freedom live on the edges of a square lattice, and the Hamiltonian is:

$$H = -J_e \sum_{\text{vertices } v} A_v - J_m \sum_{\text{plaquettes } p} B_p$$

where $A_v = \prod_{j \in v} \sigma_j^x$ and $B_p = \prod_{j \in p} \sigma_j^z$ are mutually commuting stabilizer operators. The ground state satisfies $A_v = B_p = +1$ for all $v, p$. On a torus, the ground-state degeneracy is 4-fold, corresponding to the four topological sectors labeled by the eigenvalues of non-contractible Wilson loop operators.

The excitations are:
- **$e$-particles** (electric charges): created by violating $A_v = +1$ at a vertex. They are bosons.
- **$m$-particles** (magnetic fluxes / visons): created by violating $B_p = +1$ at a plaquette. They are bosons.
- **$\epsilon = e \times m$ (fermions)**: the composite of an $e$ and an $m$ particle is a fermion.

Crucially, $e$ and $m$ have nontrivial **mutual statistics**: transporting an $e$-particle around an $m$-particle produces a phase of $-1$ (semionic mutual statistics). This mutual statistics is the defining feature that makes the toric code topologically ordered -- it is impossible in any short-range entangled state.

### String-net condensation

Levin and Wen (2005) generalized the toric code to **string-net models**, which provide a systematic construction of all (doubled) topological orders in 2D. The degrees of freedom are "string types" living on the edges of a trivalent lattice, subject to branching rules given by a fusion category. When the strings condense -- when the ground state is an equal-weight superposition of all allowed string configurations -- the resulting phase has topological order. The anyon content is determined by the input fusion category. This framework unifies the FQHE, toric code, and doubled Chern-Simons theories within a single lattice construction and provides a concrete sense in which topological order arises from the condensation of extended objects.

### Entanglement spectrum

Li and Haldane (2008) showed that the **entanglement spectrum** -- the set of eigenvalues $\{\xi_i\}$ of the entanglement Hamiltonian $H_E = -\ln \rho_A$ -- provides a finer fingerprint of topological order than the entanglement entropy alone. For a fractional quantum Hall state, the low-lying entanglement spectrum matches the edge-state spectrum predicted by conformal field theory, counting states sector by sector. This bulk-edge correspondence via entanglement provides a practical tool for identifying topological order in numerical wave functions and distinguishing between competing candidate states.

### Connection to topological quantum computation

Topological order provides a physically motivated approach to fault-tolerant quantum computation. The idea (Kitaev, 2003; Freedman, Kitaev, Larsen, Wang, 2003) is to encode quantum information in the degenerate ground-state space of a topologically ordered system and manipulate it by braiding anyonic excitations. Because the degeneracy is topologically protected, the encoded information is immune to local noise without active error correction. The computational power depends on the anyon type: Abelian anyons (toric code) allow topological quantum memory but not universal computation; Ising anyons allow a restricted gate set that must be supplemented; Fibonacci anyons allow universal computation by braiding alone.

## Mathematical framework

The mathematical structure underlying topological order is a **modular tensor category** (MTC), which specifies:

- The set of anyon types $\{a, b, c, \ldots\}$ including the vacuum $1$.
- Fusion rules: $a \times b = \sum_c N_{ab}^c\, c$, where $N_{ab}^c$ are non-negative integers.
- The $S$-matrix: $S_{ab}$ encodes the mutual braiding statistics and determines the total quantum dimension via $\mathcal{D} = 1/S_{1a}$ for $a$ the vacuum.
- The $T$-matrix: $T_{aa} = e^{2\pi i h_a}$ encodes the topological spin (self-statistics) of anyon $a$.

The modular data $(S, T)$ completely characterizes the topological order and determines all universal physical quantities: ground-state degeneracy on genus-$g$ surfaces ($= |\{a\}|^g$ for Abelian theories), fusion rules, and braiding matrices.

For the toric code: the $S$-matrix is $S = \frac{1}{2}\begin{pmatrix} 1 & 1 & 1 & 1 \\ 1 & 1 & -1 & -1 \\ 1 & -1 & 1 & -1 \\ 1 & -1 & -1 & 1 \end{pmatrix}$ in the basis $\{1, e, m, \epsilon\}$.

## Key results and implications

- Topological order provides the first examples of quantum phases that lie outside the Landau symmetry-breaking classification: they have no local order parameter, no broken symmetry, yet are genuinely distinct from trivial phases.
- The fractional quantum Hall effect demonstrates topological order in nature: the quantized Hall conductance is measured to parts per billion, and fractional charge $e/3$ has been directly observed via shot-noise measurements (de Picciotto et al., 1997; Saminadayar et al., 1997).
- The toric code proves that topological order can exist in simple, local, exactly solvable Hamiltonians without external magnetic fields or Landau levels.
- String-net condensation provides a complete classification of bosonic topological orders in 2D, unifying seemingly disparate examples.
- The entanglement spectrum has become a standard diagnostic tool in numerical studies, capable of distinguishing topological phases that have the same symmetry.

## Failure modes and limitations

- **Finite temperature in 2D.** Topological order in two spatial dimensions is destroyed at any nonzero temperature in systems with local interactions. The reason is that anyonic excitations are thermally activated with a Boltzmann factor $e^{-\Delta/k_B T}$ and, once present, their uncontrolled braiding decoheres the topological ground-state space. The topological memory time decreases exponentially with system size divided by a temperature-dependent correlation length. This is a fundamental obstruction: 2D topological order is a zero-temperature phenomenon. (In 3D and higher, self-correcting topological memories are possible in principle.)
- A common misconception is confusing topological order with **symmetry-protected topological (SPT) phases** such as topological insulators. SPT phases have no anyonic excitations, no ground-state degeneracy on a torus, and no long-range entanglement -- they are short-range entangled states protected by symmetry. Topological order, by contrast, is intrinsic and persists even when all symmetries are explicitly broken.
- Identifying topological order experimentally is difficult because there is no local order parameter to measure. Smoking-gun evidence requires detecting fractional charge, fractional statistics, or topology-dependent ground-state degeneracy -- all non-local properties.
- Numerical identification of topological order on finite systems is complicated by finite-size corrections to $\gamma$ and by the exponentially small energy splittings between topological sectors.

## Experimental evidence

- **Fractional quantum Hall effect.** The $\nu = 1/3$ state (Tsui, Stormer, Gossard, 1982) is the paradigmatic topologically ordered phase. Fractional charge $e^* = e/3$ was measured via shot noise (de Picciotto et al., 1997). Fractional statistics have been probed in Fabry-Perot interferometry experiments (Nakamura et al., 2020), with results consistent with anyonic statistics at $\nu = 1/3$.
- **$\nu = 5/2$ state.** Thermal Hall conductance measurements (Banerjee et al., 2018) are consistent with the non-Abelian Pfaffian (or anti-Pfaffian) state, though the interpretation is debated. Interferometry experiments to directly test non-Abelian statistics are ongoing.
- **$\alpha$-RuCl$_3$.** In the field-induced paramagnetic phase above $\sim 7$ T, the reported half-quantized thermal Hall conductivity $\kappa_{xy}/T = (\pi/12)(k_B^2/\hbar)$ (Kasahara et al., 2018) was interpreted as evidence for chiral Majorana edge modes of a non-Abelian topological phase, though subsequent experiments have questioned the quantization and its origin.
- **Quantum simulation.** Toric-code Hamiltonians have been realized in small-scale quantum processors (Google Quantum AI, Satzinger et al., 2021), demonstrating the creation and braiding of $e$ and $m$ anyons, as well as the topological ground-state degeneracy.

## Sources

- X.-G. Wen, "Topological orders in rigid states," *International Journal of Modern Physics B* **4**, 239 (1990).
- X.-G. Wen, *Quantum Field Theory of Many-Body Systems*, Oxford University Press, 2004.
- A. Kitaev, "Fault-tolerant quantum computation by anyons," *Annals of Physics* **303**, 2 (2003).
- M. A. Levin and X.-G. Wen, "String-net condensation: A physical mechanism for topological phases," *Physical Review B* **71**, 045110 (2005).
- A. Kitaev and J. Preskill, "Topological entanglement entropy," *Physical Review Letters* **96**, 110404 (2006).
- M. Levin and X.-G. Wen, "Detecting topological order in a ground state wave function," *Physical Review Letters* **96**, 110405 (2006).

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

[[Physics Worldmap]] · [[Condensed Matter Physics Map]] · [[Topological Insulators|← previous]] · [[Strongly Correlated Electrons|next →]]
