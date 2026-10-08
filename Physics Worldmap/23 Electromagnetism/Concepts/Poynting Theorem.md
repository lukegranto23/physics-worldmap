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

# Poynting theorem

Electromagnetic fields carry energy, exchange it with charged matter, and transport it across boundaries. The useful statement is local: energy lost from a region must enter matter there or flow through its boundary. Circuit power and field-energy flux must agree when they describe the same physical system.

Prerequisites: [[Maxwell Equations]], [[Vector Calculus]], [[Magnetic Field and Lorentz Force]]. Study route: [[Electromagnetism — Fields Energy and Gauge Study Route]].

## Convention and scope

Use SI units and a fixed control volume. For microscopic fields with **total** charge-current density $\mathbf J$, define

$$
u=\frac{\epsilon_0 E^2}{2}+\frac{B^2}{2\mu_0},
\qquad
\mathbf S=\frac{\mathbf E\times\mathbf B}{\mu_0}.
$$

Here $u$ has units $\mathrm{J\,m^{-3}}$, $\mathbf S$ has units $\mathrm{W\,m^{-2}}$, and $\mathbf J\cdot\mathbf E$ has units $\mathrm{W\,m^{-3}}$. The vacuum constants appear even when microscopic charges are present; “vacuum form” does not mean $\mathbf J=0$. Singular point-charge self-fields require additional care beyond this smooth-field derivation.

The balance is

$$
\boxed{\partial_tu+\nabla\cdot\mathbf S=-\mathbf J\cdot\mathbf E.}
$$

Positive $\mathbf J\cdot\mathbf E$ means the field does work on matter. The magnetic force contributes no instantaneous particle power because $\mathbf v\cdot(\mathbf v\times\mathbf B)=0$. These are the microscopic energy-transfer conventions in [Feynman II, §§27–2–27–3](https://www.feynmanlectures.caltech.edu/II_27.html).

## Derivation to reproduce

Dot the Ampère–Maxwell equation with $\mathbf E/\mu_0$:

$$
\frac1{\mu_0}\mathbf E\cdot(\nabla\times\mathbf B)
=\mathbf J\cdot\mathbf E+\epsilon_0\mathbf E\cdot\partial_t\mathbf E.
$$

Use the product identity

$$
\nabla\cdot(\mathbf E\times\mathbf B)
=\mathbf B\cdot(\nabla\times\mathbf E)
-\mathbf E\cdot(\nabla\times\mathbf B),
$$

then substitute Faraday's law $\nabla\times\mathbf E=-\partial_t\mathbf B$. The two remaining field terms combine into $\partial_tu$, proving the balance. No plane-wave approximation was used.

Integration over a stationary volume $V$, with outward normal $\mathbf n$, gives

$$
\frac{d}{dt}\int_Vu\,d^3x
=-\oint_{\partial V}\mathbf S\cdot\mathbf n\,dA
-\int_V\mathbf J\cdot\mathbf E\,d^3x.
$$

Outward flux removes field energy; inward flux supplies it. A moving boundary needs the corresponding transport term and is not covered by merely reusing this fixed-volume expression. Field energy need not be conserved separately from material energy.

## Worked example: power entering a resistive segment

Consider an idealized long cylindrical resistor carrying steady current along $+z$. Choose radius $a=0.50\,\mathrm{mm}$, length $\ell=0.12\,\mathrm m$, conductivity $\sigma=2.0\times10^6\,\mathrm{S\,m^{-1}}$, and current $I=0.80\,\mathrm A$. Assume uniform current, constant conductivity, no magnetization, and a sufficiently remote or coaxially symmetric return path; neglect end effects. This local long-cylinder approximation is not a complete circuit-field solution.

Ohm's law gives

$$
J_z=\frac{I}{\pi a^2}=1.019\times10^6\,\mathrm{A\,m^{-2}},
\qquad E_z=\frac{J_z}{\sigma}=0.5093\,\mathrm{V\,m^{-1}}.
$$

At the cylindrical surface,

$$
B_\varphi(a)=\frac{\mu_0 I}{2\pi a}\simeq3.20\times10^{-4}\,\mathrm T.
$$

Because $\hat{\mathbf z}\times\hat{\boldsymbol\varphi}=-\hat{\mathbf r}$, the energy flux points **inward**, with

$$
S_r(a)=-\frac{E_zB_\varphi}{\mu_0}
=-129.69\,\mathrm{W\,m^{-2}}.
$$

The incoming lateral power is

$$
P_{\rm in}=2\pi a\ell |S_r|=0.04889\,\mathrm W.
$$

Independently, the voltage drop is $E_z\ell=0.06112\,\mathrm V$, giving $I\Delta V=0.04889\,\mathrm W$. Integrating $\sigma E_z^2$ over the resistor gives the same heat-production rate. The field energy is stationary, not vanishing; inward flux balances conversion to material energy.

This numerical exercise is constructed here, not copied from a textbook problem. The broader point that steady fields can feed dissipation is discussed in [Feynman II, §27–5](https://www.feynmanlectures.caltech.edu/II_27.html). Surface charge and the external supply establish the fields; treating the resistor alone does not locate every part of the complete energy path.

## What changes inside materials?

The macroscopic equations give an exact identity

$$
\nabla\cdot(\mathbf E\times\mathbf H)
=-\mathbf J_{\rm free}\cdot\mathbf E
-\mathbf E\cdot\partial_t\mathbf D
-\mathbf H\cdot\partial_t\mathbf B.
$$

For a stationary, linear, isotropic, nondispersive medium with time-independent positive $\epsilon,\mu$, the last two terms are $-\partial_t(\epsilon E^2/2+\mu H^2/2)$. Those restrictions make this simple positive stored-energy formula possible. The conventions are given in [MIT 6.974, §2.1.3 and Table 2.1](https://ocw.mit.edu/courses/6-974-fundamentals-of-photonics-quantum-electronics-spring-2006/ce6075363fa304e0a61078f7048e96f9_maxwell_eq_iso.pdf).

With temporal dispersion, $\mathbf D(t)$ depends on the field's history. Replacing $\epsilon_0$ by $\epsilon(\omega)$ inside an instantaneous quadratic energy formula is not justified. Absorption also transfers energy into material degrees of freedom. A material model and a stated field/material energy split are needed; microscopic conservation has not failed. [Philbin, *Physical Review A* 83, 013823, abstract](https://doi.org/10.1103/PhysRevA.83.013823) specifically treats conserved energy in dispersive, lossless media, not arbitrary lossy media.

## Checks and common errors

- A resistor with $I\to0$ has $P\to0$ quadratically. Reversing $I$ reverses both fields and leaves inward power unchanged.
- A vacuum traveling plane wave obeys $|\mathbf S|=cu$; arbitrary configurations need not. Static stored electric energy may have $\mathbf S=0$.
- Zero net outward flux does not imply zero local flux. Standing waves can exchange energy locally without time-averaged net power.
- $\mathbf S$ is a flux, not an energy density. Power requires an oriented area integral and, when appropriate, a time average.
- Correctly applying this established theorem is a consistency test, not a new theory of energy transport.

## Source-audit boundary

The linked source sections were checked for the stated conventions and qualifications; the algebra and numerical exercise were worked independently. This is targeted verification, not a complete audit of electromagnetic energy in every material.

## Navigation

[[Physics Worldmap]] · [[Electromagnetism Map]] · [[Electromagnetic Waves|← previous]] · [[Electromagnetic Momentum|next →]] · [[Electromagnetism — Fields Energy and Gauge Study Route]]
