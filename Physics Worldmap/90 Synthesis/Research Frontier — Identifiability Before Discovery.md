---
type: research-roadmap
field: Cross-field
epistemic_status: speculative
level: advanced
tags: [physics, research, identifiability, response, experimental-design]
created: 2026-09-04
updated: 2026-09-18
prior_art_audit: targeted-screen-with-scoped-primary-method-reproduction
---

# Research Frontier — Identifiability Before Discovery

> [!important] Working direction, not discovery
> Build reduced descriptions that report when the observations leave their response uncertain, and recommend measurements that reduce that uncertainty. Existing aliasing, model-reduction, error-bound, and experimental-design literature must be treated as the starting point, not renamed as a new theory.

[[Synthesis Lab]] · [[Synthesis Session 001 — Response-Preserving Coarse-Graining]] · [[Benchmark 001 — Equilibrium Versus Forced Response]] · [[Benchmark 002 — The Sampling Boundary of Prediction]]

## What our work actually establishes

Latest gate: [[Instrument Feasibility — Response Bounds Before Data Claims]] finds a conventional camera regime where the broad blur allowance is uninformative under the displayed reference assumptions, and an optical regime where the camera observation model does not apply. [[Public Data Lead — Conditioned Hydrodynamic Brownian Motion]] supplies a specific public-data lead and a known Gaussian-conditioning baseline. No external-data result has yet been reproduced.

