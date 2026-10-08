---
title: "Synthesis Session 002 — Holographic Coarse-Graining and the Memory of Spacetime"
type: synthesis
field: "Cross-domain"
epistemic_status: "conjectural"
level: "advanced"
tags: [physics, synthesis, quantum-gravity, holography, coarse-graining, information]
created: 2026-07-30
updated: 2026-09-02
prior_art_audit: initial-not-exhaustive
---

# Synthesis Session 002 — Holographic Coarse-Graining and the Memory of Spacetime

> [!warning] Research status
> This note develops a **candidate analogy**, not an established identification and not a novelty claim. Replica-wormhole contributions have not been derived as a Mori–Zwanzig memory kernel. The included finite-size SYK calculation does not model an evaporating black hole, and its original cumulative-backflow criterion was invalidated by observation-window dependence.

[[Synthesis Lab]] · [[Deep Dive — Mori-Zwanzig Projection|Mori–Zwanzig Projection]] · [[Black Hole Information Problem]] · [[Synthesis Session 001 — Response-Preserving Coarse-Graining]]

## 1. The careful question

Projection methods and holographic effective descriptions both separate retained from unretained information. That structural resemblance motivates a precise question:

> In a specified solvable model of an evaporating gravitating system coupled to a bath, can an operator-space Mori–Zwanzig projection onto a declared semiclassical algebra produce a memory-kernel feature tied quantitatively to the independently computed quantum-extremal-surface transition?

This is much narrower than saying that “the Page time is a Markov-to-non-Markov transition.” The latter statement is currently unsupported and is projection- and observable-dependent even before gravity is considered.

## 2. Established ingredients

### Mori–Zwanzig identity

Given a Liouville generator $L$, an operator-space projection $P$, and $Q=1-P$, the Dyson identity yields an exact generalized equation for projected observables. Schematically,

$$
\dot Z(t)=F[Z(t)]+\int_0^t \mathcal K(t-s;Z(s))\,ds+\eta(t).
$$

The drift, memory, and orthogonal term depend on the projection, inner product, initial ensemble, and observable algebra. A short or small kernel for one projection does not define an invariant property of the full system. Equilibrium fluctuation–dissipation relations also require a specified normalization and equilibrium inner product; the scalar mnemonic $\langle\eta(t)\eta(0)\rangle\propto K(t)$ is not a universal operator identity.

### Holographic reconstruction

In semiclassical code subspaces of AdS/CFT, bulk reconstruction has the structure of operator-algebra quantum error correction. Leading holographic entanglement entropy is related to an extremal area, with bulk-entropy corrections incorporated by generalized entropy. These are controlled results **conditional on the holographic dictionary and its regime**, not direct empirical statements about our universe.

### Islands and the Page curve

In controlled gravitating-system-plus-bath models, competing generalized-entropy saddles reproduce a unitary Page-curve shape. The transition selects a different quantum extremal surface in the entropy calculation. It does not by itself prove that local semiclassical evolution becomes non-Markovian at that time, nor that a particular temporal memory kernel equals a replica-wormhole saddle.

## 3. Where the analogy can fail

| Proposed bridge | Necessary caution |
|---|---|
| retained bulk fields ↔ resolved variables | Mori–Zwanzig projects observables or distributions after an inner product is chosen; a code-subspace isometry is not automatically that projection |
| replica wormholes ↔ temporal memory | wormholes are saddle contributions to replicated entropy calculations; memory kernels describe time-nonlocal reduced dynamics |
| Page time ↔ memory onset | “memory onset” changes with the observable, state, projection, metric, smoothing, and threshold |
| exact boundary unitarity ↔ exact projected equation | the formal projected identity is exact, but closure and a tractable kernel are not |
| island dominance ↔ failure of all semiclassical observables | an entropy saddle can change while many local observables remain accurately semiclassical |

A useful connection must derive a mapping between mathematical objects, not merely align their narratives.

## 4. A falsifiable program

### Model

Use a model with actual information transfer to a bath: for example, a coupled SYK/bath construction or a solvable two-dimensional gravity model whose radiation entropy and generalized-entropy saddles are independently calculable. A fixed finite Hamiltonian with a fixed bipartition is a control system, not an evaporation model.

