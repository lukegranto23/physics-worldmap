---
type: "concept"
field: "Cosmology"
epistemic_status: "open"
level: "advanced"
tags: ["physics", "field/cosmology", "status/open", "level/advanced"]
aliases: []
created: 2026-07-30
updated: 2026-07-30
note_maturity: expanded
source_audit: bibliography-present-needs-claim-audit
---

# Hubble Tension

> [!summary] Core idea
> Some early- and late-universe inferences of the present expansion rate disagree beyond expected uncertainties, with cause unsettled.

> [!note] Documentation status
> This expanded note includes a canonical bibliography but has not yet received a claim-by-claim source audit. The epistemic label describes the standing of the underlying physics in its stated regime; it does not certify every sentence or equation in this note.

## Mathematical handle

$H_0^{\rm early}\ne H_0^{\rm late}$ statistically

The expression is an orientation point, not a substitute for checking assumptions, sign conventions, units, boundary conditions, and the regime in which it was derived.

## Epistemic status

**Open.** This is unresolved. Competing explanations or incomplete evidence must remain visible.

## Place in the world map

- Domain: [[Cosmology Map]]
- Field-level guiding question (context only): “What are dark matter and dark energy?”
- Nearby concepts: [[Physics Worldmap]] · [[Cosmology Map]] · [[Cosmological Constant Problem|← previous]] · [[Reionization|next →]]

## Physical content

The Hubble tension is the statistically significant disagreement between two classes of measurements of the present-day expansion rate of the universe, parametrized by the Hubble constant $H_0$. Measurements anchored in the early universe (using the [[Cosmic Microwave Background|CMB]] as calibrated by the $\Lambda$CDM cosmological model) consistently yield a lower value, while measurements based on the local distance ladder (using Cepheids, [[Supernovae|Type Ia Supernovae]], and other astrophysical distance indicators) yield a higher value. The discrepancy has grown in significance over the past decade and currently stands at roughly $4$--$6\sigma$ depending on the datasets compared.

The two headline numbers are:

- **Planck CMB (early universe)**: $H_0 = 67.36 \pm 0.54$ km/s/Mpc (Planck Collaboration, 2018). This value is not a direct measurement of the present expansion rate but is inferred by fitting the $\Lambda$CDM model to the detailed pattern of CMB temperature and polarization anisotropies. The acoustic peak positions, heights, and damping tail constrain the cosmological parameters jointly, and $H_0$ is extracted as part of this global fit.

- **SH0ES distance ladder (late universe)**: $H_0 = 73.04 \pm 1.04$ km/s/Mpc (Riess et al., 2022). This measurement uses a three-rung distance ladder: geometric parallaxes (from HST and Gaia) calibrate Cepheid period-luminosity relations in nearby galaxies, Cepheids then calibrate [[Supernovae|Type Ia supernova]] peak luminosities in galaxies at intermediate distances, and finally the calibrated supernovae measure $H_0$ from the Hubble flow at cosmological distances.

The difference of $\sim 5.7$ km/s/Mpc, while small in absolute terms ($\sim 8\%$), is large relative to the quoted uncertainties. If both measurements are correct and their error budgets are reliable, this discrepancy requires an explanation beyond the standard $\Lambda$CDM model.

Multiple independent local measurements support the higher value. The H0LiCOW/TDCOSMO program uses strong gravitational lensing time delays to measure $H_0 = 73.3^{+1.7}_{-1.8}$ km/s/Mpc, independent of the distance ladder. The Megamaser Cosmology Project obtains $H_0 = 73.9 \pm 3.0$ km/s/Mpc from geometric maser distances to galaxies in the Hubble flow. Surface brightness fluctuation methods also favor the high end.

However, there are also "intermediate" measurements. The Tip of the Red Giant Branch (TRGB) calibration of Type Ia supernovae (Freedman et al., 2019-2024) has yielded values between $\sim 69$ and $\sim 72$ km/s/Mpc depending on the treatment of photometric calibration and crowding corrections, potentially bridging the gap. Early JWST observations of both Cepheids and TRGB stars have been scrutinized intensely: JWST photometry of Cepheids in SH0ES galaxies confirms the HST-based Cepheid photometry, largely ruling out crowding bias as the source of the discrepancy (Riess et al., 2024), though Freedman et al. (2024) using JWST-calibrated TRGB report values closer to the Planck result. The situation remains unsettled.

The tension matters because, if real, it points to new physics in the expansion history of the universe. Several classes of theoretical resolutions have been proposed:

