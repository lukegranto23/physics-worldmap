---
type: computational-benchmark
field: Statistical Physics
epistemic_status: effective
level: advanced
tags: [anomalous-diffusion, memory-kernel, identifiability, information-theory, linear-response]
created: 2026-09-13
updated: 2026-09-14
note_maturity: expanded
source_audit: explicit-derivation-and-checked-computation-with-primary-prior-art
---

# Benchmark 011 — Finite Observations and Infinite-Time Claims

Two physically admissible memory models can have different infinite-time diffusion exponents while their finite sampled observations are arbitrarily hard to distinguish. This is not just a failure of our reconstruction algorithm: it persists when a statistical test receives the complete measured velocity vectors and knows both candidate models exactly.

For one computed example, 4,096 independent trajectories, each sampled 20 times, give a detection-power upper bound of about **5.96% at a 5% false-positive limit**. One model is asymptotically subdiffusive; the other eventually diffuses normally. This is an information limit under a stated idealized experiment, not a measured detector success rate or a claim that real materials are unknowable.

The tempered physical model and crossover are established prior art. The finite-window estimate below is our explicit derivation using standard convolution and statistical-distance arguments. No novelty claim is made.

[[Benchmark 010 — Noisy Memory and the Prediction Horizon]] · [[Finite Memory and the Return to Normal Diffusion]] · [[Research Frontier — Identifiability Before Discovery]]

## 1. Change the physical model, not the fitting method

Use a free, linear generalized Langevin model in dimensionless units with mass, thermal energy, and fractional friction scale equal to one. Let its causal friction kernel be

$$
\gamma_\epsilon(t)=\frac{e^{-\epsilon t}}{\sqrt{\pi t}},\qquad t>0,\quad\epsilon\ge0.
$$

Assume a stationary, Gaussian equilibrium velocity process. The fluctuation-dissipation relation and equilibrium preparation give its normalized velocity autocorrelation through

$$
\widetilde\gamma_\epsilon(s)=(s+\epsilon)^{-1/2},\qquad
\widetilde C_\epsilon(s)=\frac{1}{s+(s+\epsilon)^{-1/2}}.
$$

The square root uses its principal branch. Gaussianity is an additional model assumption, not a consequence of the fluctuation-dissipation relation alone. The singular kernel represents a generalized thermal force, not a force with finite instantaneous variance; the velocity variance is finite and equals one.

