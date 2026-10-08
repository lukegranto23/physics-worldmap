---
type: "concept"
field: "Condensed Matter Physics"
epistemic_status: "active"
level: "advanced"
tags: ["physics", "field/condensed", "status/active", "level/advanced"]
aliases: ["QSL", "Spin Liquid"]
created: 2026-07-30
updated: 2026-09-04
note_maturity: expanded
source_audit: bibliography-present-needs-claim-audit
---

# Quantum Spin Liquids

> [!summary] Core idea
> Quantum spin liquids are interacting spin phases without conventional magnetic order whose excitations and entanglement require descriptions beyond a trivial paramagnet. Gapped topological and gapless varieties differ; chiral spin liquids may break time-reversal symmetry.

> [!note] Documentation status
> Expanded orientation. Exactly solved models establish theoretical possibilities; identifying particular materials remains a separate empirical task.

## What “disordered” does not mean

No magnetic order alone is insufficient: singlet product states, valence-bond solids, disorder-induced freezing, and finite-temperature paramagnets can also lack ordinary magnetic order. Examine lattice symmetries, excitations, and nonlocal diagnostics. Definitions and classification are especially subtle for gapless phases. [Zhou, Kanoda, and Ng](https://arxiv.org/abs/1607.03228)

## RVB picture

A resonating-valence-bond ansatz superposes singlet coverings,
$$
|\Psi_{\rm RVB}\rangle=\sum_C a_C|C\rangle.
$$
An individual covering usually breaks lattice symmetries; a suitable superposition may restore them. The ansatz is a candidate wavefunction, not proof of its being the ground state or of topological order.

## Controlled example: Kitaev honeycomb model

For bond labels $\alpha=x,y,z$,
$$
H=-\sum_{\langle ij\rangle_\alpha}J_\alpha\sigma_i^\alpha\sigma_j^\alpha.
$$
A Majorana representation with a local physical-state constraint maps it to free matter Majoranas in static $\mathbb Z_2$ gauge sectors. Plaquette fluxes commute with the unperturbed Hamiltonian.

For positive couplings, a dominant coupling gives a gapped Abelian regime; the triangle-inequality region is gapless. Suitable weak time-reversal-breaking perturbations can open a non-Abelian gap. Generic magnetic fields spoil exact solvability, so the perturbative effective result must not be called an exact solution at arbitrary field. [Kitaev](https://arxiv.org/abs/cond-mat/0506438)

## Fractionalization and entanglement

Spinons, visons, and Majorana descriptions arise in different models; not every spin liquid has all of them. Excitations can carry fractionalized quantum numbers or emergent gauge charge not available to a single local excitation.

For a suitable simply connected region in a gapped two-dimensional topological phase,
$$
S(A)=\alpha|\partial A|-\gamma+\cdots,\qquad \gamma=\ln\mathcal D.
$$
For toric-code-type $\mathbb Z_2$ order, $\mathcal D=2$. Extracting the topological contribution requires cancelling nonuniversal boundary terms and controlling finite-size effects. This is not a universal diagnostic for every gapless spin liquid.

## Partons: useful but conditional

Writing $\mathbf S_i=\tfrac12 f_i^\dagger\boldsymbol\sigma f_i$ with single occupancy enlarges the Hilbert space and introduces gauge redundancy. Projected mean-field ansätze supply candidates; gauge fluctuations may confine them. Projective-symmetry-group data constrain symmetry implementation but do not alone completely classify phases or guarantee stability.

## How to establish a candidate

Combine order-parameter exclusion, symmetry analysis, gaps, spectroscopy, transport, and appropriate topological diagnostics. Repeat finite-size calculations on multiple geometries. Real materials have additional exchanges, anisotropy, disorder, and lattice coupling. Neither a continuum in scattering nor a low ordering temperature uniquely establishes a QSL.

For dated evidence and unresolved experimental interpretations, consult [[Physics Frontiers 2026 Evidence Audit]] rather than treating historical candidate measurements as final verdicts.

## Recall checks

Give a nonmagnetic state that is not a QSL; explain why chiral QSLs invalidate “no symmetry breaking”; distinguish a parton redundancy from a physical gauge excitation; state the assumptions behind $\gamma=\ln\mathcal D$.

## Navigation

[[Condensed Matter Physics Map]] · [[Frustrated Magnets]] · [[Topological Order]] · [[Quantum Entanglement]] · [[Frustrated Systems and Computational Hardness]] · [[Physics Worldmap]]
