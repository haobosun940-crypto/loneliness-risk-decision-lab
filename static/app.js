const appState = {
  language: "en",
  config: null,
  summary: null,
  charts: {},
};

const routeByPath = {
  "/": "home",
  "/index.html": "home",
  "/survey": "survey",
  "/dashboard": "dashboard",
  "/research": "research",
  "/evidence": "evidence",
  "/downloads": "downloads",
  "/contact": "contact",
};

const i18n = {
  en: {
    subtitle: "Quantifying social connection, reward timing, conflict response, and risk preference",
    navHome: "Home",
    navDashboard: "Dashboard",
    navQuestionnaire: "Survey",
    navResearch: "Research",
    navData: "Data Lab",
    navEvidence: "Evidence",
    navDownloads: "Downloads",
    navFaq: "FAQ",
    liveSystem: "Live research system",
    methodTag: "Psychology + statistics",
    eyebrow: "Behavioral decision science research system",
    headline: "Loneliness, connection, and risky decisions",
    lead: "A brighter research interface for testing how social connection predicts immediate rewards, impulsive spending, risky choices, and conflict-response style.",
    hypothesisLabel: "Primary hypothesis",
    hypothesisText: "Higher loneliness predicts a higher Risk Decision Index, while social connection buffers the pattern.",
    cockpitKicker: "Quant cockpit",
    cockpitTitle: "From social signals to risk estimates",
    startTest: "Start the decision test",
    startTestShort: "Start Test",
    exportCsv: "Export CSV",
    openStatistics: "Open statistics",
    openWorkflow: "Open workflow map",
    openCharts: "Open model charts",
    pulseEyebrow: "Research pulse",
    pulseTitle: "Why this topic belongs at the intersection of psychology and statistics.",
    metricSample: "Synthetic pilot n",
    metricLive: "Live submissions",
    metricAlpha: "Loneliness alpha",
    pipelineEyebrow: "End-to-end research workflow",
    pipelineTitle: "Four agents turn a psychology question into a statistical system.",
    agent1: "Data Intake Agent",
    agent1Text: "Separates synthetic pilot rows, live submissions, and public benchmark notes inside SQLite.",
    agent2: "Scoring Agent",
    agent2Text: "Converts questionnaire items and choices into 0-100 psychological and behavioral indices.",
    agent3: "Modeling Agent",
    agent3Text: "Runs reliability, correlation, OLS, logistic tendency, and ANOVA summaries.",
    agent4: "Report Agent",
    agent4Text: "Feeds the dashboard, participant report, PDF paper, workbook, slide deck, and video script.",
    resultEyebrow: "Model outputs",
    resultTitle: "The synthetic pilot shows a positive loneliness-risk gradient.",
    modelTable: "OLS model table",
    modelNote: "Standardized predictors estimate the composite Risk Decision Index.",
    testEyebrow: "Interactive questionnaire",
    testTitle: "Complete the risk-decision test and generate a profile.",
    testNote: "This is an educational research instrument, not a mental-health diagnosis. Submitted responses are stored locally as live submissions.",
    sectionSignals: "Social signals",
    sectionLoneliness: "Loneliness and connection battery",
    sectionChoices: "Choice tasks",
    submitSave: "Save and score",
    scoreOnly: "Score without saving",
    profileEyebrow: "Personal profile",
    dataEyebrow: "Database preview",
    dataTitle: "Synthetic pilot data, live submissions, and exportable tables remain separated.",
    shareTitle: "Share-ready questionnaire",
    shareText: "The QR code and link are generated from the current website address.",
    copyLink: "Copy link",
    copiedLink: "Copied",
    evidenceEyebrow: "Evidence base",
    evidenceTitle: "Every construct is tied to a measurement or mechanism source.",
    footer: "Synthetic pilot data are disclosed; live data are local to this server.",
  },
  zh: {
    subtitle: "量化社交连接、即时奖励、冲突反应与风险偏好",
    navHome: "首页",
    navDashboard: "数据看板",
    navQuestionnaire: "问卷",
    navResearch: "研究设计",
    navData: "数据实验室",
    navEvidence: "文献依据",
    navDownloads: "下载",
    navFaq: "FAQ",
    liveSystem: "实时研究系统",
    methodTag: "心理学 + 统计学",
    eyebrow: "行为决策科学研究系统",
    headline: "孤独感、连接感与风险选择",
    lead: "一个更明亮的研究界面，用来测试社交连接如何预测即时奖励、冲动消费、高风险选择和冲突反应。",
    hypothesisLabel: "核心假设",
    hypothesisText: "更高的孤独感会预测更高的风险决策指数，而社交连接感会起到缓冲作用。",
    cockpitKicker: "量化驾驶舱",
    cockpitTitle: "从社交信号到风险估计",
    startTest: "开始决策测试",
    startTestShort: "Start Test",
    exportCsv: "导出 CSV",
    openStatistics: "展开统计图",
    openWorkflow: "展开研究流程",
    openCharts: "展开模型图表",
    pulseEyebrow: "研究引入",
    pulseTitle: "为什么这个主题属于心理学与统计学的交叉。",
    metricSample: "模拟试点样本 n",
    metricLive: "真实提交数",
    metricAlpha: "孤独量表 alpha",
    pipelineEyebrow: "端到端研究流程",
    pipelineTitle: "四个模块把心理学问题变成统计系统。",
    agent1: "数据收集 Agent",
    agent1Text: "在 SQLite 中区分 synthetic pilot、live submissions 和 public benchmark。",
    agent2: "评分 Agent",
    agent2Text: "把问卷和选择任务转换为 0-100 的心理与行为指标。",
    agent3: "建模 Agent",
    agent3Text: "运行信度、相关、OLS、logistic 倾向模型和 ANOVA 摘要。",
    agent4: "报告 Agent",
    agent4Text: "驱动仪表盘、个人报告、PDF 论文、Excel、PPT 和视频脚本。",
    resultEyebrow: "模型输出",
    resultTitle: "模拟试点数据显示孤独感越高，风险决策指数越高。",
    modelTable: "OLS 模型表",
    modelNote: "用标准化预测变量估计综合风险决策指数。",
    testEyebrow: "互动问卷",
    testTitle: "完成风险决策测试并生成个人画像。",
    testNote: "这是教育研究工具，不是心理健康诊断。提交的数据会作为 live submissions 存在本地数据库中。",
    sectionSignals: "社交信号",
    sectionLoneliness: "孤独感与连接感量表",
    sectionChoices: "选择任务",
    submitSave: "保存并评分",
    scoreOnly: "仅评分不保存",
    profileEyebrow: "个人画像",
    dataEyebrow: "数据库预览",
    dataTitle: "模拟试点数据、真实提交和可导出表格保持分离。",
    shareTitle: "可分享问卷",
    shareText: "二维码和链接会根据当前网站地址自动生成。",
    copyLink: "复制链接",
    copiedLink: "已复制",
    evidenceEyebrow: "证据基础",
    evidenceTitle: "每个变量都对应测量或机制来源。",
    footer: "Synthetic pilot 数据已明确标注；live data 保存在本地服务器。",
  },
};

