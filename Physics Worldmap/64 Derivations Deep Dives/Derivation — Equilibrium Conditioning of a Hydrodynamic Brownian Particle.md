---
title: "Derivation — Equilibrium Conditioning of a Hydrodynamic Brownian Particle"
type: derivation
field: "Statistical Physics"
epistemic_status: established
level: advanced
tags: [physics, derivation, deep-dive, brownian-motion, hydrodynamic-memory, basset, conditioning]
created: 2026-10-06
updated: 2026-10-06
note_maturity: worked-derivation
source_audit: canonical-derivation-needs-citation-audit
---

# Derivation — Equilibrium Conditioning of a Hydrodynamic Brownian Particle

> [!summary] Core result
> For a trapped sphere with Basset–Boussinesq memory in thermal equilibrium, the mean displacement conditioned on an initial velocity $v_0$ is $m\chi(t)v_0$. Here $\chi$ is the position response to an impulsive force, and $m$ includes half the displaced fluid mass.
>
> The naive initial-value problem, with the particle at $v_0$ and the fluid at rest, adds a term $z\,\mathcal L^{-1}[s^{-1/2}/P(s)]\,v_0$. That term does **not** describe the equilibrium ensemble. Position conditioning is identical in both formulations.

Used by [[Benchmark 014 — Preregistered Conditioned Brownian Reproduction]] and [[Benchmark 015 — Gain-Free Test of Hydrodynamic Memory]]. Background: [[Public Data Lead — Conditioned Hydrodynamic Brownian Motion]].

## 1. Model

A sphere of radius $a$ and density $\rho_p$ moves in an incompressible fluid with density $\rho_f$ and viscosity $\eta$, in a harmonic trap of stiffness $K$. It obeys

$$
m\ddot x=-\gamma\dot x-z\sqrt{\tfrac{1}{\pi}}\int_{-\infty}^{t}\frac{\ddot x(s)}{\sqrt{t-s}}\,ds-Kx+F_{\text{th}}(t),
$$

with the following coefficients:
- $m=m_p+\tfrac12 m_f$, the particle mass plus half the displaced fluid mass;
- $\gamma=6\pi\eta a$;
- $z=6\pi a^2\sqrt{\rho_f\eta}$.

The two time scales are $\tau_p=m/\gamma$ and $\tau_f=\rho_f a^2/\eta$, and $z^2/(m\gamma)=\tau_f/\tau_p$. The thermal force is coloured, with its correlation fixed by the fluctuation–dissipation theorem. Faxén corrections and fluid compressibility are neglected.

**Response function.** With Laplace variable $s$, a force impulse gives

$$
\hat\chi(s)=\frac{1}{P(s)},\qquad P(s)=ms^2+zs^{3/2}+\gamma s+K .
$$

## 2. Equilibrium covariance and Gaussian conditioning

**Covariances.** The classical fluctuation–dissipation theorem for a linear stationary system gives

$$
C_x(t)=\langle x(t)x(0)\rangle=k_BT\Big(\tfrac1K-\int_0^{|t|}\chi\Big),\qquad
\langle x(t)v(0)\rangle=-C_x'(t)=k_BT\,\chi(t),\qquad
C_v(t)=k_BT\,\dot\chi(t).
$$

Two checks: $C_x(0)=k_BT/K$ because $\int_0^\infty\chi=\hat\chi(0)=1/K$, and $C_v(0)=k_BT/m$ because $\dot\chi(0^+)=1/m$. Stationarity makes $x(0)$ and $v(0)$ uncorrelated.

**Conditioning.** The process is Gaussian, so conditioning on $(x_0,v_0)$ is exact linear regression:

$$
\mathbb E[x(t)\mid x_0,v_0]=K\Big(\int_t^\infty\chi\Big)x_0+m\chi(t)v_0,
$$

$$
\operatorname{Cov}[x(t_1),x(t_2)\mid x_0,v_0]
=k_BT\big[c(t_1)+c(t_2)-c(|t_1-t_2|)-m\chi(t_1)\chi(t_2)-Kc(t_1)c(t_2)\big],
$$

where $c(t)=\int_0^t\chi$. Conditioning on velocity alone, with $D=x(t)-x(0)$ and $x_0$ averaged over its equilibrium law, gives

$$
\mathbb E[D^2\mid v_0]=2k_BT\,c(t)-k_BT\,m\chi(t)^2+m^2\chi(t)^2v_0^2 .
$$

## 3. Why the initial-value problem differs

Suppose the history integral starts at $t=0$, with prescribed $x(0)=x_0$, $\dot x(0)=v_0$ and the fluid at rest. The Laplace transform of the Basset term is then $z(s^{3/2}\hat x-s^{1/2}x_0-s^{-1/2}v_0)$, so

$$
\hat x(s)=\frac{m(sx_0+v_0)+\gamma x_0+zs^{1/2}x_0+zs^{-1/2}v_0}{P(s)}.
$$

