# Evidence Brief Template — Portfolio-Grade

**Author:** Maria Camila Cuesta  
**Focus Areas:** Medical Affairs • Scientific Communication • Evidence Synthesis • Effect Sizes • Reproducibility

This repository provides a **production-style template** to auto-generate a concise **Evidence Brief** (Markdown) from a structured study definition (YAML) and outcomes (CSV). It calculates **risk-based effect sizes** (RD, RR, OR) with **95% CIs**, renders a professional brief via **Jinja2**, and saves publication-ready **figures**.

## What it does
1) Load inputs (YAML + CSV)  
2) Compute effect sizes and 95% CIs  
3) Render Markdown brief via Jinja2 + figure  
4) Guarantee reproducibility with tests and a clean structure

## Repository structure
- `src/brief.py` — utilities (loading, effects, plotting, rendering)  
- `templates/brief_template.md.j2` — Markdown template for the brief  
- `notebooks/evidence_brief.ipynb` — end-to-end demo  
- `tests/` — unit tests (schema, effects, rendering)  
- `docs/wiki/` — scientific docs (methodology, dataset & ethics, reproduction, interpretation)  
- `docs/briefs/` — generated evidence briefs (Markdown)  
- `data/`, `figures/`, `outputs/` — input/generated artifacts (gitignored)

## Expected outputs
- `docs/briefs/evidence_brief.md` — brief final en Markdown  
- `figures/risk_Primary.png` — figura de riesgo por brazo

MIT License © 2025 — Maria Camila Cuesta. Synthetic data only.