const itemText = {
  en: {
    lq: [
      "I often feel that I lack close social contact.",
      "I feel left out of important conversations.",
      "I wish I had more people I could rely on.",
      "I often feel disconnected even when I am online.",
      "I feel that my relationships are less satisfying than I want.",
      "I feel unseen in my peer group.",
      "I spend more time alone than I would prefer.",
    ],
    sci: [
      "I have people I can contact when I need advice.",
      "I feel included in at least one group or community.",
      "My online interactions usually make me feel connected.",
      "I can talk honestly with someone when I feel stressed.",
      "I have regular face-to-face contact with people I trust.",
      "I feel that I belong in my current school, work, or social setting.",
    ],
  },
  zh: {
    lq: [
      "我经常觉得缺少亲密的社交联系。",
      "我觉得自己被排除在重要对话之外。",
      "我希望有更多可以依靠的人。",
      "即使在线上，我也常常觉得和别人 disconnected。",
      "我觉得目前的人际关系没有达到我的期待。",
      "我在同伴群体中常常觉得自己不被看见。",
      "我独处的时间比我希望的更多。",
    ],
    sci: [
      "需要建议时，我有人可以联系。",
      "我觉得自己属于至少一个群体或社区。",
      "我的线上互动通常会让我感觉更有连接感。",
      "压力大时，我可以和某个人坦诚交流。",
      "我会定期和信任的人面对面交流。",
      "我觉得自己属于当前的学校、工作或社交环境。",
    ],
  },
};

