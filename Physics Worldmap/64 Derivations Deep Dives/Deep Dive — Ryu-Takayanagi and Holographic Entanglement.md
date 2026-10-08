---
title: "Deep Dive — Ryu-Takayanagi and Holographic Entanglement"
type: derivation
field: "Relativity and Gravitation"
epistemic_status: mixed
level: advanced
tags: [physics, derivation, deep-dive, holography, entanglement]
created: 2026-07-31
updated: 2026-09-02
note_maturity: worked-derivation
source_audit: canonical-derivation-needs-citation-audit
---

# Deep Dive — Ryu-Takayanagi and Holographic Entanglement

## The question

Assuming a holographic duality with a semiclassical bulk description, a boundary CFT region $A$ has a von Neumann entanglement entropy $S(\rho_A)$. What bulk geometric quantity computes its leading contribution?

> [!warning] Conditional status
> The RT/HRT and quantum-extremal-surface prescriptions are highly developed results **within holographic duality and their controlled semiclassical regimes**. AdS/CFT itself remains a conjectured duality, and none of these formulas is a general identity for arbitrary quantum systems or gravitating spacetimes.

## Setup and assumptions

We assume a regime where a semiclassical AdS/CFT description is under perturbative control:

1. **Large-$N$, strong-coupling limit**: The boundary theory has a large effective number of degrees of freedom, while parameters are chosen so both bulk quantum loops and string-scale corrections are suppressed. The precise dictionary is model- and convention-dependent.
2. **Static spacetime**: The bulk geometry is time-independent. (The covariant generalization by Hubeny-Rangamani-Takayanagi handles time-dependent cases.)
3. **Einstein gravity**: The bulk action is the Einstein-Hilbert action with possible matter fields but no higher-derivative gravitational terms.

For an AdS$_{d+1}$/CFT$_d$ dual pair, the boundary theory is $d$-dimensional and a boundary spatial slice is $(d-1)$-dimensional. We partition such a spatial slice into a region $A$ and its complement $\bar{A}$.

## The Ryu-Takayanagi formula

**Leading semiclassical prescription** (Ryu and Takayanagi, 2006): The entanglement entropy of region $A$ in a static holographic state is

$$S(\rho_A) = \frac{\text{Area}(\gamma_A)}{4 G_N}$$

where $\gamma_A$ is the minimal-area codimension-2 surface in the bulk that:
- Is homologous to $A$ (meaning $\gamma_A$ and $A$ together bound a bulk region, the **homology constraint**).
- Is anchored to $\partial A$ (the boundary of region $A$ on the AdS boundary).

When multiple extremal surfaces exist, take the one with smallest area.

## Derivation sketch: the replica trick

A standard derivation within semiclassical holography uses the **gravitational replica trick** (Lewkowycz and Maldacena, 2013). It assumes replica-symmetric saddles and an analytic continuation away from integer replica number; these are substantive assumptions, not a fully general proof.

### Step 1: Replica trick for entanglement entropy

For any quantum state $\rho_A$, the von Neumann entropy can be computed via the replica trick:

$$S(\rho_A) = -\operatorname{Tr}(\rho_A \ln \rho_A) = -\lim_{n \to 1} \frac{\partial}{\partial n} \operatorname{Tr}(\rho_A^n)$$

The $n$-th Renyi entropy is $S_n = \frac{1}{1-n} \ln \operatorname{Tr}(\rho_A^n)$. We compute $\operatorname{Tr}(\rho_A^n)$ for integer $n$, then analytically continue to $n \to 1$.

### Step 2: Path integral for $\operatorname{Tr}(\rho_A^n)$

In a $d$-dimensional CFT, $\operatorname{Tr}(\rho_A^n)$ is computed by a path integral on an $n$-sheeted branched cover $\mathcal{M}_n$ of the original Euclidean spacetime. The branch cut runs along $A$: going around $\partial A$ cycles through $n$ copies of the manifold.

$$\operatorname{Tr}(\rho_A^n) = \frac{Z[\mathcal{M}_n]}{(Z[\mathcal{M}_1])^n}$$