| Question | Evidence | Status |
|---|---|---|
| Does matching a one-time equilibrium marginal determine response? | Benchmark 001: identical Gaussian marginals, different response | No, in the explicit model family |
| Can a response fit help a restricted closure? | Benchmark 001: about 26–27% relative error reductions on held-out forcings | Yes, in one linear example; stronger reference wins on response |
| Do exact equilibrium time series always remove ambiguity? | Benchmark 002: identical regularly sampled position laws, different continuous responses | No, under the declared unknown-mass observation constraints |
| Can extra observations distinguish those aliases? | Benchmark 002: known mass or one extra exact covariance lag | Yes for the constructed family, not a general noise-robust result |
| Can a designed lag help with finite noisy data? | [[Benchmark 003 — Noisy Measurements and False Confidence]]: 7/6,000 identification errors at 32 pairs for the Gaussian-distance design | Yes, within a known three-model family |
| Does its confidence set detect a missing true model? | Benchmark 003: 2,000/2,000 false singleton assurances at 128 pairs for omitted alias 4 | No; relative model comparison is not family validation |
| Can standard checks reject the entire candidate family? | [[Benchmark 004 — Rejecting Inadequate Models]]: two-lag checks reject three omitted systems in all 2,000 trials at 512 pairs | Yes in those cases; 5% detuning still causes false reassurance in 88–93% of trials |
| Is poor detection always fixable by a better test? | [[Benchmark 005 — Information Limits and Better Measurements]]: 17/54 cells have a power upper bound below 50% | No, within those specified observation settings |
| Can timing improve near-resonance detection? | Benchmark 005: a standard sensitivity-based lag raises a practical check from 4.24% to 93.12% in one fresh case | Yes at matched pair count; not a universal or time-cost-matched optimum |
| Does range-based timing beat local sensitivity everywhere? | [[Benchmark 006 — Unknown Shifts and Misfocused Tests]]: improved −9.3% detection, reduced +2.7% detection, including a time-cost proxy | No; the finite-grid robustness criterion trades off power |
| Can more data always rescue a valid detector? | [[When More Data Cannot Rescue a Misfocused Test]]: negative asymptotic evidence growth for a pure damping mismatch | No; a fixed alternative list may remain blind despite informative observations |
| Does family rejection diagnose new physical dynamics? | Benchmark 006: sensor-only error causes 97.83% rejection in one setting, with unchanged physical response | No; the rejected model includes observation assumptions |
| Can calibration help at a fixed total reading budget? | [[Benchmark 007 — Calibration Before Physical Attribution]]: one nuisance-aware damping-detection rate rises from 15.10% to 89.83% | Yes under calibrated Gaussian-noise transfer, with explicit cost and timing assumptions |
| Does marginal noise calibration resolve sensor-versus-dynamics ambiguity? | [[Sensor Correlations and the Boundary of Physical Attribution]]: identical observed Gaussian laws, 34.97% response discrepancy | No; unmeasured error correlations can preserve exact ambiguity |
| Can matched-lag calibration resolve that constructed ambiguity? | [[Benchmark 008 — Matched-Lag Calibration]]: sensor-twin physical warnings fall from 93.53% to 0.43%, with a 100% observed sensor alarm | Yes when the paired calibration law transfers; physical power falls under the broader nuisance model |
| Have we built a new warning algorithm? | None | No |
| Have we reproduced a published thermal-memory method? | [[Benchmark 009 — Published Subdiffusion Memory Reproduction]] | One clean case through final Lanczos, plus a paper control; spectral-modification cases, authors' code, and noisy MD data remain |
| Does the restricted reconstruction work on independently generated noisy correlations? | [[Benchmark 010 — Noisy Memory and the Prediction Horizon]]: 104 of 800 datasets accepted after fallback; 13 verification groups passed | Sometimes; omitted spectral repair dominates rejections, and fallback shortens the fitted window |
| Does an accurate clean correlation fit guarantee the eventual transport law? | Benchmark 010: eight post-hoc extrapolation checks and [[Finite Memory and the Return to Normal Diffusion]] | No; the specified finite stable realization becomes normally diffusive while the fractional target remains subdiffusive |
| Does an infinite-time distinction alone establish finite-data discrimination? | [[Benchmark 011 — Finite Observations and Infinite-Time Claims]]: 16 verification groups passed; one Gaussian experiment bounds every size-5% test's power by about 5.96% | No; fixed finite observations cannot uniformly separate zero cutoff from all positive cutoffs, even though their eventual diffusion exponents differ |
| Can extra physical information narrow a finite-time response set without fitting one kernel? | [[Benchmark 012 — Acceleration Information and Certified Displacement]]: 17 checks, 24 inference datasets, 288 intervals; 77.20% median paired width reduction at $M=4096$, $T=6$ | Yes for the declared Gaussian experiment with known velocity variance and 256 additional ideal instantaneous acceleration readings; not a cost-matched advantage, and $T=30$ remains broad |
| Can ordinary finite differences supply the same acceleration certificate? | [[Acceleration Sum Rules and the Sampling Ambiguity]] and the 14-check post-hoc diagnostic: 11 returned miscalibrated intervals miss a passive alias, one trial is withheld; 12 correct-bound controls include truth | No without additional physical assumptions or measurements: exactly equal sampled laws can hide arbitrarily large finite instantaneous acceleration variance |
| Does a published conditioned-displacement result survive a preregistered, measurement-level Gaussian prediction? | [[Benchmark 014 — Preregistered Conditioned Brownian Reproduction]]: six digest-verified traces; 1% bin max $|z|=1.62$, median error 3.2%, descriptive slope 2.517 | Yes for the particle, as a scoped reproduction; empty-trap control fails at lags 1–2 and a ~3% systematic shortfall is unexplained |
| Have we tested nonlinear transfer? | None | No; still necessary |

The second benchmark was prioritized ahead of the nonlinear study because a universal warning claim would fail at the information level before any optimization mattered. This does not replace the nonlinear study or excuse weak baselines.

## The candidate question

For a **declared class of thermal systems**, specified sensors, sampling intervals, finite observation budget, and force family:

> Can we provide a useful bound on response uncertainty, then choose a low-cost additional measurement that reduces that bound with reliable coverage?

“Useful” must include width as well as coverage: saying “anything can happen” is sometimes correct but not an accurate prediction. “Reliable” means checked against cases the method did not tune on. “Low-cost” needs a declared budget in samples, observation time, or injected energy.

Symbolically, let $\mathcal M(D)$ contain the admissible models consistent with data $D$ and its uncertainty. For a declared force $f$, examine

$$
\mathcal R_f(D)=\{y_M[f]:M\in\mathcal M(D)\}.
$$

The response spread of this set may indicate ambiguity that a single best fit hides. This is a schematic connection to set-membership identification and robust prediction, not a new formalism. A finite search over models can miss admissible alternatives: its observed spread is not automatically a rigorous upper uncertainty bound.

