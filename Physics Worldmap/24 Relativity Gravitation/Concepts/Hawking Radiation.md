---
type: "concept"
field: "Relativity and Gravitation"
epistemic_status: "mixed"
level: "advanced"
tags: ["physics", "field/relativity", "status/mixed", "level/advanced"]
aliases: []
created: 2026-07-30
updated: 2026-09-02
note_maturity: expanded
source_audit: bibliography-present-needs-claim-audit
---

# Hawking Radiation

> [!summary] Core idea
> Semiclassical quantum field theory predicts approximately thermal radiation from a stationary black-hole horizon, with $T_H$ set by its surface gravity; the inverse-mass form applies specifically to a Schwarzschild black hole.

> [!note] Documentation status
> This expanded note includes a canonical bibliography but has not yet received a claim-by-claim source audit. The epistemic label describes the standing of the underlying physics in its stated regime; it does not certify every sentence or equation in this note.

## Mathematical handle

$T_H=\hbar\kappa/(2\pi c k_B)$; for Schwarzschild, $\kappa=c^4/(4GM)$

The expression is an orientation point, not a substitute for checking assumptions, sign conventions, units, boundary conditions, and the regime in which it was derived.

## Epistemic status

**Mixed.** The Hawking effect is a robust, model-conditional result of quantum field theory on a classical black-hole spacetime. Hawking radiation from an astrophysical black hole has not been directly detected, and the late evaporation regime lies beyond the controlled semiclassical approximation.

## Place in the world map

- Domain: [[Relativity and Gravitation Map]]
- Field-level guiding question (context only): “What observations are invariant across observers and coordinate systems?”
- Nearby concepts: [[Physics Worldmap]] · [[Relativity and Gravitation Map]] · [[Black Hole Thermodynamics|← previous]] · [[Singularities and Cosmic Censorship|next →]]

## Physical content

Hawking radiation is the theoretical prediction that black holes are not perfectly black but emit thermal radiation with a characteristic temperature inversely proportional to their mass. Stephen Hawking derived this result in 1974-1975 by studying the behavior of [[Quantum Field Theory and Particle Physics Map|quantum fields]] propagating on a classical black hole spacetime that forms from gravitational collapse. The calculation revealed a deep connection between gravity, quantum mechanics, and thermodynamics that remains one of the most important results in theoretical physics.

The physical picture proceeds as follows. Consider a quantum field in the vacuum state long before a star collapses to form a black hole. Field modes of definite positive frequency with respect to the time coordinate of the distant past propagate inward, pass through the collapsing matter, and emerge in the exterior of the newly formed black hole. However, the extreme gravitational blueshift near the forming horizon stretches and scrambles these modes: a mode that was positive-frequency in the past becomes a superposition of positive- and negative-frequency modes with respect to the natural time coordinate of a late-time observer at infinity. This **mode mixing** means that the initial vacuum state contains particles as perceived by the late-time observer. Hawking showed, via a **Bogoliubov transformation** relating the "in" and "out" mode decompositions, that the resulting particle spectrum is precisely thermal -- a Planck distribution at temperature $T_H$.

The key step in the derivation is tracing the high-frequency outgoing modes backward in time. A mode that reaches infinity at late retarded time $u$ originated from a mode that passed exponentially close to the last ray that just fails to escape the black hole. The relationship between the ingoing and outgoing coordinates near the horizon is logarithmic: $u \sim -\bar\kappa^{-1} \ln(v_0 - v)$, where $v_0$ labels the last ingoing null ray that forms the horizon and $\bar\kappa=\kappa/c$ is the surface-gravity redshift rate. For Schwarzschild, $\kappa=c^4/(4GM)$ and $\bar\kappa=c^3/(4GM)$. This exponential redshift is the origin of the thermal spectrum. The Bogoliubov coefficient connecting positive-frequency "in" modes to negative-frequency "out" modes satisfies $|\beta_{\omega\omega'}|^2 / |\alpha_{\omega\omega'}|^2 = e^{-2\pi\omega/\bar\kappa}$, which is the Boltzmann factor for a thermal distribution at $T_H = \hbar\bar\kappa/(2\pi k_B)=\hbar\kappa/(2\pi c k_B)$.

