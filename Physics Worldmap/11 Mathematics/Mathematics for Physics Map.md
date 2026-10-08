---
type: "map-of-content"
field: "Mathematics for Physics"
epistemic_status: "mixed"
level: "all"
tags: ["physics", "map", "field/mathematics"]
aliases: []
created: 2026-07-30
updated: 2026-07-30
---

# Mathematics for Physics Map

> [!abstract]
> The reusable structures for expressing states, change, symmetry, geometry, uncertainty, and approximation.

## Questions that organize the field

- Which mathematical representation makes the physics simplest?
- What assumptions guarantee existence, uniqueness, stability, and convergence?
- Which invariants survive a change of coordinates or basis?
- What is exact, what is asymptotic, and what is numerical?

## Working principles

- Choose coordinates last; identify geometry and symmetry first.
- Track domains, boundary conditions, regularity, and convergence.
- Use dimensionless variables and limiting cases before computation.
- Distinguish formal manipulations from controlled theorems or approximations.

## Canonical mathematical handles

- **Eigenproblem:** $A\mathbf v=\lambda\mathbf v$ — Normal modes and stationary states reduce to spectral structure.
- **Fourier transform:** $\tilde f(k)=\int f(x)e^{-ikx}\,dx$ — Translations become phases and derivatives become multiplication.
- **Green function:** $L G(x,x')=\delta(x-x')$ — A linear response to a point source builds the general solution.
- **Variational derivative:** $\delta S/\delta\phi=0$ — Optimization in function space yields field equations.

## Concept atlas

