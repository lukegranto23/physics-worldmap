# Internal review, 8 October 2026: NOT READY FOR SUBMISSION

An adversarial referee pass (an independent AI agent told to find errors) recommended **major revision**. I verified the central points myself against the code and the results files.

**Verified errors**
1. **The theory framing is wrong at its core.** Beyond the stencil reach, the "universal operator distortion" of the cusp term is a pure **t² term**: 1 − Φ_α/continuum = 0.7577 k^(−1/2) exactly, for order 8 and α = ½. That is the same form as the noise leak. The two combine to r²(1/c − 1/S), where c = kT/m and S is the measured Var W. They therefore cancel when the measured velocity variance equals kT/m, which the data authors checked and reported (98% of the theoretical SD). The k_min "design criterion" and the "no clean window" conclusion are withdrawn.
2. **The leak identity is misapplied.** It is exact only beyond the stencil reach (k > 4 for order 8) and for white noise. Its "machine-precision" check was circular. At k = 1 the leak/cusp ratio is −0.42, not +1.8.
3. **"Within 1.6% from 0.75 to 192 µs" is false.** The deviation reaches −2.14% at 135.75 µs. The pre-committed consistency test *rejected* the published model (χ² = 3906 on 16 dof), and the abstract omits this.
4. **"71/51/27/16/9% of the measured value" is mislabelled.** These are shares of the *forward prediction*. As shares of the measured value they are 88/51/25/16/9%.
5. **Smaller numbers.** Φ(16) = 0.81, not 0.82. The first-order theory differs from full Basset by 8% at 3 µs, not "1–5%".

**Significant (reviewer findings, not all re-verified)**
- **Straw-man risk.** The nine-variant test refutes a processing-invariance hypothesis that the authors never stated. The extreme ratios (0.25) and exponents (~2.9) occur when the coarse bins are as long as the lag. At the published processing the exponent is 2.29, against 2.32 for the continuum theory. The authors' paper already attributes the first point to finite differencing and laser noise.
- **Hidden misfit.** The forward model itself misses the published curve by −20% at 0.75 µs and +8.6% at 3 µs. The ratio construction hides this.
- **"Preregistered" is overstated.** The freezes are same-day commits to a personal repository. The hypotheses were formed after the data had already been analysed, and there was a partial unblinding.
- **Thin literature review.** Regression dilution, motion blur and the dependence of measured velocity variance on time resolution are established topics.
- **Velocity-roughness section.** The two preprints were not read; this section should be dropped or made conditional.

**What survives:** the Gaussian-conditioning algebra, the exact cancellation of the ballistic part, the continuum limit, and the nine-variant ratios, which reproduce exactly. The gain-free slope agrees with the published Basset model to about 2%, with an unexplained 1–2% residual.

**Recommendation:** do not submit. The note already emailed to the data author needs a short correction (drafted 8 October, not sent without the owner's approval).
