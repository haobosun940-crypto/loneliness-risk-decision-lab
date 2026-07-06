#!/usr/bin/env python3
"""Generate synthetic pilot data, statistics, charts, database, QR, and PDF.

The synthetic rows are explicitly labeled as demonstration data. They are
designed to be plausible and internally consistent with the published research
logic, not to pretend that a human-subjects study has already been completed.
"""

from __future__ import annotations

import csv
import json
import math
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import qrcode
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Image as RLImage,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
ASSET_DIR = ROOT / "assets"
OUTPUT_DIR = ROOT / "outputs"
TMP_DIR = ROOT / "tmp"

QUESTIONNAIRE_URL = "http://localhost:8765/survey"
RNG = np.random.default_rng(20260701)


SOURCES = [
    {
        "id": "russell_1996_ucla",
        "type": "scale_foundation",
        "citation": "Russell, D. W. (1996). UCLA Loneliness Scale (Version 3): Reliability, validity, and factor structure. Journal of Personality Assessment, 66(1), 20-40.",
        "url": "https://doi.org/10.1207/s15327752jpa6601_2",
        "used_for": "Loneliness measurement precedent and reliability expectations.",
    },
    {
        "id": "hughes_2004_tils",
        "type": "scale_foundation",
        "citation": "Hughes, M. E., Waite, L. J., Hawkley, L. C., & Cacioppo, J. T. (2004). A short scale for measuring loneliness in large surveys. Research on Aging, 26(6), 655-672.",
        "url": "https://doi.org/10.1177/0164027504268574",
        "used_for": "Short-form loneliness survey design logic.",
    },
    {
        "id": "hawkley_cacioppo_2010",
        "type": "theory",
        "citation": "Hawkley, L. C., & Cacioppo, J. T. (2010). Loneliness matters: A theoretical and empirical review of consequences and mechanisms. Annals of Behavioral Medicine, 40(2), 218-227.",
        "url": "https://doi.org/10.1007/s12160-010-9210-8",
        "used_for": "Mechanism model linking perceived isolation with attention, affect, and behavior.",
    },
    {
        "id": "cacioppo_hawkley_2009",
        "type": "theory",
        "citation": "Cacioppo, J. T., & Hawkley, L. C. (2009). Perceived social isolation and cognition. Trends in Cognitive Sciences, 13(10), 447-454.",
        "url": "https://doi.org/10.1016/j.tics.2009.06.005",
        "used_for": "Social threat monitoring and cognition mechanism.",
    },
    {
        "id": "lee_2001_connectedness",
        "type": "scale_foundation",
        "citation": "Lee, R. M., Draper, M., & Lee, S. (2001). Social connectedness, dysfunctional interpersonal behaviors, and psychological distress: Testing a mediator model. Journal of Counseling Psychology, 48(3), 310-318.",
        "url": "https://doi.org/10.1037/0022-0167.48.3.310",
        "used_for": "Social connectedness construct and buffering logic.",
    },
    {
        "id": "blais_weber_2006_dospert",
        "type": "scale_foundation",
        "citation": "Blais, A. R., & Weber, E. U. (2006). A Domain-Specific Risk-Taking (DOSPERT) scale for adult populations. Judgment and Decision Making, 1(1), 33-47.",
        "url": "https://doi.org/10.1017/S1930297500000334",
        "used_for": "Risk-taking task design by domain.",
    },
    {
        "id": "kirby_1999_delay",
        "type": "behavioral_task",
        "citation": "Kirby, K. N., Petry, N. M., & Bickel, W. K. (1999). Heroin addicts have higher discount rates for delayed rewards than non-drug-using controls. Journal of Experimental Psychology: General, 128(1), 78-87.",
        "url": "https://doi.org/10.1037/0096-3445.128.1.78",
        "used_for": "Monetary choice task precedent for delay discounting.",
    },
    {
        "id": "rook_fisher_1995_impulse",
        "type": "scale_foundation",
        "citation": "Rook, D. W., & Fisher, R. J. (1995). Normative influences on impulsive buying behavior. Journal of Consumer Research, 22(3), 305-313.",
        "url": "https://doi.org/10.1086/209452",
        "used_for": "Impulsive consumption construct.",
    },
    {
        "id": "duclos_2013_social_exclusion_risk",
        "type": "mechanism",
        "citation": "Duclos, R., Wan, E. W., & Jiang, Y. (2013). Show me the honey! Effects of social exclusion on financial risk-taking. Journal of Consumer Research, 40(1), 122-135.",
        "url": "https://doi.org/10.1086/668900",
        "used_for": "Social exclusion and risky financial decision mechanism.",
    },
    {
        "id": "mead_2011_social_exclusion_spending",
        "type": "mechanism",
        "citation": "Mead, N. L., Baumeister, R. F., Stillman, T. F., Rawn, C. D., & Vohs, K. D. (2011). Social exclusion causes people to spend and consume strategically in the service of affiliation. Journal of Consumer Research, 37(5), 902-919.",
        "url": "https://doi.org/10.1086/656667",
        "used_for": "Affiliation-seeking consumption after exclusion.",
    },
    {
        "id": "surgeon_general_2023",
        "type": "public_context",
        "citation": "Office of the U.S. Surgeon General. (2023). Our Epidemic of Loneliness and Isolation: The U.S. Surgeon General's Advisory on the Healing Effects of Social Connection and Community.",
        "url": "https://www.hhs.gov/sites/default/files/surgeon-general-social-connection-advisory.pdf",
        "used_for": "Public-health context for social connection.",
    },
    {
        "id": "owid_social_connections",
        "type": "public_context",
        "citation": "Our World in Data. Social Connections and Loneliness.",
        "url": "https://ourworldindata.org/social-connections-and-loneliness",
        "used_for": "Public context and cross-national social connection background.",
    },
    {
        "id": "cdc_yrbs",
        "type": "public_context",
        "citation": "Centers for Disease Control and Prevention. Youth Risk Behavior Surveillance System (YRBSS).",
        "url": "https://www.cdc.gov/yrbs/",
        "used_for": "Adolescent risk-behavior survey context.",
    },
]


