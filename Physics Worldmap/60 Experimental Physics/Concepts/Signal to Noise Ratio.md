---
type: "concept"
field: "Experimental Physics"
epistemic_status: "established"
level: "intermediate"
tags: ["physics", "field/experimental", "status/established", "level/intermediate"]
aliases: []
created: 2026-07-30
updated: 2026-09-02
note_maturity: orientation-stub
source_audit: orientation-summary-needs-canonical-source
---

# Signal to Noise Ratio

> [!summary] Core idea
> SNR compares expected signal to noise in a specified bandwidth, statistic, and observation time.

> [!caution] Orientation status
> This is a compact orientation note and has not yet been source-audited. The epistemic label describes the standing of the underlying physics in its stated regime; it does not certify every sentence or equation in this note.

## Mathematical handle

$\mathrm{SNR}^2=4\int|\tilde h(f)|^2/S_n(f)\,df$

This is the optimal matched-filter SNR for a known waveform in zero-mean stationary Gaussian noise, using a one-sided noise power spectral density and compatible Fourier conventions. The matched filter saturates the Cauchy–Schwarz upper bound among linear filters under those assumptions. Template mismatch, nonstationarity, non-Gaussian tails, calibration uncertainty, nuisance parameters, and search trials generally reduce realized detection performance, so this expression is not a universal definition of SNR.

## Epistemic status

**Established.** This is a well-established framework or result within its stated domain.

## Place in the world map

- Domain: [[Experimental Physics Map]]
- Field-level guiding question (context only): “What observable best distinguishes competing models?”
- Nearby concepts: [[Physics Worldmap]] · [[Experimental Physics Map]] · [[Noise Spectral Density|← previous]] · [[Lock In Detection|next →]]

## Reasoning checks

1. State the physical objects and observables without using the displayed equation.
2. Check dimensions and identify every limiting assumption.
3. Give one regime where this description succeeds and one where it needs correction.
4. Name an experiment, simulation, or observation that could determine its parameters.
5. Explain how this idea changes when the dominant length, time, energy, or particle-number scale changes.

## Expansion queue

- [ ] Add a derivation from the nearest prerequisite principles.
- [ ] Add a worked example with units.
- [ ] Add a primary or canonical source.
- [ ] Add a failure case, misconception, or counterexample.

## Navigation

[[Physics Worldmap]] · [[Experimental Physics Map]] · [[Noise Spectral Density|← previous]] · [[Lock In Detection|next →]]
