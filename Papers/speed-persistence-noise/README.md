# Localization error and the speed–persistence coupling — manuscript draft

**Status:** complete draft, 8 October 2026. Not submitted or posted anywhere.

| File | What it is |
|---|---|
| `main.tex` | REVTeX 4.2 source (Physical Review E style). Compile with `pdflatex main.tex` twice. |
| `main.pdf` | The compiled paper: 4 pages, 2 figures, 1 table. |
| `figures/` | Copies of lab outputs: `noise_made_coupling.png` (lab 48) and `sensitivity_curves.png` (lab 52, using labs 49–51). |
| `preview.html` | A pandoc rendering for reading without LaTeX. The layout is approximate. |

## Ready to use

`main.tex` compiles cleanly. The only message is REVTeX's harmless "deferred float" warning; every float is placed. The author line, date, acknowledgements and AI-assistance statement are filled in. No edits are needed before reading or sharing.

**References.** All nine were checked against Crossref or Zenodo metadata on 8 October 2026: Maiuri et al. (Cell 2015), Ganusov, Zenkov and Majumder (Phys. Biol. 2023, 025001), Michalet (PRE 2010), Berglund (PRE 2010), Wortel et al. (ImmunoInformatics 2021), Fazeli et al. (F1000Research 2020), Gómez-de-Mariscal et al. (PLoS Biol. 2024), and Zenodo 4034929 and 8420011.

## Judgement calls, not edits

1. **Full texts not read.** The full texts of Maiuri et al. and Ganusov et al. could not be read here, so the paper describes them only at the level of their abstracts. Before submitting, check that no earlier paper already models localization error in speed–persistence analyses. A limited search found none, which is why the paper says "we work out" rather than claiming priority.
2. **A correction is built in.** Section V reports, on purpose, that an upper bound I first computed was invalid (selection bias). The lab history keeps both versions (lab 51 amendment).
3. **Venue.** Options include Phys. Biol., PRE, Biophys. J. (as a short communication), or a bioRxiv preprint.
4. **Courtesy.** The in vitro data come from the Jacquemet lab (Åbo Akademi / Turku). A short note to them before posting would be polite but is not required: the data are CC-BY.

## Claims, and where they come from

| Claim | Source |
|---|---|
| Closed form for ρ and E[cos θ]; MC agreement within 1–2% | lab 48 |
| Protocol, self-tests, non-identifiability of σ | lab 49 (frozen `c795361`, four pre-data amendments); Benchmark 019 |
| In vivo results (T cells, B cells, neutrophils) | lab 49; Benchmark 019 |
| In vitro results, frozen verdict NOT ROBUST | lab 50 (frozen `849616a`); Benchmark 020 |
| Lower bound σ ≳ 0.2 µm, invalid upper bound, split-half bound | lab 51 (post hoc, amended); Benchmark 020 |
| Figure 2 | lab 52 |