QUESTIONNAIRE = {
    "study_title": "Loneliness, Social Connection, and Risk Decisions",
    "research_question": (
        "Among late adolescents and emerging adults in digitally mediated school "
        "and college communities, how does loneliness predict immediate-reward "
        "preference, impulsive spending, risky choice, and conflict-response style, "
        "and does social connectedness buffer the association?"
    ),
    "topic_formula": {
        "broad_field": "Social psychology and behavioral decision science",
        "specific_population": "Late adolescents and emerging adults aged 16-24",
        "specific_variable": "Loneliness and perceived social connectedness",
        "specific_outcome": "Risk Decision Index from delay, spending, risk, and conflict tasks",
        "specific_context": "Digitally mediated peer networks in school and college settings",
    },
    "constructs": [
        "Loneliness Index (custom 7-item short battery, 0-100)",
        "Social Connection Index (custom 6-item behavioral/perceived support battery, 0-100)",
        "Immediate Reward Bias (6 binary delay-choice tasks, 0-100)",
        "Impulsive Spending Score (5 Likert items, 0-100)",
        "High-Risk Choice Score (5 binary choice tasks, 0-100)",
        "Conflict Defense Score (5 conflict-response scenarios, 0-100)",
        "Risk Decision Index = .35*Reward + .25*Spending + .25*Risk + .15*Conflict",
    ],
    "hypotheses": [
        "H1: Higher loneliness will predict a higher Risk Decision Index.",
        "H2: Social connectedness will negatively predict the Risk Decision Index and partially buffer loneliness.",
        "H3: The loneliness association will be strongest for immediate reward and impulsive spending.",
        "H4: Higher loneliness will be associated with more defensive conflict choices, especially withdrawal or reactive replies.",
    ],
    "disclosure": (
        "The seeded dataset is synthetic pilot data generated for demonstration. "
        "Live website submissions are stored separately as live_submissions."
    ),
}


def ensure_dirs() -> None:
    for path in [DATA_DIR, ASSET_DIR, OUTPUT_DIR, TMP_DIR / "pdf", TMP_DIR / "video"]:
        path.mkdir(parents=True, exist_ok=True)


def sigmoid(x: np.ndarray | float) -> np.ndarray | float:
    return 1 / (1 + np.exp(-x))


def likert_from_latent(latent: np.ndarray, noise: float = 0.75, reverse: bool = False) -> np.ndarray:
    values = latent + RNG.normal(0, noise, len(latent))
    if reverse:
        values = -values
    cut = np.quantile(values, [0.08, 0.28, 0.55, 0.80])
    return np.digitize(values, cut) + 1


def scale_0_100(x: pd.Series | np.ndarray, min_value: float, max_value: float) -> pd.Series | np.ndarray:
    return (x - min_value) / (max_value - min_value) * 100


