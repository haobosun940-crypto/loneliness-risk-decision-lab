#!/usr/bin/env python3
"""Build the expanded paper-style PDF for the loneliness risk project."""

from __future__ import annotations

import json
from pathlib import Path
from xml.sax.saxutils import escape

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Table, TableStyle


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
ASSET_DIR = ROOT / "assets"
OUTPUT_DIR = ROOT / "outputs"
PDF_PATH = OUTPUT_DIR / "loneliness_risk_research_paper.pdf"


def load_json(name: str):
    return json.loads((DATA_DIR / name).read_text(encoding="utf-8"))


def p(text: str, style) -> Paragraph:
    return Paragraph(escape(text), style)


def rich(text: str, style) -> Paragraph:
    return Paragraph(text, style)


def format_p(value: float) -> str:
    return "<.001" if value < 0.001 else f"{value:.3f}"


def header_footer(canvas, doc) -> None:
    canvas.saveState()
    canvas.setFont("Helvetica", 8.8)
    canvas.setFillColor(colors.HexColor("#5D6B7C"))
    canvas.drawString(0.65 * inch, 0.42 * inch, "Loneliness, Social Connection, and Risk Decisions")
    canvas.drawRightString(7.85 * inch, 0.42 * inch, f"Page {doc.page}")
    canvas.restoreState()


def table_style(header: str = "#2563EB", font_size: float = 8.8) -> TableStyle:
    return TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(header)),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), font_size),
            ("LEADING", (0, 0), (-1, -1), font_size + 2.6),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#D5E4F2")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F3FAFF")]),
            ("LEFTPADDING", (0, 0), (-1, -1), 5),
            ("RIGHTPADDING", (0, 0), (-1, -1), 5),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ]
    )


def table_cell(value, font_size: float, is_header: bool = False) -> Paragraph:
    style = ParagraphStyle(
        name=f"TableCell-{font_size}-{is_header}",
        fontName="Helvetica-Bold" if is_header else "Helvetica",
        fontSize=font_size,
        leading=font_size + 2.4,
        textColor=colors.white if is_header else colors.black,
        alignment=TA_LEFT,
        wordWrap="CJK",
    )
    return Paragraph(escape(str(value)), style)


def build_styles():
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="PaperTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=22,
            leading=26,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#102033"),
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Subtitle",
            parent=styles["BodyText"],
            fontSize=10.5,
            leading=14.2,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#5D6B7C"),
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Section",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=15.5,
            leading=18.5,
            textColor=colors.HexColor("#1D4ED8"),
            spaceBefore=8,
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Subsection",
            parent=styles["Heading3"],
            fontName="Helvetica-Bold",
            fontSize=12.2,
            leading=15,
            textColor=colors.HexColor("#102033"),
            spaceBefore=6,
            spaceAfter=3,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Body",
            parent=styles["BodyText"],
            fontSize=10.2,
            leading=13.2,
            alignment=TA_JUSTIFY,
            spaceAfter=3,
        )
    )
    styles.add(
        ParagraphStyle(
            name="BodySmall",
            parent=styles["BodyText"],
            fontSize=9.0,
            leading=11.3,
            alignment=TA_LEFT,
            spaceAfter=1.0,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Caption",
            parent=styles["BodyText"],
            fontSize=8.6,
            leading=10.4,
            textColor=colors.HexColor("#5D6B7C"),
            spaceAfter=4,
        )
    )
    return styles


def add_table(story, rows, widths, header="#2563EB", font_size=8.8):
    wrapped_rows = [
        [table_cell(cell, font_size, row_idx == 0) for cell in row]
        for row_idx, row in enumerate(rows)
    ]
    table = Table(wrapped_rows, colWidths=widths, repeatRows=1)
    table.setStyle(table_style(header, font_size))
    story.append(table)


def image(path: str, width: float, height: float) -> Image:
    return Image(str(ASSET_DIR / path), width=width, height=height)