const taskText = {
  en: {
    now: "Now",
    later: "Later",
    safe: "Safe",
    risky: "Risky",
    low: "Low",
    high: "High",
    delay: [
      ["$20 today or $35 in 30 days?", "$20 today", "$35 later"],
      ["$15 today or $28 in 14 days?", "$15 today", "$28 later"],
      ["$40 today or $70 in 60 days?", "$40 today", "$70 later"],
      ["$8 today or $18 in 7 days?", "$8 today", "$18 later"],
      ["$55 today or $95 in 90 days?", "$55 today", "$95 later"],
      ["$30 today or $45 in 21 days?", "$30 today", "$45 later"],
    ],
    risk: [
      ["Keep a guaranteed small gain or try a larger uncertain gain?", "Guaranteed", "Uncertain"],
      ["Use a familiar route or take a shortcut with a chance of delay?", "Familiar", "Shortcut"],
      ["Choose a stable project or a bold project with uncertain reward?", "Stable", "Bold"],
      ["Follow a known study plan or gamble on a last-minute strategy?", "Known", "Gamble"],
      ["Save the money or invest in a volatile opportunity?", "Save", "Volatile"],
    ],
    spend: [
      "I would buy something quickly if it made me feel socially included.",
      "I make unplanned purchases when I feel emotionally low.",
      "Limited-time online deals are hard for me to ignore.",
      "I would spend money to avoid feeling left out.",
      "I later regret purchases made during stressful or lonely moments.",
    ],
    conflict: [
      "When a friend does not reply, I withdraw instead of checking in calmly.",
      "In conflict, I send a reactive message before thinking it through.",
      "I avoid direct conversation even when clarification would help.",
      "I interpret neutral silence as rejection.",
      "I escalate tone when I feel excluded.",
    ],
  },
  zh: {
    now: "现在",
    later: "以后",
    safe: "安全",
    risky: "风险",
    low: "低",
    high: "高",
    delay: [
      ["今天拿 20 美元，还是 30 天后拿 35 美元？", "今天 20", "以后 35"],
      ["今天拿 15 美元，还是 14 天后拿 28 美元？", "今天 15", "以后 28"],
      ["今天拿 40 美元，还是 60 天后拿 70 美元？", "今天 40", "以后 70"],
      ["今天拿 8 美元，还是 7 天后拿 18 美元？", "今天 8", "以后 18"],
      ["今天拿 55 美元，还是 90 天后拿 95 美元？", "今天 55", "以后 95"],
      ["今天拿 30 美元，还是 21 天后拿 45 美元？", "今天 30", "以后 45"],
    ],
    risk: [
      ["选择确定的小收益，还是尝试更大的不确定收益？", "确定", "不确定"],
      ["走熟悉路线，还是走可能延误的捷径？", "熟悉", "捷径"],
      ["选择稳定项目，还是回报不确定的大胆项目？", "稳定", "大胆"],
      ["按计划学习，还是赌一个临时策略？", "计划", "赌一把"],
      ["存钱，还是投入波动较大的机会？", "存钱", "波动机会"],
    ],
    spend: [
      "如果能让我感觉融入群体，我会快速购买某件东西。",
      "情绪低落时，我会有计划外消费。",
      "限时优惠很难让我忽视。",
      "为了避免被排除在外，我愿意花钱。",
      "我会后悔在压力或孤独时做出的消费。",
    ],
    conflict: [
      "朋友不回复时，我会退缩，而不是冷静确认。",
      "冲突中，我会先发一条反应强烈的信息。",
      "即使澄清有帮助，我也会避免直接沟通。",
      "我会把中性的沉默理解成拒绝。",
      "当我觉得被排除时，我的语气会升级。",
    ],
  },
};

