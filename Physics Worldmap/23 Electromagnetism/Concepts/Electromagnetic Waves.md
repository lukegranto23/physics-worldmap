---
type: "concept"
field: "Electromagnetism"
epistemic_status: "established"
level: "intermediate"
tags: ["physics", "field/electromagnetism", "status/established", "level/intermediate"]
aliases: []
created: 2026-07-30
updated: 2026-09-17
note_maturity: expanded
source_audit: derived-with-canonical-references-and-targeted-checks
---

# Electromagnetic waves

In a source-free vacuum region, Maxwell's equations admit traveling disturbances of the electric and magnetic fields. Their propagation does not require a material medium. The simplest solution, a traveling plane wave, is a useful local model far from a radiation source; it is not a universal description near charges, within waveguides, or inside matter.

Prerequisites: [[Maxwell Equations]], [[Vector Calculus]], [[Polarization]]. Energy accounting continues in [[Poynting Theorem]]. Follow [[Electromagnetism — Fields Energy and Gauge Study Route]] for a derivation-and-check sequence.

## From Maxwell's equations to a wave equation

Assume classical linear vacuum electrodynamics in an inertial frame, with $\rho=0$ and $\mathbf J=0$ throughout the region under consideration. In SI units,

$$
\nabla\cdot\mathbf E=0,\quad\nabla\cdot\mathbf B=0,
\quad\nabla\times\mathbf E=-\partial_t\mathbf B,
\quad\nabla\times\mathbf B=\mu_0\epsilon_0\partial_t\mathbf E.
$$

Take the curl of Faraday's equation and use $\nabla\times(\nabla\times\mathbf E)=\nabla(\nabla\cdot\mathbf E)-\nabla^2\mathbf E$. The divergence term vanishes, leaving

$$
\left(\nabla^2-\frac1{c^2}\partial_t^2\right)\mathbf E=0,
\qquad c=\frac1{\sqrt{\mu_0\epsilon_0}}.
$$

The same manipulation gives the wave equation for $\mathbf B$. Independently solving two vector wave equations can nevertheless produce pairs that violate Maxwell's coupling and divergence constraints. Retain those constraints when choosing initial data. [Feynman II, §§20–1–20–2](https://www.feynmanlectures.caltech.edu/II_20.html) provides the source-free plane-wave and three-dimensional derivations.

## Plane-wave relations and their signs

Use real fields represented by complex amplitudes with convention

$$
\mathbf E(\mathbf r,t)=\operatorname{Re}\{\mathbf E_0e^{i(\mathbf k\cdot\mathbf r-\omega t)}\},
\qquad\omega>0.
$$

Substitution gives

$$
\mathbf k\cdot\mathbf E_0=\mathbf k\cdot\mathbf B_0=0,
\quad\mathbf k\times\mathbf E_0=\omega\mathbf B_0,
\quad\omega=c|\mathbf k|.
$$

Thus $\mathbf B_0=\hat{\mathbf k}\times\mathbf E_0/c$. The cross-product sign identifies the propagation direction. For a linearly polarized wave moving along $+z$,

$$
\mathbf E=E_0\cos(kz-\omega t)\hat{\mathbf x},
\qquad\mathbf B=\frac{E_0}{c}\cos(kz-\omega t)\hat{\mathbf y}.
$$

Here $E_0$ is the **peak**, not rms, amplitude. The fields are in phase; at a zero crossing both vanish. A complex $\mathbf E_0$ can represent elliptical polarization through relative phases of its transverse components.

For this single traveling wave, the instantaneous electric and magnetic energy densities are equal. Hence

$$
u=\epsilon_0 E^2,\qquad\mathbf S=cu\hat{\mathbf k},
\qquad\langle S\rangle=\frac12\epsilon_0cE_0^2=\frac{E_0^2}{2Z_0},
$$

where $Z_0=\sqrt{\mu_0/\epsilon_0}\simeq376.73\,\Omega$. The factor $1/2$ comes from averaging $\cos^2$, not from weakening the magnetic contribution. With rms amplitude instead, $\langle S\rangle=E_{\rm rms}^2/Z_0$.

## Worked example: a radio-frequency plane wave

Construct a vacuum wave with $f=150\,\mathrm{MHz}$ and peak electric amplitude $E_0=12.0\,\mathrm{V\,m^{-1}}$. Take propagation along $+z$ and electric polarization along $x$. Using $c=299792458\,\mathrm{m\,s^{-1}}$,

