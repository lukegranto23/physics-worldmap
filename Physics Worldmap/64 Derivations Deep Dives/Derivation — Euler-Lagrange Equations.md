---
title: "Derivation — Euler-Lagrange Equations"
type: derivation
field: "Classical Mechanics"
epistemic_status: established
level: intermediate
tags: [physics, derivation, deep-dive]
created: 2026-07-30
updated: 2026-07-30
note_maturity: worked-derivation
source_audit: canonical-derivation-needs-citation-audit
---

# Derivation — Euler-Lagrange Equations

## Target

Derive the equations obeyed by a path that makes the action stationary.

## Setup

For generalized coordinates $q_i(t)$, define

$$S[q]=\int_{t_1}^{t_2}L(q_i,\dot q_i,t)\,dt.$$

Compare $q_i(t)$ with nearby paths $q_i(t)+\epsilon\eta_i(t)$ whose endpoints are fixed:

$$\eta_i(t_1)=\eta_i(t_2)=0.$$

## Variation

To first order,

$$
\delta S
=\epsilon\int_{t_1}^{t_2}
\left(
\frac{\partial L}{\partial q_i}\eta_i+
\frac{\partial L}{\partial\dot q_i}\dot\eta_i
\right)dt.
$$

Integrate the second term by parts:

$$
\int \frac{\partial L}{\partial\dot q_i}\dot\eta_i\,dt
=
\left[\frac{\partial L}{\partial\dot q_i}\eta_i\right]_{t_1}^{t_2}
-\int\frac d{dt}\left(\frac{\partial L}{\partial\dot q_i}\right)\eta_i\,dt.
$$

The boundary term vanishes because the endpoint variations vanish. Therefore

$$
\delta S
=\epsilon\int_{t_1}^{t_2}
\left[
\frac{\partial L}{\partial q_i}
-\frac d{dt}\left(\frac{\partial L}{\partial\dot q_i}\right)
\right]\eta_i\,dt.
$$

The $\eta_i(t)$ are otherwise arbitrary. The fundamental lemma of the calculus of variations implies

$$
\boxed{\frac d{dt}\frac{\partial L}{\partial\dot q_i}
-\frac{\partial L}{\partial q_i}=0.}
$$

## Recovering Newton

For a particle with $L=\tfrac12m\dot{\mathbf r}^2-V(\mathbf r)$,

$$\frac d{dt}(m\dot{\mathbf r})+\nabla V=0,$$

so $m\ddot{\mathbf r}=-\nabla V$.

## What was assumed

- differentiable paths and Lagrangian;
- fixed endpoint values;
- local dependence on $q$, $\dot q$, and $t$;
- holonomic constraints already encoded in the coordinates, or handled separately.

Higher derivatives, fields, nonholonomic constraints, dissipation, and variable endpoints modify the calculation but not the logic.

## Connected notes

[[Calculus of Variations]] · [[Lagrangian Mechanics]] · [[Constraints and Generalized Coordinates]] · [[Noethers Theorem in Mechanics]]

## Navigation

[[Derivation Atlas]] · [[Physics Worldmap]]