def build_pdf() -> None:
    stats = load_json("stats_summary.json")
    sources = load_json("sources.json")
    config = load_json("study_config.json")
    df = pd.read_csv(DATA_DIR / "synthetic_participants.csv")

    styles = build_styles()
    doc = SimpleDocTemplate(
        str(PDF_PATH),
        pagesize=letter,
        rightMargin=0.55 * inch,
        leftMargin=0.55 * inch,
        topMargin=0.52 * inch,
        bottomMargin=0.56 * inch,
    )
    story = []

    story.append(rich("Loneliness, Social Connection, and Risk Decisions", styles["PaperTitle"]))
    story.append(
        p(
            "A quantitative psychology and statistics study of immediate rewards, impulsive spending, risky choices, and conflict-response style among late adolescents and emerging adults.",
            styles["Subtitle"],
        )
    )
    story.append(
        p(
            "Author format: student research system prototype. Data status: synthetic pilot sample plus separated live submissions. Website component: public questionnaire, scoring algorithm, SQLite database, dashboard, QR link, workbook, slide deck, and video script.",
            styles["BodySmall"],
        )
    )

    story.append(rich("Abstract", styles["Section"]))
    story.append(
        p(
            "This paper reports a complete research design and pilot analysis for the question of whether loneliness predicts risk-oriented decision making. The specific population is late adolescents and emerging adults, especially high school students, college students, and early-career young adults whose peer relationships are partly mediated by digital communication. The main psychological predictors are perceived loneliness and perceived social connectedness. The outcome is a composite Risk Decision Index built from four behavioral domains: preference for immediate rewards, impulsive spending, high-risk choices, and defensive responses to interpersonal conflict. The current dataset contains 420 synthetic pilot observations that are clearly labeled as demonstration data. The same system also stores live questionnaire submissions separately so future analyses can be updated with real participants. In the synthetic pilot, internal consistency is strong for the loneliness battery and social-connection battery, the ANOVA comparing loneliness tertiles is large, and the regression model shows a positive loneliness coefficient with a negative social-connection coefficient. The results should be interpreted as an educational, reproducible demonstration rather than as clinical diagnosis or final causal evidence.",
            styles["Body"],
        )
    )
    story.append(rich("<b>Keywords:</b> loneliness; social connectedness; risk decision making; delay discounting; impulsive spending; ANOVA; OLS regression; adolescent psychology", styles["BodySmall"]))

    story.append(rich("1. Background and Theoretical Motivation", styles["Section"]))
    story.append(
        p(
            "Loneliness is not simply being alone. In social psychology, loneliness is usually understood as perceived social isolation: a mismatch between desired and actual social connection. This distinction matters because two people can have the same number of contacts but different levels of perceived belonging. Prior loneliness theory suggests that perceived isolation may increase attention to social threat, heighten negative affect, and change the way people interpret ambiguous interpersonal events. These mechanisms are relevant to decision making because risky or impulsive choices often emerge under emotional pressure, social exclusion, and short-term attempts to regain control or belonging.",
            styles["Body"],
        )
    )
    story.append(
        p(
            "The project intentionally combines psychology and statistics. Psychology defines the constructs and mechanisms: loneliness, social connectedness, reward sensitivity, social exclusion, affiliation motives, and conflict interpretation. Statistics turns those constructs into measured variables, checks reliability, estimates group differences, and evaluates whether associations remain after controls. The website is therefore not only a display surface; it is the research instrument, data pipeline, scoring system, and live analysis interface.",
            styles["Body"],
        )
    )

    story.append(rich("2. Research Question and Boundary", styles["Section"]))
    story.append(
        p(
            "The research boundary follows the required formula: broad field plus specific population plus specific variable plus specific outcome plus specific context. The broad field is social psychology and behavioral decision science. The population is late adolescents and emerging adults, approximately ages 16 to 24. The core predictor is loneliness, examined together with social connectedness as a possible buffer. The outcome is the Risk Decision Index. The context is digitally mediated peer networks in school, college, and early-career communities.",
            styles["Body"],
        )
    )
    add_table(
        story,
        [
            ["Boundary element", "Operational definition in this project"],
            ["Broad field", "Social psychology, behavioral decision science, and applied statistics."],
            ["Specific population", "Late adolescents and emerging adults, with emphasis on student and young-adult peer networks."],
            ["Specific variable", "Loneliness score from a seven-item custom battery, interpreted with social-connection score."],
            ["Specific result", "Risk Decision Index from delay choices, spending items, risky choices, and conflict responses."],
            ["Specific background", "Digitally mediated peer communication, including platform sessions, messages, face-to-face contact, group activities, and trusted contacts."],
        ],
        [1.55 * inch, 5.25 * inch],
        header="#1D4ED8",
    )

    story.append(rich("3. Hypotheses", styles["Section"]))
    hypotheses = [
        ["H1", "Higher loneliness will be associated with a higher Risk Decision Index."],
        ["H2", "Higher social connectedness will be associated with a lower Risk Decision Index."],
        ["H3", "Loneliness will be positively associated with immediate-reward preference and impulsive spending."],
        ["H4", "Social connectedness will partially buffer risk by reducing conflict-defense responses and short-horizon choices."],
        ["H5", "The effect pattern will remain visible after controlling for age, stress, sleep, and platform-session intensity."],
    ]
    add_table(story, [["Hypothesis", "Prediction"]] + hypotheses, [0.75 * inch, 6.05 * inch], header="#0F766E")

    story.append(rich("4. Population, Sampling, and Data Status", styles["Section"]))
    story.append(
        p(
            f"The synthetic pilot contains n={stats['n']} rows. It is designed to represent the target study population across age, student status, platform use, messaging frequency, in-person contact, trusted-contact count, stress, and sleep. These rows are not presented as collected human-subject observations. They are a reproducible pilot dataset that lets the full system be tested before classmates or outside participants submit responses. Live submissions entered through the website are stored in a separate database table with source_type equal to live_submission.",
            styles["Body"],
        )
    )
    add_table(
        story,
        [
            ["Sample feature", "Purpose"],
            ["Age range", "Focuses the study on late adolescence and emerging adulthood, a period with active peer-network development."],
            ["Student or early-career status", "Captures school, college, and young-adult social contexts where peer connection can shape decisions."],
            ["Digital contact indicators", "Measures platform sessions, messages, and online interaction intensity."],
            ["Offline connection indicators", "Measures in-person conversations, shared meals or events, group activities, and trusted contacts."],
            ["Stress and sleep controls", "Reduces the chance that loneliness is simply standing in for general strain or low recovery."],
        ],
        [1.55 * inch, 5.25 * inch],
        header="#2563EB",
    )

    story.append(rich("5. Measurement and Experiment Design", styles["Section"]))
    story.append(
        p(
            "The instrument uses both self-report items and small choice tasks. The loneliness battery includes seven items scored from 1 to 5 and transformed to a 0-100 scale. The social-connection battery includes six items, also transformed to 0-100. Behavioral tasks then measure four decision domains. Delay-choice items ask participants to choose between an immediate smaller reward and a later larger reward. Spending items measure emotional and affiliation-related purchase tendencies. Risk-choice items present safe versus uncertain options. Conflict-response items measure withdrawal, escalation, rejection interpretation, and avoidance when interpersonal ambiguity occurs.",
            styles["Body"],
        )
    )
    constructs = config.get("questionnaire", {}).get("constructs", [])
    construct_rows = [["Construct", "Measurement logic"]]
    for item in constructs[:8]:
        label = item.split("(")[0].strip()
        construct_rows.append([label, item])
    add_table(story, construct_rows, [1.55 * inch, 5.45 * inch], header="#0284C7", font_size=8.2)
    story.append(
        p(
            "The Risk Decision Index is a weighted composite: 0.35 times immediate-reward bias, 0.25 times impulsive-spending score, 0.25 times high-risk-choice score, and 0.15 times conflict-defense score. This weighting makes reward timing the largest component while still treating consumer behavior, risky choice, and conflict response as essential behavioral manifestations of risk orientation.",
            styles["Body"],
        )
    )
    story.append(image("method_flow.png", width=6.45 * inch, height=3.55 * inch))
    story.append(p("Figure 1. Full research pipeline from question boundary and questionnaire design to scoring, modeling, and public reporting.", styles["Caption"]))

    story.append(rich("6. Statistical Analysis Plan", styles["Section"]))
    story.append(
        p(
            "The statistical workflow has four layers. First, reliability analysis estimates whether the custom loneliness and social-connection item batteries behave consistently. Second, correlations describe the zero-order relationships among loneliness, connectedness, digital contact, offline contact, and risk components. Third, one-way ANOVA compares mean Risk Decision Index across loneliness tertiles. Fourth, OLS regression estimates the unique contribution of loneliness while controlling for social connectedness, stress, age, platform sessions, sleep, and the loneliness-by-connectedness interaction. A logistic tendency model is also included for top-quartile risk classification.",
            styles["Body"],
        )
    )
    add_table(
        story,
        [
            ["Analysis", "Question answered"],
            ["Cronbach alpha", "Do the items within each psychological battery have acceptable internal consistency?"],
            ["Correlation matrix", "Which variables move together before controls are added?"],
            ["ANOVA", "Do low, moderate, and high loneliness groups differ in mean risk score?"],
            ["OLS regression", "Does loneliness still predict risk after accounting for connectedness and controls?"],
            ["Logistic tendency", "Which predictors increase the odds of being in the highest-risk group?"],
        ],
        [1.55 * inch, 5.25 * inch],
        header="#7C3AED",
    )

    story.append(rich("7. Results: Reliability and Group Differences", styles["Section"]))
    alpha = stats["cronbach_alpha"]
    story.append(
        p(
            f"The custom loneliness scale has alpha={alpha['loneliness_custom_7_item']}, and the social-connection scale has alpha={alpha['social_connection_custom_6_item']}. In a student research context, these values indicate that the item batteries are internally coherent in the synthetic pilot. The ANOVA comparing loneliness tertiles yields F({stats['anova']['df_between']}, {stats['anova']['df_within']})={stats['anova']['F']:.2f}, eta squared={stats['anova']['eta_squared']:.3f}, permutation p={stats['anova']['p_permutation']:.4f}. This means the loneliness-group factor accounts for a substantial share of variation in the Risk Decision Index in the pilot.",
            styles["Body"],
        )
    )
    story.append(image("chart_anova_groups.png", width=6.2 * inch, height=3.55 * inch))
    story.append(
        p(
            "Figure 2. The Risk Decision Index rises across low, moderate, and high loneliness tertiles. The figure should be read as a group-level comparison rather than a statement about every individual participant.",
            styles["Caption"],
        )
    )
    group_rows = [["Group", "n", "Loneliness", "Connection", "Risk Index"]]
    for row in stats["group_summary"]:
        group_rows.append(
            [
                row["loneliness_group"],
                str(row["n"]),
                f"{row['loneliness_score']:.1f}",
                f"{row['social_connection_score']:.1f}",
                f"{row['risk_decision_index']:.1f}",
            ]
        )
    add_table(story, group_rows, [1.8 * inch, 0.55 * inch, 1.25 * inch, 1.25 * inch, 1.25 * inch], header="#2563EB")

    story.append(rich("8. Results: Regression Model", styles["Section"]))
    story.append(
        p(
            "The regression model is the most important statistical test because it asks whether loneliness remains associated with risk when other plausible explanations are included. In the synthetic pilot, the standardized loneliness coefficient is positive, while the standardized social-connection coefficient is negative. Stress is also positive, which is theoretically sensible because stress can increase short-term emotion regulation and lower deliberative control. Age and platform sessions are weaker in the model, and the interaction term is exploratory.",
            styles["Body"],
        )
    )
    story.append(image("chart_regression_coefficients.png", width=5.85 * inch, height=2.8 * inch))
    story.append(p("Figure 3. OLS coefficients using standardized predictors. Positive bars indicate higher predicted Risk Decision Index; negative bars indicate lower predicted risk.", styles["Caption"]))

    ols_rows = [["Term", "Estimate", "SE", "t", "p", "95% CI"]]
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
    add_table(story, ols_rows, [2.0 * inch, 0.75 * inch, 0.62 * inch, 0.62 * inch, 0.62 * inch, 1.45 * inch], header="#102033", font_size=8.0)

    story.append(rich("9. Interpreting the Visualizations", styles["Section"]))
    story.append(
        p(
            "The dashboard charts should be explained in class as inferential aids, not decorative graphics. The ANOVA bar chart shows group separation: if loneliness is meaningful for risk decisions, the high-loneliness group should show a higher average Risk Decision Index than the low-loneliness group. The coefficient chart shows controlled associations: loneliness is interpreted after accounting for social connection, stress, age, sleep, platform sessions, and the interaction term. The scatterplot shows individual-level variation, reminding viewers that the relationship is probabilistic rather than deterministic.",
            styles["Body"],
        )
    )
    story.append(image("chart_scatter_loneliness_risk.png", width=6.0 * inch, height=3.15 * inch))
    story.append(p("Figure 4. Individual-level scatterplot showing the loneliness-risk association and the remaining variability around the trend.", styles["Caption"]))
    story.append(image("chart_decision_types.png", width=4.85 * inch, height=1.95 * inch))
    story.append(p("Figure 5. Distribution of profile labels assigned by the scoring algorithm. These labels summarize behavioral tendency and are not diagnostic categories.", styles["Caption"]))

    story.append(rich("10. Psychological Interpretation", styles["Section"]))
    story.append(
        p(
            "The theoretical interpretation is that loneliness may increase risk-oriented choices through short-horizon regulation and social-repair motives. A lonely participant may prefer immediate reward because the present emotional state feels more urgent than a delayed benefit. The same participant may be more vulnerable to impulsive spending when purchases signal inclusion or reduce the feeling of exclusion. In conflict scenarios, loneliness may increase rejection sensitivity, making neutral silence feel more threatening. Social connectedness can buffer these tendencies because trusted contacts, belonging, and face-to-face interaction provide alternative ways to regulate stress and restore social security.",
            styles["Body"],
        )
    )
    story.append(
        p(
            "The statistical model does not prove causality. However, it gives a disciplined way to test whether the pattern is visible in data and whether it remains after controls. This is the value of combining psychological theory with regression and ANOVA: theory explains why the relationship might exist, while statistics checks whether the observed pattern is larger than random noise in the measured sample.",
            styles["Body"],
        )
    )

    story.append(rich("11. Data Collection, Ethics, and Live Deployment", styles["Section"]))
    story.append(
        p(
            "The live website is designed for public questionnaire collection through a QR code or public link. When a participant completes the test, the site calculates a personal score report and stores the response separately from the synthetic pilot data. For a formal study, the questionnaire should include consent language, avoid unnecessary identifiers, clarify that the tool is not clinical diagnosis, and explain how data will be stored and used. If the study is presented in a school or competition context, the report should clearly state which results come from synthetic pilot data and which results come from live classmate submissions.",
            styles["Body"],
        )
    )
    story.append(
        p(
            "The system currently supports three levels of transparency: the source table discloses the literature and public-context references, the workbook separates datasets into tabs, and the website labels live submissions separately from synthetic pilot rows. This separation is important because simulated rows help demonstrate analysis, while real rows are the only basis for claims about actual participants.",
            styles["Body"],
        )
    )

    story.append(rich("12. Applications", styles["Section"]))
    story.append(
        p(
            "The project can be used as a classroom research demonstration, a student social-science presentation, a prototype for a larger survey, or a methodological example of how to transform a broad psychological topic into a measurable statistical design. The most practical application is not to label individuals as risky, but to show how social connection may shape decision environments. If live data eventually confirm the pattern, interventions might focus on strengthening belonging, increasing trusted contacts, and improving conflict clarification before high-stakes choices are made.",
            styles["Body"],
        )
    )

    story.append(rich("13. Limitations", styles["Section"]))
    limitations = [
        "Synthetic pilot data cannot establish real-world prevalence or causal effects.",
        "Self-report items may be affected by social desirability and momentary mood.",
        "The Risk Decision Index is a designed composite, so alternative weighting schemes should be tested.",
        "The current model is cross-sectional and cannot determine whether loneliness causes risk choices or risk choices increase isolation.",
        "Live data should include consent, sample-size planning, and robustness checks before formal claims are made.",
    ]
    for item in limitations:
        story.append(rich(f"- {escape(item)}", styles["Body"]))

    story.append(rich("14. Conclusion", styles["Section"]))
    story.append(
        p(
            "This study demonstrates a complete psychology-and-statistics research pipeline for the question of how loneliness may change risk decision making. The key contribution is not only the written argument but the integrated system: a bounded research question, operationalized measures, a database, a questionnaire, a scoring model, visualizations, and a paper-style analysis. In the synthetic pilot, loneliness is positively associated with the Risk Decision Index, social connectedness is negatively associated with it, and ANOVA shows clear group separation across loneliness tertiles. The next scientific step is to collect real responses through the public website, preserve the separation between synthetic and live data, and rerun the same reliability, ANOVA, correlation, and regression analyses on the live sample.",
            styles["Body"],
        )
    )

    story.append(rich("References", styles["Section"]))
    refs = list(sources)
    refs.append(
        {
            "citation": "World Health Organization. Commission on Social Connection.",
            "url": "https://www.who.int/groups/commission-on-social-connection",
        }
    )
    for idx, src in enumerate(refs, 1):
        story.append(p(f"{idx}. {src['citation']} URL: {src['url']}", styles["BodySmall"]))

    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(PDF_PATH)


if __name__ == "__main__":
    build_pdf()
