---
type: research-derivation
field: Statistical Physics
epistemic_status: effective
level: advanced
tags: [linear-response, camera-exposure, motion-blur, uncertainty-quantification, calibration, spectral-measures]
created: 2026-09-16
updated: 2026-09-16
note_maturity: expanded
source_audit: derived-with-primary-prior-art-and-independent-mathematical-review
---

# Camera Exposure and Finite-Time Response Bounds

A camera measures a time-averaged position, not an instantaneous position or an instantaneous velocity. Correcting localization noise alone does not remove the resulting motion blur. This note derives conservative finite-time response bounds for an explicitly specified shutter and a separately calibrated noise channel.

[[Benchmark 013 — Camera Exposure and Response Uncertainty]] tests these ideas on synthetic thermal models. [[Benchmark 012 — Acceleration Information and Certified Displacement]] supplies the preceding sampling ambiguity. [[Prior Art — Spectral Bounds and Physical Response]] records the broader research context.

The camera observation model and the importance of static localization error, dynamic exposure error, and calibration matching are established prior art. Savin and Doyle analyze those errors in particle-tracking microrheology; Berglund develops a statistical camera-tracking treatment including exposure and localization noise. [Savin and Doyle, 2005](https://doi.org/10.1529/biophysj.104.042457); [Berglund, 2010](https://doi.org/10.1103/PhysRevE.82.011917)

The inequalities below are derived explicitly here. They are not attributed as theorems of those papers. A checked derivation is not a claim of historical originality; novelty remains unestablished.

## 1. Target, assumptions, and camera operator

Initially use dimensionless units with stationary, zero-mean velocity variance equal to one. Assume mean-square integrable velocity and a nonnegative spectral probability measure:

$$
C(t)=\mathbb E[V(t)V(0)]
=\int_0^\infty\cos(\omega t)\,\rho(d\omega),
\qquad \rho\ge0,\quad\int\rho=1.
$$

No acceleration variance, frequency cutoff, or particular memory-kernel family is required. Gaussianity is unnecessary for the deterministic bounds, but is required for the exact chi-square confidence construction in Section 5.

Define displacement and half its variance by

$$
D_T=X(T)-X(0)=\int_0^T V(s)\,ds,
\qquad J(T)=\frac12\operatorname{Var}D_T
=\int_0^\infty g_T(\omega)\,\rho(d\omega),
$$

$$
g_T(\omega)=\frac{1-\cos(\omega T)}{\omega^2},
\qquad g_T(0)=T^2/2.
$$

Position itself need not be stationary. One may anchor it at an arbitrary initial position; that common anchor cancels from all differences below.

For rectangular exposure of duration $h>0$, use two forward position averages:

$$
\overline X_h(t)=\frac1h\int_t^{t+h}X(s)\,ds,
\qquad \overline D_{T,h}=\overline X_h(T)-\overline X_h(0)
=\frac1h\int_0^h [X(T+s)-X(s)]\,ds.
$$

Thus the record extends through $T+h$, even though the two exposure starts are separated by $T$. The noiseless camera functional is

$$
\overline J(T,h)=\frac12\operatorname{Var}\overline D_{T,h}
=\int_0^\infty g_T(\omega)
\operatorname{sinc}^2(\omega h/2)\,\rho(d\omega),
\qquad \operatorname{sinc}x=\frac{\sin x}{x}.
$$

This formula remains valid for $T<h$, when the two exposure windows overlap. Whether the corresponding localization errors are independent is a separate instrument question; overlap does not justify independence.

Under equilibrium fluctuation-dissipation and linear response, the unblurred $J$ also determines the response to a weak step force, with physical factors restored in Section 6. This connection needs physical equilibrium assumptions, not merely a stationary Gaussian covariance. [Kubo, 1957](https://doi.org/10.1143/JPSJ.12.570)

Importantly, $\overline J$ is **not** generally the ordinary camera mean response to a force switched on at time zero. If the unblurred mean step response is $J(t)$ in these units, the mean difference of forward camera exposures is

$$
\frac1h\int_0^h [J(T+s)-J(s)]\,ds,
$$

not $\overline J$. The present method uses an unforced camera variance to bound the underlying unblurred response.

## 2. Universal blur bound, with two proofs

For every $T,h>0$,

$$
0\le J(T)-\overline J(T,h)\le\frac{h^2}{6}.
$$

### Spectral proof

Put $x=\omega h/2$. Since $0\le\operatorname{sinc}^2x\le1$ and $g_T\ge0$, blur cannot increase this variance functional.

If $U$ and $W$ are independent uniform variables on $[-1,1]$, then

$$
1-\operatorname{sinc}^2x
=\mathbb E[1-\cos(x(U-W))]
\le\tfrac12x^2\mathbb E[(U-W)^2]
=x^2/3.
$$

Consequently, pointwise in frequency,

$$
g_T(\omega)[1-\operatorname{sinc}^2(\omega h/2)]
\le\frac{h^2}{12}[1-\cos(\omega T)]
\le\frac{h^2}{6}.
$$

Integration against the probability measure proves the assertion. The same proof gives $J-\overline J\le h^2[1-C(T)]/12$ if the unblurred lag correlation is independently available.

### Time-domain proof

Let $U_s=X(T+s)-X(s)$. Stationarity of velocity makes the variance of each $U_s$ equal to $2J(T)$. The variance identity for an average gives

$$
J-\overline J
=\frac{1}{4h^2}\int_0^h\int_0^h
\mathbb E[(U_s-U_t)^2]\,ds\,dt.
$$

For $s\ge t$,

$$
U_s-U_t=\int_t^s[V(T+u)-V(u)]\,du.
$$

The triangle inequality in $L^2$ and unit velocity variance imply
$\|U_s-U_t\|_2\le2|s-t|$. Therefore

$$
J-\overline J
\le\frac1{h^2}\int_0^h\int_0^h(s-t)^2\,ds\,dt
=h^2/6.
$$

Both proofs allow overlapping exposures. Neither assumes differentiable velocity.

### Sharpness and dependence on $T/h$

The constant $1/6$ cannot be reduced uniformly over all horizon-to-exposure ratios: take a spectral line with $\omega T=\pi$ and let $T/h\to\infty$. The blur loss divided by $h^2$ tends to $1/6$.

For a fixed ratio $r=T/h$, the sharp unconditional loss over this broad spectral class is instead

$$
B_*(T,h)=h^2\sup_{x\ge0}
\frac{[1-\cos(2rx)][1-\operatorname{sinc}^2x]}{4x^2}.
$$

Its value is attained by a maximizing spectral line when the maximum is positive. The simple universal envelope is
$B_*\le\min(h^2/6,T^2/2)$. A numerical frequency-grid maximum alone is not a certified upper bound on this supremum; any numerical replacement must also control between-grid and tail errors.

## 3. A sharp special case: exposure equals the horizon

When $T=h$, write $u=\operatorname{sinc}^2(\omega h/2)\in[0,1]$. Then

$$
J=\frac{h^2}{2}\mathbb E_\rho[u],
\qquad \overline J=\frac{h^2}{2}\mathbb E_\rho[u^2].
$$

The inequalities $u^2\le u$ and $(\mathbb Eu)^2\le\mathbb Eu^2$ give the exact conditional range

$$
\overline J\le J\le h\sqrt{\overline J/2}.
$$

This range is sharp for every $\overline J\in[0,h^2/2]$ over the stated stationary spectral class:

- For the upper endpoint, choose a single frequency with constant $u=\sqrt{2\overline J/h^2}$. Such a frequency exists because the first sinc lobe takes every value between zero and one.
- For the lower endpoint, mix a zero-frequency component ($u=1$) with a shutter-zero frequency ($u=0$), assigning probability $2\overline J/h^2$ to the first.

A spectral line has a stationary Gaussian realization $V(t)=A\cos\omega t+B\sin\omega t$ with independent unit-variance Gaussian $A,B$. Independent sums realize the mixtures. The zero-frequency component is a mean-zero random constant velocity. These are legitimate stationary Gaussian examples, but are not asserted to be stable dissipative free-GLE realizations or ergodic systems.

Also $u-u^2\le1/4$, so the sharp unconditional bound at $T=h$ is

$$
J-\overline J\le h^2/8.
$$

A single frequency with $\operatorname{sinc}^2(\omega h/2)=1/2$ attains it.

## 4. Conditional improvement for an integer horizon-to-exposure ratio

If $T/h=m$ is a positive integer, then $|\sin(mx)|\le m|\sin x|$. With $u=\operatorname{sinc}^2x$, this implies

$$
g_T(\omega)\le\frac{T^2}{2}u,
\qquad g_T(\omega)^2\le\frac{T^2}{2}g_T(\omega)u.
$$

Jensen's inequality therefore yields

$$
J(T)\le T\sqrt{\overline J(T,h)/2}.
$$

Given a confidence interval $[\overline J_L,\overline J_U]$, valid bounds on the same confidence event are

$$
\overline J_L\le J(T)\le
\min\!\left\{
\overline J_U+h^2/6,
T\sqrt{\overline J_U/2},
T^2/2\right\}.
$$

For $T=h$, replace $h^2/6$ by $h^2/8$, or use the sharper conditional formula directly. For $m>1$, the square-root inequality is valid but is not claimed to give the complete sharp conditional range.

The integer restriction matters. At $\omega=2\pi/h$, the shutter has a zero, so $\overline J=0$. If $T/h$ is not an integer, the same spectral line has

$$
J=\frac{h^2}{4\pi^2}[1-\cos(2\pi T/h)]>0.
$$

Thus the conditional square-root bound is false in general for noninteger $T/h$. The unconditional $h^2/6$ bound remains valid. The bound actually used in an experiment must be recorded in its protocol.

## 5. Calibrated pair noise, including bounded transfer error

An observed camera difference is

$$
Y=\overline D_{T,h}+\epsilon_T-\epsilon_0,
\qquad \operatorname{Var}Y=2\overline J+N_{\rm true},
$$

assuming additive signal-independent noise. The relevant noise power is the **pair-difference variance**

$$
N_{\rm true}=\operatorname{Var}(\epsilon_T-\epsilon_0)
=\sigma_T^2+\sigma_0^2-2\operatorname{Cov}(\epsilon_T,\epsilon_0).
$$

It equals twice a per-frame variance only under equal variances and independent endpoint errors. Adjacent differences from one sequence reuse localization errors and are correlated; summing such differences telescopes rather than accumulating independent frame-difference noise.

Suppose $M$ independent trajectory pairs supply centered Gaussian sample variance $s_Y^2$, and $L$ independent immobile calibration pairs supply centered Gaussian sample variance $s_N^2$. Unknown constant offsets are removed by centering, so the degrees of freedom are $M-1$ and $L-1$. For either channel, a two-sided variance interval with failure budget $\alpha$ is

$$
I(s^2,n,\alpha)=
\left[
\frac{(n-1)s^2}{\chi^2_{n-1,1-\alpha/2}},
\frac{(n-1)s^2}{\chi^2_{n-1,\alpha/2}}
\right].
$$

Write the observation interval as $[A,B]$ and the calibration-noise interval as $[C,D]$. Allow a guaranteed variance-transfer envelope

$$
(1-\delta)N_{\rm cal}\le N_{\rm true}\le(1+\delta)N_{\rm cal},
\qquad0\le\delta<1.
$$

On the two-channel confidence event,

$$
2\overline J\in
\left[
\max\{0,A-(1+\delta)D\},
B-(1-\delta)C
\right]\cap[0,T^2].
$$

If this intersection is empty, report incompatible constraints and withhold an interval. In particular, do not silently turn a negative upper endpoint into a claim of exactly zero signal. Under the assumptions, incompatibility can occur only outside the common confidence event.

Divide the compatible endpoints by two to obtain $[\overline J_L,\overline J_U]$. For arbitrary $T/h$, the universal response interval is

$$
\left[
\overline J_L,
\min\{T^2/2,\overline J_U+h^2/6\}
\right].
$$

The common event has probability at least $1-\alpha_Y-\alpha_N$ by the union bound. Independence between the two confidence events is not needed for that step; the declared independent Gaussian observations within each sample are needed for its chi-square law. A probabilistic rather than guaranteed transfer envelope needs its own failure budget.

The parameter $\delta$ must bound the actual change of pair-noise variance; it is not inferred merely by writing a wider formula. Changes in illumination, focus, signal-dependent localization, camera settings, shutter timing, or error correlation may violate it. Static calibration under different noise-to-signal conditions is not automatically transportable to moving particles. This instrument-matching issue is already central to the particle-tracking error literature. [Savin and Doyle, 2005](https://doi.org/10.1529/biophysj.104.042457)

Coverage here is for a prechosen horizon and acquisition condition. Trying many exposures and publishing the narrowest interval needs a simultaneous guarantee or an independent selection/validation design.

## 6. Physical units and practical limits

For physical velocity covariance $C_v$ with known $C_v(0)=c$, let $J=\tfrac12\operatorname{Var}D_T$ retain physical units of length squared. Then

$$
0\le J-\overline J\le c h^2/6,
\qquad J\le cT^2/2.
$$

For integer $T/h$, the conditional upper bound becomes $J\le T\sqrt{c\overline J/2}$; the special-case loss is $ch^2/8$. A valid known upper bound $c\le C_U$ can replace $c$ conservatively. The physical scalar step susceptibility is $\beta J$ under the equilibrium classical linear-response assumptions, where $\beta=1/(k_BT_{\rm bath})$. For a particle of mass $m$ with equipartition, $c=k_BT_{\rm bath}/m$.

These statements do **not** establish that a normal camera can resolve inertial Brownian motion. In the elementary inertial Langevin model, $C_v(t)=c e^{-|t|/\tau_m}$ and

$$
J(T)=c\left[\tau_m T-\tau_m^2(1-e^{-T/\tau_m})\right].
$$

At $T\gg\tau_m$, $J\simeq c\tau_m T$, so the worst-case relative blur allowance is approximately

$$
\frac{ch^2/6}{J(T)}\simeq\frac{h^2}{6\tau_m T}.
$$

That allowance can be enormous when exposure is long compared with the inertial relaxation time. A formally valid absolute bound may therefore be scientifically uninformative. This is an experimental-feasibility constraint, not something improved by increasing the number of repeated images alone.

Ideal overdamped Brownian position has no finite instantaneous velocity variance and lies outside the theorem. Its familiar rectangular-exposure result, for $T\ge h$, is $\overline J=D(T-h/3)$ rather than $J=DT$; it is a separate limiting model, not a counterexample to the finite-velocity bound. The distinction between camera artifacts and physical dynamics is treated in [Berglund, 2010](https://doi.org/10.1103/PhysRevE.82.011917).

Finally, the bounds apply to the measured finite horizon. They do not identify a memory kernel, determine an infinite-time diffusion exponent, validate an instrument, or predict beyond the record. Unknown shutter shape and timing, unbounded noise transfer, non-Gaussian sampling, dependent particles, and unknown equilibrium conditions require additional analysis.

## Primary sources and derivation status

- Thierry Savin and Patrick S. Doyle, *Static and Dynamic Errors in Particle Tracking Microrheology*, Biophysical Journal **88**, 623–638 (2005). [DOI](https://doi.org/10.1529/biophysj.104.042457) · [Author-hosted paper](https://web.mit.edu/doylegroup/pubs/BiophysJ-Savin05.pdf).
- Andrew J. Berglund, *Statistics of camera-based single-particle tracking*, Physical Review E **82**, 011917 (2010). [DOI](https://doi.org/10.1103/PhysRevE.82.011917) · [NIST-hosted paper](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=905460).
- Ryogo Kubo, *Statistical-Mechanical Theory of Irreversible Processes. I. General Theory and Simple Applications to Magnetic and Conduction Problems*, Journal of the Physical Society of Japan **12**, 570–586 (1957). [DOI](https://doi.org/10.1143/JPSJ.12.570).

These sources establish the surrounding measurement and response framework. The elementary inequalities and attainability constructions above are shown in full so they can be checked without relying on an originality claim or an unspecified theorem citation.

[[Benchmark 013 — Camera Exposure and Response Uncertainty]] · [[Benchmark 012 — Acceleration Information and Certified Displacement]] · [[Prior Art — Spectral Bounds and Physical Response]] · [[Synthesis Lab]] · [[Physics Worldmap]]
