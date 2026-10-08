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

# Maxwell Equations

Maxwell's equations constrain electromagnetic fields and specify how they evolve with charge and current. They are a classical physical theory, not a consequence of vector calculus alone. The mathematics below derives consistency conditions and predictions **from** that theory.

## 1. Conventions and scope

Use SI units in a fixed inertial frame. $\mathbf E$ is in V m$^{-1}$, $\mathbf B$ in tesla, total charge density $\rho$ in C m$^{-3}$, and total current density $\mathbf J$ in A m$^{-2}$. The microscopic/vacuum-form equations are

$$
\nabla\cdot\mathbf E=\rho/\epsilon_0,\qquad
\nabla\cdot\mathbf B=0,
$$
$$
\nabla\times\mathbf E=-\partial_t\mathbf B,\qquad
\nabla\times\mathbf B=\mu_0\mathbf J+\mu_0\epsilon_0\partial_t\mathbf E.
$$

The first pair supplies divergence constraints; the second pair supplies evolution. “Vacuum form” does not mean that $\rho$ and $\mathbf J$ must vanish: explicit charges can be present. Singular point charges require distributional interpretation. Smooth-field calculations exclude their singular points.

In macroscopic matter, one may instead use $\nabla\cdot\mathbf D=\rho_{\rm free}$ and $\nabla\times\mathbf H=\mathbf J_{\rm free}+\partial_t\mathbf D$, together with the unchanged Faraday and magnetic-divergence equations. Constitutive relations are additional physics. Constant scalar $\epsilon,\mu$ do not describe arbitrary anisotropic, dispersive, nonlinear, or lossy materials. Do not mix free current with the microscopic $\mathbf E,\mathbf B$ equations while dropping bound sources.

For fixed surfaces, the divergence and Stokes theorems convert the equations into charge/flux and circulation statements. Moving circuits require the extra care in [[Faradays Law]]. See the canonical equation summary in [OpenStax, §16.1](https://openstax.org/books/university-physics-volume-2/pages/16-1-maxwells-equations-and-electromagnetic-waves).

## 2. Why the displacement-current term matters

Take the divergence of the last equation. Since a curl has zero divergence,

$$
0=\mu_0\nabla\cdot\mathbf J+
\mu_0\epsilon_0\partial_t(\nabla\cdot\mathbf E)
=\mu_0(\nabla\cdot\mathbf J+\partial_t\rho).
$$

Thus local charge conservation follows:

$$
\partial_t\rho+\nabla\cdot\mathbf J=0.
$$

Without displacement current, Ampère's magnetostatic equation would impose $\nabla\cdot\mathbf J=0$, forbidding local charge accumulation. The term repairs that inconsistency. Charge conservation alone does **not** uniquely derive all of Maxwell's theory; additional divergence-free terms would escape this consistency test. The physical equations require empirical justification. [Feynman Lectures II, §18–1](https://www.feynmanlectures.caltech.edu/II_18.html).

Conversely, evolve the curl equations with a charge-conserving source. Then $\partial_t(\nabla\cdot\mathbf B)=0$ and $\partial_t(\nabla\cdot\mathbf E-\rho/\epsilon_0)=0$. Correct initial constraints remain correct. An evolution algorithm that violates discrete charge conservation can generate spurious longitudinal fields even if its wave plots look plausible.

## 3. Worked example: a charging capacitor

Consider circular parallel plates of radius $a=0.020$ m, gap $d=0.001$ m, and charging current $I=0.010$ A. Work near the central gap, neglect fringing, and assume changes are slow compared with the light-crossing time $a/c$. This is a quasistatic approximation, not the exact radiating solution for finite plates.

With $A=\pi a^2$, Gauss's law gives $E\simeq Q/(\epsilon_0A)$ and hence

$$
\dot E=\frac{I}{\epsilon_0\pi a^2}
\simeq8.99\times10^{11}\ \mathrm{V\,m^{-1}\,s^{-1}}.
$$

A circular Ampèrian loop of radius $r<a$ in the gap encloses no conduction current but has changing electric flux. Therefore

$$
2\pi rB_\phi=\mu_0\epsilon_0\pi r^2\dot E,
\qquad B_\phi=\frac{\mu_0Ir}{2\pi a^2}.
$$

At $r=0.010$ m, $B_\phi\simeq5.00\times10^{-8}$ T, or 50.0 nT. Across the entire plate area, $I_d=\epsilon_0A\dot E=I$. Displacement current is a field-rate contribution with units of current, not evidence that charge carriers cross the vacuum gap.

Checks: the near-axis field vanishes linearly with $r$; reversing charging reverses circulation; $I=0$ gives no charging-induced magnetic field. The capacitor mechanism and surface-consistency argument are discussed in [Feynman II, §18–2](https://www.feynmanlectures.caltech.edu/II_18.html). The numerical parameters here are a local worked example.

## 4. From the same equations to waves

In a source-free vacuum region, curl Faraday's equation and substitute Ampère–Maxwell:

$$
\nabla(\nabla\cdot\mathbf E)-\nabla^2\mathbf E
=-\mu_0\epsilon_0\partial_t^2\mathbf E.
$$

Because $\nabla\cdot\mathbf E=0$ there,

$$
\left(\nabla^2-c^{-2}\partial_t^2\right)\mathbf E=0,
\qquad c^{-2}=\mu_0\epsilon_0,
$$

and similarly for $\mathbf B$. Solutions of the vector wave equation must still satisfy the Maxwell constraints and the correct relationship between $\mathbf E$ and $\mathbf B$. Choosing arbitrary independent wave solutions for the two fields does not suffice. Continue with [[Electromagnetic Waves]] and [[Poynting Theorem]].

## 5. Boundaries and unfinished work

Maxwell's equations need initial/boundary conditions and sources. If sources respond to the fields, their dynamics and constitutive behavior must be supplied too. The force on a test charge is the additional Lorentz law $q(\mathbf E+\mathbf v\times\mathbf B)$. Quantum photon statistics and nonlinear quantum-vacuum corrections lie beyond this classical linear vacuum theory.

Reconstruct the divergence calculation without notes. Then explain why a charging capacitor cannot be treated as a steady current everywhere. The [[Electromagnetism — Fields Energy and Gauge Study Route]] adds exercises and targeted numerical checks; those do not constitute a complete electromagnetism or experimental audit.

[[Physics Worldmap]] · [[Electromagnetism Map]] · [[Gausss Law]] · [[Faradays Law]] · [[Gauge Transformations]] · [[Inductance|← previous]] · [[Electromagnetic Waves|next →]]