$$
\lambda=\frac cf=1.99862\,\mathrm m,\qquad
\omega=2\pi f=9.42478\times10^8\,\mathrm{s^{-1}},
$$

$$
k=\frac{2\pi}{\lambda}=3.14377\,\mathrm{m^{-1}},\qquad
B_0=\frac{E_0}{c}=4.00277\times10^{-8}\,\mathrm T.
$$

With $\epsilon_0\simeq8.85419\times10^{-12}\,\mathrm{F\,m^{-1}}$,

$$
\langle S\rangle=0.191118\,\mathrm{W\,m^{-2}},\qquad
\langle u\rangle=6.37502\times10^{-10}\,\mathrm{J\,m^{-3}}.
$$

A surface of area $8.0\,\mathrm{cm^2}=8.0\times10^{-4}\,\mathrm{m^2}$, normal to propagation, has mean incident electromagnetic flux $P=0.152895\,\mathrm{mW}$ through it. This is a geometric flux calculation, **not** an assertion that a small antenna absorbs that power: receiving power depends on effective aperture, polarization, impedance matching, and scattering. Tilting a geometric surface through angle $\theta$ multiplies its flux by $\cos\theta$ for a locally uniform wave.

These numerical choices are an original exercise. Check units independently: $\epsilon_0cE_0^2$ is power per area, whereas $\epsilon_0E_0^2$ is energy per volume. The distinction prevents confusing an intensity measurement with total radiation energy.

## Counterexample: source-free does not mean one traveling wave

Add equal linearly polarized waves traveling along $+z$ and $-z$. One consistent standing-wave pair is

$$
E_x=2E_0\cos(kz)\cos(\omega t),
\qquad
B_y=\frac{2E_0}{c}\sin(kz)\sin(\omega t).
$$

At $z=0$, the magnetic field vanishes at every instant while the electric field oscillates. Thus $E=cB$ and equal electric/magnetic energy do not hold pointwise for arbitrary source-free superpositions. The local Poynting flux oscillates, but its time average is zero. The field stores energy without net traveling-wave power. Direct substitution into Faraday's law checks the relative sign; merely summing electric fields would miss this constraint.

## Material waves and limits of the model

In a homogeneous, stationary, isotropic, linear **nondispersive lossless** medium with positive $\epsilon,\mu$, the analogous transverse plane-wave speed is $v=1/\sqrt{\epsilon\mu}$, and impedance is $\sqrt{\mu/\epsilon}$. These are material parameters, not automatically vacuum constants. In a transparent dispersive band, real $k$ depends on frequency; phase speed $\omega/k$ and narrow-band envelope speed $(dk/d\omega)^{-1}$ need not agree. Loss, anisotropy, spatial dispersion, or guided boundaries require further changes. [MIT 6.974, §§2.1.2 and 2.1.6–2.1.7](https://ocw.mit.edu/courses/6-974-fundamentals-of-photonics-quantum-electronics-spring-2006/ce6075363fa304e0a61078f7048e96f9_maxwell_eq_iso.pdf) treats isotropic propagation and dispersion conventions.

The transverse claim above concerns a propagating vacuum plane-wave component; longitudinal electric fields can occur near sources, in guided configurations, and in plasma modes. An infinite plane wave also has infinite total energy, so it idealizes a finite beam or wave packet over a limited region. Where quantum processes or nonlinear vacuum response matter, classical linear vacuum electrodynamics is itself an approximation.

## Retrieval checks

1. Reverse propagation without changing electric polarization. Which magnetic sign must change?
2. Double $E_0$: $B_0$ doubles, but intensity quadruples. Change $f$ at fixed $E_0$: vacuum wavelength changes, while ideal intensity does not.
3. Explain why the standing wave satisfies Maxwell's equations but violates the single-traveling-wave amplitude rule.
4. Identify the information needed to turn incident flux into received antenna power.

## Source-audit boundary

The linked sections support the stated vacuum and material conventions. Algebra, the numerical example, and the standing-wave check were worked independently. This note does not provide a full treatment of radiation, waveguide modes, or material constitutive response.

## Navigation

[[Physics Worldmap]] · [[Electromagnetism Map]] · [[Maxwell Equations|← previous]] · [[Poynting Theorem|next →]] · [[Electromagnetism — Fields Energy and Gauge Study Route]]