where $Z[\mathcal{M}_n]$ is the partition function on the $n$-sheeted manifold.

### Step 3: Bulk dual of the replicated boundary

By AdS/CFT, $Z[\mathcal{M}_n] = Z_{\text{grav}}[\mathcal{B}_n]$, where $\mathcal{B}_n$ is the bulk geometry whose conformal boundary is $\mathcal{M}_n$. In the large-$N$ (classical gravity) limit:

$$Z_{\text{grav}}[\mathcal{B}_n] \approx e^{-I[\mathcal{B}_n]}$$

where $I[\mathcal{B}_n]$ is the on-shell gravitational action of the dominant bulk saddle.

Assuming the boundary replica symmetry $\mathbb{Z}_n$ extends into the dominant bulk saddle, define the quotient geometry

$$\hat{\mathcal B}_n=\mathcal B_n/\mathbb Z_n.$$

Away from the fixed set, the cover has $n$ copies of the quotient and $I[\mathcal B_n]=nI[\hat{\mathcal B}_n]$. The quotient has a codimension-two fixed locus carrying a conical defect; treating its replica-number variation carefully produces the entropy term.

### Step 4: The conical singularity

The fixed-point set of the $\mathbb{Z}_n$ replica symmetry in the bulk is a codimension-2 surface. On the quotient space $\hat{\mathcal{B}}_n$, this fixed-point set becomes a **conical singularity** with deficit angle $\delta = 2\pi(1 - 1/n)$.

For Einstein gravity, the curvature localized at a cone of opening angle $2\pi/n$ makes the replica derivative of the on-shell action proportional to the fixed-set area. A convenient form of the gravitational entropy is

$$
S_A=\left.(n\partial_n-1)I[\mathcal B_n]\right|_{n=1}
=\frac{\operatorname{Area}(\gamma_A)}{4G_N}.
$$

This expression avoids treating an off-shell cone contribution as a standalone derivation; the equations of motion and the $n\to1$ regularity condition are essential.

### Step 5: Taking the $n \to 1$ limit

Equivalently, differentiating the normalized replicated partition function at $n=1$ extracts precisely the same area contribution. The analytic continuation from integer $n$ and the selection of the dominant saddle remain part of the prescription.

### Step 6: Extremality and minimality

The saddle-point condition for the bulk geometry requires that the metric equation of motion is satisfied everywhere, including at the conical singularity in the $n \to 1$ limit. Lewkowycz and Maldacena showed that this requires $\gamma$ to be an **extremal surface** (vanishing mean curvature, or equivalently, locally extremizing area). Among all extremal surfaces homologous to $A$, the dominant saddle corresponds to the one with minimal area.

## The quantum extremal surface formula

The RT formula receives quantum corrections at order $G_N^0$ (subleading in $1/N$). The **quantum extremal surface (QES)** formula (Engelhardt and Wall, 2014) is:

$$S(\rho_A) = \min_{\gamma} \operatorname{ext}_{\gamma} \left[\frac{\text{Area}(\gamma)}{4 G_N} + S_{\text{bulk}}(\Sigma_\gamma)\right]$$

where $S_{\text{bulk}}(\Sigma_\gamma)$ is the von Neumann entropy of quantum fields in the bulk region $\Sigma_\gamma$ bounded by $\gamma$ and $A$. The instruction is: find all surfaces that extremize the **generalized entropy** (area term plus bulk entropy), then take the minimum.

This quantum-corrected formula is the foundation for the **island rule**, which reproduces a unitary Page curve in important controlled models. Whether and how it furnishes a complete microscopic resolution in general quantum gravity remains an active question.

## The island formula

For a gravitating system (like an evaporating black hole) coupled to a non-gravitating bath (the radiation), the island formula computes the entropy of the radiation $R$:

$$S(R) = \min \operatorname{ext} \left[\frac{\text{Area}(\partial I)}{4 G_N} + S_{\text{bulk}}(I \cup R)\right]$$

where $I$ is an **island** -- a region of the gravitating spacetime that is separated from $R$ but contributes to the entropy calculation. The minimization is over all possible islands (including the trivial island $I = \emptyset$).

