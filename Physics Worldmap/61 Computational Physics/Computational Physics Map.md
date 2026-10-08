---
type: "map-of-content"
field: "Computational Physics"
epistemic_status: "mixed"
level: "all"
tags: ["physics", "map", "field/computational"]
aliases: []
created: 2026-07-30
updated: 2026-07-30
---

# Computational Physics Map

> [!abstract]
> Numerical representation, simulation, inference, verification, validation, and reproducible scientific software.

## Questions that organize the field

- Which discretization preserves the important invariants and scales?
- Is numerical error smaller than modeling and measurement uncertainty?
- How can algorithms be verified, validated, profiled, and reproduced?
- When do surrogate or learned models generalize beyond training data?

## Working principles

- Verification asks whether equations were solved correctly; validation asks whether the right equations were solved.
- Convergence, stability, conditioning, and conservation are first-class outputs.
- Use exact solutions, manufactured solutions, and independent implementations as tests.
- Save parameters, seeds, versions, and provenance with results.

## Canonical mathematical handles

- **Discretization error:** $e_h=C h^p+o(h^p)$ — Grid refinement estimates convergence order.
- **Condition number:** $\kappa(A)=\|A\|\|A^{-1}\|$ — Sensitivity limits achievable numerical accuracy.
- **Monte Carlo error:** $\sigma_{\bar f}\sim\sigma_f\sqrt{2\tau_{\rm int}/N}$ — Correlation reduces effective sample count.
- **Bayesian inverse:** $p(\theta\mid y)\propto p(y\mid\theta)p(\theta)$ — Simulation and inference combine in a generative model.

## Concept atlas

| Concept | Level | Status | One-line orientation |
|---|---:|---|---|
| [[Computational Modeling Workflow]] | introductory | established | A simulation workflow turns assumptions into equations, discretization, implementation, tests, results, and uncertainty-aware claims. |
| [[Floating Point Arithmetic]] | introductory | established | Finite binary representation introduces rounding, overflow, cancellation, and nonassociativity. |
| [[Conditioning and Stability]] | intermediate | established | Conditioning belongs to the problem; stability describes how an algorithm amplifies errors. |
| [[Root Finding]] | introductory | established | Bisection, Newton, secant, and safeguarded hybrids solve nonlinear scalar or vector equations with different guarantees. |
| [[Numerical Differentiation]] | introductory | established | Finite differences approximate derivatives but balance truncation against noise and roundoff. |
| [[Numerical Integration]] | introductory | established | Quadrature approximates integrals using weighted samples and adapts to smoothness and singular structure. |
| [[ODE Time Integration]] | introductory | established | Explicit, implicit, adaptive, and geometric integrators trade accuracy, stability, cost, and invariant preservation. |
| [[Symplectic Integrators]] | advanced | established | Symplectic methods preserve phase-space geometry and give bounded long-time energy error for Hamiltonian systems. |
| [[Boundary Value Solvers]] | intermediate | established | Shooting, finite difference, collocation, and finite element methods solve differential equations with spatial endpoint data. |
| [[Finite Difference Methods]] | intermediate | established | Grid stencils approximate differential operators with truncation error analyzed by Taylor expansion. |
| [[Finite Volume Methods]] | advanced | established | Fluxes across control-volume faces enforce discrete local conservation and handle shocks robustly. |
| [[Finite Element Methods]] | advanced | established | Weak formulations approximate fields with local basis functions on flexible meshes. |
| [[Spectral Methods]] | advanced | established | Global basis functions achieve rapid convergence for smooth solutions but require geometry and discontinuity care. |
| [[Linear Solvers]] | intermediate | established | Direct factorizations and iterative Krylov methods solve sparse or dense systems with preconditioning. |
| [[Eigenvalue Algorithms]] | intermediate | established | Power, Lanczos, Arnoldi, and dense decompositions extract modes, spectra, and stability information. |
| [[Fast Fourier Transform]] | introductory | established | The FFT computes discrete Fourier transforms in $O(N\log N)$, enabling spectral analysis and convolution. |
| [[Monte Carlo Integration]] | intermediate | established | Random or quasirandom samples estimate high-dimensional expectations with dimension-insensitive basic convergence. |
| [[Markov Chain Monte Carlo]] | advanced | established | A Markov chain with a target stationary distribution samples difficult probability landscapes after convergence diagnostics. |
| [[Molecular Dynamics]] | intermediate | established | Interacting particles are integrated through time to estimate dynamical and equilibrium properties under ensembles and force models. |
| [[Lattice Simulations]] | advanced | established | Fields or spins are discretized on a lattice for statistical and quantum many-body calculations. |
| [[N Body Simulation]] | intermediate | established | Gravitational or electrostatic many-body dynamics uses direct, tree, mesh, or hybrid force algorithms. |
| [[Computational Fluid Dynamics]] | advanced | active | CFD discretizes conservation laws with stability, conservation, turbulence, and boundary treatment central. |
| [[Parameter Estimation]] | intermediate | established | Optimization or posterior inference fits model parameters while accounting for noise, priors, and degeneracy. |
| [[Uncertainty Quantification]] | advanced | active | UQ propagates uncertain inputs, model discrepancy, numerical error, and observation noise into predictions. |
| [[Verification and Validation]] | introductory | established | Code verification checks implementation; solution verification estimates numerical error; validation compares model predictions with reality. |
| [[Reproducible Scientific Computing]] | introductory | established | Reproducibility records source, environment, parameters, random seeds, data lineage, and generated artifacts. |
| [[Physics Informed Machine Learning]] | advanced | active | Learning methods can embed symmetries, conservation, differential equations, and uncertainty, but do not replace validation. |
| [[Surrogate Models]] | advanced | active | Reduced or learned emulators approximate expensive forward models within a declared training domain and error budget. |
| [[Inverse Problems]] | advanced | established | Inverse problems infer hidden causes from indirect data and are often ill-posed without regularization or prior structure. |

## Frontier queue

- [ ] Exascale multiscale simulation and energy-efficient algorithms
- [ ] Differentiable simulation and uncertainty-aware inverse design
- [ ] Structure-preserving machine learning for physical systems
- [ ] Quantum algorithms with demonstrated scientific advantage
- [ ] Reproducibility and verification of large simulation campaigns

Current evidence and sources belong in [[Open Problems Dashboard]] and the individual frontier notes. A checked box means “reviewed recently,” never “solved.”

## Neighboring fields

[[Mathematics for Physics Map]] · [[Experimental Physics Map]] · [[Nonlinear Dynamics and Complex Systems Map]]

## Suggested study loop

1. Read the field questions, then explain them from memory.
2. Learn the introductory concepts and reproduce their limiting cases.
3. Derive at least one canonical equation from a variational, symmetry, or conservation principle.
4. Reproduce one landmark result computationally or from public data.
5. Audit one frontier claim: known facts, model dependence, discriminating observable, and next experiment.

## Navigation

[[Physics Worldmap]] · [[Learning Paths]] · [[Epistemic Status and Claim Hygiene]] · [[Synthesis Lab]]
