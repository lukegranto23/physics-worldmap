---
type: "concept"
field: "Electromagnetism"
epistemic_status: "established"
level: "advanced"
tags: ["physics", "field/electromagnetism", "status/established", "level/advanced"]
aliases: []
created: 2026-07-30
updated: 2026-09-17
note_maturity: expanded
source_audit: derived-with-canonical-references-and-targeted-checks
---

# Gauge transformations

A gauge transformation changes the potentials describing an electromagnetic configuration without changing its local electric and magnetic fields. It is a redundancy of description, not an operation that rotates the apparatus or physically changes its fields. Quantum matter must be transformed consistently as well; arbitrary potential values are not directly observable.

Prerequisites: [[Vector Calculus]], [[Maxwell Equations]], [[Magnetic Field and Lorentz Force]]. Continue through [[Electromagnetism — Fields Energy and Gauge Study Route]] toward [[Gauge Symmetry]] and [[Covariant Electrodynamics]].

## Definitions and local derivation

In SI units, write

$$
\mathbf B=\nabla\times\mathbf A,
\qquad\mathbf E=-\nabla\phi-\partial_t\mathbf A.
$$

The scalar potential $\phi$ has units volts; $\mathbf A$ has units $\mathrm{V\,s\,m^{-1}}=\mathrm{T\,m}$. For a sufficiently smooth scalar $\chi$ of units $\mathrm{V\,s}$, set

