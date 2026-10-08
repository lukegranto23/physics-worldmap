---
type: reference
field: Statistical Physics
epistemic_status: established
level: advanced
tags: [prior-art, spectral-measures, inverse-problems, uncertainty, linear-response, experimental-design]
created: 2026-09-15
updated: 2026-09-15
note_maturity: expanded
source_audit: primary-method-screen
---

# Prior Art — Spectral Bounds and Physical Response

The mathematical foundations of the proposed response-bound program are established. Positive spectral measures, optimization of linear functionals under finite moment constraints, polynomial dual certificates, and simultaneous confidence bounds obtained from a common confidence set all have direct prior art. Applying these ideas to equilibrium displacement is useful synthesis, not by itself a breakthrough.

This is a targeted primary-source screen, completed on 15 September 2026. It is not an exhaustive literature review or a certification that any remaining application is new. The linked papers were inspected for the particular claims below; a search result's absence is not evidence of novelty.

[[Benchmark 012 — Acceleration Information and Certified Displacement]] · [[Benchmark 011 — Finite Observations and Infinite-Time Claims]] · [[Research Frontier — Identifiability Before Discovery]] · [[Synthesis Lab]]

## 1. The closest mathematical match

Karlsson and Georgiou's *Uncertainty Bounds for Spectral Estimation* treats the positive spectral measures consistent with finite covariance information. Section IV, equations (5)–(7), bounds an arbitrary continuous symmetric spectral functional by optimizing cosine-polynomial minorants and majorants. This is the direct predecessor of the proposed moment-dual calculation. Section III includes bounded errors in covariance lags, and Theorem 1 connects shrinking uncertainty to weak continuity. The paper also studies filter-bank tuning. Its general uncertainty viewpoint includes spectral lines and does not require choosing one fitted spectrum. It does not make acceleration-informed continuous-time displacement from the present finite Gaussian experiment its specific application. [Author manuscript, Sections III–IV](https://people.kth.se/~johan79/papers/KGTACversion_2submitted.pdf); [2013 publication record, DOI 10.1109/TAC.2013.2251775](https://experts.umn.edu/en/publications/uncertainty-bounds-for-spectral-estimation).

**Consequence for our claim:** neither the positive-measure formulation nor its cosine-polynomial dual is ours to claim as new.

## 2. Confidence calibration and continuum safety

