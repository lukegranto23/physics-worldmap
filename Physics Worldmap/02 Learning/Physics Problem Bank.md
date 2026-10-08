---
type: problem-bank
field: Physics
epistemic_status: reference
level: all
tags: [physics, learning, problems, recall]
created: 2026-07-30
updated: 2026-07-30
---

# Physics Problem Bank

Use [[Problem Solving Protocol]]. Predict the sign, scaling, and order of magnitude before calculation. The checks are not complete solutions.

## Foundations and mathematical structure

### P01 — Dimensionless pendulum

A simple pendulum's period may depend on length $L$, mass $m$, gravity $g$, and small initial angle $\theta_0$. Use dimensional analysis to constrain the form. Which part cannot be obtained from dimensions?

> [!check]- Check
> $T=\sqrt{L/g}\,F(\theta_0)$; mass drops out. Dimensional analysis cannot determine the dimensionless function or the small-angle factor $2\pi$.

### P02 — Covariance propagation

Two calibrated measurements $x$ and $y$ have covariance matrix $\Sigma$. Derive the first-order variance of $f=x/y$ and identify the sign of the covariance term.

> [!check]- Check
> Use $\nabla f=(1/y,-x/y^2)$. Then $\sigma_f^2=\nabla f^T\Sigma\nabla f$ and the cross term is $-2x\,\operatorname{cov}(x,y)/y^3$.

### P03 — Symmetry audit

For $L=\tfrac12m(\dot x^2+\dot y^2)-V(\sqrt{x^2+y^2})$, identify three continuous symmetries or cyclic structures and their conserved quantities.

> [!check]- Check
> Time translation gives energy; planar rotations give angular momentum; if the potential is absent, spatial translations give momentum. For a nonconstant central potential, translations are broken.

### P04 — Green-function boundary choice

Explain why the equation $LG=\delta$ does not define a unique Green function. Give two physical choices for the wave operator.

> [!check]- Check
> Homogeneous solutions can be added. Boundary or causal conditions select retarded, advanced, Feynman, outgoing, periodic, Dirichlet, and other Green functions.

## Classical mechanics, waves, and continua

### P05 — Orbit scaling

Use Newtonian gravity and dimensional analysis to derive the scaling of orbital period with semimajor axis for fixed central mass.

> [!check]- Check
> $T\propto a^{3/2}/\sqrt{GM}$; the exact Kepler result is $T^2=4\pi^2a^3/(GM)$.

### P06 — Normal modes

Two equal masses $m$ are connected in a line by three equal springs $k$ between fixed walls. Write the stiffness matrix and obtain both mode frequencies.

> [!check]- Check
> $K=k\begin{pmatrix}2&-1\\-1&2\end{pmatrix}$; eigenvalues are $k$ and $3k$, so $\omega=\sqrt{k/m}$ and $\sqrt{3k/m}$.

### P07 — Resonance and causality

For the damped oscillator susceptibility $\chi(\omega)=1/[m(\omega_0^2-\omega^2-2i\gamma\omega)]$, relate pole location, ringdown, linewidth, and causal response.

> [!check]- Check
> Stable poles lie in the lower half complex-frequency plane under the stated Fourier convention; decay rate is $\gamma$ in the underdamped regime and the response linewidth is of order $2\gamma$.

### P08 — Boundary-layer estimate

Balance streamwise advection and transverse viscous diffusion over a flat plate to estimate laminar boundary-layer thickness.

> [!check]- Check
> $U^2/L\sim\nu U/\delta^2$, so $\delta/L\sim Re_L^{-1/2}$. The numerical coefficient and downstream dependence require the similarity solution.

### P09 — Shock admissibility

Mass and momentum jump conditions allow multiple discontinuities. What additional physical condition selects an ordinary compressive shock?

> [!check]- Check
> Entropy must increase across the shock; characteristics enter rather than emerge from an admissible compressive shock under the usual hyperbolic conservation law.

## Electromagnetism and optics

### P10 — Capacitor energy routes

Derive parallel-plate capacitor energy both from $U=\tfrac12QV$ and by integrating electromagnetic energy density. State the neglected edge effect.

