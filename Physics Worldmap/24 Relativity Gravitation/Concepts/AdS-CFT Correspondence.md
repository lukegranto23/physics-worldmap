---
type: "concept"
field: "Relativity and Gravitation"
epistemic_status: "conjectural"
level: "advanced"
tags: ["physics", "field/relativity", "status/conjectural", "level/advanced"]
aliases: ["AdS/CFT", "Maldacena duality", "gauge/gravity duality", "holographic duality"]
created: 2026-07-30
updated: 2026-07-30
note_maturity: expanded
source_audit: bibliography-present-needs-claim-audit
---

# AdS-CFT Correspondence

> [!summary] Core idea
> The AdS/CFT conjecture identifies Type IIB string theory on $\text{AdS}_5 \times S^5$ with $\mathcal{N}=4$ super-Yang-Mills theory in four dimensions. More broadly, gauge/gravity dualities propose equivalent descriptions of certain anti-de Sitter quantum-gravity systems and nongravitational boundary theories.

> [!note] Documentation status
> This expanded note includes a canonical bibliography but has not yet received a claim-by-claim source audit. The epistemic label describes the standing of the underlying physics in its stated regime; it does not certify every sentence or equation in this note.

## Why this matters

This is the best-developed realization of the [[Holographic Principle]]. If the conjecture is exact, the boundary theory supplies a nonperturbative definition of the corresponding quantum-gravity theory in AdS. In controlled large-$N$, strong-coupling regimes, the dictionary also maps some strongly coupled quantum calculations to tractable semiclassical gravity problems.

## Mathematical framework

### The original conjecture (Maldacena, 1997)

Consider $N$ coincident D3-branes in Type IIB string theory. Maldacena's decoupling argument motivates two descriptions of the same low-energy sector:
1. **Open string side**: $\mathcal{N}=4$ $SU(N)$ super-Yang-Mills (SYM) in 4 dimensions with coupling $g_{YM}$.
2. **Closed string side**: Type IIB string theory on $\text{AdS}_5 \times S^5$ with radius $L$ and string coupling $g_s$.

The parameters match as:

