---
type: "map-of-content"
field: "Physics"
epistemic_status: "mixed"
level: "all"
tags: ["map", "method"]
aliases: []
created: 2026-07-30
updated: 2026-07-30
---

# Theory Experiment Computation Loop

```mermaid
flowchart LR
  Q["Question"] --> M["Model and assumptions"]
  M --> P["Observable prediction"]
  P --> D["Experimental design"]
  D --> Y["Calibrated data"]
  Y --> I["Inference and uncertainty"]
  I --> C["Model comparison"]
  C -->|revise| M
  C -->|new question| Q
  M --> S["Simulation or analytic calculation"]
  S --> P
  Y --> V["Validation data"]
  V --> S
```

The loop is only as strong as its weakest interface. A beautiful model without an observable is not yet an empirical theory; a precise dataset without a measurement model is not yet a physical conclusion.

## Interface checklist

- Question → model: scope and alternatives are explicit.
- Model → prediction: approximation and numerical errors are bounded.
- Prediction → design: the observable separates plausible models.
- Instrument → data: calibration, background, selection, and drift are modeled.
- Data → inference: likelihood and priors are inspectable.
- Inference → claim: effect size, uncertainty, and domain are reported.

Navigate: [[Experimental Physics Map]] · [[Computational Physics Map]] · [[Epistemic Status and Claim Hygiene]]