def generate_synthetic_data(n: int = 420) -> pd.DataFrame:
    age = RNG.choice(np.arange(16, 25), size=n, p=[0.08, 0.12, 0.16, 0.17, 0.15, 0.13, 0.09, 0.06, 0.04])
    gender = RNG.choice(["Female", "Male", "Nonbinary/Other", "Prefer not to say"], size=n, p=[0.49, 0.45, 0.03, 0.03])
    status = RNG.choice(["High school", "Undergraduate", "Gap year", "Early career"], size=n, p=[0.44, 0.39, 0.07, 0.10])
    region = RNG.choice(["North America", "East Asia", "Europe", "Other"], size=n, p=[0.46, 0.31, 0.14, 0.09])

    latent_loneliness = RNG.normal(0, 1, n)
    stress = np.clip(50 + 12 * latent_loneliness + RNG.normal(0, 16, n), 0, 100)
    latent_connection = -0.58 * latent_loneliness + RNG.normal(0, 0.82, n)

    platform_sessions = np.clip(np.round(8 + 2.4 * latent_loneliness + RNG.normal(0, 3.8, n)), 0, 32).astype(int)
    messages_day = np.clip(np.round(19 + 5.4 * latent_connection - 1.2 * latent_loneliness + RNG.normal(0, 8, n)), 0, 80).astype(int)
    in_person_week = np.clip(np.round(9 + 2.7 * latent_connection - 1.8 * latent_loneliness + RNG.normal(0, 4.5, n)), 0, 35).astype(int)
    meals_week = np.clip(np.round(3.2 + 1.1 * latent_connection - 0.55 * latent_loneliness + RNG.normal(0, 1.8, n)), 0, 14).astype(int)
    group_month = np.clip(np.round(2.4 + 1.0 * latent_connection + RNG.normal(0, 1.4, n)), 0, 10).astype(int)
    trusted_contacts = np.clip(np.round(2.2 + 0.9 * latent_connection - 0.4 * latent_loneliness + RNG.normal(0, 1.1, n)), 0, 8).astype(int)
    sleep_hours = np.clip(7.1 - 0.32 * latent_loneliness - 0.015 * stress + RNG.normal(0, 0.75, n), 4.2, 9.5)

    rows = {
        "participant_id": [f"SYN-{i + 1:04d}" for i in range(n)],
        "source_type": ["synthetic_pilot"] * n,
        "age": age,
        "gender": gender,
        "student_status": status,
        "region": region,
        "platform_sessions_per_day": platform_sessions,
        "messages_sent_per_day": messages_day,
        "in_person_conversations_per_week": in_person_week,
        "shared_meals_or_social_events_per_week": meals_week,
        "group_activities_per_month": group_month,
        "trusted_contacts_count": trusted_contacts,
        "sleep_hours": np.round(sleep_hours, 1),
        "self_reported_stress_0_100": np.round(stress, 1),
    }

    for i in range(1, 8):
        rows[f"lq{i}"] = likert_from_latent(latent_loneliness, noise=0.68 + i * 0.02)
    for i in range(1, 7):
        rows[f"sci{i}"] = likert_from_latent(latent_connection, noise=0.70 + i * 0.03)

    reward_p = sigmoid(-0.35 + 0.58 * latent_loneliness - 0.28 * latent_connection + 0.012 * (stress - 50))
    for i in range(1, 7):
        rows[f"delay_immediate_choice_{i}"] = RNG.binomial(1, np.clip(reward_p + RNG.normal(0, 0.04, n), 0.04, 0.96))

    spend_latent = 0.45 * latent_loneliness - 0.22 * latent_connection + 0.011 * (stress - 50) + RNG.normal(0, 0.65, n)
    for i in range(1, 6):
        rows[f"spend{i}"] = likert_from_latent(spend_latent, noise=0.64 + i * 0.04)

    risk_p = sigmoid(-0.42 + 0.39 * latent_loneliness - 0.17 * latent_connection + 0.008 * (stress - 50))
    for i in range(1, 6):
        rows[f"risk_choice_{i}"] = RNG.binomial(1, np.clip(risk_p + RNG.normal(0, 0.05, n), 0.04, 0.95))

    conflict_latent = 0.42 * latent_loneliness - 0.38 * latent_connection + 0.010 * (stress - 50) + RNG.normal(0, 0.58, n)
    for i in range(1, 6):
        rows[f"conflict_defense_{i}"] = likert_from_latent(conflict_latent, noise=0.70)

    df = pd.DataFrame(rows)
    df["loneliness_score"] = scale_0_100(df[[f"lq{i}" for i in range(1, 8)]].mean(axis=1), 1, 5).round(1)
    df["social_connection_score"] = scale_0_100(df[[f"sci{i}" for i in range(1, 7)]].mean(axis=1), 1, 5).round(1)
    df["immediate_reward_bias"] = (df[[f"delay_immediate_choice_{i}" for i in range(1, 7)]].mean(axis=1) * 100).round(1)
    df["impulsive_spending_score"] = scale_0_100(df[[f"spend{i}" for i in range(1, 6)]].mean(axis=1), 1, 5).round(1)
    df["high_risk_choice_score"] = (df[[f"risk_choice_{i}" for i in range(1, 6)]].mean(axis=1) * 100).round(1)
    df["conflict_defense_score"] = scale_0_100(df[[f"conflict_defense_{i}" for i in range(1, 6)]].mean(axis=1), 1, 5).round(1)
    df["risk_decision_index"] = (
        0.35 * df["immediate_reward_bias"]
        + 0.25 * df["impulsive_spending_score"]
        + 0.25 * df["high_risk_choice_score"]
        + 0.15 * df["conflict_defense_score"]
    ).round(1)
    df["loneliness_group"] = pd.qcut(
        df["loneliness_score"],
        3,
        labels=["Low loneliness", "Moderate loneliness", "High loneliness"],
    ).astype(str)
    q75 = float(df["risk_decision_index"].quantile(0.75))
    df["top_quartile_risk"] = (df["risk_decision_index"] >= q75).astype(int)
    df["decision_type"] = df.apply(classify_decision_type, axis=1)
    df["created_at"] = datetime.now(timezone.utc).isoformat()
    df["data_note"] = "Synthetic pilot row generated for reproducible demonstration."
    return df


def classify_decision_type(row: pd.Series) -> str:
    if row["risk_decision_index"] < 38 and row["social_connection_score"] >= 55:
        return "Social-buffered deliberator"
    if row["immediate_reward_bias"] >= 67 and row["impulsive_spending_score"] >= 60:
        return "Reward-sensitive accelerator"
    if row["high_risk_choice_score"] >= 70:
        return "Risk-seeking chooser"
    if row["conflict_defense_score"] >= 65:
        return "Conflict-defensive responder"
    return "Balanced decision-maker"


def cronbach_alpha(df: pd.DataFrame, cols: list[str]) -> float:
    item_variances = df[cols].var(axis=0, ddof=1).sum()
    total_variance = df[cols].sum(axis=1).var(ddof=1)
    k = len(cols)
    return float(k / (k - 1) * (1 - item_variances / total_variance))


def zscore(series: pd.Series) -> pd.Series:
    return (series - series.mean()) / series.std(ddof=0)


def ols(y: pd.Series, x: pd.DataFrame) -> pd.DataFrame:
    x_mat = np.column_stack([np.ones(len(x)), x.to_numpy(dtype=float)])
    y_vec = y.to_numpy(dtype=float)
    beta = np.linalg.inv(x_mat.T @ x_mat) @ x_mat.T @ y_vec
    pred = x_mat @ beta
    resid = y_vec - pred
    n, p = x_mat.shape
    sigma2 = (resid @ resid) / (n - p)
    cov = sigma2 * np.linalg.inv(x_mat.T @ x_mat)
    se = np.sqrt(np.diag(cov))
    t_stat = beta / se
    p_norm = np.array([math.erfc(abs(t) / math.sqrt(2)) for t in t_stat])
    names = ["Intercept"] + list(x.columns)
    return pd.DataFrame(
        {
            "term": names,
            "estimate": beta,
            "std_error": se,
            "t_stat": t_stat,
            "p_approx": p_norm,
            "ci_low": beta - 1.96 * se,
            "ci_high": beta + 1.96 * se,
        }
    )


