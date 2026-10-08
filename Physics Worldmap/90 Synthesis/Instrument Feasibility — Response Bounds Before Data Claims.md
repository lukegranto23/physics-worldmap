---
type: research-derivation
field: Statistical Physics
epistemic_status: effective
level: advanced
tags: [instrument-feasibility, particle-tracking, motion-blur, calibration, inertial-brownian-motion, research-gates]
created: 2026-09-17
updated: 2026-09-18
note_maturity: expanded
source_audit: two-primary-experiments-scoped-metadata-review-with-explicit-conditional-calculations
---

# Instrument Feasibility — Response Bounds Before Data Claims

Two real experiments clarify the next research gate. A conventional camera study has usable exposure metadata but lacks a verified mass bound in the inspected report; conditional calculations indicate that the general finite-velocity blur allowance would be extremely loose. A high-bandwidth optical experiment supplies inertial scales, but its detector is not a camera and its velocity-averaging time cannot be substituted for a position shutter.

**Neither is currently a fully specified external-data validation of Benchmark 013.** This is a feasibility and evidence audit, not a reanalysis of raw trajectories, an experimental result, a hardware recommendation, or a novelty claim.

Read with [[Benchmark 013 — Camera Exposure and Response Uncertainty]] and [[Camera Exposure and Finite-Time Response Bounds]].

## 1. What must be small, and what must be known

Let $T$ denote the displacement lag, $h$ a verified rectangular **position exposure**, and $c=C_v(0)$ the physical one-coordinate velocity variance. For the unblurred half-MSD $J(T)$, the bound established in the linked derivation is

$$
B(h)=\frac{c h^2}{6},\qquad
0\le J(T)-\overline J(T,h)\le B(h).
$$

Thus a necessary screening condition for this particular additive allowance to consume at most a fraction $\epsilon$ of the target is

$$
h\le\sqrt{\frac{6\epsilon J(T)}{c}}.
$$

This is not a sufficient condition for an informative confidence interval: noise, calibration transfer, statistical uncertainty, and uncertainty in $c$ still contribute. A point estimate of particle mass is not an upper confidence bound on velocity variance.

For a homogeneous sphere in an unbounded Newtonian fluid, the **conditional Stokes/equipartition estimate** is

$$
m=\frac{4\pi}{3}\rho_p a^3,\quad
\gamma=6\pi\eta a,\quad
\tau_m=\frac{m}{\gamma}=\frac{2\rho_p a^2}{9\eta},\quad
c=\frac{k_B\Theta}{m},\quad D=\frac{k_B\Theta}{\gamma}.
$$

Here $\Theta$ is bath temperature, $a$ particle radius, and $\eta$ dynamic viscosity. If an approximately free diffusive interval exists with $J(T)\simeq DT$, then

$$
\frac{B}{J}\simeq\frac{h^2}{6\tau_m T}.
$$

Do not use this approximation in a ballistic interval or after an optical trap has caused the MSD to plateau. Hydrodynamic memory also makes $\tau_m$ a scale, not necessarily an exponential correlation-decay time.

## 2. Published observation channels: do not merge these columns

| Quantity | Savin–Doyle, 2005: camera | Kheifets et al., 2014: optical detector |
|---|---|---|
| Selected physical case | Fluorescent beads, diameter 0.925 µm, in water at 23°C; viscosity approximately 1 mPa s | Barium-titanate-glass bead in acetone; fitted diameter $3.72\pm0.06$ µm; temperature 291 K |
| Readout | Hitachi KP-M1A CCD; horizontal tracking of interlaced fields at 60 Hz | Split-beam balanced photodetection; reported bandwidth above 50 MHz |
| Reported temporal quantities | Actual shutters $1/60,1/125,1/250,1/500$ s; fitted MSD lags $1/60$ to 0.1 s | $\tau_p=11.0$ µs, $\tau_f=8.5$ µs; **velocity** averaging 0.16 µs |
| Quantity not supplied by that entry | Verified bead mass/density | Equivalent rectangular position-shutter duration |

