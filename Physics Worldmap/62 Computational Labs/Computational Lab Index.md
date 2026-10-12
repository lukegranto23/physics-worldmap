---
type: lab-index
field: Computational Physics
epistemic_status: reference
level: all
tags: [physics, computation, lab, reproducible]
created: 2026-07-30
updated: 2026-09-18
---

# Computational Lab Index

[[Physics Worldmap]] · [[Computational Physics Map]] · [[Theory Experiment Computation Loop]]

Open [[Computational Lab Gallery]] to inspect the validated quick-run results.

The separate [[Electromagnetism — Fields Energy and Gauge Study Route]] uses [[check_electromagnetism.py]] and [[electromagnetism-checks.json]] for fourteen targeted example checks. This foundation helper is not an additional numbered research lab; it checks selected calculations, not the entire field.

## Computational Physics Laboratory

These small laboratories turn central physics equations into experiments that can
be rerun, modified, and falsified. The core programs (01–13) use only Python,
NumPy, and Matplotlib; later research programs may also require SciPy. Each core program:

- states its units and modelling assumptions near the top;
- accepts `--out-dir` and writes a figure plus machine-readable data;
- uses a fixed random seed when randomness is involved;
- performs at least one comparison with an analytic result, conservation law, or
  exact bound, and exits with an error if that check fails;
- supports `--quick` for a fast smoke test.

Run a lab from this directory, for example:

```powershell
python -m pip install -r requirements.txt
python 01_projectile_symplectic.py --quick
python 07_schrodinger_1d.py
python 08_ising_monte_carlo.py --seed 2026
python run_all.py --quick
```

By default results go into `results/<lab-name>/`.  Choose another location with
`--out-dir PATH`.  The figures are explanatory summaries, while the `.npz` or
`.csv` files preserve the numbers needed for later analysis.

`run_all.py` executes core labs 01–13 and fails immediately if a built-in check fails. Exploratory labs 14–16 must be run individually; they are not hypothesis-validation tests and are excluded from this suite.

> [!success] Validated environment
> The 13 core quick labs passed again on 2026-09-04 with Python 3.14.3, NumPy 2.4.3, and Matplotlib 3.10.8. The declared dependency ranges are broader, so rerun the suite after installation.

## Index

| Lab | Model | Main numerical idea | Built-in check |
|---|---|---|---|
| `01_projectile_symplectic.py` | Projectile in uniform gravity | Velocity Verlet vs. Euler | Analytic trajectory and energy |
| `02_nbody_orbits.py` | Sun–Earth–Jupiter gravity | Symplectic N-body integration | Energy, angular momentum, momentum |
| `03_coupled_oscillators.py` | Fixed-end mass–spring chain | Matrix normal modes | Closed-form mode frequencies |
| `04_laplace_electrostatics.py` | Two electrodes in a grounded box | Finite-difference relaxation | Discrete Laplace residual and symmetry |
| `05_wave_fdtd.py` | Vibrating string | Leapfrog/FDTD wave update | Exact standing-wave solution |
| `06_heat_diffusion.py` | Conducting rod | Explicit FTCS diffusion | Exact decaying Fourier mode |
| `07_schrodinger_1d.py` | Infinite quantum well | Hamiltonian diagonalization and spectral evolution | Exact energies, norm conservation |
| `08_ising_monte_carlo.py` | 2-D ferromagnetic Ising model | Checkerboard Metropolis sampling | Thermodynamic bounds and phase trend |
| `09_random_walks.py` | Independent 2-D lattice walkers | Monte Carlo ensemble | Einstein mean-square-displacement law |
| `10_lorenz_chaos.py` | Lorenz convection model | RK4 and tangent-separation estimate | Convergence and Lyapunov range |
| `11_special_relativity.py` | Lorentz transformations | Event and velocity transforms | Invariant interval and inverse map |
| `12_friedmann_cosmology.py` | Flat matter–Lambda universe | Friedmann quadrature | Closure, present expansion, cosmic age |
| `13_data_fitting_uncertainty.py` | Pendulum measurement of \(g\) | Weighted least squares and Monte Carlo | Pull/coverage and covariance checks |

