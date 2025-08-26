# Reproduction Guide

1. Install dependencies from `requirements.txt` in a clean environment.  
2. Open the notebook `notebooks/evidence_brief.ipynb` and run all cells to:  
   - Load YAML/CSV  
   - Compute effect sizes  
   - Render the Markdown brief  
   - Generate the figure
3. The brief will be available at `docs/briefs/evidence_brief.md`.

Run tests with `pytest -q` to validate core logic.
