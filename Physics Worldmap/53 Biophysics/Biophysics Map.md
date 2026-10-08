---
type: "map-of-content"
field: "Biophysics"
epistemic_status: "mixed"
level: "all"
tags: ["physics", "map", "field/biophysics"]
aliases: []
created: 2026-07-30
updated: 2026-07-30
---

# Biophysics Map

> [!abstract]
> Physical principles of molecules, cells, organisms, neural systems, evolution, and living nonequilibrium matter.

## Questions that organize the field

- How do molecular fluctuations produce reliable biological function?
- How do energy, information, mechanics, and control interact in living systems?
- Which collective principles span scales from proteins to populations?
- What distinguishes living active matter from generic driven matter?

## Working principles

- Thermal fluctuations, chemical free energy, and finite copy numbers matter.
- Biological function is conditional on environment, evolution, and control architecture.
- Separate descriptive fits from mechanistic and causal models.
- Connect models to perturbations, not only correlations.

## Canonical mathematical handles

- **Chemical kinetics:** $\dot c_i=\sum_r\nu_{ir}v_r(c)$ — Reaction networks transform concentrations.
- **Diffusion:** $\partial_tc=D\nabla^2c$ — Molecules spread by random motion.
- **Membrane potential:** $C_m\dot V=-\sum_i I_i+I_{\rm ext}$ — Capacitance and ionic currents govern voltage.
- **Fitness dynamics:** $\dot x_i=x_i(f_i-\bar f)$ — Relative reproductive success changes population fractions.

## Concept atlas

| Concept | Level | Status | One-line orientation |
|---|---:|---|---|
| [[Thermal Fluctuations in Biology]] | introductory | established | At cellular scales, energies often compete with $k_BT$, making stochastic dynamics functionally important. |
| [[Biomolecular Forces]] | intermediate | established | Electrostatics, hydrogen bonding, hydrophobic effects, dispersion, sterics, and entropy shape molecular structure and recognition. |
| [[Protein Folding]] | intermediate | active | Amino-acid sequence and environment define a rugged free-energy landscape over conformations and kinetics. |
| [[Molecular Motors]] | advanced | active | Motor proteins couple chemical free energy to directed motion through stochastic mechanochemical cycles. |
| [[Diffusion Limited Processes]] | intermediate | established | Search, binding, transport, and reaction times are constrained by Brownian motion and geometry. |
| [[Reaction Diffusion in Biology]] | intermediate | established | Local biochemical reactions coupled to molecular transport generate gradients, waves, and patterns. |
| [[Gene Regulatory Networks]] | intermediate | active | Genes and regulators form noisy nonlinear networks with feedback, switching, and information processing. |
| [[Stochastic Gene Expression]] | advanced | established | Finite molecular counts produce intrinsic noise, bursts, and heterogeneous cell states. |
| [[Chemical Master Equation]] | advanced | established | Discrete reaction probabilities evolve through gain and loss terms over molecular-count states. |
| [[Biological Membranes]] | intermediate | established | Lipid bilayers self-assemble into flexible selective boundaries hosting transport, signaling, and force generation. |
| [[Ion Channels and Membrane Voltage]] | intermediate | established | Selective channels and pumps create electrochemical gradients and nonlinear electrical dynamics. |
| [[Hodgkin Huxley Model]] | advanced | established | Voltage-gated conductances reproduce action-potential initiation and propagation with empirical gating kinetics. |
| [[Neural Coding]] | advanced | active | Neural systems represent and transform information through spike timing, rates, populations, and dynamics. |
| [[Sensory Adaptation]] | intermediate | active | Feedback adjusts response range and can approximately preserve sensitivity across background levels. |
| [[Morphogenesis]] | advanced | active | Gene regulation, mechanics, transport, growth, and active forces create reproducible biological form. |
| [[Cytoskeleton Mechanics]] | advanced | active | Actin, microtubules, motors, crosslinkers, and membranes generate force, shape, transport, and division. |
| [[Collective Cell Migration]] | advanced | active | Cells coordinate adhesion, polarity, force transmission, and chemical cues to move as groups. |
| [[Population Dynamics]] | introductory | established | Birth, death, competition, dispersal, and environmental variation shape population trajectories. |
| [[Evolutionary Dynamics]] | intermediate | established | Mutation, selection, drift, recombination, and ecology change heritable distributions over generations. |
| [[Fitness Landscapes]] | intermediate | active | Genotype or phenotype maps to context-dependent reproductive success, with epistasis shaping accessible paths. |
| [[Epidemiological Dynamics]] | introductory | established | Compartment, network, and agent models link transmission, recovery, immunity, behavior, and intervention. |
| [[Origin of Life Physics]] | advanced | open | Research seeks pathways from driven chemistry to compartmentalized, self-maintaining, heritable, evolvable systems. |

## Frontier queue

- [ ] Physical principles of cellular organization and phase separation
- [ ] Predictive protein folding, dynamics, and design
- [ ] Neural computation across scales
- [ ] Thermodynamic limits of sensing, adaptation, and replication
- [ ] Origin of life and transitions to evolvable self-maintaining systems
- [x] Measurement artefacts in the cell speed–persistence coupling: [[Benchmark 019 — Localization Noise and the Speed-Persistence Coupling]], [[Benchmark 020 — In Vitro T Cells and the Noise Margin of Speed-Persistence Coupling]], [[Benchmark 021 — Calibrating Localization Error in Zebrafish T-Cell Tracks]]

Current evidence and sources belong in [[Open Problems Dashboard]] and the individual frontier notes. A checked box means “reviewed recently,” never “solved.”

## Neighboring fields

[[Soft Matter Map]] · [[Statistical Physics Map]] · [[Nonlinear Dynamics and Complex Systems Map]] · [[Thermodynamics Map]]

## Suggested study loop

1. Read the field questions, then explain them from memory.
2. Learn the introductory concepts and reproduce their limiting cases.
3. Derive at least one canonical equation from a variational, symmetry, or conservation principle.
4. Reproduce one landmark result computationally or from public data.
5. Audit one frontier claim: known facts, model dependence, discriminating observable, and next experiment.

## Navigation

[[Physics Worldmap]] · [[Learning Paths]] · [[Epistemic Status and Claim Hygiene]] · [[Synthesis Lab]]