## Exploratory programs — not established research results

| Lab | Numerical scope | Interpretation limit |
|---|---|---|
| `14_syk_mori_zwanzig.py` | Small SYK matrices, correlation-kernel inversion, selected-pair trace distance | Fixed subsystem, not evaporation; no Page-time/memory equivalence |
| `15_rg_fisher_geometry.py` | Ising sampling, uncalibrated correlation-to-coupling proxy, Fisher response | Proxy is not valid 2D inverse inference; constructed potential is not an independent c-function |
| `16_bures_thermalization_geometry.py` | Subsystem entropy, purity, Bures trajectory geometry | Finite-window diagnostics only; no gravitational or non-Markovianity equivalence |

See [[Synthesis Session 002 — Holographic Coarse-Graining and the Memory of Spacetime]], [[Synthesis Session 003 — RG Flow as Information Geometry and the Shape of Scale]], and [[Synthesis Session 004 — The Geometry of Thermalization]] for corrected interpretation and falsification criteria. Corrected quick runs are saved in `results/exploratory_corrected/`. Historical exploratory results were preserved outside this release and must not be cited as evidence for the revised hypotheses.

## Response-preservation pilot

[[Benchmark 001 — Equilibrium Versus Forced Response]] documents `17_response_preserving_reduction.py`: an exact thermal oscillator comparison with 32 passing checks, frozen training/test settings, and reproducible output in `results/response_benchmark/`. It is separate from the core 01–13 runner and exploratory 14–16 programs. One-time equilibrium matching does not preserve forced dynamics; fitting response helps this example but does not beat the full-information balanced reference on response. No discovery or full four-system validation is claimed.

## Sampling and identifiability boundary

[[Benchmark 002 — The Sampling Boundary of Prediction]] documents `18_sampling_identifiability_boundary.py`: exact thermal covariance and response calculations with 31 passing checks. Outputs are in `results/sampling_boundary/`. This example of established aliasing limits what a warning can infer from regularly sampled positions when mass is unknown. It uses no stochastic simulation and is separate from the core 01–13 runner. See [[Research Frontier — Identifiability Before Discovery]] for the research implications.

## Noisy measurement-design control

[[Benchmark 003 — Noisy Measurements and False Confidence]] documents `19_noisy_measurement_design.py`: a fixed-protocol comparison of five observation schedules, finite-sample confidence sets, and a predeclared omitted-model stress test. It saves 120,000 dataset evaluations and sufficient statistics in `results/measurement_design/`; designs share common random numbers. Eleven implementation checks passed. Better discrimination within a known candidate family did not protect against omitted physics. This is separate from the core 01–13 runner and does not reproduce a published thermal-memory algorithm.

## Rejecting the candidate family

[[Benchmark 004 — Rejecting Inadequate Models]] documents `20_family_rejection.py`: 96,000 dataset evaluations comparing no family check, split-likelihood rejection, and a concentration-bound rejection check. Equal reading budgets are used for one or two lags; fresh omitted models replace the previous alias-4 stress case. Eighteen implementation checks passed. Several mismatches are caught, but a 5% detuning near resonance remains difficult despite large response error. Outputs are in `results/family_rejection/`; this program is separate from core labs 01–13.

## Oracle and information-limit audit

[[Benchmark 005 — Information Limits and Better Measurements]] documents `21_oracle_detection_limits.py`, which reuses rejection functions from lab 20. It compares a calibrated known-alternative oracle, two practical checks, exact Gaussian KL power bounds, and standard local-Fisher measurement timing across 54 fresh cells. Ten implementation checks passed; outputs are in `results/oracle_detection/`. The oracle is not an equally informed practical competitor. No general warning or new theory is claimed.

## Unknown-shift design and post-hoc diagnosis

