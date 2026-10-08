---
type: computational-benchmark
field: Statistical Physics
epistemic_status: effective
level: advanced
tags: [memory-kernel, anomalous-diffusion, validation, identifiability, linear-response]
created: 2026-09-12
updated: 2026-09-13
note_maturity: expanded
source_audit: independently-audited-computation-with-primary-method-sources
---

# Benchmark 010 — Noisy Memory and the Prediction Horizon

The noisy experiment accepts 104 of 800 datasets after reducing model order and the fitted time window. The more consequential result comes from the clean reference: its small correlation error coexists with an eventual change from subdiffusion to ordinary diffusion. A prediction horizon and a forcing-frequency range are therefore part of the model's physical specification.

[[Finite Memory and the Return to Normal Diffusion]] derives the conditions and limits. The cutoff phenomenon is established in the literature; this benchmark computes its consequences for our reproduced model.

[[Benchmark 009 — Published Subdiffusion Memory Reproduction]] · [[Research Frontier — Identifiability Before Discovery]]

## 1. Scope of the experiment

The input target remains $C_*(t)=E_{3/2}(-|t|^{3/2})$, with $\gamma_*(t)=1/\sqrt{\pi t}$ and $m=\beta=1$.

Lab 28 uses a **restricted implementation** of the Bockius construction: moment/Jacobi recurrence, Newton derivative constraint, stable auxiliary realization, sampled positive-real screen, and regularized thermal covariance/noise construction. It reduces $n$ from 10 toward 4 after failure.

The paper's Appendix B deletes unstable modes and represents negative discrete poles using oscillatory pairs. Our restricted stress implementation instead reports those cases as requiring spectral repair. Consequently, its rejection rates cannot be attributed to the full published method. The final Lanczos change of coordinates is unnecessary for these predictions and is not run in lab 28. [Bockius et al., Appendix B](https://arxiv.org/html/2101.02657#A2)

The paper's noisy test uses molecular dynamics data and permits reducing order when necessary. Our Gaussian ensemble noise is a distinct synthetic experiment. [Bockius et al., Section 3.3](https://arxiv.org/html/2101.02657#S3.SS3)

## 2. Data with independent provenance

For 20 observation times $0,0.6,\ldots,11.4$, define the analytic Toeplitz covariance

$$
K_{ij}=C_*(0.6|i-j|).
$$

Its smallest numerical eigenvalue is 0.09359. Each dataset is an exact Wishart scatter matrix

$$
S=\sum_{r=1}^M X_rX_r^T,\qquad X_r\sim N(0,K),
$$

representing $M$ independent velocity-trajectory vectors. The reconstruction sees only

$$
\widehat c_k=S_{0k}/S_{00},\qquad \widehat c_0=1.
$$

These estimates are correlated across lags. With $c=K_{0,\mathrm{rest}}$ and $R=K_{\mathrm{rest},\mathrm{rest}}-cc^T$, Gaussian conditioning gives

$$
E[\widehat c]=c,\qquad
\operatorname{Cov}(\widehat c)=\frac{R}{M-2}.
$$

Indeed, $X_{\mathrm{rest}}=cX_0+\epsilon$, where $\epsilon$ is independent of $X_0$ with covariance $R$. Conditional on $S_{00}$, the estimation error is Gaussian with covariance $R/S_{00}$; $S_{00}\sim\chi^2_M$. Its marginal distribution is multivariate Student $t_M$ with scale $R/M$.

The generator uses the analytic target only. It does not simulate the fitted model. A separate explicit-trajectory check confirms the mean and covariance formulas. This is a mathematical Gaussian-process dataset, not hardware observations or Lennard-Jones trajectories.

The locally recorded September 5 protocol chose four sizes $M=64,256,1024,4096$, 200 datasets per size, and seed 20260905 before the original full run. The September 12 version 1.1 is an explicitly post-run audit amendment. The original files are preserved in the workspace's `work/noisy-memory-v1-2026-09-05` folder.

## 3. Acceptance and what it means

