---
type: computational-benchmark
field: Cross-field
epistemic_status: effective
level: advanced
tags: [physics, synthesis, identifiability, response, sampling, reproducibility]
created: 2026-09-04
updated: 2026-09-04
source_audit: explicit-model-derived-with-prior-art-screen
note_maturity: expanded
---

# Benchmark 002 — The Sampling Boundary of Prediction

> [!important] Outcome
> Three ordinary thermal oscillators have identical equilibrium position statistics at every integer sample time, but different responses to the same continuous forcing. The result is an explicit instance of established system aliasing, not a new theorem or physical discovery. It rules out an unconditional response certificate based only on those samples when mass and unresolved frequencies are unknown.

[[Benchmark 001 — Equilibrium Versus Forced Response]] · [[Research Frontier — Identifiability Before Discovery]] · [[Computational Lab Index]] · [[Linear Response Theory]]

## 1. Why investigate this before a nonlinear warning model?

The proposed next goal was a warning, computed before forcing, that predicts reduced-model failure. Before trying a regression or new memory closure, ask whether the permitted input data can possibly determine the target response.

Benchmark 001 fixed the mass and supplied exact continuous-frequency response during training. Here the information is deliberately different: exact, regularly sampled equilibrium **positions only**, with known temperature, stiffness, decay rate, and sampling interval, but unknown mass. Momenta, velocities, off-grid observations, and forcing responses are withheld.

This is an adversarial identifiability test, not a typical-data performance study or a direct competitor to Benchmark 001.

The [protocol](../62%20Computational%20Labs/sampling_boundary_protocol.json) was written before the first run. Its SHA-256 is:

    96566563d8e3ca12908ebf7df9bdbb56d600686a4f2c800335f9994868090ff2

This is a local prospective record, not independently registered research. No selection or classification threshold was tuned on results.

## 2. Construct the indistinguishable systems

For each positive integer $j$, define a damped angular frequency and physical parameters

$$
\omega_j=\frac{2\pi j}{\Delta},\qquad
m_j=\frac{k}{\omega_j^2+\alpha^2},\qquad
\zeta_j=2\alpha m_j,
$$

where $k>0$ is stiffness, $\alpha>0$ is the decay rate, and $\Delta>0$ is the sampling interval. Each system obeys the usual underdamped thermal Langevin equation

$$
dq=v\,dt,\qquad
m_j\,dv=(-kq-\zeta_jv+f(t))dt+\sqrt{2\zeta_j k_BT}\,dW.
$$

The potential is the same $\tfrac12 kq^2$ for every model. All masses and frictions are positive, all dynamics are stable, and thermal noise obeys the appropriate fluctuation–dissipation relation.

At zero force,

$$
\langle q^2\rangle=\frac{k_BT}{k},\quad
\langle v^2\rangle=\frac{k_BT}{m_j},\quad
\langle qv\rangle=0.
$$

The equilibrium position autocovariance follows by solving the homogeneous mean equation with these initial covariances:

$$
C_j(t)=\frac{k_BT}{k}e^{-\alpha |t|}
\left[\cos(\omega_j|t|)+\frac{\alpha}{\omega_j}\sin(\omega_j|t|)\right].
$$

At every integer multiple of the sample spacing, the sine vanishes and the cosine equals one:

$$
C_j(n\Delta)=\frac{k_BT}{k}e^{-\alpha|n|\Delta},
\qquad n\in\mathbb Z.
$$

The right-hand side contains no $j$. All sampled means are zero; all processes are Gaussian. Consequently **every finite-dimensional joint law of the sampled positions is identical** across the entire constructed family. This is stronger than matching a variance or a finite list of empirical correlations.

Equivalently, their sampled positions obey the same AR(1) law,

$$
q_{n+1}=r q_n+\epsilon_n,\quad
r=e^{-\alpha\Delta},\quad
\epsilon_n\sim\mathcal N\left(0,\frac{k_BT}{k}(1-r^2)\right),
$$

with independent innovations. Sampling for longer at the same spacing cannot resolve this ambiguity. Identical law does not mean independently generated realizations have identical sample values.

## 3. Why forcing distinguishes them

For the convention $f(t)=\operatorname{Re}(f_\nu e^{i\nu t})$,

$$
\chi_j(\nu)=\frac{1}{k-m_j\nu^2+i\zeta_j\nu}.
$$

These functions depend on $j$. The common static limit $1/k$ does not determine finite-frequency response. This is not a violation of fluctuation–dissipation theory: continuous-time equilibrium correlations differ between observation times. Sampling has discarded the information needed to reconstruct them without further assumptions.

Set $k=k_BT=\Delta=1$, $\alpha=0.2$, $j=1,2,3$, and apply a force of amplitude 0.1 at angular frequency $\nu=2\pi$. Exact results are:

| Model | Mass | Off-grid covariance at lag 0.137 | Periodic steady-state displacement amplitude |
|---|---:|---:|---:|
| 1 | 0.025304657 | 0.657703 | 1.572189 |
| 2 | 0.006330970 | -0.130856 | 0.133292 |
| 3 | 0.002814161 | -0.819290 | 0.112495 |

The largest response amplitude is approximately 13.98 times the smallest. These are exact linear-model responses after transients have decayed, not noisy trajectories, nonlinear resonances, or experimental measurements.

The finite numerical sampled-covariance comparison agrees within $4.2\times10^{-17}$ relative error. The all-lag equality is established by the formula above, not extrapolated from that numerical check.

![Sampling boundary](../62%20Computational%20Labs/results/sampling_boundary/sampling_boundary.png)

## 4. A lower bound on what any point prediction can achieve

Suppose a predictor receives only the common sampled equilibrium law and the declared force. It must return the same predicted complex susceptibility $\widehat\chi$ regardless of which compatible oscillator is the true one. The triangle inequality gives

$$
\max_j|\widehat\chi-\chi_j|
\geq \frac12\max_{i,j}|\chi_i-\chi_j|.
$$

At the chosen frequency the response diameter is 15.735278, so the worst-case absolute susceptibility error is at least 7.867639. Multiplying by the force amplitude gives a bound of 0.786764 on absolute **complex displacement-amplitude** error. This is not a bound on the difference of amplitude magnitudes, a normalized trajectory error, or the minimum error for each model separately.

For an estimator based on random finite sampled data, their common data distribution yields the corresponding bound on worst-case expected absolute error. More data of the same kind cannot remove exact non-identifiability.

A warning can honestly say “ambiguous” for the entire family. What it cannot do from these data alone is identify which member's continuous response is correct. A small sampled residual or a rank-one sampled covariance Hankel matrix cannot certify intersample physics.

## 5. What additional information changes the answer?

- **Known mass:** together with $k,\alpha$, it fixes the positive frequency $\sqrt{k/m-\alpha^2}$ in this family. The counterexample does not apply to that information setting.
- **Velocity or momentum statistics:** equipartition depends on mass and distinguishes these models.
- **Off-grid equilibrium correlations:** the extra lag 0.137 separates the three tested members. This means estimating a covariance from repeated data, not taking one magical position reading.
- **Frequency restrictions:** a justified bound on unresolved oscillation frequencies can exclude aliases. A bound must come from physics or measurements, not the fitted model alone.
- **Designed forcing measurements:** a response experiment can supply information missing from passive observations.

The off-grid result is only for the finite tested family with exact covariance. It does not prove one extra lag suffices for arbitrary oscillators, finite noise, hidden networks, or nonlinear dynamics. Finite temporal averaging by an instrument also changes the observation model and must be accounted for.

## 6. Reproduce and audit

From the computational-labs directory:

~~~powershell
python 18_sampling_identifiability_boundary.py
~~~

The [source](../62%20Computational%20Labs/18_sampling_identifiability_boundary.py) writes [results and 31 checks](../62%20Computational%20Labs/results/sampling_boundary/results.json), [model values](../62%20Computational%20Labs/results/sampling_boundary/models.csv), [arrays](../62%20Computational%20Labs/results/sampling_boundary/arrays.npz), and the figure. It is separate from the core 01–13 runner. NumPy and Matplotlib are the only external dependencies.

All 31 checks passed: thermal Lyapunov identities; positive mass and stability; matrix versus analytic covariance and susceptibility; the exact sample transition; common static response; fluctuation–dissipation spectra; sampled Hankel rank; distinct forcing response; off-grid discrimination for this family; identical-parameter control; and known-mass recovery. No time-stepping approximation or stochastic sampling is used.

## 7. Prior art and claim boundary

System aliasing is established. [Yue et al.](https://arxiv.org/abs/1605.08590) study ambiguity under low-frequency sampling and the role of prior information. The present thermal example is a worked derivation for this vault, not a claim to originate their general phenomenon.

[González et al.](https://arxiv.org/abs/2410.19629) analyze sampling and input conditions for system identification, including circumstances allowing identification beyond ordinary reconstruction limits. This is why the counterexample is explicitly restricted to passive regularly sampled positions and unknown mass; it must not be generalized into a claim that all slow-sampled forced identification is impossible.

Both author abstracts were inspected in this pass. Neither algorithm nor all theorem assumptions have been reproduced. A full-text theorem comparison is still required before any novelty assessment.

## 8. Research decision

The broad promise “predict failure from equilibrium data” needs qualification. The next candidate target is **response uncertainty over all physically admissible models compatible with the available observations, followed by a measurement that reduces that uncertainty**.

This connects to established robust identification and experimental design. It is a direction to investigate, not a new method. First bound the information available; then test whether a physically constrained method improves on the best known alternatives. See [[Research Frontier — Identifiability Before Discovery]] for the updated research gates.

## Navigation

[[Synthesis Session 001 — Response-Preserving Coarse-Graining]] · [[Synthesis Lab]] · [[Release Status and Next Work]] · [[Physics Worldmap]]
