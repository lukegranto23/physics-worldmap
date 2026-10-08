---
type: "concept"
field: "Relativity and Gravitation"
epistemic_status: "open"
level: "advanced"
tags: ["physics", "field/relativity", "status/open", "level/advanced"]
aliases: []
created: 2026-07-30
updated: 2026-07-30
note_maturity: expanded
source_audit: bibliography-present-needs-claim-audit
---

# Quantum Gravity

> [!summary] Core idea
> A quantum theory of dynamical spacetime is required where curvature and quantum fluctuations are simultaneously strong.

> [!note] Documentation status
> This expanded note includes a canonical bibliography but has not yet received a claim-by-claim source audit. The epistemic label describes the standing of the underlying physics in its stated regime; it does not certify every sentence or equation in this note.

## Mathematical handle

$\ell_P=\sqrt{\hbar G/c^3}$

The expression is an orientation point, not a substitute for checking assumptions, sign conventions, units, boundary conditions, and the regime in which it was derived.

## Epistemic status

**Open.** This is unresolved. Competing explanations or incomplete evidence must remain visible.

## Place in the world map

- Domain: [[Relativity and Gravitation Map]]
- Field-level guiding question (context only): “What observations are invariant across observers and coordinate systems?”
- Nearby concepts: [[Physics Worldmap]] · [[Relativity and Gravitation Map]] · [[Singularities and Cosmic Censorship|← previous]]

## Physical content

Quantum gravity is the as-yet-unfinished project of unifying [[Quantum Mechanics Map|quantum mechanics]] with [[Relativity and Gravitation Map|general relativity]]. The need arises because general relativity treats spacetime as a smooth, dynamical manifold whose curvature is sourced by matter, while quantum field theory treats fields as operator-valued distributions on a fixed background. These two pictures collide whenever curvature fluctuations become large on scales where quantum effects are important -- near [[Singularities and Cosmic Censorship|singularities]] inside black holes, at the Big Bang, and at the Planck scale $\ell_P \sim 1.6 \times 10^{-35}$ m, $t_P \sim 5.4 \times 10^{-44}$ s, $E_P \sim 1.2 \times 10^{19}$ GeV.

The most immediate obstacle is **non-renormalizability**. If one naively quantizes general relativity by expanding the metric as $g_{\mu\nu} = \eta_{\mu\nu} + \kappa h_{\mu\nu}$ with $\kappa = \sqrt{32\pi G}$ and computes loop diagrams, new ultraviolet divergences appear at each loop order that cannot be absorbed into the existing coupling constants. The gravitational coupling $G$ has dimensions of $[\text{length}]^2$ in natural units, making the theory perturbatively non-renormalizable by power counting. At two loops, Goroff and Sagnotti (1986) showed that pure gravity produces a divergence proportional to $R_{\mu\nu}^{\ \ \rho\sigma} R_{\rho\sigma}^{\ \ \alpha\beta} R_{\alpha\beta}^{\ \ \mu\nu}$ with a nonzero coefficient, confirming that the theory is not finite even in the absence of matter.

Several major research programs address this problem from different angles. **String Theory** replaces point particles with extended one-dimensional objects, which softens ultraviolet behavior and naturally incorporates a massless spin-2 excitation (the graviton). It requires extra spatial dimensions and has an enormous landscape of vacua ($\sim 10^{500}$), making contact with observation difficult. **Loop Quantum Gravity** takes background independence as a starting principle and quantizes the gravitational field directly using Ashtekar connection variables; the resulting Hilbert space has a basis of spin networks, and geometric operators (area, volume) acquire discrete spectra with a minimum area gap $\Delta A \sim \ell_P^2$. **Asymptotic safety** posits that gravity possesses a non-trivial ultraviolet fixed point of the renormalization group, making it non-perturbatively renormalizable despite its perturbative non-renormalizability. **Causal set theory** discretizes spacetime as a locally finite partial order, recovering the manifold only in a continuum limit. **Causal dynamical triangulations** construct a path integral over geometries by gluing simplices with a causal (Lorentzian) structure, producing a four-dimensional universe in numerical simulations.

A conceptual issue that pervades all approaches is the **problem of time**. In canonical general relativity, the Hamiltonian constraint $\mathcal{H} \approx 0$ implies that the total Hamiltonian vanishes, so the Wheeler-DeWitt equation $\hat{\mathcal{H}} |\Psi\rangle = 0$ has no external time parameter. How dynamics and causality emerge from a "frozen" wave function of the universe remains deeply unclear. Closely related is the demand for **background independence**: because the metric is itself the dynamical variable, any quantum theory of gravity should not presuppose a fixed spacetime geometry.

The [[Hawking Radiation|black hole information problem]] provides perhaps the sharpest constraint on quantum gravity. Hawking's calculation shows that black holes radiate thermally, implying that pure states can apparently evolve into mixed states, violating unitarity. Any consistent theory of quantum gravity must explain how information is preserved or must modify quantum mechanics itself. Recent developments involving the [[Quantum Entanglement|island formula]] and replica wormholes in the gravitational path integral suggest that spacetime topology change may be essential to preserving unitarity, but the full picture remains incomplete.

## Mathematical framework

The **Planck scale** sets the natural units where quantum gravitational effects become order one:

$$\ell_P = \sqrt{\frac{\hbar G}{c^3}} \approx 1.616 \times 10^{-35}\ \text{m}, \qquad m_P = \sqrt{\frac{\hbar c}{G}} \approx 2.176 \times 10^{-8}\ \text{kg}, \qquad t_P = \sqrt{\frac{\hbar G}{c^5}} \approx 5.391 \times 10^{-44}\ \text{s}$$

The **Einstein-Hilbert action** that one would like to quantize is:

$$S_{\text{EH}} = \frac{1}{16\pi G} \int d^4x \sqrt{-g}\, R$$

where $g = \det(g_{\mu\nu})$ is the metric determinant and $R$ is the Ricci scalar. Perturbative quantization expands $g_{\mu\nu} = \bar{g}_{\mu\nu} + \kappa h_{\mu\nu}$ around a background $\bar{g}_{\mu\nu}$, yielding graviton propagators and vertices. The graviton propagator in de Donder gauge goes as $\sim 1/k^2$, and the three-graviton vertex carries two derivatives, giving a coupling that grows with energy -- the hallmark of non-renormalizability.

The **Wheeler-DeWitt equation** (the canonical quantization approach) reads:

$$\hat{\mathcal{H}} \Psi[h_{ij}] = \left( -16\pi G\, G_{ijkl} \frac{\delta^2}{\delta h_{ij}\, \delta h_{kl}} - \frac{\sqrt{h}}{16\pi G}\,{}^{(3)}R \right) \Psi[h_{ij}] = 0$$

where $h_{ij}$ is the 3-metric on a spatial slice, $G_{ijkl}$ is the DeWitt supermetric, and ${}^{(3)}R$ is the spatial Ricci scalar. This equation has no time derivative; the wave functional $\Psi$ is annihilated by the Hamiltonian constraint.

In **loop quantum gravity**, the area operator has a discrete spectrum:

$$\hat{A}(\Sigma) = 8\pi \gamma \ell_P^2 \sum_{p} \sqrt{j_p(j_p + 1)}$$

where the sum is over punctures of the spin network with the surface $\Sigma$, $j_p$ are half-integer spin labels, and $\gamma$ is the Barbero-Immirzi parameter.

## Key results and implications

- No fully consistent, predictive quantum theory of gravity currently exists. This makes it the central open problem in fundamental physics.
- Dimensional analysis alone constrains quantum gravitational effects to be negligibly small ($\sim E^2/E_P^2$) at accessible energies, explaining why gravity appears perfectly classical in all existing experiments.
- Black hole entropy $S = A/(4\ell_P^2)$ counts microstates of quantum geometry in both string theory (Strominger-Vafa, 1996) and loop quantum gravity, providing partial evidence for these programs.
- The [[Cosmological Constant Problem]] can be viewed as a low-energy consequence of not understanding the quantum vacuum of gravity.
- If [[Inflation|inflation]] occurred, the primordial gravitational wave spectrum encodes information about energy scales that approach the Planck regime.

## Failure modes and limitations

- All current approaches are incomplete. String theory lacks a non-perturbative, background-independent formulation for cosmological spacetimes. Loop quantum gravity struggles with the semiclassical limit and has not demonstrated the recovery of smooth spacetime dynamics at large scales in full generality. Asymptotic safety has not been proven to exist beyond truncated renormalization group calculations.
- A common misconception is that "spacetime is made of discrete atoms" -- this is a prediction of some approaches (LQG, causal sets) but not others (string theory, asymptotic safety).
- Another error is conflating the Planck scale with a hard boundary beyond which physics is unknowable. The Planck scale marks where current frameworks fail, not a physical barrier.
- Some formulations of quantum gravity (e.g., the string landscape) may be unfalsifiable in practice, raising questions about the boundary between physics and mathematics.

## Experimental evidence

Direct experimental evidence for quantum gravity does not exist. The Planck energy $\sim 10^{19}$ GeV is $10^{15}$ times beyond the reach of the LHC. However, several indirect windows constrain the space of theories:

- **CMB B-mode polarization**: A detection of primordial gravitational waves via B-modes would constrain the energy scale of inflation and probe physics near the Planck scale. The BICEP/Keck experiments currently set upper bounds on the tensor-to-scalar ratio $r < 0.036$ (95% CL).
- **Black hole observations**: The Event Horizon Telescope images of M87* and Sgr A* are consistent with general relativity but do not yet probe quantum gravitational corrections.
- **Gravitational wave echoes**: Post-merger signals from LIGO/Virgo could in principle reveal Planck-scale modifications to the black hole horizon structure; no echoes have been confirmed.
- **Tabletop experiments**: Proposals (Bose et al., 2017; Marletto and Vedral, 2017) aim to detect gravitationally induced entanglement between mesoscopic masses, which would demonstrate that gravity can mediate quantum information.

## Sources

- C. Kiefer, *Quantum Gravity*, 3rd ed., Oxford University Press, 2012.
- C. Rovelli, *Quantum Gravity*, Cambridge University Press, 2004.
- J. Polchinski, *String Theory*, vols. 1-2, Cambridge University Press, 1998.

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

[[Physics Worldmap]] · [[Relativity and Gravitation Map]] · [[Singularities and Cosmic Censorship|← previous]]