def logistic_irls(y: pd.Series, x: pd.DataFrame, max_iter: int = 60) -> pd.DataFrame:
    x_mat = np.column_stack([np.ones(len(x)), x.to_numpy(dtype=float)])
    y_vec = y.to_numpy(dtype=float)
    beta = np.zeros(x_mat.shape[1])
    for _ in range(max_iter):
        eta = np.clip(x_mat @ beta, -18, 18)
        p = sigmoid(eta)
        w = np.clip(p * (1 - p), 1e-5, None)
        z = eta + (y_vec - p) / w
        xtw = x_mat.T * w
        new_beta = np.linalg.pinv(xtw @ x_mat) @ (xtw @ z)
        if np.max(np.abs(new_beta - beta)) < 1e-7:
            beta = new_beta
            break
        beta = new_beta
    eta = np.clip(x_mat @ beta, -18, 18)
    p = sigmoid(eta)
    w = np.clip(p * (1 - p), 1e-5, None)
    cov = np.linalg.pinv((x_mat.T * w) @ x_mat)
    se = np.sqrt(np.diag(cov))
    z_stat = beta / se
    p_norm = np.array([math.erfc(abs(z) / math.sqrt(2)) for z in z_stat])
    names = ["Intercept"] + list(x.columns)
    return pd.DataFrame(
        {
            "term": names,
            "logit_estimate": beta,
            "odds_ratio": np.exp(beta),
            "std_error": se,
            "z_stat": z_stat,
            "p_approx": p_norm,
        }
    )


def anova_permutation(df: pd.DataFrame, y_col: str, group_col: str, iterations: int = 1500) -> dict:
    groups = [g[y_col].to_numpy() for _, g in df.groupby(group_col, sort=False)]
    all_y = df[y_col].to_numpy()
    grand = all_y.mean()
    ss_between = sum(len(g) * (g.mean() - grand) ** 2 for g in groups)
    ss_within = sum(((g - g.mean()) ** 2).sum() for g in groups)
    df_between = len(groups) - 1
    df_within = len(all_y) - len(groups)
    f_val = (ss_between / df_between) / (ss_within / df_within)
    eta2 = ss_between / (ss_between + ss_within)

    labels = df[group_col].to_numpy()
    perm_f = []
    for _ in range(iterations):
        shuffled = RNG.permutation(all_y)
        temp = pd.DataFrame({"y": shuffled, "g": labels})
        perm_groups = [g["y"].to_numpy() for _, g in temp.groupby("g", sort=False)]
        perm_grand = shuffled.mean()
        perm_ssb = sum(len(g) * (g.mean() - perm_grand) ** 2 for g in perm_groups)
        perm_ssw = sum(((g - g.mean()) ** 2).sum() for g in perm_groups)
        perm_f.append((perm_ssb / df_between) / (perm_ssw / df_within))
    p_perm = (sum(v >= f_val for v in perm_f) + 1) / (iterations + 1)
    return {
        "outcome": y_col,
        "group": group_col,
        "F": float(f_val),
        "df_between": int(df_between),
        "df_within": int(df_within),
        "eta_squared": float(eta2),
        "p_permutation": float(p_perm),
    }


def compute_stats(df: pd.DataFrame) -> dict:
    model_df = pd.DataFrame(
        {
            "loneliness_z": zscore(df["loneliness_score"]),
            "social_connection_z": zscore(df["social_connection_score"]),
            "stress_z": zscore(df["self_reported_stress_0_100"]),
            "age_z": zscore(df["age"]),
            "platform_sessions_z": zscore(df["platform_sessions_per_day"]),
            "sleep_z": zscore(df["sleep_hours"]),
            "loneliness_x_connection": zscore(df["loneliness_score"]) * zscore(df["social_connection_score"]),
        }
    )
    ols_results = ols(df["risk_decision_index"], model_df)
    logit_results = logistic_irls(df["top_quartile_risk"], model_df)
    anova = anova_permutation(df, "risk_decision_index", "loneliness_group")

    corr_cols = [
        "loneliness_score",
        "social_connection_score",
        "immediate_reward_bias",
        "impulsive_spending_score",
        "high_risk_choice_score",
        "conflict_defense_score",
        "risk_decision_index",
        "platform_sessions_per_day",
        "messages_sent_per_day",
        "in_person_conversations_per_week",
    ]
    corr = df[corr_cols].corr().round(3)
    group_summary = (
        df.groupby("loneliness_group", sort=False)
        .agg(
            n=("participant_id", "count"),
            loneliness_score=("loneliness_score", "mean"),
            social_connection_score=("social_connection_score", "mean"),
            immediate_reward_bias=("immediate_reward_bias", "mean"),
            impulsive_spending_score=("impulsive_spending_score", "mean"),
            high_risk_choice_score=("high_risk_choice_score", "mean"),
            conflict_defense_score=("conflict_defense_score", "mean"),
            risk_decision_index=("risk_decision_index", "mean"),
        )
        .round(2)
        .reset_index()
        .sort_values("loneliness_score")
    )
    type_counts = df["decision_type"].value_counts().rename_axis("decision_type").reset_index(name="n")

    return {
        "n": int(len(df)),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "cronbach_alpha": {
            "loneliness_custom_7_item": round(cronbach_alpha(df, [f"lq{i}" for i in range(1, 8)]), 3),
            "social_connection_custom_6_item": round(cronbach_alpha(df, [f"sci{i}" for i in range(1, 7)]), 3),
        },
        "ols": ols_results.round(4).to_dict(orient="records"),
        "logit": logit_results.round(4).to_dict(orient="records"),
        "anova": {k: round(v, 4) if isinstance(v, float) else v for k, v in anova.items()},
        "correlation_matrix": corr.to_dict(),
        "group_summary": group_summary.to_dict(orient="records"),
        "decision_type_counts": type_counts.to_dict(orient="records"),
        "public_benchmarks": public_benchmarks(),
    }


