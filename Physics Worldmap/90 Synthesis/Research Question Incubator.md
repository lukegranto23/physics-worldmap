---
type: "research-incubator"
field: "Physics"
epistemic_status: "speculative"
level: "all"
tags: ["synthesis", "questions"]
aliases: []
created: 2026-07-30
updated: 2026-07-30
---

# Research Question Incubator

These are **prompts**, not discoveries or claims of novelty.

## Prompt 1 — learned coarse-graining with physical guarantees

Can a coarse-graining map be optimized to preserve a chosen set of causal response functions while enforcing locality, symmetry, and a monotonic information measure? Benchmark it first on Ising, diffusion, and lattice-wave systems with known renormalization behavior.

**Discriminator:** out-of-distribution prediction of long-wavelength response, not reconstruction error.

## Prompt 2 — defect scaling in driven active media

Does a finite-rate transition in an active material exhibit a generalized Kibble-Zurek scaling whose exponents can be predicted from independently measured relaxation and correlation scales?

**Discriminator:** a pre-registered exponent relation across quench protocols, separated from coarsening after the transition.

## Prompt 3 — thermodynamic cost of adaptive sensing

Can the frequency-resolved violation of fluctuation-dissipation relations bound the information gain of an adaptive biochemical sensor more tightly than total entropy production alone?

**Discriminator:** simultaneous response, spontaneous-noise, chemical-work, and mutual-information measurements in a minimal synthetic circuit.

## Prompt 4 — topology-aware inverse design under loss

Can inverse design optimize a measurable transport objective while certifying that it is protected by a non-Hermitian or driven topological invariant over manufacturing uncertainty?

**Discriminator:** robustness scaling compared with equally optimized but topologically unconstrained designs.

## Prompt 5 — multiscale anomaly triage

Can dimensionless residual patterns across multiple experiments identify whether an anomaly is more consistent with calibration drift, missing effective operators, or incorrect boundary conditions?

**Discriminator:** blinded recovery of planted failure modes in synthetic and historical benchmark datasets.

## Prompt 6 — Mori-Zwanzig memory kernel in holographic models

Can a Mori-Zwanzig kernel and a channel-level non-Markovianity measure be computed for the same reduced observables in a controlled many-body model, and do either track an independently specified entropy milestone? A useful test must distinguish fixed-bipartition entanglement dynamics from an evaporation Page curve and must not identify a selected trace-distance revival with an optimized measure over the reduced channel.

**Discriminator:** pre-register the projection, observable, initial-state ensemble, memory statistic, entropy statistic, and observation window. A relation is credible only if it survives window changes, finite-size scaling, null models, and at least one model with a controlled gravitational interpretation. See [[Synthesis Session 002 — Holographic Coarse-Graining and the Memory of Spacetime]].

## Prompt 7 — sign-problem hardness and frustrated quantum magnets

Across a specified family of frustrated Hamiltonians, do representation-dependent QMC sign severity, NQS approximation error, NQS optimization failure, and bipartite entanglement complexity covary after basis and computational budget are controlled? Frustration itself does not guarantee a sign problem, topological order, or NQS failure, so each variable must be measured rather than inferred from the model label.

**Discriminator:** compare matched system sizes, bases, samplers, ansatz capacities, and optimization budgets across triangular, kagome, and $J_1$-$J_2$ benchmarks. Repeat in more than one basis and on held-out model families; report representation error separately from optimizer variance. See [[Frustrated Systems and Computational Hardness]].

## Prompt 8 — entanglement structure as a diagnostic for effective-theory completeness

In controlled holographic or lattice models, is the entanglement spectrum more sensitive than entropy alone to specified omissions from an effective description? Ryu-Takayanagi relates boundary entropy to an extremal-area term only within a holographic semiclassical regime; neither it nor an entanglement spectrum provides a general certificate that an effective theory is complete.

**Discriminator:** in a model with a known continuum limit, deliberately omit selected relevant or irrelevant operators, refit all remaining parameters, and compare held-out entropy spectra and ordinary correlators across lattice spacings. The proposal earns value only if the spectral statistic detects omissions that comparably precise correlators miss.

## Prompt 9 — emergent conservation laws from Mori-Zwanzig projection

Can projection-operator methods quantify the longevity of an approximately conserved observable when symmetry-breaking processes are present but parametrically slow? Projection does not create a conservation law: any long lifetime must ultimately follow from the microscopic generator, selection rules, scale separation, or suppressed rates.

**Discriminator:** begin with a solvable model containing a tunable weak symmetry-breaking rate. Derive its memory kernel and test whether the inferred slow pole and error bounds reproduce the exact relaxation timescale across temperature and coupling. Only then consider more complicated field-theory applications.

## Prompt 10 — quantum Darwinism and the holographic principle

Quantum Darwinism concerns redundant, classically accessible records of pointer observables in many environmental fragments. Holographic quantum error correction concerns reconstruction of a bulk operator algebra from authorized boundary regions. Can a common tensor-network model display both structures, and if so, under what state, channel, and observable restrictions?

**Discriminator:** encode a classical label and a quantum logical subsystem separately. Measure Holevo-accessible information about the label in many disjoint fragments, then measure logical-operator recovery fidelity for authorized regions. Mutual information alone is insufficient. If recovery occurs without redundant classical records—or records occur without logical recovery—the proposed equivalence fails. See [[Quantum Darwinism and Holographic Encoding]].

## Prompt 11 — RG flow as natural gradient descent on the Fisher manifold

When can an RG flow be represented as a metric-gradient flow, and when—if ever—does the relevant field-theory metric coincide with a Fisher metric estimated from a statistical ensemble? In two-dimensional QFT, the precise gradient formula can include correction and antisymmetric terms, schematically $\partial_i c=-(g_{ij}+\Delta g_{ij}+b_{ij})\beta^j$; this is not the blanket statement that every RG flow is Fisher natural-gradient descent. See the [Friedan–Konechny gradient formula](https://doi.org/10.1088/1751-8113/43/21/215401).

**Discriminator:** use at least two running couplings, estimate both candidate metrics in stated coordinates, and test the full gradient relation and its residuals under reparameterization. A one-coupling cosine is always $\pm1$ away from zeros and cannot discriminate the hypothesis. See [[Synthesis Session 003 — RG Flow as Information Geometry and the Shape of Scale]].

## Prompt 12 — robustness audit for memory and entropy proxies

How sensitive are the apparent memory-onset and entropy-turnover times in a finite interacting model to the observable, initial-state pair, subsystem, time grid, smoothing rule, and stopping window? This is a reproducibility question, not a finite-size confirmation exercise.

**Discriminator:** publish the complete sensitivity surface across those choices and compare against integrable, random-matrix, and Markovian null models. A candidate relationship advances only if a window-independent statistic has stable uncertainty, survives held-out choices, and is defined on a physical reduced channel. Computational Lab 14 is an exploratory implementation, not evidence for a Page-time identification.

## Navigation

- [[Physics Worldmap|Home]]
- [[Synthesis Lab|Synthesis lab]]