[[Benchmark 006 — Unknown Shifts and Misfocused Tests]] documents lab 22 (22_range_measurement_design.py): 768,000 simulated dataset evaluations of four observation schedules, equal-reading and time-proxy budgets, and three alternative-blind tests. Twenty-one checks passed. Lab 23 (23_range_design_diagnostics.py) adds three checked, explicitly post-hoc Gaussian-information diagnostics without changing the frozen comparison. [[When More Data Cannot Rescue a Misfocused Test]] derives the fixed-mixture failure. Outputs are in results/range_design/. Neither program is part of the core 01–13 teaching suite.

## Calibration and physical attribution

[[Benchmark 007 — Calibration Before Physical Attribution]] documents lab 24 (24_sensor_calibration.py): 810,000 dataset evaluations with independent calibration costs, exact chi-square nuisance intervals, and a relaxed split-likelihood reference. Sixteen checks passed. SciPy is required in addition to NumPy and Matplotlib. Lab 25 (25_sensor_dynamics_ambiguity.py) adds twelve post-hoc algebraic checks for [[Sensor Correlations and the Boundary of Physical Attribution]]. Outputs are in results/sensor_calibration/. The counterexample does not alter the frozen comparison, and neither program belongs to the core 01–13 teaching suite.

## Matched-lag paired calibration

[[Benchmark 008 — Matched-Lag Calibration]] documents lab 26 (26_paired_sensor_calibration.py): 585,000 dataset evaluations comparing absent, isolated, and paired calibration under matched reading budgets. Twenty-seven checks passed. The protocol records and corrects a failed positive-covariance validation before the accepted run. Outputs are in results/paired_calibration/. [[Matched-Condition Calibration]] states the reusable experimental principle. This program remains outside the core 01–13 teaching suite.

## Published thermal-memory reproduction

[[Benchmark 009 — Published Subdiffusion Memory Reproduction]] documents lab 27 (27_thermal_memory_reproduction.py): a scoped independent implementation of the clean $\tau=0.6$, $n=10$ subdiffusion example in Bockius et al. It implements the moment-Jacobi recurrence, analytic derivative, Newton constraint, stable realization, diagnostic kernel, sampled positive-real screen, regularized Riccati covariance, thermal noise-factor check, and final nonsymmetric Lanczos sweep. Twenty-nine checks passed, including the paper's reported coarse-grid derivative control. It does not implement spectral-modification cases or molecular-dynamics experiments. Outputs are in results/thermal_memory_reproduction/.

## Noisy memory and physical extrapolation

[[Benchmark 010 — Noisy Memory and the Prediction Horizon]] documents lab 28 (`28_noisy_memory_stress.py`) and lab 29 (`29_memory_extrapolation.py`). Lab 28 reconstructs 800 independently generated Gaussian-trajectory datasets and accepts 104 after reducing order and shortening the fitted time window. Thirteen verification groups passed. Its restricted branch rejects cases requiring the paper's spectral repair, so these rejection rates do not evaluate the full published method. The data are synthetic equilibrium correlations, not molecular-dynamics or hardware observations.

Lab 29 evaluates the saved regularized matrices without refitting. Eight checks passed for the analytic displacement, matrix integration, zero-frequency diffusivity, and force-response identities. The clean model's eventual ordinary diffusion is an established finite-memory effect; [[Finite Memory and the Return to Normal Diffusion]] proves it under explicit stability and stationary-covariance conditions. This extrapolation analysis is post-hoc. Protocols and outputs are recorded in `noisy_memory_stress_protocol.json`, `memory_extrapolation_protocol.json`, and `results/noisy_memory_stress/`.

## Finite observations and asymptotic transport

[[Benchmark 011 — Finite Observations and Infinite-Time Claims]] documents lab 30 (`30_tempered_memory_boundary.py`): exact population covariances and Gaussian information bounds for the established fractional and tempered-memory family. All 16 verification groups passed. For cutoff $\epsilon=10^{-4}$, 4,096 independent trajectories sampled at 20 times from 0 to 11.4 give a detection-power upper bound of about 5.96% at a 5% false-positive limit, even when both models are known. This is an evaluated analytic bound, not an achieved detection rate. The exploratory protocol is `tempered_memory_boundary_protocol.json`; curves, covariances, and checks are in `results/tempered_memory_boundary/`.

