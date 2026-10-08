---
type: computational-benchmark
field: Statistical Physics
epistemic_status: effective
level: advanced
tags: [brownian-motion, hydrodynamic-memory, fractal-dimension, roughness-exponent, measurement-operator, reanalysis]
created: 2026-10-08
updated: 2026-10-08
note_maturity: expanded
source_audit: preprints-known-only-from-search-summaries; data-digest-verified
---

# Benchmark 018 — Apparent Velocity Roughness and the 7/4 Fractal Dimension

**Status:** theory plus a post hoc descriptive comparison on the digest-verified Dryad traces. There is no preregistered decision rule. The two preprints that motivate this note could not be read here (arXiv is blocked), and their processing is unknown. So this note says what *would* follow for velocity-increment scaling estimated from stencil velocities. It does not say that those papers are wrong.

Lab 47 is `47_velocity_roughness_estimator_bias.py`, with outputs and the figure `apparent_velocity_roughness.png` in `results/velocity_roughness/`.

## Context

Two 2026 preprints (arXiv:2605.16252 and 2605.16247) discuss a velocity roughness exponent $H_v=1/4$, equivalently a fractal dimension $d_v=2-H_v=7/4$, for Brownian motion with fluid inertia. They read it as a change of universality class.

The theory behind that value is standard. If $C_v(\tau)=c-a|\tau|^{1/2}$ (Basset memory), then $\operatorname{Var}[v(t)-v(0)]=2a\,t^{1/2}$, so $H_v=1/4$ at short times.

## Theory: stencil velocities look smoother

[[Derivation — Conditioning on an Estimated Velocity]] uses the bin-averaged generalised covariance, so here
$$\operatorname{Var}(W_k-W_0)=a\Delta^\alpha\,\Psi_\alpha(k),$$
with weights $d_{l-k}-d_l$. These annihilate constant and linear motion, so the ballistic term cancels. In the continuum limit $\Psi\to2k^\alpha$, and a check at $k=2000$ gives 0.986. The apparent $H_v$ is half the local log-slope of $\Psi$:

| True $H_v$ | Stencil | Apparent $H_v$ at $k=1$ / 2 / 4 / 8 / 16 |
|---|---|---|
| 0.25 (Basset) | order 8 | 0.67 / 0.50 / 0.36 / 0.31 / 0.29 |
| 0.25 | order 2 | 0.79 / 0.65 / 0.43 / 0.34 / 0.31 |
| 0.50 (Langevin) | order 8 | 0.77 / 0.66 / 0.56 / 0.52 / 0.51 |

As for the conditioned MSD, softer cusps recover most slowly. Values for $\alpha$ between ¼ and 1 are in `results.json`.

**Full published Basset model**, order 8 at 750 ns, noise-free. The apparent $H_v$ at lags 1–64 is 0.67, 0.50, 0.37, 0.35, 0.32, 0.29, 0.27, 0.24, 0.22, 0.19, 0.17, 0.15. It passes through ¼ near 11 µs on its way down to the trap-dominated regime and **never plateaus at ¼**.

## Data (descriptive)

Velocities were recomputed from the supplied positions with stencils of order 2, 4 and 8 at 750 ns. Empty-trap increment variances were subtracted. The published gain was used.

- **Noise-subtracted data follow the forward model.** From lag 4 onward they are within 1–6% of the full Basset model for all three stencils. At lags 2–4 they are 13–18% above it. That is the band where lab 45 found the 100–400 kHz excess.
- **Raw data show a pseudo-plateau.** Without noise subtraction, the order-8 apparent $H_v$ is 0.27, 0.21, 0.24, 0.23, 0.23, 0.22, 0.21 at lags 2–16 (1.5–12 µs). Read naively, that looks like a scaling regime with $H_v\approx1/4$. It is actually a falling curve flattened by detector noise.

## Interpretation

- **Physics.** In these data, $H_v=1/4$ is consistent with Basset memory. But it shows up only as the value the local exponent passes through, not as a plateau.
- **Method.** A plateau near ¼ in stencil-velocity increments is not by itself evidence of a $d_v=7/4$ scaling regime. Operator smoothing pushes the exponent up at short lags. Noise pulls it down. Trap and higher-order hydrodynamics pull it down at long lags.
- **Remedy.** Forward-model the estimator, as here. Lab 46's criterion applies: for $\alpha=\tfrac12$ the estimator bias falls below 0.05 in $H_v$ only beyond about 20–40 bins, by which point the trap has entered at these parameters.

## Limits

- The preprints' exact estimator is not known. Their scale-dependent absolute slope $E|\Delta v|/\Delta t$ has the same exponent as the variance for Gaussian increments, but their binning, filtering and data may differ.
- The analysis is first order in $a$ for the universal curves. The full-model comparison covers only the published parameters.
- The noise-subtraction caveats of [[Benchmark 015 — Gain-Free Test of Hydrodynamic Memory]] apply (lab 45).

## Next

If the preprints' processing becomes readable, apply lab 47 to their exact estimator. Add this figure to any follow-up with the data authors; it is the velocity-roughness counterpart of [[Benchmark 017 — Processing Dependence of the Conditioned Super-Ballistic Signal]].

[[Derivation — Conditioning on an Estimated Velocity]] · [[Benchmark 017 — Processing Dependence of the Conditioned Super-Ballistic Signal]] · [[Computational Lab Index]]