def public_benchmarks() -> list[dict]:
    return [
        {
            "benchmark": "US public-health advisory frames loneliness and isolation as a population-level health concern.",
            "value": "Context note",
            "source_id": "surgeon_general_2023",
            "url": "https://www.hhs.gov/sites/default/files/surgeon-general-social-connection-advisory.pdf",
        },
        {
            "benchmark": "Cross-national social connection indicators vary substantially by country and age group.",
            "value": "Context note",
            "source_id": "owid_social_connections",
            "url": "https://ourworldindata.org/social-connections-and-loneliness",
        },
        {
            "benchmark": "YRBSS provides repeated adolescent risk-behavior context for study framing.",
            "value": "Context note",
            "source_id": "cdc_yrbs",
            "url": "https://www.cdc.gov/yrbs/",
        },
    ]


def write_core_files(df: pd.DataFrame, stats: dict) -> None:
    df.to_csv(DATA_DIR / "synthetic_participants.csv", index=False)
    with open(DATA_DIR / "sources.json", "w", encoding="utf-8") as f:
        json.dump(SOURCES, f, indent=2)
    with open(DATA_DIR / "study_config.json", "w", encoding="utf-8") as f:
        json.dump({"questionnaire": QUESTIONNAIRE, "sources": SOURCES}, f, indent=2)
    with open(DATA_DIR / "stats_summary.json", "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)
    with open(DATA_DIR / "public_benchmarks.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["benchmark", "value", "source_id", "url"])
        writer.writeheader()
        writer.writerows(public_benchmarks())
    write_stata_do_file()
    write_readme_data_dictionary()
    write_sqlite(df, stats)


def write_stata_do_file() -> None:
    text = """* Loneliness and Risk Decisions - Stata-ready analysis script
clear all
set more off
import delimited "data/synthetic_participants.csv", clear

* Reliability checks
alpha lq1-lq7
alpha sci1-sci6

* Standardized predictors
egen loneliness_z = std(loneliness_score)
egen social_connection_z = std(social_connection_score)
egen stress_z = std(self_reported_stress_0_100)
egen age_z = std(age)
egen platform_sessions_z = std(platform_sessions_per_day)
egen sleep_z = std(sleep_hours)
gen loneliness_x_connection = loneliness_z * social_connection_z

* Core OLS model
reg risk_decision_index loneliness_z social_connection_z stress_z age_z platform_sessions_z sleep_z loneliness_x_connection, robust

* Logistic model for top quartile risk profile
logit top_quartile_risk loneliness_z social_connection_z stress_z age_z platform_sessions_z sleep_z loneliness_x_connection
estat classification

* Group comparison
oneway risk_decision_index loneliness_group, tabulate

* Outcome-specific models
foreach y in immediate_reward_bias impulsive_spending_score high_risk_choice_score conflict_defense_score {
    reg `y' loneliness_z social_connection_z stress_z age_z platform_sessions_z sleep_z loneliness_x_connection, robust
}
"""
    (DATA_DIR / "stata_analysis.do").write_text(text, encoding="utf-8")


def write_readme_data_dictionary() -> None:
    lines = [
        "# Data dictionary",
        "",
        "All seeded rows use `source_type = synthetic_pilot`. They are simulated for method demonstration and should not be described as human-subject data.",
        "",
        "Key variables:",
        "- `loneliness_score`: custom 7-item loneliness battery scaled 0-100.",
        "- `social_connection_score`: custom 6-item connection/support battery scaled 0-100.",
        "- `immediate_reward_bias`: percentage of delay-choice tasks where the immediate reward was selected.",
        "- `impulsive_spending_score`: custom 5-item spending impulse battery scaled 0-100.",
        "- `high_risk_choice_score`: percentage of risk tasks where the riskier option was selected.",
        "- `conflict_defense_score`: custom conflict-withdrawal/reactivity task scaled 0-100.",
        "- `risk_decision_index`: weighted composite = 0.35*reward + 0.25*spending + 0.25*risk + 0.15*conflict.",
        "- `top_quartile_risk`: 1 if the risk index is in the sample top quartile.",
        "",
        "Recommended next step: collect live survey responses through the website. Those rows are stored as `live_submission` in SQLite and should be exported before inferential claims are made.",
    ]
    (DATA_DIR / "DATA_DICTIONARY.md").write_text("\n".join(lines), encoding="utf-8")


def write_sqlite(df: pd.DataFrame, stats: dict) -> None:
    db_path = DATA_DIR / "loneliness_risk.db"
    if db_path.exists():
        db_path.unlink()
    con = sqlite3.connect(db_path)
    df.to_sql("responses", con, index=False, if_exists="replace")
    con.execute(
        """
        CREATE TABLE IF NOT EXISTS live_responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            language TEXT,
            age INTEGER,
            population TEXT,
            source_type TEXT,
            loneliness_score REAL,
            social_connection_score REAL,
            immediate_reward_bias REAL,
            impulsive_spending_score REAL,
            high_risk_choice_score REAL,
            conflict_defense_score REAL,
            risk_decision_index REAL,
            decision_type TEXT,
            raw_json TEXT NOT NULL
        )
        """
    )
    con.execute(
        """
        CREATE TABLE IF NOT EXISTS citations (
            id TEXT PRIMARY KEY,
            type TEXT,
            citation TEXT,
            url TEXT,
            used_for TEXT
        )
        """
    )
    con.executemany(
        "INSERT OR REPLACE INTO citations(id, type, citation, url, used_for) VALUES (?, ?, ?, ?, ?)",
        [(s["id"], s["type"], s["citation"], s["url"], s["used_for"]) for s in SOURCES],
    )
    con.execute(
        """
        CREATE TABLE IF NOT EXISTS model_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            generated_at TEXT,
            result_json TEXT
        )
        """
    )
    con.execute(
        "INSERT INTO model_results(generated_at, result_json) VALUES (?, ?)",
        (stats["generated_at"], json.dumps(stats)),
    )
    con.commit()
    con.close()


def save_chart(path: Path) -> None:
    plt.tight_layout()
    plt.savefig(path, dpi=180, bbox_inches="tight")
    plt.close()


def make_charts(df: pd.DataFrame, stats: dict) -> None:
    plt.style.use("seaborn-v0_8-whitegrid")

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(df["loneliness_score"], df["risk_decision_index"], s=26, alpha=0.55, c="#2457A6", edgecolors="none")
    coef = np.polyfit(df["loneliness_score"], df["risk_decision_index"], 1)
    xs = np.linspace(df["loneliness_score"].min(), df["loneliness_score"].max(), 100)
    ax.plot(xs, coef[0] * xs + coef[1], color="#D84E38", linewidth=2.5)
    ax.set_title("Loneliness is positively associated with the Risk Decision Index")
    ax.set_xlabel("Loneliness Index (0-100)")
    ax.set_ylabel("Risk Decision Index (0-100)")
    save_chart(ASSET_DIR / "chart_scatter_loneliness_risk.png")

    group_df = pd.DataFrame(stats["group_summary"])
    fig, ax = plt.subplots(figsize=(8, 5))
    colors_bar = ["#2D6A6A", "#E0A72E", "#C94C4C"]
    ax.bar(group_df["loneliness_group"], group_df["risk_decision_index"], color=colors_bar)
    ax.set_ylim(0, max(85, group_df["risk_decision_index"].max() + 10))
    ax.set_title("Risk Decision Index rises across loneliness tertiles")
    ax.set_ylabel("Mean Risk Decision Index")
    ax.tick_params(axis="x", rotation=8)
    for i, value in enumerate(group_df["risk_decision_index"]):
        ax.text(i, value + 1.5, f"{value:.1f}", ha="center", fontweight="bold")
    save_chart(ASSET_DIR / "chart_anova_groups.png")

    ols_df = pd.DataFrame(stats["ols"])
    ols_df = ols_df[ols_df["term"] != "Intercept"].copy()
    fig, ax = plt.subplots(figsize=(8, 5))
    y = np.arange(len(ols_df))
    ax.barh(y, ols_df["estimate"], color=["#C94C4C" if v > 0 else "#2D6A6A" for v in ols_df["estimate"]])
    ax.axvline(0, color="#252525", linewidth=1)
    ax.set_yticks(y)
    ax.set_yticklabels([t.replace("_", " ") for t in ols_df["term"]])
    ax.set_title("OLS coefficients for the Risk Decision Index")
    ax.set_xlabel("Unstandardized coefficient on standardized predictors")
    save_chart(ASSET_DIR / "chart_regression_coefficients.png")

    corr = pd.DataFrame(stats["correlation_matrix"])
    fig, ax = plt.subplots(figsize=(8, 7))
    im = ax.imshow(corr.values, cmap="RdBu_r", vmin=-1, vmax=1)
    ax.set_xticks(np.arange(len(corr.columns)))
    ax.set_yticks(np.arange(len(corr.index)))
    ax.set_xticklabels([c.replace("_", "\n") for c in corr.columns], fontsize=7)
    ax.set_yticklabels([c.replace("_", " ") for c in corr.index], fontsize=8)
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
    for i in range(len(corr.index)):
        for j in range(len(corr.columns)):
            ax.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center", fontsize=6, color="#111")
    ax.set_title("Correlation structure of social connection and decision variables")
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    save_chart(ASSET_DIR / "chart_correlation_heatmap.png")

    type_df = pd.DataFrame(stats["decision_type_counts"])
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(type_df["decision_type"], type_df["n"], color="#456990")
    ax.invert_yaxis()
    ax.set_title("Decision profiles in the synthetic pilot sample")
    ax.set_xlabel("Count")
    save_chart(ASSET_DIR / "chart_decision_types.png")

    draw_flow_diagram(ASSET_DIR / "method_flow.png")


def draw_flow_diagram(path: Path) -> None:
    width, height = 1600, 900
    img = Image.new("RGB", (width, height), "#F7F5F0")
    draw = ImageDraw.Draw(img)
    try:
        title_font = ImageFont.truetype("Arial.ttf", 54)
        body_font = ImageFont.truetype("Arial.ttf", 28)
        small_font = ImageFont.truetype("Arial.ttf", 22)
    except OSError:
        title_font = ImageFont.load_default()
        body_font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    draw.text((80, 55), "From Social Disconnection to Quantified Decision Risk", fill="#1C2430", font=title_font)
    blocks = [
        ("1. Social Signals", "Loneliness, connection,\ncontact frequency,\nstress and sleep", (80, 190), "#2D6A6A"),
        ("2. Choice Tasks", "Delay choices,\nspending impulse,\nrisk scenarios,\nconflict response", (480, 190), "#456990"),
        ("3. Stats Engine", "Reliability, OLS,\nlogit, ANOVA,\ncorrelation matrix", (880, 190), "#D98E04"),
        ("4. Personal Report", "Risk Decision Index,\ndecision profile,\nbehavioral suggestions", (1280, 190), "#B23A48"),
    ]
    for title, body, (x, y), color in blocks:
        draw.rounded_rectangle((x, y, x + 260, y + 420), radius=26, fill="white", outline=color, width=6)
        draw.rectangle((x, y, x + 260, y + 72), fill=color)
        draw.text((x + 22, y + 20), title, fill="white", font=body_font)
        draw.multiline_text((x + 24, y + 118), body, fill="#1C2430", font=body_font, spacing=10)
    for x in [355, 755, 1155]:
        draw.line((x, 400, x + 90, 400), fill="#1C2430", width=6)
        draw.polygon([(x + 90, 400), (x + 65, 383), (x + 65, 417)], fill="#1C2430")
    draw.text((80, 695), "Design constraint: broad field + specific population + predictor + outcome + context", fill="#1C2430", font=body_font)
    draw.text((80, 745), "Population: late adolescents and emerging adults aged 16-24 in digitally mediated school/college networks.", fill="#445", font=small_font)
    img.save(path)


def make_qr() -> None:
    qr = qrcode.QRCode(version=3, box_size=10, border=3)
    qr.add_data(QUESTIONNAIRE_URL)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#1C2430", back_color="#FFFFFF").convert("RGB")
    canvas = Image.new("RGB", (560, 660), "#F7F5F0")
    canvas.paste(img.resize((420, 420)), (70, 45))
    draw = ImageDraw.Draw(canvas)
    try:
        title_font = ImageFont.truetype("Arial.ttf", 26)
        body_font = ImageFont.truetype("Arial.ttf", 18)
    except OSError:
        title_font = ImageFont.load_default()
        body_font = ImageFont.load_default()
    draw.text((55, 500), "Loneliness & Risk Decision Survey", fill="#1C2430", font=title_font)
    draw.text((55, 540), "Local link: http://localhost:8765/survey", fill="#394150", font=body_font)
    draw.text((55, 572), "Use after starting server.py", fill="#394150", font=body_font)
    canvas.save(ASSET_DIR / "questionnaire_qr.png")


def pdf_header_footer(canvas, doc) -> None:
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#5B6472"))
    canvas.drawString(0.72 * inch, 0.45 * inch, "Loneliness, Social Connection, and Risk Decisions")
    canvas.drawRightString(7.8 * inch, 0.45 * inch, f"Page {doc.page}")
    canvas.restoreState()


def build_pdf_report(df: pd.DataFrame, stats: dict) -> None:
    pdf_path = OUTPUT_DIR / "loneliness_risk_research_paper.pdf"
    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=letter,
        rightMargin=0.68 * inch,
        leftMargin=0.68 * inch,
        topMargin=0.62 * inch,
        bottomMargin=0.66 * inch,
    )
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="PaperTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=18,
            leading=22,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#1C2430"),
            spaceAfter=12,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Section",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=16,
            textColor=colors.HexColor("#243B53"),
            spaceBefore=12,
            spaceAfter=5,
        )
    )
    styles.add(
        ParagraphStyle(
            name="BodyTight",
            parent=styles["BodyText"],
            fontSize=9.2,
            leading=12,
            alignment=TA_LEFT,
            spaceAfter=5,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Caption",
            parent=styles["BodyText"],
            fontSize=8,
            leading=10,
            textColor=colors.HexColor("#5B6472"),
            spaceAfter=8,
        )
    )

    story = []
    story.append(Paragraph("Loneliness, Social Connection, and Risk Decisions", styles["PaperTitle"]))
    story.append(
        Paragraph(
            "A quantitative behavioral-decision study design using survey indicators, choice tasks, regression, ANOVA, and an interactive data-collection website.",
            styles["BodyTight"],
        )
    )
    story.append(Spacer(1, 0.08 * inch))
    story.append(Paragraph("<b>Abstract</b>", styles["Section"]))
    story.append(
        Paragraph(
            "This project tests whether loneliness predicts a higher tendency toward immediate rewards, impulsive spending, risky choices, and defensive conflict responses among late adolescents and emerging adults. "
            "The study uses a custom short-form questionnaire and simple behavioral choice tasks, then integrates reliability analysis, OLS regression, logistic classification, and one-way ANOVA. "
            "The seeded dataset contains synthetic pilot observations for reproducible demonstration; live website submissions are stored separately and can replace or extend the pilot sample.",
            styles["BodyTight"],
        )
    )
    story.append(Paragraph("<b>Research-question boundary</b>", styles["Section"]))
    boundary_rows = [["Component", "Specification"]] + [[k.replace("_", " ").title(), v] for k, v in QUESTIONNAIRE["topic_formula"].items()]
    table = Table(boundary_rows, colWidths=[1.8 * inch, 5.0 * inch])
    table.setStyle(basic_table_style(header_color="#243B53"))
    story.append(table)
    story.append(Paragraph("<b>Theoretical model</b>", styles["Section"]))
    story.append(
        Paragraph(
            "The mechanism is intentionally cross-disciplinary. Psychology supplies the construct chain: perceived social isolation can heighten social-threat monitoring, negative affect, and affiliation motives. "
            "Statistics supplies the testable model: the Risk Decision Index is predicted from loneliness, connectedness, stress, age, platform intensity, sleep, and the loneliness-by-connectedness interaction.",
            styles["BodyTight"],
        )
    )
    story.append(RLImage(str(ASSET_DIR / "method_flow.png"), width=6.75 * inch, height=3.8 * inch))
    story.append(Paragraph("Figure 1. Full workflow from social signals to quantified decision profile.", styles["Caption"]))
    story.append(Paragraph("<b>Measures and scoring</b>", styles["Section"]))
    measure_rows = [["Construct", "Operationalization"]] + [[m.split(" (")[0], m] for m in QUESTIONNAIRE["constructs"]]
    table = Table(measure_rows, colWidths=[2.1 * inch, 4.7 * inch])
    table.setStyle(basic_table_style(header_color="#2D6A6A"))
    story.append(table)
    story.append(Paragraph("<b>Statistical results on the synthetic pilot sample</b>", styles["Section"]))
    alpha = stats["cronbach_alpha"]
    story.append(
        Paragraph(
            f"The synthetic pilot sample contains n={stats['n']} rows. Internal consistency was acceptable for the custom loneliness battery (alpha={alpha['loneliness_custom_7_item']}) "
            f"and social connection battery (alpha={alpha['social_connection_custom_6_item']}). The one-way ANOVA comparing loneliness tertiles on the Risk Decision Index yielded "
            f"F({stats['anova']['df_between']}, {stats['anova']['df_within']})={stats['anova']['F']:.2f}, eta^2={stats['anova']['eta_squared']:.3f}, permutation p={stats['anova']['p_permutation']:.4f}.",
            styles["BodyTight"],
        )
    )
    story.append(RLImage(str(ASSET_DIR / "chart_anova_groups.png"), width=6.25 * inch, height=3.75 * inch))
    story.append(Paragraph("Figure 2. Mean Risk Decision Index by loneliness tertile.", styles["Caption"]))
    story.append(RLImage(str(ASSET_DIR / "chart_regression_coefficients.png"), width=6.25 * inch, height=3.75 * inch))
    story.append(Paragraph("Figure 3. OLS model coefficients using standardized predictors.", styles["Caption"]))
    story.append(PageBreak())
    story.append(Paragraph("<b>Model table</b>", styles["Section"]))
    ols_rows = [["Term", "Estimate", "SE", "t", "p approx", "95% CI"]]
    for row in stats["ols"]:
        ols_rows.append(
            [
                row["term"].replace("_", " "),
                f"{row['estimate']:.2f}",
                f"{row['std_error']:.2f}",
                f"{row['t_stat']:.2f}",
                format_p(row["p_approx"]),
                f"[{row['ci_low']:.2f}, {row['ci_high']:.2f}]",
            ]
        )
    table = Table(ols_rows, colWidths=[2.25 * inch, 0.8 * inch, 0.65 * inch, 0.55 * inch, 0.72 * inch, 1.25 * inch])
    table.setStyle(basic_table_style(header_color="#456990", font_size=7.2))
    story.append(table)
    story.append(Paragraph("<b>Interpretation</b>", styles["Section"]))
    story.append(
        Paragraph(
            "In the demonstration data, loneliness is a positive predictor of the composite risk index even after controlling for connectedness, stress, platform intensity, sleep, and age. "
            "Social connectedness is negative in the same model, consistent with a buffering interpretation. The interaction term should be treated as exploratory until live data are collected.",
            styles["BodyTight"],
        )
    )
    story.append(RLImage(str(ASSET_DIR / "chart_scatter_loneliness_risk.png"), width=6.25 * inch, height=3.75 * inch))
    story.append(Paragraph("Figure 4. Participant-level association between loneliness and the Risk Decision Index.", styles["Caption"]))
    story.append(Paragraph("<b>Data governance</b>", styles["Section"]))
    story.append(
        Paragraph(
            "The live website avoids clinical diagnosis and provides only an educational risk-profile report. For human-subject research, the questionnaire should be reviewed by a supervisor or ethics board, "
            "use consent language, avoid collecting unnecessary identifiers, and clearly separate pilot/synthetic rows from real submissions.",
            styles["BodyTight"],
        )
    )
    story.append(Paragraph("<b>References</b>", styles["Section"]))
    for i, src in enumerate(SOURCES, 1):
        story.append(Paragraph(f"{i}. {src['citation']} URL: {src['url']}", styles["Caption"]))
    doc.build(story, onFirstPage=pdf_header_footer, onLaterPages=pdf_header_footer)


