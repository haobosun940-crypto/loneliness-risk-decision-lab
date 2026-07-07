#!/usr/bin/env python3
"""Build the GitHub Pages static prototype in docs/."""

from __future__ import annotations

import csv
import json
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
BASE_PATH = "/loneliness-risk-decision-lab"
PUBLIC_SITE = "https://haobosun940-crypto.github.io/loneliness-risk-decision-lab"
EXPECTED_API = "https://loneliness-risk-decision-lab.onrender.com"
ROUTES = ["", "survey", "dashboard", "research", "evidence", "downloads", "contact"]
OUTPUT_FILES = [
    "loneliness_risk_research_paper.pdf",
    "loneliness_risk_research_report.docx",
    "loneliness_risk_research_deck.pptx",
    "loneliness_risk_research_workbook.xlsx",
    "loneliness_risk_intro_video.mp4",
    "loneliness_risk_research_package.zip",
    "loneliness_risk_video_script.txt",
]


def copytree_clean(src: Path, dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns(".DS_Store", "__pycache__", "*.pyc", "*.inspect.ndjson"))


def page_href(path: str) -> str:
    if path == "/":
        return f"{BASE_PATH}/"
    if path in {"/survey", "/dashboard", "/research", "/evidence", "/downloads", "/contact"}:
        return f"{BASE_PATH}{path}/"
    return f"{BASE_PATH}{path}"


def transform_html(html: str) -> str:
    config_tag = f'    <script src="{BASE_PATH}/page-config.js"></script>\n'
    html = html.replace("    <script src=\"/static/qrcode.min.js\"></script>\n", config_tag + f"    <script src=\"{BASE_PATH}/static/qrcode.min.js\"></script>\n")
    html = re.sub(r'(href|src)="(/(?:static|assets|outputs|api)[^"]*)"', lambda m: f'{m.group(1)}="{BASE_PATH}{m.group(2)}"', html)
    for route in ["/survey", "/dashboard", "/research", "/evidence", "/downloads", "/contact"]:
        html = html.replace(f'href="{route}"', f'href="{page_href(route)}"')
    html = html.replace('href="/"', f'href="{BASE_PATH}/"')
    return html


def build_static_api() -> None:
    api_dir = DOCS / "api"
    api_dir.mkdir(parents=True, exist_ok=True)
    stats = json.loads((ROOT / "data" / "stats_summary.json").read_text(encoding="utf-8"))
    config = json.loads((ROOT / "data" / "study_config.json").read_text(encoding="utf-8"))
    synthetic_rows = list(csv.DictReader((ROOT / "data" / "synthetic_participants.csv").open(encoding="utf-8")))
    preview_keys = [
        "participant_id",
        "source_type",
        "age",
        "gender",
        "student_status",
        "region",
        "loneliness_score",
        "social_connection_score",
        "immediate_reward_bias",
        "impulsive_spending_score",
        "high_risk_choice_score",
        "conflict_defense_score",
        "risk_decision_index",
        "decision_type",
    ]
    responses = {
        "synthetic": [{key: row.get(key, "") for key in preview_keys} for row in synthetic_rows[:80]],
        "live": [],
    }
    summary = {
        "seeded_stats": stats,
        "source_counts": {
            "synthetic_pilot": stats["n"],
            "live_submission": 0,
            "public_benchmark": len(stats.get("public_benchmarks", [])),
        },
        "live_summary": None,
    }
    (api_dir / "config.json").write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")
    (api_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    (api_dir / "responses.json").write_text(json.dumps(responses, ensure_ascii=False, indent=2), encoding="utf-8")

    export_path = api_dir / "export.csv"
    export_fields = ["participant_name", *[field for field in synthetic_rows[0].keys() if field != "participant_id"]]
    with export_path.open("w", encoding="utf-8", newline="") as f:
      writer = csv.DictWriter(f, fieldnames=export_fields)
      writer.writeheader()
      for row in synthetic_rows:
          writer.writerow({"participant_name": row["participant_id"], **{field: row.get(field, "") for field in export_fields if field != "participant_name"}})


def main() -> None:
    if DOCS.exists():
        shutil.rmtree(DOCS)
    DOCS.mkdir(parents=True)
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")

    copytree_clean(ROOT / "static", DOCS / "static")
    copytree_clean(ROOT / "assets", DOCS / "assets")
    (DOCS / "outputs").mkdir()
    for name in OUTPUT_FILES:
        shutil.copy2(ROOT / "outputs" / name, DOCS / "outputs" / name)
    build_static_api()

    config = {
        "basePath": BASE_PATH,
        "apiBase": EXPECTED_API,
        "staticApiBase": f"{BASE_PATH}/api",
        "publicSiteUrl": PUBLIC_SITE,
        "preferStaticApi": True,
    }
    (DOCS / "page-config.js").write_text(f"window.LRDL_CONFIG = {json.dumps(config, ensure_ascii=False, indent=2)};\n", encoding="utf-8")

    html = transform_html((ROOT / "static" / "index.html").read_text(encoding="utf-8"))
    for route in ROUTES:
        route_dir = DOCS / route if route else DOCS
        route_dir.mkdir(parents=True, exist_ok=True)
        (route_dir / "index.html").write_text(html, encoding="utf-8")
    (DOCS / "404.html").write_text(html, encoding="utf-8")
    print({"docs": str(DOCS), "public_site": PUBLIC_SITE, "routes": len(ROUTES)})


if __name__ == "__main__":
    main()
