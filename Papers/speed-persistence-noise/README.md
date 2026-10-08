# Localization error and the speed–persistence coupling — manuscript draft

**Status: NOT READY.** An internal review on 8 October 2026 found major problems, including that the zebrafish headline is wrong. See `REVIEW_STATUS.md`. Do not submit or post this draft as it stands.

| File | What it is |
|---|---|
| `main.tex` | REVTeX 4.2 source (Physical Review E style). Compile with `pdflatex main.tex` twice. |
| `main.pdf` | The compiled paper: 5 pages, 2 figures, 2 tables. |
| `figures/` | Copies of lab outputs: `noise_made_coupling.png` (lab 48) and `sensitivity_curves.png` (lab 52, using labs 49–51). |
| `preview.html` | A pandoc rendering for reading without LaTeX. The layout is approximate. |

## Ready to use

`main.tex` compiles cleanly. The only message is REVTeX's harmless "deferred float" warning; every float is placed. The author line, date, acknowledgements and AI-assistance statement are filled in. No edits are needed before reading or sharing.

**References.** All ten were checked against Crossref or Zenodo metadata on 8 October 2026: Maiuri et al. (Cell 2015), Jerison and Quake (eLife 2020), Ganusov, Zenkov and Majumder (Phys. Biol. 2023, 025001), Michalet (PRE 2010), Berglund (PRE 2010), Wortel et al. (ImmunoInformatics 2021), Fazeli et al. (F1000Research 2020), Gómez-de-Mariscal et al. (PLoS Biol. 2024), and Zenodo 4034929 and 8420011.

## Judgement calls, not edits

1. **Full texts not read.** The full texts of Maiuri et al. and Ganusov et al. could not be read here, so the paper describes them only at the level of their abstracts. Before submitting, check that no earlier paper already models localization error in speed–persistence analyses. A limited search found none, which is why the paper says "we work out" rather than claiming priority.
2. **Two corrections are built in.** Section V reports, on purpose, that an upper bound I first computed was invalid (selection bias). Section VI reports that the frozen MSD-intercept calibration over-corrected and was excluded by a consistency bound. The lab history keeps every version (lab 51 amendment, labs 53 and 54).
3. **Venue.** Options include Phys. Biol., PRE, Biophys. J. (as a short communication), or a bioRxiv preprint.
4. **Courtesy, in vitro.** The in vitro data come from the Jacquemet lab (Åbo Akademi / Turku). A short note to them before posting would be polite but is not required: the data are CC-BY.
5. **Courtesy, zebrafish.** Section VI largely *supports* Jerison and Quake's coupling against a noise artefact. A short note to them after posting would be natural.

## Claims, and where they come from

| Claim | Source |
|---|---|
| Closed form for ρ and E[cos θ]; MC agreement within 1–2% | lab 48 |
| Protocol, self-tests, non-identifiability of σ | lab 49 (frozen `c795361`, four pre-data amendments); Benchmark 019 |
| In vivo results (T cells, B cells, neutrophils) | lab 49; Benchmark 019 |
| In vitro results, frozen verdict NOT ROBUST | lab 50 (frozen `849616a`); Benchmark 020 |
| Lower bound σ ≳ 0.2 µm, invalid upper bound, split-half bound | lab 51 (post hoc, amended); Benchmark 020 |
| Figure 2 | lab 52 |
| Zebrafish frozen test; MSD calibration over-corrects | lab 53 (frozen `4028d77`); Benchmark 021 |
| Cauchy–Schwarz split bound, synthetic validation, fish f_noise ≤ 13–23% | lab 54 (post hoc); Benchmark 021 |
