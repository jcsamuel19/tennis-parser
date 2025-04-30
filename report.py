"""CLI: parses log → computes stats → writes HTML report & (optional) parse tree."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from jinja2 import Environment, FileSystemLoader, select_autoescape

from lexer_parser import parse, _PARSER  # re‑use cached parser for tree
from stats import compute_all

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
TEMPLATE_DIR = Path(__file__).parent / "templates"
TEMPLATE_DIR.mkdir(exist_ok=True)
TEMPLATE_FILE = TEMPLATE_DIR / "report.html.jinja"
OUTPUT_DIR = Path(__file__).parent / "demo_output"
OUTPUT_DIR.mkdir(exist_ok=True)

# Write a minimal template on first run so students don’t forget
auto_template = """<!doctype html>
<html>
<head><meta charset="utf-8"><title>Tennis Stats</title></head>
<body>
<h1>Tennis Stats Dashboard</h1>
<h2>Outcome Counts</h2>
{{ outcome_table | safe }}
<h2>Aces vs Double Faults</h2>
{{ ace_df_table | safe }}
<img src="bar.png" alt="Outcome Bar Chart"/>
</body>
</html>"""
if not TEMPLATE_FILE.exists():
    TEMPLATE_FILE.write_text(auto_template, encoding="utf-8")

# Jinja2 env
_env = Environment(
    loader=FileSystemLoader(str(TEMPLATE_DIR)),
    autoescape=select_autoescape(["html"]),
)


def _make_bar_chart(df: pd.DataFrame, path: Path) -> None:
    """Simple stacked bar chart of outcomes."""
    ax = df.set_index("player")[["ACE", "WINNER", "ERROR", "DF"]].plot(
        kind="bar", stacked=False, figsize=(6, 4)
    )
    ax.set_ylabel("Count")
    ax.figure.tight_layout()
    ax.figure.savefig(path)
    plt.close(ax.figure)


def build_report(points_text: str, show_tree: bool = False) -> Path:
    """Return path to generated HTML file."""
    points = parse(points_text)
    stats = compute_all(points)

    # Save bar chart
    chart_path = OUTPUT_DIR / "bar.png"
    _make_bar_chart(stats["by_outcome"], chart_path)

    # Optional: save parse tree png via lark.tree_to_png (needs graphviz)
    if show_tree:
        try:
            parse_tree_path = OUTPUT_DIR / "parse_tree.png"
            _PARSER.parse(points_text + "").save_png(str(parse_tree_path))  # type: ignore[attr-defined]
        except Exception:
            print("[warn] graphviz not available; skipping tree PNG")

    # Render HTML
    tmpl = _env.get_template("report.html.jinja")
    html = tmpl.render(
        outcome_table=stats["by_outcome"].to_html(index=False),
        ace_df_table=stats["ace_df"].to_html(index=False),
    )
    out_file = OUTPUT_DIR / "report.html"
    out_file.write_text(html, encoding="utf-8")
    return out_file


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Generate tennis stats dashboard")
    ap.add_argument("log", help="match log text file path")
    ap.add_argument("--tree", action="store_true", help="export parse tree PNG")
    args = ap.parse_args()

    text = Path(args.log).read_text(encoding="utf-8")
    html_path = build_report(text, show_tree=args.tree)
    print(f"Report generated: {html_path.relative_to(Path.cwd())}")
