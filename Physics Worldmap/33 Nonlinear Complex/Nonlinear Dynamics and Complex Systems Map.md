---
type: "map-of-content"
field: "Nonlinear Dynamics and Complex Systems"
epistemic_status: "mixed"
level: "all"
tags: ["physics", "map", "field/nonlinear"]
aliases: []
created: 2026-07-30
updated: 2026-07-30
---

# Nonlinear Dynamics and Complex Systems Map

> [!abstract]
> Feedback, instability, chaos, synchronization, networks, patterns, adaptation, and multiscale collective behavior.

## Questions that organize the field

- Which qualitative behaviors are structurally stable?
- How do feedback and nonlinearity generate new scales and patterns?
- How do microscopic interactions create collective computation or adaptation?
- What can be predicted when trajectories are chaotic?

## Working principles

- Analyze fixed points and bifurcations before simulating trajectories.
- Separate deterministic chaos from stochastic noise.
- Seek dimensionless control parameters and order parameters.
- Quantify ensembles, invariants, and prediction horizons rather than overfitting individual paths.

## Canonical mathematical handles

- **Dynamical system:** $\dot{\mathbf x}=\mathbf f(\mathbf x;\mu)$ — State evolves under a parameterized vector field.
- **Linear stability:** $\dot{\delta x}=J\,\delta x$ — Jacobian eigenvalues control local perturbations.
- **Lyapunov exponent:** $\lambda=\lim_{t\to\infty}t^{-1}\ln(\delta(t)/\delta(0))$ — Positive lambda signals exponential sensitivity.
- **Reaction diffusion:** $\partial_t\mathbf u=D\nabla^2\mathbf u+\mathbf f(\mathbf u)$ — Local reactions and transport can form patterns.

## Concept atlas

| Concept | Level | Status | One-line orientation |
|---|---:|---|---|
| [[Dynamical Systems]] | introductory | established | A dynamical system specifies a state space and a rule for continuous or discrete evolution. |
| [[Phase Portraits]] | introductory | established | A phase portrait visualizes trajectories, invariant sets, flow direction, and long-time behavior in state space. |
| [[Fixed Points]] | introductory | established | Fixed points are states unchanged by evolution and organize nearby dynamics. |
| [[Linear Stability]] | intermediate | established | Eigenvalues of the Jacobian determine local growth, decay, rotation, and marginal directions near a fixed point. |
| [[Limit Cycles]] | intermediate | established | A limit cycle is an isolated periodic orbit that may attract or repel neighboring trajectories. |
| [[Bifurcations]] | intermediate | established | A bifurcation is a qualitative change in invariant sets or stability as parameters cross critical values. |
| [[Saddle Node Bifurcation]] | intermediate | established | A stable and unstable fixed point collide and annihilate at a fold. |
| [[Pitchfork Bifurcation]] | intermediate | established | A symmetry-changing instability creates or destroys symmetry-related fixed points. |
| [[Hopf Bifurcation]] | advanced | established | A conjugate eigenvalue pair crossing the imaginary axis creates or destroys a periodic orbit. |
| [[Deterministic Chaos]] | intermediate | established | Chaotic systems are deterministic yet exhibit bounded aperiodic behavior and exponential sensitivity to initial conditions. |
| [[Lyapunov Exponents]] | advanced | established | Lyapunov exponents measure asymptotic expansion or contraction rates of infinitesimal perturbations. |
| [[Strange Attractors]] | advanced | established | A strange attractor combines attracting dynamics with fractal geometry and chaotic motion. |
| [[Lorenz System]] | intermediate | established | A three-variable convection model exhibits fixed points, bifurcations, and a canonical chaotic attractor. |
| [[Logistic Map]] | introductory | established | A one-dimensional iterated map displays fixed points, period doubling, chaos, and universality. |
| [[Poincare Sections]] | advanced | established | A transversal slice converts continuous flow into a return map, exposing periodicity, tori, and chaos. |
| [[KAM Theory]] | advanced | established | Many invariant tori of a nondegenerate integrable Hamiltonian survive sufficiently small perturbations at incommensurate frequencies. |
| [[Synchronization]] | intermediate | established | Coupled oscillators can lock phases or frequencies through interaction despite heterogeneity. |
| [[Pattern Formation]] | advanced | established | Instabilities of homogeneous states generate spatial structure selected by nonlinear saturation and transport. |
| [[Turing Patterns]] | advanced | established | Different diffusion rates can destabilize a reaction equilibrium and create stationary spatial patterns. |
| [[Self Organized Criticality]] | advanced | active | Some slowly driven dissipative systems evolve toward scale-free avalanche statistics without fine parameter tuning. |
| [[Networks and Graph Dynamics]] | intermediate | established | Interactions on a graph couple local dynamics to degree, motifs, communities, and spectral structure. |
| [[Percolation]] | intermediate | established | Random connectivity undergoes a geometric transition where a system-spanning component appears. |
| [[Agent Based Models]] | introductory | active | Agent rules generate collective outcomes but require sensitivity analysis, calibration, and caution about identifiability. |
| [[Multiscale Complexity]] | advanced | open | Complex systems couple structures and dynamics across scales, often defeating single-level descriptions. |
| [[Causal Inference in Dynamical Systems]] | advanced | active | Interventions, temporal structure, and mechanistic constraints are needed to distinguish causation from correlation. |

## Frontier queue

- [ ] Predictability and control of high-dimensional chaos
- [ ] Causal emergence and effective macroscopic variables
- [ ] Collective intelligence in biological and artificial systems
- [ ] Multilayer network dynamics and systemic risk
- [ ] Universal structure in active and adaptive matter

Current evidence and sources belong in [[Open Problems Dashboard]] and the individual frontier notes. A checked box means “reviewed recently,” never “solved.”

## Neighboring fields

[[Statistical Physics Map]] · [[Biophysics Map]] · [[Fluid Dynamics Map]] · [[Computational Physics Map]]

## Suggested study loop

1. Read the field questions, then explain them from memory.
2. Learn the introductory concepts and reproduce their limiting cases.
3. Derive at least one canonical equation from a variational, symmetry, or conservation principle.
4. Reproduce one landmark result computationally or from public data.
5. Audit one frontier claim: known facts, model dependence, discriminating observable, and next experiment.

## Navigation

[[Physics Worldmap]] · [[Learning Paths]] · [[Epistemic Status and Claim Hygiene]] · [[Synthesis Lab]]
