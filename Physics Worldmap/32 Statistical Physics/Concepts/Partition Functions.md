---
type: "concept"
field: "Statistical Physics"
epistemic_status: "established"
level: "introductory"
tags: ["physics", "field/statistical", "status/established", "level/introductory"]
aliases: []
created: 2026-07-30
updated: 2026-09-04
note_maturity: expanded
source_audit: bibliography-present-needs-claim-audit
---

# Partition Functions

> [!summary] Core idea
> The partition function normalizes equilibrium probabilities. Its logarithmic derivatives generate equilibrium means and fluctuations—but only when the ensemble, held-fixed variables, and Hamiltonian dependence are specified.

## Canonical setting

For a system weakly coupled to a large equilibrium heat bath, at fixed volume, particle number, and external control parameters,
$$
Z(\beta)=\sum_n g_n e^{-\beta E_n}
=\operatorname{Tr}e^{-\beta H},\qquad \beta=(k_BT)^{-1}.
$$
Here $g_n$ counts degeneracy if $n$ labels distinct energies; do not multiply by degeneracy again when summing individual states. The trace must converge. At strong system–bath coupling, the bare-system Gibbs state generally needs correction.

## Derivative identities

For a temperature-independent Hamiltonian,
$$
U=-\partial_\beta\ln Z,\qquad
\partial_\beta^2\ln Z=\langle H^2\rangle-\langle H\rangle^2,
$$
$$
F=-k_BT\ln Z,\qquad
S=k_B(\ln Z+\beta U),\qquad
C_V=\frac{\operatorname{Var}(H)}{k_BT^2}.
$$
The last identity follows from $d\beta/dT=-1/(k_BT^2)$. Its nonnegative right side is a canonical-ensemble statement, not a proof that negative heat capacities cannot occur in other ensembles or nonadditive systems.

For an external parameter $\lambda$, $\partial_\lambda F=\langle\partial_\lambda H\rangle$ in the Gibbs ensemble under regularity conditions. For noncommuting quantum operators, higher-response derivatives are not in general ordinary equal-time covariances.

## Worked example: a two-level unit

Let energies be $0$ and $\Delta$, each nondegenerate:
$$
Z=1+e^{-x},\quad p_{\rm exc}=\frac{1}{1+e^x},\quad
U=\Delta p_{\rm exc},\quad
\frac{C_V}{k_B}=x^2p_{\rm exc}(1-p_{\rm exc}),\quad
x=\frac{\Delta}{k_BT}.
$$
Choose $\Delta/k_B=120$ K and $T=60$ K. Then $x=2$,
$p_{\rm exc}=0.119203$, $U/k_B=14.30435$ K,
$S/k_B=0.365334$, and $C_V/k_B=0.419974$.

As $T\to0^+$, the unique ground state gives $S\to0$ and activated heat capacity. As $T\to\infty$, both states become equally likely, $S\to k_B\ln2$, and $C_V\to0$. High entropy does not require high heat capacity.

## Change the energy zero without changing physics

Replacing $E_n$ by $E_n+c$ gives
$$
Z'=e^{-\beta c}Z,\quad U'=U+c,\quad F'=F+c,
$$
while probabilities, entropy, and heat capacity remain unchanged when $c$ is independent of temperature and controls. This is a useful code test.

## Classical measure and particle exchange

For $N$ identical dilute classical particles in three dimensions, one common semiclassical convention is
$$
Z_N=\frac{1}{N!h^{3N}}\int d^{3N}q\,d^{3N}p\,e^{-\beta H}.
$$
The state-counting measure makes $Z$ dimensionless; $N!$ handles indistinguishability in this regime. Quantum degeneracy requires Bose/Fermi state counting rather than treating this as an exact quantum formula.

When particle number fluctuates, use the grand partition function $\Xi=\operatorname{Tr}e^{-\beta(H-\mu N)}$ and its own held-fixed-variable rules. Do not mix canonical and grand-canonical derivatives.

## Sources and recall

[Tong, Statistical Physics §1.3.1–1.3.3](https://davidtong.org/teaching/statistical-physics/statmechhtml/S1) checks the canonical identities; [§2, Classical Gases](https://davidtong.org/teaching/statistical-physics/) directs further reading on the measure. The numerical example and energy-zero invariance are tested in [[Mechanics to Statistical Physics — Foundation Study Route]].

Derive the variance identity, identify all held-fixed controls in $C_V$, and explain why differentiating a temperature-dependent effective Hamiltonian needs extra terms.

## Navigation

[[Canonical Ensemble]] · [[Grand Canonical Ensemble]] · [[Gibbs Entropy]] · [[Classical Ideal Gas Statistics]] · [[Statistical Physics Map]] · [[Physics Worldmap]]
