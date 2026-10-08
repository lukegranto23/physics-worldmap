---
type: investigation-index
created: 2026-09-18
updated: 2026-09-22
---

# Field investigations

An outward-looking research notebook, separate from the physics vault. Follow public evidence, build safe tests where they clarify a claim, and distinguish known work from genuinely new findings.

## First trail

[Case 001 — When verified software betrays trust](./001%20%E2%80%94%20When%20Verified%20Software%20Betrays%20Trust.md)

Status: primary-source incident/disclosure review, current September 2026 control checks, eight offline influence-graph scenarios checked. No active third-party testing. New-vulnerability and novelty claims: none.

## Concrete code investigation

[Case 002 — Reproduced dist-verification failure](./002-dist-verification/Finding.md): pinned `actions/attest` workflow code; seven local regression fixtures plus a September 20 isolated actual-project build. The real compiler restores an intentionally omitted JavaScript chunk, but all three original comparisons miss it; the applied patch detects it and accepts unchanged output. Source and dependencies remain unchanged. Semantic whitespace remains a separate language fixture. No remote-exploitation claim or external submission. See the report for limits and build evidence.

## Template-level prevention

[Case 003 — Template comparison](./003-template-comparison/Finding.md): seven local fixtures plus an isolated real Rollup build. An intentionally omitted source map is restored by the compiler but missed by the original check; the patch detects it and accepts complete output. The initial Linux test caught CRLF patch formatting, now corrected and retested on Windows/Linux. The template already cleans output, so Case 002's stale-output flaw does not transfer. No action runtime failure, downstream-prevalence claim, or external submission.

## Follow-up evidence

September 22: [pre-install cleanup review](./003-template-comparison/Preinstall%20Cleanup%20Review.md) records an offline differential: the template's cleanup before `npm ci` requires absent npm metadata, while cleanup with locked dependencies installed succeeds locally. The package script already cleans output after installation, making the early step redundant. This is a reproducibility recommendation, not an exploit or a new vulnerability claim.

September 21: [clean-build follow-up](./002-dist-verification/Clean%20Build%20Follow-up.md) establishes a second independent issue in the same pinned tree: a normal rebuild preserves `184.index.js`, but a clean build does not generate it. The comparison-only fix cannot expose stale output retained by the build itself. A failed baseline probe was rejected and preserved; the corrected probe matches all shared file hashes.

- Trust-boundary handoffs in build automation: compare vulnerable/fixed local fixtures against existing analysis, with explicit false-positive controls.
- Persistent state across privilege changes: examine whether the same review questions transfer to notebooks and agent memory, without assuming identical mechanisms.
- Claims with incomplete scope: collect examples where identity, integrity, authorization, and behavior are mistakenly treated as interchangeable guarantees.

## Reusable prevention tool

[Read-only output-tree checker](./tools/README.md): compares generated directories without Git tracking/ignore rules or whitespace suppression. Eighteen Linux tests pass; Windows passes thirteen with five explicit POSIX skips. Against hash-verified saved real builds, it identifies only the stale `184.index.js` and accepts output from two independent clean builds. It is an experimental comparator for frozen trees, not an atomic snapshot, security sandbox, or proof of safe code. [Integration evidence](./tools/saved-build-validation.json).

## Research boundaries

September 21 impact refinement: [static chunk audit](./002-dist-verification/Impact%20Assessment.md) finds no direct loader request for stale chunk 184; its implementation equals current chunk 606 after identifier normalization. This narrows the interpretation to duplicate leftover output, with no demonstrated runtime exploit. The referenced omitted chunk 606 remains a valid compiler/comparison regression case. External submission is awaiting user authorization; local investigation can continue.

Use primary sources; record event and publication dates separately. Read remote code as untrusted data. Do not execute unknown notebooks, download malware, probe unrelated infrastructure, contact people, or publish allegations as incidental research steps. A public disclosure is someone else's discovery unless we independently establish a new result. A successful toy model checks its assumptions and implementation, not the world.

## Continuity

The physics notes saved before this change of direction are preserved. Their September 18 release packaging is unfinished; the previous archive was not replaced. The interrupted local-workspace security review was not completed and yielded no clean bill of health.
