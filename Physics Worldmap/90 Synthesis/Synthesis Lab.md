---
type: "synthesis-map"
field: "Physics"
epistemic_status: "mixed"
level: "all"
tags: ["synthesis", "research", "map"]
aliases: []
created: 2026-07-30
updated: 2026-09-18
---

# Synthesis Lab

This is where the vault tries to become more than an encyclopedia. Connections are promoted only when they preserve mechanisms, not merely vocabulary.

## Connection workflow

```mermaid
flowchart LR
  A["Structure in field A"] --> I["Invariant mathematical core"]
  B["Structure in field B"] --> I
  I --> D["Differences in degrees of freedom and regime"]
  D --> H["Candidate hypothesis"]
  H --> K["Consistency checks"]
  K --> P["Distinct observable prediction"]
  P --> F["Falsifier or experiment"]
  F --> U["Update connection ledger"]
```

## Active research boundary

[[Research Frontier — Identifiability Before Discovery]] records the current direction, prior-work screen, and gates before any contribution claim. [[Benchmark 002 — The Sampling Boundary of Prediction]] adds a verified thermal aliasing counterexample: sampled position laws can agree while continuous response differs. This is established system aliasing applied to our research question, not a new theory.

[[Benchmark 003 — Noisy Measurements and False Confidence]] adds 120,000 simulated dataset evaluations of noisy observation schedules. A standard Gaussian-distance design improves known-family identification but gives false singleton confidence when the true model is omitted. This separates candidate discrimination from checking whether the candidate family is adequate; no novelty is claimed.

[[Benchmark 004 — Rejecting Inadequate Models]] implements explicit family rejection with split-likelihood and concentration checks. Two observation lags detect several omitted systems, but a small near-resonance detuning still produces frequent false reassurance. The new question is whether this reflects measurement limits or test inefficiency.

[[Benchmark 005 — Information Limits and Better Measurements]] separates provably information-limited observations from settings helped by better timing. A standard local-Fisher lag raises one practical detection rate from 4.24% to 93.12%; an oracle comparison is retained with its extra-information caveat. No new detection theory is claimed.

[[Benchmark 006 — Unknown Shifts and Misfocused Tests]] compares four schedules and three standard tests without supplying the true frequency shift. Range timing helps some cases but sacrifices local sensitivity. [[When More Data Cannot Rescue a Misfocused Test]] derives why a fixed alternative list can have detection probability tending to zero despite a physically important mismatch.

[[Benchmark 007 — Calibration Before Physical Attribution]] adds independent calibration and continuous-noise nuisance control. One fixed-budget damping-detection rate rises from 15.10% to 89.83%, while calibration transfer failure invalidates physical attribution. [[Sensor Correlations and the Boundary of Physical Attribution]] constructs identical measured laws from changed dynamics or correlated sensor errors, with a 34.97% response discrepancy. This motivated the paired-calibration test in Benchmark 008; explicit response-set coverage remains unfinished.

[[Benchmark 008 — Matched-Lag Calibration]] performs that paired-calibration control. Isolated calibration gives the same physical warning for exact dynamic-law twins; matched-lag noise pairs separate their causes when calibration transfers. [[Matched-Condition Calibration]] records the broader experimental principle and its power–attribution tradeoff. The next gate is transfer beyond constructed Gaussian observations.

[[Benchmark 009 — Published Subdiffusion Memory Reproduction]] leaves the internally constructed detector loop. It independently reconstructs a published clean subdiffusion VACF and memory kernel, builds a verified regularized thermal covariance/noise factor, completes the final Lanczos transform with residual auditing, and reproduces the coarse-grid derivative control. [[Correlation-to-Memory Reconstruction from a VACF]] derives the bridge and its regularity/positivity limits. The paper's noisy molecular-dynamics and spectral-modification cases remain open.

[[Benchmark 010 — Noisy Memory and the Prediction Horizon]] adds a documented synthetic noise experiment: 104 of 800 datasets pass after order and time-window reduction, with 13 verification groups passed. The restricted implementation omits spectral repair, which dominates its rejections. A separate post-hoc analysis passes eight checks and exposes the clean model's eventual change from subdiffusion to ordinary diffusion. [[Finite Memory and the Return to Normal Diffusion]] explains why this established cutoff effect makes the intended prediction horizon part of the model specification.

[[Benchmark 011 — Finite Observations and Infinite-Time Claims]] completes an analytic comparison of fractional and tempered memory with 16 verification groups passed. Different eventual diffusion exponents can coexist with arbitrarily close laws for any fixed finite sampling schedule and repetition count. At $\epsilon=10^{-4}$, 4,096 independent trajectories with 20 samples each yield a detection-power upper bound of about 5.96% at a 5% false-positive limit on the declared schedule. This bound constrains every test in that Gaussian experiment; it is not an achieved rate or a novel physical mechanism. The next target is a prediction region on a declared finite domain.

