---
type: research-communication-draft
field: Statistical Physics
epistemic_status: effective
level: advanced
tags: [brownian-motion, hydrodynamic-memory, reanalysis, communication, draft]
created: 2026-10-08
updated: 2026-10-08
note_maturity: draft
source_audit: digest-verified-public-data-and-notebooks-read-as-text
---

# Draft Technical Note — Processing Dependence for the Data Authors

> [!warning] Errors in the sent note (found by internal review, 2026-10-08)
> 1. **"Within 1.6%" should be about 2.1%.** The worst lag is 136 µs, and the formal consistency test rejected the model.
> 2. **"Noise supplies 9–71% of the measured value" is mislabelled.** Those are shares of the forward prediction, and they assume the particle-run noise equals the empty trap's.
> 3. **The "nearly cancelling" framing missed the point.** Both effects are t² terms whose sum vanishes when the measured Var W = kT/m, which the authors reported (98%).
> 4. **The note missed that the paper already flags the first point** as set by finite differencing and laser noise.
> 5. **"Frozen before each confirmatory statistic" overstates it.** The freezes were self-recorded commits, and the hypotheses were formed after the data were analysed.
>
> A short correction email was drafted for the owner's approval.


> [!note] Sent 2026-10-08
> An email version of this note was sent by the vault owner to the paper's corresponding author on 2026-10-08. It was shorter and in the first person. It disclosed AI assistance with the analysis and code, and linked this public repository. No reply had been received when this note was updated. Record any reply here, and keep the analysis notes unchanged until the authors' points have been checked.

**To:** the authors of "Observation of super-ballistic Brownian dynamics in liquid", *Sci. Adv.* (2026), doi:10.1126/sciadv.aeb4579.

**Subject:** A reanalysis of your Dryad data (doi:10.5061/dryad.pvmcvdnz4): measurement-operator effects on the conditioned MSD.

---

Thank you for depositing the processed traces and notebooks. They made a fully reproducible reanalysis possible. We are writing to share three findings and ask whether they match your understanding.

**1. Hydrodynamic memory is confirmed without the volts-to-metres calibration.**
- The regression slope $R_k=\operatorname{Cov}(D_k,W)/\operatorname{Var}W$ is in seconds and independent of the gain. We subtract the empty-trap moments.
- Your fitted Basset parameters predict it within 1.6% from 0.75 to 192 µs, with no free parameters, once the 750 ns bin average and eighth-order stencil are modelled.
- A memoryless Langevin model is decisively rejected.
- Equipartition through the same operator reproduces your fitted gain to 0.7–1.6%.

**2. The conditioned MSD depends strongly on the velocity estimator.** Through the bin-and-stencil operator, your fitted Basset model predicts two effects at 0.75–12 µs:
- the zero-velocity conditioned MSD falls to 0.26–0.87 of the continuum expression $2k_BT\int_0^t\chi-k_BTm\chi^2$;
- the empty-trap noise supplies 9–71% of the measured value.

We then recomputed $W$ from your supplied positions in nine ways: central stencils of order 2, 4 and 8, on positions coarsened by 1, 2 and 4 bins.
- The conditioned MSD changed by factors down to 0.25, as the forward model predicts: median deviation 2.4%, $Z=20.9$ over 32 cells.
- A processing-independent reading gives $Z=4773$.
- Over 3–12 µs, the apparent log-log exponent ranges from 2.29 to 2.96 depending only on processing.

Our reading: your Basset analysis is right, but the plotted conditioned curve is a processing-dependent statistic. Its agreement with the continuum curve at your settings reflects operator suppression and detector noise nearly cancelling. Did your analysis account for this in a way we missed?

**3. An unexplained 1–2% residual at 2–12 µs.** At the observable's 0.04–0.4% precision, the gain-free slope shows a structured deviation of up to about 1.6% at 2–12 µs. None of the following removes it:
- a free memory exponent;
- detector low-pass filtering;
- single- or two-component rescaling of the empty-trap noise;
- per-trace fits. It is present in every trace, with heterogeneous per-trace parameters.

We cannot test the Tikhonov high-pass inversion, trace timing or detector linearity from the processed files. We would value your view, or the raw records if they can be shared.

**Reproducibility.**
- All seven Dryad files were checked against their published SHA-256 digests. Notebooks were read as text, not executed.
- Protocols were frozen before each confirmatory statistic, with synthetic positive and negative controls. Every amendment is dated.
- Code: labs 34–42 in the vault's `62 Computational Labs`. Results are in its `results/` folders. No third-party data are redistributed.

---

Supporting notes: [[Benchmark 015 — Gain-Free Test of Hydrodynamic Memory]] · [[Benchmark 017 — Processing Dependence of the Conditioned Super-Ballistic Signal]] · [[Benchmark 016 — Stratified Conditioning and an Estimator Artifact]] · [[Derivation — Equilibrium Conditioning of a Hydrodynamic Brownian Particle]]