def basic_table_style(header_color: str, font_size: float = 8.0) -> TableStyle:
    return TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(header_color)),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), font_size),
            ("LEADING", (0, 0), (-1, -1), font_size + 2),
            ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#D8DEE6")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F4F7FA")]),
            ("LEFTPADDING", (0, 0), (-1, -1), 5),
            ("RIGHTPADDING", (0, 0), (-1, -1), 5),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]
    )


def format_p(p: float) -> str:
    if p < 0.001:
        return "<.001"
    return f"{p:.3f}"


def write_video_script(stats: dict) -> None:
    script = f"""Loneliness, Social Connection, and Risk Decisions.

This project asks a narrow research question: among late adolescents and emerging adults in digitally mediated school and college networks, does loneliness predict riskier decisions?

The design combines psychology and statistics. Psychology defines the constructs: loneliness, social connectedness, immediate reward bias, impulsive spending, risky choice, and defensive conflict response. Statistics turns those constructs into measurable variables, checks reliability, and estimates regression models.

The current database begins with {stats['n']} synthetic pilot rows. They are not presented as real human-subject data. They let the website, questionnaire, workbook, and paper demonstrate the full research pipeline before live data collection begins.

The core result in the demonstration sample is clear: the Risk Decision Index rises across loneliness tertiles. The OLS model shows a positive loneliness coefficient and a negative social connectedness coefficient after controls for stress, age, sleep, and platform intensity.

The website then closes the loop. A participant completes the questionnaire, receives a personal risk-decision profile, and the response is stored separately as a live submission. As real responses accumulate, the same charts and models can be updated.

The research is therefore not only a written report. It is a reproducible social-science system: literature, measurement, data collection, database, regression, visualization, and participant feedback in one workflow.
"""
    (OUTPUT_DIR / "loneliness_risk_video_script.txt").write_text(script, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    df = generate_synthetic_data()
    stats = compute_stats(df)
    write_core_files(df, stats)
    make_charts(df, stats)
    make_qr()
    build_pdf_report(df, stats)
    write_video_script(stats)
    print(json.dumps({"rows": len(df), "output": str(OUTPUT_DIR), "database": str(DATA_DIR / "loneliness_risk.db")}, indent=2))


if __name__ == "__main__":
    main()
