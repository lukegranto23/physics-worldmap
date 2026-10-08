---
type: "concept"
field: "Cosmology"
epistemic_status: "open"
level: "advanced"
tags: ["physics", "field/cosmology", "status/open", "level/advanced"]
aliases: []
created: 2026-07-30
updated: 2026-07-30
note_maturity: expanded
source_audit: bibliography-present-needs-claim-audit
---

# Cosmological Constant Problem

> [!summary] Core idea
> Observed vacuum-like energy is extraordinarily small relative to naive quantum-field estimates and not understood.

> [!note] Documentation status
> This expanded note includes a canonical bibliography but has not yet received a claim-by-claim source audit. The epistemic label describes the standing of the underlying physics in its stated regime; it does not certify every sentence or equation in this note.

## Mathematical handle

$\rho_\Lambda^{1/4}\sim\mathrm{meV}$

The expression is an orientation point, not a substitute for checking assumptions, sign conventions, units, boundary conditions, and the regime in which it was derived.

## Epistemic status

**Open.** This is unresolved. Competing explanations or incomplete evidence must remain visible.

## Place in the world map

- Domain: [[Cosmology Map]]
- Field-level guiding question (context only): “What are dark matter and dark energy?”
- Nearby concepts: [[Physics Worldmap]] · [[Cosmology Map]] · [[Dark Energy|← previous]] · [[Hubble Tension|next →]]

## Physical content

The cosmological constant problem is widely regarded as the most severe fine-tuning problem in all of physics. It concerns the enormous discrepancy between the observed value of the vacuum energy density driving the accelerated expansion of the universe and the value predicted by naive estimates from [[Quantum Field Theory and Particle Physics Map|quantum field theory]]. The discrepancy spans roughly 120 orders of magnitude -- by far the worst quantitative disagreement between theory and observation in the history of science.

In quantum field theory, every field contributes to the vacuum energy through zero-point fluctuations. A free scalar field with mass $m$ has a vacuum energy density obtained by summing the zero-point energies $\frac{1}{2}\hbar\omega_k$ over all modes up to some ultraviolet cutoff $\Lambda$:

$$\rho_{\rm vac} \sim \int_0^\Lambda \frac{d^3k}{(2\pi)^3} \frac{1}{2}\sqrt{k^2 + m^2} \sim \frac{\Lambda^4}{16\pi^2}$$

If the cutoff is set at the Planck scale $\Lambda \sim M_{\rm Pl} \sim 10^{18}$ GeV, this gives $\rho_{\rm vac} \sim M_{\rm Pl}^4 \sim 10^{74}\ \text{GeV}^4$. Even taking a more conservative cutoff at the electroweak scale ($\Lambda \sim 100$ GeV), the estimate is $\rho_{\rm vac} \sim 10^8\ \text{GeV}^4$. The observed value of the vacuum energy density, inferred from the accelerated expansion of the universe ([[Dark Energy]]) and from CMB observations, is:

$$\rho_{\Lambda}^{\rm obs} \sim (2.3 \times 10^{-3}\ \text{eV})^4 \sim 10^{-47}\ \text{GeV}^4$$

The ratio $\rho_{\Lambda}^{\rm obs}/M_{\rm Pl}^4 \sim 10^{-121}$ -- a mismatch of 121 orders of magnitude. This has been called "the worst prediction in all of physics," though more precisely it is a failure of the prediction rather than a wrong answer: the prediction itself rests on assumptions about how vacuum energy gravitates.

The problem actually comes in two parts. The **"old" cosmological constant problem** (pre-1998) was: why is the cosmological constant exactly zero, or at least so small? Many physicists expected that some unknown symmetry would set $\Lambda = 0$. The discovery of the accelerated expansion (Riess et al. 1998, Perlmutter et al. 1999) transformed this into the **"new" cosmological constant problem**: why is $\Lambda$ small but *nonzero*, with a value that happens to be comparable to the present matter density (the "coincidence problem")?