**Early-universe modifications** (pre-recombination): These aim to reduce the sound horizon $r_s$ at recombination, which would increase the inferred $H_0$ from the CMB. Proposals include **early dark energy** (EDE) -- a scalar field that contributes $\sim 5$--$10\%$ of the total energy density around matter-radiation equality and then decays quickly -- and **additional relativistic species** ($\Delta N_{\rm eff}$), which increase the radiation density and thus the expansion rate before recombination. Increasing $N_{\rm eff}$ by $\sim 0.2$--$0.5$ above the Standard Model value of 3.044 can raise $H_0$ to $\sim 69$--$70$ km/s/Mpc, but current CMB data constrain $N_{\rm eff}$ tightly, and the required values are in tension with Big Bang nucleosynthesis.

**Late-universe modifications** (post-recombination): These modify the distance-redshift relation at $z < 1$ to reconcile local and CMB-based measurements. Examples include evolving dark energy (with $w$ transitioning from $w < -1$ at high $z$ to $w > -1$ today), interacting dark energy-dark matter models, and modified gravity theories. However, late-time modifications generically worsen the fit to BAO and supernova data, making them less favored.

**Systematic errors**: It remains possible that unrecognized systematics in either the CMB analysis or the distance ladder could account for part or all of the tension. For the distance ladder, potential issues include Cepheid crowding and blending, metallicity effects on the period-luminosity relation, and photometric calibration. For the CMB, the analysis relies heavily on the assumed $\Lambda$CDM model; systematic errors in foreground removal or in the assumed lensing amplitude could bias $H_0$. Most experts consider the systematic error budgets to be well-characterized, but the possibility of correlated systematics is difficult to exclude definitively.

## Mathematical framework

The **Hubble constant** is defined as the present-day value of the Hubble parameter:

$$H_0 = H(t_0) = \frac{\dot{a}(t_0)}{a(t_0)}$$

where $a(t)$ is the cosmic scale factor. In the Friedmann equation:

$$H^2(z) = H_0^2 \left[\Omega_r (1+z)^4 + \Omega_m (1+z)^3 + \Omega_k (1+z)^2 + \Omega_\Lambda\right]$$

where $\Omega_r, \Omega_m, \Omega_k, \Omega_\Lambda$ are the density parameters for radiation, matter, curvature, and dark energy respectively. The CMB constrains the combination $\Omega_m h^2$ and $\Omega_b h^2$ (where $h = H_0 / (100\ \text{km/s/Mpc})$) with high precision through the acoustic peak structure. The physical matter density $\Omega_m h^2$ determines the sound horizon at recombination:

$$r_s = \int_{z_*}^{\infty} \frac{c_s(z)}{H(z)}\, dz$$

where $z_* \approx 1090$ is the redshift of recombination, and $c_s = c/\sqrt{3(1 + 3\rho_b / 4\rho_\gamma)}$ is the baryon-photon fluid sound speed. The CMB acoustic peaks measure the angular scale $\theta_s = r_s / D_A(z_*)$, where $D_A$ is the angular diameter distance. Since $\theta_s$ is measured to $0.03\%$ precision, the inferred $H_0$ depends sensitively on $r_s$ and on the assumed expansion history between $z_*$ and today.

The **tension in numbers**:

| Measurement | $H_0$ (km/s/Mpc) | Method | Reference |
|------------|-------------------|--------|-----------|
| Planck 2018 | $67.36 \pm 0.54$ | CMB + $\Lambda$CDM | Planck Collaboration |
| SH0ES 2022 | $73.04 \pm 1.04$ | Cepheids + SNe Ia | Riess et al. |
| H0LiCOW/TDCOSMO | $73.3^{+1.7}_{-1.8}$ | Lensing time delays | Wong et al. |
| CCHP (TRGB) 2024 | $69.85 \pm 1.75$ | TRGB + SNe Ia | Freedman et al. |
| Megamasers | $73.9 \pm 3.0$ | Geometric masers | Pesce et al. |

The Planck--SH0ES discrepancy is $\Delta H_0 / \sigma \approx 5.0$, using the combined uncertainty $\sigma = \sqrt{0.54^2 + 1.04^2} \approx 1.17$ km/s/Mpc.

**Early dark energy** modifies the Friedmann equation by adding a component:

$$\rho_{\rm EDE}(z) = \rho_{\rm EDE,0}\, f(z)$$

where $f(z)$ is sharply peaked near $z \sim 3000$--$5000$ (around matter-radiation equality). A common parametrization uses an axion-like potential $V(\phi) \propto [1 - \cos(\phi/f)]^n$ that behaves like a cosmological constant while the field is frozen, then dilutes faster than radiation once it begins oscillating. Models with $f_{\rm EDE}(z_c) \sim 0.05$--$0.10$ (the fractional energy density at the critical redshift $z_c$) can raise $H_0$ to $\sim 71$--$73$ km/s/Mpc while maintaining an acceptable fit to CMB and large-scale structure data.

