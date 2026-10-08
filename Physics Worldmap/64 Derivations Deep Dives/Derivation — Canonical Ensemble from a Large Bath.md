---
title: "Derivation — Canonical Ensemble from a Large Bath"
type: derivation
field: "Statistical Physics"
epistemic_status: established
level: intermediate
tags: [physics, derivation, deep-dive]
created: 2026-07-30
updated: 2026-07-30
note_maturity: worked-derivation
source_audit: canonical-derivation-needs-citation-audit
---

# Derivation — Canonical Ensemble from a Large Bath

## Setup

A small system $S$ exchanges energy with a much larger isolated bath $B$. The total energy is fixed:

$$E_{\rm tot}=E_i+E_B.$$

Assume weak coupling so energies are additive and the total composite explores compatible microstates.

## Bath multiplicity

The probability of system microstate $i$ is proportional to the number of bath states at the remaining energy:

$$p_i\propto\Omega_B(E_{\rm tot}-E_i).$$

Write bath entropy $S_B(E)=k_B\ln\Omega_B(E)$ and expand because $E_i$ is small relative to the bath:

$$
S_B(E_{\rm tot}-E_i)
\approx S_B(E_{\rm tot})
-E_i\left(\frac{\partial S_B}{\partial E_B}\right)
+\cdots.
$$

Using $\partial S/\partial E=1/T$,

$$
\Omega_B(E_{\rm tot}-E_i)
\propto e^{-E_i/(k_BT)}.
$$

Normalize:

$$
\boxed{p_i=\frac{e^{-\beta E_i}}{Z}},\qquad
\boxed{Z=\sum_ie^{-\beta E_i}},\qquad
\beta=\frac1{k_BT}.
$$

## Thermodynamics from $Z$

$$
F=-k_BT\ln Z,\qquad
\langle E\rangle=-\frac{\partial\ln Z}{\partial\beta},
$$

and

$$
\operatorname{Var}(E)=\frac{\partial^2\ln Z}{\partial\beta^2}
=k_BT^2C_V.
$$

## Assumptions and failure regimes

- weak system-bath coupling;
- bath much larger than the system;
- equilibrium or suitable typicality/ergodicity assumptions;
- additive conserved energy.

Small baths, long-range interactions, strong coupling, integrability, glassiness, localization, or driven steady states can require different ensembles or explicit dynamics.

## Connected notes

[[Canonical Ensemble]] · [[Partition Functions]] · [[Temperature]] · [[Fluctuations]] · [[Ergodicity and Typicality]]

## Navigation

[[Derivation Atlas]] · [[Physics Worldmap]]