> [!check]- Check
> With $E=V/d$, $u=\epsilon_0E^2/2$, and volume $Ad$, the field energy is $\epsilon_0AV^2/(2d)=CV^2/2$ for $C=\epsilon_0A/d$. Fringing is neglected.

### P11 — Plane-wave geometry

Starting from source-free Maxwell equations, show that a monochromatic plane wave is transverse and obtain $B_0/E_0$.

> [!check]- Check
> $\mathbf k\cdot\mathbf E_0=\mathbf k\cdot\mathbf B_0=0$ and $\mathbf B_0=(\mathbf k\times\mathbf E_0)/\omega$, so $B_0=E_0/c$ in vacuum.

### P12 — Diffraction resolution

Estimate the smallest lateral feature resolvable by a conventional far-field optical system with wavelength $\lambda$ and numerical aperture NA. What assumption makes “resolution limit” nonabsolute?

> [!check]- Check
> A common Rayleigh scale is $0.61\lambda/\mathrm{NA}$. Priors, near fields, nonlinear response, structured illumination, sparsity, and the chosen discrimination criterion alter what can be inferred.

### P13 — Gauge-invariant phase

Explain why potentials can affect interference even in a region where local $\mathbf E$ and $\mathbf B$ vanish, without making gauge choice observable.

> [!check]- Check
> The closed-loop phase depends on the gauge-invariant flux $\oint\mathbf A\cdot d\mathbf l=\int\mathbf B\cdot d\mathbf A$; open-path phases transform with endpoint matter phases.

## Relativity and gravitation

### P14 — Twin paths

Two clocks depart and reunite. One follows a piecewise inertial high-speed path; the other remains approximately inertial. Compute elapsed proper times and explain why no frame-symmetry paradox remains.

> [!check]- Check
> Integrate $d\tau=dt\sqrt{1-v^2/c^2}$ along each worldline. The paths between the same reunion events are not symmetric; acceleration marks the turnaround but path-dependent proper time is the invariant explanation.

### P15 — Photon sphere scale

For Schwarzschild spacetime, dimensional reasoning gives characteristic radii proportional to $GM/c^2$. Look up or derive the photon-sphere radius and compare it with the horizon.

> [!check]- Check
> $r_{\rm ph}=3GM/c^2$ and $r_s=2GM/c^2$ in Schwarzschild coordinates. The photon sphere is unstable and outside the horizon.

### P16 — Weak gravitational redshift

Expand the stationary metric result for two clocks separated by small Newtonian potential difference $\Delta\Phi$.

> [!check]- Check
> $\Delta\nu/\nu\approx\Delta\Phi/c^2$ to first order, with sign determined by which clock is deeper in the potential.

### P17 — Inspiral chirp

Explain qualitatively why a compact binary's gravitational-wave frequency and amplitude rise as it loses energy.

> [!check]- Check
> Negative binding energy becomes more negative as separation shrinks; orbital speed and frequency increase. The quadrupole radiation strength rises with faster, more compact motion until strong-field merger.

## Quantum mechanics and information

### P18 — Well-width scaling

If an infinite well width doubles, how do its energies, momentum scale, and characteristic revival times change?

> [!check]- Check
> $E_n\propto L^{-2}$ and $p_n\propto L^{-1}$. Times built from $\hbar/E$ scale as $L^2$.

### P19 — Superposition versus mixture

Construct a measurement that distinguishes $(|0\rangle+|1\rangle)/\sqrt2$ from the equal incoherent mixture.

> [!check]- Check
> Measure in the $|+\rangle,|-\rangle$ basis. The superposition gives $+$ with unit probability; the mixture gives equal probabilities.

### P20 — Entangled subsystem

Trace one qubit out of $(|00\rangle+|11\rangle)/\sqrt2$ and compute purity and entropy of the reduced state.

> [!check]- Check
> $\rho_A=I/2$, purity $\operatorname{Tr}\rho_A^2=1/2$, and entropy $\ln2$ with natural logarithm.

### P21 — Tunneling sensitivity

Use WKB to explain why a modest barrier-width change can alter a decay rate by orders of magnitude.

> [!check]- Check
> $T\sim\exp[-2\int\sqrt{2m(V-E)}\,dx/\hbar]$; width enters the exponent, not merely a prefactor.