The exponential cutoff is not introduced here as a new mechanism. Goychuk's 2009 paper gives the shifted fractional-friction transform; Goychuk and Pöschel's 2020 paper explicitly studies the exponentially tempered kernel and the free-system crossover toward ordinary diffusion. We specialize that known family to exponent one-half and no spatial potential. [Goychuk, Section II.1](https://arxiv.org/html/0905.0826#S2.SS1); [Goychuk and Pöschel, Section 2, Eq. 1 and following](https://arxiv.org/html/2009.04896#S2)

For no cutoff,

$$
C_0(t)=E_{3/2}(-t^{3/2}),\qquad
\operatorname{MSD}_0(t)=2t^2 E_{3/2,3}(-t^{3/2})
\sim\frac{4\sqrt t}{\sqrt\pi}.
$$

For every fixed positive cutoff, the velocity correlation is integrable and

$$
D_\epsilon=\int_0^\infty C_\epsilon(t)\,dt
=\widetilde C_\epsilon(0)=\sqrt\epsilon>0,
\qquad \operatorname{MSD}_\epsilon(t)\sim2\sqrt\epsilon\,t.
$$

The memory cutoff timescale is $1/\epsilon$; this is not an exact threshold at which a fitted transport exponent suddenly changes. The limiting MSD exponent jumps from $1/2$ to $1$ at zero cutoff. The diffusion coefficient itself is **continuous**, since $D_\epsilon\to0=D_0$. There is no arbitrarily large absolute DC-mobility discrepancy as $\epsilon\downarrow0$.

## 2. A finite-window continuity bound

For every fixed $T$, the kernel discrepancy satisfies

$$
\int_0^T |\gamma_0(u)-\gamma_\epsilon(u)|\,du
\le \frac{\epsilon}{\sqrt\pi}\int_0^T u^{1/2}\,du
=\frac{2\epsilon T^{3/2}}{3\sqrt\pi},
$$

using $0\le1-e^{-\epsilon u}\le\epsilon u$.

An explicit correlation bound follows without solving the dynamics. Subtract the two Laplace-domain resolvents:

$$
\widetilde C_\epsilon-\widetilde C_0
=\widetilde C_\epsilon\widetilde C_0
(\widetilde\gamma_0-\widetilde\gamma_\epsilon).
$$

In time, this is the causal triple convolution

$$
C_\epsilon-C_0=C_\epsilon*C_0*(\gamma_0-\gamma_\epsilon).
$$

Every normalized stationary autocorrelation obeys $|C(t)|\le1$. Therefore $|(C_\epsilon*C_0)(v)|\le v$, and

$$
\begin{aligned}
|C_\epsilon(t)-C_0(t)|
&\le\int_0^t(t-u)(\gamma_0(u)-\gamma_\epsilon(u))\,du\\
&\le\frac{\epsilon}{\sqrt\pi}\int_0^t(t-u)u^{1/2}\,du
=\frac{4\epsilon t^{5/2}}{15\sqrt\pi}.
\end{aligned}
$$

Thus $C_\epsilon\to C_0$ uniformly on every fixed finite window. This bound is intentionally conservative at large times and does not locate the crossover precisely. Uniform convergence on each bounded window does not imply uniform agreement on the whole half-line.

## 3. From close correlations to a limit on every test

Choose $n$ distinct observation times in a window of span $T$. An observed equilibrium trajectory vector has law

$$
P_\epsilon=N(0,K_\epsilon),\qquad
(K_\epsilon)_{ij}=C_\epsilon(|t_i-t_j|).
$$

The zero-cutoff covariance $K_0$ is strictly positive definite. One way to see this is to use the velocity spectrum $S_0(\omega)=2\operatorname{Re}\widetilde C_0(i\omega)$, which is positive for every nonzero frequency. A nonzero linear combination of distinct-time samples has a nonzero exponential polynomial in frequency, hence strictly positive variance when integrated against that spectrum. Numerical positive definiteness is also checked for the concrete schedule below.

For $M$ independent trajectory vectors, define the whitened covariance difference

$$
A=K_0^{-1/2}(K_\epsilon-K_0)K_0^{-1/2}.
$$

Taking the Gaussian log-density ratio and its expectation gives

$$
\begin{aligned}
\mathcal K_M
&=D_{\rm KL}(P_\epsilon^{\otimes M}\Vert P_0^{\otimes M})\\
&=\frac M2\left[\operatorname{tr}(K_0^{-1}K_\epsilon)-n
-\log\det(K_0^{-1}K_\epsilon)\right]\\
&=\frac M2\left[\operatorname{tr}A-\log\det(I+A)\right].
\end{aligned}
$$

KL uses natural logarithms and is directed from the positive-cutoff alternative to the zero-cutoff null. Independent repetitions multiply KL by $M$; the $n$ samples within a trajectory remain correlated.

For any possibly randomized test $0\le\phi\le1$ with $E_0\phi\le\alpha$,

$$
E_\epsilon\phi
\le\min\left\{1,\alpha+\operatorname{TV}(P_\epsilon^{\otimes M},P_0^{\otimes M})\right\}
\le\min\left\{1,\alpha+\sqrt{\mathcal K_M/2}\right\}.
$$

Here total variation is half the density $L_1$ distance. The last step is the standard Pinsker inequality. [Canonne, Section 1, Lemma 2](https://arxiv.org/html/2202.07198#S1)

The finite-window estimate makes the limit quantitative. Put $b=4/(15\sqrt\pi)$ and $\lambda=\lambda_{\min}(K_0)>0$. Then

$$
\|A\|_F\le\frac{n b\epsilon T^{5/2}}{\lambda}.
$$

For $\|A\|_2\le r<1$, integrating $a/(1+a)$ bounds each eigenvalue contribution by $a-\log(1+a)\le a^2/[2(1-r)]$. Hence

$$
\mathcal K_M\le\frac{M\|A\|_F^2}{4(1-r)}.
$$

In particular, once $\|A\|_2\le1/2$,

$$
\operatorname{TV}(P_\epsilon^{\otimes M},P_0^{\otimes M})
\le\frac{\sqrt M\,n b\epsilon T^{5/2}}{2\lambda}.
$$

For any **fixed finite** schedule and finite number of independent repetitions, test power therefore approaches its null rejection probability as $\epsilon\downarrow0$. There is no test whose power is uniformly separated above its size against *every* positive cutoff. This statement does not say that a specified nonzero cutoff remains undetectable as observation resources increase.

## 4. Concrete calculation on the existing observation schedule

Lab 30 uses the same observation times as the noisy reconstruction study: $0,0.6,\ldots,11.4$, giving 20 velocities per trajectory. It evaluates exact population covariances, not fitted matrices or randomly generated estimates. The null covariance has minimum eigenvalue 0.0935900.

The following bounds use $M=4096$ independent trajectories and $\alpha=0.05$. They give the test the full 81,920 scalar velocity readings, their grouping into trajectories, and exact knowledge of both models.

| Positive cutoff $\epsilon$ | Memory timescale $1/\epsilon$ | Largest sampled covariance difference | KL per trajectory | Detection-power upper bound |
|---:|---:|---:|---:|---:|
| $10^{-5}$ | 100,000 | $4.91694\times10^{-6}$ | $4.54501\times10^{-10}$ | 5.0965% |
| $10^{-4}$ | 10,000 | $4.91661\times10^{-5}$ | $4.54306\times10^{-8}$ | 5.9646% |
| $10^{-3}$ | 1,000 | $4.91329\times10^{-4}$ | $4.52361\times10^{-6}$ | 14.6251% |
| $10^{-2}$ | 100 | $4.88038\times10^{-3}$ | $4.33755\times10^{-4}$ | 99.2513% |
| $10^{-1}$ | 10 | $4.57178\times10^{-2}$ | $3.05817\times10^{-2}$ | 100% (uninformative) |

A low upper bound constrains every test in this experiment, including an oracle likelihood-ratio test. A large upper bound does not establish that any test achieves high power. These are analytic inequalities evaluated numerically, not Monte Carlo confidence intervals or interval-arithmetic certificates.

Any decision using only the normalized VACF estimates from Benchmark 010 is also a decision based on these complete vectors. Compressing the data cannot evade the bound. Adding parameter uncertainty or independent sensor noise cannot make this particular pair easier to distinguish under the same observations.

![Finite observations and infinite-time transport](../62%20Computational%20Labs/results/tempered_memory_boundary/tempered_memory_boundary.png)

The low-frequency mobility panel shows the known difference between $\chi_0(\omega)\to0$ and $\chi_\epsilon(\omega)\to\sqrt\epsilon$ as frequency decreases. It is an all-time stationary-response calculation, not a claim that this limit has been measured within the short trajectory window.

## 5. A bounded forced probe does not remove the limiting ambiguity

For an additive predetermined force $f$ applied starting at time zero, the mean velocity is $\mu_\epsilon=C_\epsilon*f$. The centered thermal covariance is unchanged in this linear model. If $\|f\|_{L^1[0,T]}\le B$, then

$$
\|\mu_\epsilon-\mu_0\|_{\infty,[0,T]}
\le b\epsilon T^{5/2}B.
$$

The Gaussian KL for sampled driven velocities acquires the extra term

$$
\frac M2(\mu_\epsilon-\mu_0)^T K_0^{-1}(\mu_\epsilon-\mu_0),
$$

which also vanishes for fixed finite resources as $\epsilon\downarrow0$. This is a derived extension, not a simulated forced experiment in Lab 30. It covers predetermined deterministic forcing, not arbitrary feedback policies or ideal continuous observation.

Forcing can still improve sensitivity to a specified cutoff. What fails is the promise to identify arbitrarily distant crossover behavior with a uniformly reliable, fixed finite experiment.

## 6. Numerical method and independent checks

Write $z=\sqrt{s+\epsilon}$. Then

$$
\widetilde C_\epsilon(s)=\frac{z}{z^3-\epsilon z+1}.
$$

For the simple cubic roots $r_j$, set $a_j=r_j/(3r_j^2-\epsilon)$. Partial fractions and the inverse transform of $1/(\sqrt{s}-r)$ give

$$
C_\epsilon(t)=e^{-\epsilon t}\sum_{j=1}^3 a_j r_j
\operatorname{erfcx}(-r_j\sqrt t).
$$

The apparent $t^{-1/2}$ terms cancel because $\sum a_j=0$; the initial variance is $\sum a_jr_j=1$. The implementation restricts the cutoff domain to $0\le\epsilon\le0.1$, covering the declared examples and avoiding unvalidated root-degeneracy cases.

To avoid cancellation in a very small KL, the code uses eigenvalues $a_j$ of the Cholesky-whitened covariance difference and a small-argument series for $a_j-\log(1+a_j)$. Direct trace/log-determinant and generalized-eigenvalue formulas provide independent numerical comparisons.

All **16 verification groups passed**. These include the initial conditions, root residuals, conjugate cancellation, zero-cutoff agreement with the earlier independent pole-and-cut quadrature, the Volterra convolution equation, a numerical Laplace-transform check, analytic versus finite-difference derivatives, positive covariance matrices, three KL calculations, and the DC mobility identities.

The maximum checked Volterra residual was $2.45\times10^{-15}$ rounded upward; the checked Laplace-transform discrepancy was below $1.36\times10^{-14}$. Sampled agreement with the finite-window inequality is an implementation check; the convolution argument supplies the proof between grid points.

A separate September 14 audit passed eight additional groups. It evaluates six declared correlation cases through a termwise inverse-Laplace series with 80-digit Decimal arithmetic, without using cubic roots or special functions in the reference calculation. Increasing both truncation limits and then precision to 100 digits checked numerical convergence. Its largest discrepancy from Lab 30 was below $1.17\times10^{-15}$, including the case $\epsilon=0.1$, $t=50$. Analytic covariance examples check both KL directions and noncommuting whitening; high-precision logarithms check cancellation handling. These finite checks are not rigorous interval enclosures or experimental validation.

The protocol was written **after preliminary calculations**. It is an exploratory specification, not a preregistration. No detector was trained, no Monte Carlo sample was selected, and these parameter values are not held-out discovery cases.

## 7. What this changes about the research program

Benchmark 010 showed that a finite reconstruction can change the eventual transport law. This benchmark separates that approximation artifact from a more fundamental issue: even within an established physical family, finite data may not settle the asymptotic law.

The next defensible target is therefore a **finite-time, finite-frequency prediction region with explicit structural assumptions**. It should state which cutoffs remain consistent with the data and how that uncertainty affects displacement or response within a declared domain. A physical lower bound on a cutoff, longer observation, or independent knowledge of the bath changes the problem and must be stated.

The planned comparison still needs the complete published spectral-repair baseline, a fractional model, and a tempered model receiving identical observations. A spread across a finite candidate list is not automatically a confidence bound over all admissible systems. Nonlinear transfer and published experimental data remain unfinished.

The present result is not an impossibility theorem for noiseless continuous trajectories, exact correlation oracles, all possible physical model classes, or all experimental designs. Nor does it certify a new physical mechanism or a novel statistical theorem. Its contribution to this vault is a reproducible, assumption-explicit connection between memory cutoffs, long-time transport, and finite observational evidence.

## Reproducible assets

From the computational-lab directory, run:

~~~powershell
python 30_tempered_memory_boundary.py
python audit_tempered_memory_boundary.py
~~~

[Exploratory protocol](../62%20Computational%20Labs/tempered_memory_boundary_protocol.json) · [Full calculations and checks](../62%20Computational%20Labs/results/tempered_memory_boundary/results.json) · [Covariances, correlations, and mobilities](../62%20Computational%20Labs/results/tempered_memory_boundary/curves_and_covariances.npz) · [Executable calculation](../62%20Computational%20Labs/30_tempered_memory_boundary.py)

[Independent audit source](../62%20Computational%20Labs/audit_tempered_memory_boundary.py) · [High-precision audit and refinement results](../62%20Computational%20Labs/results/tempered_memory_boundary/independent_audit.json)

The results preserve the script, protocol, independent reference, and array-file hashes plus library versions. No noisy reconstruction needs to be rerun for this calculation.

[[Benchmark 005 — Information Limits and Better Measurements]] · [[Computational Lab Index]] · [[Synthesis Lab]] · [[Release Status and Next Work]] · [[Physics Worldmap]]
