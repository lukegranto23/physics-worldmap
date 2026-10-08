---
type: "map-of-content"
field: "Experimental Physics"
epistemic_status: "mixed"
level: "all"
tags: ["physics", "map", "field/experimental"]
aliases: []
created: 2026-07-30
updated: 2026-07-30
---

# Experimental Physics Map

> [!abstract]
> How instruments turn physical interactions into calibrated evidence with quantified uncertainty.

## Questions that organize the field

- What observable best distinguishes competing models?
- How do calibration, background, drift, selection, and systematics affect inference?
- Which detector transduction chain preserves the needed information?
- Is a result reproducible, robust, and appropriately blinded?

## Working principles

- Design from the inference target backward to the instrument.
- Maintain a complete uncertainty and provenance chain.
- Use controls, randomization, blinding, calibration, and null tests where applicable.
- Report likelihoods and assumptions, not only point estimates or significance.

## Canonical mathematical handles

- **Measurement model:** $y=f(x,\theta)+\epsilon$ — Data arise from signal, nuisance parameters, and noise.
- **Propagation:** $\Sigma_y\approx J\Sigma_xJ^T$ — Local uncertainty maps through a transformation.
- **Poisson counts:** $P(n\mid\lambda)=e^{-\lambda}\lambda^n/n!$ — Independent rare event counts fluctuate as Poisson variables.
- **Likelihood ratio:** $\Lambda=L(\theta_0,\hat{\hat\eta})/L(\hat\theta,\hat\eta)$ — Hypotheses are compared while profiling nuisance parameters.

## Concept atlas

| Concept | Level | Status | One-line orientation |
|---|---:|---|---|
| [[Experimental Design]] | introductory | established | A good experiment maps a scientific question to discriminating observables, controls, resources, and a prespecified analysis. |
| [[Measurement Models]] | intermediate | established | A generative model connects latent physical quantities and nuisance parameters to detector data. |
| [[Accuracy Precision and Resolution]] | introductory | established | Accuracy concerns closeness to a reference, precision repeatability, and resolution distinguishable change. |
| [[Random and Systematic Uncertainty]] | introductory | established | Random variation averages statistically; systematic effects bias or distort results and require modeling or controls. |
| [[Uncertainty Propagation]] | introductory | established | Covariance is transformed through a measurement function, linearly for small uncertainties or by sampling when nonlinear. |
| [[Calibration]] | introductory | established | Calibration establishes the relation between instrument response and standards across range, time, and environment. |
| [[Traceability and Metrology]] | intermediate | established | Traceability links a result through documented calibrations to recognized standards with uncertainty at every step. |
| [[Noise Spectral Density]] | intermediate | established | Power spectral density describes variance distributed by frequency and supports filtering and sensitivity budgets. |
| [[Signal to Noise Ratio]] | intermediate | established | SNR compares expected signal to noise in a specified bandwidth, statistic, and observation time. |
| [[Lock In Detection]] | intermediate | established | Phase-sensitive demodulation isolates a modulated signal in a narrow bandwidth away from low-frequency drift. |
| [[Feedback and Control]] | intermediate | established | Feedback stabilizes experimental variables and shapes response, noise, bandwidth, and robustness. |
| [[Analog and Digital Acquisition]] | introductory | established | Sampling, filtering, quantization, dynamic range, timing, and aliasing determine retained information. |
| [[Particle Detectors]] | intermediate | established | Ionization, scintillation, semiconductor excitation, calorimetry, tracking, and timing identify particle interactions. |
| [[Photon Detectors]] | intermediate | established | Photodiodes, photomultipliers, superconducting sensors, and cameras convert absorbed photons to electrical or thermal signals. |
| [[Vacuum Systems]] | intermediate | established | Pressure regimes, conductance, pumping speed, outgassing, and leaks control gas density and collision rates. |
| [[Cryogenics]] | advanced | established | Low-temperature experiments manage cooling power, heat leaks, thermalization, vibration, and thermometry. |
| [[Spectroscopy Methods]] | intermediate | established | Spectroscopy estimates transition frequencies, linewidths, shifts, and amplitudes using controlled sources and calibrated detectors. |
| [[Imaging and Tomography]] | intermediate | established | Imaging maps spatial structure through a point-spread function; tomography reconstructs interiors from projections or waves. |
| [[Interferometry]] | intermediate | established | Interferometers convert phase differences into intensity and can measure displacement, time, refractive index, and fields. |
| [[Counting Statistics]] | introductory | established | Discrete independent events often follow Poisson statistics, while dead time, pileup, and correlations modify counts. |
| [[Hypothesis Tests and Significance]] | intermediate | established | A p-value measures tail probability under a null model and is not the probability that the null is true. |
| [[Bayesian Experimental Inference]] | intermediate | established | Bayesian analysis combines likelihood and prior to infer parameters, predictions, and model odds. |
| [[Look Elsewhere Effect]] | advanced | established | Searching many locations or hypotheses inflates the chance of an extreme local fluctuation. |
| [[Blinding and Reproducibility]] | introductory | established | Blinding limits analyst feedback into choices; reproducibility requires data, code, environment, and procedural provenance. |

## Frontier queue

- [ ] Quantum-enhanced sensing beyond classical resource limits
- [ ] Detectors for ultralight dark matter and extremely weak forces
- [ ] Distributed observatories and real-time multimessenger inference
- [ ] Reproducible analysis pipelines with auditable systematics
- [ ] Autonomous experiment design and closed-loop laboratories

Current evidence and sources belong in [[Open Problems Dashboard]] and the individual frontier notes. A checked box means “reviewed recently,” never “solved.”

## Neighboring fields

[[Foundations of Physics Map]] · [[Computational Physics Map]] · [[Atomic Molecular and Optical Physics Map]]

## Suggested study loop

1. Read the field questions, then explain them from memory.
2. Learn the introductory concepts and reproduce their limiting cases.
3. Derive at least one canonical equation from a variational, symmetry, or conservation principle.
4. Reproduce one landmark result computationally or from public data.
5. Audit one frontier claim: known facts, model dependence, discriminating observable, and next experiment.

## Navigation

[[Physics Worldmap]] · [[Learning Paths]] · [[Epistemic Status and Claim Hygiene]] · [[Synthesis Lab]]
