---
type: "concept"
field: "Relativity and Gravitation"
epistemic_status: "open"
level: "advanced"
tags: ["physics", "field/relativity", "status/open", "level/advanced"]
aliases: ["information paradox", "black hole information paradox", "information loss problem"]
created: 2026-07-30
updated: 2026-07-30
note_maturity: expanded
source_audit: bibliography-present-needs-claim-audit
---

# Black Hole Information Problem

> [!summary] Core idea
> If a black hole evaporates completely via thermal [[Hawking Radiation]], a pure quantum state appears to evolve into a mixed thermal state, violating the unitarity of quantum mechanics. Resolving this conflict between general relativity and quantum theory is one of the deepest problems in theoretical physics.

> [!note] Documentation status
> This expanded note includes a canonical bibliography but has not yet received a claim-by-claim source audit. The epistemic label describes the standing of the underlying physics in its stated regime; it does not certify every sentence or equation in this note.

## Why this matters

This is not an academic curiosity. It forces a choice among principles that are individually well-tested: (1) general relativity is approximately correct near horizons of large black holes, (2) quantum mechanics is unitary, (3) quantum field theory on curved spacetime is reliable in low-curvature regions. At least one must give way in a theory of [[Quantum Gravity]].

## Mathematical framework

### Hawking's original argument (1976)

Consider a star collapsing to form a [[Black Holes|black hole]]. The initial state $|\Psi_{\text{in}}\rangle$ is pure. Hawking showed that the outgoing radiation at late times is in a thermal mixed state with density matrix:

$$\rho_{\text{out}} = \frac{1}{Z}\sum_n e^{-\omega_n / T_H}\, |n\rangle\langle n|$$

where $T_H = \hbar c^3 / (8\pi G M k_B)$ is the Hawking temperature. The entanglement entropy of the radiation grows monotonically as more radiation is emitted:

$$S_{\text{rad}}(t) \nearrow \quad \text{(Hawking's calculation: monotonically increasing)}$$

If the black hole evaporates completely ($M \to 0$), the leading semiclassical description leaves a mixed radiation state. The evolution $|\Psi_{\text{in}}\rangle\langle\Psi_{\text{in}}| \to \rho_{\text{out}}$ would not be unitary. Its radiation entropy is of order the initial black-hole thermodynamic entropy in a quasistatic evaporation estimate, but the two entropies are conceptually distinct.

### The Page curve (1993)

Using typical-state/random-unitary assumptions, Don Page argued that if evaporation is unitary (the black hole plus radiation form a pure state at all times), the radiation entanglement entropy should approximately follow:

$$S_{\text{rad}}(t) = \begin{cases} S_{\text{coarse}}(t) \approx \text{(grows as radiation accumulates)} & t < t_{\text{Page}} \\ S_{BH}(t) \approx A(t)/(4G) & t > t_{\text{Page}} \end{cases}$$

The **Page time** is the crossover where the effective radiation and remaining-black-hole entropy scales become comparable; its precise location depends on the evaporation model. Before that time, small subsystems of the radiation can look thermal. Afterward, unitary models require correlations with earlier radiation to lower the total radiation entropy. A gravitational derivation of this behavior is an important consistency test, not by itself a microscopic account of information transfer.

### Entanglement entropy and unitarity

For a bipartite pure state $|\Psi\rangle_{AB}$:

$$S_A = S_B$$

If the black hole subsystem $B$ and radiation subsystem $A$ form a pure state, their **von Neumann entanglement entropies** obey $S(A)=S(B)$. This $S(B)$ must not be identified automatically with the thermodynamic Bekenstein-Hawking entropy, although the latter estimates the logarithm of available black-hole states in semiclassical reasoning. Complete unitary evaporation requires the final radiation entropy to return to zero, whereas Hawking's leading semiclassical calculation predicts continued growth.

## Physical content

### Proposed resolutions

#### 1. Information is truly lost (Hawking, 1976-2004)

Hawking originally proposed that quantum gravity permits non-unitary evolution. This requires modifying quantum mechanics. Banks, Peskin, and Susskind (1984) showed that generic violations of unitarity lead to violations of energy conservation or locality, making this option unattractive. Hawking later conceded (2004) that information is likely preserved, partly based on [[AdS-CFT Correspondence|AdS/CFT]] arguments.

#### 2. Remnants

The black hole might stop evaporating at the Planck mass, leaving a stable remnant containing all the information. The problem: a remnant of Planck mass would need an unbounded number of internal states (to store the information of arbitrarily large initial black holes), leading to pair-production catastrophes and infinite phase-space contributions.

#### 3. Black hole complementarity (Susskind, 1993)

Black-hole complementarity proposes that no single observer sees a violation. An infalling observer crosses the horizon smoothly and encounters nothing special. A distant observer sees information encoded in subtle correlations of the Hawking radiation, which is eventually released. These descriptions are complementary -- no observer accesses both -- but whether this resolves the full consistency problem is debated. The Page time is a characteristic crossover, not necessarily the first release of any information.

#### 4. Firewalls (AMPS, 2012)

Almheiri, Marolf, Polchinski, and Sully argued that complementarity leads to a contradiction. In the old-black-hole regime, purification requires appropriate correlations between early radiation $R$ and later mode $B$, while a smooth semiclassical horizon requires near-vacuum entanglement between $B$ and its interior partner. Strong subadditivity constrains these simultaneous requirements; literal maximal entanglement of both pairs is not necessary for the argument. If unitarity wins, the $B$-$\tilde{B}$ entanglement breaks, creating a high-energy "firewall" at the horizon -- contradicting the equivalence principle.

The three assumptions in tension (any resolution must abandon at least one):
1. **Unitarity**: evolution is unitary.
2. **Semiclassical EFT**: effective field theory is valid outside the stretched horizon.
3. **No drama**: an infalling observer encounters nothing special at the horizon.

#### 5. ER = EPR (Maldacena and Susskind, 2013)

Entangled particles are connected by non-traversable Einstein-Rosen bridges (wormholes). The $B$-$\tilde{B}$ entanglement is a geometric connection (wormhole) between the black hole interior and the radiation. This modifies the geometry rather than breaking entanglement, potentially avoiding firewalls. The idea is suggestive but not yet a complete calculation.

### The island formula and replica wormholes (2019-2020)

A major recent advance in controlled gravitational models uses the quantum extremal surface (QES) prescription and replica methods:

$$S_{\text{rad}} = \min\!\left\{\underset{\text{ext}}{\text{ext}}\left[\frac{\text{Area}(\partial I)}{4G_N} + S_{\text{bulk}}(\text{rad} \cup I)\right]\right\}$$

where the extremization is over surfaces $\partial I$ and $I$ is an "island" -- a bulk region that is geometrically inside the black hole but contributes to the radiation's entanglement entropy.

**Before the Page time**: no island contributes; $S_{\text{rad}}$ grows (matching Hawking).

**After the Page time**: an island appears inside the black hole. The area term dominates and decreases as the black hole shrinks. The radiation entropy follows the Page curve.

The island formula was derived in two independent ways:
- **Penington; Almheiri-Engelhardt-Marolf-Maxfield (2019)**: using quantum extremal surfaces in models coupled to a bath.
- **Replica wormholes (Penington-Shenker-Stanford-Yang; Almheiri-Hartman-Maldacena-Shaghoulian-Tajdini, 2019-2020)**: Euclidean gravity path integral with replica symmetry breaking produces new saddle-point geometries (wormholes connecting replicas) that reproduce the island formula.

## What IS and IS NOT resolved

### What controlled calculations establish

- Assuming an exact duality to a standard unitary boundary theory, bulk evolution must admit a unitary description.
- Island/QES prescriptions reproduce a Page-like curve in controlled models such as JT gravity coupled to a bath and in selected higher-dimensional constructions.
- Replica-wormhole saddle points provide a gravitational path-integral route to these generalized-entropy results, subject to the assumptions of the model, ensemble interpretation, and saddle approximation.

### What is NOT resolved

- **No mechanism**: the island formula tells us *that* information comes out but not *how*. The detailed mechanism by which Hawking radiation carries information remains unknown.
- **Firewall / no-drama**: whether an infalling observer encounters anything unusual at the horizon is not settled. The island formula is a statement about entanglement entropy, not about local physics at the horizon.
- **Real black holes**: all rigorous calculations are in models (JT gravity, AdS). Whether the same mechanism applies to astrophysical black holes in asymptotically flat spacetime is assumed but not proven.
- **Interior interpretation**: what happens inside the black hole after the Page time (when the island appears) remains deeply unclear. The interior may not be a smooth geometry in the usual sense.
- **Size and origin of corrections**: Hawking's calculation is a controlled leading semiclassical result in its regime. How exact unitary information is encoded, and whether a simple universal $e^{-S_{BH}}$ characterization captures the relevant corrections for realistic black holes, remain subjects of research.

## Key results

- Hawking (1976): information loss argument.
- Page (1993): the Page curve as the unitary prediction.
- Susskind (1993): complementarity.
- AMPS (2012): firewall argument.
- Penington (2019), AEMM (2019): island formula from quantum extremal surfaces.
- PSSY, AHMMST (2019-2020): replica wormhole derivation.

## Open questions

1. **Mechanism of information transfer.** How does information get from behind the horizon to the radiation?
2. **Interior geometry.** What is the correct description of the black hole interior after the Page time?
3. **Flat space.** Do islands and replica wormholes work without AdS/CFT?
4. **Massive remnant problem.** If the endpoint of evaporation is a Planck-mass remnant, how is the information released?
5. **Experimental signatures.** Are there observable consequences of information preservation (e.g., in gravitational wave echoes or analog black holes)?

## Connection to other fields

- [[Hawking Radiation]]: the source of the problem.
- [[Black Hole Thermodynamics]]: entropy counting and the generalized second law.
- [[Holographic Principle]] and [[AdS-CFT Correspondence]]: frameworks in which a unitary description is strongly motivated, conditional on the proposed duality.
- [[Quantum Error Correction and Gravity]]: bulk reconstruction and entanglement wedges are central to the island formula.
- [[Quantum Entanglement]]: monogamy of entanglement is the core tension.
- [[Quantum Gravity]]: the information problem is a primary motivation for quantum gravity research.
- [[Decoherence]]: distinguishing genuine information loss from effective decoherence.

## Sources

- Hawking, S. W. (1976). "Breakdown of predictability in gravitational collapse." *Phys. Rev. D* 14, 2460.
- Page, D. N. (1993). "Average entropy of a subsystem." *Phys. Rev. Lett.* 71, 1291. arXiv:gr-qc/9305007.
- Almheiri, A., Marolf, D., Polchinski, J., Sully, J. (2013). "Black holes: complementarity vs. firewalls." *JHEP* 02, 062. arXiv:1207.3123.
- Penington, G. (2020). "Entanglement wedge reconstruction and the information problem." *JHEP* 09, 002. arXiv:1905.08255.
- Almheiri, A., Engelhardt, N., Marolf, D., Maxfield, H. (2019). "The entropy of bulk quantum fields and the entanglement wedge of an evaporating black hole." *JHEP* 12, 063. arXiv:1905.08762.
- Almheiri, A., Hartman, T., Maldacena, J., Shaghoulian, E., Tajdini, A. (2021). "The entropy of Hawking radiation." *Rev. Mod. Phys.* 93, 035002. arXiv:2006.06872. (Review.)

## Epistemic status

**Open.** Page-like curves have been derived in tractable gravitational models, demonstrating compatibility between semiclassical gravitational entropy prescriptions and unitary expectations in those settings. The microscopic mechanism, interior interpretation, ensemble subtleties, endpoint of evaporation, and applicability to realistic asymptotically flat black holes remain open.

## Navigation

[[Physics Worldmap]] · [[Relativity and Gravitation Map]] · [[Black Holes]] · [[Hawking Radiation]] · [[Black Hole Thermodynamics]] · [[Holographic Principle]] · [[AdS-CFT Correspondence]]
