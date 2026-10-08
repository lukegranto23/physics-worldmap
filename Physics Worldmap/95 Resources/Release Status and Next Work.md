---
type: guide
field: Physics
epistemic_status: reference
level: all
tags: [physics, release, maintenance, coverage]
created: 2026-09-04
updated: 2026-09-18
---

# Release Status and Next Work

## What is ready

This edition is a broad, navigable physics scaffold, not an exhaustive or fully source-audited encyclopedia. It contains 25 main field maps, 663 concept notes, 67 experiment/observation notes, 26 derivations, a 45-problem bank, reading routes, dated frontier reviews, and disciplined synthesis protocols. Counts exclude templates where relevant; the generated [[Vault Health Report]] supplies the live inventory.

The concept layer currently has **631 orientation stubs and 32 more-developed notes**. An epistemic label such as “established” describes the underlying subject in its stated regime, not the completeness or correctness of every sentence in the note. Most notes still need canonical-source and claim-level expansion.

## Foundation expansion

[[Mechanics to Statistical Physics — Foundation Study Route]] now connects six expanded notes: Lagrangian mechanics, Noether's theorem, Hamiltonian mechanics, Liouville's theorem, Gibbs entropy, and partition functions. Each includes assumptions, reconstructible mathematics, worked examples, caveats, and canonical references. Eight groups of independent calculation checks passed; six additional held-out exercises include hidden solutions. This reduces the introductory-stub count by six, without claiming full source certification.

The September 17–18 foundation checkpoint adds [[Electromagnetism — Fields Energy and Gauge Study Route]] and six expanded notes: Gauss's law, Faraday's law, Maxwell's equations, Poynting's theorem, electromagnetic waves, and gauge transformations. Fourteen independent calculation groups pass, with hashes tying the report to the checked sources. Six reconstruction exercises have hidden solutions; these are practice, not held-out evidence of mastery. The checks include deliberately wrong signs and the wrong fixed-voltage capacitor force obtained by omitting the voltage source. They validate selected examples, not all electromagnetism.

## Response-preservation pilot

[[Benchmark 001 — Equilibrium Versus Forced Response]] adds the first completed pilot for Session 001. A response-fitted oscillator matches the stationary observed marginal and reduces pulse/chirp errors by about 27%/26% against the equilibrium-only tie-break. A full-information balanced reference is substantially better on response, with some equilibrium error. All 32 numerical/algebraic checks passed. This is a limited exact-model demonstration, not the broader four-system validation or a new theory.

## Identifiability boundary

[[Benchmark 002 — The Sampling Boundary of Prediction]] constructs three thermal oscillators with identical regularly sampled equilibrium position laws and almost fourteen-fold variation in response amplitude to a declared force. All 31 checks passed. This is an example of established aliasing under unknown-mass, position-only assumptions, not a discovery or a general prohibition on prediction. [[Research Frontier — Identifiability Before Discovery]] records the updated direction and what remains unreproduced.

## Noisy measurement design

[[Benchmark 003 — Noisy Measurements and False Confidence]] extends the sampling example to finite noisy observations. A standard Gaussian-distance design makes 7 identification errors in 6,000 in-family trials at 32 pairs, but gives false singleton assurances in all 2,000 omitted-truth trials at 128 pairs. Eleven implementation checks passed across a 120,000-evaluation study. Results include uncertainty estimates and the missing-model failure; they are not a breakthrough or a general response guarantee. The next protocol must separate model discrimination from an independent family-adequacy check.

## Candidate-family rejection

[[Benchmark 004 — Rejecting Inadequate Models]] adds explicit “none of these models” checks using a published split-likelihood method and a concentration baseline. The 96,000-evaluation study catches several omitted systems with two observation lags, while mostly missing a 5% near-resonance detuning that causes about 146% response error. Eighteen implementation checks passed. The failure is retained as the next research target; no general response certificate is claimed.

## Information limits and measurement timing

