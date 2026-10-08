---
type: computational-benchmark
field: Statistical Physics
epistemic_status: effective
level: advanced
tags: [physics, generalized-langevin, memory-kernel, reproduction, model-reduction]
created: 2026-09-05
updated: 2026-09-05
source_audit: primary-method-and-equations-inspected-scoped-reproduction
note_maturity: expanded
---

# Benchmark 009 — Published Subdiffusion Memory Reproduction

> [!important] Outcome
> A scoped, independent implementation reproduces the clean $\tau=0.6$, $n=10$ subdiffusion case of Bockius et al. through the moment-Jacobi, Newton-constraint, stable-realization, diagnostic memory-recovery, regularized thermal-covariance, and final Lanczos stages. It also reproduces their reported coarse-grid unconstrained derivative. This is not the authors' code or a reproduction of every paper experiment.

[[Correlation-to-Memory Reconstruction from a VACF]] · [[Research Frontier — Identifiability Before Discovery]] · [[Synthesis Session 001 — Response-Preserving Coarse-Graining]]

## Why this benchmark exists

Benchmarks 001–008 were internally constructed controls. They clarified response ambiguity, detection limits, and sensor attribution, but they did not establish that this vault could implement a leading thermal-memory method from its published equations.

This benchmark begins that external-method gate with [Bockius, Shea, Jung, Schmid, and Hanke (2021)](https://arxiv.org/html/2101.02657). Their method maps equally spaced normalized velocity-autocorrelation samples to an extended Markov representation of a generalized Langevin equation. The paper's Section 3.1 supplies an analytic subdiffusion test with

$$
C_V(t)=E_{3/2}(-|t|^{3/2}),
\qquad
\gamma(t)=\frac{1}{\sqrt{\pi t}},
$$

in reduced units $m=\beta=1$.

The [local protocol](../62%20Computational%20Labs/thermal_memory_reproduction_protocol.json) records the precise implemented and omitted stages. It was written after exploratory implementation checks, so its thresholds are regression gates, **not** an external preregistration. Versions 1.1 and 1.2 record post-first-run additions of the Riccati/noise-factor and final Lanczos stages after independent residual checks; earlier gates were unchanged.

## What was implemented

The independent program follows these published components:

1. Evaluate the analytic VACF on the paper's equally spaced grid.
2. Implement Appendix C, Algorithm 2: construct the nonsymmetric Jacobi matrix $J$ from the moment functional $\Phi[x^\nu]=y_\nu$, together with its analytic derivative with respect to $y_1$.
3. Use the Appendix A block-matrix logarithm to evaluate the Fréchet derivative and perform the paper's Newton update enforcing $\operatorname{Re}A_{11}\approx0$.
4. Form $A=\tau^{-1}\log J$ for the primary case, where no discrete pole is negative real or lies on/outside the unit circle.
5. Partition

$$
A=\begin{pmatrix}0&b^T\\-c&A_0\end{pmatrix}
$$

and recover the diagnostic memory kernel

$$
\gamma_N(t)=b^T e^{tA_0}c.
$$

6. Sample the paper's positive-real condition

$$
\operatorname{Re}\!\left[b^T(i\omega I-A_0)^{-1}c\right]\ge0
$$

over nine decades in frequency.

7. Solve the regularized Riccati equation from the paper's Equation 62 for the auxiliary covariance $\Sigma_0$, construct its rank-one noise factor $L$, and verify

$$
A_\delta\Sigma+\Sigma A_\delta^T=-LL^T,
\qquad
\Sigma e_1=e_1,
$$

with $A_{\delta,11}=-10^{-5}$.

8. Apply the final nonsymmetric Lanczos sweep initialized at $e_1$, checking the similarity relation, the signed $(+k,-k)$ coupling, tridiagonal leakage, kernel invariance, and the transformed Lyapunov identity.

The analytic target is evaluated with a pole-plus-branch-cut integral representation. On 21 points from $t=0$ to $5$, it agrees with the defining Mittag-Leffler series to maximum absolute error $2.86\times10^{-15}$.

## Primary reproduction

The paper's $\tau=0.6$, $n=10$ case uses 20 exact VACF samples. The Newton iteration terminates after seven recorded evaluations (six updates):

| Quantity | Result |
|---|---:|
| Original $y_1$ | 0.6845298938 |
| Adjusted $y_1$ | 0.6861128425 |
| Absolute adjustment | 0.0015829487 |
| $|A_{11}|$ after adjustment | $1.47\times10^{-6}$ |
| Jacobi moment-identity maximum error | $9.55\times10^{-13}$ |
| Largest discrete-pole modulus | 0.9699403 |
| Largest real part of an $A$ eigenvalue | $-0.0508679$ |

The reconstructed VACF has RMSE $8.18\times10^{-4}$ on 601 points spanning $0\le t\le30$. It interpolates the adjusted samples to $9.55\times10^{-13}$. The difference between original and adjusted data is concentrated in $y_1$, exactly as the published Newton construction specifies.

The recovered kernel has log-RMSE 0.1392 against $1/\sqrt{\pi t}$ on 180 logarithmically spaced points from $t=0.05$ to $12$. This metric compares multiplicative shape error; it is not an uncertainty estimate.

![Published subdiffusion memory reproduction](../62%20Computational%20Labs/results/thermal_memory_reproduction/thermal_memory_reproduction.png)

## The structural mismatch is part of the result

The exact kernel diverges as $t\downarrow0$. The finite-state reconstruction is continuous and has

$$
\gamma_N(0)=b^Tc=3.94637.
$$

It therefore cannot converge pointwise to the target at the origin at fixed order. Its close VACF fit does not erase this representational mismatch. The result illustrates a recurring model-reduction lesson: an observed correlation can be approximated extremely well even when a latent kernel has the wrong local regularity.

The sampled positive-real diagnostic remains nonnegative on $10^{-5}\le\omega\le10^4$, with minimum $1.97\times10^{-7}$. This is a numerical screen, not an analytic proof over all frequencies.

The constructive thermal stage returns a positive-definite $\Sigma_0$ with minimum eigenvalue $5.66\times10^{-7}$. The Riccati residual is $3.62\times10^{-15}$ in Frobenius norm, and the full stationary Lyapunov residual is $1.59\times10^{-10}$. The regularized stochastic realization remains stable and has VACF RMSE $8.18\times10^{-4}$ on $[0,30]$. These residuals validate the algebraic construction for this numerical realization; they do not prove positive-realness symbolically.

The final Lanczos transform recovers $k=1.98655$ and the first couplings $T_{12}=+k$, $T_{21}=-k$ to $1.33\times10^{-15}$. Similarity error is $4.74\times10^{-13}$; the transformed kernel differs by at most $8.05\times10^{-9}$ and the transformed Lyapunov residual is $2.21\times10^{-10}$. Loss of biorthogonality is $1.17\times10^{-6}$ and produces maximum off-tridiagonal leakage $1.29\times10^{-5}$. This is a finite-precision tridiagonalization, not an exactly sparse symbolic matrix; the paper explicitly warns about this numerical failure mode.

## Published negative control

Bockius et al. report that their $\tau=1.0$, $n=6$ constrained approximation does not yield a positive-real transfer function. They also report that dropping the derivative constraint produces $\dot f(0)=-0.204$.

Our unconstrained Algorithm 2 realization gives

$$
\dot f(0)=A_{11}=-0.2042285,
$$

reproducing the reported rounded value. This is more informative than showing only the successful curve: coarse sampling loses the short-time structure needed by the smooth-at-origin constraint.

## Exact scope and omissions

This is a **method-faithful scoped reproduction**. It is not a reproduction of the authors' software, all six parameter choices, or their molecular-dynamics examples. These branches remain unimplemented here:

- deletion of spurious modes and duplication of negative-real discrete modes;
- tests on noisy molecular-dynamics data.

Because the primary case needs no spectral modification, it isolates the core algorithm without mode deletion or duplication. The final Lanczos coordinates have now been constructed and checked, including their small finite-precision leakage.

## Verification

Lab 27 passed **29 checks**. They cover independent target evaluation, moment identities, Newton convergence, pole admissibility, stability, dense VACF error, kernel shape, sampled positive-real behavior, Riccati and Lyapunov residuals, covariance positivity, Lanczos similarity and kernel invariance, and the published negative-control derivative.

From the computational-lab directory:

~~~powershell
python 27_thermal_memory_reproduction.py
~~~

[Program](../62%20Computational%20Labs/27_thermal_memory_reproduction.py) · [Protocol](../62%20Computational%20Labs/thermal_memory_reproduction_protocol.json) · [Results](../62%20Computational%20Labs/results/thermal_memory_reproduction/results.json) · [Arrays](../62%20Computational%20Labs/results/thermal_memory_reproduction/curves.npz)

## Next gate

Test the complete clean-case pipeline on noisy data not generated by the reconstruction code, including sampling/order sensitivity and positive-real failure rates. Only after that should the research branch compare memory uncertainty or propose an extension.

[[Computational Lab Index]] · [[Release Status and Next Work]] · [[Physics Worldmap]]