function t(key) {
  return i18n[appState.language][key] ?? i18n.en[key] ?? key;
}

function currentRoute() {
  return routeByPath[window.location.pathname] ?? "home";
}

function applyRoute() {
  const route = currentRoute();
  document.body.dataset.route = route;
  document.body.classList.add("route-mode");
  document.querySelectorAll("[data-pages]").forEach((section) => {
    const pages = section.dataset.pages.split(/\s+/);
    section.classList.toggle("is-route-visible", pages.includes(route));
  });
  document.querySelectorAll("[data-route-link]").forEach((link) => {
    link.classList.toggle("is-active", link.dataset.routeLink === route);
  });
  const testSection = document.querySelector("#questionnaire");
  if (testSection) {
    testSection.classList.toggle("is-collapsed", route !== "survey");
  }
  requestAnimationFrame(() => {
    Object.values(appState.charts).forEach((chart) => chart.resize());
  });
}

async function getJson(url, options) {
  const response = await fetch(url, options);
  if (!response.ok) throw new Error(`${response.status} ${response.statusText}`);
  return response.json();
}

function applyLanguage() {
  document.documentElement.lang = appState.language;
  document.querySelectorAll("[data-i18n]").forEach((el) => {
    el.textContent = t(el.dataset.i18n);
  });
  const languageLabel = document.querySelector("#languageToggle span");
  if (languageLabel) languageLabel.textContent = appState.language === "en" ? "中文" : "EN";
  renderLikert();
  renderTasks();
  if (appState.summary) renderCharts(appState.summary);
  if (window.lucide) window.lucide.createIcons();
  applyRoute();
}

function renderLikert() {
  const grid = document.querySelector("#likertGrid");
  const lq = itemText[appState.language].lq;
  const sci = itemText[appState.language].sci;
  const rows = [];
  lq.forEach((text, idx) => rows.push({ name: `lq${idx + 1}`, text, value: 3 }));
  sci.forEach((text, idx) => rows.push({ name: `sci${idx + 1}`, text, value: 3 }));
  grid.innerHTML = rows
    .map(
      (item) => `
      <label class="likert-item">
        <span>${item.text}</span>
        <select name="${item.name}">
          ${[1, 2, 3, 4, 5].map((v) => `<option value="${v}" ${v === item.value ? "selected" : ""}>${v}</option>`).join("")}
        </select>
      </label>`,
    )
    .join("");
}

function renderTasks() {
  const grid = document.querySelector("#choiceTasks");
  const copy = taskText[appState.language];
  const html = [];
  copy.delay.forEach((task, idx) => {
    html.push(choiceTask(`delay_immediate_choice_${idx + 1}`, task[0], task[1], task[2], 1));
  });
  copy.risk.forEach((task, idx) => {
    html.push(choiceTask(`risk_choice_${idx + 1}`, task[0], task[1], task[2], 0));
  });
  copy.spend.forEach((text, idx) => {
    html.push(rangeTask(`spend${idx + 1}`, text, copy.low, copy.high, 3));
  });
  copy.conflict.forEach((text, idx) => {
    html.push(rangeTask(`conflict_defense_${idx + 1}`, text, copy.low, copy.high, 3));
  });
  grid.innerHTML = html.join("");
  grid.querySelectorAll(".choice-buttons button").forEach((button) => {
    button.addEventListener("click", () => {
      const task = button.closest(".task");
      task.querySelectorAll("button").forEach((b) => b.classList.remove("active"));
      button.classList.add("active");
      task.querySelector("input[type=hidden]").value = button.dataset.value;
    });
  });
  grid.querySelectorAll("input[type=range]").forEach(bindRangeLabel);
}