### Projection

Declare all of the following before computing a kernel:

1. the resolved operator algebra;
2. the equilibrium or nonequilibrium inner product defining $P$;
3. the initial system–bath state;
4. which observables the closure must predict;
5. how the kernel norm is made dimensionless;
6. the time window and resolution;
7. an independently defined QES/Page transition time.

### Comparisons

- Compare local correlators, radiation entropy, conserved charges, and reconstruction-sensitive observables separately.
- Include non-holographic random-matrix and integrable controls with matched Hilbert-space size.
- Test several legitimate projections. A feature that disappears under small projection changes is not a universal gravitational signature.
- Prefer a kernel-derived prediction on held-out forcing or initial states over a post-hoc coincidence of two extracted times.

### Decision rule

Evidence for the bridge would require a pre-registered, window-independent kernel feature that:

- converges under time-step, sample, and system-size refinement;
- tracks an independently computed QES transition across parameter changes, rather than only in one realization;
- is absent or parametrically different in matched non-holographic controls;
- improves a held-out observable prediction over a Markov closure;
- survives reasonable changes of the projection.

The proposal is disfavored if the feature tracks recurrence time, observation-window length, arbitrary thresholds, or generic finite-system thermalization instead of the QES transition.

## 5. What Computational Lab 14 does—and does not do

`62 Computational Labs/14_syk_mori_zwanzig.py` is retained as an **exploratory finite-matrix diagnostic**. It constructs a small $q=4$ SYK Hamiltonian, checks the Majorana algebra and entropy bounds, evolves a product state under a fixed closed Hamiltonian, and computes several correlation and trace-distance diagnostics.

It does **not** currently test the central gravitational question:

- the system does not evaporate into an external bath;
- the time of the first smoothed entropy maximum is an **entanglement-peak time**, not the black-hole Page time;
- trace-distance revival for selected initial states is not the optimized Breuer–Laine–Piilo measure of a fully characterized reduced dynamical map;
- the former “50% cumulative backflow” time scales with the chosen observation window and is therefore not intrinsic;
- small-$N$ recurrences dominate late-time behavior;
- the earlier local observable omitted the factor of $i$ in $i\chi_0\chi_1$, so Hermitianization annihilated it. The release code corrects that implementation bug, but earlier kernel plots must not be interpreted.

The earlier numerical claim of Page-time/memory equivalence is therefore **withdrawn**. The computation remains useful as a lesson in defining operational diagnostics and detecting post-hoc thresholds.

## 6. Prior-art boundary

Mori–Zwanzig projection, holographic RG, error-correcting reconstruction, islands, replica wormholes, open-system non-Markovianity, and SYK/JT low-energy matching are all established research literatures. This note has not established that their proposed combination is absent from prior work. Any future novelty statement requires a systematic literature matrix comparing the projection, resolved algebra, model, kernel, and observable.

Useful anchors:

- [Mori, *Progress of Theoretical Physics* 33, 423 (1965)](https://doi.org/10.1143/PTP.33.423)
- [Almheiri, Dong, and Harlow, *JHEP* 2015, 163](https://doi.org/10.1007/JHEP04(2015)163)
- [Penington, *JHEP* 2020, 002](https://doi.org/10.1007/JHEP09(2020)002)
- [Almheiri, Engelhardt, Marolf, and Maxfield, *JHEP* 2019, 063](https://doi.org/10.1007/JHEP12(2019)063)
- [[Synthesis Session 001 — Response-Preserving Coarse-Graining]] for a better-controlled general benchmark.

## 7. Next action

- [ ] Replace the fixed-bipartition control with a genuine system–bath evaporation model.
- [ ] Define $P$ on an explicit operator algebra and derive the corresponding kernel.
- [ ] Validate kernel extraction on a model with a known generalized Langevin equation.
- [ ] Pre-register an intrinsic statistic before comparing with a QES transition.
- [ ] Treat a null result as informative: replica saddles and dynamical memory may be distinct structures.

## Navigation

[[Synthesis Lab]] · [[Connection Ledger]] · [[Research Question Incubator]] · [[Open Problems Dashboard]] · [[Physics Worldmap]]
