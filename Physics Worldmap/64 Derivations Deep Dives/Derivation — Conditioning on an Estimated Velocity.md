---
title: "Derivation — Conditioning on an Estimated Velocity"
type: derivation
field: "Statistical Physics"
epistemic_status: effective
level: advanced
tags: [physics, derivation, conditioning, measurement-operator, brownian-motion, hydrodynamic-memory, experimental-design]
created: 2026-10-08
updated: 2026-10-08
note_maturity: worked-derivation
source_audit: limited-prior-art-screen-no-direct-match
---

# Derivation — Conditioning on an Estimated Velocity

> [!summary] Result
> A velocity-conditioned MSD is never measured with the instantaneous velocity. Selection uses a stencil applied to binned positions. Suppose the velocity covariance has a short-time cusp, $C_v(\tau)=c-a|\tau|^\alpha$ with $0<\alpha\le1$. Then the measured zero-velocity conditioned MSD is a sum of three terms with different exponents:
>
> $$M(t_k)\simeq\underbrace{a\,\Delta^{\alpha+2}\,\Phi_\alpha(k)}_{\text{distorted cusp}}+\underbrace{\tfrac{\varepsilon}{1+\varepsilon}\,\tfrac{r_k^2}{s}}_{\approx\,\varepsilon c t_k^2\text{: ballistic leak}}+\underbrace{2\sigma^2}_{\text{noise floor}}+\dots$$
>
> Here $t_k=k\Delta$, $\Delta$ is the bin width, $\varepsilon$ is the noise share of the velocity estimate's variance, and $\sigma^2$ is the white position noise. $\Phi_\alpha$ is a universal function of the lag in bins: it depends only on $\alpha$ and the stencil. The true law $t^{\alpha+2}$ appears only when the cusp term dominates and $k$ is large. Softer cusps, meaning stronger memory, take longest to recover.

Developed from [[Benchmark 017 — Processing Dependence of the Conditioned Super-Ballistic Signal]]. Code: lab 46, `46_estimated_velocity_conditioning_theory.py`, with outputs and the figure `universal_operator_curves.png` in `results/estimated_velocity_theory/`.

## 1. Setup

- **Process.** $x(t)$ is stationary and Gaussian, with velocity covariance $C_v(\tau)=c-a|\tau|^\alpha+o(|\tau|^\alpha)$. Hydrodynamic (Basset) memory gives $\alpha=\tfrac12$. Ordinary Langevin dynamics gives $\alpha=1$.
- **Measurement.**
  - Positions are bin averages $Y_n=\Delta^{-1}\int_{n\Delta}^{(n+1)\Delta}x$.
  - The velocity estimate is $W=\Delta^{-1}\sum_l d_lY_{n+l}$, using a central stencil with $\sum_l d_l=0$ and $\sum_l l\,d_l=1$, so it is exact for linear motion.
  - Selection is on $W\approx0$. The displacement is $D_k=Y_k-Y_0$.
- **Gaussian conditioning.** The conditioned MSD is $u_k-r_k^2/s$, with $u_k=\operatorname{Var}D_k$, $r_k=\operatorname{Cov}(D_k,W)$ and $s=\operatorname{Var}W$.

## 2. The cusp term is universal

Expand to first order in $a$. The constant part $c$ of $C_v$ corresponds to ballistic motion, $x=v_0t$. For that motion $D_k=v_0k\Delta$ and $W=v_0$ exactly, so the ballistic contributions cancel:

$$u-\frac{r^2}{s}\;\xrightarrow{\;c\text{ only}\;}\;c\,t_k^2-\frac{(c\,t_k)^2}{c}=0 .$$

What remains, to first order in $a$, is the variance of the residual functional

$$L_k=Y_k-Y_0-k\sum_l d_lY_l ,$$

which annihilates constant and linear motion. It is evaluated with the generalised position covariance belonging to $-a|\tau|^\alpha$:

$$\gamma(\tau)=\frac{a\,|\tau|^{\alpha+2}}{(\alpha+1)(\alpha+2)},\qquad -\gamma''=-a|\tau|^\alpha .$$

Bin-averaging $\gamma$ and scaling out $\Delta$ give $M_\text{cusp}=a\Delta^{\alpha+2}\Phi_\alpha(k)$. Here $\Phi_\alpha$ depends only on $\alpha$, the stencil and $k$, not on any other physics.

In the continuum limit $\Phi_\alpha\to2k^{\alpha+2}/(\alpha+2)$. This recovers the known instantaneous result $E[D^2\mid v_0=0]=2a\,t^{\alpha+2}/(\alpha+2)$; for $\alpha=\tfrac12$ that is $\tfrac45at^{5/2}$.

## 3. The ballistic leak from a noisy velocity estimate

Add independent white position noise $\sigma^2$. It increases $s$ by $\sigma_W^2=\sigma^2\sum d_l^2/\Delta^2$. For $k$ beyond the stencil reach, $r_k$ is unchanged. Exactly,

