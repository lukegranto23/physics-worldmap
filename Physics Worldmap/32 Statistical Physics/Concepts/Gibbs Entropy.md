---
type: "concept"
field: "Statistical Physics"
epistemic_status: "established"
level: "intermediate"
tags: ["physics", "field/statistical", "status/established", "level/intermediate"]
aliases: []
created: 2026-07-30
updated: 2026-09-04
note_maturity: expanded
source_audit: bibliography-present-needs-claim-audit
---

# Gibbs Entropy

> [!summary] Core idea
> Gibbs entropy is a functional of probabilities over a specified set of microstates. Its value depends on what distinctions the description retains; it is not interchangeable with every other use of “entropy.”

## Definition and elementary checks

For normalized discrete probabilities,
$$
S_G=-k_B\sum_i p_i\ln p_i,\qquad 0\ln0:=0.
$$
Natural logarithms give units J K$^{-1}$ after multiplying by $k_B$. For $M$ possible states, $0\le S_G\le k_B\ln M$, with the upper bound at uniform probabilities.

For independent systems, $p_{ij}=p_iq_j$ and the logarithm factorizes, giving $S(A,B)=S(A)+S(B)$. For correlated classical systems,
$$
S(A)+S(B)-S(A,B)=k_B I(A:B)\ge0.
$$
The independence assumption is what licenses additivity.

## Derive the canonical distribution

Maximize $S_G/k_B$ subject to $\sum_i p_i=1$ and $\sum_i p_iE_i=U$:
$$
\delta\left[-\sum_i p_i\ln p_i-\alpha(\sum_i p_i-1)
-\beta(\sum_i p_iE_i-U)\right]=0.
$$
Then $p_i=e^{-\beta E_i}/Z$, with $Z=\sum_i e^{-\beta E_i}$, and
$$
S_G=k_B(\ln Z+\beta U).
$$
The multiplier has units inverse energy; equilibrium thermodynamics identifies $\beta=1/(k_BT)$. This is an equilibrium inference or variational characterization, not a dynamical proof that an isolated initial state reaches equilibrium.

## Worked coarse-graining example

Take four equally weighted reference cells with probabilities $(0.4,0.1,0.2,0.3)$. Forget distinctions within cells 1–2 and 3–4, then reconstruct a uniform distribution inside each pair. The resulting four-cell vector is $(0.25,0.25,0.25,0.25)$.

The fine entropy is $1.279854\,k_B$; reconstructed entropy is $\ln4\,k_B=1.386294\,k_B$. The increase is $0.106440\,k_B$.

But the two pair-label probabilities are $(0.5,0.5)$ and their entropy is only $\ln2\,k_B$. This is not a contradiction: entropy of the coarse label and entropy of the reconstructed microstate distribution are different quantities. A numerical test checks all three.

## Relative entropy and equilibrium free energy

For an arbitrary distribution $p$ and the Gibbs distribution $\pi$ at a fixed Hamiltonian and positive temperature,
$$
\mathcal F[p]=\sum_i p_iE_i-TS_G[p],\qquad
\mathcal F[p]-F_{\rm eq}=k_BT D_{\rm KL}(p\|\pi)\ge0.
$$
This identity compares states, not rates. Monotonic relaxation of this free energy requires specified dynamics, such as an appropriate thermal Markov process—not merely the identity.

## Continuous and quantum cautions

For phase-space densities, write entropy relative to a declared dimensionless reference measure $d\mu$, with $\int\rho\,d\mu=1$. Taking the logarithm of a dimensionful density without a reference silently changes entropy under unit changes. Classical absolute entropy also involves phase-space-cell and indistinguishability conventions.

Quantum von Neumann entropy is $-k_B\operatorname{Tr}\rho\ln\rho$. Global unitary evolution preserves its spectrum and entropy; a subsystem's entropy may change. This parallels, but is not identical to, fine-grained classical entropy conservation in [[Liouvilles Theorem]].

## Sources, limitations, and recall

[Tong, Statistical Physics §1.3](https://davidtong.org/teaching/statistical-physics/statmechhtml/S1) provides canonical weights and equilibrium entropy relations. The coarse-graining and relative-entropy calculations are explicitly reconstructed here and tested locally. Full claim-level source coverage remains pending.

Explain why maximum entropy is not a thermalization theorem. Compute entropy before and after forgetting a label, stating which probability space is being used.

## Navigation

[[Statistical Physics Map]] · [[Boltzmann Entropy]] · [[Ensembles]] · [[Partition Functions]] · [[Liouvilles Theorem]] · [[Information Theory]] · [[Mechanics to Statistical Physics — Foundation Study Route]] · [[Physics Worldmap]]
