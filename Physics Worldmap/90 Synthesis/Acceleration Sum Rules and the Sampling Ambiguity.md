---
type: research-derivation
field: Statistical Physics
epistemic_status: established
level: advanced
tags: [generalized-langevin, fluctuation-dissipation, spectral-measures, aliasing, uncertainty-quantification, linear-response]
created: 2026-09-15
updated: 2026-09-16
source_audit: derived-with-primary-prior-art
note_maturity: expanded
---

# Acceleration Sum Rules and the Sampling Ambiguity

Equally spaced velocity observations need not determine even a finite-time displacement response. This remains true within stable, passive, free thermal models. Knowing the velocity variance and imposing fluctuation–dissipation consistency do not remove the ambiguity. An additional bound on acceleration variance restricts the unresolved high-frequency motion and permits useful, explicitly conditional response bounds.

The statements below are mathematical consequences of the stated effective-model assumptions, not a proposed new physical law. Spectral moment optimization and its function-majorant dual are established prior art. The research question is whether specific, independently justified physical information makes the resulting displacement bounds useful at an experimentally relevant prediction horizon. [Karlsson and Georgiou, *Uncertainty Bounds for Spectral Estimation*, equations 5–7](https://people.kth.se/~johan79/papers/KGTACversion_2submitted.pdf)

[[Benchmark 012 — Acceleration Information and Certified Displacement]] · [[Benchmark 011 — Finite Observations and Infinite-Time Claims]] · [[Prior Art — Spectral Bounds and Physical Response]]

## 1. Observable, normalization, and model class

Use units with mass and inverse temperature equal to one. Let $V(t)$ be a real, zero-mean stationary velocity with $C(0)=1$ and a probability spectral measure on nonnegative angular frequencies:

$$
C(t)=\mathbb E[V(t)V(0)]
=\int_0^\infty\cos(\omega t)\,\rho(d\omega),
\qquad \rho\geq0,
\qquad \int\rho(d\omega)=1.
$$

For $X(T)-X(0)=\int_0^T V(t)\,dt$, define

$$
J(T)=\int_0^T(T-t)C(t)\,dt
=\int_0^\infty g_T(\omega)\,\rho(d\omega),
$$

$$
g_T(\omega)=\frac{1-\cos(\omega T)}{\omega^2},
\qquad g_T(0)=\frac{T^2}{2}.
$$

The mean squared displacement is $2J(T)$. In an equilibrium model satisfying the corresponding linear-response fluctuation–dissipation relation, $J(T)$ is also the mean displacement response per unit constant force switched on at time zero. The response interpretation requires that physical response assumption; the covariance identity for the mean squared displacement does not.

The initial data are $c_k=C(k\Delta)$, $k=0,\ldots,n$, or simultaneous uncertainty intervals for them. The spectral optimization class can include nonmixing or nondiffusive processes as well as free diffusive ones. Bounds over this larger class are conservative for any physical subclass contained in it; extremal spectra must not automatically be described as stable finite-dimensional Langevin realizations.

## 2. Exact aliasing survives free passive thermal dynamics

Fix $a>0$ and an integer $q\geq0$. Let

$$
b_q=\frac{2\pi q}{\Delta},
\qquad C_q(t)=e^{-a|t|}\cos(b_qt).
$$

Every model has exactly the same complete lattice covariance sequence:

$$
C_q(k\Delta)=e^{-a|k|\Delta}
\quad\text{for every integer }k.
$$

These are not merely abstract positive-definite functions. Take the free position $dX=V\,dt$ and the equilibrium Ornstein–Uhlenbeck velocity–auxiliary system

$$
d\begin{pmatrix}V\\Y\end{pmatrix}
=\begin{pmatrix}-a&-b_q\\b_q&-a\end{pmatrix}
\begin{pmatrix}V\\Y\end{pmatrix}dt
+\sqrt{2a}\,d\begin{pmatrix}W_1\\W_2\end{pmatrix},
$$

with independent Wiener processes and initial covariance $I$. Its drift eigenvalues are $-a\pm ib_q$, and its stationary covariance solves $AI+IA^\mathsf T=-2aI$. There is no confining force on $X$.

Equilibrium here refers to the stationary thermal velocity–auxiliary variables. A free position on the whole real line has no normalizable stationary spatial law. The skew coupling is compatible with generalized time reversal taking $V$ odd and $Y$ even; an antisymmetric drift alone is not evidence of thermodynamic driving.

Eliminating $Y$ gives an instantaneous friction coefficient $a$ plus an exponential memory kernel $b_q^2e^{-at}$. Equivalently, the causal velocity admittance and friction transform are

$$
\chi_q(s)=\frac{s+a}{(s+a)^2+b_q^2},
\qquad \widetilde\gamma_q(s)
=\frac1{\chi_q(s)}-s
=a+\frac{b_q^2}{s+a}.
$$

The friction transform is positive real for $\operatorname{Re}s>0$. The eliminated noise has the equilibrium white contribution with covariance $2a\delta(t-t')$ and the independent colored contribution with covariance $b_q^2e^{-a|t-t'|}$. Thus the model has the required thermal noise–friction relation. Expressing the instantaneous term as a friction coefficient avoids endpoint conventions for a delta-function memory kernel.

All models retain unit velocity variance, unit high-frequency inertial normalization $\chi_q(s)\sim1/s$, the same instantaneous friction $a$, and a strictly positive diffusion coefficient

$$
D_q=\chi_q(0)=\frac{a}{a^2+b_q^2}>0.
$$

Nevertheless, with $z_q=a-ib_q$,

$$
J_q(T)=\operatorname{Re}\left[
\frac{T}{z_q}-\frac{1-e^{-z_qT}}{z_q^2}
\right],
$$

$$
0\leq J_q(T)\leq\frac{aT+2}{a^2+b_q^2}
\longrightarrow0\qquad(q\longrightarrow\infty)
$$

for every fixed $T>0$. The model $q=0$ instead has

$$
J_0(T)=\frac{T}{a}-\frac{1-e^{-aT}}{a^2}>0.
$$

Because these processes are Gaussian, equality of the lattice covariance sequences also gives equality of every finite-dimensional sampled trajectory distribution. Increasing the number of trajectories, or the number of observations on the same exact time lattice, cannot distinguish this family. This is a sampling counterexample, not a statement that all real experiments have this ambiguity: off-lattice timing, sensor filtering information, acceleration observations, or additional justified physical restrictions can distinguish it.

This family has a white-noise term in $dV$ and infinite acceleration variance. It therefore does **not** satisfy the finite-acceleration assumption introduced next. That is precisely the extra information being tested, not a defect to conceal in the comparison.

## 3. A finite-acceleration thermal target

For $\kappa>0$ and $\nu>0$, consider the free exponential-memory model

$$
\gamma(t)=\kappa e^{-\nu t},
\qquad
\chi(s)=\frac{s+\nu}{s^2+\nu s+\kappa}.
$$

A thermal realization is

$$
dX=V\,dt,\qquad dV=-Y\,dt,
\qquad dY=(\kappa V-\nu Y)\,dt+\sqrt{2\kappa\nu}\,dW.
$$

The stationary covariance of $(V,Y)$ is $\operatorname{diag}(1,\kappa)$, and the drift is Hurwitz. The velocity covariance obeys

$$
C''+\nu C'+\kappa C=0,
\qquad C(0)=1,\qquad C'(0)=0.
$$

Its one-sided spectral density is

$$
\rho(\omega)=\frac{2}{\pi}
\frac{\kappa\nu}{(\kappa-\omega^2)^2+\nu^2\omega^2},
\qquad \omega\geq0,
$$

and its sum rules and diffusion coefficient are

$$
\int_0^\infty\rho(\omega)\,d\omega=1,
\qquad
\int_0^\infty\omega^2\rho(\omega)\,d\omega
=-C''(0)=\mathbb E[\dot V^2]=\kappa,
\qquad D=\frac\nu\kappa.
$$

Here $\dot V=-Y$ exists in mean square; the second spectral moment is finite, although the fourth is not. The formulas follow directly from the displayed realization and from $(2/\pi)\operatorname{Re}\chi(i\omega)$. The covariance-to-memory identity $\widetilde\gamma=1/\widetilde C-s$ is the normalized scalar Mori relation. [*Analysis of the Dynamics in Linear Chain Models by means of Generalized Langevin Equations*, equations 11–12](https://link.springer.com/article/10.1007/s10955-024-03274-z)

For inference, knowing $\mathbb E[\dot V^2]\leq K$ is **additional physical information**. It is not a consequence of $C(0)=1$, Gaussianity, stationarity, or fluctuation–dissipation alone. A synthetic experiment may deliberately supply the true $K$ as an oracle prior, but must label that choice. A physical experiment needs a justified force-variance bound or an acceleration measurement with its own uncertainty. Reusing a fitted model's acceleration variance as if it were independently established would make the test circular.

Statistical independence of the acceleration and covariance measurements is not mandatory if their uncertainty statements have valid joint coverage. What is mandatory is an honestly justified joint information set.

In particular, a finite-difference acceleration is not automatically such an upper bound. Its variance is $2[1-C(h)]/h^2=\int 2[1-\cos(\omega h)]/h^2\,\rho(d\omega)\le\int\omega^2\rho(d\omega)$. A confidence upper limit for this finite-difference variance is an upper limit for a generally smaller quantity. Bandwidth or independent force/acceleration information must justify any transfer to instantaneous acceleration variance.

### A stronger alias family with finite acceleration

The ambiguity does not depend on the white noise in the earlier velocity equation. Write $a=\sqrt\kappa$, let $b_q=2\pi q/\Delta$, and define

$$
A_q=\begin{pmatrix}0&-a\\a&-\nu\end{pmatrix}\otimes I_2
+I_2\otimes\begin{pmatrix}0&-b_q\\b_q&0\end{pmatrix}.
$$

Observe the first coordinate of $dZ=A_qZ\,dt+G\,dW$, with $GG^T=\operatorname{diag}(0,0,2\nu,2\nu)$ and stationary covariance $I_4$. The full drift is Hurwitz and $A_q+A_q^T+GG^T=0$. The parity matrix $E=\operatorname{diag}(-1,1,1,-1)$ satisfies $EA_qE=A_q^T$, giving the appropriate equilibrium time-reversal symmetry with the observed velocity odd.

The Kronecker terms commute, so the covariance is

$$
C_q(t)=C_{\rm base}(t)\cos(b_qt),\qquad
C_q(k\Delta)=C_{\rm base}(k\Delta).
$$

The observed velocity has once continuously differentiable paths, not infinitely differentiable paths. Each member has finite instantaneous acceleration variance

$$
\mathbb E[\dot V_q^2]=\kappa+b_q^2,
$$

and strictly positive diffusivity

$$
D_q=\operatorname{Re}\chi_{\rm base}(ib_q)
=\frac{\kappa\nu}{(\kappa-b_q^2)^2+\nu^2b_q^2}>0.
$$

Removing the observed coordinate leaves a stable hidden drift $B$ with $B+B^T\preceq0$. Its scalar memory transform is $d^T(sI-B)^{-1}d$, hence passive in the right half-plane. This is a free thermal GLE, not just an arbitrary covariance extension. Passivity does not require an everywhere nonnegative or completely monotone time-domain memory kernel; imposing either stronger restriction changes the class.

For every fixed $T$, the Riemann–Lebesgue lemma applied to $(T-t)C_{\rm base}(t)$ on $[0,T]$ gives $J_q(T)\to0$. All models are normally diffusive; different asymptotic exponents are not needed for this finite-time ambiguity.

Independent pairs sampled a time $\Delta$ apart give identical Gaussian finite-difference acceleration laws in every member. Thus even those additional pairs cannot supply a uniformly informative upper confidence bound on instantaneous acceleration variance. If $U$ were uniformly $1-\alpha$ valid over all $q$, its common observation law would have to satisfy

$$
\Pr(U\ge\kappa+b_q^2)\ge1-\alpha\quad\text{for every }q,
\qquad\text{hence}\qquad\Pr(U=+\infty)\ge1-\alpha.
$$

This is a statement about the specified lattice observations and this unrestricted alias family. It does not include direct instantaneous acceleration, continuous displacement increments, or general forced observations. [[Benchmark 012 — Acceleration Information and Certified Displacement]] checks the matrices and demonstrates the danger of substituting finite-difference calibration for a genuinely justified acceleration bound.

### What additional information could repair finite-difference calibration?

For example, if an independently justified *physical* spectral support bound $\omega\le\Omega<2\pi/h$ holds, then

$$
\sigma_{\rm FD}^2=\int\omega^2\operatorname{sinc}^2(\omega h/2)\,\rho(d\omega)
\ge\operatorname{sinc}^2(\Omega h/2)\int\omega^2\rho(d\omega),
$$

where $\operatorname{sinc}(x)=\sin(x)/x$. A valid finite-difference variance upper limit can then be divided by that known positive factor. A detector's limited bandwidth is not proof that the physical spectrum has that support. The exponential-memory target above has an unbounded spectrum and does not satisfy this illustrative hard-cutoff assumption; a tail-moment allowance or a different physical justification would be needed.

## 4. Two simple bounds before optimization

Assume $\int\omega^2\rho(d\omega)\leq K$.

### Ballistic lower bound

The global inequality $\cos u\leq1-u^2/2+u^4/24$ gives

$$
\max\left(0,\frac{T^2}{2}-\frac{KT^4}{24}\right)
\leq J(T)\leq\frac{T^2}{2}.
$$

The lower bound is informative at sufficiently short times, without using any nonzero covariance lag. A finite acceleration bound alone does not guarantee a useful positive lower bound at every horizon. For example, spectra supported on nonzero frequencies $2\pi j/T$ have $J(T)=0$; appropriate mixtures can have any prescribed second moment at least $(2\pi/T)^2$. Such spectral-line examples demonstrate the limit of the broad positive-measure class, not a normally diffusive realization.

### Interpolation bound inside the observation window

For an integer $m\geq1$ with $T=m\Delta$ and all $c_0,\ldots,c_m$ observed, integrate the piecewise-linear interpolant of $C$ exactly:

$$
J_{\rm PL}(T)=
\left(\frac{T\Delta}{2}-\frac{\Delta^2}{6}\right)c_0
+\Delta\sum_{k=1}^{m-1}(T-k\Delta)c_k
+\frac{\Delta^2}{6}c_m.
$$

The spectral moment bound implies $|C''(t)|\leq K$. On an interval $[a,b]$ of length $\Delta$, linear-interpolation error is at most $K(t-a)(b-t)/2$. Integrating this error against $T-t$ and summing the intervals yields

$$
\left|J(T)-J_{\rm PL}(T)\right|
\leq\frac{KT^2\Delta^2}{24}.
$$

With covariance intervals, add the corresponding weighted sum of interval radii to this error. These formulas provide an independent check on an optimized certificate. They do not justify extrapolating the interpolation bound beyond the last observed lag.

## 5. A global dual certificate for displacement

Suppose the admissible spectra satisfy the observed moment constraints and $\int\omega^2\rho\leq K$. For $\sigma\in\{+1,-1\}$, seek real coefficients $a_\sigma$, $y_{\sigma,k}$ and $b_\sigma\geq0$ such that

$$
q_\sigma(\omega)=a_\sigma+b_\sigma\omega^2
+\sum_{k=1}^n y_{\sigma,k}\cos(k\Delta\omega)
-\sigma g_T(\omega)\geq0
\quad\text{for all }\omega\geq0.
$$

For exact moments, integration gives

$$
\sigma J(T)\leq B_\sigma,
\qquad
B_\sigma=a_\sigma+b_\sigma K
+\sum_{k=1}^n y_{\sigma,k}c_k.
$$

Hence $-B_-\leq J(T)\leq B_+$. Intersect with the elementary interval $[0,T^2/2]$. If the second moment is known exactly, using it as an upper bound is still a valid relaxation; do not describe that relaxation as exploiting the equality completely.

For a simultaneous uncertainty box $|c_k-\widehat c_k|\leq\eta_k$, replace the bound by

$$
B_\sigma=a_\sigma+b_\sigma K
+\sum_{k=1}^n y_{\sigma,k}\widehat c_k
+\sum_{k=1}^n|y_{\sigma,k}|\eta_k.
$$

On the event that all covariance constraints and the acceleration bound hold, every such certificate is valid. Thus a simultaneous information set with coverage at least $1-\alpha$ transfers that coverage to the response interval. Optimizing the certificate after seeing the data does not invalidate this deterministic implication. Pointwise covariance error bars without a simultaneous-coverage argument are insufficient.

Bounding functionals over a feasible information set, instead of assigning uncertainty only to one reconstructed model, is a longstanding inverse-problem strategy. [Philip B. Stark, *Uncertainties for Functions*](https://www.stat.berkeley.edu/~stark/Seminars/nsf-doe-98.htm)

## 6. From a frequency grid to a continuum guarantee

A grid-only primal optimum is **not** a rigorous bound for all continuous spectra. Restricting support to grid points removes feasible models and can narrow the apparent range. A dual majorant must be checked between nodes and at arbitrarily high frequencies.

### Finite interval

For either sign,

$$
\sup_{\omega\in[0,R]}|q_\sigma''(\omega)|
\leq M_\sigma
:=2b_\sigma+
\sum_{k=1}^n|y_{\sigma,k}|(k\Delta)^2
+\frac{T^4}{12}.
$$

The last term follows by differentiating
$g_T(\omega)=\int_0^T(T-t)\cos(\omega t)dt$ twice and bounding the resulting integral. If consecutive verification nodes are at most $h$ apart, their piecewise-linear interpolation differs from $q_\sigma$ by at most $M_\sigma h^2/8$.

Consequently, if the evaluated minimum node value is $q_{\min}$, adding

$$
\delta_\sigma=\max\left(0,\frac{M_\sigma h^2}{8}-q_{\min}\right)
$$

to $a_\sigma$ certifies nonnegativity on the finite interval in exact arithmetic. It increases $B_\sigma$ by the same amount. In computation, add a stated allowance for node-evaluation and solver residuals as well. This is an analytic continuum correction implemented in floating point, not an interval-arithmetic proof of every floating-point operation.

### Infinite-frequency tail

Because $0\leq g_T(\omega)\leq2/\omega^2$ for $\omega>0$, the sufficient condition

$$
a_\sigma+b_\sigma R^2
-\sum_{k=1}^n|y_{\sigma,k}|
-\frac{2\max(\sigma,0)}{R^2}\geq0
$$

certifies $q_\sigma(\omega)\geq0$ for all $\omega\geq R$. The lower envelope used here is nondecreasing on that tail. The inequality can be included during optimization; a subsequent positive constant correction preserves it. Replacing the last numerator by $2$ for both signs is also safe, but more conservative.

This absolute-coefficient tail test is sufficient, not necessary. It can loosen a bound substantially; failure of this particular test does not prove that a proposed majorant is invalid.

### Exact lattice improvement for the upper bound

When the prediction time is also $T=m\Delta$, fold each frequency to its principal representative $\omega_0\in[0,\pi/\Delta]$ with $\cos(\Delta\omega_0)=\cos(\Delta\omega)$. Every observed cosine is unchanged. The numerator of $g_T$ is unchanged too, and $\omega\geq\omega_0$, so

$$
g_T(\omega)\leq g_T(\omega_0).
$$

The zero-frequency limit is treated by continuity; a nonzero alias of zero has numerator zero. For $b_+\geq0$,

$$
q_+(\omega)-q_+(\omega_0)
=b_+(\omega^2-\omega_0^2)
+g_T(\omega_0)-g_T(\omega)\geq0.
$$

Thus certifying the upper majorant on $[0,\pi/\Delta]$ already certifies it globally. This can avoid the conservative tail test, including when $b_+=0$. The argument is specific to lattice-aligned prediction times and is not the corresponding proof for the lower majorant.

## 7. Falsifiable research question and stopping rules

Compare the certified displacement range from the same finite observations with and without a justified acceleration bound. Test interpolation horizons and progressively longer extrapolation horizons. Keep the truth out of optimization except for clearly labeled supplied physical information.

Useful outcomes include a narrow bound that demonstrably contains the target response, or a wide bound showing that this calculation does not yet certify the desired prediction. Proving that the measurements themselves are insufficient requires separated feasible witnesses or a suitable sharpness argument, not just a wide conservative outer interval. Neither outcome identifies a unique memory kernel. The central question is how much extra acceleration information improves a physical prediction, not whether a chosen reconstruction curve looks accurate.

Do not report a numerical interval as sharp unless feasible extremal witnesses and a controlled primal–dual gap establish that claim for the stated class. Report continuum corrections, tail treatment, statistical coverage assumptions, and floating-point limitations separately. No novelty claim is attached to the optimization method or to the elementary derivations in this note.

[[Finite Memory and the Return to Normal Diffusion]] · [[Research Frontier — Identifiability Before Discovery]] · [[Synthesis Lab]]
