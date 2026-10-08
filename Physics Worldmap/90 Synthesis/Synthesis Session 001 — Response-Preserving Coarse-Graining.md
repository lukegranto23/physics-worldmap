---
type: synthesis-session
field: Cross-field
epistemic_status: speculative
level: advanced
tags: [physics, synthesis, coarse-graining, response, research-program]
created: 2026-07-30
updated: 2026-09-04
prior_art_audit: initial-not-exhaustive
---

# Synthesis Session 001 — Response-Preserving Coarse-Graining

> [!important] Status
> This is a **testable research program**, not a new established theory and not a claim of novelty. An initial literature audit finds close prior work for every ingredient. The potentially useful contribution is the combination and benchmark protocol.

[[Synthesis Lab]] · [[Renormalization as Compression Across Scales]] · [[Linear Response Theory]] · [[Deep Dive — Mori-Zwanzig Projection|Mori-Zwanzig Projection]] · [[Computational Lab Index]]

## 1. Pattern noticed across the map

Many fields replace a high-dimensional state with a smaller description:

- renormalization keeps long-distance variables;
- hydrodynamics keeps conserved densities and slow modes;
- Mori–Zwanzig projection produces resolved dynamics plus memory and noise;
- graph coarsening preserves selected Laplacian modes;
- reduced-order modeling preserves a response or invariant manifold;
- information bottlenecks preserve information about a chosen relevance variable;
- experimental design keeps observables that discriminate models.

All are answers to a hidden question:

> **Relevant for what future intervention or prediction?**

A reduced variable can reproduce a stationary distribution while failing the response to forcing. Conversely, a model can reproduce one impulse response while distorting equilibrium fluctuations, conservation, or rare events. The objective defining “relevance” must therefore be operational.

## 2. Established ingredients

The following are already literature, not inventions here:

1. Real-space mutual information can identify useful coarse variables and reproduce renormalization behavior in statistical systems: [Koch-Janusz and Ringel, Nature Physics 14, 578–582 (2018)](https://doi.org/10.1038/s41567-018-0081-4).
2. Information-bottleneck relevance has been connected analytically to low-scaling-dimension RG operators: [Gordon et al., Physical Review Letters 126, 240601 (2021)](https://doi.org/10.1103/PhysRevLett.126.240601).
3. Information-theoretic optimality criteria for real-space RG have been developed for clean and disordered systems: [Lenggenhager et al., Physical Review X 10, 011037 (2020)](https://doi.org/10.1103/PhysRevX.10.011037).
4. Past–future information bottlenecks connect predictive compression with system identification and model reduction: [Creutzig, Globerson, and Tishby, Physical Review E 79, 041925 (2009)](https://doi.org/10.1103/PhysRevE.79.041925).
5. Mori–Zwanzig projection has been used to derive non-Markovian closure models for under-resolved turbulence: [Parish and Duraisamy, Physical Review Fluids 2, 014604 (2017)](https://doi.org/10.1103/PhysRevFluids.2.014604).
6. Structure-preserving reduced models can retain Lagrangian and symplectic properties: [Carlberg, Tuminaro, and Boggs, SIAM Journal on Scientific Computing 37, B153–B184 (2015)](https://doi.org/10.1137/140959602).
7. Spectral graph coarsening and sparsification can preserve selected low graph-Laplacian structure: [Brissette, Huang, and Slota, SIAM Journal on Matrix Analysis and Applications 44, 1032–1046 (2023)](https://doi.org/10.1137/21M1458119) and [Babecki, Steinerberger, and Thomas, SIAM Journal on Discrete Mathematics 39, 449–483 (2025)](https://doi.org/10.1137/23M1610069).
8. Recent climate-emulator work emphasizes that matching stationary statistics does not guarantee correct forced response, and proposes response theory as an audit: [Falasca, Physical Review Research 7, 043314 (2025)](https://doi.org/10.1103/2f4r-k8lr).
9. Balanced truncation is a direct input/output model-reduction framework that ranks states by joint controllability and observability: [Moore, IEEE Transactions on Automatic Control 26, 17–32 (1981)](https://doi.org/10.1109/TAC.1981.1102568).
10. $\mathcal H_2$-optimal and transfer-function interpolation methods directly target forced input/output behavior: [Gugercin, Antoulas, and Beattie, SIAM Journal on Matrix Analysis and Applications 30, 609–638 (2008)](https://doi.org/10.1137/060666123).
11. Port-Hamiltonian and related reductions can preserve energy-based interconnection structure while reducing nonlinear dynamics: [Chaturantabut, Beattie, and Gugercin, SIAM Journal on Scientific Computing 38, B837–B865 (2016)](https://doi.org/10.1137/15M1055085).

The prior-art conclusion is strong: **neither “information-theoretic coarse-graining” nor “response-preserving, structure-aware model reduction” is new by itself.** Any contribution would have to be a precisely distinguished theorem, algorithm, physical regime, or benchmark result.

## 3. Candidate synthesis

Define a coarse representation $Z=C(X)$ of a fine state $X$. Optimize it against four physically distinct losses:

$$
\mathcal L
=
\lambda_{\rm stat}\mathcal L_{\rm stationary}
+\lambda_{\rm resp}\mathcal L_{\rm response}
+\lambda_{\rm struct}\mathcal L_{\rm structure}
+\lambda_{\rm mem}\mathcal L_{\rm memory}.
$$

The weighted sum above is only schematic. Each term must be normalized to a dimensionless held-out error; otherwise the $\lambda$ values make the result arbitrary. A Pareto comparison should be reported alongside any scalarized optimum.

### Stationary fidelity

Declare stationary observables $O_j$ and distributions $p(y)$ before fitting. One possible normalized loss is

$$
\mathcal L_{\rm stationary}
=D_{\rm JS}(p_{\rm red}(y),p_{\rm fine}(y))
+\sum_jw_j
\frac{(\langle O_j\rangle_{\rm red}-\langle O_j\rangle_{\rm fine})^2}
{s_j^2}.
$$

Here $s_j$ is a declared physical or sampling scale. Predictive information,

$$I(Z_t;Y_{t+\tau}),$$

is a distinct optional objective: it measures retained information about a specified future target, not stationary-distribution fidelity.

### Interventional response

Preserve a family of impulse or susceptibility kernels:

$$
\chi_{AB}(t)
=\left.\frac{\delta\langle A(t)\rangle}{\delta f_B(0)}\right|_{f=0}.
$$

The forcing family must be declared. A representation cannot preserve responses to arbitrary unknown interventions at fixed dimension.

For declared observables $A$, inputs $B$, and test forcings $f$, use a normalized held-out response loss such as

$$
\mathcal L_{\rm response}
=\sum_{A,B,f}w_{ABf}
\frac{\|\chi^{\rm red}_{AB,f}-\chi^{\rm fine}_{AB,f}\|_2^2}
{\|\chi^{\rm fine}_{AB,f}\|_2^2+\epsilon_{\rm scale}}.
$$

### Physical structure

Penalize violation of:

- symmetry equivariance;
- conservation laws and continuity equations;
- positivity and probability normalization;
- symplectic, metric, or detailed-balance structure where applicable;
- locality or controlled interaction range.

Each item needs a unitless violation metric. Examples include relative conservation drift, probability outside the physical domain, symmetry-equivariance residual, and change in the passivity or symplectic condition.

### Memory accounting

When unresolved variables feed back, allow a projection-dependent nonlinear memory form:

$$
\dot Z(t)
=F[Z(t)]
+\int_0^t\mathcal K[Z(s),t-s]\,ds
+\eta(t).
$$

The linear convolution $K(t-s)Z(s)$ is only a local linear ansatz. A Markov reduced model should be accepted only when residual memory is negligible on the target timescale or its prediction error is bounded. Comparisons must match **effective state order**: delay coordinates, recurrent hidden state, and explicit memory variables count toward model dimension.

## 4. Main hypothesis

> Given identical training trajectories, model-capacity budget, optimization budget, and effective state order, a coarse model trained with a declared response objective will reduce normalized error on held-out interventions relative to a data-matched stationary-only objective, without exceeding predeclared stationary-fidelity or structure-violation tolerances.

This is deliberately modest. It could be false where equilibrium relations or modal structure already determine response, the chosen state resolves every relevant slow variable, forced data add no useful information, or the response-aware objective merely overfits.

## 5. Falsifiable benchmark

Use four systems already represented in the vault.

### A. Coupled oscillator chain

Fine state: positions and momenta of every mass. The deterministic conservative version is a **transfer-function and structure test**, not a stationary-distribution test. A separate Langevin-bath version supplies a reproducible stationary ensemble.

Intervention: localized impulse or boundary drive.

Targets:

- low-frequency transfer functions;
- energy conservation;
- normal-mode frequencies and damping if added.

Baselines: block average, principal components, low normal modes, balanced truncation, $\mathcal H_2$ interpolation, and a structure-preserving Lagrangian or port-Hamiltonian projection.

### B. Heat or diffusion equation

Fine state: grid temperature. The deterministic version tests Green functions; a stochastically forced version is required if stationary-distribution fidelity is scored.

Intervention: localized heat pulse or boundary-temperature step.

Targets:

- Green function at held-out sensor locations;
- heat balance including imposed boundary flux and source work;
- positivity and monotonic decay.

### C. Two-dimensional Ising dynamics

Fine state: spins with single-spin-flip Glauber dynamics so magnetization is not conserved.

Linear-response intervention: a small field pulse or small boundary field. A finite temperature quench is a separately scored nonlinear, nonstationary benchmark and must not be pooled with the susceptibility test.

Targets:

- magnetization response;
- correlation length and relaxation time;
- equilibrium distribution and fluctuation–response consistency.

Baselines: block spin, majority rule, PCA-like embeddings, real-space mutual information.

### D. High-dimensional chaotic flow

Use Lorenz-96 or a discretized Burgers/fluid system as the headline coarse-graining test. The included three-variable Lorenz-63 lab is only a pipeline check because it offers little meaningful dimensional reduction.

Intervention: small time-dependent perturbation to a parameter or state component.

Targets:

- ensemble response, not individual long-horizon trajectories;
- invariant distribution;
- finite-time prediction and uncertainty calibration.

## 6. Pre-registered decision rule

Before opening held-out results, freeze per-system observables, forcing distributions, effective state order, tolerances, bootstrap procedure, and aggregation rule. For each method:

1. give every method the **same unforced and forced trajectories**; vary only the objective or reduction rule;
2. match trainable parameters, latent plus memory state order, optimization steps, and tuning budget;
3. include data-matched rollout, balanced-truncation/$\mathcal H_2$, spectral, and structure-preserving baselines where applicable;
4. label held-out forcings as interpolation or extrapolation in amplitude, frequency, location, and shape;
5. measure normalized stationary, response, structure, and cost metrics over seeds and finite-data budgets.

### Provisional quantitative rule

Pilot runs may set physically defensible scales, after which thresholds are frozen. A concrete initial rule is:

- median held-out response error improves by at least 20% relative to the strongest data-matched baseline;
- a paired 95% bootstrap confidence interval for improvement excludes zero;
- stationary error worsens by no more than 5% relative, not five percentage points;
- relative conserved-balance residual remains below $10^{-3}$ where the fine solver satisfies that scale;
- positivity, probability normalization, and declared symmetry constraints have zero hard violations;
- success occurs in at least three of four systems, including one stochastic and one deterministic system, with no system showing more than 10% response degradation.

The synthesis is rejected under this rule if those conditions fail. The numeric thresholds are placeholders until a pilot establishes resolution and sampling floors; changing them after held-out evaluation invalidates the preregistration.

The benchmark is successful even if the hypothesis fails, because it distinguishes when stationary compression is sufficient from when response-aware or memory-aware reduction is needed.

## 7. Likely outcomes and interpretations

| Outcome | Interpretation |
|---|---|
| stationary and response objectives choose the same variables | candidate evidence that equilibrium or modal structure is sufficient; verify across forcings and seeds |
| response objective adds another mode | candidate response-relevant direction; test variance, controllability, and causal intervention before interpreting it |
| matched memory model outperforms a Markov model | candidate evidence for unresolved feedback; rule out extra capacity, optimization, and misspecification first |
| response improves but conservation breaks | the representation is predictive but physically unsafe outside the training envelope |
| no method transfers to held-out forcing | latent dimension, forcing family, or assumed closure is inadequate |

## 8. Stronger speculative extension

One could search for a **minimal intervention-complete state**: the smallest representation sufficient to predict a specified algebra of future observables under a specified algebra of interventions, within an error tolerance.

That phrase resembles sufficient statistics, predictive-state representations, causal states, control-theoretic realization, and information bottlenecks. A genuine contribution would require proving a new relation among those frameworks or demonstrating a physical regime where the combined constraints yield a previously inaccessible prediction.

## 9. Pilot outcome — September 4, 2026

[[Benchmark 001 — Equilibrium Versus Forced Response]] implements one exact thermal two-oscillator pilot with frozen settings, a one-parameter response fit, a balanced-truncation reference, held-out frequency/pulse/chirp tests, and 32 passing implementation checks. Response fitting improves pulse/chirp errors by about 27%/26% against the declared stationary tie-break without changing the observed equilibrium marginal. The full-information balanced reference is much stronger on response, with nonzero equilibrium error.

This is not an equal-data multi-system study, evidence of novelty, or a pass of the provisional quantitative rule above. The exact memory susceptibility is an algebraic reference, not a state-matched competitor. See the benchmark for data access, checks, and the untested next protocol.

### Information boundary added September 4

[[Benchmark 002 — The Sampling Boundary of Prediction]] shows why a pre-intervention warning needs explicit sensor, sampling, and parameter assumptions. Three thermal oscillators with unknown masses have the same regularly sampled position law but different forced responses. This is a constructive instance of known aliasing, not a new theorem, and it does not apply to the known-mass information setting of Benchmark 001. [[Research Frontier — Identifiability Before Discovery]] records the resulting research gates.

### Finite-data control added September 4

[[Benchmark 003 — Noisy Measurements and False Confidence]] evaluates noisy observation timing and a known-candidate confidence set. Designed measurements improve discrimination within the specified family, but excluding the true model causes false reassurance. A family-rejection test is still needed. This is not the original matched-capacity multi-system study or a reproduction of a thermal-memory-learning method.

### Family-rejection control added September 4

[[Benchmark 004 — Rejecting Inadequate Models]] implements two controlled family-rejection checks on fresh omitted-model cases. The checks catch several mismatches but mostly miss a small near-resonance detuning with large response error. Observation-space model adequacy and operational response accuracy remain distinct. The original four-system hypothesis is still unevaluated.

### Detection-limit audit added September 4

[[Benchmark 005 — Information Limits and Better Measurements]] compares information bounds, a known-alternative oracle, practical checks, and local-Fisher timing on fresh parameters. Some cases are information-limited; one practical detection rate rises from 4.24% to 93.12% with changed timing. This remains a restricted Gaussian observation study, not the full multi-system response-preservation hypothesis.

### Unknown-shift and cost audit added September 4

[[Benchmark 006 — Unknown Shifts and Misfocused Tests]] adds alternative-blind tests, finite-grid range design, and a declared time-cost proxy. Better coverage of some frequency shifts trades off local sensitivity. A pure damping change produces roughly 20% reference-response error while the fixed-mixture detector's rejection probability tends to zero with increasing data; [[When More Data Cannot Rescue a Misfocused Test]] records the assumptions and derivation. Sensor calibration errors can instead produce strong rejection without altered physical response. These results refine the warning problem but do not complete the original multi-system reduction study.

### Calibration and attribution audit added September 4

[[Benchmark 007 — Calibration Before Physical Attribution]] adds a frozen independent-calibration comparison with nuisance-aware warnings. Calibration helps detect one decay change at fixed reading budget, but transfer failure invalidates physical attribution. [[Sensor Correlations and the Boundary of Physical Attribution]] gives an exact sensor-versus-dynamics ambiguity and a response-uncertainty lower bound for the declared independent-pair experiment. This refines the measurement assumptions needed for a response certificate; it does not reproduce an unknown-memory method or complete the original multi-system hypothesis.

### Matched-lag calibration added September 5

[[Benchmark 008 — Matched-Lag Calibration]] tests the measurement proposed by Benchmark 007. Paired zero-reference observations at the dynamic lags separate constructed sensor/dynamics twins when their calibration law transfers; isolated calibration cannot. [[Matched-Condition Calibration]] records the transfer assumption and power cost. This closes one linear-Gaussian control but not the memory-reconstruction, nonlinear, or multi-system gates.

## 10. Next action

- [x] Implement a limited, exact oscillator pilot and report its negative as well as positive findings.

- [ ] Add impulse-response output to the coupled-oscillator and heat labs.
- [ ] Implement block, spectral, balanced-truncation/$\mathcal H_2$, structure-preserving, and response-aware reductions with matched effective state order and training data.
- [ ] Measure memory kernels or residual autocorrelation.
- [ ] Add a literature matrix comparing objective, symmetry, intervention class, and guarantees.
- [ ] Do not use the word “new” until the literature matrix and benchmark reveal a specific difference.