$$g_{YM}^2 = 4\pi g_s, \qquad \frac{L^4}{\alpha'^2} = 4\pi g_s N = g_{YM}^2 N = \lambda$$

where $\lambda = g_{YM}^2 N$ is the 't Hooft coupling and $\alpha'=\ell_s^2$. This common convention uses $\operatorname{Tr}(T^aT^b)=\delta^{ab}/2$; factors of two can move with gauge-generator normalization. The conjecture claims an exact equivalence for all $N$ and $\lambda$, whereas most direct calculations control special limits or protected quantities.

### Useful limits

- **Planar limit** ($N \to \infty$, $\lambda$ fixed): the gauge-theory genus expansion maps to a weakly coupled string expansion; the string worldsheet can still be strongly curved when $\lambda$ is not large.
- **Strong coupling** ($\lambda \gg 1$ in addition): strings are short compared to $L$, so classical (super)gravity on $\text{AdS}_5 \times S^5$ is a good approximation. This is the most calculationally powerful regime.
- **Weak coupling** ($\lambda \ll 1$): perturbative gauge theory is valid, but the bulk description involves highly curved, stringy geometry.

### The AdS metric

$\text{AdS}_{d+1}$ in Poincare coordinates:

$$ds^2 = \frac{L^2}{z^2}\left(-dt^2 + d\vec{x}^2 + dz^2\right)$$

The boundary is at $z \to 0$; the deep interior ("IR" in the bulk) is $z \to \infty$. The radial coordinate $z$ maps to the energy scale in the CFT: $z \sim 1/E$.

### The GKPW relation

The central quantitative statement, due to Gubser-Klebanov-Polyakov and Witten (1998):

$$\left\langle \exp\!\left(\int d^d x\, \phi_0(\vec{x})\,\mathcal{O}(\vec{x})\right)\right\rangle_{\text{CFT}} = Z_{\text{string}}\!\left[\phi \big|_{z\to 0} = \phi_0\right]$$

The left side is the generating functional for CFT correlators of an operator $\mathcal{O}$, sourced by $\phi_0$. The right side is the bulk string-theory partition function with the boundary condition that the bulk field $\phi$ approaches $\phi_0$ at the AdS boundary (with Euclidean-signature conventions understood).

In the classical gravity limit ($N \to \infty$, $\lambda \to \infty$):

$$Z_{\text{string}} \approx e^{-S_{E,\text{on-shell}}[\phi_{\text{cl}}]}$$

where $\phi_{\text{cl}}$ is the classical solution with the given boundary condition. CFT correlation functions become derivatives of the on-shell gravitational action.

### The holographic dictionary

| Bulk (gravity) | Boundary (CFT) |
|---|---|
| Scalar field of mass $m$ | Operator of dimension $\Delta$, where $m^2 L^2 = \Delta(\Delta - d)$ |
| Gauge field $A_\mu$ | Conserved current $J^\mu$ |
| Metric perturbation $h_{\mu\nu}$ | Stress tensor $T^{\mu\nu}$ |
| Black hole | Thermal state at temperature $T = r_+/(\pi L^2)$ for planar BH |
| Radial coordinate $z$ | Energy scale $E \sim 1/z$ (renormalization group) |
| Geodesic length | Two-point function (heavy operators) |
| Minimal surface area | Entanglement entropy (Ryu-Takayanagi) |

### Holographic renormalization

Near the boundary $z \to 0$, bulk fields diverge. These divergences map to UV divergences of the CFT. The procedure of adding covariant boundary counterterms to regulate the on-shell action is *holographic renormalization*. It produces finite, scheme-dependent correlation functions that satisfy the expected CFT Ward identities.

### Ryu-Takayanagi formula (2006)

The entanglement entropy of a boundary region $A$ in the CFT vacuum is:

$$S_A = \frac{\text{Area}(\gamma_A)}{4 G_N}$$

where $\gamma_A$ is the minimal-area bulk surface homologous to $A$ and anchored on $\partial A$. This connects quantum information in the CFT to geometry in the bulk. The quantum-corrected version (Faulkner-Lewkowycz-Maldacena, 2013) adds bulk entanglement entropy:

$$S_A = \frac{\text{Area}(\gamma_A)}{4 G_N} + S_{\text{bulk}}(\Sigma_A)$$

where $\Sigma_A$ is the bulk region between $A$ and $\gamma_A$, and $\gamma_A$ now extremizes the *generalized entropy*.

## Physical content

### Why the duality is believed

No general first-principles proof is known, but there is extensive and mutually consistent theoretical evidence:

1. **Symmetry matching**: The isometry group of $\text{AdS}_5 \times S^5$ is $SO(4,2) \times SO(6)$, which matches the conformal group times the $R$-symmetry of $\mathcal{N}=4$ SYM.
2. **BPS spectrum**: Protected states (BPS operators) match exactly between both sides at all couplings.
3. **Anomalies**: The conformal anomaly of $\mathcal{N}=4$ SYM ($a = c = N^2/4$ at large $N$) matches the holographic calculation.
4. **Integrability**: In the planar limit, both sides exhibit integrable structures. The spin-chain / string Bethe ansatz interpolates between weak and strong coupling with no sign of discontinuity.
5. **Precision tests**: Localization results give exact answers for certain partition functions and Wilson loops that agree with gravity at strong coupling.

### Finite temperature and black holes

A black hole in AdS corresponds to a thermal state in the CFT. The Hawking-Page phase transition (thermal AdS $\leftrightarrow$ large AdS black hole) maps to a confinement-deconfinement transition in the gauge theory. This was one of the first physical predictions.

### Applications beyond the original setting

The correspondence has been generalized to:
- Different dimensions (AdS$_3$/CFT$_2$, AdS$_4$/CFT$_3$, AdS$_7$/CFT$_6$).
- Less supersymmetry and broken conformal invariance (holographic QCD, applied holography).
- Condensed matter applications: holographic superconductors, strange metals, entanglement phase transitions.
- [[Black Hole Information Problem]]: the existence of a unitary boundary dual strongly suggests information is preserved.

## Key results

- Maldacena (1997): original conjecture.
- Gubser-Klebanov-Polyakov; Witten (1998): GKPW prescription for computing correlators.
- Ryu-Takayanagi (2006): entanglement entropy from minimal surfaces.
- Faulkner-Lewkowycz-Maldacena (2013): quantum corrections to Ryu-Takayanagi.
- Engelhardt-Wall (2014): quantum extremal surface prescription.
- Integrability of planar $\mathcal{N}=4$ SYM / strings on $\text{AdS}_5 \times S^5$ (Beisert et al., 2012 review).

## Open questions

1. **Proof of the duality.** There is no first-principles derivation. The strongest checks are precision tests in protected sectors.
2. **Beyond AdS.** Our universe has a positive cosmological constant ($\Lambda > 0$). A $dS/CFT$ analogue is not well-understood.
3. **Flat space holography.** Asymptotically flat spacetimes do not have a conformal boundary. Celestial holography and BMS symmetry are active approaches.
4. **Bulk reconstruction.** How much of the bulk geometry can be reconstructed from boundary data? The [[Quantum Error Correction and Gravity|quantum error correction]] perspective has been illuminating.
5. **Strongly coupled CFT at finite $N$.** Most calculations rely on the large-$N$ or strong-coupling limit. Finite-$N$ corrections probe stringy and quantum gravity effects.

## Connection to other fields

- [[Holographic Principle]]: AdS/CFT is its best-developed proposed realization.
- [[Black Hole Information Problem]]: in examples with a standard unitary boundary theory, the conjectured dual description strongly supports bulk unitarity.
- [[Black Hole Thermodynamics]] and [[Hawking Radiation]]: black hole entropy and temperature emerge from the boundary theory.
- [[Quantum Error Correction and Gravity]]: within semiclassical code subspaces, bulk reconstruction has quantum-error-correcting structure.
- [[Tensor Networks and Physics]]: MERA and holographic codes model the AdS/CFT entanglement structure.
- [[Quantum Gravity]]: if exact, AdS/CFT provides a nonperturbative definition of particular quantum-gravity theories in AdS.
- [[Quantum Entanglement]]: entanglement entropy has a geometric dual.

## Sources

- Maldacena, J. (1998). "The large-$N$ limit of superconformal field theories and supergravity." *Adv. Theor. Math. Phys.* 2, 231. arXiv:hep-th/9711200.
- Witten, E. (1998). "Anti-de Sitter space and holography." *Adv. Theor. Math. Phys.* 2, 253. arXiv:hep-th/9802150.
- Gubser, S., Klebanov, I., Polyakov, A. (1998). "Gauge theory correlators from non-critical string theory." *Phys. Lett. B* 428, 105. arXiv:hep-th/9802109.
- Ryu, S., Takayanagi, T. (2006). "Holographic derivation of entanglement entropy from AdS/CFT." *Phys. Rev. Lett.* 96, 181602. arXiv:hep-th/0603001.
- Aharony, O., et al. (2000). "Large $N$ field theories, string theory and gravity." *Phys. Rept.* 323, 183. arXiv:hep-th/9905111. (Comprehensive review.)
- Natsuume, M. (2015). *AdS/CFT Duality User Guide.* Springer.

## Epistemic status

**Conjectural, with extensive theoretical support.** AdS/CFT has passed many nontrivial checks, including protected and integrable sectors, but no general proof or independent experimental test establishes the full equivalence. Its best-controlled examples concern anti-de Sitter boundary conditions rather than the approximately de Sitter cosmology of our universe.

## Navigation

[[Physics Worldmap]] · [[Relativity and Gravitation Map]] · [[Holographic Principle]] · [[Black Hole Information Problem]] · [[Quantum Error Correction and Gravity]] · [[Quantum Gravity]]
