---
type: "map-of-content"
field: "Statistical Physics"
epistemic_status: "mixed"
level: "all"
tags: ["physics", "map", "field/statistical"]
aliases: []
created: 2026-07-30
updated: 2026-07-30
---

# Statistical Physics Map

> [!abstract]
> How microscopic multiplicity, probability, interactions, and coarse-graining produce macroscopic laws and phases.

## Questions that organize the field

- Why do equilibrium ensembles work, and when do they fail?
- How do phase transitions and universality emerge from many degrees of freedom?
- How do systems relax, age, transport, or remain out of equilibrium?
- How are information and thermodynamic entropy related?

## Working principles

- Specify ensemble, constraints, conserved quantities, and thermodynamic limit.
- Entropy depends on macrostate and coarse-graining; probabilities depend on preparation.
- Correlation length and symmetry identify critical behavior.
- Nonequilibrium claims require timescale, driving, and bath assumptions.

## Canonical mathematical handles

- **Boltzmann entropy:** $S=k_B\ln\Omega$ — Multiplicity connects microstates to thermodynamic entropy.
- **Canonical distribution:** $p_i=e^{-\beta E_i}/Z$ — A subsystem equilibrated with a heat bath has Boltzmann weights.
- **Partition function:** $Z=\sum_i e^{-\beta E_i}$ — Thermodynamic potentials and moments derive from Z.
- **Fluctuation-dissipation:** $\chi''(\omega)\leftrightarrow\text{equilibrium correlations}$ — Response and spontaneous fluctuations are linked near equilibrium.

## Concept atlas