Acceptance requires convergence of the Newton constraint, admissible discrete poles under this restricted branch, stable full and auxiliary matrices, sampled positive-real behavior, a covariance meeting the numerical positivity tolerance, and small Riccati, Lyapunov, and interpolation residuals. The actual regularized matrix $A_\delta$ is now used for the correlation prediction.

Noisy data are not required to pass, and prediction error against the analytic truth is not used to select order. The evaluation's good-correlation threshold is RMSE $\le0.01$ on 301 evenly spaced points in $[0,30]$. The poor-kernel threshold is logarithmic RMSE $>0.5$ on 120 logarithmically spaced points in $[0.05,12]$, with sign mismatches assigned infinite extended loss. These weightings differ and do not form a confidence statement.

Reducing $n$ also discards late samples: the fitted interval shortens from $[0,11.4]$ at $n=10$ to $[0,4.2]$ at $n=4$. It changes both capacity and temporal coverage.

## 4. Noisy results

| Ensemble size | Accepted after fallback | Wilson 95% interval | Median VACF RMSE among accepted | Kernel sign mismatches among accepted |
|---:|---:|---:|---:|---:|
| 64 | 16/200 (8.0%) | 4.98–12.60% | 0.05077 | 15/16 |
| 256 | 17/200 (8.5%) | 5.37–13.19% | 0.03249 | 7/17 |
| 1024 | 31/200 (15.5%) | 11.14–21.16% | 0.02151 | 5/31 |
| 4096 | 40/200 (20.0%) | 15.05–26.09% | 0.01062 | 2/40 |

None of the 800 noisy datasets passed at $n=10$. For each group of 200, zero observed successes still has a Wilson upper endpoint of 1.88%; it does not establish zero success probability.

There are 5,504 individual attempted fits. Of these, 4,556 reach a pole pattern that this implementation sends to the unimplemented spectral-repair branch. That limitation dominates the experiment. It is not evidence that the paper's complete method fails on the same inputs.

Twenty-nine accepted kernels become nonpositive somewhere on the evaluation grid, disagreeing with this strictly positive target. Sign-changing kernels can still be thermally admissible. Their logarithmic error is undefined, so outputs retain a categorical sign flag, a null log value, an explicit extended-loss status, and an always-defined relative RMSE. No point is silently counted as an accurate reconstruction because its log error cannot be plotted.

![Noisy memory study](../62%20Computational%20Labs/results/noisy_memory_stress/noisy_memory_stress.png)

The original and audited runs select the same 104 datasets. One meets the chosen good-VACF/poor-kernel definition: $M=1024$, replicate 196, $n=5$, VACF RMSE 0.009598, kernel log-RMSE 0.56893. A single threshold-selected example is a diagnostic lead, not a general frequency claim.

At $M=4096$, the median accepted Newton adjustment of $y_1$ is about 1.81 times that estimator's unconditional sampling standard deviation. Interpolation of the *adjusted* samples must therefore be distinguished from agreement with the original measurements. This standardized adjustment is descriptive; selection prevents interpreting it as an unadjusted significance test.

## 5. A stronger question: what motion does the model predict?

Lab 29 is a **post-hoc analysis**, specified after inspecting the noisy results. It uses saved regularized matrices and changes no fit. For a stationary additive sinusoidal force, compare the predicted velocity mobility

$$
\chi_N(\omega)=e_1^T(i\omega I-A_\delta)^{-1}e_1
$$

with the exact target

$$
\chi_*(\omega)=\frac{1}{i\omega+(i\omega)^{-1/2}}.
$$

For the clean model, maximum complex relative error over logarithmic frequency grids is 0.77% on $[0.3,3]$, 1.17% on $[3,30]$, 4.71% on $[0.03,0.3]$, and 679% on $[10^{-4},10^{-2}]$. These are band diagnostics; the large relative error at low frequency occurs as the true response tends to zero.

The same physical distinction appears in mean-square displacement. The exact target obeys

$$
M_*(t)=2t^2E_{3/2,3}(-t^{3/2})\sim\frac{4\sqrt t}{\sqrt\pi}.
$$

The clean fitted model instead has

