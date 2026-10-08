---
title: "Derivation — Mean-Field Ising Critical Point"
type: derivation
field: "Statistical Physics"
epistemic_status: established
level: advanced
tags: [physics, derivation, deep-dive]
created: 2026-07-30
updated: 2026-07-30
note_maturity: worked-derivation
source_audit: canonical-derivation-needs-citation-audit
---

# Derivation — Mean-Field Ising Critical Point

## Model

$$H=-J\sum_{\langle ij\rangle}s_is_j-h\sum_is_i,\qquad s_i=\pm1.$$

For coordination number $z$, replace neighboring spins by their mean magnetization

$$m=\langle s_i\rangle.$$

Each spin sees an effective field

$$h_{\rm eff}=h+zJm.$$

The single-spin thermal average is

$$
\boxed{m=\tanh[\beta(h+zJm)]}.
$$

This self-consistency equation is the mean-field theory.

## Critical temperature

At $h=0$ and small $m$,

$$\tanh(\beta zJm)\approx\beta zJm-\frac13(\beta zJm)^3+\cdots.$$

A nonzero solution first appears when

$$\beta_c zJ=1,\qquad \boxed{k_BT_c^{\rm MF}=zJ}.$$

Just below $T_c$, solve the cubic balance:

$$m\propto(T_c-T)^{1/2}.$$

Mean field predicts critical exponent $\beta_{\rm mag}=1/2$.

## Why it fails near low-dimensional critical points

The approximation neglects spatial correlations. Near a continuous transition the correlation length diverges, making fluctuations across all scales important. In the two-dimensional nearest-neighbor Ising model the exact magnetization exponent is $1/8$, not $1/2$.

The Ginzburg criterion estimates where fluctuations invalidate mean field; the renormalization group explains the correct universal exponents.

## Connected notes

[[Ising Model]] · [[Order Parameters and Symmetry Breaking]] · [[Landau Theory]] · [[Critical Phenomena]] · [[Renormalization Group]]

## Navigation

[[Derivation Atlas]] · [[Physics Worldmap]]
