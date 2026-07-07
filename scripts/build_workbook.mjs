import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const dataDir = path.join(root, "data");
const outputDir = path.join(root, "outputs");
const previewDir = path.join(root, "tmp", "spreadsheets", "preview");
const outputPath = path.join(outputDir, "loneliness_risk_research_workbook.xlsx");

function parseCsv(text) {
  const lines = text.trim().split(/\r?\n/);
  return lines.map((line) => line.split(","));
}

function colName(n) {
  let s = "";
  while (n > 0) {
    const m = (n - 1) % 26;
    s = String.fromCharCode(65 + m) + s;
    n = Math.floor((n - m) / 26);
  }
  return s;
}

function rangeAddress(row1, col1, row2, col2) {
  return `${colName(col1)}${row1}:${colName(col2)}${row2}`;
}

function idx(headers, name) {
  const i = headers.indexOf(name);
  if (i < 0) throw new Error(`Missing header ${name}`);
  return i + 1;
}

function styleTitle(range, fill = "#1C2430") {
  range.format = {
    fill,
    font: { bold: true, color: "#FFFFFF", size: 14 },
  };
}

function styleHeader(range, fill = "#243B53") {
  range.format = {
    fill,
    font: { bold: true, color: "#FFFFFF" },
    borders: { preset: "all", style: "thin", color: "#D8DEE6" },
  };
}

function styleTable(range) {
  range.format = {
    borders: { preset: "all", style: "thin", color: "#D8DEE6" },
  };
}

async function writeBlob(filePath, blob) {
  await fs.writeFile(filePath, new Uint8Array(await blob.arrayBuffer()));
}