| Concept | Level | Status | One-line orientation |
|---|---:|---|---|
| [[Microstates Macrostates and Multiplicity]] | introductory | established | A macrostate groups many microscopic configurations consistent with chosen coarse observables. |
| [[Boltzmann Entropy]] | introductory | established | For an equiprobable macrostate, entropy is proportional to the logarithm of compatible microstates. |
| [[Gibbs Entropy]] | intermediate | established | The Gibbs entropy extends entropy to a probability distribution over microstates. |
| [[Ensembles]] | introductory | established | Microcanonical, canonical, and grand-canonical ensembles encode different idealized exchanges and constraints. |
| [[Ergodicity and Typicality]] | advanced | active | Ergodicity equates long-time and ensemble averages under conditions; typicality explains why most compatible states look macroscopicly alike. |
| [[Microcanonical Ensemble]] | intermediate | established | An isolated equilibrium system is modeled as uniform over states in a narrow energy shell. |
| [[Canonical Ensemble]] | introductory | established | A small system weakly coupled to a large heat bath has probabilities proportional to Boltzmann weights. |
| [[Grand Canonical Ensemble]] | intermediate | established | A subsystem exchanging energy and particles is governed by temperature and chemical potential. |
| [[Partition Functions]] | introductory | established | A partition function normalizes equilibrium weights and generates thermodynamic quantities through derivatives. |
| [[Classical Ideal Gas Statistics]] | introductory | established | Independent translational degrees of freedom yield the ideal-gas equation and Sackur-Tetrode entropy with quantum counting. |
| [[Maxwell Boltzmann Distribution]] | introductory | established | Classical equilibrium particle velocities follow a Gaussian component distribution and a characteristic speed distribution. |
| [[Bose Einstein Statistics]] | intermediate | established | Indistinguishable bosons have occupation numbers enhanced in already occupied states and can macroscopically condense. |
| [[Fermi Dirac Statistics]] | intermediate | established | Indistinguishable fermions obey exclusion and fill states up to a Fermi surface at low temperature. |
| [[Density of States]] | intermediate | established | The density of states counts available modes per energy interval and controls thermodynamics and transitions. |
| [[Fluctuations]] | intermediate | established | Equilibrium variances are related to response functions and scale subextensively away from criticality. |
| [[Correlation Functions]] | intermediate | established | Correlation functions quantify how fluctuations at different points and times co-vary and reveal characteristic scales. |
| [[Phase Transitions]] | intermediate | established | Thermodynamic phases change nonanalytically in an ideal infinite-system limit and sharply but smoothly in finite systems. |
| [[Order Parameters and Symmetry Breaking]] | intermediate | established | An order parameter distinguishes phases and may select one of symmetry-related equilibrium states. |
| [[Landau Theory]] | advanced | established | A symmetry-constrained free-energy expansion describes mean-field phase behavior near continuous transitions. |
| [[Critical Phenomena]] | advanced | established | Near a continuous transition, diverging correlation length produces scaling, large fluctuations, and universal exponents. |
| [[Renormalization Group]] | advanced | established | Coarse-graining followed by rescaling generates flows in theory space; fixed points explain universality and relevant variables. |
| [[Ising Model]] | intermediate | established | Binary spins with local coupling form a minimal model for collective ordering, criticality, and universality. |
| [[Random Walks and Diffusion]] | introductory | established | Independent increments produce mean-square displacement growing linearly with time and converge to diffusion. |
| [[Brownian Motion]] | intermediate | established | Thermal molecular impacts drive stochastic motion whose diffusion and drag are linked at equilibrium. |
| [[Langevin Equation]] | intermediate | established | Resolved variables evolve under deterministic drift plus random forcing with statistics determined by the bath model. |
| [[Fokker Planck Equation]] | advanced | established | A probability density for Markov diffusion evolves by drift and diffusion currents. |
| [[Linear Response Theory]] | advanced | established | Weak perturbations produce responses given by causal susceptibilities and equilibrium correlation functions. |
| [[Fluctuation Dissipation Theorem]] | advanced | established | Near equilibrium, spontaneous fluctuations determine the dissipative response to weak forcing. |
| [[Kinetic Theory]] | advanced | established | A distribution in phase space evolves through streaming, forces, and collisions and links microscopic scattering to transport. |
| [[Boltzmann Equation and H Theorem]] | advanced | established | Under molecular-chaos assumptions, dilute-gas kinetics approaches equilibrium with monotonic H functional. |
| [[Nonequilibrium Steady States]] | advanced | active | Persistent driving and dissipation maintain stationary probability currents and positive entropy production. |
| [[Fluctuation Theorems]] | advanced | established | Exact relations constrain probabilities of positive and negative entropy production over finite times under specified dynamics. |
| [[Glasses and Slow Dynamics]] | advanced | open | Disordered or frustrated systems fall out of equilibrium, age, and explore rugged state landscapes over broad timescales. |
| [[Eigenstate Thermalization Hypothesis]] | advanced | active | Hypothesis linking simple observables in typical chaotic eigenstates to thermal values; supported broadly, but not a universal theorem. |

## Frontier queue

- [ ] Universal principles far from equilibrium
- [ ] Glass transition and slow dynamics
- [ ] Many-body localization and thermalization boundaries
- [ ] Active matter and living nonequilibrium systems
- [ ] Information-theoretic coarse-graining and learned effective theories

Current evidence and sources belong in [[Open Problems Dashboard]] and the individual frontier notes. A checked box means “reviewed recently,” never “solved.”

## Neighboring fields

[[Thermodynamics Map]] · [[Nonlinear Dynamics and Complex Systems Map]] · [[Condensed Matter Physics Map]] · [[Biophysics Map]]

## Suggested study loop

1. Read the field questions, then explain them from memory.
2. Learn the introductory concepts and reproduce their limiting cases.
3. Derive at least one canonical equation from a variational, symmetry, or conservation principle.
4. Reproduce one landmark result computationally or from public data.
5. Audit one frontier claim: known facts, model dependence, discriminating observable, and next experiment.

## Navigation

[[Physics Worldmap]] · [[Learning Paths]] · [[Epistemic Status and Claim Hygiene]] · [[Synthesis Lab]]