The **[[Horizons Effective Temperatures and Information|Unruh Effect]]** provides an illuminating flat-spacetime analogue. A uniformly accelerating observer in Minkowski space perceives the Minkowski vacuum as a thermal bath at the Unruh temperature $T_U = \hbar a/(2\pi c k_B)$, where $a$ is the proper acceleration. By the equivalence principle, an observer hovering at fixed radius outside a black hole is accelerating; the local Unruh temperature they perceive, when redshifted to infinity, yields exactly the Hawking temperature. This connection underscores that Hawking radiation is fundamentally a consequence of the interplay between quantum fields and horizons, not specific to black holes.

Hawking radiation has profound implications for the [[Black Hole Thermodynamics|thermodynamics of black holes]]. Combined with Bekenstein's identification of black hole entropy $S = k_B A/(4\ell_P^2)$, it turns the correspondence between black-hole mechanics and thermodynamics into a semiclassical thermodynamic relation, schematically $d(Mc^2) = T_H\,dS + \Omega\,dJ + \Phi\,dQ$. A radiating Schwarzschild black hole loses mass on a semiclassical timescale $\tau \sim G^2 M^3/(\hbar c^4)$, which for a solar-mass black hole is $\sim 10^{67}$ years. The approximation does not determine the Planck-scale endpoint, so complete evaporation is not an established conclusion.

## Mathematical framework

The **Hawking temperature** for a Schwarzschild black hole of mass $M$ is:

$$T_H = \frac{\hbar c^3}{8\pi G M k_B} \approx 6.17 \times 10^{-8} \left(\frac{M_\odot}{M}\right)\ \text{K}$$

where $\hbar$ is the reduced Planck constant, $G$ is Newton's gravitational constant, $c$ is the speed of light, $k_B$ is Boltzmann's constant, and $M_\odot$ is the solar mass. For a black hole of mass $M \sim M_\odot$, this temperature is $\sim 10^{-8}$ K -- negligible compared to the CMB temperature of 2.7 K.

The **Bogoliubov transformation** connecting "in" modes $\{f_\omega\}$ and "out" modes $\{p_\omega, \bar{p}_\omega\}$ (where $\bar{p}_\omega$ are modes that fall into the black hole) is:

$$f_\omega = \int_0^\infty d\omega' \left(\alpha_{\omega\omega'}\, p_{\omega'} + \beta_{\omega\omega'}\, \bar{p}_{\omega'}\right)$$

The expected number of particles in mode $\omega$ observed at infinity is:

$$\langle N_\omega \rangle = \int_0^\infty d\omega'\, |\beta_{\omega\omega'}|^2 = \frac{\Gamma_\omega}{e^{2\pi\omega/\bar\kappa} - 1}$$

where $\Gamma_\omega$ is the greybody factor (the transmission probability through the effective potential barrier surrounding the black hole) and $\bar\kappa=\kappa/c$ is the surface gravity expressed as a frequency. For a Schwarzschild black hole, $\bar\kappa=c^3/(4GM)$. The factor $1/(e^{2\pi\omega/\bar\kappa} - 1)$ is the Bose-Einstein distribution at temperature $T = \hbar\bar\kappa/(2\pi k_B)=T_H$.

The **luminosity** of the Hawking process (for a Schwarzschild black hole, dominated by massless fields) scales as:

$$P \sim \frac{\hbar c^6}{G^2 M^2}$$

giving an **evaporation time**:

$$\tau \sim \frac{G^2 M^3}{\hbar c^4} \approx 2.1 \times 10^{67} \left(\frac{M}{M_\odot}\right)^3\ \text{years}$$

For Kerr and Reissner-Nordstrom black holes, the temperature generalizes: for a Kerr black hole with angular momentum $J$,

$$T_H = \frac{\hbar c}{4\pi k_B} \cdot \frac{r_+ - r_-}{r_+^2 + a^2}$$

where $r_\pm = GM/c^2 \pm \sqrt{(GM/c^2)^2 - a^2}$ and $a = J/(Mc)$.

## Key results and implications

