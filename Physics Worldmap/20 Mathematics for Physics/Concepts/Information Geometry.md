---
type: "concept"
field: "Mathematics for Physics"
epistemic_status: "established"
level: "advanced"
tags: ["physics", "field/mathematics", "status/established", "level/advanced"]
aliases: ["Fisher information metric", "statistical manifold"]
created: 2026-07-30
updated: 2026-09-04
note_maturity: expanded
source_audit: bibliography-present-needs-claim-audit
---

# Information Geometry

> [!summary] Core idea
> A regular identifiable family of probability distributions has a Fisher metric that quantifies infinitesimal distinguishability. Geometry on distributions is not automatically geometry of physical spacetime.

> [!note] Documentation status
> Expanded orientation; canonical references are provided, but application-specific identifications require separate audits.

## Classical metric and local distances

For a smooth normalized family $p(x|\theta)$ with parameter-independent support and suitable integrability,
$$
g^F_{ij}=\mathbb E_\theta[\partial_i\log p\,\partial_j\log p].
$$
It is positive semidefinite and becomes a metric after nonidentifiable directions are removed. Under regularity conditions it equals $-\mathbb E[\partial_i\partial_j\log p]$.

The local expansions are
$$
D_{\rm KL}(p_\theta\|p_{\theta+d\theta})
=\tfrac12 g^F_{ij}d\theta^id\theta^j+O(\|d\theta\|^3),
$$
$$
8\left(1-\int\sqrt{p_\theta p_{\theta+d\theta}}\,dx\right)
=g^F_{ij}d\theta^id\theta^j+O(\|d\theta\|^3).
$$
The second relation is infinitesimal, not an exact formula for arbitrary finite separations. Chentsov's finite-sample-space theorem characterizes the Fisher metric, up to scale, using congruent Markov embeddings/sufficient-statistic invariance. Arbitrary stochastic coarse-graining is contractive, not generally an isometry.

## Exponential families and dual coordinates

For $p(x|\theta)=h(x)\exp[\theta^iT_i(x)-\psi(\theta)]$,
$$
\eta_i=\partial_i\psi=\mathbb E[T_i],\qquad
g^F_{ij}=\partial_i\partial_j\psi=\operatorname{Cov}(T_i,T_j).
$$
The expectation of the score $\mathbb E[\partial_i\log p]$ is zero, not the expectation-coordinate vector. Exponential and mixture connections are dual; their flatness on full regular exponential families does not make every statistical manifold dually flat.

## Worked example

For a Gaussian with mean $\mu$ and standard deviation $\sigma$,
$$
ds^2=\frac{d\mu^2+2\,d\sigma^2}{\sigma^2}.
$$
With $x=\mu/\sqrt2$ and $y=\sigma$, this is $2(dx^2+dy^2)/y^2$: a scaled hyperbolic metric. The coordinate rescaling matters when drawing geodesics.

## Natural gradient and estimation

The natural-gradient vector is $(\operatorname{grad}_g L)^i=(g^{-1})^{ij}\partial_jL$. It gives steepest local change at fixed metric length. The continuous vector field is coordinate invariant, but a finite Euler update need not be. Better convergence is not guaranteed: metric estimation, conditioning, regularization, and cost matter.

For $n$ independent samples, a regular unbiased estimator satisfies
$\operatorname{Cov}(\hat\theta)\succeq(ng^F)^{-1}$.
Finite-sample attainability requires additional conditions; asymptotic efficiency is a different statement.

## Quantum metrics

Define the SLD by $\partial_i\rho=(\rho L_i+L_i\rho)/2$ and
$$
(F_Q)_{ij}=\tfrac12\operatorname{Tr}\rho\{L_i,L_j\},
\qquad ds_B^2=\tfrac14(F_Q)_{ij}d\theta^id\theta^j.
$$
For a single parameter, the SLD QFI is the maximum classical Fisher information obtainable by optimizing the measurement locally. Multiparameter optima can be incompatible. Petz's classification gives infinitely many monotone quantum metrics; SLD/Bures is not the unique one. [Petz](https://doi.org/10.1016/0024-3795(94)00211-8), [Braunstein and Caves](https://doi.org/10.1103/PhysRevLett.72.3439)

## Connections and boundaries

Canonical thermodynamics gives $g_{\beta\beta}=\operatorname{Var}(E)=k_BT^2C_V$ when $\beta=1/(k_BT)$. Relations to entropy-Hessian/Ruppeiner geometry depend on coordinates, constraints, and conventions. Curvature is not a universal detector of every phase transition.

QFT information metrics require regulators and careful operator normalization. RG monotonicity does not by itself prove Fisher natural-gradient flow. See [[Synthesis Session 003 — RG Flow as Information Geometry and the Shape of Scale]].

## Canonical references and recall

Amari, *Information Geometry and Its Applications* (2016); Chentsov, *Statistical Decision Rules and Optimal Inference* (1982). Derive the covariance identity above, state when a metric is singular, and distinguish endpoint distance from accumulated trajectory length.

## Navigation

[[Mathematics for Physics Map]] · [[Information Theory]] · [[Differential Geometry]] · [[Statistical Estimation]] · [[Synthesis Session 004 — The Geometry of Thermalization]] · [[Physics Worldmap]]
