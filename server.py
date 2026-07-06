#!/usr/bin/env python3
"""Local full-stack server for the Loneliness and Risk Decisions project."""

from __future__ import annotations

import csv
import io
import json
import math
import mimetypes
import os
import shutil
import sqlite3
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse


ROOT = Path(__file__).resolve().parent
STATIC_DIR = ROOT / "static"
DATA_DIR = ROOT / "data"
ASSET_DIR = ROOT / "assets"
SEED_DB_PATH = DATA_DIR / "loneliness_risk.db"
DB_PATH = Path(os.environ.get("LONELINESS_DB_PATH", str(SEED_DB_PATH)))
PAGE_ROUTES = {"/", "/index.html", "/survey", "/dashboard", "/research", "/evidence", "/downloads", "/contact"}


def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def scale_0_100(value: float, min_value: float = 1.0, max_value: float = 5.0) -> float:
    return max(0.0, min(100.0, (value - min_value) / (max_value - min_value) * 100.0))


def number(payload: dict, key: str, default: float = 0.0) -> float:
    try:
        return float(payload.get(key, default))
    except (TypeError, ValueError):
        return default


def item_values(payload: dict, prefix: str, count: int, default: float = 3.0) -> list[float]:
    return [number(payload, f"{prefix}{i}", default) for i in range(1, count + 1)]


def binary_values(payload: dict, prefix: str, count: int) -> list[float]:
    values = []
    for i in range(1, count + 1):
        raw = payload.get(f"{prefix}{i}", 0)
        if isinstance(raw, bool):
            values.append(1.0 if raw else 0.0)
        else:
            try:
                values.append(1.0 if float(raw) >= 1 else 0.0)
            except (TypeError, ValueError):
                values.append(0.0)
    return values


def classify(scores: dict) -> str:
    if scores["risk_decision_index"] < 38 and scores["social_connection_score"] >= 55:
        return "Social-buffered deliberator"
    if scores["immediate_reward_bias"] >= 67 and scores["impulsive_spending_score"] >= 60:
        return "Reward-sensitive accelerator"
    if scores["high_risk_choice_score"] >= 70:
        return "Risk-seeking chooser"
    if scores["conflict_defense_score"] >= 65:
        return "Conflict-defensive responder"
    return "Balanced decision-maker"


def score_payload(payload: dict) -> dict:
    loneliness_score = scale_0_100(mean(item_values(payload, "lq", 7)))
    social_connection_score = scale_0_100(mean(item_values(payload, "sci", 6)))
    immediate_reward_bias = mean(binary_values(payload, "delay_immediate_choice_", 6)) * 100
    impulsive_spending_score = scale_0_100(mean(item_values(payload, "spend", 5)))
    high_risk_choice_score = mean(binary_values(payload, "risk_choice_", 5)) * 100
    conflict_defense_score = scale_0_100(mean(item_values(payload, "conflict_defense_", 5)))
    risk_decision_index = (
        0.35 * immediate_reward_bias
        + 0.25 * impulsive_spending_score
        + 0.25 * high_risk_choice_score
        + 0.15 * conflict_defense_score
    )
    scores = {
        "loneliness_score": round(loneliness_score, 1),
        "social_connection_score": round(social_connection_score, 1),
        "immediate_reward_bias": round(immediate_reward_bias, 1),
        "impulsive_spending_score": round(impulsive_spending_score, 1),
        "high_risk_choice_score": round(high_risk_choice_score, 1),
        "conflict_defense_score": round(conflict_defense_score, 1),
        "risk_decision_index": round(risk_decision_index, 1),
    }
    scores["decision_type"] = classify(scores)
    scores["interpretation"] = interpret(scores)
    return scores


def interpret(scores: dict) -> str:
    risk = scores["risk_decision_index"]
    loneliness = scores["loneliness_score"]
    connection = scores["social_connection_score"]
    if risk >= 70:
        risk_text = "high"
    elif risk >= 50:
        risk_text = "moderate"
    else:
        risk_text = "lower"
    if loneliness >= 65 and connection < 45:
        mechanism = "The profile suggests a combination of perceived isolation and weaker social buffering."
    elif loneliness >= 65:
        mechanism = "Loneliness is elevated, but some connection resources remain visible."
    elif connection >= 60:
        mechanism = "Social connection appears to be a protective factor in this profile."
    else:
        mechanism = "The profile is mixed and should be interpreted as educational, not diagnostic."
    return f"Your composite risk-decision profile is {risk_text}. {mechanism}"