[[Benchmark 005 — Information Limits and Better Measurements]] evaluates fresh detunings/noise levels. Analytic bounds put detection power below 50% in 17 of 54 declared observation settings. In another case, a standard sensitivity-based lag raises a practical check from 4.24% to 93.12% detection at the same reading count. Ten implementation checks passed. Oracle results carry explicit knowledge and calibration caveats; this is a controlled progress result, not a novel universal detector.

## Unknown-shift measurement design

[[Benchmark 006 — Unknown Shifts and Misfocused Tests]] adds a frozen 768,000-dataset comparison with no true-alternative oracle. Range-based timing improves some fresh shifts at equal reading count and under a declared time-cost proxy, but loses local sensitivity. Twenty-one implementation checks and three post-hoc diagnostic checks passed. [[When More Data Cannot Rescue a Misfocused Test]] explains an asymptotic failure of the fixed-mixture detector for a roughly 20% response mismatch. A sensor-only stress also causes strong rejection despite unchanged physical dynamics. No universal detector or novel physical law is claimed.

## Sensor calibration and attribution

[[Benchmark 007 — Calibration Before Physical Attribution]] adds 810,000 simulated dataset evaluations with costed independent calibration. In one fixed-reading-budget case, nuisance-aware damping-change detection rises from 15.10% to 89.83%. Calibration drift causes strong warnings without changed dynamics, and [[Sensor Correlations and the Boundary of Physical Attribution]] shows an exact ambiguity even with correctly calibrated marginal variance. Sixteen benchmark checks and twelve post-hoc algebraic checks passed. These are conditional measurement-model results, not proof of a universal detector or new physics.

## Matched-lag calibration

[[Benchmark 008 — Matched-Lag Calibration]] adds a 585,000-dataset, reading-budget-matched comparison. Isolated calibration cannot distinguish exact changed-dynamics and correlated-sensor twins. Paired noise calibration at the measurement lags separates the causes under a transfer assumption, while lowering physical-detection power under the broader sensor model. Twenty-seven checks passed. An invalid proposed covariance was caught and transparently amended before the accepted run. No hardware validation or universal attribution is claimed.

## Published thermal-memory baseline

[[Benchmark 009 — Published Subdiffusion Memory Reproduction]] adds a scoped independent reproduction of the clean $\tau=0.6$, $n=10$ subdiffusion case from Bockius et al. The moment identities, Newton constraint, stable realization, VACF, diagnostic kernel, sampled positive-real condition, regularized Riccati covariance, thermal noise-factor identity, final Lanczos invariants, and reported coarse-grid derivative passed twenty-nine checks. [[Correlation-to-Memory Reconstruction from a VACF]] records the derivation and structural limits. Spectral-modification cases, other parameter cases, the authors' code, and noisy molecular-dynamics examples are not yet reproduced.

## Noisy memory and the prediction horizon

[[Benchmark 010 — Noisy Memory and the Prediction Horizon]] adds 800 independently generated synthetic datasets, 5,504 logged fit attempts, and 104 accepted reconstructions after reducing order and the fitted time window. Thirteen verification groups passed. The restricted implementation omits the paper's spectral-repair branch, which dominates its rejections; this is not a reproduction of the paper's noisy molecular-dynamics experiment.

Eight additional checks passed in a post-hoc physical extrapolation audit of the saved matrices. The clean reference eventually predicts ordinary diffusion while the analytic target remains subdiffusive. [[Finite Memory and the Return to Normal Diffusion]] derives the precise conditions and exceptions for this established finite-memory effect. Finite-window accuracy and thermal admissibility do not alone certify the eventual transport law.

## Finite observations and infinite-time claims