- Within semiclassical gravity, Hawking radiation makes black-hole temperature and entropy operational thermodynamic quantities rather than merely formal analogies.
- A black hole that emits radiation loses mass. Extrapolating the semiclassical temperature suggests accelerating evaporation, but the final state—complete evaporation, a remnant, or something else—requires [[Quantum Gravity]] and is unknown.
- The **information paradox**: if the radiation is exactly thermal (carrying no information about the initial state that formed the black hole), then the evaporation process maps pure states to mixed states, violating unitarity. This paradox has driven decades of research, leading to proposals including black hole complementarity, the firewall argument (AMPS, 2012), soft hair (Hawking-Perry-Strominger, 2016), and the island formula involving quantum extremal surfaces.
- The [[Black Hole Thermodynamics|Generalized Second Law]] -- that the sum of ordinary entropy plus black hole entropy never decreases -- is consistent with Hawking radiation: as the black hole shrinks, its Bekenstein-Hawking entropy decreases, but the entropy of the emitted radiation more than compensates.

## Failure modes and limitations

- The **trans-Planckian problem**: outgoing Hawking quanta observed at infinity with wavelength $\sim R_S$ (the Schwarzschild radius) originated as modes with exponentially short wavelengths near the horizon, far beyond the Planck scale. The derivation assumes that ordinary quantum field theory applies to these trans-Planckian modes, which is questionable. Studies using modified dispersion relations (Unruh, 1995; Corley and Jacobson, 1996) show that the thermal spectrum is robust against Planck-scale modifications, but this remains an assumption.
- The calculation is performed in the **semiclassical approximation**: the metric is treated classically, and only the matter fields are quantized. This is self-consistent only when the backreaction of the radiation on the geometry is small, which fails near the endpoint of evaporation.
- A common misconception is that Hawking radiation arises from virtual particle pairs straddling the horizon, with one partner falling in and the other escaping. While this is a useful heuristic, it is misleading: the actual derivation involves global mode decomposition, not local pair creation at the horizon.
- The greybody factors $\Gamma_\omega$ are often omitted in popular treatments; their inclusion means the spectrum is not perfectly Planckian but is modified by the black hole's effective potential.

## Experimental evidence

Hawking radiation has never been directly observed. For astrophysical black holes, the Hawking temperature is many orders of magnitude below the CMB temperature, making detection impossible with current or foreseeable technology. However:

- **Analogue gravity experiments**: In 2016 and subsequent work, Jeff Steinhauer (Technion) reported the observation of thermal phonon emission from a sonic horizon in a Bose-Einstein condensate, constituting an analogue of Hawking radiation. The measured spectrum was approximately thermal and exhibited quantum correlations (entanglement) between the partner modes on opposite sides of the horizon.
- **Primordial black holes**: If black holes with initial mass $\sim 5 \times 10^{11}$ kg formed in the early universe, they would be completing their evaporation now, potentially producing detectable gamma-ray bursts. No such signal has been confirmed, placing constraints on the abundance of such primordial black holes.
- The theoretical prediction is widely regarded as robust because it follows from well-established principles (quantum field theory on curved spacetime, the equivalence principle) with minimal assumptions.

## Sources

- S. W. Hawking, "Particle creation by black holes," *Communications in Mathematical Physics* **43**, 199 (1975).
- R. M. Wald, *Quantum Field Theory in Curved Spacetime and Black Hole Thermodynamics*, University of Chicago Press, 1994.
- L. Susskind and J. Lindesay, *An Introduction to Black Holes, Information and the String Theory Revolution*, World Scientific, 2005.

## Reasoning checks

1. State the physical objects and observables without using the displayed equation.
2. Check dimensions and identify every limiting assumption.
3. Give one regime where this description succeeds and one where it needs correction.
4. Name an experiment, simulation, or observation that could determine its parameters.
5. Explain how this idea changes when the dominant length, time, energy, or particle-number scale changes.

## Expansion queue

- [x] Add a derivation from the nearest prerequisite principles.
- [x] Add a worked example with units.
- [x] Add a primary or canonical source.
- [x] Add a failure case, misconception, or counterexample.

## Navigation

[[Physics Worldmap]] · [[Relativity and Gravitation Map]] · [[Black Hole Thermodynamics|← previous]] · [[Singularities and Cosmic Censorship|next →]]