$$
\boxed{\mathbf A'=\mathbf A+\nabla\chi,
\qquad\phi'=\phi-\partial_t\chi.}
$$

Commuting partial derivatives gives

$$
\mathbf B'=\mathbf B+\nabla\times\nabla\chi=\mathbf B,
$$

$$
\mathbf E'=\mathbf E+\nabla\partial_t\chi
-\partial_t\nabla\chi=\mathbf E.
$$

Thus the Lorentz force is unchanged. Locally, the homogeneous Maxwell equations permit a potential description. Global existence and gauge equivalence require attention to the domain, singularities, boundary conditions, and topology. The magnetostatic gradient freedom and its interference interpretation are discussed in [Feynman II, §15–5](https://www.feynmanlectures.caltech.edu/II_15.html); the time-dependent invariance above is explicitly derived here.

## Gauge fixing is a computational choice

Two frequent choices are Coulomb gauge, $\nabla\cdot\mathbf A=0$, and Lorenz gauge,

$$
\nabla\cdot\mathbf A+\frac1{c^2}\partial_t\phi=0.
$$

“Lorenz” names the gauge condition; it is distinct from “Lorentz” in the force law. Substitution shows that a transformation preserves Coulomb gauge when $\nabla^2\chi=0$ and preserves Lorenz gauge when

$$
\left(\nabla^2-\frac1{c^2}\partial_t^2\right)\chi=0.
$$

Gauge fixing can therefore leave residual freedom until boundary and initial conditions are supplied. In Lorenz gauge, the sourced potential equations are wave equations; choosing their retarded solution also imposes a radiation condition, not just a gauge label.

In Coulomb gauge an instantaneous scalar-potential solution does not imply instantaneous transmission of a measurable electric signal: the vector-potential contribution must also be included. [Jackson, “From Lorenz to Coulomb and other explicit gauge transformations” (2002), abstract](https://arxiv.org/abs/physics/0204034) addresses this cancellation and equality of physical fields. It is not evidence for superluminal electromagnetism.

## Worked example: a nonzero electric field with zero scalar potential

Take the idealized uniform static field $\mathbf E=E_0\hat{\mathbf x}$ with $E_0=75\,\mathrm{V\,m^{-1}}$ and $\mathbf B=0$. In a region where this approximation is valid, one representation is

$$
\phi=-E_0x,\qquad\mathbf A=0.
$$

Choose $\chi=-E_0xt$. Then

$$
\phi'=0,\qquad\mathbf A'=-E_0t\hat{\mathbf x},
\qquad-\partial_t\mathbf A'=E_0\hat{\mathbf x}.
$$

At $x=0.024\,\mathrm m$ and $t=0.004\,\mathrm s$,

$$
\phi=-1.8\,\mathrm V,\quad
\chi=-0.0072\,\mathrm{V\,s},\quad
\mathbf A'=-0.300\,\mathrm{V\,s\,m^{-1}}\hat{\mathbf x}.
$$

A positive test charge $q=2.0\,\mathrm{nC}$ experiences $qE_0=1.50\times10^{-7}\,\mathrm N$ in either representation. If it moves $0.024\,\mathrm m$ along $+x$, the field does $qE_0\Delta x=3.60\times10^{-9}\,\mathrm J$ of work. Setting $\phi'=0$ did not remove the force or the work. Inferring the field from $-\nabla\phi'$ alone would discard the essential time-dependent term.

For nonrelativistic motion,

$$
L=\tfrac12m v^2+q\mathbf v\cdot\mathbf A-q\phi,
\qquad L'=L+q\frac{d\chi}{dt}.
$$

The total derivative changes endpoint terms in the action but not the Euler–Lagrange trajectory with fixed endpoints. Canonical momentum changes as $\mathbf p'=\mathbf p+q\nabla\chi$, whereas kinetic momentum remains

$$
m\mathbf v=\mathbf p-q\mathbf A=\mathbf p'-q\mathbf A'.
$$

The canonical-momentum shift at $t=0.004\,\mathrm s$ is $-6.00\times10^{-10}\,\mathrm{kg\,m\,s^{-1}}\hat{\mathbf x}$. It is not a mechanical kick. These values and the endpoint calculation are an original consistency exercise.

## Quantum phase and global topology

With Hamiltonian

$$
H=\frac{(-i\hbar\nabla-q\mathbf A)^2}{2m}+q\phi,
$$

the corresponding transformation is $\psi'=e^{iq\chi/\hbar}\psi$. Direct differentiation shows

$$
(-i\hbar\nabla-q\mathbf A')\psi'
=e^{iq\chi/\hbar}(-i\hbar\nabla-q\mathbf A)\psi.
$$

The extra time derivative cancels the shift in $q\phi$. Density and mechanical current are unchanged, although the phase assigned to $\psi$ changes.

Around an inaccessible static flux tube, interference may depend on

$$
\exp\!\left(\frac{iq}{\hbar}\oint\mathbf A\cdot d\boldsymbol\ell\right)
=\exp(iq\Phi/\hbar).
$$

This loop quantity is invariant under smooth, single-valued $\chi$. More general admissible descriptions must preserve single-valued quantum transition phases. A region with a hole can have zero local $\mathbf B$ without every potential being globally gauge-equivalent to zero there. The measurable Aharonov–Bohm phase is not a measurement of a freely chosen gauge. The flux-dependent interference calculation appears in the directly accessible [Feynman II, §15–5](https://www.feynmanlectures.caltech.edu/II_15.html). Also see [Tong, *Applications of Quantum Mechanics*, §1.3.2](https://www.damtp.cam.ac.uk/user/tong/aqm/aqm.pdf); only its indexed static-flux section was accessible during this check.

## Checks and cautions

- For time-independent $\chi$, $\phi$ is unchanged but $\mathbf A$ need not be. A constant $\chi$ changes neither potential.
- Transforming only $\mathbf A$ while ignoring the required scalar-potential or wavefunction change is not a consistent time-dependent gauge transformation.
- A gauge condition is not an extra Maxwell equation or an experimentally imposed restriction on physical fields.
- Local equality of fields does not by itself settle all global quantum boundary conditions. Conversely, the Aharonov–Bohm effect does not abolish gauge redundancy.
- Substitute the numerical example into both gauge conditions. Both potentials satisfy Coulomb and Lorenz gauge here: gauge fixing need not be unique.

## Source-audit boundary

The linked sections support the indicated conventional interpretation, causality statement, and flux-phase example. The displayed algebra and numbers were worked independently. This targeted check does not cover quantization on all spacetime topologies.

## Navigation

[[Physics Worldmap]] · [[Electromagnetism Map]] · [[Antennas and Radiation Patterns|← previous]] · [[Covariant Electrodynamics|next →]] · [[Electromagnetism — Fields Energy and Gauge Study Route]]
