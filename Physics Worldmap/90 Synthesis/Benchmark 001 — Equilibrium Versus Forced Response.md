---
type: computational-benchmark
field: Cross-field
epistemic_status: effective
level: advanced
tags: [physics, synthesis, response, coarse-graining, reproducibility]
created: 2026-09-04
updated: 2026-09-04
source_audit: explicit-model-derived-with-method-references
note_maturity: expanded
---

# Benchmark 001 — Equilibrium Versus Forced Response

> [!important] Result and scope
> Completed linear-Gaussian pilot, not a new theory. Two reduced models reproduce the same one-time equilibrium distribution exactly, but their forced responses differ. Fitting one damping parameter improves held-out pulse and chirp errors by approximately 27% and 26%, respectively. A conventional balanced-truncation reference is substantially more accurate on response, with some loss of equilibrium agreement. This does **not** validate the broader four-system hypothesis.

[[Synthesis Session 001 — Response-Preserving Coarse-Graining]] · [[Mechanics to Statistical Physics — Foundation Study Route]] · [[Computational Lab Index]] · [[Linear Response Theory]]

## 1. Question and frozen protocol

Can matching static equilibrium data leave a model dynamically wrong? Can a small amount of response information improve it without changing its equilibrium distribution?

The [protocol](../62%20Computational%20Labs/response_benchmark_protocol.json) was written before the first numerical run on September 4, 2026. It fixes physical parameters, model family, training frequencies, search grid, unseen forcing, and numerical tolerances. This is a local prospective record, not an independently timestamped preregistration.

Protocol SHA-256:

    ced715912bfaf5c482739677fd55a1bdde43fdd043b4f6c9032a710646085647

No parameter or held-out test changed after inspecting the results. Three fluctuation–dissipation identity checks were added afterward as an implementation audit; they did not select or alter the models. They are not advertised as preregistered checks.

## 2. Fine system and what equilibrium means

Use nondimensional units with masses and $k_BT$ equal to one. Two damped, thermally driven oscillators obey

$$
dq=p\,dt,\qquad
dp=(-Kq-\Gamma p+e_1 f(t))dt+\sqrt{2k_BT\Gamma}\,dW,
$$

$$
K=\begin{pmatrix}2&1.5\\1.5&5\end{pmatrix},
\qquad \Gamma=\operatorname{diag}(0.3,0.6).
$$

The two Wiener processes are independent. $K$ is positive definite. The positive off-diagonal term is a valid stable quadratic coupling; these coordinates need not be the displacements of a particular untransformed spring network.

The force acts on $p_1$; the measured output is $q_1$. The four-state order is $(q_1,q_2,p_1,p_2)$. At zero force the canonical stationary covariance is

$$
\Sigma=\operatorname{diag}(k_BT K^{-1},\,k_BT I).
$$

Integrating out $q_2,p_2$ gives the observed equilibrium marginal

$$
\rho(q_1,p_1)\propto
\exp\left[-\frac{p_1^2+k_{\rm eff}q_1^2}{2k_BT}\right],
\qquad
k_{\rm eff}=2-\frac{1.5^2}{5}=1.55.
$$

Thus $\operatorname{Var}(q_1)=1/1.55$, $\operatorname{Var}(p_1)=1$, and their equal-time covariance is zero. Because the distribution is Gaussian, matching this covariance and zero mean matches the entire **one-time** marginal, not merely its first two moments.

It does not match multi-time correlations or the full hidden-state distribution. Response is related to *dynamical* equilibrium correlations by fluctuation–dissipation theory; nothing here contradicts that relation. The noise/response identity is independently checked below.

## 3. Competitors and information budgets

The equilibrium-preserving two-state family is

$$
dq=p\,dt,\qquad
dp=(-1.55q-\gamma p+f(t))dt+\sqrt{2\gamma k_BT}\,dW.
$$

Every $\gamma>0$ has the observed stationary marginal above and the same static susceptibility $1/1.55$. Equilibrium data alone cannot identify $\gamma$.

