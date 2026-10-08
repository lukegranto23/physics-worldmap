---
type: "concept"
field: "Electromagnetism"
epistemic_status: "established"
level: "introductory"
tags: ["physics", "field/electromagnetism", "status/established", "level/introductory"]
aliases: ["Faraday's Law"]
created: 2026-07-30
updated: 2026-09-17
note_maturity: expanded
source_audit: derived-with-canonical-references-and-targeted-checks
---

# Faraday's Law

Changing magnetic fields make electric fields circulate. A moving conductor can also develop an electromotive force in a static magnetic field. The compact flux rule combines these mechanisms; keeping them separate prevents sign mistakes and false energy arguments.

## 1. A fixed loop and its orientation

For a fixed closed curve $C$ bounding a fixed surface $S$, choose the curve orientation by the right-hand rule relative to $d\mathbf A$. Define $\Phi_B=\int_S\mathbf B\cdot d\mathbf A$. In SI,

$$
\oint_C\mathbf E\cdot d\boldsymbol\ell
=-\frac{d\Phi_B}{dt},\qquad
\nabla\times\mathbf E=-\partial_t\mathbf B.
$$

Stokes's theorem converts the two forms into one another for smooth fields. Magnetic flux is in webers and Wb s$^{-1}$ is a volt. The flux uses the **open** spanning surface, not a closed Gaussian surface. Different spanning surfaces give the same flux when $\nabla\cdot\mathbf B=0$ and the field is regular over the enclosed volume.

The loop may be a mathematical curve with no wire. The induced field exists regardless of whether charges are available to make a current. When a conducting path is present, its resistance, inductance, geometry, and other sources determine the current; the induction law alone does not give $I$. See [OpenStax §13.1](https://openstax.org/books/university-physics-volume-2/pages/13-1-faradays-law) for the flux convention.

## 2. Worked field example: a long solenoid

Approximate a long solenoid by a uniform axial field $B_z(t)$ for $r<a$ and negligible external magnetic field. Assume axial symmetry, neglect end effects and rapid-propagation corrections. Let $a=0.030$ m and $\dot B_z=+0.200$ T s$^{-1}$. The positive loop direction is counterclockwise as viewed from $+z$.

The enclosed flux is $\pi r^2B_z$ inside and $\pi a^2B_z$ outside. Therefore

$$
E_\phi(r)=
\begin{cases}
-r\dot B_z/2,&r<a,\\
-a^2\dot B_z/(2r),&r>a.
\end{cases}
$$

At $r=0.010$ m, $E_\phi=-0.00100$ V m$^{-1}$. At $r=0.060$ m, $E_\phi=-0.00150$ V m$^{-1}$. Both point clockwise. At the outer loop, the signed emf is

$$
\mathcal E=2\pi rE_\phi=-\pi a^2\dot B_z
\simeq-5.65\times10^{-4}\ \mathrm V.
$$

The external electric field is not zero merely because the local changing magnetic field is negligible there. Its curl vanishes locally outside, yet its circulation around a loop linking the solenoid is nonzero. That exterior domain is multiply connected: no single-valued scalar potential accounts for this entire induced field. This distinction connects induction to the domain assumptions in [[Gauge Transformations]].

The inside expression is regular at the axis; the two expressions agree at $r=a$. A numerical curl check should be performed away from the idealized interface rather than differentiating a discontinuous model indiscriminately.

## 3. Moving boundaries: which velocity enters?

For a smooth material loop with local boundary velocity $\mathbf u$, the geometric transport identity is

$$
\frac{d}{dt}\int_{S(t)}\mathbf B\cdot d\mathbf A
=\int_{S(t)}\partial_t\mathbf B\cdot d\mathbf A
-\oint_{C(t)}(\mathbf u\times\mathbf B)\cdot d\boldsymbol\ell.
$$

Combining it with Faraday's field equation yields

$$
\oint_{C(t)}(\mathbf E+\mathbf u\times\mathbf B)\cdot d\boldsymbol\ell
=-\frac{d\Phi_B}{dt}.
$$

The left side includes motional emf from the Lorentz force. $\mathbf u$ is the motion of the circuit element, not an arbitrary velocity assigned to the drawn surface. For a thin wire, an additional carrier drift parallel to the wire contributes no tangential magnetic-force term. Sliding contacts and changing electrical connections require tracking the actual conducting path; blindly differentiating a convenient geometric flux can fail. [Feynman Lectures II, §§17–1–17–2](https://www.feynmanlectures.caltech.edu/II_17.html) explicitly distinguishes the two mechanisms and discusses flux-rule cautions.

## 4. Worked energy check: a sliding rod

A rod of length $\ell=0.250$ m slides at $u=3.00$ m s$^{-1}$ on rails in a uniform perpendicular field $B=0.400$ T. The closed circuit has resistance $R=2.00\ \Omega$. Ignore self-inductance, rail resistance already included in $R$, and mechanical friction; take the steady resistive response.

The emf magnitude is $Bu\ell=0.300$ V, giving $I=0.150$ A. The magnetic force on the rod has magnitude $I\ell B=0.0150$ N and opposes the imposed motion. Thus

$$
P_{\rm mechanical}=Fu=0.0450\ \mathrm W
=I^2R=P_{\rm heat}.
$$

This equality checks the Lenz-law sign. If the force reinforced the motion in this passive model, the energy balance would be wrong. A magnetic Lorentz force does no work on an individual charge at its total velocity; the moving apparatus's mechanical work, electric forces, and dissipative interactions account for the circuit's energy transfer. “The static magnetic field supplies the heat” is not the correct accounting. Continue with [[Poynting Theorem]].

## 5. What the minus sign does and does not say

The induced current's magnetic effect opposes the **change** in linked flux, not necessarily the applied field itself. Decreasing a positive flux can induce a field in the same direction as the original field. Reversing the chosen loop orientation reverses both the signed emf and flux without changing the physical prediction.

In time-dependent induction, an electrostatic scalar voltage difference need not represent a path-independent line integral. A meter and its leads form part of a measuring loop; lead routing can matter. A transformer with $N$ turns uses flux linkage $\sum_i\Phi_i$, reducing to $N\Phi$ only when the same flux links each turn.

## Reconstruction and evidence

Re-derive the exterior-solenoid result without assuming that electric fields require nearby magnetic fields. Then calculate how the sliding-rod power changes if its speed doubles, holding $B,\ell,R$ fixed. The ideal model predicts four times the heating, with the external drive supplying it.

These are established classical predictions with explicitly idealized examples, not new discoveries. [[Faraday Electromagnetic-Induction Experiments]] provides the experiment connection. The [[Electromagnetism — Fields Energy and Gauge Study Route]] supplies independent exercises and scoped calculation checks.

[[Physics Worldmap]] · [[Electromagnetism Map]] · [[Magnetic Materials|← previous]] · [[Inductance|next →]] · [[Maxwell Equations]]
