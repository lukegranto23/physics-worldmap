# Conditioning on estimated velocities — manuscript draft

**Status:** first full draft, 8 October 2026. Not submitted or posted anywhere.

| File | What it is |
|---|---|
| `main.tex` | REVTeX 4.2 source (Physical Review E style). Compile with `pdflatex main.tex` twice. |
| `figures/` | Copies of the lab outputs the paper uses (labs 41/44, 45, 46, 47). |
| `preview.html` | A pandoc rendering for reading without LaTeX. The layout is approximate. |

## Before anyone posts this

1. **Wait for the data authors.** The paper is partly about their result. Give them time to reply to the 8 October email, and fold in any correction they offer.
2. **Verify the references.** Every citation was written from memory, apart from the Science Advances DOI, the Dryad DOI and the two arXiv numbers, which were confirmed by web search. Check volumes, pages and author lists against the originals. Read the two 2026 preprints (arXiv:2605.16252, 2605.16247) to find out how they estimate velocity, and adjust the velocity-roughness paragraph to match.
3. **Make sure you can defend every number.** Each one traces to a lab in `Physics Worldmap/62 Computational Labs` and to its write-up, Benchmarks 014–018 and the derivation notes.
4. **Keep the AI-assistance statement.** It is in the acknowledgements and reflects how the work was done.
5. **Plan for arXiv endorsement.** First-time submitters in physics usually need an endorser. Asking the data authors, or a physicist you know, is the normal route.
6. **Choose a venue later.** Options include a short paper (Phys. Rev. E, Am. J. Phys. for a pedagogical angle), a comment on the original article, or a preprint only. Decide once the authors have replied.

## Claims, and where they come from

| Claim | Source |
|---|---|
| Three-term decomposition, universal Φ, leak identity, design criterion | lab 46; `Derivation — Conditioning on an Estimated Velocity` |
| Calibration-free regression slope within 1.6%; Langevin rejected | lab 35, controls in lab 38; Benchmark 015 |
| Nine-variant processing test, Z 20.9 vs 4773 | lab 41, frozen before the data run; Benchmark 017 |
| Nonzero-speed sign change | lab 43; Benchmark 017 |
| Velocity-roughness pseudo-plateau | lab 47; Benchmark 018 |
| Noise not particle-independent; 100–400 kHz excess | lab 45; Benchmark 015 |
