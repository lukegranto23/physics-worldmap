---
type: "guide"
field: "Foundations"
epistemic_status: "reference"
level: "all"
tags: ["guide", "epistemology", "status"]
aliases: []
created: 2026-07-30
updated: 2026-07-30
---

# Epistemic Status and Claim Hygiene

Physics becomes unreliable when mathematical beauty, empirical success, interpretation, and speculation are placed on one level. Every important claim in this vault should be classifiable.

| Label | Meaning | Required support |
|---|---|---|
| **established** | Repeatedly tested result or mature framework inside a stated domain | observations or experiments, uncertainty, domain |
| **effective** | Reliable scale-limited model without a claim of fundamental truth | small parameters, matching regime, error estimate |
| **active** | Established ingredients with unresolved mechanism or quantitative prediction | current evidence and competing accounts |
| **open** | No accepted solution or decisive evidence | precise question, constraints, discriminating tests |
| **conjectural** | A precise mathematically or physically motivated proposition not established as a general description of nature | explicit domain, assumptions, known realizations, counterexamples, distinguishing consequences |
| **speculative** | A structured possibility not established by evidence | assumptions, consistency checks, novel prediction, falsifier |
| **mixed** | A map or synthesis containing multiple statuses | status identified at claim level |
| **reference** | Workflow, notation, bibliography, or navigation | provenance and maintenance date |

## Claim ladder

`observation → calibrated datum → empirical regularity → model → mechanism → theory → interpretation`

Each arrow adds assumptions. Record them.

## Two independent status layers

`epistemic_status` classifies the **scientific subject matter** in its stated regime; it does not certify that every sentence in a note has already received a note-level source audit. `note_maturity` describes how developed the note is, while `source_audit` classifies its **documentation state**. For example, an established law can live in an orientation summary whose primary or canonical citations are still pending.

Treat `source_audit: orientation-summary-needs-canonical-source`, `source_audit: bibliography-present-needs-claim-audit`, and `source_audit: canonical-derivation-needs-citation-audit` as explicit work queues, not as doubt about the underlying well-tested physics. A claim becomes citation-audited only after its assumptions, domain, and supporting source have been checked under [[Source and Citation Policy]].

## Mandatory checks for a new idea

1. **Units:** Is every equation dimensionally consistent?
2. **Symmetry:** What transformations must leave observables invariant?
3. **Limits:** Does it recover established theories where they work?
4. **Degrees of freedom:** What exists in the model, and what has been integrated out?
5. **Stability and causality:** Are energies bounded appropriately, initial-value problems sensible, and signals causal?
6. **Probability:** Is the likelihood or stochastic rule normalized and operational?
7. **Novelty check:** Is this already known under another name?
8. **Prediction:** What observable differs from the baseline model?
9. **Falsifier:** Which outcome would reduce confidence?
10. **Scale and feasibility:** Can an existing or plausible experiment see the effect?

See [[Hypothesis Development Protocol]] and [[Source and Citation Policy]].
