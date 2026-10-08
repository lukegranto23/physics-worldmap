---
title: "Derivation — Infinite Quantum Well"
type: derivation
field: "Quantum Mechanics"
epistemic_status: established
level: introductory
tags: [physics, derivation, deep-dive]
created: 2026-07-30
updated: 2026-07-30
note_maturity: worked-derivation
source_audit: canonical-derivation-needs-citation-audit
---

# Derivation — Infinite Quantum Well

## Problem

A particle is confined to $0<x<L$ by infinite potential walls:

$$
V(x)=
\begin{cases}
0,&0<x<L,\\
\infty,&\text{otherwise}.
\end{cases}
$$

The wavefunction vanishes at the walls and outside.

## Stationary equation

Inside,

$$-\frac{\hbar^2}{2m}\frac{d^2\psi}{dx^2}=E\psi.$$

For positive $E$, define $k=\sqrt{2mE}/\hbar$:

$$\psi(x)=A\sin kx+B\cos kx.$$

Boundary condition $\psi(0)=0$ gives $B=0$. The other wall requires

$$\sin(kL)=0\quad\Rightarrow\quad kL=n\pi,\qquad n=1,2,\ldots$$

Thus

$$
\boxed{E_n=\frac{n^2\pi^2\hbar^2}{2mL^2}},
\qquad
\boxed{\psi_n(x)=\sqrt{\frac2L}\sin\frac{n\pi x}{L}}.
$$

The normalization follows from $\int_0^L|\psi_n|^2dx=1$.

## Physical checks

- $E$ has dimensions of energy.
- Confinement energy grows as $L^{-2}$.
- There is no $n=0$ state: it would be the zero wavefunction after applying both boundaries.
- The ground energy is nonzero because a localized state cannot have identically zero momentum spread.
- The eigenfunctions are orthogonal and complete for square-integrable functions satisfying the boundaries.

## General state

$$
\psi(x,t)=\sum_{n=1}^\infty c_n\psi_n(x)e^{-iE_nt/\hbar},
\qquad
c_n=\int_0^L\psi_n^*(x)\psi(x,0)\,dx.
$$

Probabilities can evolve even though each energy eigenstate's density is stationary.

## Connected notes

[[Infinite and Finite Square Wells]] · [[Stationary States]] · [[Fourier Analysis]] · [[Uncertainty Relations]] · [[Computational Lab Index]]

## Navigation

[[Derivation Atlas]] · [[Physics Worldmap]]
