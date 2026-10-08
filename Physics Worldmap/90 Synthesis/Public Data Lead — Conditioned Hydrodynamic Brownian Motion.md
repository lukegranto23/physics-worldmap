---
type: research-derivation
field: Statistical Physics
epistemic_status: effective
level: advanced
tags: [brownian-motion, hydrodynamic-memory, conditioning, public-data, observation-operator]
created: 2026-09-18
updated: 2026-09-18
note_maturity: expanded
source_audit: primary-paper-and-repository-metadata-reviewed-no-data-reproduction
---

# Public Data Lead — Conditioned Hydrodynamic Brownian Motion

> [!note] Update 2026-10-06
> Data acquired and digest-verified; the CSVs hold six traces, resolving the five-versus-six question. The preregistered reproduction is in [[Benchmark 014 — Preregistered Conditioned Brownian Reproduction]].

**Status:** a specific public-data candidate and a reconstructible mathematical baseline, not an experimental reproduction or a new physical discovery. The immediate question is whether a conditional-displacement result survives a measurement-matched Gaussian prediction and dependence-aware uncertainty calculation.

This extends [[Instrument Feasibility — Response Bounds Before Data Claims]] without pretending that optical photodetection is a rectangular camera exposure.

## What has actually been inspected

Boynewicz, Thumann, and Raizen report short-time $t^{5/2}$ displacement scaling after selecting near-zero initial velocities of an optically trapped particle in liquid. This is a **conditioned ensemble**, not a replacement for ordinary unconditioned equilibrium diffusion. The final article uses joint Gaussian conditioning in its theory. Its measurement chain includes split-beam photodetection, regularized inversion of a high-pass filter, 750 ns effective time resolution, and an eighth-order finite-difference velocity estimate. Methods describe six calibration traces; conditioning selects velocities within 1% of the measured standard deviation. [Final article, 4 February 2026, Results and Materials and Methods](https://raizenlab.ph.utexas.edu/pub/2026_superballistic_BM_liquid.pdf), [DOI](https://doi.org/10.1126/sciadv.aeb4579).

The [Dryad record](https://datadryad.org/dataset/doi:10.5061/dryad.pvmcvdnz4), dated 13 January 2026, lists particle and empty-trap position/velocity CSVs, `fitting.ipynb`, `conditioning.ipynb`, and a README. Its embedded documentation describes **five** independent traces per data file, at 750 ns spacing, and identifies the supplied traces as processed outputs of the fitting stage. Thus the six-versus-five trace discrepancy needs resolution; these should not be described as raw detector voltages. Actual file schemas, units, notebook implementation, and correspondence between files have not been inspected.

[Dryad's published terms, sections 1 and 4](https://datadryad.org/terms), specify CC0 release of deposited datasets and encourage reuse with scholarly credit. This is repository-level reuse evidence, not verification of every downloaded file's notices. The article itself states CC BY 4.0. No third-party data or notebook is redistributed in this checkpoint. The README download returned HTTP 403 through the retrieval tool; the embedded README was readable. No access restriction was bypassed.

## A baseline that can be derived before fitting anything

The following is standard Gaussian regression, independently reconstructed here. It is not a claimed new theorem or a competing explanation of the paper.

Let $V(t)$ be a real, centered, stationary Gaussian velocity with finite variance $c=C(0)>0$ and covariance $C(t)=\mathbb E[V(t)V(0)]$. Assume mean-square continuity at zero, and define the integrated displacement and two deterministic integrals:

$$
D(t)=\int_0^t V(s)\,ds,\qquad
A(t)=\int_0^t C(s)\,ds,\qquad
J(t)=\int_0^t(t-s)C(s)\,ds.
$$

Stationarity and integration give $\operatorname{Var}D=2J$ and $\operatorname{Cov}(D,V(0))=A$. The joint covariance is therefore

$$
\operatorname{Cov}\begin{pmatrix}D\\V(0)\end{pmatrix}
=\begin{pmatrix}2J&A\\A&c\end{pmatrix}.
$$

Write $D=(A/c)V(0)+Z$. The residual $Z$ is uncorrelated with $V(0)$ and, by joint Gaussianity, independent of it. Hence

$$
\mathbb E[D\mid V(0)=v]=\frac{A}{c}v,
\qquad \operatorname{Var}(D\mid V(0)=v)=2J-\frac{A^2}{c},
$$

$$
\boxed{\mathbb E[D^2\mid V(0)=v]
=2J-\frac{A^2}{c}+\frac{A^2v^2}{c^2}.}
$$

Conditioning on an exact value uses the Gaussian regular conditional distribution; it does not presume a positive probability of observing exactly zero. Positive semidefiniteness requires $2Jc\ge A^2$. A negative computed conditional variance signals inconsistent inputs or numerical error, not negative physical fluctuations. Integrating over $v\sim N(0,c)$ returns the unconditioned $2J$, which is a useful check.

### How the exponent changes

Suppose, on the model's small-time range,

$$
C(t)=c-a t^\alpha+o(t^\alpha),\qquad a>0,\quad0<\alpha\le1.
$$

Direct integration, rather than a fitted power law, yields

$$
A=ct-\frac{a}{\alpha+1}t^{\alpha+1}+o(t^{\alpha+1}),
\qquad
2J=ct^2-\frac{2a}{(\alpha+1)(\alpha+2)}t^{\alpha+2}
+o(t^{\alpha+2}).
$$

The ballistic terms cancel under exact zero-velocity conditioning:

$$
\boxed{\mathbb E[D^2\mid V(0)=0]
=\frac{2a}{\alpha+2}t^{\alpha+2}+o(t^{\alpha+2}).}
$$

A square-root covariance cusp ($\alpha=1/2$) therefore gives $(4a/5)t^{5/2}$; the exponential Ornstein–Uhlenbeck covariance has $\alpha=1$, $a=c/\tau$, and gives $(2c/3\tau)t^3$. Nonzero fixed $v$ restores a leading $v^2t^2$ contribution to the second moment. These statements concern the chosen observable and ensemble; the higher exponent does not mean a universal faster-than-ballistic transport law. Hydrodynamic incompressibility and finite detector bandwidth do not hold down to arbitrarily short physical times.

### Do not silently condition the initial position too

For a stationary trapped coordinate $X$, let $q=\operatorname{Var}X(0)$ and $B=\operatorname{Cov}(D,X(0))$. If $X(0)$ and $V(0)$ are uncorrelated and jointly Gaussian, conditioning **both** to zero gives variance $2J-A^2/c-B^2/q$, not just $2J-A^2/c$. At nonzero conditioning values the squared conditional mean must also be included.

For a stationary position with mean-square derivative $V$, stationarity gives $B=-J$ exactly. Since $J=ct^2/2+o(t^2)$, the additional subtraction starts at order $t^4$. It can still matter at finite experimental lags. Match the selection rule before comparing an entire curve. A derivation with $x(0)=0$ must not automatically be compared with an ensemble that only restricts estimated velocity.

## The detector changes the conditioning question

As a deliberately simplified example, let $W=V(0)+\eta$, where $\eta$ is independent, centered **Gaussian** noise with variance $n$. Then

$$
\mathbb E[D^2\mid W=0]=2J-\frac{A^2}{c+n}
=\frac{cn}{c+n}t^2+o(t^2)\quad(n>0).
$$

Imperfect selection leaves a ballistic term at the shortest times. Knowing the noise variance alone does **not** justify this identity for arbitrary non-Gaussian noise. Nor does this example describe a velocity obtained by differentiating the same noisy position record used for $D$; its errors are generally correlated with displacement errors and with nearby conditioning points.

There is a more useful measurement-level identity. Let $Y_j$ be the centered processed detector samples, and define measured displacement $D_k=Y_{j+k}-Y_j$ and a specified linear velocity proxy $W_j=\sum_\ell d_\ell Y_{j+\ell}$. For jointly Gaussian samples, set

$$
u_k=\operatorname{Var}D_k,\qquad
s=\operatorname{Var}W_j>0,\qquad
r_k=\operatorname{Cov}(D_k,W_j).
$$

Then the exact measured conditional second moment is

$$
\mathbb E[D_k^2\mid W_j=w]
=u_k-\frac{r_k^2}{s}+\frac{r_k^2w^2}{s^2}.
$$

This automatically retains noise correlations and stencil overlap **if** the covariance used really describes the complete processed observation channel. For a finite symmetric bin $|W_j|\le b$, replace $w^2$ by the corresponding truncated-Gaussian second moment. With $z=b/\sqrt s$, standard-normal density $\varphi$, and distribution function $\Phi$,

$$
\mathbb E[W_j^2\mid |W_j|\le b]
=s\left[1-\frac{2z\varphi(z)}{2\Phi(z)-1}\right].
$$

The $b\to0$ and $b\to\infty$ limits recover exact-zero conditioning and the unconditioned second moment respectively. Tiny-bin evaluation needs stable arithmetic; direct subtraction can lose precision.

## A connection to the earlier identifiability work

For a centered Gaussian observation process, its covariance determines every finite-dimensional distribution, including the conditional statistic above. **Conditioning cannot distinguish two models that already have identical laws for those same observed samples.** Changing the measured channel or acquiring finer-time information can distinguish them; relabeling a statistic cannot.

This is an application of established Gaussian probability and the information boundary studied in [[Benchmark 002 — The Sampling Boundary of Prediction]], not a denial of the experimental value of conditional ensembles. Conditioning can expose a physically interpretable contribution hidden in an unconditional average. It does not, by itself, create independent evidence beyond the complete Gaussian observation law.

## Concrete next experiment, with failure criteria

1. **Acquisition and provenance:** use a permitted repository download route, record version, file hashes, notices, shapes, units, and trace mapping. Resolve five versus six traces before attributing an exact reproduction. Preserve the distinction between detector raw data, processed positions, and derived velocities.
2. **Observation reconstruction:** inspect the notebooks as text before executing them. Record differencing coefficients, edge treatment, filtering, downsampling, deconvolution, regularization, and any model-based calibration. A calibration fitted to hydrodynamic theory is not independent confirmation of that theory.
3. **Frozen comparison:** declare lag range, conditioning-bin widths, position selection, and exclusion rules before examining conditional residuals. Estimate covariance on disjoint calibration material where possible, then predict held-out conditional means and second moments with the measurement-level identity. Account for any fitting performed jointly across traces; nominal trace splitting cannot undo shared preprocessing.
4. **Dependence and controls:** retain whole-trace structure, examine block-length sensitivity, propagate covariance/calibration estimation error, and process empty-trap references with the same pipeline. Overlapping starts and bins are not independent trials. Five traces alone do not justify a high-precision uncertainty claim.
5. **Decision:** agreement would be a scoped reproduction of Gaussian conditional physics. Persistent disagreement first triggers processing, noise-transfer, nonstationarity, selection, and Gaussian-assumption checks—not an announcement of new forces. Demonstrated higher-order structure beyond a validated Gaussian observation model would justify a separate, prospectively specified research question.

No data-analysis result, numerical coverage guarantee, or improvement over the published method is claimed here. The mathematical identities have been derived and independently reviewed; the proposed external-data checks have not been run.

[[Instrument Feasibility — Response Bounds Before Data Claims]] · [[Research Frontier — Identifiability Before Discovery]] · [[Synthesis Lab]] · [[Source and Citation Policy]]