$$
D_N=e_1^T(-A_\delta)^{-1}e_1=0.07466356,
\qquad M_N(t)\sim2D_Nt.
$$

| Time | Exact target MSD | Clean model MSD | Relative error |
|---:|---:|---:|---:|
| 1 | 0.84370 | 0.84843 | 0.56% |
| 10 | 7.13480 | 7.19977 | 0.91% |
| 30 | 12.36095 | 12.56117 | 1.62% |
| 100 | 22.56759 | 24.22490 | 7.34% |
| 1000 | 71.36496 | 158.65466 | 122.31% |
| 10000 | 225.67583 | 1502.59879 | 565.82% |

The first sampled time after the training window with displacement error above 10% is approximately 118.90. This grid crossing is not a certified uniform horizon or an experimental timescale. All times use the problem's reduced units.

![Response and long-time displacement](../62%20Computational%20Labs/results/noisy_memory_stress/memory_extrapolation.png)

All 104 accepted noisy realizations also have positive DC diffusivity. Their median values are 0.4343, 0.4064, 0.2759, and 0.2323 as ensemble size increases. Prediction errors quoted for them are conditional on acceptance; rejected datasets remain part of the study accounting.

This is the established finite-memory cutoff effect, whose conditions are proved in [[Finite Memory and the Return to Normal Diffusion]]. It does not contradict a method intended for a finite range. [Goychuk 2009, Section II and Appendix A](https://arxiv.org/html/0905.0826#A1)

## 6. What the audit corrected

The September 5 outputs contained a nonstandard JSON infinity value and plots that omitted kernels whose logarithmic error was undefined. The audit also found a catch-all failure category that hid unsupported negative-pole cases, missing finite/real checks, and use of an unregularized matrix for predictions even though the thermal test used its regularized counterpart.

Version 1.1 corrects those issues, preserves every input dataset and fitted matrix, and logs each attempted order and rejection reason. It retains the original ensemble sizes, seed, order range, and error thresholds. Direct matrix exponentials replace a spectral evaluation that previously discarded imaginary residuals. An independent review of the original accepted fits found no realized instability or significant complex residual; the corrections improve the validity and accounting of the experiment.

The amended lab passed 13 verification groups; the physical extrapolation audit passed eight. The latter checks the analytic MSD against an independent series, integrated matrix dynamics against a second closed-form calculation, and mobility against the memory-transfer formula.

## 7. Research decision

The useful question is now the supported prediction domain, rather than acceptance alone. The next comparison should include the full spectral-repair baseline, a fractional-memory model, and a tempered fractional model with an unknown physical cutoff. They must receive the same observations and be judged on declared time horizons and forcing bands.

A real material may cross over to normal diffusion. Our analytic target has no cutoff by construction; its infinite tail is not evidence that every physical system has one. The experiment should ask what finite observations can actually constrain about that distinction.

[[Benchmark 011 — Finite Observations and Infinite-Time Claims]] now supplies an analytic and numerical information-limit extension: arbitrarily small positive physical cutoffs cannot be distinguished uniformly from zero cutoff by a fixed finite Gaussian observation experiment. This separates observational limits from the fitted model's finite-memory artifact.

## Reproducible assets

From the computational-lab directory:

~~~powershell
python 28_noisy_memory_stress.py
python 29_memory_extrapolation.py
~~~

[Noise protocol](../62%20Computational%20Labs/noisy_memory_stress_protocol.json) · [Extrapolation protocol](../62%20Computational%20Labs/memory_extrapolation_protocol.json) · [Study results](../62%20Computational%20Labs/results/noisy_memory_stress/results.json) · [Every attempt](../62%20Computational%20Labs/results/noisy_memory_stress/attempts.jsonl) · [Trial table](../62%20Computational%20Labs/results/noisy_memory_stress/trials.csv) · [Inputs and models](../62%20Computational%20Labs/results/noisy_memory_stress/inputs_and_models.npz) · [Extrapolation results](../62%20Computational%20Labs/results/noisy_memory_stress/extrapolation.json)

[[Computational Lab Index]] · [[Release Status and Next Work]] · [[Physics Worldmap]]