Labs 27–30 require SciPy and run separately from the core teaching suite. Lab 27's opening description predates its implemented Riccati and final Lanczos stages; the benchmark note and executable stages document the actual scope, while the historical source is retained to preserve its recorded hash.

The supplementary `audit_tempered_memory_boundary.py` independently checks Lab 30 using high-precision inverse-Laplace series and analytic covariance examples. Eight audit groups passed on September 14; the saved `results/tempered_memory_boundary/independent_audit.json` includes precision/truncation refinements and provenance hashes. It does not rerun or alter Lab 30's original results.

## Acceleration information and certified displacement

[[Benchmark 012 — Acceleration Information and Certified Displacement]] documents lab 31 (`31_spectral_response_bounds.py`): an application of established spectral moment bounds, exact Gaussian confidence calibration, and between-grid/tail corrections over continuous frequency. Seventeen verification groups passed. Twenty-four inference datasets produce 288 intervals across three information modes and four horizons; a separate 20,000-dataset audit checks the underlying confidence event. These are ensemble displacement-response bounds, not prediction intervals for individual trajectories or an interval-arithmetic proof.

At $M=4096$ and $T=6$, adding 256 independent, ideal instantaneous acceleration readings reduces interval width by 77.20% at the median of paired comparisons. Known velocity variance and the stated Gaussian observation law are essential; the added observable is not an equal-hardware or equal-cost comparison. Bounds remain broad at $T=30$. [[Acceleration Sum Rules and the Sampling Ambiguity]] derives the physical constraint and [[Prior Art — Spectral Bounds and Physical Response]] records the prior-art limits.

Lab 32 (`32_acceleration_calibration_alias.py`) is a separate post-hoc sensor-transfer diagnostic, with fourteen checks passed. A finite-acceleration, passive thermal alias has identical sampled velocity laws but a different displacement response. Deliberately treating finite-difference variance as instantaneous acceleration variance yields eleven returned intervals that all miss the aliased truth; one further declared trial is withheld after an unbounded-dual solver report. All twelve correctly supplied oracle controls include the truth. This failure does not invalidate lab 31 under its ideal instantaneous-reading assumptions.

Protocols are `spectral_response_protocol.json` and `acceleration_alias_diagnostic_protocol.json`; inputs, results, certificates, and plots are in `results/spectral_response/`. Labs 31–32 require SciPy and run separately from the core teaching suite. No new optimization method or genuine breakthrough is claimed; measurement bandwidth, matched acquisition costs, and real-data transfer are the next tests.

## Camera exposure and finite-horizon response

[[Benchmark 013 — Camera Exposure and Response Uncertainty]] documents lab 33 (`33_camera_response_bounds.py`): 480,000 exact Gaussian sufficient-statistic datasets, 1,440,000 interval attempts, and 22 passing verification groups. Two rectangular position exposures measure a filtered displacement functional, not instantaneous acceleration. The response bounds use known finite velocity variance, explicit blur allowances, and costed paired localization calibration. [[Camera Exposure and Finite-Time Response Bounds]] gives the proofs, including a sharp exposure-equals-horizon special case and a noninteger-timing counterexample. Outputs and all sufficient statistics are in `results/camera_response/`. A 20% calibration mismatch breaks the exact-transfer analysis in one condition; permitting that drift restores coverage but broadens the interval beyond the small true response. No hardware validation, optimal shutter, state-of-the-art victory, or novelty is claimed. This lab is separate from the core teaching runner.