async function main() {
  await fs.mkdir(outputDir, { recursive: true });
  await fs.mkdir(previewDir, { recursive: true });

  const rawRows = parseCsv(await fs.readFile(path.join(dataDir, "synthetic_participants.csv"), "utf8"));
  const headers = rawRows[0];
  const displayHeaders = headers.map((header) => (header === "participant_id" ? "participant_name" : header));
  const body = rawRows.slice(1).map((row) =>
    row.map((value) => {
      if (value === "") return null;
      const asNum = Number(value);
      return Number.isFinite(asNum) && value.trim() !== "" ? asNum : value;
    }),
  );
  const stats = JSON.parse(await fs.readFile(path.join(dataDir, "stats_summary.json"), "utf8"));
  const sources = JSON.parse(await fs.readFile(path.join(dataDir, "sources.json"), "utf8"));
  const config = JSON.parse(await fs.readFile(path.join(dataDir, "study_config.json"), "utf8"));
  const links = JSON.parse(await fs.readFile(path.join(dataDir, "publication_links.json"), "utf8"));
  const stata = await fs.readFile(path.join(dataDir, "stata_analysis.do"), "utf8");

  const workbook = Workbook.create();
  const dashboard = workbook.worksheets.add("Dashboard");
  const raw = workbook.worksheets.add("Synthetic Raw");
  const processed = workbook.worksheets.add("Processed Scores");
  const models = workbook.worksheets.add("Model Results");
  const corrSheet = workbook.worksheets.add("Correlation Matrix");
  const sourcesSheet = workbook.worksheets.add("Sources");
  const questionnaire = workbook.worksheets.add("Questionnaire");
  const linksSheet = workbook.worksheets.add("Publication Links");
  const stataSheet = workbook.worksheets.add("Stata Notes");

  for (const sheet of [dashboard, raw, processed, models, corrSheet, sourcesSheet, questionnaire, linksSheet, stataSheet]) {
    sheet.showGridLines = false;
  }

  dashboard.getRange("A1:H1").merge();
  dashboard.getRange("A1").values = [["Loneliness, Social Connection, and Risk Decisions"]];
  styleTitle(dashboard.getRange("A1:H1"));
  dashboard.getRange("A2:B2").values = [["Developer", "He Haoze (何昊泽)"]];
  styleTable(dashboard.getRange("A2:B2"));
  dashboard.getRange("A2").format = { fill: "#E6F7F5", font: { bold: true, color: "#0F766E" } };
  dashboard.getRange("B2").format = { fill: "#F7FCFB", font: { bold: true, color: "#0F172A" } };
  dashboard.getRange("A3:B8").values = [
    ["Metric", "Value"],
    ["Synthetic pilot rows", null],
    ["Mean loneliness score", null],
    ["Mean social connection", null],
    ["Mean Risk Decision Index", null],
    ["Loneliness alpha", stats.cronbach_alpha.loneliness_custom_7_item],
  ];
  dashboard.getRange("B4:B7").formulas = [
    [`=COUNTA('Processed Scores'!A2:A${body.length + 1})`],
    [`=AVERAGE('Processed Scores'!D2:D${body.length + 1})`],
    [`=AVERAGE('Processed Scores'!E2:E${body.length + 1})`],
    [`=AVERAGE('Processed Scores'!J2:J${body.length + 1})`],
  ];
  styleHeader(dashboard.getRange("A3:B3"), "#2D6A6A");
  styleTable(dashboard.getRange("A3:B8"));
  dashboard.getRange("B5:B8").format.numberFormat = "0.0";
  dashboard.getRange("B8").format.numberFormat = "0.000";
  dashboard.getRange("A1:A15").format.columnWidthPx = 210;
  dashboard.getRange("B1:B15").format.columnWidthPx = 90;

  const groupStart = 3;
  dashboard.getRange("D2:G2").merge();
  dashboard.getRange("D2").values = [["Group comparison"]];
  styleTitle(dashboard.getRange("D2:G2"), "#456990");
  dashboard.getRange("D3:G6").values = [
    ["Loneliness group", "Mean risk index", "Mean connection", "n"],
    ...stats.group_summary.map((g) => [
      g.loneliness_group,
      g.risk_decision_index,
      g.social_connection_score,
      g.n,
    ]),
  ];
  dashboard.getRange("D1:D24").format.columnWidthPx = 190;
  dashboard.getRange("E1:G24").format.columnWidthPx = 120;
  styleHeader(dashboard.getRange("D3:G3"), "#456990");
  styleTable(dashboard.getRange("D3:G6"));
  const groupChart = dashboard.charts.add("bar", dashboard.getRange("D3:E6"));
  groupChart.title = "Risk Decision Index rises across loneliness tertiles";
  groupChart.hasLegend = false;
  groupChart.yAxis = { numberFormatCode: "0", min: 0, max: 100 };
  groupChart.setPosition("D8", "K24");

  dashboard.getRange("A11:B15").values = [
    ["ANOVA statistic", "Value"],
    ["F", stats.anova.F],
    ["df", `${stats.anova.df_between}, ${stats.anova.df_within}`],
    ["eta squared", stats.anova.eta_squared],
    ["permutation p", stats.anova.p_permutation],
  ];
  styleHeader(dashboard.getRange("A11:B11"), "#B23A48");
  styleTable(dashboard.getRange("A11:B15"));
  dashboard.getRange("B12:B15").format.numberFormat = "0.000";

  dashboard.getRange("A18:B24").values = [
    ["Publication link", "URL or note"],
    ["Current public survey", links.current_public_survey],
    ["Current public site", links.current_public_site],
    ["GitHub repository", links.github_repository],
    ["Render Blueprint", links.render_blueprint],
    ["Expected permanent survey", links.render_expected_survey],
    ["Link status", links.note],
  ];
  styleHeader(dashboard.getRange("A18:B18"), "#0F766E");
  styleTable(dashboard.getRange("A18:B24"));
  dashboard.getRange("B18:B24").format.wrapText = true;
  dashboard.getRange("A18:A24").format.columnWidthPx = 190;
  dashboard.getRange("B18:B24").format.columnWidthPx = 440;

  raw.getRange(rangeAddress(1, 1, rawRows.length, displayHeaders.length)).values = [displayHeaders, ...body];
  styleHeader(raw.getRange(rangeAddress(1, 1, 1, headers.length)), "#1C2430");
  raw.freezePanes.freezeRows(1);
  raw.getRange(rangeAddress(1, 1, Math.min(rawRows.length, 60), headers.length)).format.autofitColumns();

  const processedHeaders = [
    "participant_name",
    "source_type",
    "age",
    "loneliness_score",
    "social_connection_score",
    "immediate_reward_bias",
    "impulsive_spending_score",
    "high_risk_choice_score",
    "conflict_defense_score",
    "risk_decision_index",
    "loneliness_group",
    "decision_type",
  ];
  processed.getRange(rangeAddress(1, 1, 1, processedHeaders.length)).values = [processedHeaders];
  styleHeader(processed.getRange(rangeAddress(1, 1, 1, processedHeaders.length)), "#2D6A6A");
  const processedMap = processedHeaders.map((h) => idx(headers, h === "participant_name" ? "participant_id" : h));
  const formulas = body.map((_, r) => processedMap.map((c) => `='Synthetic Raw'!${colName(c)}${r + 2}`));
  processed.getRange(rangeAddress(2, 1, body.length + 1, processedHeaders.length)).formulas = formulas;
  processed.freezePanes.freezeRows(1);
  processed.getRange(rangeAddress(1, 1, Math.min(body.length + 1, 80), processedHeaders.length)).format.autofitColumns();
  processed.getRange(`D2:J${body.length + 1}`).format.numberFormat = "0.0";

  models.getRange("A1:H1").merge();
  models.getRange("A1").values = [["Regression, classification, and ANOVA results"]];
  styleTitle(models.getRange("A1:H1"));
  const olsRows = [["Term", "Estimate", "SE", "t", "p approx", "CI low", "CI high"]].concat(
    stats.ols.map((r) => [r.term, r.estimate, r.std_error, r.t_stat, r.p_approx, r.ci_low, r.ci_high]),
  );
  models.getRange(rangeAddress(3, 1, 3 + olsRows.length - 1, 7)).values = olsRows;
  styleHeader(models.getRange("A3:G3"), "#456990");
  styleTable(models.getRange(rangeAddress(3, 1, 3 + olsRows.length - 1, 7)));
  models.getRange(`B4:G${3 + olsRows.length - 1}`).format.numberFormat = "0.000";
  models.getRange("A1:A28").format.columnWidthPx = 190;
  models.getRange("B1:G28").format.columnWidthPx = 96;

  const coefChart = models.charts.add("bar", models.getRange(`A5:B${3 + olsRows.length - 1}`));
  coefChart.title = "OLS coefficients for Risk Decision Index";
  coefChart.hasLegend = false;
  coefChart.setPosition("I3", "P20");

  const logitRows = [["Term", "Logit estimate", "Odds ratio", "SE", "z", "p approx"]].concat(
    stats.logit.map((r) => [r.term, r.logit_estimate, r.odds_ratio, r.std_error, r.z_stat, r.p_approx]),
  );
  const logitStart = 15;
  models.getRange(rangeAddress(logitStart, 1, logitStart + logitRows.length - 1, 6)).values = logitRows;
  styleHeader(models.getRange(rangeAddress(logitStart, 1, logitStart, 6)), "#D98E04");
  styleTable(models.getRange(rangeAddress(logitStart, 1, logitStart + logitRows.length - 1, 6)));
  models.getRange(rangeAddress(logitStart + 1, 2, logitStart + logitRows.length - 1, 6)).format.numberFormat = "0.000";

  models.getRange("H23:K28").values = [
    ["ANOVA", "Value", "", ""],
    ["F", stats.anova.F, "", ""],
    ["df between", stats.anova.df_between, "", ""],
    ["df within", stats.anova.df_within, "", ""],
    ["eta squared", stats.anova.eta_squared, "", ""],
    ["permutation p", stats.anova.p_permutation, "", ""],
  ];
  styleHeader(models.getRange("H23:K23"), "#B23A48");
  styleTable(models.getRange("H23:K28"));

  const corr = stats.correlation_matrix;
  const corrNames = Object.keys(corr);
  const corrRows = [["Variable", ...corrNames]].concat(corrNames.map((r) => [r, ...corrNames.map((c) => corr[c][r])]));
  corrSheet.getRange(rangeAddress(1, 1, corrRows.length, corrRows[0].length)).values = corrRows;
  styleHeader(corrSheet.getRange(rangeAddress(1, 1, 1, corrRows[0].length)), "#1C2430");
  styleTable(corrSheet.getRange(rangeAddress(1, 1, corrRows.length, corrRows[0].length)));
  corrSheet.getRange(rangeAddress(2, 2, corrRows.length, corrRows[0].length)).format.numberFormat = "0.000";
  corrSheet.getRange(rangeAddress(1, 1, corrRows.length, corrRows[0].length)).format.autofitColumns();

  const sourceRows = [["ID", "Type", "Citation", "URL", "Used for"]].concat(
    sources.map((s) => [s.id, s.type, s.citation, s.url, s.used_for]),
  );
  sourcesSheet.getRange(rangeAddress(1, 1, sourceRows.length, 5)).values = sourceRows;
  styleHeader(sourcesSheet.getRange("A1:E1"), "#2D6A6A");
  styleTable(sourcesSheet.getRange(rangeAddress(1, 1, sourceRows.length, 5)));
  sourcesSheet.getRange("C:E").format.wrapText = true;
  sourcesSheet.getRange("A1:E20").format.autofitColumns();

  const qRows = [
    ["Section", "Content"],
    ["Research question", config.questionnaire.research_question],
    ...Object.entries(config.questionnaire.topic_formula).map(([k, v]) => [k.replaceAll("_", " "), v]),
    ["Disclosure", config.questionnaire.disclosure],
    ...config.questionnaire.hypotheses.map((h) => ["Hypothesis", h]),
    ...config.questionnaire.constructs.map((c) => ["Construct", c]),
  ];
  questionnaire.getRange(rangeAddress(1, 1, qRows.length, 2)).values = qRows;
  styleHeader(questionnaire.getRange("A1:B1"), "#456990");
  styleTable(questionnaire.getRange(rangeAddress(1, 1, qRows.length, 2)));
  questionnaire.getRange("B:B").format.wrapText = true;
  questionnaire.getRange("A1:B40").format.autofitColumns();

  const linkRows = [
    ["Asset", "URL", "Use"],
    ["Developer", "He Haoze (何昊泽)", "Visible authorship and project developer credit."],
    ["Current public site", links.current_public_site, "Public homepage while the local server and tunnel remain running."],
    ["Current public survey", links.current_public_survey, "Share this with classmates for immediate survey collection."],
    ["GitHub repository", links.github_repository, "Source code, outputs, and reproducibility record."],
    ["Render Blueprint", links.render_blueprint, "Permanent deployment setup for a stable public link."],
    ["Expected permanent survey", links.render_expected_survey, "Use this route after Render deployment is live."],
    ["Local survey", links.local_survey, "Local development and classroom demo on the same machine."],
    ["Verification date", links.last_verified, "Last checked by the project build workflow."],
  ];
  linksSheet.getRange(rangeAddress(1, 1, linkRows.length, 3)).values = linkRows;
  styleHeader(linksSheet.getRange("A1:C1"), "#0F766E");
  styleTable(linksSheet.getRange(rangeAddress(1, 1, linkRows.length, 3)));
  linksSheet.getRange("B:C").format.wrapText = true;
  linksSheet.getRange("A1:A20").format.columnWidthPx = 190;
  linksSheet.getRange("B1:B20").format.columnWidthPx = 460;
  linksSheet.getRange("C1:C20").format.columnWidthPx = 380;

  const stataLines = [["Line", "Command"]].concat(stata.split(/\r?\n/).map((line, i) => [i + 1, line]));
  stataSheet.getRange(rangeAddress(1, 1, stataLines.length, 2)).values = stataLines;
  styleHeader(stataSheet.getRange("A1:B1"), "#B23A48");
  styleTable(stataSheet.getRange(rangeAddress(1, 1, stataLines.length, 2)));
  stataSheet.getRange("B:B").format.wrapText = true;
  stataSheet.getRange("A1:B80").format.autofitColumns();

  const inspect = await workbook.inspect({
    kind: "sheet,table,drawing",
    maxChars: 6000,
    tableMaxRows: 8,
    tableMaxCols: 8,
  });
  console.log(inspect.ndjson);

  const errors = await workbook.inspect({
    kind: "match",
    searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
    options: { useRegex: true, maxResults: 200 },
    summary: "formula error scan",
  });
  console.log(errors.ndjson);

  for (const name of ["Dashboard", "Synthetic Raw", "Processed Scores", "Model Results", "Correlation Matrix", "Sources", "Questionnaire", "Publication Links", "Stata Notes"]) {
    const preview = await workbook.render({ sheetName: name, autoCrop: "all", scale: 1, format: "png" });
    await writeBlob(path.join(previewDir, `${name.replaceAll(" ", "_")}.png`), preview);
  }

  const output = await SpreadsheetFile.exportXlsx(workbook);
  await output.save(outputPath);
  console.log(JSON.stringify({ outputPath, previewDir }));
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
