---
type: "reference"
field: "Physics"
epistemic_status: "reference"
level: "all"
tags: ["reference", "notation", "units"]
aliases: []
created: 2026-07-30
updated: 2026-07-30
---

# Notation Units and Conventions

## Default

- SI units unless a note explicitly declares natural, Gaussian, geometric, or lattice units.
- Metric signature $(-,+,+,+)$ unless stated otherwise.
- $c$, $\hbar$, $k_B$, and $G$ remain visible in cross-field notes; specialist derivations may set them to 1.
- Repeated tensor indices are summed when explicitly declared.
- Fourier convention: $\tilde f(k)=\int f(x)e^{-ikx}\,dx$ and $f(x)=(2\pi)^{-n}\int\tilde f(k)e^{ikx}\,dk$.
- Probabilities use $p$ for densities or mass functions and $P$ for events where practical.

## Unit discipline

1. Write a numerical value as value × unit.
2. Convert once at an interface, not repeatedly inside a calculation.
3. Use dimensionless logarithm arguments and exponentials.
4. Record constants and reference datasets with version and uncertainty.
5. Distinguish angular frequency $\omega$ from cyclic frequency $f$: $\omega=2\pi f$.

## Common dimensionless groups

| Group | Meaning |
|---|---|
| $Re=UL/\nu$ | inertia / viscosity |
| $Ma=U/c_s$ | flow speed / sound speed |
| $Pe=UL/D$ | advection / diffusion |
| $Kn=\lambda_{\rm mfp}/L$ | microscopic / continuum scale |
| $Fr=U/\sqrt{gL}$ | inertia / gravity |
| $We=\rho U^2L/\gamma$ | inertia / surface tension |
| $\alpha=e^2/(4\pi\epsilon_0\hbar c)$ | electromagnetic coupling |
| compactness $GM/(Rc^2)$ | gravitational strength |

See [[Scale Ladder]] and [[Dimensional Analysis]].