**The $x_0$ part agrees.** It equals $x_0(P-K)/(sP)=x_0[1/s-K/(sP)]$, whose inverse is $x_0K\int_t^\infty\chi$. That is exactly the equilibrium regression coefficient.

**The $v_0$ part does not.** It is $(m+zs^{-1/2})v_0/P$, while the equilibrium coefficient is $mv_0/P$. The extra $zs^{-1/2}v_0/P$ describes a particle that has moved at $v_0$ without the fluid having set up the matching vorticity. That state is not drawn from the equilibrium ensemble. An *impulsive* kick to a particle at rest in a quiescent fluid does give $m v_0/P$. This is the classical identity between the normalised velocity autocorrelation and impulsive relaxation, associated with Widom and with Hauge and Martin-Löf.

**Size of the difference** at the published parameters ($a=3.398$ µm, $K=7.80\times10^{-5}$ N/m, BaTiO₃ in acetone):

| $t$ | 1 µs | 5 µs | 20 µs | 50 µs |
|---|---:|---:|---:|---:|
| (IVP mean)/(equilibrium mean) | 1.111 | 1.253 | 1.530 | 1.894 |

## 4. Short-time expansion

**Expanding the response.** For $s\to\infty$, $1/P=1/(ms^2)-z/(m^2s^{5/2})+(z^2/m^3-\gamma/m^2)/s^3+\dots$. Hence

$$
C_v(t)=\frac{k_BT}{m}-\frac{2k_BTz}{m^2\sqrt\pi}t^{1/2}+k_BT\Big(\frac{z^2}{m^3}-\frac{\gamma}{m^2}\Big)t+O(t^{3/2}).
$$

**General formula.** For a velocity covariance of the form $C=c-at^{1/2}+b_1t$, the identity $\mathbb E[D^2\mid v_0=0]=2J-A^2/c$ (with $A$ and $J$ as defined in the public-data note) gives

$$
\mathbb E[D^2\mid v_0=0]=\frac45a\,t^{5/2}-\Big(\frac23b_1+\frac{4a^2}{9c}\Big)t^3+\dots
$$

**Result for the hydrodynamic sphere.** Substituting the coefficients above:

$$
\boxed{\mathbb E[D^2\mid v_0=0]=\frac{8k_BTz}{5\sqrt\pi\,m^2}t^{5/2}
+\frac23\frac{k_BT\gamma}{m^2}\Big[1-\Big(1+\frac{8}{3\pi}\Big)\frac{\tau_f}{\tau_p}\Big]t^3+O(t^{7/2}).}
$$

With $z=\gamma\sqrt{\tau_f}$, this coincides term by term with the authors' short-time form, and with the $\beta$ coefficient in their analysis code. Numerically, the two-term form matches the exact conditional moment to 0.02% at 10 ns, 0.2% at 100 ns and 1.9% at 1 µs.

## 5. Independent numerical verification

$\chi$, $\int\chi$ and $\mathcal L^{-1}[s^{-1/2}/P]$ were evaluated two ways:
- by Talbot numerical Laplace inversion at 30-digit precision;
- by the erfcx partial-fraction form over the roots of $u^4-(z/m)u^3+(\gamma/m)u^2+K/m$, with $u=-\sqrt s$.

They agree to at least 7 significant digits from 0.1 to 200 µs. The authors' analysis functions `b_inverse_form`, `c_inverse_form` and `s_minus_half_b_inverse_form` (read as text, re-implemented) equal $\chi$, $\int_0^t\chi$ and $-\mathcal L^{-1}[s^{-1/2}/P]$ respectively.

Consequence: their analytic conditional MSD, with the $v_0$ term commented out, **is** exact equilibrium Gaussian conditioning. Leaving the term out is correct, not an omission.

## 6. Assumptions and failure regimes

- **Incompressibility** fails below the sound-crossing time $a/c_s$, which is nanoseconds here.
- **Faxén and wall corrections** are neglected. The particle is assumed far from surfaces.
- **The trap is assumed harmonic.** The fluid is Newtonian with constant temperature.
- **The detector is not ideal.** Measured statistics need the bin-and-stencil operator (see [[Benchmark 015 — Gain-Free Test of Hydrodynamic Memory]]).

## Sources

- **Primary texts:**
  - Hauge and Martin-Löf, *J. Stat. Phys.* **7**, 259 (1973), on fluctuating hydrodynamics and Brownian motion;
  - Clercx and Schram, *Phys. Rev. A* **46**, 1942 (1992), on trapped-sphere hydrodynamic correlation functions and the partial-fraction form.
- **Data and analysis code:** Boynewicz, Thumann and Raizen, *Sci. Adv.* (2026), doi:10.1126/sciadv.aeb4579, and its Dryad notebooks.

> [!note] Documentation status
> These citations are from memory and were not re-opened in this session; they need a pinpoint audit under [[Source and Citation Policy]]. The mathematics above was re-derived and numerically checked independently of them.

[[Derivation Atlas]] · [[Statistical Physics Map]] · [[Synthesis Lab]]