[[Benchmark 011 — Finite Observations and Infinite-Time Claims]] completes an analytic and numerical comparison of established fractional and tempered-memory models. All 16 verification groups passed. At cutoff $\epsilon=10^{-4}$, 4,096 independent Gaussian trajectories with 20 samples each on $0,0.6,\ldots,11.4$ imply a detection-power upper bound of about 5.96% at a 5% false-positive limit, even with exact knowledge of both models. Their eventual diffusion exponents differ, although the finite sampled laws are close. The calculation is exploratory and the bound is not an achieved test rate, an experimental measurement, or a novelty claim. The general conclusion fixes the finite observation resources before taking the cutoff toward zero.

## Acceleration information and certified displacement

[[Benchmark 012 — Acceleration Information and Certified Displacement]] adds an application of established spectral moment bounds with Gaussian confidence calibration and explicit continuous-frequency corrections. Seventeen main verification groups passed. Twenty-four inference datasets yield 288 intervals across three information modes and four horizons; a separate 20,000-dataset audit checks the common confidence event. [[Prior Art — Spectral Bounds and Physical Response]] records the direct mathematical predecessors, and [[Acceleration Sum Rules and the Sampling Ambiguity]] derives the physical assumptions.

At $M=4096$ and $T=6$, 256 additional independent, ideal instantaneous acceleration readings reduce interval width by 77.20% at the median of paired comparisons. Known velocity variance, Gaussian observations, and the distinct acceleration observable are explicit requirements. This is not a matched-hardware or matched-cost improvement. Bounds remain broad at $T=30$, and the evaluated horizons do not constitute a numerical uniform-in-time certificate.

The post-hoc calibration diagnostic adds fourteen passing checks and retains a concrete failure. A passive thermal model with finite acceleration can have the same lattice-sampled velocity and finite-difference laws but a much smaller true displacement response. Deliberately transferring finite-difference variance into an instantaneous-acceleration upper bound produces eleven returned intervals that all miss the truth; one declared trial is withheld after an unbounded-dual solver report. All twelve correctly supplied physical-bound controls include the truth. The diagnostic tests a misuse of the calibration assumption, not a failure of the main result under its stated ideal readings.

No genuine breakthrough or new optimization method is claimed. The result redirects the next experiment toward sensor bandwidth, matched acquisition costs, and external-data validation.

## Camera exposure and calibration transfer

[[Benchmark 013 — Camera Exposure and Response Uncertainty]] adds 480,000 synthetic datasets, 1,440,000 interval attempts, and 22 passing verification groups for explicitly averaged position measurements. [[Camera Exposure and Finite-Time Response Bounds]] derives bounds without ideal acceleration readings, retaining known finite velocity variance and the equilibrium interpretation. It includes a sharp special case when exposure equals the target horizon, without claiming historical novelty.

All calibration readings are counted. Across in-scope cells, empirical coverage is 97.40–100%, with no misses on the common confidence event. A 20% unmodeled calibration drift reduces one exact-transfer coverage rate to 28.33%. An explicit ±20% allowance restores coverage in that tested cell, but the median interval width is about 158% of the small true response. A separate independent audit passes seventeen checks, recomputes every interval, and verifies the camera covariance by a different integral. The result is a conditional synthetic measurement study, not a usable camera guarantee or forecasting breakthrough. Instrument feasibility and external calibration/reference data are the next gate.

The September 18 feasibility checkpoint adds [[Instrument Feasibility — Response Bounds Before Data Claims]]: a conventional camera's broad allowance can be too loose to help, while optical velocity averaging cannot be substituted for camera exposure. [[Public Data Lead — Conditioned Hydrodynamic Brownian Motion]] identifies a public processed-data repository, records unresolved provenance/access details, and derives the standard Gaussian conditional-displacement baseline, including noisy and finite-bin selection. This is source review and mathematics, not a reproduced experiment.

## Public-data follow-ups (October 6–8)

[[Benchmark 014 — Preregistered Conditioned Brownian Reproduction]] reproduced the published conditioned $t^{5/2}$ on the digest-verified Dryad traces. Three follow-ups on the same files:

- **[[Benchmark 016 — Stratified Conditioning and an Estimator Artifact]].**
  - The empty-trap failure is slowly varying detector-noise power.
  - Most of the particle's ~3% shortfall is calibration transfer between trace halves. The in-sample residual is −0.8% ± 1.0%.
  - A preregistered "supported" verdict for the particle is withdrawn: an eight-seed stationary audit (lab 37) shows the primary variance proxy is itself biased.
- **[[Benchmark 015 — Gain-Free Test of Hydrodynamic Memory]].**
  - The observable is the regression slope $\operatorname{Cov}(D,W)/\operatorname{Var}W$, in seconds, with no volts-to-metres gain.
  - The published Basset model, with no free parameters, matches it within 1.6% from 0.75 to 192 µs. Memoryless Langevin is decisively rejected.
  - Lab 38's synthetic controls validated the frozen rules before the real run.
  - A sub-percent structured residual at 2–12 µs remains unexplained by the five frozen diagnostics of lab 40.
- **[[Benchmark 017 — Processing Dependence of the Conditioned Super-Ballistic Signal]].**
  - A forward model shows two effects at 0.75–6 µs. The measurement operator suppresses the conditioned MSD to 0.26–0.79 of the continuum curve. Detector noise supplies 16–71% of the measured value.
  - A confirmatory test, frozen before data, recomputed velocity nine ways. The conditioned MSD changes by factors down to 0.25, as the forward model predicts ($Z=20.9$ over 32 cells), and the processing-independent reading is rejected ($Z=4773$).
  - The apparent 3–12 µs exponent ranges from 2.29 to 2.96 with processing alone.
  - Basset physics stands. The published curve is a processing-dependent statistic, and its agreement with the continuum $t^{5/2}$ curve is a near-cancellation.

**Generalisation (lab 46).** [[Derivation — Conditioning on an Estimated Velocity]] gives universal operator factors, an exact velocity-noise leak and a design criterion for any velocity cusp. **[[Benchmark 018 — Apparent Velocity Roughness and the 7-4 Fractal Dimension]]** (lab 47) applies the same lens to velocity-increment scaling. The apparent $H_v$ passes through ¼ but never plateaus, and raw data show a noise-made pseudo-plateau.

**Beyond physics (labs 48–49).** [[Benchmark 019 — Localization Noise and the Speed-Persistence Coupling]] carries the estimator lesson to cell migration. In three public in vivo immune-cell datasets, T cells and neutrophils show no noise-correctable speed–persistence gap. The B-cell gap would be explained by only 0.3–0.4 µm of localization error. The common turning-angle metric is the noise-sensitive one. In vitro ([[Benchmark 020 — In Vitro T Cells and the Noise Margin of Speed-Persistence Coupling]]), T cells show a strong coupling. The frozen verdict is that the margin is under one pixel. A post hoc lower bound on the localization error from near-immobile tracks (lab 51, σ ≳ 0.2 µm) shows that noise explains at least 12–14% of it. An independent calibration is still needed to bound it from above. A first, selection-biased upper bound was withdrawn after a synthetic control failed. In the zebrafish T-cell tracks of Jerison & Quake ([[Benchmark 021 — Calibrating Localization Error in Zebrafish T-Cell Tracks]]), long 12 s tracks allow a valid upper bound on the noise (σ ≤ 0.40 µm). An initial claim that this coupling is robust (at most 13–23% from noise) was **withdrawn after an internal referee review**. The 12 s calibration comes from a single movie, the same-session rockout movies imply σ ≥ 0.46 µm, and the tercile attribution was biased. Revised (lab 55): noise explains roughly 20–40% of it. The draft paper on this thread was withdrawn and deleted after the review. The standard MSD-intercept calibration fails on cells because fast real motion masquerades as noise.

Lab 39 independently confirms that the authors' commented-out $v_0$ term describes release after steady dragging, not equilibrium. It also corrects the physical labelling in [[Derivation — Equilibrium Conditioning of a Hydrodynamic Brownian Particle]].

## Precision work

