#!/usr/bin/env python3
"""Build a root-domain static deployment in dist/.

This build is meant for Netlify, Cloudflare Pages, Vercel static hosting, or
any custom www/apex domain where the site is served from "/" instead of the
GitHub Pages project subpath.
"""

from __future__ import annotations

import csv
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
PUBLIC_SITE = "https://www.lonelinessriskdecisionlab.com"
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


def build_static_api() -> None:
    api_dir = DIST / "api"
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
            writer.writerow(
                {
                    "participant_name": row["participant_id"],
                    **{field: row.get(field, "") for field in export_fields if field != "participant_name"},
                }
            )


def main() -> None:
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)
    (DIST / ".nojekyll").write_text("", encoding="utf-8")

    copytree_clean(ROOT / "static", DIST / "static")
    copytree_clean(ROOT / "assets", DIST / "assets")
    (DIST / "outputs").mkdir()
    for name in OUTPUT_FILES:
        shutil.copy2(ROOT / "outputs" / name, DIST / "outputs" / name)
    build_static_api()

    config = {
        "basePath": "",
        "apiBase": "",
        "staticApiBase": "/api",
        "publicSiteUrl": PUBLIC_SITE,
        "preferStaticApi": True,
    }
    (DIST / "page-config.js").write_text(f"window.LRDL_CONFIG = {json.dumps(config, ensure_ascii=False, indent=2)};\n", encoding="utf-8")

    html = (ROOT / "static" / "index.html").read_text(encoding="utf-8")
    config_tag = '    <script src="/page-config.js"></script>\n'
    html = html.replace('    <script src="/static/qrcode.min.js"></script>\n', config_tag + '    <script src="/static/qrcode.min.js"></script>\n')
    for route in ROUTES:
        route_dir = DIST / route if route else DIST
        route_dir.mkdir(parents=True, exist_ok=True)
        (route_dir / "index.html").write_text(html, encoding="utf-8")
    (DIST / "404.html").write_text(html, encoding="utf-8")
    print({"dist": str(DIST), "public_site": PUBLIC_SITE, "routes": len(ROUTES)})


if __name__ == "__main__":
    main()