## Key results and implications

- The Hubble tension is currently the most statistically significant anomaly in precision cosmology. If it persists and is confirmed as physical, it would be the first observational evidence for physics beyond $\Lambda$CDM.
- JWST observations have largely confirmed the HST Cepheid photometry, disfavoring simple systematic explanations involving photometric crowding bias in the SH0ES analysis.
- Early dark energy is currently the leading theoretical proposal for resolving the tension, but it introduces new fine-tuning issues (why the field activates near matter-radiation equality) and faces increasing pressure from combined CMB + large-scale structure analyses.
- The tension highlights the remarkable precision of modern cosmology: $H_0$ is constrained to better than $2\%$ by multiple independent methods, and the disagreement is at the $\sim 8\%$ level.
- If resolved in favor of the local value ($H_0 \sim 73$), the universe is younger ($\sim 12.6$ Gyr vs. $\sim 13.8$ Gyr in $\Lambda$CDM), with implications for stellar ages and structure formation.

## Failure modes and limitations

- A common error is assuming that the Planck measurement of $H_0$ is "model-independent." It is not: the Planck value is the $H_0$ that best fits the CMB data within the $\Lambda$CDM model. Different cosmological models fitted to the same CMB data can yield different $H_0$ values. However, simple extensions of $\Lambda$CDM typically worsen the fit unless carefully constructed.
- The TRGB calibration remains controversial: different groups analyzing essentially the same photometric data obtain different results depending on choices about color cuts, photometric zeropoints, and the treatment of the TRGB detection algorithm. This methodological spread is itself a source of systematic uncertainty.
- Local measurements of $H_0$ assume a smooth Hubble flow at the distances used ($z \gtrsim 0.023$). If we live in a local underdensity (a "Hubble bubble"), this could bias local measurements high. However, most analyses find that such a void would need to be implausibly large ($\gtrsim 100$ Mpc) to explain the full tension.
- The tension could in principle be a statistical fluke, but at $\sim 5\sigma$ this is extremely unlikely (probability $< 10^{-6}$) if the error budgets are correct.

## Experimental evidence

- **CMB**: Planck (2018), ACT (2020), and SPT (2021) all obtain $H_0 \approx 67$--$68$ km/s/Mpc within $\Lambda$CDM. The consistency between three independent CMB experiments strengthens the case that the CMB-derived value is robust.
- **Distance ladder**: The SH0ES program has systematically improved the Cepheid distance ladder over two decades, reducing systematic uncertainties through geometric anchors (NGC 4258 maser distance, Milky Way parallaxes from HST/Gaia, LMC detached eclipsing binaries).
- **JWST**: Observations of Cepheids in SH0ES galaxies (2023-2024) confirm the HST photometry at the $\sim 0.01$ mag level, ruling out crowding as a dominant systematic. However, JWST observations of TRGB and J-region Asymptotic Giant Branch (JAGB) stars have yielded varying results depending on the group and calibration choices.
- **DESI BAO** (2024): Early DESI baryon acoustic oscillation results are consistent with $\Lambda$CDM but show mild ($\sim 2$--$3\sigma$) preference for evolving dark energy ($w_0 > -1$, $w_a < 0$), which could affect the interpretation of the tension.
- **Gravitational wave standard sirens**: The binary neutron star merger GW170817 with electromagnetic counterpart gave $H_0 = 70.0^{+12.0}_{-8.0}$ km/s/Mpc (Abbott et al., 2017), consistent with both values but with large uncertainty. Future detections will improve this constraint, providing a completely independent measurement pathway.

## Sources

- L. Verde, T. Treu, and A. G. Riess, "Tensions between the early and the late universe," *Nature Astronomy* **3**, 891 (2019).
- A. G. Riess et al., "A comprehensive measurement of the local value of the Hubble constant," *The Astrophysical Journal Letters* **934**, L7 (2022).
- E. Di Valentino et al., "In the realm of the Hubble tension -- a review of solutions," *Classical and Quantum Gravity* **38**, 153001 (2021).

## Reasoning checks

1. State the physical objects and observables without using the displayed equation.
2. Check dimensions and identify every limiting assumption.
3. Give one regime where this description succeeds and one where it needs correction.
4. Name an experiment, simulation, or observation that could determine its parameters.
5. Explain how this idea changes when the dominant length, time, energy, or particle-number scale changes.

## Expansion queue

- [x] Add a derivation from the nearest prerequisite principles.
- [x] Add a worked example with units.
- [x] Add a primary or canonical source.
- [x] Add a failure case, misconception, or counterexample.

## Navigation

[[Physics Worldmap]] · [[Cosmology Map]] · [[Cosmological Constant Problem|← previous]] · [[Reionization|next →]]