function choiceTask(name, prompt, left, right, defaultValue) {
  return `
    <div class="task">
      <p>${prompt}</p>
      <input type="hidden" name="${name}" value="${defaultValue}">
      <div class="choice-buttons">
        <button type="button" data-value="0" class="${defaultValue === 0 ? "active" : ""}">${left}</button>
        <button type="button" data-value="1" class="${defaultValue === 1 ? "active" : ""}">${right}</button>
      </div>
    </div>`;
}

function rangeTask(name, prompt, low, high, value) {
  return `
    <label class="task">
      <p>${prompt}</p>
      <input name="${name}" type="range" min="1" max="5" value="${value}">
      <span class="range-value">${low} ${value} ${high}</span>
    </label>`;
}

function bindRangeLabel(input) {
  const update = () => {
    const label = input.parentElement.querySelector(".range-value");
    if (label) label.textContent = input.value;
  };
  input.addEventListener("input", update);
  update();
}

function collectForm() {
  const form = document.querySelector("#surveyForm");
  const data = Object.fromEntries(new FormData(form).entries());
  data.language = appState.language;
  for (const key of Object.keys(data)) {
    if (data[key] !== "" && !Number.isNaN(Number(data[key]))) data[key] = Number(data[key]);
  }
  return data;
}

function destroyChart(id) {
  if (appState.charts[id]) {
    appState.charts[id].destroy();
    delete appState.charts[id];
  }
}

function renderCharts(summary) {
  const stats = summary.seeded_stats;
  animateNumber("#sampleN", summary.source_counts.synthetic_pilot, 0);
  animateNumber("#liveN", summary.source_counts.live_submission, 0);
  document.querySelector("#alphaLonely").textContent = stats.cronbach_alpha.loneliness_custom_7_item;
  document.querySelector("#anovaF").textContent = Number(stats.anova.F).toFixed(2);
  document.querySelector("#etaSquared").textContent = Number(stats.anova.eta_squared).toFixed(3);
  const loneliness = stats.ols.find((row) => row.term === "loneliness_z");
  const connection = stats.ols.find((row) => row.term === "social_connection_z");
  if (loneliness) document.querySelector("#heroLonelinessBeta").textContent = `+${Number(loneliness.estimate).toFixed(2)}`;
  if (connection) document.querySelector("#heroConnectionBeta").textContent = Number(connection.estimate).toFixed(2);

  destroyChart("group");
  const groups = stats.group_summary;
  appState.charts.group = new Chart(document.querySelector("#groupChart"), {
    type: "bar",
    data: {
      labels: groups.map((g) => g.loneliness_group),
      datasets: [
        {
          label: "Mean Risk Decision Index",
          data: groups.map((g) => g.risk_decision_index),
          backgroundColor: ["#2D6A6A", "#D98E04", "#B23A48"],
          borderColor: "#1C2430",
          borderWidth: 1,
          borderRadius: 0,
        },
      ],
    },
    options: chartOptions("Risk Decision Index by loneliness tertile"),
  });

  const ols = stats.ols.filter((row) => row.term !== "Intercept");
  destroyChart("coef");
  appState.charts.coef = new Chart(document.querySelector("#coefChart"), {
    type: "bar",
    data: {
      labels: ols.map((row) => row.term.replaceAll("_", " ")),
      datasets: [
        {
          label: "Coefficient",
          data: ols.map((row) => row.estimate),
          backgroundColor: ols.map((row) => (row.estimate >= 0 ? "#B23A48" : "#2D6A6A")),
          borderColor: "#1C2430",
          borderWidth: 1,
        },
      ],
    },
    options: chartOptions("OLS coefficients", true),
  });

  destroyChart("type");
  appState.charts.type = new Chart(document.querySelector("#typeChart"), {
    type: "doughnut",
    data: {
      labels: stats.decision_type_counts.map((d) => d.decision_type),
      datasets: [
        {
          data: stats.decision_type_counts.map((d) => d.n),
          backgroundColor: ["#2D6A6A", "#456990", "#D98E04", "#B23A48", "#678D58"],
          borderColor: "#FFFFFF",
          borderWidth: 3,
        },
      ],
    },
    options: chartOptions("Decision profile mix"),
  });

  renderModelTable(stats.ols);
}