Sources: [Savin–Doyle, Methods and Newtonian-fluid results](https://pmc.ncbi.nlm.nih.gov/articles/PMC1305040/); [Kheifets et al., pp. 1494–1495 and Figures 2–3](https://raizenlab.ph.utexas.edu/pub/kheifets_science.pdf). The original PDF pages were visually checked: the optical averaging time is **0.16 µs**, not 0.16 ms.

## 3. Camera calculation: a density-parameterized rejection test

The camera paper does not provide a bead mass or density in the inspected methods. No manufacturer product identity has been established here, so a density has **not** been assigned to those experimental beads.

Instead define the explicit sensitivity parameter

$$
R=\frac{\rho_p}{1000\,\mathrm{kg}\,\mathrm{m}^{-3}}.
$$

Using the reported radius and approximate water viscosity in the conditional spherical Stokes model gives

$$
m=(4.1440\times10^{-16})R\,\mathrm{kg},\qquad
\tau_m=(4.7535\times10^{-8})R\,\mathrm{s},
$$

$$
c=\frac{9.8667\times10^{-6}}{R}\,\mathrm{m}^2\,\mathrm{s}^{-2},
\qquad D\simeq0.4690\,\mu\mathrm{m}^2\,\mathrm{s}^{-1}.
$$

These are our **conditional calculations**, not fitted or measured values quoted from the experiment. In particular, $R=1$ below is a numerical reference, not a claim about bead composition. The diffusion estimate comes from Stokes–Einstein, not from digitizing a published MSD curve.

| Reported shutter $h$ | Reported-range lag $T$ | Model half-MSD $DT$, µm² | Additive allowance $B$, µm² | Ratio $B/(DT)$ |
|---:|---:|---:|---:|---:|
| 0.002 s | $1/60$ s | 0.007817 | $6.578/R$ | $841.5/R$ |
| 0.002 s | 0.1 s | 0.04690 | $6.578/R$ | $140.2/R$ |
| $1/60$ s | $1/60$ s | 0.007817 | $456.8/R$ | $58436.8/R$ |

At the reference $R=1$, keeping this allowance below 10% of $DT$ would require approximately **21.8 µs** exposure at $T=1/60$ s, or **53.4 µs** at $T=0.1$ s. These are calculated requirements, not available shutter settings or proposed instrument specifications. They scale as $\sqrt R$ under this model.

The large allowance is not the actual blur: for ideal diffusive position, the familiar model correction is $Dh/3$ in half-MSD. Its smallness does not prove the much broader spectral certificate is informative. Conversely, a loose certificate does not invalidate the published camera experiment.

The integer-ratio refinement does not automatically save the proposal. At $T=h=1/60$ s and $R=1$, substituting $\overline J\simeq D(T-h/3)$ into the sharp conditional upper bound $h\sqrt{c\overline J/2}$ still gives an upper endpoint roughly **342 times** $DT$. This is another model screening calculation, not an empirical identification interval.

**Decision:** do not apply nominal 95% camera bounds to this study using an invented density. Even under the displayed reference assumptions, the general guarantee is too loose to support a precision claim at these lags.

## 4. High-bandwidth calculation: promising scale, wrong observation operator

For the selected optical case, the reported hydrodynamic velocity normalization is $(0.180\,\mathrm{mm}\,\mathrm{s}^{-1})^2$, and the fitted trap stiffness is $K=(3.2\pm0.2)\times10^{-4}\,\mathrm{N}\,\mathrm{m}^{-1}$. The MSD plateaus under confinement before a purely diffusive regime is reached. [Kheifets et al., Figure 2 and adjacent text](https://raizenlab.ph.utexas.edu/pub/kheifets_science.pdf)

Using those rounded fitted quantities gives the **model-derived** effective mass and plateau half-MSD

$$
c_* =3.24\times10^{-8}\,\mathrm{m}^2\,\mathrm{s}^{-2},\qquad
m_* =\frac{k_B(291\,\mathrm{K})}{c_*}\simeq1.24\times10^{-13}\,\mathrm{kg},
$$

$$
J_{\mathrm{plateau}}=\frac{k_B(291\,\mathrm{K})}{K}
\simeq1.26\times10^{-17}\,\mathrm{m}^2.
$$

The last expression uses equilibrium harmonic confinement; it is not a digitized measurement or a free-particle $DT$ extrapolation.

Trapping does not itself invalidate the equilibrium response connection: for a weak force conjugate to the actual coordinate $X$, the step susceptibility can still be $\beta J(T)$. It changes the function $J(T)$ and invalidates unqualified free-diffusion scaling. A perturbation of detector voltage is not automatically that conjugate mechanical force.

There is also a mass-convention issue. Within the incompressible hydrodynamic sphere model,

$$
m_*=m_p+m_a,\qquad
\frac{m_a}{m_p}=\frac{\tau_f}{9\tau_p}\simeq0.08586.
$$

Thus the same fitted-model values imply $m_p\simeq1.14\times10^{-13}$ kg. If bare-particle classical equipartition is the intended velocity convention, its variance would be approximately $3.52\times10^{-8}\,\mathrm{m}^2\,\mathrm{s}^{-2}$, not $c_*$. Neither rounded normalization is a demonstrated confidence ceiling covering an unspecified microscopic frequency range. The physical variable and validity of its mass model must be specified before importing a global spectral bound.

For orientation only, a **hypothetical rectangular position channel** using these two reference variance conventions would need $h\lesssim14.6$–$15.2$ µs for $B\le0.1J_{\mathrm{plateau}}$. This is a counterfactual filter requirement, not a bound on the actual detector's bias.

The published 0.16 µs velocity average and the detector bandwidth do not determine that hypothetical $h$. A detector transfer function, AC/DC-channel combination, and digital processing can differ fundamentally from a nonnegative rectangular position shutter. We therefore calculate **no actual-camera blur fraction for this experiment**. In particular, neither $h=0.16$ µs nor $h=1/(50\,\mathrm{MHz})$ is inserted into the camera theorem.

**Decision:** the inertial scales justify investigating the real detector operator, not relabeling photodetection as camera tracking. A generalized filter-specific bound would be needed before reusing this channel.

## 5. Access, calibration, independence, and reuse gates

For the camera study, fixed-bead calibration and matching of noise-to-signal conditions are described. The ensemble uses fragments of recorded trajectories; it is not the independent-pair construction in Benchmark 013. No raw-trajectory archive or permissive data license was located in the inspected article. The article carries Biophysical Society copyright. [Savin–Doyle, Methods, fixed-bead results, and article notice](https://pmc.ncbi.nlm.nih.gov/articles/PMC1305040/)

For the optical study, the reported records are 0.35-second trajectories, with uncertainty assessed through ten subtrajectory fits. Empty-trap noise was measured at matched detection power. The paper offers raw data and analysis code **upon request** and carries an AAAS personal/noncommercial-use notice; a reusable data license is not established. [Kheifets et al., pp. 1494–1496 and title-page notice](https://raizenlab.ph.utexas.edu/pub/kheifets_science.pdf)

No author was contacted, no raw dataset was acquired, and no external files are redistributed in this note. “Not located” describes this scoped inspection, not proof that an archive does not exist elsewhere.

For either experiment, the following remain separate requirements:

1. Obtain the actual observation/filter metadata and its uncertainty, with timing units verified; field rate or bandwidth is not shutter duration.
2. Establish a justified $C_v(0)$ upper bound, including mass, temperature, and model-convention uncertainty rather than only nominal central values.
3. Obtain raw trajectories and a matched noise reference with permission for the intended reuse; quantify a calibration-transfer envelope rather than assuming the ±20% development value.
4. Reconstruct statistical dependence. Displacement pairs sharing positions or physical time are not automatically independent Gaussian samples; subdividing a movie does not create the chi-square degrees of freedom used in Benchmark 013.
5. Check whether the resulting physical-unit intervals can be useful before any coverage demonstration, and compare against a published instrument-aware analysis under matched assumptions.

## 6. Research consequence

The immediate contribution is a rejection gate: do not spend another synthetic sweep disguising an uninformative physical allowance or an unspecified detector as an external validation. The camera example calls for a stronger, physically justified spectral restriction or a sharper camera-specific method. The optical example calls for a measured transfer-function treatment and a dependence-aware statistical construction.

The numerical requirements above are feasibility estimates conditional on explicit models. They establish neither a new physical law nor a demonstrated improvement over existing particle-tracking methods.

A distinct newer public-data candidate is examined in [[Public Data Lead — Conditioned Hydrodynamic Brownian Motion]]. The present two-experiment audit makes no claim that public Brownian-motion data are unavailable in general. Any new candidate still needs its own observation-operator, processing, statistical-dependence, and reuse-permission audit.

Primary papers: [Savin and Doyle, *Static and Dynamic Errors in Particle Tracking Microrheology* (2005), DOI 10.1529/biophysj.104.042457](https://doi.org/10.1529/biophysj.104.042457); [Kheifets et al., *Observation of Brownian Motion in Liquids at Short Times: Instantaneous Velocity and Memory Loss* (2014), DOI 10.1126/science.1248091](https://doi.org/10.1126/science.1248091).

[[Camera Exposure and Finite-Time Response Bounds]] · [[Benchmark 013 — Camera Exposure and Response Uncertainty]] · [[Prior Art — Spectral Bounds and Physical Response]] · [[Research Frontier — Identifiability Before Discovery]] · [[Synthesis Lab]]
