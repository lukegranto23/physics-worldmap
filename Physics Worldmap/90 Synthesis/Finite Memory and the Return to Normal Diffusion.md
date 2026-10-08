---
type: research-derivation
field: Statistical Physics
epistemic_status: established
level: advanced
tags: [generalized-langevin, anomalous-diffusion, memory-kernel, model-reduction, linear-response, asymptotics]
created: 2026-09-12
updated: 2026-09-13
source_audit: derived-with-primary-prior-art
note_maturity: expanded
---

# Finite Memory and the Return to Normal Diffusion

An accurate finite-time approximation to fractional subdiffusion can eventually become normally diffusive. For a fixed, finite, stable thermal realization with a stable auxiliary block, that crossover follows from its nonzero zero-frequency mobility. It can occur far beyond the window over which the model was fitted or intended to operate.

This is an established consequence of a finite memory cutoff, not a new discovery or a contradiction of the cited reconstruction method. Goychuk explicitly discusses eventual normal diffusion for a finite exponential approximation, including a case whose crossover lies far beyond the reported simulations. The value of the present derivation is to state the conditions precisely and turn them into validation questions. [Goychuk 2009, Section II and Appendix A](https://arxiv.org/html/0905.0826#A1)

[[Benchmark 009 — Published Subdiffusion Memory Reproduction]] · [[Correlation-to-Memory Reconstruction from a VACF]] · [[Research Frontier — Identifiability Before Discovery]]

## 1. Observable and normalization

Use reduced units with inverse temperature and mass $\beta=m=1$, so an equilibrium velocity has variance one. Let $V(t)$ be a zero-mean stationary velocity, and define

$$
C(t)=\langle V(t)V(0)\rangle,
\qquad C(0)=1,
\qquad X(t)-X(0)=\int_0^t V(u)\,du.
$$

The position is an integrated velocity in a free translational coordinate; its distribution need not be stationary. Its mean squared displacement is

$$
M(t)=\left\langle [X(t)-X(0)]^2\right\rangle
=2\int_0^t(t-u)C(u)\,du.
$$

Consequently,

$$
\widetilde M(s)=\frac{2\widetilde C(s)}{s^2},
\qquad \operatorname{Re}s>0.
$$

These relations require stationary velocity statistics, not a positive correlation at every time. Anticorrelations are allowed. They agree with the normalized correlation and displacement relations in [Goychuk 2009, Appendix A, equations 15–18](https://arxiv.org/html/0905.0826#A1).

## 2. The exact fractional target

For the target used in [[Benchmark 009 — Published Subdiffusion Memory Reproduction]],

$$
\gamma_*(t)=\frac{1}{\sqrt{\pi t}},
\qquad
\widetilde\gamma_*(s)=s^{-1/2},
$$

with the principal square-root branch in the right half-plane. The normalized correlation obeys

$$
\widetilde C_*(s)
=\frac{1}{s+s^{-1/2}}
=\frac{s^{1/2}}{s^{3/2}+1},
\qquad
C_*(t)=E_{3/2,1}(-t^{3/2}).
$$

The two-parameter Mittag–Leffler function is

$$
E_{a,b}(z)=\sum_{k=0}^{\infty}\frac{z^k}{\Gamma(ak+b)}.
$$

Using its Laplace transform gives the exact displacement formula

$$
\widetilde M_*(s)=\frac{2s^{-3/2}}{s^{3/2}+1},
\qquad
M_*(t)=2t^2E_{3/2,3}(-t^{3/2}).
$$

At short times $M_*(t)\sim t^2$, consistent with a finite equilibrium velocity variance. On the negative real axis, the leading algebraic Mittag–Leffler asymptotic yields

$$
E_{3/2,3}(-t^{3/2})
\sim\frac{t^{-3/2}}{\Gamma(3/2)},
$$

and therefore

$$
\boxed{M_*(t)\sim\frac{4\sqrt t}{\sqrt\pi}\quad(t\to\infty).}
$$

This explicit inversion justifies the result without applying an unqualified Tauberian argument to a sign-changing correlation. In the same limit,

$$
C_*(t)\sim-\frac{1}{2\sqrt\pi\,t^{3/2}},
\qquad
\int_0^\infty C_*(t)\,dt=\widetilde C_*(0)=0.
$$

The correlation is absolutely integrable, but its absolute first time moment is not. Thus zero asymptotic diffusion coefficient does not imply bounded displacement: the persistent anticorrelation tail produces the $\sqrt t$ growth.

## 3. A precise finite-realization proposition

Consider a finite real matrix of the form

$$
A_\delta=
\begin{bmatrix}
-\delta & b^T\\
-c & A_0
\end{bmatrix},
$$

where $b,c$ are real vectors. The small $\delta>0$ used in numerical thermal realizations is allowed; the argument also works for $\delta=0$ when the conditions below hold.

Assume:

1. Both $A_\delta$ and $A_0$ are Hurwitz: every eigenvalue has strictly negative real part.
2. The Ornstein–Uhlenbeck system $dY=A_\delta Y\,dt+G\,dW$ has its zero-mean stationary initialization with finite covariance $\Sigma$ satisfying

$$
\Sigma\succeq0,
\qquad
A_\delta\Sigma+\Sigma A_\delta^T=-GG^T,
\qquad
\Sigma e_1=e_1.
$$

3. The resolved velocity is $V=e_1^TY$ and position is its time integral as in Section 1.

The covariance conditions encode the required normalization and lack of instantaneous equilibrium covariance between the resolved velocity and auxiliaries. Strict positivity of $\Sigma$ and controllability of every auxiliary coordinate are not additional requirements for the following scalar conclusion.

Stationarity gives

$$
C(t)=e_1^Te^{tA_\delta}\Sigma e_1
=e_1^Te^{tA_\delta}e_1,
$$

and hence

$$
\widetilde C(s)
=e_1^T(sI-A_\delta)^{-1}e_1
=\frac{1}{s+\delta+\kappa(s)},
\qquad
\kappa(s)=b^T(sI-A_0)^{-1}c.
$$

This block realization and compatible stationary covariance are the framework used by [Bockius et al. 2021, Section 2.2 and Appendix C](https://arxiv.org/html/2101.02657#A3). The following asymptotic proof is an explicit deduction for that framework.

### Finite and strictly positive diffusion coefficient

Since $A_0$ is Hurwitz it is invertible, and

$$
\kappa_0=b^T(-A_0)^{-1}c
$$

is finite. The Schur complement identity at $s=0$ gives

$$
\det(-A_\delta)=\det(-A_0)(\delta+\kappa_0).
$$

For any finite real Hurwitz matrix $B$, $\det(-B)>0$: its negative real eigenvalues contribute positive factors to $\det(-B)$, and its nonreal eigenvalues occur in conjugate pairs with positive product. Therefore

$$
\delta+\kappa_0
=\frac{\det(-A_\delta)}{\det(-A_0)}>0.
$$

It follows that

$$
\boxed{
D=\int_0^\infty C(u)\,du
=-e_1^TA_\delta^{-1}e_1
=\frac{1}{\delta+\kappa_0}>0.
}
$$

The determinant proof does not assume the memory kernel is pointwise positive. Stability establishes the algebraic sign; the stationary covariance conditions establish that $C$ is the correlation of the specified physical stochastic model. The determinants are useful for the proof, not the recommended numerical route: compute $D$ through linear solves.

### Long-time displacement

Finite-dimensional Hurwitz dynamics decay exponentially, possibly multiplied by a polynomial if the matrix has nontrivial Jordan blocks. Both $\int_0^\infty|C(u)|\,du$ and $\int_0^\infty u|C(u)|\,du$ are finite. Thus

$$
M(t)=2Dt-2\int_0^\infty uC(u)\,du+o(1)
=2Dt+O(1).
$$

More explicitly, $\int_0^\infty ue^{uA_\delta}\,du=A_\delta^{-2}$, so the constant term is $-2e_1^TA_\delta^{-2}e_1$. Consequently,

$$
\boxed{M(t)\sim2Dt\quad(t\to\infty),\qquad D>0.}
$$

The exact fractional target and each fixed finite model in this class have different eventual growth laws, even when their correlations agree very well on the measured interval.

## 4. Exceptions and the order of limits

The proposition is not a statement about every finite stochastic model.

- If $A_0$ is singular, zero diffusion is possible even with stable $A_\delta$. A confined oscillator has $A=[-\gamma,-\omega_0^2;1,0]$, with $\gamma,\omega_0>0$, and velocity transform $s/(s^2+\gamma s+\omega_0^2)$. Its integrated velocity is a bounded stationary-position difference at long times; here the auxiliary block is zero and the proposition does not apply.
- If the full matrix is not Hurwitz, undamped or zero modes can sustain correlations and produce other behavior, including ballistic contributions. Invertibility alone does not replace decay.
- Without the stationary covariance normalization, the resolvent entry need not equal the measured velocity correlation. A good deterministic response fit does not by itself supply a thermal noise model.
- Infinite-dimensional models or parameter limits that move poles toward zero can retain a power-law tail. A statement for each fixed finite model is not uniform in such limits.

For clarity, suppose a sequence of admissible finite models satisfies $M_N(t)\to M_*(t)$ for every fixed $t>0$. This convergence is an assumption about the approximation sequence, not something guaranteed by increasing the fitted order. For each fixed $N$, however,

$$
\frac{M_N(t)}{M_*(t)}
\sim\frac{D_N\sqrt\pi}{2}\sqrt t\longrightarrow\infty.
$$

Therefore the two iterated limits of this ratio differ:

$$
\lim_{t\to\infty}\lim_{N\to\infty}\frac{M_N(t)}{M_*(t)}=1,
\qquad
\lim_{N\to\infty}\lim_{t\to\infty}\frac{M_N(t)}{M_*(t)}=\infty.
$$

Making the approximation more accurate can push the crossover outward without removing it for a fixed model. Reducing the numerical regularization $\delta$ alone also does not remove the mismatch if $A_0$ stays stable and $\kappa_0$ stays finite and nonzero.

## 5. What to validate in practice

Specify the intended time horizon and forcing-frequency range before evaluating a model. A finite approximation may be entirely useful on that domain. Report performance there separately from extrapolation toward zero frequency or arbitrarily late time.

For an additive force on the resolved velocity and the convention $F(t)=\operatorname{Re}(F_0e^{i\omega t})$, the stationary linear mobility in these units is

$$
\chi(\omega)=\widetilde C(i\omega)
=\frac{1}{i\omega+\delta+\kappa(i\omega)}.
$$

The fractional target has $\chi_*(\omega)\sim(i\omega)^{1/2}\to0$ as $\omega\to0^+$, whereas the finite model has $\chi(0)=D>0$. Measure complex mobility error, amplitude and phase error on declared bands, alongside displacement error on declared horizons. Use the regularized matrix for both thermal validation and these predictions.

The response error obeys the exact identity

$$
\chi-\chi_*
=-\chi\chi_*\left[(\delta+\kappa)-\kappa_*\right],
$$

where the transforms are evaluated at the same frequency. This weighting explains why an error in the inferred memory need not have the same practical importance at every frequency. Report the implied $D$ and long-time growth law as structural properties, without treating those properties as evidence of error within an untested finite operating window.

For noisy inference, keep model rejection rates and conditional prediction errors visible, and evaluate predictions on data or analytic frequencies excluded from fitting and model selection. Equilibrium linear response is already fixed by an exact all-time VACF; its role here is to test finite-data prediction and expose unsupported extrapolation. It does not add an independent physical law.

## Sources and scope

- Igor Goychuk, *Viscoelastic subdiffusion: from anomalous to normal*, Physical Review E **80**, 046125 (2009). [Open manuscript](https://arxiv.org/html/0905.0826), [DOI](https://doi.org/10.1103/PhysRevE.80.046125). Section II describes exponential memory and its low-frequency cutoff; Appendix A connects correlation to displacement and discusses eventual normal diffusion of the finite approximation.
- N. Bockius, J. Shea, G. Jung, F. Schmid, M. Hanke, *Model reduction techniques for the computation of extended Markov parameterizations for generalized Langevin equations* (2021). [Open manuscript](https://arxiv.org/html/2101.02657), [DOI](https://doi.org/10.1088/1361-648X/abe6df). The relevant ingredients are the subdiffusion target, block realization, stationary covariance, and regularized thermal construction.

This note supplies algebra and a validation criterion. It contains no new empirical result and makes no novelty claim for the finite-memory crossover.

## Connected calculations

[[Benchmark 010 — Noisy Memory and the Prediction Horizon]] evaluates displacement and force-response errors for the reproduced finite models. [[Benchmark 011 — Finite Observations and Infinite-Time Claims]] asks a distinct question: whether finite sampled observations can distinguish an actual physical memory cutoff from an infinite power-law tail.

[[Computational Lab Index]] · [[Synthesis Lab]] · [[Physics Worldmap]]
