---
title: "Derivation — Quantum Harmonic Oscillator by Ladder Operators"
type: derivation
field: "Quantum Mechanics"
epistemic_status: established
level: intermediate
tags: [physics, derivation, deep-dive]
created: 2026-07-30
updated: 2026-09-02
note_maturity: worked-derivation
source_audit: canonical-derivation-needs-citation-audit
---

# Derivation — Quantum Harmonic Oscillator by Ladder Operators

## Hamiltonian

$$H=\frac{p^2}{2m}+\frac12m\omega^2x^2,\qquad [x,p]=i\hbar.$$

Define dimensionless ladder operators

$$
a=\sqrt{\frac{m\omega}{2\hbar}}x+\frac{i}{\sqrt{2m\hbar\omega}}p,
\qquad
a^\dagger=\sqrt{\frac{m\omega}{2\hbar}}x-\frac{i}{\sqrt{2m\hbar\omega}}p.
$$

The canonical commutator gives

$$[a,a^\dagger]=1.$$

Expanding $a^\dagger a$ yields

$$H=\hbar\omega\left(a^\dagger a+\frac12\right)
=\hbar\omega(N+\tfrac12).$$

## Spectrum

If $N|n\rangle=n|n\rangle$, commutators

$$[N,a]=-a,\qquad[N,a^\dagger]=a^\dagger$$

show that $a$ lowers and $a^\dagger$ raises $n$ by one. Positivity

$$\langle\psi|N|\psi\rangle=\|a|\psi\rangle\|^2\ge0$$

prevents an infinite descending chain. A ground state obeys $a|0\rangle=0$, and

$$
|n\rangle=\frac{(a^\dagger)^n}{\sqrt{n!}}|0\rangle,
\qquad
\boxed{E_n=\hbar\omega(n+\tfrac12)}.
$$

## Ground wavefunction

In position space, $p=-i\hbar\,d/dx$. The equation $a\psi_0=0$ gives

$$
\frac{d\psi_0}{dx}=-\frac{m\omega}{\hbar}x\psi_0,
$$

so

$$
\psi_0(x)=\left(\frac{m\omega}{\pi\hbar}\right)^{1/4}
e^{-m\omega x^2/(2\hbar)}.
$$

## Why this matters

Every stable **linear bosonic normal mode**, or mode of a quadratic Hamiltonian after diagonalization, is oscillator-like. Quantized free fields, phonons, photons, molecular vibrations, and linearized circuits reuse this algebra; interacting, constrained, fermionic, or strongly anharmonic degrees of freedom need additional structure.

## Connected notes

[[Quantum Harmonic Oscillator]] · [[Position and Momentum]] · [[Deep Dive — Harmonic Oscillator as Universal Local Physics|Harmonic Oscillator as Universal Local Physics]] · [[Phonons]] · [[Quantum Fields and Particles]]

## Navigation

[[Derivation Atlas]] · [[Physics Worldmap]]
