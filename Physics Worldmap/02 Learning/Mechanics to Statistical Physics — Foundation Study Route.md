---
type: learning
field: Physics
epistemic_status: reference
level: intermediate
tags: [physics, learning, mechanics, statistical-physics, verification]
created: 2026-09-04
updated: 2026-09-04
---

# Mechanics to Statistical Physics — Foundation Study Route

This route develops one important chain: equations of motion → conserved quantities → transport of probability → equilibrium descriptions. The final arrow is not automatic. Hamiltonian mechanics alone does not prove thermalization or monotonic thermodynamic entropy growth.

## Read, reconstruct, test

| Step | Note | Reconstruct without notes | Boundary to remember |
|---|---|---|---|
| 1 | [[Lagrangian Mechanics]] | Integrate the first variation by parts | Stationary action can be a saddle |
| 2 | [[Noethers Theorem in Mechanics]] | Derive the charge including its boundary term | A symmetry of one orbit is not a variational symmetry |
| 3 | [[Hamiltonian Mechanics]] | Perform the Legendre transformation | Singular Lagrangians require constraint analysis |
| 4 | [[Liouvilles Theorem]] | Derive zero divergence and density transport | Energy conservation is not required |
| 5 | [[Gibbs Entropy]] | Derive canonical weights and the coarse-cell example | Fine entropy, coarse-label entropy, and reconstructed entropy differ |
| 6 | [[Partition Functions]] | Differentiate log Z and track held-fixed controls | A temperature-dependent effective Hamiltonian needs extra terms |

Source references are attached to the individual notes. The examples below and the accompanying calculation checks are local reconstructions, not copied textbook exercises. Targeted checks do not constitute an exhaustive claim-level source audit.

## Six held-out exercises

Try each before opening its check. Then compare the derivation, not only the final number.

### 1. Coordinate and parameter discipline

A pendulum has length 1.20 m and mass 0.35 kg. Derive the exact angular equation and its small-amplitude period, using $g=9.81$ m s$^{-2}$. At amplitude 0.20 rad, estimate the leading relative period correction.

<details>
<summary>Check</summary>

$\ddot\theta+(g/\ell)\sin\theta=0$, $T_0=2\pi\sqrt{\ell/g}\approx2.198$ s. The mass cancels. The leading correction is $\theta_0^2/16=0.0025$, or 0.25%. This estimate excludes damping and higher amplitude corrections.

</details>

### 2. Momentum balance under an external force

A free particle is subjected to a constant force $f$. Use $L=m\dot q^2/2+fq$. For a spatial translation, derive the momentum balance and find a conserved explicitly time-dependent combination.

<details>
<summary>Check</summary>

$\dot p=f$, so $p-ft$ is conserved. At fixed time, $\delta L/\epsilon=f=d(ft)/dt$, giving a Noether boundary term $B=ft$ and charge $p-ft$. Ordinary momentum is not conserved.

</details>

### 3. A total derivative changes representation

Add $d(aq^2/2)/dt=aq\dot q$ to $L_0=m\dot q^2/2-kq^2/2$, with constant $a$. Find the new canonical momentum and Hamiltonian, and show that the physical acceleration is unchanged.

<details>
<summary>Check</summary>

$p=m\dot q+aq$ and $H=(p-aq)^2/(2m)+kq^2/2$. Hamilton's equations imply $m\ddot q=-kq$. The canonical momentum shifts while the mechanical velocity does not.

</details>

### 4. Volume versus energy

For $H(q,p,t)=p^2/(2m)+k(t)q^2/2$, calculate $dH/dt$ and phase-space divergence. Can one vanish while the other does not?

<details>
<summary>Check</summary>

$dH/dt=\dot k(t)q^2/2$, while $\partial_q\dot q+\partial_p\dot p=0$. An external stiffness protocol can perform work without violating Liouville's theorem.

</details>

### 5. Degeneracy changes state counting

A unit has one ground state of energy 0 and three excited states of energy $\Delta$. Find its partition function, total excited probability, and high-temperature entropy.

<details>
<summary>Check</summary>

$Z=1+3e^{-\beta\Delta}$, $P_{\rm exc}=3e^{-\beta\Delta}/Z$, and $S\to k_B\ln4$ as $T\to\infty$. Each excited microstate has probability $e^{-\beta\Delta}/Z$; do not confuse that with their summed probability.

</details>

### 6. A correlation invisible in the marginals

Two classical bits have joint probabilities $p_{00}=p_{11}=1/2$ and $p_{01}=p_{10}=0$. Find their marginal entropies, joint entropy, and mutual information. What changes if you replace the joint state by the product of its marginals?

<details>
<summary>Check</summary>

$S(A)=S(B)=k_B\ln2$, $S(A,B)=k_B\ln2$, and $I(A:B)=\ln2$ nats. The product distribution gives probability $1/4$ to all four states, joint entropy $2k_B\ln2$, and zero mutual information. Discarding correlations changes the model even while all single-bit probabilities stay fixed.

</details>

## Reproducible checks

From the vault folder in PowerShell:

~~~powershell
python ".\95 Resources\Tools\check_foundations.py"
~~~

The program [[check_foundations.py]] needs NumPy and writes [[foundation-checks.json]]. It checks eight groups of calculations:

1. Action variation with both positive and negative directions.
2. Oscillator Legendre transformation and exact-energy trajectory.
3. Galilean boost boundary term and broken rotational-symmetry torque.
4. Symplectic versus explicit Euler phase-volume behavior.
5. Partition derivatives, heat capacity, and energy-zero invariance.
6. Fine, coarse-label, and reconstructed probability entropies.
7. Free-energy excess as relative entropy.
8. Global quantum entropy under a finite unitary transformation.

All eight passed on September 4, 2026. They are finite example checks, not proofs of the general theorems, tests of the six held-out exercises above, or evidence for new physics.

## The useful synthesis question

Suppose a reduced model matches equilibrium probabilities. Does it also predict how those probabilities and observables respond to a controlled perturbation?

The notes explain why this is nontrivial: static state counting does not specify dynamical closure, and discarding correlations can change response while preserving some marginal statistics. This motivates [[Synthesis Session 001 — Response-Preserving Coarse-Graining]], but does not prove its candidate criterion or claim novelty.

That concrete step is now implemented in [[Benchmark 001 — Equilibrium Versus Forced Response]]: a small coupled-oscillator comparison with exact response, frozen training/test settings, and competing reduced models. Read its results before predicting which observables a richer closure must preserve. The full multi-system research program remains unfinished.

## Navigation

[[Learning Paths]] · [[Physics Problem Bank]] · [[Release Status and Next Work]] · [[Synthesis Lab]] · [[Physics Worldmap]]