def load_json(path: Path) -> dict | list:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def ensure_runtime_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not DB_PATH.exists() and SEED_DB_PATH.exists():
        shutil.copyfile(SEED_DB_PATH, DB_PATH)


def db() -> sqlite3.Connection:
    ensure_runtime_db()
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con


class Handler(BaseHTTPRequestHandler):
    server_version = "LonelinessRiskLab/1.0"

    def log_message(self, fmt: str, *args) -> None:
        print("[%s] %s" % (self.log_date_time_string(), fmt % args))

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path
        if path in PAGE_ROUTES:
            return self.send_file(STATIC_DIR / "index.html", "text/html; charset=utf-8")
        if path == "/favicon.ico":
            return self.send_file(STATIC_DIR / "favicon.svg", "image/svg+xml")
        if path == "/api/config":
            return self.send_json(load_json(DATA_DIR / "study_config.json"))
        if path == "/api/summary":
            return self.send_json(self.summary())
        if path == "/api/responses":
            params = parse_qs(parsed.query)
            limit = int(params.get("limit", ["80"])[0])
            return self.send_json(self.get_responses(limit=limit))
        if path == "/api/export.csv":
            return self.send_csv()
        if path.startswith("/static/"):
            return self.send_file(STATIC_DIR / path.removeprefix("/static/"))
        if path.startswith("/assets/"):
            return self.send_file(ASSET_DIR / path.removeprefix("/assets/"))
        if path.startswith("/outputs/"):
            return self.send_file(ROOT / path.removeprefix("/"))
        return self.not_found()

    def do_HEAD(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path
        if path in PAGE_ROUTES:
            return self.send_file(STATIC_DIR / "index.html", "text/html; charset=utf-8", head_only=True)
        if path == "/favicon.ico":
            return self.send_file(STATIC_DIR / "favicon.svg", "image/svg+xml", head_only=True)
        if path.startswith("/static/"):
            return self.send_file(STATIC_DIR / path.removeprefix("/static/"), head_only=True)
        if path.startswith("/assets/"):
            return self.send_file(ASSET_DIR / path.removeprefix("/assets/"), head_only=True)
        if path.startswith("/outputs/"):
            return self.send_file(ROOT / path.removeprefix("/"), head_only=True)
        return self.not_found()

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        try:
            length = int(self.headers.get("Content-Length", "0"))
            body = self.rfile.read(length)
            payload = json.loads(body.decode("utf-8")) if body else {}
        except json.JSONDecodeError:
            return self.send_json({"error": "Invalid JSON"}, status=HTTPStatus.BAD_REQUEST)

        if parsed.path == "/api/score":
            return self.send_json(score_payload(payload))
        if parsed.path == "/api/submit":
            scores = score_payload(payload)
            self.insert_live_response(payload, scores)
            return self.send_json({"saved": True, "scores": scores, "summary": self.summary()})
        return self.not_found()

    def insert_live_response(self, payload: dict, scores: dict) -> None:
        with db() as con:
            con.execute(
                """
                INSERT INTO live_responses (
                    created_at, language, age, population, source_type,
                    loneliness_score, social_connection_score, immediate_reward_bias,
                    impulsive_spending_score, high_risk_choice_score,
                    conflict_defense_score, risk_decision_index, decision_type, raw_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    datetime.now(timezone.utc).isoformat(),
                    str(payload.get("language", "en")),
                    int(number(payload, "age", 0)),
                    str(payload.get("population", "unknown")),
                    "live_submission",
                    scores["loneliness_score"],
                    scores["social_connection_score"],
                    scores["immediate_reward_bias"],
                    scores["impulsive_spending_score"],
                    scores["high_risk_choice_score"],
                    scores["conflict_defense_score"],
                    scores["risk_decision_index"],
                    scores["decision_type"],
                    json.dumps(payload, ensure_ascii=False),
                ),
            )

    def summary(self) -> dict:
        stats = load_json(DATA_DIR / "stats_summary.json")
        with db() as con:
            live_count = con.execute("SELECT COUNT(*) AS n FROM live_responses").fetchone()["n"]
            live_avg = con.execute(
                """
                SELECT
                    AVG(loneliness_score) AS loneliness_score,
                    AVG(social_connection_score) AS social_connection_score,
                    AVG(risk_decision_index) AS risk_decision_index
                FROM live_responses
                """
            ).fetchone()
            recent = [
                dict(row)
                for row in con.execute(
                    """
                    SELECT created_at, age, population, loneliness_score, social_connection_score,
                           risk_decision_index, decision_type
                    FROM live_responses
                    ORDER BY id DESC
                    LIMIT 8
                    """
                ).fetchall()
            ]
        return {
            "seeded_stats": stats,
            "source_counts": {
                "synthetic_pilot": stats["n"],
                "live_submission": live_count,
                "public_benchmark": len(stats.get("public_benchmarks", [])),
            },
            "live_averages": {k: (round(live_avg[k], 2) if live_avg[k] is not None else None) for k in live_avg.keys()},
            "recent_live_submissions": recent,
        }

    def get_responses(self, limit: int = 80) -> dict:
        limit = max(1, min(limit, 500))
        with db() as con:
            synthetic = [
                dict(row)
                for row in con.execute(
                    """
                    SELECT participant_id, source_type, age, gender, student_status, region,
                           loneliness_score, social_connection_score, immediate_reward_bias,
                           impulsive_spending_score, high_risk_choice_score, conflict_defense_score,
                           risk_decision_index, decision_type
                    FROM responses
                    LIMIT ?
                    """,
                    (limit,),
                ).fetchall()
            ]
            live = [
                dict(row)
                for row in con.execute(
                    """
                    SELECT id AS participant_id, source_type, age, population,
                           loneliness_score, social_connection_score, immediate_reward_bias,
                           impulsive_spending_score, high_risk_choice_score, conflict_defense_score,
                           risk_decision_index, decision_type
                    FROM live_responses
                    ORDER BY id DESC
                    LIMIT ?
                    """,
                    (limit,),
                ).fetchall()
            ]
        return {"synthetic": synthetic, "live": live}

    def send_csv(self) -> None:
        rows = self.get_responses(limit=500)
        out = io.StringIO()
        fieldnames = [
            "participant_id",
            "source_type",
            "age",
            "gender",
            "student_status",
            "population",
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
        writer = csv.DictWriter(out, fieldnames=fieldnames)
        writer.writeheader()
        for source in ["synthetic", "live"]:
            for row in rows[source]:
                writer.writerow({key: row.get(key, "") for key in fieldnames})
        content = out.getvalue().encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/csv; charset=utf-8")
        self.send_header("Content-Disposition", 'attachment; filename="loneliness_risk_export.csv"')
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def send_file(self, path: Path, content_type: str | None = None, head_only: bool = False) -> None:
        try:
            resolved = path.resolve()
            if not str(resolved).startswith(str(ROOT.resolve())):
                return self.not_found()
            data = resolved.read_bytes()
        except FileNotFoundError:
            return self.not_found()
        mime = content_type or mimetypes.guess_type(str(path))[0] or "application/octet-stream"
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        if not head_only:
            self.wfile.write(data)

    def send_json(self, payload: dict | list, status: HTTPStatus = HTTPStatus.OK) -> None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def not_found(self) -> None:
        self.send_json({"error": "Not found"}, status=HTTPStatus.NOT_FOUND)


def run(host: str | None = None, port: int | None = None) -> None:
    host = host or os.environ.get("HOST", "0.0.0.0")
    port = port or int(os.environ.get("PORT", "8765"))
    ensure_runtime_db()
    server = ThreadingHTTPServer((host, port), Handler)
    print(f"Loneliness Risk Lab running at http://{host}:{port}")
    print("Press Ctrl+C to stop.")
    server.serve_forever()


if __name__ == "__main__":
    run()