[[Benchmark 012 — Acceleration Information and Certified Displacement]] implements that finite-time target using established spectral moment duals with explicit continuous-frequency corrections. Seventeen main verification groups passed across 24 inference datasets and 288 intervals, with a separate 20,000-dataset calibration audit. At $M=4096$, $T=6$, adding 256 independent ideal instantaneous acceleration readings gives a 77.20% median paired width reduction; this information-addition result is not cost-matched and does not resolve the broad $T=30$ uncertainty.

The fourteen-check post-hoc diagnostic sharpens the experimental boundary: ordinary finite-difference readings cannot replace instantaneous acceleration calibration. A passive thermal family with finite acceleration gives exactly the same sampled Gaussian velocity laws while hiding a much smaller displacement response. Eleven returned, deliberately miscalibrated intervals all miss that response; one declared trial is withheld after an unbounded-dual solver report; all twelve correct-bound controls include it. [[Acceleration Sum Rules and the Sampling Ambiguity]] states the assumptions and proof. [[Prior Art — Spectral Bounds and Physical Response]] makes clear that this is an application of established methods, not a genuine breakthrough. The live question is now how bandwidth-aware measurements buy reliable response information at a matched cost, and whether that survives real-data transfer.

[[Benchmark 013 — Camera Exposure and Response Uncertainty]] makes the observation operator explicit: a camera averages positions, not velocities. The accompanying [[Camera Exposure and Finite-Time Response Bounds]] removes the ideal acceleration assumption for a recorded-horizon target, derives conservative blur bounds and a sharp special case, and retains the known-velocity-variance requirement. A 480,000-dataset study passes 22 checks and exposes a practical tradeoff: protecting against calibration drift can leave too much uncertainty for a useful relative response claim. This is a synthetic measurement-bound result, not new physics. The next gate is external instrument feasibility and matched reference data, not repeated tuning on the same thermal aliases.

## Synthesis sessions

[[Instrument Feasibility — Response Bounds Before Data Claims]] now tests the physical scales and observation assumptions against two published instruments. [[Public Data Lead — Conditioned Hydrodynamic Brownian Motion]] identifies a newer public repository and connects conditioned displacement to standard Gaussian regression: conditioning can reveal a hidden contribution without adding information beyond the complete Gaussian observation law. The next work is a detector-matched reproduction, not a novelty claim; data acquisition and processing inspection remain open.

- [[Synthesis Session 001 — Response-Preserving Coarse-Graining]] — When does a coarse-grained model preserve selected causal response functions, not just stationary distributions? Four benchmark systems and pre-registered decision rules. **Status:** [[Benchmark 001 — Equilibrium Versus Forced Response|linear-Gaussian pilot completed]]; full four-system implementation and literature-complete comparison pending.
- [[Synthesis Session 002 — Holographic Coarse-Graining and the Memory of Spacetime]] — Can a properly defined reduced-dynamics memory diagnostic track an independently defined entropy milestone in a controlled finite model? The current toy calculation does not model evaporation, compute a black-hole Page curve, or evaluate a fully optimized channel measure. **Status:** exploratory question; earlier support claim withdrawn and diagnostics being redesigned.
- [[Synthesis Session 003 — RG Flow as Information Geometry and the Shape of Scale]] — Under what assumptions does a multi-coupling RG flow have a metric-gradient description, and when can a statistical Fisher metric be identified with the field-theory metric? A one-coupling alignment test is non-discriminating. **Status:** candidate program; needs multi-coupling flows, scheme controls, and comparison with the precise gradient formula.
- [[Synthesis Session 004 — The Geometry of Thermalization]] — What do endpoint distance, trajectory length, distinguishability contraction, and revivals each reveal about reduced-state dynamics? These quantities are related but not interchangeable. **Status:** exploratory numerical geometry; no Page-time or BLP identification claimed.

## Cross-domain connection notes

- [[Renormalization as Compression Across Scales]]
- [[Geometry of Dynamics and Inference]]
- [[Topological Defects Across Matter and Cosmology]]
- [[Fluctuation Response and Biological Sensing]]
- [[Horizons Effective Temperatures and Information]]
- [[Networks Transport and Collective Modes]]
- [[Frustrated Systems and Computational Hardness]]
- [[Quantum Darwinism and Holographic Encoding]]
- [[External Research Bridge — Imported Leads and Provenance]]

## Guardrails

- A shared equation may reflect a deep equivalence, a universality class, an approximation, or a superficial analogy. Identify which.
- A new variable must map to an observable.
- A proposed interaction must respect relevant symmetries and conservation laws.
- A model that can fit anything predicts nothing.
- “Not yet ruled out” is not evidence.
- Search the literature before calling an idea novel.
- A finite-size numerical coincidence is not a scaling law; report sensitivity to window, estimator, initial state, and model definition.
- Do not rename a proxy after the phenomenon it is meant to test. Define each observable operationally and state what it cannot establish.

Use [[Hypothesis Development Protocol]], [[Connection Ledger]], and [[Research Question Incubator]].
