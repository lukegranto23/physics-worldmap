---
title: Physics Frontiers and Open Problems
aliases:
  - Physics frontier map
  - Open problems in physics
type: frontier-dashboard
field: Physics
epistemic_status: mixed
level: advanced
tags:
  - map/frontiers
  - physics/open-problems
  - status/current
status_as_of: 2026-07-30
source_policy: Primary collaborations, laboratories, agencies, consensus reports, and major reviews
---

# Physics Frontiers and Open Problems

[[Physics Worldmap]] · [[Open Problems Dashboard]] · [[Epistemic Status and Claim Hygiene]]

> [!important] Status discipline
> This is a map of *live research questions*, not a catalogue of promised revolutions. “Open” can mean an unknown fact, an incomplete theory, a mathematical obstruction, an unresolved experimental tension, or an engineering barrier. Those are different kinds of ignorance and should not be conflated.

## Evidence legend

| Label | Meaning |
|---|---|
| **Observed** | A direct, calibrated empirical result, replicated or independently cross-checked where feasible. |
| **Established within model** | A robust inference or derivation conditional on stated assumptions and a defined regime. |
| **Broadly established** | Convergent empirical and theoretical support across the tested domain. |
| **Constraint** | A null result or precision measurement that excludes part of parameter space. |
| **Tension / hint** | Interesting discrepancy or model preference whose significance depends on data combinations, assumptions, or unresolved systematics. |
| **Open** | No accepted answer; several viable explanations may coexist. |
| **Engineering frontier** | Underlying physics may be known, but reliable, scalable, economical implementation is not. |

Status applies at the level of an individual claim. A single table row can contain an observation, a model-conditional inference, a constraint, and an open question; read each sentence with its cited assumptions and caveats rather than assigning one confidence level to the whole topic.

