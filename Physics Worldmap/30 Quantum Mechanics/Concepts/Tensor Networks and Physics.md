---
type: "concept"
field: "Quantum Mechanics"
epistemic_status: "mixed"
level: "advanced"
tags: ["physics", "field/quantum", "status/mixed", "level/advanced"]
aliases: ["tensor networks", "MPS", "DMRG", "MERA", "PEPS"]
created: 2026-07-30
updated: 2026-09-04
note_maturity: expanded
source_audit: bibliography-present-needs-claim-audit
---

# Tensor Networks and Physics

> [!summary] Core idea
> Tensor networks are structured decompositions of many-body quantum states and operators that exploit entanglement patterns for efficient representation, simulation, and -- remarkably -- provide a geometric language connecting quantum information to spacetime.

> [!note] Documentation status
> This expanded note includes a canonical bibliography but has not yet received a claim-by-claim source audit. The epistemic label describes the standing of the underlying physics in its stated regime; it does not certify every sentence or equation in this note.

## Why this matters

A generic state of $n$ qubits requires $2^n$ amplitudes. Tensor networks exploit special entanglement structure, especially in low-dimensional ground states. Many physically relevant states, including long-time entangled states, still require prohibitively large bond dimensions. Their use in holography is model-dependent, not a general derivation of gravity.

## Mathematical framework

### Tensor network basics

A rank-$k$ tensor $T_{i_1 i_2 \cdots i_k}$ is contracted with other tensors by summing over shared indices. A tensor network is a graph whose nodes are tensors and whose edges represent index contractions. The "physical" (open) indices label the Hilbert space; the "bond" (contracted) indices have dimension $\chi$ called the **bond dimension**, controlling the expressiveness and cost.

### Matrix Product States (MPS)

For a 1D chain of $n$ sites with local Hilbert space dimension $d$:

$$|\Psi\rangle = \sum_{s_1, \ldots, s_n} A^{s_1}_{a_0 a_1} A^{s_2}_{a_1 a_2} \cdots A^{s_n}_{a_{n-1} a_n} |s_1 s_2 \cdots s_n\rangle$$

Each $A^{s_i}$ is a $\chi \times \chi$ matrix (for open boundary conditions, $A^{s_1}$ is $1 \times \chi$ and $A^{s_n}$ is $\chi \times 1$). The state is specified by $n d \chi^2$ parameters instead of $d^n$.

**Entanglement structure**: for any bipartition cutting one bond, the entanglement entropy is bounded by:

$$S \le \log \chi$$

This is an *area law*: in 1D, the "area" of a cut is a single point, so $S = O(1)$. Ground states of gapped 1D Hamiltonians satisfy area-law entanglement (Hastings, 2007), making MPS efficient representations.

### DMRG (Density Matrix Renormalization Group)

White's DMRG algorithm (1992) is, in modern language, a variational optimization over MPS. Given a Hamiltonian $H$:

$$E_{\mathrm{var}}(\chi) = \min_{|\Psi\rangle \in \text{MPS}_\chi} \frac{\langle \Psi|H|\Psi\rangle}{\langle \Psi|\Psi\rangle}$$

This variational minimum is an upper bound to the true ground energy, not generally equal to it at finite bond dimension. Optimization may find a local minimum. The optimization sweeps through the chain, locally updating one or two tensors at a time. Computational cost scales as $O(n d \chi^3)$. For gapped 1D systems, DMRG with moderate $\chi$ gives essentially exact ground-state energies and correlations. It is the gold standard for 1D quantum many-body physics.

### MERA (Multi-scale Entanglement Renormalization Ansatz)

Vidal's MERA (2007) is a hierarchical tensor network with two types of tensors at each scale:
- **Disentanglers** $u$: unitary tensors that remove short-range entanglement.
- **Isometries** $w$: coarse-graining tensors that reduce the number of sites.

The network has a tree-like structure with $O(\log n)$ layers. The state is:

$$|\Psi\rangle = \left(\prod_{\tau=1}^{T} \prod_i u_i^{(\tau)} \prod_j w_j^{(\tau)}\right) |0\rangle^{\otimes m}$$

