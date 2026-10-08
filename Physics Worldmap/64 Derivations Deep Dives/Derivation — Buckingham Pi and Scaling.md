---
title: "Derivation — Buckingham Pi and Scaling"
type: derivation
field: "Mathematics for Physics"
epistemic_status: established
level: intermediate
tags: [physics, derivation, deep-dive]
created: 2026-07-30
updated: 2026-07-30
note_maturity: worked-derivation
source_audit: canonical-derivation-needs-citation-audit
---

# Derivation — Buckingham Pi and Scaling

## Target

Reduce a physical relation among dimensional variables to a smaller relation among dimensionless groups, then use it to predict scaling without solving the dynamics.

## Linear-algebra derivation

Suppose an observable depends on $n$ dimensional variables,

$$q_1=f(q_2,\ldots,q_n).$$

Choose $k$ independent base dimensions, such as mass $M$, length $L$, and time $T$. Represent each variable by a dimension vector:

$$[q_j]=M^{a_{1j}}L^{a_{2j}}T^{a_{3j}}\cdots.$$

Collect the exponents in a $k\times n$ dimension matrix $D$. A monomial

$$\Pi=\prod_{j=1}^n q_j^{x_j}$$

is dimensionless exactly when

$$D\mathbf x=0.$$

Rank-nullity gives $n-r$ independent null vectors, where $r=\operatorname{rank}D\le k$. Therefore the original law can be written as a relation among $n-r$ independent dimensionless products:

$$F(\Pi_1,\ldots,\Pi_{n-r})=0.$$

This is Buckingham's Pi theorem in computational form.

## Worked example — drag on a sphere

Let drag $F$ depend on fluid density $\rho$, speed $U$, sphere diameter $d$, and dynamic viscosity $\mu$. Five variables use three base dimensions, so expect two independent groups. A convenient choice is

$$C_D=\frac{F}{\tfrac12\rho U^2A},\qquad Re=\frac{\rho Ud}{\mu}.$$

Thus

$$C_D=\Phi(Re).$$

Dimensional analysis cannot determine $\Phi$, but it proves that geometrically similar, steady, incompressible Newtonian experiments collapse to one curve if those are truly the only relevant variables.

## Checks and failure modes

- If compressibility matters, add sound speed and obtain Mach number.
- If a free surface matters, add gravity and surface tension, producing Froude and Weber numbers.
- A dimensionally valid formula can still violate symmetry, causality, or data.
- Constants such as $2$ or $\pi$ cannot be obtained from dimensions.

## Connected notes

[[Dimensional Analysis]] · [[Units Dimensions and Conventions]] · [[Dimensional Analysis in Fluids]] · [[Approximation and Regime Map]]

## Navigation

[[Derivation Atlas]] · [[Physics Worldmap]]