function chartOptions(title, horizontal = false) {
  return {
    indexAxis: horizontal ? "y" : "x",
    responsive: true,
    maintainAspectRatio: false,
    animation: { duration: 900, easing: "easeOutQuart" },
    plugins: {
      title: { display: true, text: title, color: "#1C2430", font: { size: 14, weight: "bold" } },
      legend: { display: false },
      tooltip: {
        backgroundColor: "#1C2430",
        titleColor: "#FFFFFF",
        bodyColor: "#FFFFFF",
        displayColors: false,
      },
    },
    scales: horizontal
      ? { x: { grid: { color: "#E1E6ED" }, ticks: { color: "#5B6472" } }, y: { grid: { display: false }, ticks: { color: "#5B6472" } } }
      : { y: { beginAtZero: true, grid: { color: "#E1E6ED" }, ticks: { color: "#5B6472" } }, x: { grid: { display: false }, ticks: { color: "#5B6472" } } },
  };
}

function animateNumber(selector, target, decimals = 0) {
  const el = document.querySelector(selector);
  if (!el) return;
  const start = Number(el.textContent) || 0;
  const duration = 650;
  const begin = performance.now();
  const tick = (now) => {
    const p = Math.min(1, (now - begin) / duration);
    const eased = 1 - Math.pow(1 - p, 3);
    const value = start + (target - start) * eased;
    el.textContent = value.toFixed(decimals);
    if (p < 1) requestAnimationFrame(tick);
  };
  requestAnimationFrame(tick);
}

function initSignalCanvas() {
  const canvas = document.querySelector("#signalCanvas");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const nodes = [
    { x: 0.18, y: 0.62, color: "#B23A48", label: "L" },
    { x: 0.36, y: 0.32, color: "#456990", label: "S" },
    { x: 0.58, y: 0.58, color: "#D98E04", label: "R" },
    { x: 0.78, y: 0.28, color: "#2D6A6A", label: "C" },
    { x: 0.82, y: 0.66, color: "#678D58", label: "I" },
  ];
  const links = [
    [0, 2],
    [1, 2],
    [2, 3],
    [2, 4],
    [0, 1],
    [3, 4],
  ];

  function resize() {
    const rect = canvas.getBoundingClientRect();
    const ratio = window.devicePixelRatio || 1;
    canvas.width = Math.max(1, Math.floor(rect.width * ratio));
    canvas.height = Math.max(1, Math.floor(rect.height * ratio));
    ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
  }

  function draw(time = 0) {
    const width = canvas.clientWidth;
    const height = canvas.clientHeight;
    ctx.clearRect(0, 0, width, height);
    const pulse = reduceMotion ? 0.55 : (Math.sin(time / 520) + 1) / 2;

    links.forEach(([from, to], idx) => {
      const a = nodes[from];
      const b = nodes[to];
      const ax = a.x * width;
      const ay = a.y * height;
      const bx = b.x * width;
      const by = b.y * height;
      const progress = reduceMotion ? 0.65 : (Math.sin(time / 720 + idx) + 1) / 2;
      ctx.beginPath();
      ctx.moveTo(ax, ay);
      ctx.lineTo(bx, by);
      ctx.strokeStyle = "rgba(28, 36, 48, 0.18)";
      ctx.lineWidth = 2;
      ctx.stroke();
      ctx.beginPath();
      ctx.arc(ax + (bx - ax) * progress, ay + (by - ay) * progress, 3.5, 0, Math.PI * 2);
      ctx.fillStyle = idx % 2 === 0 ? "#B23A48" : "#2A9D8F";
      ctx.fill();
    });

    nodes.forEach((node, idx) => {
      const x = node.x * width;
      const y = node.y * height;
      const radius = 17 + (idx % 2 === 0 ? pulse * 3 : (1 - pulse) * 2);
      ctx.beginPath();
      ctx.arc(x, y, radius + 7, 0, Math.PI * 2);
      ctx.fillStyle = `${node.color}22`;
      ctx.fill();
      ctx.beginPath();
      ctx.arc(x, y, radius, 0, Math.PI * 2);
      ctx.fillStyle = node.color;
      ctx.fill();
      ctx.lineWidth = 2;
      ctx.strokeStyle = "#1C2430";
      ctx.stroke();
      ctx.fillStyle = "#FFFFFF";
      ctx.font = "800 12px Inter, sans-serif";
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      ctx.fillText(node.label, x, y + 0.5);
    });

    if (!reduceMotion) requestAnimationFrame(draw);
  }

  resize();
  window.addEventListener("resize", () => {
    resize();
    if (reduceMotion) draw(0);
  });
  requestAnimationFrame(draw);
}