## Prior-work screen — September 4, 2026

The following author abstracts or publisher summaries were inspected on September 4. Subsequent work read the Bockius primary method and reproduced its scoped clean case in Benchmark 009; Benchmark 010 tests a restricted implementation on independently generated noisy data. The other entries remain a targeted screen, with full implementations and theorem assumptions not yet audited or reproduced.

| Work | Already covers | What we must distinguish |
|---|---|---|
| [Ma, Li, Liu: Langevin reduced-order techniques](https://arxiv.org/abs/1802.10133) | Krylov projection, moment matching, stochastic consistency conditions | Merely adding thermal noise and memory is not new |
| [Bockius et al.: extended Markov parameterizations](https://arxiv.org/abs/2101.02657) | Auxiliary-state models from velocity correlations, positivity constraints, noisy examples | A correlation-to-memory fit needs comparison to this class |
| [Lang and Lu: learning memory kernels](https://arxiv.org/abs/2402.11705) | Regularized correlation/kernel learning and error control | A proposed warning may be weaker than existing error estimates |
| [Colangeli, Duong, Muntean: hybrid reduction](https://arxiv.org/abs/2405.16157) | Invariant-manifold reduction with thermal consistency and scale separation | A restricted response certificate must add something beyond known reduction guarantees |
| [Yue et al.: system aliasing](https://arxiv.org/abs/1605.08590) | Sampling-induced ambiguity, sampling criteria, prior information | Benchmark 002 is an example of existing theory |
| [González et al.: sampling and identification](https://arxiv.org/abs/2410.19629) | Sampling/input conditions and statistical consistency | Slow sampling does not by itself prove forced identification impossible |

This is a targeted screen, not evidence that the candidate question has no answer in the literature. The next search must explicitly include set-membership identification, optimal experimental design, robust control, and thermodynamic system identification.

The September 12–13 extension also checked [Goychuk's primary treatment of the finite-memory cutoff](https://arxiv.org/html/0905.0826), including eventual normal diffusion of a finite exponential approximation. [[Finite Memory and the Return to Normal Diffusion]] makes that established result's assumptions explicit for our block realizations. The current boundary study must distinguish an observation-level result from rediscovering this known asymptotic crossover.

The September 15–16 extension, [[Prior Art — Spectral Bounds and Physical Response]], identifies direct predecessors for the positive-measure moment problem, cosine-polynomial dual bounds, and strict simultaneous confidence sets. Benchmark 012 applies those established constructions to displacement with acceleration information and explicit continuum-frequency corrections. Neither the optimization framework nor the existence of sampling aliases is a contribution claim.

The finite-data confidence construction in [[Benchmark 003 — Noisy Measurements and False Confidence]] uses a fixed-mixture likelihood ratio and Markov's inequality; [Safe Testing](https://arxiv.org/abs/1906.07801) provides the broader established e-value context. Information-based design for candidate discrimination is also established, for example [Daunizeau et al.](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1002280). Neither source's full algorithm is claimed reproduced.

## Gates before calling anything a contribution

1. **Theorem and implementation reproduction.** Read full methods, record assumptions and guarantees, reproduce one thermal-memory baseline and one uncertainty/identification baseline. Keep paper-level reproduction distinct from implementing a vaguely similar algorithm.
2. **Information audit.** Declare observed coordinates, sampling/averaging, known masses, temperature, force access, unresolved-frequency bounds, and effective state order. Test exact aliases and near-aliases. Do not use hidden full-model parameters as supposedly observable warning features.
3. **Frozen finite-data comparison.** Separate development systems from held-out systems. Compare sample-only, irregular-sampling, velocity-sensor, and forced-probe options at matched explicit budgets. Include always-warn, never-warn, and conventional uncertainty baselines.
4. **Nonlinear stress test.** Introduce a quartic observed potential coupled to a harmonic bath, then vary coupling/time separation and forcing amplitude. Start where stationary distributions or elimination formulas can be independently checked. Equilibrium linear-response identities do not certify finite-amplitude nonlinear response.
5. **Falsification and transfer.** Try a second bath structure and a second physical system. Report false reassurance, unnecessary warnings, response error, and measurement cost—not only average improvement.
6. **Novelty decision.** State a precise difference from prior work: a sharper restricted bound, a cheaper measurement with demonstrated coverage, a counterexample to a published claim, or a regime where existing methods systematically fail. Otherwise label the output a reproduction or useful benchmark.

These are research gates, not a completed preregistration. The numerical budgets, uncertainty procedures, and pass/fail criteria for the next experiment must be fixed before its held-out outcomes are inspected.

## Design constraints worth keeping

- Additional memory variables, delays, and recurrent states count toward model capacity.
- A physically inconsistent but accurate model is not interchangeable with a thermally consistent one; report both axes.
- Equal sampled laws make an impossibility result precise; nearly equal laws require finite-sample distinguishability analysis rather than rhetoric.
- Known mass removes the specific alias family in Benchmark 002. Do not smuggle that example into a known-mass comparison.
- An added off-grid covariance lag costs repeated measurements and has uncertainty.
- An instantaneous acceleration reading is a different observable from a finite velocity difference. Its transfer to a spectral second-moment bound requires an audited sensor bandwidth and observation law; a high sampling count does not remove exact lattice aliases.
- Candidate-model spread may expose a missing assumption without locating the true physical model.
- Negative results should change the next experiment, not be hidden by changing thresholds.

## Next executable milestone

Benchmark 004 now implements the family-rejection control motivated by Benchmark 003, using the published split-likelihood construction and an independent chi-square concentration check. The relevant split-test theorem and proof were inspected; this is a verified implementation of that statistical construction, not a reproduction of all experiments in the paper. It still does not satisfy the thermal-memory reproduction gate.

Benchmark 005 completes the next local audit with new detunings and noise levels, a calibrated known-alternative oracle, exact Gaussian information distances, and standard Fisher-sensitive observation timing. Some cells are provably information-limited; others improve dramatically with changed timing. The oracle's extra information and simpler null constraint prevent treating its gap as pure algorithmic inefficiency.

Benchmark 006 completes a finite-grid unknown-detuning comparison using local-Fisher, null-discrimination, and range-maximin schedules, with equal reading counts and an explicit time-cost proxy. It uses fresh shifts and preserves negative results. Robustness does not mean uniform power improvement, and the time proxy does not replace actual equilibrium preparation costs.

Benchmark 007 implements independent noise calibration, exact nuisance-interval moment tests, and a broader split-Gaussian fit with a safe null-likelihood relaxation. Calibration and a damping-sensitive lag complement each other in one fixed-reading-budget case. The broader split fit remains weaker at finite sample size. A deliberate calibration-transfer failure removes the physical interpretation of its warnings.

The post-hoc [[Sensor Correlations and the Boundary of Physical Attribution]] identifies what isolated calibration still cannot measure: within-pair sensor covariance. It gives an exact two-mechanism ambiguity and a lower bound on the response-set diameter required for uniform coverage over those mechanisms.

Benchmark 008 implements noise-only calibration pairs at the dynamic lags under a matched reading budget. It compares absent, isolated, and paired calibration and derives conditional family-warning control with unknown lag-dependent sensor covariance. The constructed twins separate only after paired calibration, but transfer failures restore false attribution. [[Matched-Condition Calibration]] records the reusable measurement principle.

Benchmark 009 begins the required departure from self-generated Gaussian controls. It reproduces the clean analytic subdiffusion example of Bockius et al. through the moment-Jacobi, Newton, stable-realization, diagnostic-kernel, regularized thermal covariance/noise-factor, and final Lanczos stages, plus the paper's reported coarse-grid unconstrained derivative. Spectral-modification cases and noisy molecular-dynamics stages remain unfinished.

Benchmark 010 completes the independent synthetic-noise milestone using Gaussian trajectory covariance from the analytic target. It records all 800 datasets and 5,504 attempted fits; 104 datasets pass the restricted branch, with 13 verification groups passed. Its omission of the paper's spectral-repair branch prevents interpreting the rejection rate as a verdict on the complete published method. The separate post-hoc response and displacement audit passes eight checks and motivates an explicit time horizon and forcing band for each prediction claim.

[[Benchmark 011 — Finite Observations and Infinite-Time Claims]] completes the fractional-versus-tempered-memory information calculation with 16 verification groups passed. For $\epsilon=10^{-4}$, 4,096 independent Gaussian trajectories sampled at 20 times from 0 to 11.4 give an upper power bound of about 5.96% at a 5% false-positive limit. The finite-window proof fixes the schedule and repetition count before taking the cutoff toward zero. It does not prevent detecting a specified positive cutoff with increasing resources, or imply a discontinuity in the diffusion coefficient itself. These exploratory development calculations motivate a finite-time, finite-frequency prediction region with explicit structural assumptions.

[[Benchmark 012 — Acceleration Information and Certified Displacement]] now supplies certified continuous-frequency outer bounds for a declared finite-time displacement functional, evaluated at four horizons. Seventeen checks passed, together with 24 inference datasets, 288 intervals, and a separate 20,000-dataset confidence-calibration audit. At $M=4096$, $T=6$, the median paired calibrated-to-uninformed width ratio is 0.227964. The additional 256 ideal instantaneous acceleration readings are an information advantage, not a matched-cost result. The bounds remain broad at $T=30$; evaluation at four horizons is not a numerical uniform-in-time certificate.

Its fourteen-check post-hoc diagnostic makes calibration transfer the next concrete gate. A stable, passive, finite-acceleration thermal family has identical lattice-sampled velocity laws and independent finite-difference laws, but a substantially different response. Invalid finite-difference-to-acceleration transfer produces eleven returned intervals, all missing the aliased response; one additional trial is withheld after an unbounded-dual solver report. All twelve controls supplied the correct physical bound include the truth. This does not contradict the main benchmark's explicitly ideal acceleration observations or establish new physics.

[[Benchmark 013 — Camera Exposure and Response Uncertainty]] implements an explicit rectangular position-exposure model and a within-camera, reading-budget-matched comparison with calibration costs. Its 480,000 synthetic datasets and 22 verification groups support the conditional confidence construction; they do not validate a camera. [[Camera Exposure and Finite-Time Response Bounds]] proves acceleration-free blur limits and a sharp exposure-equals-horizon special case. In one condition, 20% unmodeled noise drift drops coverage to 28.33%; an explicit ±20% allowance restores empirical coverage but leaves a median interval about 1.58 times the true small response. Measuring a target-aligned passive displacement over the existing record is not extrapolation beyond it.

The physical-units feasibility audit is now recorded in [[Instrument Feasibility — Response Bounds Before Data Claims]]. The next executable milestone is acquisition and provenance inspection of the processed trajectories identified in [[Public Data Lead — Conditioned Hydrodynamic Brownian Motion]], followed by a frozen, measurement-matched conditional-covariance reproduction. The repository documentation and paper disagree on the number of traces, and the download route used here returned HTTP 403 for the README; file contents remain uninspected. Resolve these gates using permitted access before analyzing results. This is not yet an application of the camera certificate: detector processing, fitted calibration, finite-difference conditioning, and statistical dependence require their own treatment. General forcing bands, nonlinear transfer, matched hardware costs, and guarantees across continuous prediction time remain unfinished.

The full spectral-repair baseline, fractional memory, and tempered fractional memory with an unknown cutoff remain a parallel model-comparison target on matched observations and declared horizons. They are not covered by the finite-acceleration example simply because they are thermal models; the singular fractional target has an infinite acceleration second moment.

The post-hoc result in [[When More Data Cannot Rescue a Misfocused Test]] is a standard likelihood-asymptotic consequence for fixed finite lists, not new theory. It explains why altering fixed positive mixture weights cannot fix the negative asymptotic rate without changing support or observations.

A full published correlation-based thermal-memory reproduction remains unfinished. Benchmark 009 establishes a scoped clean-data baseline and Benchmark 010 adds an independent synthetic stress test with a restricted branch. Neither establishes performance for the full noisy-memory method, experimental transport, or nonlinear warnings.

The vault remains a broad scaffold; this research branch does not imply complete mastery of physics, permanent learning, or a solved theory.

## Navigation

[[Computational Lab Index]] · [[Release Status and Next Work]] · [[Physics Worldmap]]