The September 14 independent audit of Benchmark 011 adds eight passing verification groups, including 80- and 100-digit series calculations, truncation refinements, and analytic covariance comparisons. Its source and full results are included with the benchmark. This release also rejects nonstandard JSON constants and checks the new results against their recorded source and input hashes.

The September 16 amendment to lab 31 adds explicit lattice and finite-coefficient guards and projects a tiny numerically negative quadratic coefficient back to its allowed nonnegative range before recomputing the certificate. The full main calculation was rerun, and the original development source, protocol, and outputs are preserved outside the portable vault. Lab 32 is explicitly post-hoc and does not retune the original development gate.

- Corrected the exploratory SYK observable to a nonzero Hermitian operator and withdrew unsupported Page-time/memory-equivalence claims.
- Corrected quantum information geometry, ETH, tensor-network, spin-liquid, holographic reconstruction, and thermodynamic qualifications in the newer notes.
- Reframed synthesis sessions as candidate programs with falsifiers, not discoveries or novelty claims.
- Separated 13 core teaching labs from three exploratory programs; the core quick suite passed all built-in checks on September 4.
- Preserved ten historical exploratory result folders outside the current release. Their old plots are not evidence for revised hypotheses.
- Repaired internal navigation and standardized maturity/source-audit metadata. Structural checks do not certify scientific truth.

## The remaining work, in order

1. **Expand the foundation layer.** Replace orientation summaries with worked derivations, assumptions, limiting cases, and pinpoint canonical citations. Start with mechanics, electromagnetism, quantum mechanics, and statistical physics.
2. **Audit claims individually.** Track each important equation and factual assertion to its source; check notation and applicable regime. A bibliography alone is not a claim audit.
3. **Deepen experiments.** Add apparatus diagrams, uncertainty budgets, analysis methods, and reproducible public data where licensing permits.
4. **Demonstrate learning through work.** Solve held-out problems and reproduce results; navigation, storage, and fluent summaries do not establish mastery.
5. **Extend Synthesis Session 001 beyond its completed pilot.** Freeze a new multi-system protocol with data-matched strong baselines, thermal-correlation alternatives, uncertainty estimates, and explicit structure constraints. The original four-system decision rule is not yet evaluated.
6. **Redesign Sessions 002–004.** They need genuinely discriminating models: system–bath evaporation for a Page-time question, multi-coupling RG for a gradient-flow question, and independently validated reduced maps for non-Markovianity.
7. **Maintain the frontier layer.** Refresh dated source reviews as primary evidence changes; never convert an old status statement into a timeless fact.

Within the active response branch, the filtered-camera development comparison is complete at matched scalar reading counts, not matched total exposure or hardware costs. The physical-units screening is now documented. The next priority is permitted acquisition and provenance inspection of the processed public traces, followed by a frozen, detector-matched Gaussian-conditioning reproduction. The public repository's five traces versus the paper's six calibration traces must be reconciled; its files have not been inspected. Ordinary finite differences still cannot be promoted to instantaneous acceleration readings, and camera position averages cannot be relabeled integrated velocity. Published molecular-dynamics or hardware validation, general forcing bands, continuous-time prediction certification, and nonlinear transfer remain open. The full spectral-repair baseline versus fractional and tempered alternatives remains a parallel memory-model comparison on matched observations. These research priorities complement the broad foundation work rather than completing the vault's field coverage.

## Release checks and limits

The [[Computational Lab Index]] records the distinction between execution, numerical checks, and physical validation. The packaged audit checks filenames, Wikilinks, metadata, encoding, and graph connectivity. Neither test suite establishes that every field is completely covered or that every derivation is correct.

No new theory is claimed by this edition. The vault is external, inspectable research memory whose contents must be retrieved and tested in context, not proof of permanent learning.

## Navigation

[[Physics Worldmap]] · [[Vault Health Report]] · [[Architecture and Completeness Audit]] · [[Epistemic Status and Claim Hygiene]] · [[Source and Citation Policy]] · [[Synthesis Lab]]