[[Benchmark 014 — Preregistered Conditioned Brownian Reproduction]] documents lab 34 (`34_conditioned_displacement_reproduction.py`): a protocol frozen before data content was seen, synthetic positive/negative self-tests (`--selftest`), and a digest-gated run on the public Dryad traces (`--data <dir>`). Outputs are in `results/conditioned_reproduction/`. Third-party data are not redistributed in the vault. This lab is separate from the core teaching runner.

Follow-up labs on the same digest-verified Dryad files (all separate from the core runner; SciPy and mpmath required):

- **Lab 35** (`35_gain_free_hydrodynamic_memory.py`, protocol `gain_free_hydrodynamics_protocol.json`). It compares Basset, initial-value and memoryless Langevin models through the measured bin-and-stencil operator. The observable is the regression slope $\operatorname{Cov}(D_k,W)/\operatorname{Var}W$, in seconds, after empty-trap noise subtraction; the volts-to-metres gain cancels. Documented in [[Benchmark 015 — Gain-Free Test of Hydrodynamic Memory]].
- **Lab 36** (`36_stratified_conditioning.py`). The preregistered variance-stratification test of Benchmark 014's anomalies.
- **Lab 37** (`37_stratification_artifact_audit.py`). A post hoc eight-seed stationary audit showing that the primary $\operatorname{Var}W$ proxy is itself biased. Labs 36–37 are documented in [[Benchmark 016 — Stratified Conditioning and an Estimator Artifact]].
- **Lab 38** (`38_gain_free_selftest.py`). Synthetic Basset and Langevin controls for lab 35's frozen rules. Positions are synthesised exactly from the FDT spectrum on a 25 ns grid and box-averaged, with white and smooth detector noise. The synthesiser's expected increment variances match lab 35's operator to about $10^{-5}$.
- **Lab 41** (`41_processing_dependence_test.py`, `--selftest` then `--data`). A confirmatory nine-variant stencil and coarsening test, frozen before data. The conditioned MSD follows the forward model ($Z=20.9$), not the processing-independent reading ($Z=4773$). Documented in [[Benchmark 017 — Processing Dependence of the Conditioned Super-Ballistic Signal]].
- **Lab 50** (`50_in_vitro_speed_persistence_test.py`). Lab 49's protocol applied to in vitro T cells (Zenodo 8420011). Documented in [[Benchmark 020 — In Vitro T Cells and the Noise Margin of Speed-Persistence Coupling]].
- **Lab 51** (`51_in_vitro_noise_bracket.py`). Post hoc: a conservative lower bound on the in vitro pipeline's localization error from near-immobile tracks (σ ≳ 0.20–0.26 µm, so noise explains at least 12–14% of the coupling). There is a split-half upper bound, valid but loose, and synthetic controls; the selection-based upper bound was withdrawn. Also redraws the sensitivity-curve figure. Documented in Benchmark 020.
- **Lab 52** (`52_speed_persistence_figure.py`). The sensitivity-curve figure for the speed–persistence paper.
- **Lab 53** (`53_calibrated_speed_persistence_test.py`). Frozen test on the Jerison & Quake tracks with an MSD-intercept noise calibration. The calibration over-corrects on real cells. Documented in [[Benchmark 021 — Calibrating Localization Error in Zebrafish T-Cell Tracks]].
- **Lab 54** (`54_noise_calibration_consistency.py`). Post hoc: a fast motion component biases the MSD-intercept calibration, while a Cauchy–Schwarz split-half upper bound stays valid. Its "at most 13–23%" result was **withdrawn** after internal review. Documented in Benchmark 021.
- **Lab 55** (`55_fixed_tercile_reanalysis.py`). Post hoc revision: fixed-tercile and pooled-moment noise attribution, which removes the tercile-recomposition bias of lab 49's protocol, re-run on all datasets. Documented in Benchmark 021.
- **Labs 48–49** (`48_speed_persistence_noise_theory.py`, `49_speed_persistence_noise_test.py`). Localization noise and the cell speed–persistence coupling: a closed-form apparent persistence for a noisy OU walk, then a frozen per-cell correction and sensitivity curve on public celltrackR immune-cell tracks. Documented in [[Benchmark 019 — Localization Noise and the Speed-Persistence Coupling]].
- **Lab 47** (`47_velocity_roughness_estimator_bias.py`). Apparent velocity roughness $H_v$ from stencil velocities, as theory plus a descriptive data comparison. The local exponent passes through ¼ but never plateaus there; raw data show a noise-made pseudo-plateau. Documented in [[Benchmark 018 — Apparent Velocity Roughness and the 7-4 Fractal Dimension]].
- **Lab 46** (`46_estimated_velocity_conditioning_theory.py`). General theory of conditioning on a stencil-estimated velocity: universal operator factors $\Phi_\alpha(k)$, the exact noise-leak identity, and checks against the full Basset model. Supports [[Derivation — Conditioning on an Estimated Velocity]].
- **Lab 45** (`45_noise_additivity_spectrum.py`). A descriptive spectral check of noise additivity. Published Basset matches the particle spectrum to 1–4% at 2–100 kHz, but the particle-run noise floor above 400 kHz is about 0.5–0.7× the empty trap's.
- **Lab 44** (`44_processing_dependence_figure.py`). A descriptive figure for Benchmark 017.
- **Lab 43** (`43_nonzero_speed_processing_test.py`). The lab 41 test at the published nonzero speeds: H_fwd at $q=0.5$ and 2, UNRESOLVED at the $q=1$ crossover, the same pattern as its self-test.
- **Lab 42** (`42_noise_transfer_test.py`). Two-component noise-transfer test of the residual; NOT EXPLAINED (Benchmark 015). Lab 40 (`40_basset_misfit_diagnostics.py`) holds the five frozen misfit diagnostics.
- **Lab 39** (`39_conditional_mean_preparations.py`). A Grünwald–Letnikov time-domain check that the equilibrium conditional mean equals the impulsive start, and that the authors' commented-out term is release after steady dragging. Supports [[Derivation — Equilibrium Conditioning of a Hydrodynamic Brownian Particle]].