Stark's strict-bounds framework optimizes properties of an unknown function over a set consistent with data and physical constraints. A statistical confidence set for the function yields simultaneous coverage for the resulting family of functional intervals. Conservative dual approximations can retain coverage when the continuum problem is solved numerically. A discretized primal model alone can produce intervals narrower than warranted. The 1992 paper develops this distinction; the author's later exposition explicitly describes simultaneous coverage and systematic-error sets. [Stark 1992, DOI 10.1029/92JB00739](https://agupubs.onlinelibrary.wiley.com/doi/abs/10.1029/92JB00739); [author's strict-bounds exposition](https://www.stat.berkeley.edu/~stark/Seminars/nsf-doe-98.htm).

**Consequence for our implementation:** a fine frequency grid is not a continuum certificate. Any between-grid correction, unbounded-frequency treatment, and floating-point tolerance must be explicit. In addition, a confidence level belongs to a stated sampling model and a calibrated common event, not merely to a plotted envelope.

## 3. What Lang–Lu proves, and what it does not

Lang and Lu's *Learning Memory Kernels in Generalized Langevin Equations* uses regularized Prony estimation and a weighted Sobolev loss. Assumptions 1–2 impose smooth, exponentially decaying kernels, correlations and derivatives, with positive Laplace-domain coercivity constants. Theorem 4.1 gives weighted-kernel identifiability. Theorem 4.2 bounds kernel error using global correlation error and force-correlation error including its derivative. When the force vanishes, the latter correlation is minus the velocity-correlation derivative, so this requirement reaches second derivatives of the velocity correlation. These are not finite-observation confidence intervals from a covariance vector. Section 6 leaves the connection between correlation-estimation error and trajectory counts, lengths, observation noise, and Prony parameters as future work. [Primary paper, Section 4 and Section 6](https://arxiv.org/html/2402.11705v2).

**Consequence for comparison:** we should not describe their result as failing because it does not promise a different guarantee. Nor should we use its identifiability theorem to justify extrapolation from finitely many noisy lags. The earlier singular fractional kernel is outside the literal smooth-kernel assumptions; tempering its long-time tail does not remove its singularity at zero.

## 4. The physical distinction in Benchmark 012

The new calculation changes the admissible physical information, not the foundations of optimization. For a normalized stationary velocity correlation with one-sided spectral measure,

$$
C(t)=\int_0^\infty\cos(\omega t)\,d\mu(\omega),
\qquad \int_0^\infty d\mu=1,
$$

the mean-square displacement is the bounded linear functional

$$
M(T)=\int_0^\infty
\frac{2[1-\cos(\omega T)]}{\omega^2}\,d\mu(\omega),
$$

with the continuous value $T^2$ at $\omega=0$. Under mean-square differentiability, an independently justified acceleration-variance bound supplies

$$
\int_0^\infty\omega^2\,d\mu(\omega)
=-C''(0)\le A.
$$

This is additional information, not something inferred for free from sampled velocities. In equilibrium linear response, a weak constant force gives a mean displacement proportional to $M(T)$; that interpretation needs the stated fluctuation–dissipation assumptions and does not extend automatically to nonlinear forcing or nonequilibrium data.

Benchmark 012 uses a free smooth exponential-memory target, $\gamma(t)=\kappa e^{-\nu t}$ with positive parameters, for which $-C''(0)=\kappa$ in the normalized units. It must not silently transfer the finite-acceleration assumption to the earlier fractional-memory target. A bound supplied from the known synthetic generator is an oracle input for testing the method, not an experimental acceleration measurement.

## 5. A testable application question, not a novelty claim

**Question:** at a fixed hardware and acquisition cost, when does independently measured acceleration information narrow a certified finite-horizon displacement interval more than collecting additional velocity trajectories at the original sampling interval?

The reason to test this comparison is structural. More independent paths reduce covariance-estimation uncertainty but do not remove the aliasing ambiguity of a fixed time lattice. A bound on high-frequency spectral mass can constrain a different part of the uncertainty. A finite number of off-grid observations can help, but does not automatically identify an unrestricted spectrum either.

A meaningful study would need all of the following:

- matched measurement budgets and a realistic instrument response, rather than treating acceleration as costless;
- acceleration uncertainty, bandwidth, and measurement noise included in the common confidence event or in conservative systematic-error allowances;
- adversarial spectra and deliberate violations of the assumed bound, not only the generating model;
- continuum-valid numerical certificates, distinguished from ordinary floating-point diagnostics;
- comparison with covariance-only and extra-sampling baselines at specified prediction horizons;
- a broader application-specific prior-art screen before making any originality claim.

The current result should therefore be called an **established-method application with explicit physical assumptions**. A genuine advance would require a nontrivial sharpness, robustness, measurement-design, or experimental result beyond the known framework.

## 6. Camera exposure: the next observation model

[[Benchmark 013 — Camera Exposure and Response Uncertainty]] follows established rectangular position-averaging and localization-noise models. [Savin and Doyle (2005), equations 6–9](https://web.mit.edu/doylegroup/pubs/BiophysJ-Savin05.pdf) give the shutter filter and MSD convolution. [Berglund (2010), equations 6–11](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=905460) describes shutter-weighted positions and the correlations created by localization noise. Its Brownian-motion likelihood is not a general likelihood for our memory-model family. The benchmark does not reproduce or outperform those full estimation procedures.

Finite-exposure inference with measurement-error confidence intervals is also established: [Relich, Olah, Cutler, and Lidke (2016)](https://doi.org/10.1103/PhysRevE.93.042401) develops Brownian diffusion estimation with blur, intermittent observations, and variable localization uncertainty. Only the abstract-level scope was checked in this screening pass; its full algorithms and comparisons remain unread and unreproduced. The [bibliographic record](https://pubmed.ncbi.nlm.nih.gov/27176323/) also links a publisher's note, which must be inspected before attempting reproduction.

[[Camera Exposure and Finite-Time Response Bounds]] gives full proofs of the elementary finite-velocity-variance blur inequality, an integer timing refinement, and a sharp special case. Those derivations are the checked local result. The targeted source search did not establish historical originality; absence of a matching search result is not evidence of novelty. The ignored-blur calculation is an intentional failure control, not a literature baseline. The ±20% transfer allowance is a declared assumption, not a newly inferred instrument property.
