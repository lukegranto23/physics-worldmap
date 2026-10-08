---
type: "concept"
field: "Computational Physics"
epistemic_status: "established"
level: "intermediate"
tags: ["physics", "field/computational", "status/established", "level/intermediate"]
aliases: []
created: 2026-07-30
updated: 2026-09-02
note_maturity: orientation-stub
source_audit: orientation-summary-needs-canonical-source
---

# Monte Carlo Integration

> [!summary] Core idea
> For independent finite-variance random samples, Monte Carlo estimates an expectation with root-mean-square error proportional to $N^{-1/2}$; dimension affects the variance and computational cost, while quasirandom methods obey different regularity-dependent bounds.

> [!caution] Orientation status
> This is a compact orientation note and has not yet been source-audited. The epistemic label describes the standing of the underlying physics in its stated regime; it does not certify every sentence or equation in this note.

## Mathematical handle

$\hat I=N^{-1}\sum_{i=1}^N f(X_i)$, with $X_i\overset{\mathrm{iid}}{\sim}p$ and $I=\mathbb E_p[f]$

If $\operatorname{Var}_p(f)<\infty$, then $\operatorname{SE}(\hat I)=\sqrt{\operatorname{Var}_p(f)/N}$. This $N^{-1/2}$ rate does not by itself guarantee dimension-independent difficulty: the variance, sampling cost, autocorrelation, and rare-event structure may worsen sharply with dimension. Markov-chain and quasi-Monte Carlo estimators require their own dependence and smoothness analyses.

## Epistemic status

**Established.** This is a well-established framework or result within its stated domain.

## Place in the world map

- Domain: [[Computational Physics Map]]
- Field-level guiding question (context only): “Which discretization preserves the important invariants and scales?”
- Nearby concepts: [[Physics Worldmap]] · [[Computational Physics Map]] · [[Fast Fourier Transform|← previous]] · [[Markov Chain Monte Carlo|next →]]

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

[[Physics Worldmap]] · [[Computational Physics Map]] · [[Fast Fourier Transform|← previous]] · [[Markov Chain Monte Carlo|next →]]
