# Methodology — Effect Sizes & Rendering

## Inputs
- **YAML (study metadata):** title, indication, population, intervention/comparator, endpoints, safety notes, key messages, limitations.  
- **CSV (outcomes):** one row per arm per endpoint with `n` and `events`.

## Calculations
For each endpoint we compute:
- **Risk (treatment/control)** = events / n  
- **Risk Difference (RD)** = risk_treatment − risk_control with Wald 95% CI  
- **Risk Ratio (RR)** with log-scale Wald 95% CI  
- **Odds Ratio (OR)** with log-scale Wald 95% CI

> Approximations are used for didactic purposes; real analyses may prefer exact/Bayesian methods or continuity corrections when counts are small.

## Rendering
- A **Jinja2** template (`templates/brief_template.md.j2`) is populated with metadata and computed effects.  
- A simple **bar chart** illustrates risks by arm for the first endpoint.  
- The final brief is saved as `docs/briefs/evidence_brief.md`.