## How to learn with these

1. Run the unmodified program and read the printed validation report.
2. Change one physical parameter and predict the result before rerunning it.
3. Halve the grid spacing or time step.  Determine the observed convergence
   order rather than trusting the nominal one.
4. Deliberately violate the stability condition (on a copy) and identify the
   numerical failure signature.
5. Replace a simplifying assumption—add drag, disorder, a potential barrier,
   curvature, or correlated measurement noise—and add a new validation.

The checks are necessary but not proofs.  Passing conservation tests can still
hide modelling errors, insufficient resolution, biased sampling, or a wrong
observable.  Each script therefore records assumptions and exposes the most
important resolution parameters at the command line.

## Reproducibility and numerical caution

- Core real-valued calculations use NumPy `float64`; quantum calculations also use `complex128`.
- Monte Carlo error bars here are pedagogical.  Near the Ising critical point,
  autocorrelation makes naive independent-sample errors too optimistic.
- Boundary conditions define the physical problem, not merely the code.  The
  Laplace, heat, wave, and quantum examples use idealized boundaries.
- Symplectic methods usually bound long-term Hamiltonian energy error; they do
  not make a coarse step accurate.
- Numerical agreement should be tested under refinement and against more than
  one independent observable before drawing physical conclusions.
- **Lab 56** (`56_spherical_code_search.py`). Basin-hopping search for spherical codes, starting from Henry Cohn's table.
- **Lab 57** (`57_spherical_code_final_check.py`). Independent 50-digit final check against the live table. Result: 35 improved entries. See [[Benchmark 022 — Improved Spherical Codes for Cohn's Table]].
- **Lab 58** (`58_exact_s5_spherical_code.py`). Exact structure of the improved (13, 59) code: an S5-symmetric 57-point core plus two rattlers. The minimal-angle cosine is a root of 1196x⁴−1428x³+411x²+18x−9, and existence is certified by exact rank. See [[Benchmark 023 — An Exact S5-Symmetric Spherical Code in 13 Dimensions]].
