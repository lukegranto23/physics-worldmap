# Conditioning on estimated velocities — manuscript draft

**Status: NOT READY.** An internal review on 8 October 2026 found major errors in the theory framing and in several numbers. See `REVIEW_STATUS.md`. Do not submit or post this draft as it stands.

| File | What it is |
|---|---|
| `main.tex` | REVTeX 4.2 source (Physical Review E style). Compile with `pdflatex main.tex` twice. |
| `main.pdf` | The compiled paper. |
| `figures/` | Copies of the lab outputs the paper uses (labs 41/44, 45, 46, 47). |
| `preview.html` | A pandoc rendering for reading without LaTeX. The layout is approximate. |

## Ready to use

`main.tex` compiles cleanly with `pdflatex` (run it twice). `main.pdf` is that output: 4 pages, 4 figures. The only message is a harmless REVTeX float-deferral warning; every figure is placed. The author line, date (`\today`), acknowledgements and AI-assistance statement are filled in. No edits are needed before reading or sharing.

**References.** These were checked against web sources on 8 October 2026: Hinch; Hauge and Martin-Löf; Clercx and Schram; Huang et al. (DOI); Franosch et al.; Kheifets et al. (DOI); Boynewicz et al. (DOI); Dryad (DOI); arXiv:2605.16247 (authors from a mirror listing). For arXiv:2605.16252 the authors could not be confirmed from this environment, so it is cited by title and arXiv number, which is an accepted format.

## Judgement calls, not edits

1. **When to post.** It is courteous to wait for the data authors' reply to the 8 October email.
2. **What the two preprints say.** Their full texts could not be read here. The manuscript already says so and claims nothing about their methods. If you read them and they treat the estimator question, add a sentence citing that.
3. **arXiv endorsement.** First-time physics submitters usually need an endorser.
4. **Venue.** Options include Phys. Rev. E, a comment on the original article, Am. J. Phys., or a preprint only.

## Claims, and where they come from

| Claim | Source |
|---|---|
| Three-term decomposition, universal Φ, leak identity, design criterion | lab 46; `Derivation — Conditioning on an Estimated Velocity` |
| Calibration-free regression slope within 1.6%; Langevin rejected | lab 35, controls in lab 38; Benchmark 015 |
| Nine-variant processing test, Z 20.9 vs 4773 | lab 41, frozen before the data run; Benchmark 017 |
| Nonzero-speed sign change | lab 43; Benchmark 017 |
| Velocity-roughness pseudo-plateau | lab 47; Benchmark 018 |
| Noise not particle-independent; 100–400 kHz excess | lab 45; Benchmark 015 |