$$\Delta M=2\sigma^2+\frac{r_k^2}{s}-\frac{r_k^2}{s+\sigma_W^2}=2\sigma^2+\frac{\varepsilon}{1+\varepsilon}\,\frac{r_k^2}{s},\qquad\varepsilon=\frac{\sigma_W^2}{s}.$$

At short times $r_k^2/s\approx c\,t_k^2$. Noise in the selection variable therefore leaks a fraction $\varepsilon/(1+\varepsilon)$ of the ballistic $t^2$ term back into a curve that should have cancelled it. That leak flattens the apparent exponent.

## 4. Numbers (lab 46)

**Operator suppression of the cusp term**, $\Phi_\alpha(k)$ divided by its continuum limit:

| | $k=1$ | $k=4$ | $k=16$ | apparent exponent at $k=1$ | $k_{\min}$, within 0.1 / 0.05 of $\alpha+2$ |
|---|---:|---:|---:|---:|---|
| $\alpha=\tfrac12$, order 8 | 0.24 | 0.62 | 0.82 | 3.41 (true 2.5) | 23 / 71 bins |
| $\alpha=\tfrac12$, order 2 | 0.21 | 0.51 | 0.76 | 3.21 | 40 / 126 bins |
| $\alpha=1$, order 8 | 0.46 | 0.85 | 0.96 | 3.59 (true 3) | 7 / 13 bins |
| $\alpha=\tfrac14$, order 8 | 0.13 | 0.39 | 0.58 | 3.32 (true 2.25) | 82 / — bins |

The full table (four values of $\alpha$, three stencils) is in `results.json`.

**Checks.**
1. **Continuum limit.** $\Phi$ approaches it slowly, reaching 0.983 at $k=2000$ for $\alpha=\tfrac12$.
2. **Against the full published-Basset forward model.** The first-order theory agrees within 1–5% up to about 3 µs. It deviates by +14% at 4.5 µs and more beyond, as higher-order hydrodynamic terms take over near $\tau_f\approx28$ µs.
3. **The leak formula** matches the exact Gaussian expression to machine precision. Its ballistic form $\varepsilon c t^2$ is accurate only at the first lags: 5% error at $k=1$, 36% at $k=4$.

**Applied to the Dryad experiment** (750 ns bins, order 8, $\varepsilon\approx0.06$): the ballistic leak divided by the cusp term is 1.8, 0.66, 0.31, 0.17 and 0.09 at 0.75, 1.5, 3, 6 and 12 µs.

## 5. Experimental-design criterion

A clean $t^{\alpha+2}$ needs all of the following:

1. **Operator:** $t\gtrsim k_{\min}\Delta$. For hydrodynamic memory with an eighth-order stencil this is about 23Δ for ±0.1 in the exponent, and about 71Δ for ±0.05.
2. **Velocity noise:** $\varepsilon c\,t^2\ll a\,t^{\alpha+2}$, that is $t\gg(\varepsilon c/a)^{1/\alpha}$.
3. **Position noise:** $2\sigma^2\ll a\,t^{\alpha+2}$.
4. **Physics:** $t$ well below the time at which higher-order terms enter. For Basset that is $\min(\tau_f,\tau_p)$.

For the published experiment, criterion 1 requires $t\gtrsim17$ µs, while criterion 4 requires $t\ll28$ µs. There is effectively **no clean scaling window**. The visible 5/2 slope is a blend of terms with exponents above and below 5/2.

**General lesson.** The softer the cusp (smaller $\alpha$, stronger memory), the slower the estimator distortion decays. So the systems where conditioning is most interesting are the ones where it is most fragile.

**Remedies:**
- Forward-model the operator and the noise, as in Benchmark 017.
- Use a gain-free regression observable, as in [[Benchmark 015 — Gain-Free Test of Hydrodynamic Memory]].
- Raise the sampling rate so that $k_{\min}\Delta\ll\tau_f$.
- Condition on an independent velocity measurement, for example Doppler velocimetry, rather than on finite differences of the same positions.

## 6. Status and prior art

- **What is standard.** The underlying mathematics is standard: Gaussian conditioning and the linear-functional variance of a process with a power-law structure function.
- **Prior-art screen.** Two web searches on 2026-10-08 found no treatment of finite-difference velocity estimation in velocity-conditioned MSDs. The nearest hit was a different mechanism: apparent superballistic motion from biased detachment in random walks. A limited screen does not establish novelty.
- **Sensitivity of related work.** A 2026 preprint on the fractal dimension of Brownian dynamics in liquids builds on the same physics. The velocity-increment version of this analysis is in [[Benchmark 018 — Apparent Velocity Roughness and the 7-4 Fractal Dimension]].
- **Validity.** The approximations are first order in $a$, with stationary Gaussian statistics and white position noise. Lab 45 shows that real noise is not white and not particle-independent.

[[Derivation Atlas]] · [[Benchmark 017 — Processing Dependence of the Conditioned Super-Ballistic Signal]] · [[Statistical Physics Map]]