Useful orientation sources include the [Particle Data Group 2026 review collection](https://pdg.lbl.gov/2026/), the US particle-physics [2023 P5 report](https://www.usparticlephysics.org/2023-p5-report/), the nuclear-science [2023 Long Range Plan](https://science.osti.gov/-/media/np/nsac/pdf/202310/NSAC-LRP-2023-v12.pdf), the National Academies’ [AMO 2020 decadal assessment](https://doi.org/10.17226/25613), [Astro2020](https://www.nationalacademies.org/publications/26141), and [Physics of Life](https://www.nationalacademies.org/projects/DEPS-BPA-17-02/publication/26403).

---

## 1. Foundations, quantum information, and quantum gravity

### Current status

General relativity and quantum field theory are extraordinarily successful in their tested regimes, but there is no empirically confirmed quantum theory of gravity. Candidate frameworks—including string theory/holography, loop approaches, asymptotic safety, causal/discrete approaches, and effective field theory—have produced important mathematical and conceptual results, but none is experimentally established as the microscopic description of spacetime. A balanced entry point is the Snowmass [Quantum Gravity and String Theory](https://arxiv.org/abs/2210.01737) report and the review of [observational signatures of quantum gravity](https://arxiv.org/abs/2205.01799).

| Frontier | What is known | What remains open | Decisive observables and programs |
|---|---|---|---|
| Quantum structure of spacetime | Gravity is a consistent low-energy effective field theory. Black-hole thermodynamics and holographic dualities connect geometry, entropy, and quantum information. | What are the fundamental degrees of freedom? Is spacetime emergent? Which candidate theory describes nature, and what uniquely testable low-energy consequences follow? | Precision clocks and interferometers; short-range gravity; strong-field gravitational waves; cosmological relics; [laboratory tests of quantum gravity](https://doi.org/10.1103/RevModPhys.97.015006). |
| Black-hole information | Page-curve behavior and “island” calculations recover unitary entropy evolution in controlled semiclassical models. | How is information encoded and recovered in realistic evaporating black holes? What describes the interior, singularity resolution, and observer-dependent reconstruction? | Hawking-like quantum simulators; holographic models; ringdown and horizon-scale tests. See the Snowmass report on [black holes and emergent spacetime](https://arxiv.org/abs/2201.03096). |
| Measurement and interpretations | Bell experiments exclude broad classes of local hidden-variable theories; the 2022 Nobel recognized decisive experimental work on Bell inequalities and entanglement ([Nobel summary](https://www.nobelprize.org/prizes/physics/2022/summary/)). | What, if anything, selects a unique outcome? Are collapse models, Everettian, relational, Bohmian, or other accounts empirically distinguishable? Where is the quantum-to-classical boundary? | Matter-wave interferometry with larger masses, optomechanics, collapse-model tests, cosmic Bell tests, and tests of macroscopic superpositions ([review](https://doi.org/10.1103/RevModPhys.90.025004)). |
| Is gravity quantum? | Consistent classical-gravity/quantum-matter models require irreducible gravitational fluctuations that can mediate classical correlations, but not quantum entanglement, and predict a distinguishing phase response. | Which protocol unambiguously tests whether gravity can transmit quantum information rather than only classical correlations plus ordinary quantum effects? | Tabletop gravity-mediated entanglement, non-Gaussian witnesses, force-noise characterization; see the 2025 analysis of [classical-gravity alternatives](https://doi.org/10.1103/PhysRevLett.134.061501). |
| Singularities and cosmic initial conditions | Classical GR predicts singular behavior under broad conditions; inflation can explain flatness and seed structure within model families. | What replaces the Big Bang and black-hole singularities? Why these initial conditions and this arrow of time? Is inflation realized, and by what field or mechanism? | CMB polarization/non-Gaussianity, primordial gravitational waves, relics and topology, quantum-cosmology consistency tests. |
| Strong-field gravity | Binary black-hole and neutron-star observations agree with GR within current precision; horizon-scale images are consistent with Kerr-like compact objects. | Are there small deviations, extra fields, horizonless objects, modified propagation, or violations of no-hair and equivalence principles? | [LVK O4b / GWTC-5.0 catalog](https://ligo.org/detections/o4b-catalog/), [Event Horizon Telescope GR tests](https://eventhorizontelescope.org/testing-general-relativity), pulsar timing, and future [LISA](https://www.esa.int/Science_Exploration/Space_Science/LISA) observations. |

### High-value conceptual bridges

- **Quantum error correction ↔ holography:** bulk reconstruction behaves like redundant quantum encoding, but analogy is not yet a derivation of our universe.
- **Entanglement ↔ geometry:** entanglement entropy constrains geometry in special theories; the scope beyond controlled holographic systems remains open.
- **Effective field theory ↔ candidate UV completions:** any proposal must recover GR and quantum field theory at accessible scales and make discriminating predictions.
- **Thermodynamics ↔ gravity:** horizon entropy and generalized second laws are robust clues, not by themselves a complete microscopic theory.

---

## 2. Particle physics and fundamental interactions

### Current status

The Standard Model continues to describe collider and precision data extremely well. ATLAS and CMS find the Higgs boson’s measured properties consistent with Standard Model expectations within present uncertainties ([joint status](https://www.atlas.cern/Updates/News/ATLAS-CMS-Higgs-2022)). No beyond-Standard-Model particle has been established at a collider. Yet the Standard Model does not identify the cosmological dark matter, explain the baryon asymmetry, incorporate gravity, or determine the observed flavor pattern.

| Frontier | What is known | What remains open | Decisive observables and programs |
|---|---|---|---|
| Higgs sector | A spin-0 Higgs boson is observed near 125 GeV. Its measured couplings to the electroweak gauge bosons and directly observed fermion species are consistent with Standard Model mass-generation expectations within current precision. | Is it elementary? What is the Higgs self-coupling and full potential? Are there additional scalars, invisible decays, or compositeness? Why is the electroweak scale so far below the Planck scale? | Differential Higgs couplings, rare/invisible decays, di-Higgs production and precision electroweak tests at the [HL-LHC](https://home.cern/press/media-kits/hl-lhc/) and possible future colliders such as the [FCC](https://home.cern/science/accelerators/future-circular-collider/science-goals/). |
| Dark matter | Astrophysical and cosmological evidence requires gravitating matter beyond known baryons in the baseline cosmology; its particle identity is unknown ([PDG review](https://pdg.lbl.gov/2026/reviews/rpp2026-rev-dark-matter.pdf)). | Is dark matter a WIMP, axion, sterile neutrino, ultralight field, primordial black hole, composite state, hidden sector, or evidence for modified gravitational dynamics? Is it one component or several? | Direct detection, axion haloscopes/helioscopes, missing-energy colliders, indirect searches, small-scale structure and lensing. [LZ’s published program](https://lz.lbl.gov/publications/) reports constraints, not a confirmed dark-matter detection; [CAST](https://home.cern/science/experiments/cast/) constrains solar axions. |
| Neutrino identity and masses | Flavor oscillation proves at least two neutrinos have nonzero mass and measures mass-squared differences and mixing angles. | Absolute mass scale; normal versus inverted ordering; Dirac versus Majorana identity; leptonic CP violation; sterile states; origin of tiny masses. | [DUNE](https://lbnf-dune.fnal.gov/about/science-goals/), [Hyper-Kamiokande](https://www-sk.icrr.u-tokyo.ac.jp/en/hk/about/research/), beta endpoint/cosmology, reactor and atmospheric data, and neutrinoless double-beta decay with [LEGEND](https://legend-exp.org/). See the [PDG neutrino review](https://pdg.lbl.gov/2026/reviews/rpp2026-rev-neutrino-mixing.pdf). |
| Matter–antimatter asymmetry | Standard Model CP violation exists but is insufficient in conventional calculations to explain the observed cosmic baryon asymmetry. | Did leptogenesis, electroweak baryogenesis, Affleck–Dine dynamics, hidden sectors, or another mechanism produce the asymmetry? | Neutrino CP phase, electric dipole moments, flavor observables, collider phase-transition probes, proton decay and cosmological relics. |
| Flavor puzzle | Quark and lepton masses and mixing parameters are measured with increasing precision. | Why three generations? What sets Yukawa hierarchies, mixing patterns, and CP phases? Are accidental symmetries clues to a deeper structure? | Rare meson and tau decays, lepton-flavor violation, CKM/PMNS overconstraints; [Belle II](https://www.belle2.org/) and LHC flavor experiments. |
| Strong CP and axions | The QCD vacuum permits CP violation, yet the neutron EDM is extremely small. | Why is the effective strong-CP angle tiny? Is the Peccei–Quinn mechanism realized, and is its axion also dark matter? | Neutron, atom and molecule EDMs; axion searches; stellar/cosmological constraints. |
| Unification and proton stability | Gauge couplings approximately approach one another at high energy in some extensions; baryon number is accidental in the Standard Model. | Is there grand unification? Does the proton decay? Are quarks and leptons composite? Are there extra dimensions or new symmetries? | Proton-decay searches, magnetic monopoles, precision coupling evolution, rare processes, cosmic relics. |
| Muon magnetic moment | Fermilab’s final 2025 measurement is the most precise experimental value. A new lattice-informed Standard Model consensus moved the central theory prediction into agreement with experiment, while tensions among hadronic-vacuum-polarization methods remain. | Can data-driven and lattice QCD calculations be reconciled? Does any residual discrepancy survive a controlled theory synthesis? | Improved hadronic cross sections and lattice calculations. Use the [final Fermilab result](https://muon-g-2.fnal.gov/result2025.pdf) and [PDG 2026 review](https://pdg.lbl.gov/2026/reviews/rpp2026-rev-g-2-muon-anom-mag-moment.pdf), not old “discovery” headlines. |

### Interpretation rule

A null search does not imply “no new physics”; it excludes models in a stated parameter region. Likewise, an anomaly is not a particle until it survives independent data, systematic checks, and a global consistency analysis.

---

## 3. Cosmology, gravitation, and astrophysics

### Current status

The six-parameter spatially flat ΛCDM model fits the CMB and much large-scale-structure data remarkably well ([Planck legacy results](https://sci.esa.int/web/planck/-/60507-planck-collaboration-2018); [parameter analysis](https://arxiv.org/abs/1807.06209)). Its dominant components—cold dark matter and dark energy—remain unidentified microscopically. Several tensions and hints are active, but none yet compels a replacement of ΛCDM.

| Frontier | What is known | What remains open | Decisive observables and programs |
|---|---|---|---|
| Dark energy and cosmic acceleration | Expansion is accelerating; a cosmological constant fits much data. | Is dark energy exactly constant, a dynamical field, modified gravity, or a sign of unrecognized systematics? Why is its scale so small? | BAO, supernovae, weak lensing, redshift-space distortions and clusters. DESI DR2 combinations strengthen a model-dependent preference for evolving dark energy at roughly 2.8–4.2σ, explicitly a **hint rather than a discovery** ([official DR2 guide](https://www.desi.lbl.gov/2025/03/19/desi-dr2-results-march-19-guide/); [Berkeley Lab summary](https://newscenter.lbl.gov/2025/03/19/new-desi-results-strengthen-hints-that-dark-energy-may-evolve/)). [Euclid](https://www.cosmos.esa.int/web/euclid), [Rubin](https://rubinobservatory.org/about), and [Roman](https://science.nasa.gov/mission/roman-space-telescope/science/) provide complementary tests. |
| Expansion-rate tension | Early-universe inference and several local distance-ladder determinations do not fully agree. | New early-universe physics, late-time dynamics, calibration or population systematics, or statistical fluctuation? | Independent distance ladders, gravitational-lens delays, standard sirens, masers, TRGB/JAGB stars, improved CMB and BAO. NASA’s overview frames the [Hubble-constant tension](https://science.nasa.gov/mission/hubble/science/science-behind-the-discoveries/hubble-constant-and-tension/). |
| Structure-growth tension | Some weak-lensing surveys prefer slightly less late-time clustering than Planck-normalized ΛCDM. | Neutrino mass, baryonic feedback, intrinsic alignments, photometric-redshift errors, modified gravity, or chance? | Cross-survey shear, CMB lensing, clusters, peculiar velocities, redshift-space distortions and hydrodynamic simulations. |
| Inflation and the primordial universe | A nearly scale-invariant, adiabatic, Gaussian spectrum explains observed structure well. | What field or mechanism drove inflation? How did it begin and end? Was there a primordial tensor background, non-Gaussianity, isocurvature, cosmic strings, or an alternative early phase? | CMB B modes, spectral running, non-Gaussianity, 21-cm cosmology and stochastic gravitational waves. [LiteBIRD](https://www.isas.jaxa.jp/en/topics/002880.html) targets large-scale CMB polarization. The [CMB-S4 science book](https://cmb-s4.uchicago.edu/book.php) remains a useful science case, but should not be treated as an assured current facility. |
| Compact objects and dense matter | Binary neutron-star multimessenger data constrain masses, radii, and tidal deformability; black-hole populations are now observable statistically. | What is the cold dense-matter equation of state? Are there phase transitions, hyperons, deconfined quarks, exotic compact objects, or mass gaps? How are heavy elements synthesized? | GW inspirals/post-mergers, NICER pulse profiles, X-ray bursts, kilonova spectroscopy, heavy-ion constraints and nuclear theory. |
| Black-hole growth and cosmic dawn | Supermassive black holes existed within the first billion years; reionization followed the first luminous sources. | Did black holes start from stellar remnants, direct collapse, dense clusters, or primordial seeds? Which sources reionized the universe, and how did the first stars form? | JWST spectroscopy, 21-cm tomography, quasar demographics, deep X-ray/radio surveys and future LISA mergers. |
| High-energy cosmic messengers | Astrophysical neutrinos, gamma rays, cosmic rays and gravitational waves reveal nonthermal sources. | Which objects accelerate ultra-high-energy cosmic rays? Where are most high-energy neutrinos produced? How do relativistic jets, shocks and magnetic reconnection work? | [IceCube](https://icecube.wisc.edu/science/research/), gamma-ray observatories, air-shower arrays, neutrino successors and time-domain multimessenger coincidences. |
| Gravitational-wave universe | Compact-binary gravitational waves are routine detections; pulsar timing arrays report evidence for a nanohertz stochastic process. | Population origins, primordial components, phase transitions, cosmic strings, eccentricity/environment, and deviations from GR. | Current [LVK O4 catalogs](https://ligo.org/detections/o4b-catalog/), [NANOGrav 15-year background evidence](https://nanograv.org/15yr/Summary/Background), next-generation ground detectors, and [LISA science](https://sci.esa.int/web/lisa/-/61366-science-objectives). |
| Habitability and life elsewhere | Thousands of exoplanets establish that planetary systems are common. | How common are temperate rocky planets, atmospheres, stable climates, biospheres, and technological life? Which biosignatures are robust against abiotic false positives? | Transit/direct-imaging spectroscopy, stellar context, comparative planetology, atmospheric retrieval and laboratory chemistry. This is a core [Astro2020](https://www.nationalacademies.org/publications/26141) theme. |

---

## 4. Nuclear physics

### Current status

QCD is the accepted fundamental theory of the strong interaction. Lattice QCD is predictive for many equilibrium quantities at low baryon chemical potential, and ab initio nuclear methods now reach increasingly heavy systems. A uniformly precise derivation of nuclei, reactions, dense matter and real-time QCD phenomena from first principles remains out of reach. The current US consensus map is the [2023 Nuclear Science Long Range Plan](https://science.osti.gov/-/media/np/nsac/pdf/202310/NSAC-LRP-2023-v12.pdf).

| Frontier | What is known | What remains open | Decisive observables and programs |
|---|---|---|---|
| Origin of nucleon mass and spin | Most proton mass is emergent QCD energy rather than the Higgs-generated current-quark masses. Quarks and gluons share momentum and angular momentum. | Quantitative decomposition of mass, spin, pressure and shear; 3D quark/gluon tomography; gluon saturation at small momentum fraction. | Deep-inelastic and exclusive scattering at the [Electron–Ion Collider](https://www.bnl.gov/eic/science.php), lattice QCD and global parton analyses. |
| Confinement and hadronization | Colored particles are not observed in isolation; jets display calculable short-distance showers plus nonperturbative fragmentation. | The real-time mechanism of confinement, formation of hadrons, exotic hadron structure, and universal description of hadronization. | Jet substructure, heavy flavor, spectroscopy, femtoscopy and lattice/amplitude methods. |
| QCD phase diagram | Relativistic heavy-ion collisions create a hot, strongly coupled quark–gluon plasma with collective flow. | Location or existence of a critical point; first-order boundary; transport coefficients; equilibration and emergence of hydrodynamics; phase structure at high density. | RHIC beam-energy scan, LHC heavy ions, fluctuation observables, jets, electromagnetic probes and finite-density theory. |
| Nuclear forces and many-body emergence | Chiral effective field theory and ab initio methods connect symmetries to nuclear interactions with quantifiable uncertainties in selected regions. | Controlled truncation errors across the nuclear chart; consistent three-body forces and currents; collective behavior, clustering and reactions. | Precision few-body data, electroweak probes, uncertainty-quantified many-body calculations and rare-isotope measurements. |
| Limits of nuclei | Thousands of nuclides are known; shell structure evolves far from stability. | Exact neutron/proton drip lines, new magic numbers, continuum effects, fission dynamics and superheavy stability. | [FRIB](https://frib.msu.edu/research-areas-and-capabilities), radioactive beams, mass/lifetime spectroscopy and reaction facilities. |
| Origin of the elements | Stellar burning and neutron-capture pathways explain broad abundance patterns. | Dominant r-process sites and conditions; p-process routes; uncertain nuclear masses, rates, beta decays and fission yields far from stability. | Rare-isotope experiments, kilonovae, metal-poor stars, meteoritic records and network calculations. |
| Dense nuclear matter | Nuclear experiments and neutron-star observations constrain the symmetry energy and equation of state. | Composition and phases of neutron-star cores; maximum mass, transport, superfluidity, deconfinement and merger remnants. | Heavy-ion collisions, neutron skins, masses/radii, tidal deformability, cooling and post-merger gravitational waves. |
| Symmetry tests | Beta decay and EDM searches tightly test weak interactions and CP symmetry. | Majorana neutrinos, new currents, scalar/tensor interactions, time-reversal violation and baryon-number violation. | Neutrinoless double-beta decay, neutron/nuclear/atomic EDMs, precision beta decay and neutron experiments. |

---

## 5. Atomic, molecular, and optical physics

### Current status

AMO physics provides some exceptionally controllable quantum systems and many of the most precise measurements ever made. Optical clocks, ultracold atoms and molecules, attosecond probes, quantum simulators and engineered photons are simultaneously tools and objects of study. The broad consensus map is [AMO 2020](https://www.nationalacademies.org/read/25613/chapter/1).

| Frontier | What is known | What remains open | Decisive observables and programs |
|---|---|---|---|
| Quantum control and computation | High-fidelity gates, small error-correcting demonstrations and programmable simulators exist on several platforms. | Fault-tolerant scaling, correlated error models, useful logical computation, verification, modular interconnects and energy/resource costs. | Logical error suppression versus code distance, randomized benchmarking limits, cross-platform verification and networked entanglement. |
| Quantum many-body dynamics | Tunable gases realize Hubbard, spin, gauge-like and topological models with site-resolved measurements. | Thermalization and its failure, entanglement growth, transport without quasiparticles, quantum scars, driven/open phases and controlled continuum limits. | Quantum gas microscopes, quench spectroscopy, entropy/entanglement proxies and analog–digital cross-checks. |
| Ultracold chemistry | Individual collision channels and some reactions can be prepared and measured quantum state by state. | Universal control of reactive scattering, complex-mediated loss, many-body chemistry and accurate dynamics on coupled potential surfaces. | Trapped molecules, external-field tuning, coincidence imaging and precision molecular theory. |
| Attosecond dynamics | Attosecond pulses expose electron motion in atoms, molecules and solids; the field was recognized by the [2023 Nobel Prize](https://www.nobelprize.org/prizes/physics/2023/summary/). | Direct reconstruction without model bias; correlated multielectron motion; charge migration versus nuclear rearrangement; steering chemistry and solids in real time. | Pump–probe spectroscopy, high-harmonic generation, photoelectron coincidence and time-resolved diffraction. |
| Precision clocks and metrology | Optical clocks reach fractional uncertainties around the \(10^{-18}\)–\(10^{-19}\) frontier; NIST reported a new ion-clock record in 2025 ([official summary](https://www.nist.gov/news-events/news/2025/07/nist-ion-clock-sets-new-record-most-accurate-clock-world)). | Robust transportable clocks, relativistic geodesy, global optical time transfer and controlled systematics at still lower levels. | Clock comparisons, height-dependent gravitational redshift, fiber/free-space links; see NIST on [fundamental tests](https://www.nist.gov/atomic-clocks/a-powerful-tool-for-science/putting-einstein-test) and [optical time transfer](https://www.nist.gov/publications/high-precision-optical-time-and-frequency-transfer). |
| Low-energy searches for new physics | Atoms and molecules amplify EDMs, parity violation, fifth forces, varying constants and ultralight-field effects. | Whether dark matter or new CP violation couples to spins, masses, frequencies or forces at accessible strength. | Molecular and atomic EDMs, clock networks, atom interferometers, spectroscopy, equivalence-principle and inverse-square-law tests. |
| Molecular complexity | Electronic-structure theory is extremely accurate for small systems and selected observables. | Predictive correlated dynamics for large, open, relativistic or strongly nonadiabatic molecules; uncertainty-calibrated chemistry from first principles. | Spectroscopy benchmarks, quantum Monte Carlo/tensor networks, ultrafast data and differentiable inverse modeling. |

---

## 6. Condensed-matter and materials physics

### Current status

Landau symmetry breaking, quasiparticles, BCS theory and topological band theory explain vast classes of matter. The frontier lies where strong correlations, frustration, topology, disorder and nonequilibrium dynamics defeat simple quasiparticle or mean-field descriptions. See the National Academies chapter on [Quantum Materials](https://www.nationalacademies.org/read/25244/chapter/5) and the community [Quantum Materials Roadmap](https://arxiv.org/abs/2102.02644).

| Frontier | What is known | What remains open | Decisive observables and programs |
|---|---|---|---|
| Unconventional superconductivity | Conventional superconductors are explained by phonon-mediated pairing and BCS/Eliashberg theory. Cuprates, iron-based, heavy-fermion and other families show phenomenology not explained by conventional phonon-mediated BCS/Eliashberg theory. | Pairing glue and order-parameter competition in each family; pseudogap relation; route to reproducible ambient-pressure room-temperature superconductivity. | Phase-sensitive probes, spectroscopy, quantum oscillations, ultrafast response, strain/pressure tuning and unbiased many-body calculations. |
| Strange metals and non-Fermi liquids | Many correlated metals show near-linear resistivity and scaling without long-lived quasiparticles. | Universal organizing principles, role of quantum criticality, Planckian bounds, holographic descriptions and connection to superconductivity. | Transport, optical conductivity, thermodynamics, noise and momentum-resolved spectroscopy; see the [strange-metals review](https://www.annualreviews.org/doi/10.1146/annurev-conmatphys-031119-050558). |
| Strong-correlation prediction | Model Hamiltonians capture local physics; numerical methods are powerful in selected dimensions and signs. | Controlled solutions of realistic 2D fermion problems, the sign problem, multiscale material prediction and interpretable reduced theories. | Cross-method benchmarks, quantum simulators, spectroscopic sum rules and uncertainty-aware materials calculations. |
| Moiré and designer quantum matter | Twist, strain and stacking create tunable flat bands, correlated insulators, magnetism and superconductivity. | Microscopic origin and universality of phases; disorder/strain control; scalable fabrication; genuinely topological and fractional states. | Local imaging, compressibility, transport, spectroscopy, controlled twist-angle series and device reproducibility. |
| Topological phases and quantum memory | Integer/fractional Hall states and many topological band phases are established. | Unambiguous non-Abelian anyons, robust topological qubits, interacting classifications, higher-order/fracton phases and useful operating temperatures. | Braiding/interferometry, fusion-rule tests, thermal Hall response, parity lifetimes and logical-qubit demonstrations. |
| Nonequilibrium quantum matter | Floquet phases, prethermal behavior and driven transitions exist in controlled systems. | Universal laws far from equilibrium, heating avoidance, open-system phases, many-body localization stability in higher dimensions and quantum hydrodynamics. | Quenches, pump–probe measurements, full counting statistics and entanglement-sensitive observables. |
| Glasses, disorder and jamming | Amorphous solids display widely shared phenomenology, slow relaxation and heterogeneous dynamics. | A complete microscopic theory of the glass transition; relation among thermodynamic, kinetic and landscape pictures; yielding and memory. | Time-resolved structure/dynamics, nonlinear rheology, ultrastable glasses and computational benchmarks; see the [computational glass review](https://www.nature.com/articles/s42254-022-00548-x). |
| Materials by design | First-principles databases and machine learning accelerate candidate discovery. | Reliable synthesis prediction, defect/interface control, metastability, lifetime, circularity and closed-loop validation. | Autonomous laboratories, in situ microscopy/spectroscopy, calibrated uncertainty and prospective—not retrospective—benchmarks. |

---

## 7. Statistical physics, nonlinear dynamics, and fluids

### Current status

Equilibrium ensembles, renormalization-group ideas and universality explain why microscopic details often disappear near equilibrium critical points. There is no comparably universal framework for arbitrary nonequilibrium steady states, turbulent flows, aging systems or multiscale adaptive networks.

| Frontier | What is known | What remains open | Decisive observables and programs |
|---|---|---|---|
| Turbulence | Navier–Stokes equations model ordinary continuum flow across vast regimes; statistical cascades and coherent structures are well documented. | Predictive closure, intermittency and anomalous scaling; transition to turbulence; wall turbulence and drag; rare events; control across scales. | High-Reynolds-number experiments, DNS/LES cross-validation, Lagrangian tracking and exact-law tests. A useful problem statement is [“What Is the Turbulence Problem?”](https://www.annualreviews.org/content/journals/10.1146/annurev-conmatphys-031620-095842). |
| Navier–Stokes regularity | Global smooth solutions are known in 2D and in restricted 3D cases. | Whether smooth, finite-energy 3D incompressible solutions exist for all time or can develop singularities—the [Clay Millennium problem](https://www.claymath.org/lectures/navier-stokes-existence-and-smoothness/). | Rigorous analysis and computer-assisted bounds. Solving regularity would **not by itself** solve practical turbulence closure. |
| Far-from-equilibrium ensembles | Fluctuation theorems, linear response, macroscopic fluctuation theory and stochastic thermodynamics cover important regimes. | A general variational or ensemble principle; phase transitions in trajectory space; entropy production inference; strongly driven interacting systems. | Full counting statistics, controlled colloids/circuits, large-deviation measurements and exact solvable limits. |
| Glass transition and aging | Relaxation becomes heterogeneous and extremely slow without ordinary crystalline order. | Whether an ideal thermodynamic transition exists in finite dimensions; relation to jamming; memory, rejuvenation and yielding. | Long-duration experiments, ultrastable glasses, colloids/granular systems, spin-glass tests and simulations. |
| Chaos and predictability | Lyapunov exponents, bifurcations and attractors characterize low-dimensional chaos. | Predictability of high-dimensional, noisy, nonstationary systems; rare extremes; causal reduction and data assimilation under model error. | Controlled nonlinear experiments, ensemble forecasts, operator-learning validation and invariant/statistical diagnostics. |
| Pattern formation | Symmetry and amplitude equations explain many near-onset patterns. | Robust principles far from onset, defects and turbulence, adaptive/active media, multiscale morphogenesis and inverse design. | Imaging, perturbation-response experiments, reduced-model falsification and controlled active materials. |
| Open quantum statistical mechanics | Lindblad dynamics and fluctuation relations describe Markovian open systems in selected limits. | Non-Markovian thermodynamics, quantum heat engines at finite power, measurement/feedback costs, dissipative phases and quantum–classical crossover. | Calorimetry, circuit/ion/atom platforms, trajectory statistics and thermodynamic consistency checks. |

The 2021 Nobel Prize highlighted how disorder, fluctuations and multiscale reasoning connect climate and spin glasses to complex systems ([Nobel scientific background](https://www.nobelprize.org/prizes/physics/2021/press-release/Complex/)).

---

## 8. Plasma physics and fusion

### Current status

Magnetic and inertial confinement have reached landmark plasma regimes. The National Ignition Facility has repeatedly produced fusion target gain above one ([LLNL ignition record](https://lasers.llnl.gov/science/achieving-fusion-ignition)), and magnetic devices have approached burning-plasma-relevant temperatures, confinement and durations. Neither result is a delivered commercial power plant: target gain is not wall-plug electrical gain, and reactor availability, fuel, materials and heat extraction remain central challenges. The US roadmap is summarized in the [DOE Fusion Energy Strategy 2024](https://www.energy.gov/fusion/doe-fusion-energy-strategy-2024-executive-summary).

| Frontier | What is known | What remains open | Decisive observables and programs |
|---|---|---|---|
| Burning plasma | Alpha heating and ignition physics are demonstrated in pulses; tokamaks and stellarators sustain hot confined plasmas. | Self-heated steady operation with sufficient gain, stability, controllability and duty cycle. | ITER’s revised baseline prioritizes staged scientific operation and targets deuterium–tritium operation later in the program; schedules are governance-dependent ([official baseline](https://www.iter.org/node/20687/new-baseline-prioritize-robust-start-exploitation)). Private and public pilot plants require transparent gain definitions. |
| Transport and turbulence | Microinstabilities and neoclassical transport explain many trends; gyrokinetics provides a predictive framework in selected regimes. | First-principles transport across edge/core, multiscale coupling, pedestal formation, energetic particles and real-time reduced models. | Validated gyrokinetic simulation, profile/flow diagnostics, perturbative transport and multi-device comparisons. |
| Stability and control | Major MHD modes and many mitigation methods are understood. | Reliable avoidance or benign termination of disruptions, edge-localized modes, runaway electrons and density-limit events in reactor conditions. | Fast diagnostics, actuators, disruption databases, physics-informed control and reactor-scale validation. |
| Plasma-facing materials | Tungsten and advanced concepts tolerate high heat better than many alternatives. | Neutron damage, helium/hydrogen retention, embrittlement, erosion/redeposition, tritium inventory, heat exhaust and remote replacement. | Fusion-neutron sources, high-heat-flux testing, component exposure and multiscale materials models. |
| Tritium and fuel cycle | D–T is the most accessible terrestrial fusion fuel; lithium blankets can in principle breed tritium. | Demonstrated reactor-scale breeding margin, extraction, inventory control, regulatory safety and startup fuel supply. | Integrated blanket modules, fuel-cycle demonstrations and independently audited tritium accounting. |
| Inertial fusion energy | NIF established target ignition and repeated target gains above unity. | Efficient high-repetition drivers, inexpensive targets, chamber clearing, target injection, wall lifetime and total plant gain. | Shot repetition, laser efficiency, manufacturing yield, coupling and full facility energy balance—not capsule yield alone. |
| Space and astrophysical plasmas | Collisionless shocks, reconnection, dynamos and turbulence operate throughout the universe. | Particle acceleration and heating, fast reconnection onset, cosmic magnetic-field origin and cross-scale energy partition. | In situ multi-spacecraft measurements, laboratory plasma experiments, kinetic simulations and multimessenger astrophysics; see the [plasma astrophysics white paper](https://arxiv.org/abs/2203.02406). |

DOE groups the fusion mission into three coupled drivers: sustain a burning plasma, engineer materials that survive extremes, and safely harness fusion energy ([official framing](https://www.energy.gov/science/articles/does-office-science-releases-vision-outlining-path-advancing-fusion-energy-science)).

---

## 9. Soft matter, biophysics, and physics of life

### Current status

Physics can now measure and perturb living systems from single molecules to ecosystems, while active matter and nonequilibrium thermodynamics provide shared language for self-driven components. A central agenda is to move from descriptive correlations to predictive, falsifiable principles that survive biological heterogeneity and evolution. See the National Academies’ [Physics of Life](https://www.nationalacademies.org/read/26403/chapter/3) report and NSF’s [Physics of Living Systems](https://www.nsf.gov/funding/opportunities/pols-physics-living-systems) program.

| Frontier | What is known | What remains open | Decisive observables and programs |
|---|---|---|---|
| Active matter | Self-propelled particles exhibit collective motion, phase separation, active turbulence and unusual stresses. | Universal classifications beyond equilibrium symmetry principles; thermodynamics of active systems; role of information and feedback; connection to living tissues. | Controlled colloids, bacterial suspensions, cytoskeletal extracts, epithelial layers and entropy-production measurements. |
| Jamming, yielding and rheology | Dense grains, emulsions and suspensions share packing- and stress-controlled phenomena. | Microscopic prediction of yielding, shear thickening, aging, avalanches, memory and failure in disordered solids. | Particle-resolved imaging, local stress, cyclic training, nonlinear rheology and scaling tests. |
| Self-assembly | Thermodynamic design rules work for many equilibrium structures; DNA and proteins provide programmable interactions. | Reliable nonequilibrium assembly, error correction, kinetic traps, multicomponent complexity and adaptive materials. | Time-resolved assembly, designed interactions, yield/error statistics and inverse-design tests. |
| Cell organization | Membranes, cytoskeletons, condensates and motor proteins organize cells dynamically. | How mechanics, phase separation, reaction networks and transport jointly set organelle identity, polarity and robustness. | Super-resolution/live-cell imaging, optogenetic perturbation, force probes, reconstitution and quantitative spatial models. |
| Morphogenesis | Gene regulation, cell mechanics and signaling guide reproducible shapes. | How local rules create global form, scaling and repair; how embryos remain robust to noise while remaining evolvable. | Organoids, synthetic embryos, lineage/force mapping, causal perturbations and multiscale theory. |
| Biological information and decisions | Molecular networks sense, encode and respond under noise and energetic constraints. | Applicable bounds on information, energy, accuracy and adaptation in real cells; how collective decisions and memory emerge. | Single-cell trajectories, perturbation-response, information flow, energetic measurements and synthetic circuits. |
| Protein dynamics and design | Structure-prediction systems, including AlphaFold, transformed access to plausible static structures; the work was recognized by the [2024 Chemistry Nobel](https://www.nobelprize.org/prizes/chemistry/2024/press-release/). | Folding pathways, conformational ensembles, allostery, intrinsically disordered proteins, interactions, cellular context, thermodynamics and experimental function. | NMR, single-molecule methods, cryo-EM ensembles, kinetics, mutational scans and prospective wet-lab validation. **Static structure prediction is not a complete solution of protein folding or function.** |
| Neural and collective dynamics | Population recordings reveal low-dimensional structure and behavior-linked activity. | Neural code, causal computation, learning across scales, consciousness, embodied control and general principles of collective animal behavior. | Closed-loop perturbation, simultaneous behavior/recording, cross-animal generalization and mechanistic models with out-of-sample predictions. |
| Origins and evolution of life | Chemistry can generate building blocks, compartments and autocatalytic motifs under plausible conditions. | Transition from geochemistry to heredity and evolution; origin of homochirality, genetic code, metabolism and robust protocells; likelihood of multiple origins. | Prebiotic chemistry, synthetic protocells, geological/planetary constraints and explicit selection experiments. |

---

## 10. Geophysics, climate, heliophysics, and complex Earth systems

### Current status

Earth and space science confront inverse problems in a system that cannot be rerun, has sparse historical coverage, spans enormous scales and contains coupled physical, chemical and biological feedbacks. The National Academies’ [Earth in Time](https://nap.nationalacademies.org/resource/25761/interactive/) assessment organizes major solid-Earth and surface priorities; the 2024 [solar and space physics decadal survey](https://nap.nationalacademies.org/resource/27938/interactive/) does the same for heliophysics.

| Frontier | What is known | What remains open | Decisive observables and programs |
|---|---|---|---|
| Geodynamo and deep Earth | Core convection sustains the magnetic field; seismology constrains radial structure and heterogeneity. | Dynamo onset, reversals and long-term power; core–mantle exchange; inner-core evolution; mantle plumes and deep volatile cycles. | Seismology, mineral physics at extreme conditions, geomagnetism, geoneutrinos and data-assimilating dynamo simulations. |
| Origin of plate tectonics | Modern plate tectonics explains seafloor spreading, subduction and continental motion. | When and why mobile-lid tectonics began; feedbacks among water, crust, mantle and life; continental stabilization. | Ancient rocks, isotope geochemistry, paleomagnetism, thermomechanical models and comparative planetology. |
| Earthquake rupture and forecasting | Plate loading and fault friction generate earthquakes; probabilistic hazard maps and rapid early-warning systems are useful. | Nucleation, cascade versus pre-set rupture, slow-slip coupling, maximum event size and skillful time-dependent forecasts. | Dense seismic/geodetic networks, borehole observatories, laboratory friction and prospective forecast tests. The USGS states that exact time–place–magnitude earthquake prediction is not currently possible ([FAQ](https://www.usgs.gov/faqs/can-you-predict-earthquakes)); early warning after rupture begins is not prediction. |
| Volcanic systems | Deformation, gas and seismicity can reveal magma movement. | Magma storage geometry, eruption triggers, transition between effusive/explosive behavior and reliable probabilistic eruption forecasts. | Satellite and ground deformation, gas chemistry, seismic imaging, petrology and real-time data fusion. |
| Climate sensitivity and clouds | Greenhouse-gas forcing and human-caused warming are established; global models reproduce many large-scale features. | Equilibrium sensitivity range, cloud/aerosol feedbacks, regional precipitation and extremes, compound events and decadal variability. | Process observations, paleoclimate, model ensembles, emergent constraints and out-of-sample regional evaluation. |
| Tipping elements and ice sheets | Abrupt transitions are physically plausible in ice sheets, circulation, ecosystems and permafrost. | Thresholds, timescales, reversibility and interaction among tipping elements; high-end sea-level trajectories and AMOC response. | Paleorecords, sustained ocean/ice observations, process models and early-warning diagnostics. See [IPCC AR6 Chapter 4](https://www.ipcc.ch/report/ar6/wg1/chapter/chapter-4/). |
| Water, carbon and critical zone | Coupled hydrologic, ecological and geochemical cycles regulate climate, soils and resources. | Groundwater depletion, vegetation–climate feedback, permafrost carbon, weathering and nutrient limits, regional predictability under land-use change. | Flux networks, isotopes, remote sensing, catchment experiments and coupled Earth-system models. |
| Space weather | Solar eruptions and solar-wind coupling drive magnetospheric and ionospheric disturbances. | Reliable eruption onset and arrival forecasts, geomagnetic-storm intensity, radiation hazards, reconnection and cross-scale energy transfer. | Continuous solar imaging, upstream monitors, multi-spacecraft constellations, ground networks and assimilative models. See NASA’s [heliophysics decadal overview](https://science.nasa.gov/heliophysics/heliophysics-decadal-survey/). |
| Multihazard risk | Hazard, exposure and vulnerability jointly determine disasters. | Cascades, correlated extremes, infrastructure/network failure, uncertainty communication and equitable adaptation under nonstationarity. | Scenario ensembles, stress tests, causal post-event analysis and prospective decision audits. |

---

## 11. Cross-domain bridge questions

These are productive connections because they share mathematics or measurable structure. They are not licenses to equate unlike systems.

| Bridge | Shared structure | Concrete research question |
|---|---|---|
| Quantum information ↔ spacetime | Entanglement, error correction, complexity | Which information-theoretic statements remain valid outside special holographic models and generate falsifiable gravitational predictions? |
| Effective field theory ↔ particles ↔ nuclei ↔ cosmology | Symmetries, scale separation, operator expansions | Can low-energy measurements consistently constrain the same ultraviolet physics across collider, nuclear, atomic and cosmological data? |
| Hydrodynamics ↔ QGP ↔ cold atoms ↔ electron fluids ↔ plasmas | Conservation laws, constitutive relations, transport | When does hydrodynamics emerge without quasiparticles, and which transport bounds or attractors are universal? |
| Topology ↔ materials ↔ photonics ↔ fluids | Global invariants and protected response | What survives interactions, disorder, dissipation and nonequilibrium driving strongly enough to build robust devices? |
| Active matter ↔ tissues ↔ robot swarms | Self-propulsion, feedback, collective modes | Which macroscopic laws depend only on symmetries and conservation, and which depend irreducibly on biological information processing? |
| Glasses ↔ optimization ↔ inference | Rugged landscapes, metastability, slow dynamics | Which glass concepts predict algorithmic hardness or learning dynamics prospectively rather than merely describing them afterward? |
| Turbulence ↔ climate ↔ astrophysical plasma | Cascades, intermittency, coherent structures | Which cascade and closure concepts transfer across compressibility, magnetization, rotation, stratification and active forcing? |
| Inverse problems ↔ all observational sciences | Latent variables, selection effects, uncertainty | How can simulation-based inference remain calibrated under model misspecification and unobserved confounders? |

---

## 12. Claims requiring explicit caveats

| Tempting claim | Accurate status |
|---|---|
| “DESI discovered evolving dark energy.” | DESI DR2 plus other datasets show a model- and combination-dependent **hint**; no discovery. |
| “Muon \(g-2\) proves new physics.” | The final experimental result is precise, but the 2025 consensus theory value is compatible; hadronic theory-method tensions remain. |
| “Bell tests prove one interpretation of quantum mechanics.” | They exclude broad local-hidden-variable models under stated assumptions; they do not select a unique interpretation. |
| “Islands solved the black-hole information problem.” | They reproduce the entropy curve in controlled models; realistic microscopic encoding, interiors and singularity resolution remain open. |
| “Gravitationally induced entanglement would automatically prove gravity is quantum.” | Classical-gravity-plus-quantum-matter alternatives can mimic some signatures; protocol assumptions and stronger witnesses matter. |
| “NIF achieved commercial breakeven.” | NIF achieved capsule/target ignition and target gain above one, not net wall-plug electricity or a power-plant cycle. |
| “AlphaFold solved protein folding.” | It transformed static structure prediction; dynamics, ensembles, interactions, thermodynamics and cellular function remain open. |
| “Earthquakes can now be predicted.” | Probabilistic hazard, operational forecasts and early warning are possible; exact time–place–magnitude prediction is not. |
| “Solving Navier–Stokes regularity solves turbulence.” | Regularity is a foundational mathematical problem; predictive turbulent statistics and closure are distinct. |
| “Agreement with GR proves there is no quantum gravity.” | It constrains deviations in measured regimes; all viable quantum-gravity theories must reproduce GR there. |
| “A null direct-detection search rules out dark matter.” | It constrains specified interactions, masses and halo assumptions; the astronomical missing-mass problem remains. |
| “A quantum simulator has solved the material.” | Analog agreement is strongest when independently calibrated, scalable, and cross-checked against controlled limits or other methods. |

---

## 13. How to turn an open problem into a serious theory note

Every speculative note should answer:

1. **Target:** What specific empirical fact, inconsistency, or missing derivation is addressed?
2. **Baseline:** What is the strongest existing model and where precisely does it fail?
3. **Assumptions:** Which symmetries, degrees of freedom, scales and initial/boundary conditions are introduced?
4. **Consistency:** Are dimensions, conservation laws, unitarity/causality, thermodynamics and known limits respected?
5. **Recovery:** Does the proposal reduce to established theory in every tested regime?
6. **Distinct prediction:** What outcome differs from alternatives, with a numerical magnitude or scaling law?
7. **Falsifier:** Which observation would rule it out?
8. **Systematics:** Could calibration, selection, nuisance parameters or model misspecification mimic the effect?
9. **Prior art:** Which existing theory already contains the same mechanism under another name?
10. **Evidence level:** Is the idea a mathematical possibility, a phenomenological model, a fitted explanation, or an independently confirmed theory?

> [!tip] Productive imagination
> The best “dot connection” is not the one with the most analogies. It is the one that compresses several facts into a smaller set of assumptions and then risks a new, falsifiable prediction.

## 14. Maintenance protocol

- Stamp every numerical constraint and experiment status with a date.
- Prefer collaboration papers and official program pages over press summaries.
- Preserve null results; they are part of the map, not failed stories.
- Separate **observed phenomenon**, **inferred parameter**, and **interpretive model**.
- Track tensions with at least: datasets used, significance metric, look-elsewhere treatment, dominant systematics, and independent replication status.
- Never silently replace an old consensus: append a short “superseded by” note so the vault records how understanding changed.
- Re-audit fast-moving sections at least yearly: dark-energy constraints, neutrino ordering/CP, direct dark-matter searches, gravitational-wave catalogs, collider anomalies, quantum-computing milestones, fusion schedules and climate-tipping estimates.