**Entanglement structure**: MERA can represent states with *logarithmic* entanglement scaling, $S \sim \log L$, characteristic of critical (gapless) 1D systems. MPS can also approximate critical states with bond dimension growing with scale and desired accuracy; polynomial growth is not by itself inefficiency.

A cut bounds entropy by the sum of log bond dimensions. Saturation is not automatic for a generic MERA; exact minimal-cut equalities require special tensor/state constructions.

### PEPS (Projected Entangled Pair States)

For 2D systems, PEPS generalize MPS to a 2D lattice:

$$|\Psi\rangle = \sum_{\{s_i\}} \text{tTr}\!\left(\bigotimes_i A^{s_i}\right) |s_1 s_2 \cdots s_n\rangle$$

where $\text{tTr}$ denotes contraction of all virtual indices according to the lattice connectivity. Each tensor $A^{s_i}$ has one physical index and as many virtual indices as lattice neighbors (e.g., 4 for a square lattice). PEPS satisfy area-law entanglement in 2D by construction.

**Computational challenge**: exact contraction of a 2D PEPS is $\#P$-hard (Schuch et al., 2007). Approximate contraction methods (boundary MPS, corner transfer matrix, Monte Carlo) are used in practice.

### Operator representations

Tensor networks also represent operators. A **Matrix Product Operator (MPO)**:

$$O = \sum_{\{s_i, s'_i\}} W^{s_1 s'_1}_{b_0 b_1} W^{s_2 s'_2}_{b_1 b_2} \cdots W^{s_n s'_n}_{b_{n-1} b_n} |s_1 \cdots s_n\rangle\langle s'_1 \cdots s'_n|$$

MPOs efficiently represent many structured operators, but not arbitrary operators at fixed bond dimension. Time evolution can be performed by applying MPO approximations of $e^{-iHt}$ (TEBD, TDVP algorithms).

## Physical content

### Area-law entanglement and efficient representation

The central physical insight: nature's states are not generic. Ground states of local Hamiltonians have limited entanglement:

| System | Entanglement scaling | Best tensor network |
|---|---|---|
| Gapped 1D | $S \sim O(1)$ (area law) | MPS / DMRG |
| Critical 1D | $S \sim \frac{c}{3}\log L$ | MERA |
| Gapped 2D | $S \sim O(L)$ (area law) | PEPS |
| 2D states with a Fermi surface | often $S\sim L\log L$ | Requires growing bond dimension or specialized networks |

The area law for gapped 1D systems was proved by Hastings (2007). In higher dimensions, area-law proofs exist for free systems and specific models but not in full generality.

### Connection to holography: MERA and AdS geometry (Swingle, 2012)

Brian Swingle observed that the layered structure of MERA resembles a discretization of anti-de Sitter space:
- The layers of the MERA correspond to different radial depths in [[AdS-CFT Correspondence|AdS]].
- The physical (UV) indices sit on the boundary; the coarse-grained (IR) top tensor sits in the interior.
- Minimal network cuts provide entropy bounds and motivate an RT-like analogy, not an exact identity for generic MERA.
- The hyperbolic geometry of the network matches the hyperbolic geometry of an AdS time slice.

This connection is suggestive but approximate. The MERA is a discrete, finite-bond-dimension structure, while AdS/CFT involves continuous geometry with infinite degrees of freedom. The [[Quantum Error Correction and Gravity|HAPPY code]] of Pastawski-Yoshida-Harlow-Preskill (2015) made the QEC aspects more precise using perfect tensors on a hyperbolic tiling.

### Computational applications

**Condensed matter physics:**
- DMRG is the standard method for 1D quantum systems (spin chains, Hubbard models, topological phases).
- 2D PEPS and infinite PEPS (iPEPS) are used for frustrated magnets, Hubbard models, and topological order.
- MERA captures critical phenomena and conformal field theory data (central charge, scaling dimensions, OPE coefficients) directly from the tensor network.

**Lattice gauge theory:**
- Tensor network methods have been applied to lattice gauge theories (Schwinger model, $\mathbb{Z}_2$ and $U(1)$ gauge theories) where Monte Carlo methods suffer from sign problems.
- They provide access to real-time dynamics, finite-density phases, and entanglement properties of gauge theories.

**Quantum chemistry:**
- DMRG applied to the electronic structure problem treats strongly correlated molecular systems (transition metal complexes, bond-breaking, active spaces) where conventional methods fail.

**Machine learning:**
- Tensor network architectures (MPS classifiers, tree tensor networks) have been explored for supervised learning with interpretability and controlled expressiveness.

## Key results

- White (1992): DMRG algorithm, revolutionizing 1D quantum simulations.
- Hastings (2007): proof of area-law entanglement for gapped 1D systems.
- Vidal (2007): MERA ansatz for critical systems.
- Verstraete, Cirac (2004): PEPS formalism for 2D systems.
- Swingle (2012): MERA as a holographic geometry.
- Schuch, Wolf, Verstraete, Cirac (2007): computational hardness of contracting PEPS.
- Pastawski, Yoshida, Harlow, Preskill (2015): perfect tensor / holographic codes.

## Open questions

1. **2D efficiency.** Can PEPS contraction be made efficient enough for quantitative predictions in 2D strongly correlated systems at scale?
2. **Fermion sign problem.** Can tensor network methods reliably solve the 2D Hubbard model at physical doping (the key unsolved problem in condensed matter)?
3. **Time evolution.** Long-time dynamics causes entanglement growth; bond dimension must grow, eventually making simulation intractable. Can this be mitigated?
4. **Higher dimensions.** Contraction cost and error control become especially demanding in three and higher spatial dimensions.
5. **Holographic dynamics.** The MERA-AdS connection is kinematic (spatial geometry). Can tensor networks capture the dynamical aspects of gravity (time evolution, black hole formation)?
6. **Continuum limit.** Continuous MERA (cMERA) and continuous MPS (cMPS) aim to describe quantum field theories directly, with application-dependent efficiency and error control.

## Connection to other fields

- [[Quantum Entanglement]]: tensor networks are organized by entanglement patterns.
- [[Quantum Error Correction]] and [[Quantum Error Correction and Gravity]]: holographic codes are tensor networks.
- [[AdS-CFT Correspondence]]: MERA as a discrete model of AdS geometry.
- [[Holographic Principle]]: area-law entanglement is the physical basis of holographic bounds.
- [[Quantum Information]]: tensor networks are a core tool in quantum information science.
- [[Linear Algebra for Physics]]: tensor decomposition and contraction are the mathematical foundation.
- [[Condensed Matter Physics Map|Condensed Matter]]: primary computational application domain.

## Sources

- White, S. R. (1992). "Density matrix formulation for quantum renormalization groups." *Phys. Rev. Lett.* 69, 2863.
- Vidal, G. (2007). "Entanglement renormalization." *Phys. Rev. Lett.* 99, 220405. arXiv:cond-mat/0512165.
- Verstraete, F., Cirac, J. I. (2004). "Renormalization algorithms for quantum-many body systems in two and higher dimensions." arXiv:cond-mat/0407066.
- Swingle, B. (2012). "Entanglement renormalization and holography." *Phys. Rev. D* 86, 065007. arXiv:0905.1317.
- Orus, R. (2014). "A practical introduction to tensor networks." *Ann. Phys.* 349, 117. arXiv:1306.2164. (Review.)
- Cirac, J. I., Perez-Garcia, D., Schuch, N., Verstraete, F. (2021). "Matrix product states and projected entangled pair states." *Rev. Mod. Phys.* 93, 045003. arXiv:2011.12127. (Comprehensive review.)

## Epistemic status

**Established** as a computational tool: MPS/DMRG is the definitive method for 1D quantum systems, with rigorous mathematical foundations. **Active** regarding the connection to gravity: the MERA-holography link is suggestive and has produced concrete models (holographic codes), but a precise correspondence to continuum AdS/CFT is not established.

## Navigation

[[Physics Worldmap]] · [[Quantum Mechanics Map]] · [[Quantum Entanglement]] · [[Quantum Error Correction]] · [[Quantum Error Correction and Gravity]] · [[AdS-CFT Correspondence]] · [[Holographic Principle]]
