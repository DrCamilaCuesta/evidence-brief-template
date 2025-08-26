\
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Tuple, List
from pathlib import Path
import numpy as np
import pandas as pd
import yaml
from jinja2 import Environment, FileSystemLoader
import matplotlib.pyplot as plt

REQUIRED_KEYS = [
    "title","indication","population","intervention","comparator",
    "endpoints","safety_notes","key_messages","limitations","created_by"
]

@dataclass
class EffectSizes:
    risk_treatment: float
    risk_control: float
    rd: float; rd_lcl: float; rd_ucl: float
    rr: float; rr_lcl: float; rr_ucl: float
    or_: float; or_lcl: float; or_ucl: float

def load_study_yaml(path: Path) -> Dict:
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    missing = [k for k in REQUIRED_KEYS if k not in data]
    if missing:
        raise ValueError(f"YAML is missing required keys: {missing}")
    if "version" not in data:
        data["version"] = "1.0"
    return data

def load_outcomes_csv(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    expected = {"arm","n","events","endpoint"}
    missing = expected.difference(df.columns)
    if missing:
        raise ValueError(f"CSV missing columns: {missing}")
    df["arm"] = df["arm"].str.lower().str.strip()
    if not set(df["arm"].unique()).issubset({"treatment","control"}):
        raise ValueError("arm must be 'treatment' or 'control'")
    return df

def _wald_ci_proportion(p: float, n: int, z: float = 1.96) -> Tuple[float, float]:
    se = np.sqrt(max(p * (1 - p) / n, 0.0))
    return (p - z * se, p + z * se)

def compute_effects_for_endpoint(df: pd.DataFrame, endpoint: str) -> EffectSizes:
    sub = df[df["endpoint"] == endpoint]
    if sub.shape[0] != 2:
        raise ValueError(f"Endpoint '{endpoint}' must have exactly two rows (treatment & control).")
    tr = sub[sub["arm"] == "treatment"].iloc[0]
    co = sub[sub["arm"] == "control"].iloc[0]
    nt, et = int(tr["n"]), int(tr["events"])
    nc, ec = int(co["n"]), int(co["events"])
    pt = et / nt if nt else np.nan
    pc = ec / nc if nc else np.nan

    # RD
    rd = pt - pc
    se_rd = np.sqrt(pt*(1-pt)/nt + pc*(1-pc)/nc)
    rd_lcl, rd_ucl = rd - 1.96*se_rd, rd + 1.96*se_rd

    # RR
    rr = (pt / pc) if pc > 0 else np.nan
    if et>0 and ec>0 and et<nt and ec<nc:
        ln_rr = np.log(rr)
        se_ln_rr = np.sqrt((1/et) - (1/nt) + (1/ec) - (1/nc))
        rr_lcl, rr_ucl = np.exp(ln_rr - 1.96*se_ln_rr), np.exp(ln_rr + 1.96*se_ln_rr)
    else:
        rr_lcl = rr_ucl = np.nan

    # OR
    ot = et / max(nt - et, 1e-9)
    oc = ec / max(nc - ec, 1e-9)
    or_ = ot / oc if oc>0 else np.nan
    if et>0 and ec>0 and et<nt and ec<nc:
        ln_or = np.log(or_)
        se_ln_or = np.sqrt(1/et + 1/(nt-et) + 1/ec + 1/(nc-ec))
        or_lcl, or_ucl = np.exp(ln_or - 1.96*se_ln_or), np.exp(ln_or + 1.96*se_ln_or)
    else:
        or_lcl = or_ucl = np.nan

    return EffectSizes(pt, pc, rd, rd_lcl, rd_ucl, rr, rr_lcl, rr_ucl, or_, or_lcl, or_ucl)

def plot_risks_bar(es: EffectSizes, endpoint: str, save_path: Path) -> Path:
    labels = ["Treatment", "Control"]
    vals = [es.risk_treatment, es.risk_control]
    plt.figure(figsize=(5,4))
    plt.bar(labels, vals)
    plt.ylim(0, 1)
    plt.ylabel("Risk (Proportion)")
    plt.title(f"Risk by Arm — {endpoint}")
    save_path.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.close()
    return save_path

def render_brief(study_yaml: Path, outcomes_csv: Path, template_dir: Path, output_md: Path) -> Path:
    meta = load_study_yaml(study_yaml)
    df = load_outcomes_csv(outcomes_csv)
    endpoints: List[str] = list(df["endpoint"].unique())
    results = {}
    for ep in endpoints:
        es = compute_effects_for_endpoint(df, ep)
        results[ep] = es.__dict__
    first_ep = endpoints[0]
    fig_path = output_md.parent.parent / "figures" / f"risk_{first_ep}.png"
    plot_risks_bar(compute_effects_for_endpoint(df, first_ep), first_ep, fig_path)

    env = Environment(loader=FileSystemLoader(str(template_dir)), autoescape=False, trim_blocks=True, lstrip_blocks=True)
    template = env.get_template("brief_template.md.j2")
    md = template.render(meta=meta, endpoints=endpoints, effects=results, figure_path=str(Path("figures") / f"risk_{first_ep}.png"))
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text(md, encoding="utf-8")
    return output_md