| Model | State count | Construction and information |
|---|---:|---|
| Fine system | 4 | Exact known dynamics; reference truth |
| Equilibrium-only | 2 | Uses $\gamma=0.3$, the original observed-coordinate damping, as the frozen tie-break |
| Response-fitted | 2 | Same family; select only $\gamma$ using eleven noiseless complex-response values |
| Balanced reference | 2 | Classical balanced truncation using the **entire** known force/output system |
| Exact eliminated response | 4-equivalent | Algebraic elimination of hidden coordinates, retaining their frequency dependence |

The response fit searches 501 logarithmically spaced dampings from 0.03 to 3.0, minimizing relative complex-response $L_2$ error over eleven angular frequencies from 0.15 to 0.65. It selects $\gamma=0.3606793304$.

This is an objective ablation within one family, not a finite-data, equal-information contest between learned algorithms. The equilibrium baseline does not use forced data. Balanced truncation has the same state count but a more flexible realization and full-model information; it is a strong contextual reference, not an information- or parameter-matched competitor. Standard Gramian balancing and projection follow the [pyMOR method documentation](https://docs.pymor.org/2024-2-0/tutorial_bt.html).

For balanced truncation, both thermal noise and the observed pair $(q_1,p_1)$ are projected with the same computed transformations. No post-hoc noise rescaling repairs the equilibrium error. Its reconstructed momentum need not equal the derivative of its output; canonical mechanical structure and passivity are not certified.

## 4. Exact answer and measurements

With sinusoidal convention $f(t)=\operatorname{Re}(f_\omega e^{i\omega t})$, elimination gives

$$
\chi_{\rm full}(\omega)=
\left[
2-\omega^2+0.3i\omega-
\frac{1.5^2}{5-\omega^2+0.6i\omega}
\right]^{-1},
\qquad
\chi_\gamma(\omega)=
\frac{1}{1.55-\omega^2+i\gamma\omega}.
$$

The rational hidden-oscillator term is verified independently against the four-state matrix resolvent. Calling it an exact memory representation does not make it a two-state Markov model: its transfer function retains four-state dynamics. A stationary stochastic memory equation would also require the appropriately filtered noise and initial-condition terms; this pilot does not discard them and claim stationary equivalence.

For each frequency grid or time series, use

$$
E=\frac{\|\widehat y-y_{\rm full}\|_2}{\|y_{\rm full}\|_2}.
$$

Frequency scores compare complex responses, including phase, not only magnitudes. Time scores compare ensemble-mean trajectories, not individual noisy realizations.

Held-out tests are ten midpoints between training frequencies; 201 frequencies over 0.8–3.0; a Gaussian pulse centered at time 8 with width 0.7; and a Hann-windowed chirp whose angular frequency increases from 0.1 to 3.0 over time 0–80. Both forced runs begin with zero-mean equilibrium initial ensembles. Linearity makes the mean obey the deterministic equation exactly.

## 5. Results

All numbers below are percentages of the corresponding reference norm. Equilibrium error is the Frobenius-relative error of the **observed pair's** covariance in the declared nondimensional coordinates, not a coordinate-invariant distance between distributions.

| Model | Equilibrium covariance | Frequency interpolation | Frequency extrapolation | Pulse | Chirp |
|---|---:|---:|---:|---:|---:|
| Equilibrium-only | Numerical zero | 2.714% | 41.697% | 33.273% | 44.817% |
| Response-fitted | Numerical zero | 1.667% | 30.702% | 24.169% | 32.960% |
| Balanced reference | 6.897% | 1.421% | 5.586% | 2.175% | 3.608% |

“Numerical zero” means below $3\times10^{-16}$ relative covariance error. The balanced model's position-variance error alone is 3.503%; the joint covariance metric should not be confused with that single variance.

Relative to the equilibrium-only baseline, response fitting reduces extrapolation error by 26.37%, pulse error by 27.36%, and chirp error by 26.46%. These are deterministic improvements on this declared example, not population estimates or confidence bounds. Substantial absolute response error remains.

![Response benchmark comparison](../62%20Computational%20Labs/results/response_benchmark/response_comparison.png)

## 6. Validation and reproduction

The [program](../62%20Computational%20Labs/17_response_preserving_reduction.py) uses NumPy and Matplotlib. From the computational-labs folder:

~~~powershell
python 17_response_preserving_reduction.py
~~~

It is separate from the core teaching suite. It writes [full results and checks](../62%20Computational%20Labs/results/response_benchmark/results.json), [machine-readable scores](../62%20Computational%20Labs/results/response_benchmark/metrics.csv), [numerical arrays](../62%20Computational%20Labs/results/response_benchmark/arrays.npz), and the figure. The result record includes protocol/source hashes and package versions.

All 32 checks passed:

- positive stiffness and stable fine/reduced dynamics;
- canonical covariance versus an independent Lyapunov solve, plus Lyapunov residuals;
- balanced transformation inverse and both balanced Gramians;
- exact elimination versus matrix response, static susceptibility, and the uncoupled limit;
- identical equilibrium marginals for different dampings, with a negative control proving their responses differ;
- an interior optimum on the frozen damping grid;
- pulse/chirp time-step refinement from 0.01 to 0.005 for all four realizations, with relative changes below $10^{-5}$;
- three post-run fluctuation–dissipation checks using independently computed thermal-noise spectra.

Specifically, with $R=(i\omega I-A)^{-1}$, the direct two-sided noise spectrum is $S_{qq}=CRGG^\mathsf{T}R^\dagger C^\mathsf{T}$. The three thermal mechanical models satisfy

$$
S_{qq}(\omega)=-\frac{2k_BT}{\omega}\operatorname{Im}\chi(\omega)
$$

on the positive test frequencies, with the sign fixed by the stated Fourier convention. See [Tong's response-theory lectures, equation 4.37 and its classical limit](https://davidtong.org/pdfs/teaching/kinetic-theory/kinetic4.pdf). The balanced projection is not assumed to satisfy this identity.

These checks audit implementation; they do not establish universality. There are no Monte Carlo samples, bootstrap intervals, fitted noise realizations, or measured experimental data.

## 7. What was learned—and what was not

**Supported:** one-time equilibrium agreement underdetermines response; adding response data helps this restricted closure; a standard control-theory reference is much stronger on response in this example.

**Not supported:** a new reduction principle, optimality, a universal equilibrium/response tradeoff, the necessity of memory for every useful approximation, or the full decision rule in Session 001. That rule requires multiple systems, data-matched strong baselines, finite-sample uncertainty, and structure checks beyond stability.

Post-result analytical explanation, not an additional fitted model: the small-frequency expansion of the exact inverse susceptibility begins

$$
\chi_{\rm full}^{-1}(\omega)=
1.55+i(0.354)\omega-(1.08352)\omega^2+O(\omega^3).
$$

The family can adjust damping but fixes the inertial coefficient to one, so one parameter cannot match both coefficients. This explains a concrete limitation without claiming that the low-frequency expansion proves the measured broad-band errors. Changing mass also changes the meaning and equilibrium variance of a retained momentum; any such extension must declare its observables again.

The next discriminating study should freeze a new protocol comparing moment-matched, structure-preserving and balanced reductions at explicit data budgets, with a richer oscillator chain and a separate diffusion problem. Add a thermal-correlation baseline: fluctuation–dissipation may extract the same response information without explicit forcing. Do not reuse these held-out outcomes to select a revised method and still call them unseen.

Prior work already connects reduction to sensitivity rather than variance alone; for example, [Otto, Padovan and Rowley's CoBRAS paper](https://arxiv.org/abs/2207.14387) balances state covariance with gradient information. Its abstract was inspected as a close-prior-work warning, not as an exhaustive literature audit or a reproduction of that algorithm.

## Navigation

[[Synthesis Lab]] · [[Release Status and Next Work]] · [[Physics Worldmap]]