function initReveal() {
  const elements = document.querySelectorAll(
    ".section-heading, .agent-grid article, .method-timeline, .chart-card, .model-table-wrap, fieldset, .form-actions, .share-panel, .table-shell, .source-list article",
  );
  elements.forEach((el) => el.classList.add("reveal"));
  if (!("IntersectionObserver" in window)) {
    elements.forEach((el) => el.classList.add("is-visible"));
    return;
  }
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12, rootMargin: "0px 0px -6% 0px" },
  );
  elements.forEach((el) => observer.observe(el));
}

function initShareLink() {
  const link = `${window.location.origin}/survey`;
  const linkEl = document.querySelector("#surveyPublicLink");
  const copyButton = document.querySelector("#copySurveyLink");
  const qrEl = document.querySelector("#surveyQrCode");
  if (linkEl) {
    linkEl.href = link;
    linkEl.textContent = link;
  }
  if (qrEl && window.QRCode) {
    qrEl.innerHTML = "";
    new window.QRCode(qrEl, {
      text: link,
      width: 220,
      height: 220,
      colorDark: "#1C2430",
      colorLight: "#FFFFFF",
      correctLevel: window.QRCode.CorrectLevel.M,
    });
  } else if (qrEl) {
    qrEl.textContent = "QR unavailable";
  }
  copyButton?.addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText(link);
    } catch {
      linkEl?.focus();
    }
    const label = copyButton.querySelector("span");
    if (label) label.textContent = t("copiedLink");
    window.setTimeout(() => {
      if (label) label.textContent = t("copyLink");
    }, 1200);
  });
}

function initDetailsCharts() {
  document.querySelectorAll("details[data-chart-details]").forEach((details) => {
    details.addEventListener("toggle", () => {
      if (!details.open) return;
      requestAnimationFrame(() => {
        Object.values(appState.charts).forEach((chart) => chart.resize());
      });
    });
  });
}

