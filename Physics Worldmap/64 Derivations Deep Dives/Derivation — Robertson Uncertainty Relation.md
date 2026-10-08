---
title: "Derivation — Robertson Uncertainty Relation"
type: derivation
field: "Quantum Mechanics"
epistemic_status: established
level: intermediate
tags: [physics, derivation, deep-dive]
created: 2026-07-30
updated: 2026-07-30
note_maturity: worked-derivation
source_audit: canonical-derivation-needs-citation-audit
---

# Derivation — Robertson Uncertainty Relation

## Target

Derive a state-dependent lower bound on dispersions of two observables.

Define centered operators

$$\tilde A=A-\langle A\rangle,\qquad \tilde B=B-\langle B\rangle.$$

For normalized $|\psi\rangle$, set

$$|\alpha\rangle=\tilde A|\psi\rangle,\qquad|\beta\rangle=\tilde B|\psi\rangle.$$

Cauchy-Schwarz gives

$$
\langle\alpha|\alpha\rangle\langle\beta|\beta\rangle
\ge|\langle\alpha|\beta\rangle|^2.
$$

The left side is $(\Delta A)^2(\Delta B)^2$. The imaginary part of the inner product is

$$
\operatorname{Im}\langle\alpha|\beta\rangle
=\frac1{2i}\langle[A,B]\rangle.
$$

Since $|z|^2\ge(\operatorname{Im}z)^2$,

$$
\boxed{\Delta A\,\Delta B\ge\frac12|\langle[A,B]\rangle|.}
$$

For $[x,p]=i\hbar$,

$$\boxed{\Delta x\,\Delta p\ge\hbar/2.}$$

## Stronger form

Keeping both real and imaginary parts gives the Schrödinger-Robertson relation:

$$
(\Delta A)^2(\Delta B)^2
\ge
\frac14|\langle[A,B]\rangle|^2
+\frac14|\langle\{\tilde A,\tilde B\}\rangle|^2.
$$

The anticommutator term captures covariance.

## Interpretive limits

This relation concerns ensemble dispersion in a quantum state. It is not simply a claim that a measuring device kicks an already definite value, nor is it a universal energy-time operator relation. Preparation uncertainty, measurement disturbance, and entropic uncertainty have distinct formulations.

## Connected notes

[[Uncertainty Relations]] · [[Compatible Observables]] · [[Position and Momentum]] · [[Quantum Measurement]]

## Navigation

[[Derivation Atlas]] · [[Physics Worldmap]]
