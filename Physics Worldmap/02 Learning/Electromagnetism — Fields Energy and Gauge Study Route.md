---
type: learning
field: Electromagnetism
epistemic_status: reference
level: intermediate
tags: [learning, electromagnetism, derivations, conservation, gauge, verification]
created: 2026-09-17
updated: 2026-09-17
---

# Electromagnetism — Fields Energy and Gauge Study Route

This route develops a coherent chain: sources constrain fields; changing fields propagate; fields transfer energy; different potentials can represent the same physics. Its purpose is reconstructible understanding, not recognition of familiar formulas.

Prerequisites: [[Vector Calculus]], basic differential equations, [[Electric Field]], [[Magnetic Field and Lorentz Force]], and work/energy in [[Classical Mechanics Map]]. Start with [[Mechanics to Statistical Physics — Foundation Study Route]] if variational mechanics or control-dependent energy derivatives are unfamiliar.

## Read, reconstruct, challenge

| Step | Expanded note | Reconstruct without copying | Boundary to remember |
|---|---|---|---|
| 1 | [[Gausss Law|Gauss's law]] | Enclosed charge, flux, and interface pillbox | Zero net flux is not zero field |
| 2 | [[Faradays Law|Faraday's law]] | Fixed-loop circulation and moving-loop emf | Loop motion and changing fields are different contributions |
| 3 | [[Maxwell Equations]] | Charge continuity and the vacuum wave equation | Evolution requires compatible divergence constraints |
| 4 | [[Electromagnetic Waves]] | Transverse fields, relative amplitudes, intensity | Near fields and material waves need different assumptions |
| 5 | [[Poynting Theorem]] | Local balance and power entering a resistor | Material energy cannot always be written as a simple quadratic |
| 6 | [[Gauge Transformations]] | Field invariance and a total Lagrangian derivative | Local gauge freedom does not erase global topology |

Each note includes SI conventions, a worked example, limitations, and checked canonical references. These are six expanded concept notes, not a complete electromagnetism textbook or a claim-by-claim certification of every sentence.

## Six reconstruction exercises

These are locally designed practice problems with hidden solutions, not an independently administered mastery test. Write the assumptions, derivation, dimensions, and limiting behavior before opening the check. Numerical agreement alone is insufficient.

### 1. Gauss's law without a uniform density

An isolated insulating ball of radius $R$ has total positive charge $Q$ and prescribed total density $\rho(r)=ar^2$ for $r<R$, zero outside. Find $a$ and both branches of $E_r(r)$. Does the field jump at the surface? For $Q=4.00$ nC, $R=0.200$ m, find the field at $r=0.100$ m.

<details>
<summary>Derivation check</summary>

Integrating $4\pi ar^4$ gives $Q=4\pi aR^5/5$, so $a=5Q/(4\pi R^5)$ and $Q_{\rm enc}(r)=Q(r/R)^5$. Thus $E_r=k_eQr^3/R^5$ inside and $k_eQ/r^2$ outside. Both give $k_eQ/R^2$ at the boundary; the finite density jump does not create a delta-function surface charge. The requested field is about $112.34$ V m$^{-1}$, outward. Units of $a$ are C m$^{-5}$. This is a specified charge distribution, not a conducting ball in equilibrium.

</details>

### 2. A magnetic field when the capacitor is momentarily uncharged

In the quasistatic, negligible-fringing circular-capacitor model, impose $I(t)=I_0\cos\Omega t$ and choose $Q(0)=0$. Find the electric field in the gap and the magnetic field for a concentric loop $r<a$. Can one be zero while the other is maximal?

<details>
<summary>Derivation check</summary>

$Q(t)=(I_0/\Omega)\sin\Omega t$ and $E(t)=I_0\sin\Omega t/(\Omega\epsilon_0\pi a^2)$. Ampère–Maxwell gives $B_\phi(r,t)=\mu_0I_0r\cos\Omega t/(2\pi a^2)$. At $t=0$, $E=0$ but its time derivative and the induced magnetic field are maximal. At a maximum of $E$, charging current and this magnetic contribution vanish. This is consistent because the source is $\dot E$, not $E$. Require $\Omega a/c\ll1$ and a sufficiently small gap; it is not the exact high-frequency finite-plate solution.

</details>

### 3. A decreasing field does not mean an opposing field

A stationary 75-turn coil has area $0.00200$ m$^2$ per turn and resistance $3.00\ \Omega$. Neglect its self-inductance and backreaction. A uniform external field perpendicular to each turn is $B(t)=0.300e^{-t/(0.400\,\mathrm s)}$ T along the positive surface normal. Find the signed emf, current, and heating at $t=0$. Which way is the induced magnetic field?

<details>
<summary>Derivation check</summary>

$\dot B(0)=-0.750$ T s$^{-1}$. Therefore $\mathcal E(0)=-NA\dot B=+0.1125$ V, $I=+0.0375$ A in the positive right-hand loop direction, and $I^2R=0.00421875$ W. Its magnetic effect points along the original positive field, opposing the decrease rather than opposing the field itself. The imposed field source participates in the energy balance; this is not energy created from nothing.

</details>

### 4. The magnetic part of a traveling wave

In source-free vacuum, take $\mathbf E=E_0\cos(kz-\omega t)\hat{\mathbf x}$ with $\omega=ck>0$. Derive $\mathbf B$ and the time-averaged intensity. What fails if the magnetic field is assigned the opposite sign while keeping the same electric wave?

<details>
<summary>Derivation check</summary>

$\mathbf B=(E_0/c)\cos(kz-\omega t)\hat{\mathbf y}$ satisfies both curl equations. The Poynting vector points along $+z$ and $\langle S\rangle=\epsilon_0cE_0^2/2$. Reversing only $\mathbf B$ violates Faraday's and Ampère–Maxwell's equations; it is not simply the same wave carrying energy backward. A true backward wave requires the changed space-time phase relation as well. For $E_0=6.00$ V m$^{-1}$, the intensity is approximately $0.0478$ W m$^{-2}$.

</details>

### 5. Why fixed voltage needs battery accounting

A vacuum parallel-plate capacitor has area $A=0.0100$ m$^2$, separation $d=0.00200$ m, and capacitance $C=\epsilon_0A/d$. With a battery maintaining $V=100$ V, find the force conjugate to increasing $d$. Explain why directly using $-\partial_d(CV^2/2)$ at fixed $V$ gives the wrong sign.

<details>
<summary>Derivation check</summary>

For the isolated fixed-charge capacitor, $U(Q,d)=Q^2/(2C)$ and $F_d=-\partial_dU|_Q=-Q^2/(2\epsilon_0A)$. With fixed voltage, charge flows to/from the battery, so field energy alone is not the correct controlled potential. Use

$$
\mathcal G(V,d)=U-VQ=-\frac12C(d)V^2,
\qquad F_d=-\partial_d\mathcal G\big|_V
=-\frac{\epsilon_0AV^2}{2d^2}.
$$

Numerically $F_d\simeq-1.11\times10^{-4}$ N, attractive. Differentiating $+CV^2/2$ at fixed voltage omits battery work and predicts an incorrect repulsion. The differential balance is $dU=V\,dQ-F_d\,dd$; eliminating $dQ$ produces $d\mathcal G=-Q\,dV-F_d\,dd$. Fringing, dielectric mechanics, and dynamic circuit effects are excluded.

</details>

### 6. A total derivative is not a new electric field

For a nonrelativistic particle of charge $q$, start from $L=m\dot{\mathbf r}^2/2+q\dot{\mathbf r}\cdot\mathbf A-q\phi$. Apply $\mathbf A'=\mathbf A+\nabla\chi$ and $\phi'=\phi-\partial_t\chi$. Find the change in $L$, in canonical momentum, and in kinetic momentum. State an assumption needed to interpret this as an innocuous local representation change.

<details>
<summary>Derivation check</summary>

$L'-L=q(\dot{\mathbf r}\cdot\nabla\chi+\partial_t\chi)=q\,d\chi/dt$. With fixed endpoints, the action variation is unchanged. Canonical momentum shifts by $q\nabla\chi$; kinetic momentum $\mathbf p-q\mathbf A=m\dot{\mathbf r}$ is unchanged. The field cancellation requires a sufficiently smooth, admissible gauge function on the domain. Singular or multivalued transformations require separate boundary/topological analysis. In quantum mechanics the state phase must also transform; changing only the potentials is not a complete gauge transformation.

</details>

## Targeted computational checks

The portable helper [[check_electromagnetism.py]] uses NumPy and SciPy and writes [[electromagnetism-checks.json]]. Run it from the vault root:

~~~powershell
python ".\95 Resources\Tools\check_electromagnetism.py"
~~~

Its 14 groups check dimensions and SI constants; a charged sphere against direct Coulomb integration; off-center flux; local charge continuity; capacitor displacement current; induction around a solenoid; moving-rod energy; resistor energy influx; plane and standing waves; two gauge examples; dielectric charge bookkeeping; and capacitor energy/force with fixed-control accounting. Some groups include deliberately wrong signs or models to ensure that the check can fail. This does not amount to an exhaustive proof of the notes or experimental validation. Source hashes identify exactly which note snapshots were checked.

## Cross-field connections that survive a derivation

The fixed-voltage exercise uses the same control-variable Legendre transformation found in thermodynamic potentials: changing which variable is externally fixed changes the energy function whose derivative gives the response. It is a concrete shared mathematical structure, not a claim that an electric circuit is identical to a thermodynamic ensemble.

The gauge exercise connects to [[Lagrangian Mechanics]]: adding a total derivative changes canonical coordinates while preserving the fixed-endpoint equations of motion. It also shows why “same physical fields” does not mean “same canonical momentum.”

Finally, the measurement work in [[Benchmark 013 — Camera Exposure and Response Uncertainty]] illustrates a related discipline: distinguish the physical quantity from its representation and from what an instrument actually measures. Gauge-related potentials are physically redundant descriptions; differently filtered sensor readings are different observables. Those are **not** the same kind of ambiguity.

## Evidence and next gaps

For experiments, connect [[Faraday Electromagnetic-Induction Experiments]] and [[Hertz Radio-Wave Experiments]] to the corresponding field predictions. Their apparatus, systematic-error budgets, and historical data need deeper expansion; a hyperlink does not complete experimental understanding.

Next foundations: electrostatic uniqueness and image methods; boundary matching and Fresnel coefficients; waveguides and transmission lines; retarded fields and radiation; covariant electrodynamics; and causal material response. The six notes here do not close those gaps. Canonical source pointers live beside the claims in the notes; derivations and practice problems are local reconstructions, not copied textbook exercises or evidence of permanent learning.

[[Electromagnetism Map]] · [[Learning Paths]] · [[Mechanics to Statistical Physics — Foundation Study Route]] · [[Physics Problem Bank]] · [[Release Status and Next Work]] · [[Physics Worldmap]]