### P22 — Adiabatic failure

A two-level gap becomes very small during a parameter ramp. Which combination controls transition probability and why can “slow” be insufficient?

> [!check]- Check
> Matrix elements of $\dot H$ relative to gap squared control adiabaticity. Near a closing gap, the required ramp time can diverge.

### P23 — Bell logic

List assumptions entering a Bell inequality and state precisely what a loophole-free violation excludes.

> [!check]- Check
> Typical assumptions include locality/factorization, measurement-setting independence, and valid outcome sampling. Violations exclude models satisfying the tested joint assumptions; they do not enable signaling or pick one ontology.

## Thermodynamics and statistical physics

### P24 — Carnot bound

Derive the reversible engine efficiency using zero total entropy change for two reservoirs.

> [!check]- Check
> $Q_H/T_H=Q_C/T_C$ and $W=Q_H-Q_C$, so $\eta=1-Q_C/Q_H=1-T_C/T_H$.

### P25 — Canonical fluctuation

Derive $\operatorname{Var}(E)=k_BT^2C_V$ from the partition function.

> [!check]- Check
> $\langle E\rangle=-\partial_\beta\ln Z$ and $\operatorname{Var}(E)=\partial_\beta^2\ln Z=-\partial_\beta\langle E\rangle=k_BT^2\partial_T\langle E\rangle$.

### P26 — Entropy and coarse-graining

Give an example where fine-grained entropy remains constant while a coarse entropy increases.

> [!check]- Check
> Hamiltonian phase-space density preserves fine-grained Gibbs entropy under Liouville flow while filamentation makes a finite-resolution coarse distribution appear more mixed.

### P27 — Critical finite size

Why does a finite Ising lattice have no true nonanalytic free-energy transition, and how can a critical point still be estimated?

> [!check]- Check
> A finite partition function is a finite analytic sum. Use finite-size scaling of susceptibility peaks, Binder cumulant crossings, correlation length, or data collapse.

### P28 — Fluctuation-response audit

Design a test of equilibrium fluctuation-dissipation behavior for a trapped colloid.

> [!check]- Check
> Measure spontaneous position spectrum and the linear response to a weak calibrated force over frequency, with temperature, trap stiffness, hydrodynamics, and detector noise controlled.

## Matter, AMO, plasma, and nuclei

### P29 — Bloch equivalence

Why are $\mathbf k$ and $\mathbf k+\mathbf G$ physically equivalent labels up to a periodic-factor convention?

> [!check]- Check
> They have the same eigenvalue under every lattice translation because $e^{i\mathbf G\cdot\mathbf R}=1$.

### P30 — Superconducting flux

Combine single-valued condensate phase with gauge coupling to obtain a quantized flux scale for charge-$2e$ pairs.

> [!check]- Check
> $\oint(\hbar\nabla\phi-2e\mathbf A)\cdot d\mathbf l$ is constrained; deep in a thick ring where superflow vanishes, $\Phi=n h/(2e)$.

### P31 — Ramsey linewidth

Why can two short separated pulses resolve a frequency much more narrowly than either pulse alone?

> [!check]- Check
> The free-evolution time $T$ accumulates phase $\Delta T$, producing fringes spaced by order $1/T$; pulse duration mainly sets the broad envelope.

### P32 — Plasma scale choice

For a given density, temperature, magnetic field, and size, calculate Debye length, Larmor radius, plasma frequency, collision time, and mean free path. Use their ordering to choose kinetic, two-fluid, or MHD modeling.

> [!check]- Check
> No universal answer: the reasoning is the result. MHD needs system scales much larger than relevant kinetic scales and a defensible closure; collisionless resonances require a kinetic distribution.

### P33 — Nuclear stability

Use the semiempirical mass formula qualitatively to explain why stable heavy nuclei require more neutrons than protons.

> [!check]- Check
> Coulomb repulsion grows strongly with proton number, while the asymmetry term penalizes neutron-proton imbalance; the minimizing compromise shifts to $N>Z$ for heavy nuclei.

### P34 — EFT remainder

An observable is calculated through order $(E/\Lambda)^2$ with coefficients of natural size and $E/\Lambda=0.1$. Estimate the next-order truncation scale and state two reasons the estimate may fail.

