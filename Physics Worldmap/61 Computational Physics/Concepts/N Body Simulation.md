---
type: "concept"
field: "Computational Physics"
epistemic_status: "established"
level: "intermediate"
tags: ["physics", "field/computational", "status/established", "level/intermediate"]
aliases: []
created: 2026-07-30
updated: 2026-07-30
note_maturity: orientation-stub
source_audit: orientation-summary-needs-canonical-source
---

# N Body Simulation

> [!summary] Core idea
> Gravitational or electrostatic many-body dynamics uses direct, tree, mesh, or hybrid force algorithms.

> [!caution] Orientation status
> This is a compact orientation note and has not yet been source-audited. The epistemic label describes the standing of the underlying physics in its stated regime; it does not certify every sentence or equation in this note.

## Mathematical handle

$\ddot r_i=G\sum_{j\ne i}m_j(r_j-r_i)/|r_j-r_i|^3$

The expression is an orientation point, not a substitute for checking assumptions, sign conventions, units, boundary conditions, and the regime in which it was derived.

## Epistemic status

**Established.** This is a well-established framework or result within its stated domain.

## Place in the world map

- Domain: [[Computational Physics Map]]
- Field-level guiding question (context only): “Which discretization preserves the important invariants and scales?”
- Nearby concepts: [[Physics Worldmap]] · [[Computational Physics Map]] · [[Lattice Simulations|← previous]] · [[Computational Fluid Dynamics|next →]]

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

[[Physics Worldmap]] · [[Computational Physics Map]] · [[Lattice Simulations|← previous]] · [[Computational Fluid Dynamics|next →]]
