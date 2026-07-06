import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const { chromium } = require("playwright");

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const outDir = path.join(root, "output", "playwright");
await fs.mkdir(outDir, { recursive: true });

const systemChrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
let launchOptions = { headless: true };
try {
  await fs.access(systemChrome);
  launchOptions.executablePath = systemChrome;
}
catch {
  // Fall back to Playwright-managed Chromium if it is installed.
}

const browser = await chromium.launch(launchOptions);
const page = await browser.newPage({ viewport: { width: 1440, height: 1100 } });
const messages = [];
page.on("console", (msg) => {
  if (["error", "warning"].includes(msg.type())) messages.push({ type: msg.type(), text: msg.text() });
});
page.on("pageerror", (error) => messages.push({ type: "pageerror", text: error.message }));

const base = (process.env.BASE_URL || "http://127.0.0.1:8765").replace(/\/$/, "");
const routes = [
  ["home", "/"],
  ["survey", "/survey"],
  ["dashboard", "/dashboard"],
  ["research", "/research"],
  ["evidence", "/evidence"],
  ["downloads", "/downloads"],
];
const routeChecks = {};

for (const [name, route] of routes) {
  await page.goto(`${base}${route}`, { waitUntil: "networkidle", timeout: 60000 });
  await page.screenshot({ path: path.join(outDir, `website-${name}.png`), fullPage: true });
  routeChecks[name] = {
    title: await page.title(),
    visibleSections: await page.locator(".page-section.is-route-visible").count(),
    activeNav: await page.locator("nav a.is-active").innerText().catch(() => ""),
  };
}

await page.goto(`${base}/survey`, { waitUntil: "networkidle", timeout: 60000 });
const surveyVisible = await page.locator("#questionnaire").isVisible();
await page.locator("#scoreOnly").click();
await page.locator("#reportOutput").waitFor({ state: "visible", timeout: 10000 });
const profile = await page.locator("#profileType").innerText();
await page.screenshot({ path: path.join(outDir, "website-survey-report.png"), fullPage: true });

await page.goto(`${base}/dashboard`, { waitUntil: "networkidle", timeout: 60000 });
const shareLink = await page.locator("#surveyPublicLink").innerText();
const responseRows = await page.locator("#responsePreview tbody tr").count();

await page.goto(`${base}/downloads`, { waitUntil: "networkidle", timeout: 60000 });
const downloadCards = await page.locator(".download-card").count();

await browser.close();

console.log(JSON.stringify({ profile, surveyVisible, shareLink, responseRows, downloadCards, routeChecks, messages, screenshots: outDir }, null, 2));