The difficulty with finding a symmetry that sets $\Lambda = 0$ is severe. Supersymmetry, if unbroken, would enforce exact cancellation between bosonic and fermionic contributions to the vacuum energy. But SUSY is broken in nature, and the residual vacuum energy from SUSY breaking is $\rho_{\rm vac} \sim m_{\rm SUSY}^4 \sim (1\ \text{TeV})^4 \sim 10^{12}\ \text{GeV}^4$ -- still 59 orders of magnitude too large. No known symmetry can make $\Lambda$ small without additional fine-tuning. The cosmological constant is not "technically natural" in 't Hooft's sense: setting $\Lambda = 0$ does not enhance the symmetry of the theory in any known way (conformal invariance, which would set it to zero, is badly broken by particle masses).

In [[Relativity and Gravitation Map|General Relativity]], the cosmological constant appears as a free parameter in Einstein's field equations:

$$G_{\mu\nu} + \Lambda g_{\mu\nu} = 8\pi G\, T_{\mu\nu}$$

The total effective cosmological constant is the sum of a "bare" geometric term $\Lambda_{\rm bare}$ and the vacuum energy contributions from all quantum fields: $\Lambda_{\rm eff} = \Lambda_{\rm bare} + 8\pi G\, \rho_{\rm vac}$. The problem is that $\Lambda_{\rm bare}$ and $\rho_{\rm vac}$ must cancel to 120 decimal places to yield the observed value. There is no known mechanism that would enforce such a cancellation.

## Mathematical framework

The **zero-point energy** of a free scalar field regularized with a hard UV cutoff $\Lambda$ gives:

$$\rho_{\rm vac} = \frac{1}{2} \int_0^\Lambda \frac{4\pi k^2\, dk}{(2\pi)^3}\, \sqrt{k^2 + m^2} \approx \frac{\Lambda^4}{16\pi^2} + \frac{m^2\Lambda^2}{16\pi^2} - \frac{m^4}{64\pi^2}\ln\frac{\Lambda^2}{m^2} + \ldots$$

The leading $\Lambda^4$ term is the quartically divergent contribution. Each particle species contributes with a sign: $+$ for bosons, $-$ for fermions. In the Standard Model, summing over all known particles does not produce a cancellation.

The **observed vacuum energy density** corresponds to:

$$\rho_\Lambda^{\rm obs} \approx 5.96 \times 10^{-27}\ \text{kg/m}^3 \approx (2.25 \times 10^{-3}\ \text{eV})^4$$

This sets the scale $\rho_\Lambda^{1/4} \sim \text{meV}$, a remarkably low energy scale with no known particle physics explanation.

**Weinberg's anthropic bound** (1987): Weinberg argued that if the cosmological constant were much larger than observed, galaxies (and hence observers) could not form. Quantitatively, structure formation requires:

$$\rho_\Lambda \lesssim \rho_{\rm matter}(z_{\rm gal}) \sim 10^{-47}\ \text{GeV}^4$$

where $z_{\rm gal} \sim \text{few}$ is the redshift at which galaxy formation occurs. The observed value is within an order of magnitude of this anthropic upper bound. If $\Lambda$ is randomly distributed across a landscape of vacua, the typical value observed by observers would be near this bound -- arguably a successful prediction, made before the 1998 discovery.

The cosmological constant also receives contributions from **phase transitions** in the early universe. The QCD phase transition shifts the vacuum energy by $\delta\rho \sim \Lambda_{\rm QCD}^4 \sim (200\ \text{MeV})^4 \sim 10^{-3}\ \text{GeV}^4$; the electroweak phase transition by $\delta\rho \sim v^4 \sim 10^8\ \text{GeV}^4$. Each of these must be separately cancelled to maintain a small $\Lambda$ after the transition, compounding the fine-tuning.

## Key results and implications