| Concept | Level | Status | One-line orientation |
|---|---:|---|---|
| [[Scalars Vectors and Tensors]] | introductory | established | Scalars, vectors, covectors, and tensors are coordinate-independent objects represented by components that transform predictably. |
| [[Linear Algebra for Physics]] | introductory | established | Vector spaces, linear maps, bases, inner products, and decompositions organize superposition and coupled degrees of freedom. |
| [[Eigenvalues and Eigenvectors]] | introductory | established | Eigenvectors retain direction under a linear map; eigenvalues encode mode frequencies, energies, stability, or principal response. |
| [[Inner Product Spaces]] | intermediate | established | An inner product defines angles, norms, projections, orthogonality, and probability amplitudes in Hilbert space. |
| [[Vector Calculus]] | introductory | established | Gradient, divergence, curl, and integral theorems connect local change with flux and circulation. |
| [[Ordinary Differential Equations]] | introductory | established | ODEs describe finite-dimensional evolution; fixed points, conserved quantities, and stability reveal qualitative behavior. |
| [[Partial Differential Equations]] | intermediate | established | PDEs describe fields and are classified by propagation, diffusion, equilibrium, nonlinearity, and boundary data. |
| [[Boundary and Initial Value Problems]] | intermediate | established | Well-posed predictions require compatible data on appropriate temporal or spatial boundaries. |
| [[Fourier Analysis]] | intermediate | established | Fourier modes diagonalize translation-invariant linear systems and separate a signal by wavelength or frequency. |
| [[Laplace and Z Transforms]] | intermediate | established | Integral transforms convert differential or recurrence equations into algebraic equations with encoded boundary data. |
| [[Green Functions]] | advanced | established | A Green function is the inverse kernel of a linear operator subject to specified boundary and causal conditions. |
| [[Complex Analysis]] | intermediate | established | Analyticity, residues, and contour deformation evaluate integrals and encode causality, waves, and response. |
| [[Calculus of Variations]] | intermediate | established | Variations find stationary functions and yield Euler-Lagrange equations for mechanics, fields, optics, and optimization. |
| [[Distributions and Generalized Functions]] | advanced | established | Distributions make delta functions and weak derivatives rigorous and allow singular sources and Green functions. |
| [[Probability Theory]] | introductory | established | Random variables, measures, conditional probability, and limit theorems formalize uncertainty and ensembles. |
| [[Bayesian Inference]] | intermediate | established | Bayesian inference updates distributions over parameters and models using likelihoods and prior information. |
| [[Statistical Estimation]] | intermediate | established | Estimators are judged by bias, variance, consistency, efficiency, calibration, and robustness. |
| [[Stochastic Processes]] | intermediate | established | A stochastic process assigns correlated random variables across time or space; Markov, Gaussian, and jump processes are central cases. |
| [[Differential Geometry]] | advanced | established | Manifolds, metrics, connections, curvature, and differential forms express coordinate-free spacetime and gauge structure. |
| [[Differential Forms]] | advanced | established | Exterior calculus unifies gradients, fluxes, orientations, and integral theorems with coordinate-free objects. |
| [[Group Theory]] | intermediate | established | Groups encode composable symmetries; representations tell how states and observables transform. |
| [[Lie Groups and Lie Algebras]] | advanced | established | Continuous symmetries are generated infinitesimally by a Lie algebra whose commutators encode local structure. |
| [[Representation Theory]] | advanced | established | Irreducible representations classify elementary symmetry types, including spin, multiplets, and normal modes. |
| [[Topology for Physics]] | advanced | established | Topology studies global properties invariant under continuous deformation and explains defects, phases, and quantized indices. |
| [[Functional Analysis]] | advanced | established | Infinite-dimensional normed spaces and operators provide the analytic foundation for quantum theory and PDEs. |
| [[Information Theory]] | intermediate | established | Entropy, mutual information, and coding theorems quantify uncertainty, correlation, and compressibility. |
| [[Graphs and Networks]] | intermediate | established | Graphs capture relational structure; spectra, flows, paths, and communities connect topology to dynamics. |
| [[Perturbation Theory]] | intermediate | established | A solution is expanded about a tractable limit, with validity controlled by a small parameter and possible secular breakdown. |
| [[Asymptotic Analysis]] | advanced | established | Asymptotics extract leading behavior in a limit even when a series is divergent or nonuniform. |
| [[Multiple Scale Analysis]] | advanced | established | Separate slow and fast variables remove secular terms and capture modulated dynamics. |
| [[Special Functions]] | intermediate | established | Orthogonal polynomials and functions arise as eigenfunctions of canonical differential operators and geometries. |
| [[Numerical Linear Algebra]] | intermediate | established | Stable factorizations and iterative solvers make large discretized physics problems tractable. |
| [[Optimization and Inverse Problems]] | intermediate | established | Optimization infers causes or controls systems from incomplete noisy observations, usually with regularization. |
| [[Information Geometry]] | advanced | established | The Fisher information metric on a statistical manifold provides a coordinate-invariant notion of distinguishability between probability distributions, connecting statistics, geometry, and physics. |

## Frontier queue

- [ ] Rigorous foundations of quantum field theory in four dimensions
- [ ] Geometric and categorical structures behind dualities
- [ ] Turbulence regularity and nonlinear PDE behavior
- [ ] Certified numerical methods for multiscale physics
- [ ] Mathematics of learning, inference, and coarse-graining

Current evidence and sources belong in [[Open Problems Dashboard]] and the individual frontier notes. A checked box means “reviewed recently,” never “solved.”

## Neighboring fields

[[Foundations of Physics Map]] · [[Computational Physics Map]] · [[Nonlinear Dynamics and Complex Systems Map]]

## Suggested study loop

1. Read the field questions, then explain them from memory.
2. Learn the introductory concepts and reproduce their limiting cases.
3. Derive at least one canonical equation from a variational, symmetry, or conservation principle.
4. Reproduce one landmark result computationally or from public data.
5. Audit one frontier claim: known facts, model dependence, discriminating observable, and next experiment.

## Navigation

[[Physics Worldmap]] · [[Learning Paths]] · [[Epistemic Status and Claim Hygiene]] · [[Synthesis Lab]]
