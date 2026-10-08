---
title: "Derivation — Fermi Golden Rule"
type: derivation
field: "Quantum Mechanics"
epistemic_status: established
level: advanced
tags: [physics, derivation, deep-dive]
created: 2026-07-30
updated: 2026-07-30
note_maturity: worked-derivation
source_audit: canonical-derivation-needs-citation-audit
---

# Derivation — Fermi Golden Rule

## Setup

Let

$$H=H_0+V(t)$$

and suppose a weak perturbation couples an initial eigenstate $|i\rangle$ to many final states $|f\rangle$. First-order time-dependent perturbation theory gives

$$
c_f^{(1)}(t)
=-\frac{i}{\hbar}\int_0^t
\langle f|V(t')|i\rangle e^{i\omega_{fi}t'}dt'.
$$

For a constant switched-on matrix element $V_{fi}$,

$$
|c_f^{(1)}(t)|^2
=\frac{|V_{fi}|^2}{\hbar^2}
\frac{4\sin^2(\omega_{fi}t/2)}{\omega_{fi}^2}.
$$

At long times, the sharply peaked sinc-squared factor behaves distributionally as

$$
\frac{4\sin^2(\omega t/2)}{\omega^2}
\longrightarrow2\pi t\,\delta(\omega).
$$

Summing over a continuum of final states with density $\rho(E_f)$ gives a transition probability linear in time:

$$
\boxed{
\Gamma_{i\to f}
=\frac{2\pi}{\hbar}|V_{fi}|^2\rho(E_f)
}
$$

evaluated at energy conservation $E_f=E_i$ or at the shifted resonance for a periodic drive.

## Conditions

- weak coupling and small depletion of the initial state;
- a dense continuum of final states;
- observation time long relative to correlation time but short enough for the perturbative exponential/rate description;
- matrix element varying slowly over the narrow energy window.

Discrete coherent two-level systems undergo Rabi oscillations instead of irreversible golden-rule decay.

## Connected notes

[[Time Dependent Perturbation Theory]] · [[Scattering in Quantum Mechanics]] · [[Spontaneous and Stimulated Emission]] · [[Radioactive Decay]]

## Navigation

[[Derivation Atlas]] · [[Physics Worldmap]]
