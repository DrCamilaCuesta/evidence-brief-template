\
from pathlib import Path
from src.brief import load_study_yaml, load_outcomes_csv, compute_effects_for_endpoint, render_brief

BASE = Path(__file__).resolve().parent.parent

def test_yaml_and_csv_ok():
    meta = load_study_yaml(BASE / "data" / "study_demo.yaml")
    assert meta["title"] and meta["created_by"]
    df = load_outcomes_csv(BASE / "data" / "outcomes_demo.csv")
    assert set(df["arm"].unique()).issubset({"treatment","control"})

def test_effects_and_render(tmp_path):
    from shutil import copyfile
    yaml_path = tmp_path / "study.yaml"
    csv_path = tmp_path / "outcomes.csv"
    copyfile(BASE / "data" / "study_demo.yaml", yaml_path)
    copyfile(BASE / "data" / "outcomes_demo.csv", csv_path)
    md_path = tmp_path / "brief.md"
    out = render_brief(yaml_path, csv_path, BASE / "templates", md_path)
    assert out.exists()
    text = out.read_text(encoding="utf-8")
    assert "Key Messages" in text and "Limitations" in text
