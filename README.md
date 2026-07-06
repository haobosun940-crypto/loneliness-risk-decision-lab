# Loneliness & Risk Decision Lab

This project is an English, full-stack research package for the question:

> Among late adolescents and emerging adults in digitally mediated school and college communities, how does loneliness predict immediate-reward preference, impulsive spending, risky choice, and conflict-response style, and does social connectedness buffer the association?

## Research Boundary

- Broad field: social psychology and behavioral decision science
- Specific population: late adolescents and emerging adults aged 16-24
- Specific variable: loneliness and perceived social connectedness
- Specific outcome: Risk Decision Index from delay, spending, risk, and conflict tasks
- Specific context: digitally mediated peer networks in school and college settings

## Deliverables

- Website and API: `server.py`, `static/`, SQLite database in `data/loneliness_risk.db`
- Paper-style PDF: `outputs/loneliness_risk_research_paper.pdf`
- Editable Word report: `outputs/loneliness_risk_research_report.docx`
- Excel workbook: `outputs/loneliness_risk_research_workbook.xlsx`
- Presentation deck: `outputs/loneliness_risk_research_deck.pptx`
- Narrated video: `outputs/loneliness_risk_intro_video.mp4`
- Survey QR: `assets/questionnaire_qr.png`
- Stata-ready script: `data/stata_analysis.do`
- Synthetic pilot data: `data/synthetic_participants.csv`

## Run the Website

```bash
python3 server.py
```

Open:

```text
http://127.0.0.1:8765
```

The questionnaire link is:

```text
http://localhost:8765/survey
```

## Site Map

- `/` - product-grade research homepage
- `/survey` - public questionnaire and personal risk-decision profile
- `/dashboard` - live database preview, QR code, CSV export, and statistical cockpit
- `/research` - research workflow, model outputs, ANOVA, OLS, and interpretation
- `/evidence` - construct-by-construct literature and public-data sources
- `/downloads` - PDF paper, Word report, PPTX deck, XLSX workbook, video, CSV export, and full package
- `/contact` - FAQ and project contact information

## Public Deployment

GitHub repository:

```text
https://github.com/haobosun940-crypto/loneliness-risk-decision-lab
```

This folder is ready for a Render web-service deployment through `render.yaml`.

1. Push this project folder to a GitHub repository.
2. Open Render, choose **New +** then **Blueprint**, and connect the repository.
3. Render will read `render.yaml`, build with `python -m compileall server.py`, and start with `python server.py`.
4. After deployment, use the Render HTTPS URL as the public questionnaire link:

```text
https://your-render-service.onrender.com/survey
```

Render Blueprint deeplink:

```text
https://dashboard.render.com/blueprint/new?repo=https://github.com/haobosun940-crypto/loneliness-risk-decision-lab
```

The default Render free deployment stores live submissions in SQLite on the service filesystem. This is acceptable for a demo, but filesystem data can be lost on rebuilds. For a longer real data-collection run, upgrade the service to a paid plan with a persistent disk and set:

```text
LONELINESS_DB_PATH=/var/data/loneliness_risk.db
```

For short classroom collection without a permanent deployment, run the site locally and expose it with Cloudflare Tunnel:

```bash
python3 server.py
cloudflared tunnel --url http://127.0.0.1:8765
```

The tunnel will print a temporary `https://*.trycloudflare.com` URL. Keep both commands running while classmates are submitting responses.

Use the printed tunnel domain plus `/survey` as the public questionnaire URL.

## Data Disclosure

The seeded data are `synthetic_pilot` rows generated for reproducible demonstration. They are not human-subject observations and should not be presented as collected participant data.

Live submissions entered through the website are stored separately in the `live_responses` table with `source_type = live_submission`.

## Scoring

The Risk Decision Index is:

```text
0.35 * Immediate Reward Bias
+ 0.25 * Impulsive Spending Score
+ 0.25 * High-Risk Choice Score
+ 0.15 * Conflict Defense Score
```

All component scores are scaled from 0 to 100.

## Ethics Note

The website is an educational research prototype, not a clinical diagnostic tool. Before collecting real data for a formal study, add consent language, remove unnecessary identifiers, obtain mentor or institutional review, and keep synthetic and live data clearly separated.