**Before the saddle transition in standard toy models**: The trivial island $I = \emptyset$ dominates, and the computed radiation entropy grows approximately as in the semiclassical Hawking calculation.

**After the saddle transition in those models**: A nontrivial island can dominate. The resulting generalized entropy follows the decreasing branch expected from a Page curve.

In the relevant evaporating-system setups, the crossing of the island and no-island generalized entropies occurs near what is called the **Page time**. This terminology should not be exported to entropy maxima in arbitrary finite bipartite systems.

## Speculative connection to Mori-Zwanzig projection

The RT and island formulas suggest a loose structural analogy with coarse-graining (see [[Synthesis Session 002 — Holographic Coarse-Graining and the Memory of Spacetime]]), but no derivation currently identifies their ingredients with a Mori–Zwanzig (MZ) decomposition:

1. **Area versus discarded information**: It is tempting to compare $\operatorname{Area}(\gamma)/4G_N$ with information excluded by a chosen effective description. It is not generally the entropy of an MZ irrelevant subspace.

2. **Islands versus memory**: Both involve information outside a naive subsystem description, but an island is selected by a generalized-entropy extremization, whereas an MZ memory kernel depends on a declared projection and dynamics.

3. **Saddle changes versus non-Markovianity**: A QES saddle change is not known to coincide with a Markov-to-non-Markov transition. Any proposed relation must specify the open-system split, projection, observable, and an intrinsic non-Markovianity measure.

This is a candidate research question, not a correspondence established by the current finite-size SYK diagnostic. A meaningful test needs an evaporating system coupled to a bath and an independently defined QES transition.

## Checks and limitations

**Dimensional check**: In $d+1$ bulk dimensions, $\gamma$ is $(d-1)$-dimensional. $\text{Area}(\gamma)/4G_N$ is dimensionless (in natural units where $G_N$ has dimensions of length$^{d-1}$), matching the dimensionless entropy $S$.

**Known limits**:
- For a single interval of length $\ell$ in the vacuum of a 2d CFT (dual to AdS$_3$), the regulated RT geodesic has length $L=2R_{\text{AdS}}\ln(\ell/\epsilon)$, giving $S=(c/3)\ln(\ell/\epsilon)$ with $c=3R_{\text{AdS}}/(2G_N^{(3)})$ at leading order.
- For a spherical region in any dimension, the RT surface is known analytically and reproduces the expected UV-divergent area law with the correct coefficient.

**Limitations**:
- The classical RT formula is valid only in the large-$N$ limit. Quantum corrections require the QES formula.
- The derivation assumes the existence of a smooth bulk dual, which may not hold for all CFT states.
- Higher-derivative gravity generally requires a generalized entropy functional (for example the Dong or Camps functional); it is not always obtained by simply substituting Wald entropy.
- The covariant (HRT) generalization to time-dependent spacetimes uses extremal surfaces rather than minimal surfaces and requires additional assumptions about the homology constraint.

## Sources

- S. Ryu and T. Takayanagi, "Holographic derivation of entanglement entropy from AdS/CFT," *Phys. Rev. Lett.* **96**, 181602 (2006).
- A. Lewkowycz and J. Maldacena, "Generalized gravitational entropy," *JHEP* **2013**, 090 (2013).
- N. Engelhardt and A. C. Wall, "Quantum extremal surfaces: holographic entanglement entropy beyond the classical regime," *JHEP* **2015**, 073 (2015).
- G. Penington, "Entanglement wedge reconstruction and the information problem," *JHEP* **2020**, 002 (2020).
- A. Almheiri, N. Engelhardt, D. Marolf, and H. Maxfield, "The entropy of bulk quantum fields and the entanglement wedge of an evaporating black hole," *JHEP* **2019**, 063 (2019).

## Navigation

[[Derivation Atlas]] · [[Holographic Principle]] · [[AdS-CFT Correspondence]] · [[Black Hole Information Problem]] · [[Quantum Error Correction and Gravity]] · [[Synthesis Session 002 — Holographic Coarse-Graining and the Memory of Spacetime]]
