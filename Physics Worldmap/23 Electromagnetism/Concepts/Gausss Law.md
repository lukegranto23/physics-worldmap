---
type: "concept"
field: "Electromagnetism"
epistemic_status: "established"
level: "introductory"
tags: ["physics", "field/electromagnetism", "status/established", "level/introductory"]
aliases: ["Gauss's Law"]
created: 2026-07-30
updated: 2026-09-17
note_maturity: expanded
source_audit: derived-with-canonical-references-and-targeted-checks
---

# Gauss's Law

Gauss's law connects the electric field's outward flux to total enclosed charge. It is always a flux constraint within classical Maxwell theory; it becomes an easy field-solving method only when symmetry and boundary conditions provide the missing spatial information.

## 1. Integral and local statements

For a closed surface $S=\partial V$, oriented outward,

$$
\oint_S\mathbf E\cdot d\mathbf A
=\frac{Q_V}{\epsilon_0},\qquad
Q_V=\int_V\rho\,d^3x.
$$

SI electric flux has units V m, equivalently N m$^2$ C$^{-1}$. The charge on the right is total charge, including bound charge if matter is resolved in the $\mathbf E$ description. The equation is not limited to electrostatics.

For regular fields the divergence theorem gives

$$
\int_V\left(\nabla\cdot\mathbf E-\rho/\epsilon_0\right)d^3x=0.
$$

If this holds for every volume, the integrand vanishes locally. Thus $\nabla\cdot\mathbf E=\rho/\epsilon_0$. For ideal point or surface charges this statement uses distributions, not ordinary derivatives at the singularity.

## 2. Electrostatic origin and an important non-implication

For a point charge $q$, Coulomb's field has signed radial component $q/(4\pi\epsilon_0r^2)$ on a centered sphere. Multiplication by $4\pi r^2$ gives flux $q/\epsilon_0$, independent of radius. Superposition and the solid-angle flux through a general closed surface yield the enclosed-charge rule. This reconstructs the electrostatic result; extending it to time-dependent fields is part of the full Maxwell framework, not a derivation from static Coulomb forces alone.

Specifying divergence does not determine a vector field. Adding any divergence-free field leaves the local Gauss constraint unchanged. In electrostatics one also uses $\nabla\times\mathbf E=0$, suitable domain assumptions, and boundary data. An external uniform electric field has zero net flux through a sphere but is not zero on that sphere.

Consequently, $Q_V=0$ means zero **net flux**, not zero field. External charges contribute to the field on the surface while their total flux contribution cancels. A spherical mathematical surface does not confer spherical symmetry on an arbitrary charge distribution. The symmetry-dependent calculation method is treated in [OpenStax, §6.3](https://openstax.org/books/university-physics-volume-2/pages/6-3-applying-gausss-law).

## 3. Worked example: volume charge, not a conductor

Take a fixed, uniformly charged insulating ball, radius $R=0.100$ m and total charge $Q=5.00$ nC, surrounded by vacuum. This is a specified total-charge distribution; ignore any additional material polarization. Its density is

$$
\rho_0=\frac{3Q}{4\pi R^3}\simeq1.19\times10^{-6}\ \mathrm{C\,m^{-3}}.
$$

Rotational symmetry of the complete isolated configuration requires $\mathbf E=E_r(r)\hat{\mathbf r}$. A concentric Gaussian sphere gives $4\pi r^2E_r=Q_{\rm enc}(r)/\epsilon_0$, where

$$
Q_{\rm enc}(r)=
\begin{cases}Q(r/R)^3,&r<R,\\Q,&r\ge R.\end{cases}
$$

Writing $k_e=1/(4\pi\epsilon_0)$,

$$
E_r(r)=
\begin{cases} k_eQr/R^3,&r<R,\\k_eQ/r^2,&r\ge R.\end{cases}
$$

Hence $E_r(0.050\,\mathrm m)\simeq2.25\times10^3$ V m$^{-1}$ and $E_r(0.200\,\mathrm m)\simeq1.12\times10^3$ V m$^{-1}$, both outward. At $r=R/2$, only $Q/8$ is enclosed. Substituting the entire charge there would overestimate the field by eightfold.

Independent checks:

- At the center, $E_r\to0$ linearly, consistent with symmetry and finite density.
- At the boundary the inside and outside fields agree; there is no delta-function surface charge in this specified model.
- Inside, $r^{-2}d(r^2E_r)/dr=3k_eQ/R^3=\rho_0/\epsilon_0$.
- Outside, that divergence is zero although the field is nonzero.

This example belongs to the same standard symmetry class as the canonical sphere calculation, with locally chosen numerical values. It is **not** the field of a charged conducting ball in electrostatic equilibrium: in that case the conductor's interior field is zero and excess charge resides on its surface.

## 4. Interface conditions and material bookkeeping

Apply the flux law to a thin pillbox crossing a surface with total charge per area $\sigma_{\rm tot}$. Let $\hat{\mathbf n}$ point from side 1 to side 2. As thickness tends to zero, the side flux vanishes when the fields remain bounded away from the surface, leaving

$$
\hat{\mathbf n}\cdot(\mathbf E_2-\mathbf E_1)=\sigma_{\rm tot}/\epsilon_0.
$$

There is no general demand that the normal electric field be continuous. For macroscopic dielectric notation, $\mathbf D=\epsilon_0\mathbf E+\mathbf P$ and $\rho_{\rm bound}=-\nabla\cdot\mathbf P$ imply

$$
\nabla\cdot\mathbf D=\rho_{\rm free},\qquad
\hat{\mathbf n}\cdot(\mathbf D_2-\mathbf D_1)=\sigma_{\rm free}.
$$

Replacing $\epsilon_0$ by a material $\epsilon$ in every vacuum formula without tracking free/bound charge is unsafe. Even when $D_n$ is continuous, $E_n$ can jump if the permittivities differ. The tangential electric condition follows from Faraday's law, not Gauss's law.

## 5. Recall and source scope

Explain why a neutral cavity may contain a nonzero electric field. Then derive the field of a density $\rho(r)=ar^2$ inside a ball: the result scales as $r^3$, not $r$. Check which assumptions would fail if nearby electrodes break rotational symmetry.

Canonical sources: [OpenStax §6.3](https://openstax.org/books/university-physics-volume-2/pages/6-3-applying-gausss-law), symmetry and enclosed-charge construction; [Feynman Lectures II, Chapter 10](https://www.feynmanlectures.caltech.edu/II_10.html), bound/free charge and dielectric fields. Derivations and numerical examples here are explanatory reconstructions, not copied exercise solutions. The study route and numerical checks are targeted, not a complete source or experimental audit.

[[Electromagnetism — Fields Energy and Gauge Study Route]] · [[Physics Worldmap]] · [[Electromagnetism Map]] · [[Electric Potential|← previous]] · [[Poisson and Laplace Equations|next →]] · [[Maxwell Equations]]