> [!check]- Check
> If the next omitted order is cubic, a nominal relative scale is $10^{-3}$. Large coefficients, symmetry suppression, nearby thresholds, logarithms, or breakdown of scale separation can change it.

## Astrophysics, cosmology, Earth, and life

### P35 — Virial contraction

Why can a self-gravitating idealized star heat up when it loses total energy?

> [!check]- Check
> With $2K+U=0$, total $E=U/2=-K$. Making $E$ more negative increases $K$, raising characteristic temperature while the system contracts.

### P36 — Expansion scalings

Derive density scaling with scale factor for matter, radiation, and vacuum energy.

> [!check]- Check
> From continuity, $\rho\propto a^{-3(1+w)}$: matter $a^{-3}$, radiation $a^{-4}$, vacuum constant.

### P37 — Dark-matter inference

For rotation curves, lensing, CMB, and structure growth, state the observable and the model-dependent step between it and “dark matter.”

> [!check]- Check
> Each measures velocities, image distortions, anisotropies, or clustering. Inferring a nonbaryonic component uses gravity, geometry, baryonic models, and a cosmological framework; convergence across different systematics is the strength.

### P38 — Climate forcing and feedback

In a one-box energy-balance model $C\dot T=F-\lambda T$, solve the step response and identify equilibrium warming and response time.

> [!check]- Check
> $T(t)=(F/\lambda)[1-e^{-t/\tau}]$ for $\tau=C/\lambda$ with the stated positive-feedback-parameter convention. Sign conventions for $\lambda$ differ, so declare one.

### P39 — Diffusion-limited sensing

Why does averaging longer improve a concentration estimate only as a square root under independent-sample assumptions? What biological features break independence?

> [!check]- Check
> Effective sample count grows linearly with time, so standard error falls as $N^{-1/2}$. Rebinding, receptor correlations, active feedback, transport, and environmental dynamics reduce or restructure independent information.

### P40 — Reaction-diffusion pattern

Linearize a two-species reaction-diffusion model and explain how diffusion can destabilize a stable well-mixed fixed point.

> [!check]- Check
> For Fourier mode $k$, analyze eigenvalues of $J-k^2D$. Unequal diffusion can make an eigenvalue positive for a finite $k$ even when eigenvalues of $J$ have negative real parts.

## Experiment, computation, and synthesis

### P41 — Discovery significance

A scan reports a local $5\sigma$ excess. List the steps needed before calling it evidence for a new particle.

> [!check]- Check
> Global trials factor, nuisance/systematic model, calibration, background alternatives, effect size, channel consistency, independent data, reproducible pipeline, and a theory-consistent parameter region.

### P42 — Grid-convergence test

Three simulations at spacings $h$, $h/2$, and $h/4$ approach a common result. Estimate observed convergence order without knowing the exact solution.

> [!check]- Check
> For asymptotic errors $Ch^p$, use $p\approx\log_2[(Q_h-Q_{h/2})/(Q_{h/2}-Q_{h/4})]$, with sign/monotonicity and regime checks.

### P43 — Conservation is not validation

A numerical integrator conserves energy to machine precision. Give three ways the physical prediction can still be wrong.

> [!check]- Check
> Wrong Hamiltonian or parameters; timestep too coarse but structure preserving; wrong boundary or initial data; another observable inaccurate; comparison outside model validity.

### P44 — Analogy promotion

Two fields use the same differential equation. What must be checked before calling the systems equivalent?

> [!check]- Check
> Map degrees of freedom, observables, units, boundary/initial conditions, noise, symmetries, nonlinear corrections, parameter regime, and allowed interventions. Shared mathematics may be only an analogy.

### P45 — Build a falsifier

Choose one prompt from [[Research Question Incubator]]. Write the baseline, minimal modification, derived quantitative difference, nuisance that can imitate it, and an outcome that lowers confidence.

> [!check]- Check
> There is no single numerical answer. Reject cards without a baseline prediction, operational observable, uncertainty budget, and explicit adverse outcome.

## Navigation

- [[Physics Worldmap|Home]]
- [[Learning Paths|Learning paths]]
