---
type: derivation
field: Statistical Physics
epistemic_status: established
level: advanced
tags: [generalized-langevin, autocorrelation, memory-kernel, realization, fluctuation-dissipation]
created: 2026-09-05
updated: 2026-09-05
source_audit: primary-equations-checked-with-local-numerical-reproduction
note_maturity: expanded
---

# Correlation-to-Memory Reconstruction from a VACF

> [!summary] Core idea
> A finite-dimensional realization of a normalized velocity autocorrelation function determines a rational memory kernel. Thermal validity requires more than a curve fit: stability, positive type, and a compatible noise covariance must also hold.

[[Benchmark 009 — Published Subdiffusion Memory Reproduction]] · [[Deep Dive — Mori-Zwanzig Projection]] · [[Open Quantum Systems]]

## 1. Correlation equation

For a scalar equilibrium generalized Langevin equation in reduced notation,

$$
\dot V(t)=-\int_0^t\gamma(t-s)V(s)\,ds+F(t),
$$

assume the random force is orthogonal to the initial resolved velocity in the projection-operator sense. The normalized velocity autocorrelation

$$
C(t)=\frac{\langle V(t)V(0)\rangle}{\langle V(0)^2\rangle}
$$

then obeys the Volterra equation

$$
\dot C(t)=-\int_0^t\gamma(t-s)C(s)\,ds,
\qquad C(0)=1.
$$

Taking the one-sided Laplace transform gives

$$
s\widetilde C(s)-1=-\widetilde\gamma(s)\widetilde C(s),
$$

so formally

$$
\boxed{\widetilde\gamma(s)=\frac{1}{\widetilde C(s)}-s.}
$$

This identity explains why correlation data contain memory information. It does not make inversion well-conditioned: finite windows, sampling, noise, zeros of $\widetilde C$, and model truncation all matter.

## 2. Extended Markov realization

Consider the deterministic part of an auxiliary-state system

$$
\frac{d}{dt}
\begin{pmatrix}V\\Y\end{pmatrix}
=
\begin{pmatrix}0&b^T\\-c&A_0\end{pmatrix}
\begin{pmatrix}V\\Y\end{pmatrix}.
$$

Solving the second row by variation of constants,

$$
Y(t)=e^{tA_0}Y(0)-\int_0^t e^{(t-s)A_0}cV(s)\,ds.
$$

Substitution into the first row yields

$$
\dot V(t)=b^Te^{tA_0}Y(0)-\int_0^t
b^Te^{(t-s)A_0}cV(s)\,ds.
$$

The auxiliary initial state contributes to the fluctuating force, while the finite-dimensional memory kernel is

$$
\boxed{\gamma_N(t)=b^Te^{tA_0}c.}
$$

If $A_0$ is stable, this is a finite sum of decaying exponential and damped-oscillatory terms. It is continuous at the origin with $\gamma_N(0)=b^Tc$.

## 3. From samples to a realization

Suppose $y_\nu=C(\nu\tau)$ for $\nu=0,\ldots,2n-1$. A Prony-type moment construction seeks a Jacobi matrix $J$ such that

$$
e_1^TJ^\nu e_1=y_\nu.
$$

If an admissible logarithm exists,

$$
A=\frac{1}{\tau}\log J
$$

gives

$$
e_1^Te^{\nu\tau A}e_1=y_\nu.
$$

Thus $C_N(t)=e_1^Te^{tA}e_1$ is an exponential interpolant. The derivative at the origin is $C_N'(0)=A_{11}$. For a continuous integrable kernel the Volterra equation gives $C'(0)=0$, motivating a small adjustment of the first nontrivial sample to enforce $A_{11}\approx0$.

This is the central construction in [Bockius et al. (2021), Sections 2 and Appendix C](https://arxiv.org/html/2101.02657).

## 4. Why positivity is a physics constraint

A stable exponential interpolation is not automatically an equilibrium autocorrelation. An autocorrelation must be of positive type, equivalently have a nonnegative spectral measure. In the auxiliary realization, a key transfer function is

$$
\kappa(s)=b^T(sI-A_0)^{-1}c.
$$

The published construction requires it to be positive real:

$$
\operatorname{Re}\kappa(i\omega)\ge0
$$

for all real frequencies in the nonsingular setting. Under the paper's controllability assumptions, the Positive Real Lemma connects this condition to a positive-semidefinite auxiliary covariance and a compatible noise factor.

This separates three questions that should never be conflated:

1. Does the finite exponential model interpolate the samples?
2. Is the continuous-time realization stable and physically admissible?
3. Does a verified stochastic forcing reproduce the required stationary covariance and fluctuation–dissipation structure?

Benchmark 009 answers much of (1), numerically screens (2), and constructs a covariance/noise factor satisfying (3) for one clean fitted realization. It does not turn the sampled frequency screen into an analytic positivity proof or establish robustness to noisy data.

## 5. Identifiability and regularity limits

Finite samples do not determine an arbitrary continuum kernel without assumptions. Choosing a finite state dimension imposes rational structure. Regular sampling can also alias continuous modes, and noise can create unstable or negligible-weight Prony components.

The subdiffusion example makes a second limitation explicit:

$$
\gamma(t)=\frac{1}{\sqrt{\pi t}}
$$

diverges at $t=0$, whereas every fixed finite auxiliary realization has finite $\gamma_N(0)$. The VACF can nevertheless be reproduced accurately on a finite interval. Therefore, small correlation error does not by itself certify the correct short-time regularity of the inferred memory.

## 6. Practical audit checklist

For any correlation-to-memory result, record:

- normalization, units, equilibrium assumptions, and preprocessing;
- sampling interval, number of samples, and observation window;
- state order and how spurious or aliased modes are handled;
- stability of both $A$ and $A_0$;
- interpolation error and held-out correlation error;
- positive-real or spectral-positivity evidence;
- construction and residual check of the stationary noise covariance;
- kernel sensitivity to sampling, order, window, and noise;
- unresolved behavior near $t=0$ and beyond the observation window.

## 7. What this enables

The realization converts a nonlocal equation into a local higher-dimensional one, useful for simulation and model reduction. More importantly for this vault, it provides a disciplined bridge between observed equilibrium correlations and candidate response dynamics. That bridge remains conditional: response prediction inherits every assumption used to select the realization and certify its thermal consistency.

[[Benchmark 002 — The Sampling Boundary of Prediction]] · [[Epistemic Status and Claim Hygiene]] · [[Theory Experiment Computation Loop]]