function initTestRouting() {
  const testSection = document.querySelector("#questionnaire");
  if (!testSection) return;
  const openLegacyHash = () => {
    if (window.location.hash !== "#questionnaire") return;
    window.history.replaceState(null, "", "/survey");
    applyRoute();
    window.setTimeout(() => testSection.scrollIntoView({ behavior: "smooth", block: "start" }), 80);
  };
  document.querySelectorAll("[data-start-test]").forEach((link) => {
    link.addEventListener("click", (event) => {
      if (window.location.pathname !== "/survey") return;
      event.preventDefault();
      applyRoute();
      testSection.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  });
  if (window.location.hash === "#questionnaire") {
    window.setTimeout(openLegacyHash, 120);
  }
  window.addEventListener("hashchange", () => {
    if (window.location.hash === "#questionnaire") openLegacyHash();
  });
}

function renderModelTable(rows) {
  const tbody = document.querySelector("#modelTableEl tbody");
  if (!tbody) return;
  tbody.innerHTML = rows
    .map(
      (row) => `<tr>
        <td>${row.term.replaceAll("_", " ")}</td>
        <td>${Number(row.estimate).toFixed(2)}</td>
        <td>${formatP(row.p_approx)}</td>
      </tr>`,
    )
    .join("");
}

function formatP(p) {
  if (Number(p) < 0.001) return "&lt;.001";
  return Number(p).toFixed(3);
}

function renderSources(config) {
  const list = document.querySelector("#sourceList");
  if (!list) return;
  list.innerHTML = config.sources
    .map(
      (source) => `<article>
        <h3>${source.id.replaceAll("_", " ")}</h3>
        <p>${source.citation}</p>
        <p><strong>Used for:</strong> ${source.used_for}</p>
        <a href="${source.url}" target="_blank" rel="noreferrer">${source.url}</a>
      </article>`,
    )
    .join("");
}

async function renderResponses() {
  const data = await getJson("/api/responses?limit=25");
  const rows = [...data.live, ...data.synthetic].slice(0, 30);
  const tbody = document.querySelector("#responsePreview tbody");
  if (!tbody) return;
  tbody.innerHTML = rows
    .map(
      (row) => `<tr>
        <td>${row.participant_id}</td>
        <td>${row.source_type}</td>
        <td>${row.age ?? ""}</td>
        <td>${row.loneliness_score ?? ""}</td>
        <td>${row.social_connection_score ?? ""}</td>
        <td>${row.risk_decision_index ?? ""}</td>
        <td>${row.decision_type ?? ""}</td>
      </tr>`,
    )
    .join("");
}

function renderReport(scores) {
  const output = document.querySelector("#reportOutput");
  if (!output) return;
  output.hidden = false;
  document.querySelector("#profileType").textContent = scores.decision_type;
  document.querySelector("#profileInterpretation").textContent = scores.interpretation;
  const labels = [
    ["Loneliness", "loneliness_score"],
    ["Social connection", "social_connection_score"],
    ["Immediate reward", "immediate_reward_bias"],
    ["Impulsive spending", "impulsive_spending_score"],
    ["High-risk choice", "high_risk_choice_score"],
    ["Conflict defense", "conflict_defense_score"],
    ["Risk Decision Index", "risk_decision_index"],
  ];
  document.querySelector("#scoreBars").innerHTML = labels
    .map(([label, key]) => {
      const value = Number(scores[key] ?? 0);
      return `<div class="score-bar">
        <span>${label}</span>
        <div class="bar-track"><div class="bar-fill" style="width:${Math.max(0, Math.min(100, value))}%"></div></div>
        <strong>${value.toFixed(1)}</strong>
      </div>`;
    })
    .join("");
  output.scrollIntoView({ behavior: "smooth", block: "center" });
}

async function score(save) {
  const payload = collectForm();
  const endpoint = save ? "/api/submit" : "/api/score";
  const result = await getJson(endpoint, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const scores = save ? result.scores : result;
  renderReport(scores);
  if (save) {
    appState.summary = result.summary;
    renderCharts(appState.summary);
    await renderResponses();
  }
}

async function boot() {
  applyRoute();
  renderLikert();
  renderTasks();
  document.querySelectorAll("input[type=range]").forEach(bindRangeLabel);
  window.addEventListener("popstate", applyRoute);
  document.querySelector("#languageToggle")?.addEventListener("click", () => {
    appState.language = appState.language === "en" ? "zh" : "en";
    applyLanguage();
  });
  document.querySelector("#surveyForm")?.addEventListener("submit", async (event) => {
    event.preventDefault();
    await score(true);
  });
  document.querySelector("#scoreOnly")?.addEventListener("click", async () => score(false));
  appState.config = await getJson("/api/config");
  appState.summary = await getJson("/api/summary");
  renderSources(appState.config);
  renderCharts(appState.summary);
  await renderResponses();
  initShareLink();
  initDetailsCharts();
  initTestRouting();
  if (window.lucide) window.lucide.createIcons();
  initSignalCanvas();
  initReveal();
  applyRoute();
}

boot().catch((error) => {
  console.error(error);
  document.body.insertAdjacentHTML("afterbegin", `<pre style="padding:16px;background:#fee;color:#900">${error.message}</pre>`);
});
