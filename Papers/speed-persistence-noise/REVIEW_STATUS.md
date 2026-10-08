# Internal review, 8 October 2026: NOT READY FOR SUBMISSION

An adversarial referee pass (an independent AI agent instructed to find errors) recommended **major revision, bordering on reject**. I checked its central claims against the data and code, and they hold.

**Fatal or major**
1. **The zebrafish headline is wrong.** The 12 s calibration comes from a single 2019 movie. The 45 s control set is 16 fish from 2018, and the rockout set is 6 of those same fish. The rockout movies' own split-half lower bound, σ ≥ 0.46–0.50 µm, exceeds the transferred 0.40 µm upper bound. The control's own upper bound (1.22 µm) was omitted. Revised: noise explains roughly 20–40% of the control coupling, not "at most 13%".
2. **Biased attribution.** Terciles were re-formed on the cells surviving the drop rule. Lab 55 fixes this and every number needs regenerating. The changes include σ½ ≈ 0.41 µm (ICAM-1), 0.30 µm (VCAM-1) and 0.30 µm (B cells).
3. **The 12 s and 48 s attributions are mutually inconsistent** under the OU model. The 12 s lag-1 statistic is dominated by non-OU structure.
4. **r\* is unbiased only as a ratio of expectations.** The words "exact" and "whatever the speed or persistence" must go.

**Significant**
- Novelty is overstated. The mechanism, independent position errors anticorrelating consecutive steps, is established in Hurford (PLoS ONE 2009, GPS turning angles) and Loosley et al. (PLoS ONE 2015, cell turning angles). OU-walk statistics with positional error are in Pedersen et al. (PRE 94, 062401, 2016), and the covariance-based σ estimator is in Vestergaard, Blainey and Flyvbjerg (PRE 2014). Ganusov et al. already flagged the noise trade-off. *(These were found by the reviewer through searches, mostly from abstracts, and have not yet been verified by me in full text.)*
- Motion blur and temporally correlated error are ignored. The "fast genuine motion" interpretation is unproven.
- The lower bound assumes slow objects are not confined (C₁ ≥ 0).
- Other gaps: frozen-run groups not all reported (mouse T, all of Dicty), the pre-specified pooled-lag σ estimates not reported, the cell bootstrap ignores movie-level clustering, and "preregistration" means same-day commits to a personal repository.

**What survives:** the closed form (verified to within 0.001 by the reviewer's Monte Carlo), the observation that the MSD-intercept calibration over-corrects on cells, and a careful negative message: the speed–persistence coupling in these datasets cannot be separated from localization error without an independent calibration.

**Recommendation:** do not submit this draft. If it is revived, reposition it as a quantitative test of a known artefact, fix the estimator, report all groups, model blur, and cite the prior work above.