- The cosmological constant problem demonstrates a deep failure in our understanding of how vacuum energy couples to gravity. It is arguably the sharpest clue that our current framework -- quantum field theory plus general relativity -- is incomplete.
- Weinberg's 1987 anthropic prediction of a small but nonzero $\Lambda$ was confirmed by the 1998 discovery of accelerated expansion, lending credibility to landscape/anthropic reasoning (though whether this constitutes an explanation is debated).
- The problem is connected to the [[Hierarchy Problem]]: both involve the radiative instability of dimensionful parameters. However, the cosmological constant problem is far more severe ($10^{120}$ vs. $10^{26}$).
- **Quintessence** models propose a dynamical scalar field $\phi$ with potential $V(\phi)$ that slowly rolls, producing an effective dark energy with $w = p/\rho$ close to but not exactly $-1$. These models trade the cosmological constant problem for the question of why $V(\phi)$ is so flat and $\phi$ is at the right value today. Current observations are consistent with $w = -1$ (a true cosmological constant).
- **Sequestering** (Kaloper and Padilla, 2014) and **unimodular gravity** modify the gravitational sector to decouple vacuum energy from curvature, but face their own difficulties with radiative stability and phase transitions.

## Failure modes and limitations

- A common error is assuming that the zero-point energy "must" gravitate. The calculation of $\rho_{\rm vac} \sim \Lambda^4$ assumes that vacuum fluctuations contribute to the stress-energy tensor in the standard way. It is logically possible that vacuum energy does not gravitate, or gravitates differently than ordinary matter, but no consistent framework implementing this is known (the Casimir effect confirms that differences in vacuum energy produce measurable forces, but the absolute vacuum energy's gravitational effect has never been measured).
- Normal ordering or subtracting the zero-point energy by hand removes the divergent contribution but provides no physical justification for why the remainder should be small.
- Supersymmetry cancels the vacuum energy only when unbroken. Once SUSY is broken (as it must be), the residual vacuum energy is set by the SUSY-breaking scale, which is many orders of magnitude above the observed $\rho_\Lambda$.
- Some approaches (e.g., the string landscape) trade a dynamical explanation for a statistical one. Whether this constitutes a satisfactory resolution is a matter of ongoing debate in the foundations of physics.
- The problem is sometimes conflated with the dark energy problem. If the cosmological "constant" is not actually constant (i.e., $w \neq -1$), the problem changes character but does not disappear.

## Experimental evidence

- **Type Ia supernovae**: The 1998 discovery of accelerated expansion by the Supernova Cosmology Project (Perlmutter et al.) and the High-z Supernova Search Team (Riess et al.) established that $\Lambda > 0$. This observation earned the 2011 Nobel Prize in Physics.
- **CMB anisotropies**: Planck satellite data (2018) constrain the dark energy density parameter to $\Omega_\Lambda = 0.6847 \pm 0.0073$, consistent with a cosmological constant ($w = -1.03 \pm 0.03$).
- **Baryon acoustic oscillations (BAO)**: Galaxy surveys (SDSS, DESI) measure the expansion history and confirm $\Lambda$CDM as the concordance model. DESI early results (2024) hinted at possible evolution of $w$ with redshift, but the significance is not yet conclusive.
- **Casimir effect**: Measurements of the Casimir force between conducting plates confirm that differences in zero-point energy produce real physical effects, establishing that vacuum fluctuations are not merely a formal device -- though this says nothing about the absolute value of $\rho_{\rm vac}$.

## Sources

- S. Weinberg, "The cosmological constant problem," *Reviews of Modern Physics* **61**, 1 (1989).
- J. Martin, "Everything you always wanted to know about the cosmological constant problem (but were afraid to ask)," *Comptes Rendus Physique* **13**, 566 (2012).
- S. M. Carroll, "The cosmological constant," *Living Reviews in Relativity* **4**, 1 (2001).

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

[[Physics Worldmap]] · [[Cosmology Map]] · [[Dark Energy|← previous]] · [[Hubble Tension|next →]]
