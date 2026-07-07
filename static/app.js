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
    lead: "A behavioral research tool for measuring how social connection relates to reward timing, conflict response, and risk preference.",
    heroPromise: "Take a 3-minute behavioral test and receive a risk-decision profile based on loneliness, social connection, and reward preference.",
    hypothesisLabel: "Primary hypothesis",
    hypothesisText: "Higher loneliness predicts a higher Risk Decision Index, while social connection buffers the pattern.",
    cockpitKicker: "Quant cockpit",
    cockpitTitle: "From social signals to risk estimates",
    startTest: "Start Decision Test",
    startTestShort: "Start Test",
    exportCsv: "Export CSV",
    openStatistics: "View statistics",
    openWorkflow: "View workflow details",
    openCharts: "View model charts",
    pulseEyebrow: "Research pulse",
    pulseTitle: "Why this topic belongs at the intersection of psychology and statistics.",
    metricSample: "Synthetic pilot n",
    metricLive: "Live submissions",
    metricAlpha: "Loneliness alpha",
    pipelineEyebrow: "End-to-end research workflow",
    pipelineTitle: "Survey, scoring, analysis, and reporting work as one visible research pipeline.",
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
    lead: "一个行为研究工具，用来测量社交连接如何关联奖励时机、冲突反应和风险偏好。",
    heroPromise: "用约 3 分钟完成行为测试，并获得基于孤独感、社交连接和奖励偏好的风险决策画像。",
    hypothesisLabel: "核心假设",
    hypothesisText: "更高的孤独感会预测更高的风险决策指数，而社交连接感会起到缓冲作用。",
    cockpitKicker: "量化驾驶舱",
    cockpitTitle: "从社交信号到风险估计",
    startTest: "开始决策测试",
    startTestShort: "Start Test",
    exportCsv: "导出 CSV",
    openStatistics: "查看统计图",
    openWorkflow: "查看流程详情",
    openCharts: "查看模型图表",
    pulseEyebrow: "研究引入",
    pulseTitle: "为什么这个主题属于心理学与统计学的交叉。",
    metricSample: "模拟试点样本 n",
    metricLive: "真实提交数",
    metricAlpha: "孤独量表 alpha",
    pipelineEyebrow: "端到端研究流程",
    pipelineTitle: "问卷、评分、分析和报告组成一个可见的研究流程。",
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

const staticTextDefaults = new WeakMap();
const zhStaticCopy = {
  "3 min test": "3 分钟测试",
  "Survey + choices": "问卷 + 选择任务",
  "Instant profile": "即时画像",
  "Research use only": "仅用于研究展示",
  "Public health": "公共健康",
  "Social connection is now treated as a population-level concern.": "社交连接已被视为群体层面的公共健康议题。",
  "Global lens": "全球视角",
  "WHO frames social connection as a cross-country wellbeing issue.": "世界卫生组织将社交连接视为跨国家的福祉议题。",
  "Youth data": "青少年数据",
  "CDC youth surveys provide a benchmark for adolescent risk context.": "CDC 青少年调查为青少年风险行为背景提供参考。",
  "Social psychology": "社会心理学",
  "Ages 16-24": "16-24 岁",
  "Loneliness": "孤独感",
  "Risk Decision Index": "风险决策指数",
  "Digital peer networks": "数字同伴网络",
  "L": "L",
  "S": "S",
  "R": "R",
  "C": "C",
  "I": "I",
  "Stress": "压力",
  "Risk decision": "风险决策",
  "Connection": "连接感",
  "Impulsivity": "冲动性",
  "Loneliness z": "孤独感 z",
  "Connection z": "连接感 z",
  "About this study": "关于本研究",
  "A research-oriented behavioral assessment, not a clinical diagnosis.": "这是面向研究的行为评估，不是临床诊断。",
  "Research question": "研究问题",
  "Does loneliness change how people choose risk?": "孤独感会改变人们如何选择风险吗？",
  "Primary focus: loneliness and social connection as predictors of immediate rewards, impulsive spending, high-risk choices, and conflict-defense responses.": "核心关注：孤独感和社交连接是否能预测即时奖励、冲动消费、高风险选择和冲突防御反应。",
  "Measurement": "测量方式",
  "Survey items + behavioral choice tasks": "问卷题项 + 行为选择任务",
  "The test uses Likert batteries, social-signal inputs, delay choices, spending scenarios, risky options, and conflict-response sliders.": "测试包含李克特量表、社交信号输入、延迟选择、消费情境、风险选项和冲突反应滑块。",
  "Boundary": "研究边界",
  "Educational research tool only": "仅作为教育研究工具",
  "Scores estimate a decision-profile index for research and class presentation. They are not mental-health diagnosis or clinical advice.": "分数用于估计研究和课堂展示中的决策画像指数，不是心理健康诊断或临床建议。",
  "Operational research OS": "运行中的研究系统",
  "One public interface connects participation, scoring, evidence, and exportable research assets.": "一个公开界面连接参与、评分、证据和可导出的研究材料。",
  "Take the behavioral test": "完成行为测试",
  "Open a focused survey route with social-signal questions and decision scenarios.": "进入独立问卷页面，完成社交信号问题和决策情境任务。",
  "Generate personal scores": "生成个人分数",
  "Receive standardized loneliness, connection, reward, spending, risk, and conflict indicators.": "获得孤独感、连接感、奖励、消费、风险和冲突指标的标准化分数。",
  "Analyze group-level data": "分析群体数据",
  "Use reliability checks, OLS, ANOVA, decision types, and chart panels for interpretation.": "使用信度检验、OLS、ANOVA、决策类型和图表面板进行解释。",
  "Export research package": "导出研究包",
  "Download the paper, Word report, slides, workbook, video, live CSV, and full package.": "下载论文、Word 报告、幻灯片、工作簿、视频、实时 CSV 和完整包。",
  "How it works": "如何使用",
  "Start with participation, end with interpretable research outputs.": "从参与测试开始，到可解释的研究输出结束。",
  "Answer a short survey": "回答简短问卷",
  "Social contact, digital behavior, loneliness, and connection are measured with numeric inputs and Likert items.": "用数字输入和李克特题项测量社交接触、数字行为、孤独感和连接感。",
  "Complete decision scenarios": "完成决策情境",
  "Delay choices, spending choices, risky options, and conflict responses turn abstract psychology into behavioral data.": "延迟选择、消费选择、风险选项和冲突反应把抽象心理变量转化为行为数据。",
  "Receive standardized scores": "获得标准化分数",
  "The site returns 0-100 indicators and a decision-profile type that can be viewed immediately.": "网站会返回 0-100 指标和可立即查看的决策画像类型。",
  "Export or analyze data": "导出或分析数据",
  "Live submissions stay separate from synthetic pilot rows and can be exported for classroom or research analysis.": "真实提交与模拟试点数据分开保存，可导出用于课堂或研究分析。",
  "Psychological mechanism": "心理机制",
  "Perceived isolation can amplify social-threat monitoring and short-horizon emotion regulation.": "感知到的孤立可能增强社会威胁监测和短期情绪调节需求。",
  "Behavioral measurement": "行为测量",
  "Delay choices, spending items, risky options, and conflict scenarios turn the construct into data.": "延迟选择、消费题项、风险选项和冲突情境把概念转化为数据。",
  "Statistical test": "统计检验",
  "Regression and ANOVA estimate whether the loneliness-risk gradient survives controls.": "回归和 ANOVA 用来估计孤独感与风险之间的梯度是否在控制变量后仍然存在。",
  "Survey Agent": "问卷 Agent",
  "collects behavioral and self-report responses": "收集行为和自陈反应",
  "Scoring Agent": "评分 Agent",
  "converts answers into standardized indicators": "把答案转化为标准化指标",
  "Analysis Agent": "分析 Agent",
  "runs OLS, ANOVA, and reliability checks": "运行 OLS、ANOVA 和信度检验",
  "Report Agent": "报告 Agent",
  "generates downloadable research materials": "生成可下载研究材料",
  "Question boundary": "问题边界",
  "field + population + predictor + outcome + context": "领域 + 人群 + 自变量 + 结果 + 背景",
  "Measurement": "测量",
  "custom items + behavioral tasks": "自定义题项 + 行为任务",
  "Modeling": "建模",
  "alpha + correlation + OLS + logit + ANOVA": "alpha + 相关 + OLS + logit + ANOVA",
  "Public study": "公开研究",
  "website + QR + live submissions": "网站 + 二维码 + 实时提交",
  "Interpretation": "解释",
  "Term": "变量",
  "Estimate": "估计值",
  "p": "p 值",
  "ANOVA F": "ANOVA F",
  "Eta squared": "Eta 平方",
  "Age": "年龄",
  "Population": "人群",
  "High school student": "高中生",
  "Undergraduate student": "本科生",
  "Early career adult": "职场早期成人",
  "Other": "其他",
  "Platform opens per day": "每天打开社交平台次数",
  "Messages sent per day": "每天发送消息数",
  "In-person conversations per week": "每周线下对话次数",
  "Shared meals or social events per week": "每周共同用餐或社交活动次数",
  "Group activities per month": "每月集体活动次数",
  "Trusted contacts": "可信任联系人数量",
  "Stress 0-100": "压力 0-100",
  "Sleep hours": "睡眠小时数",
  "Participant": "参与者",
  "Source": "来源",
  "Risk Index": "风险指数",
  "Type": "类型",
  "Research package": "研究材料包",
  "Download the paper, Word report, deck, workbook, video, and data exports.": "下载论文、Word 报告、演示文稿、工作簿、视频和数据导出。",
  "The project is structured as a reusable research-product template: public site, live survey, SQLite data pipeline, statistical report, and presentation assets.": "该项目被组织成可复用的研究产品模板：公开网站、实时问卷、SQLite 数据管线、统计报告和展示材料。",
  "For participants": "面向参与者",
  "Immediate profile and response copy for people taking the test.": "为测试参与者提供即时画像和回应数据副本。",
  "Profile": "个人画像",
  "Generate personal risk-decision profile": "生成个人风险决策画像",
  "Web result · instant": "网页结果 · 即时",
  "Live CSV": "实时 CSV",
  "Current survey export": "当前问卷导出",
  "CSV · live local data": "CSV · 本地实时数据",
  "For researchers / instructors": "面向研究者 / 指导老师",
  "Academic materials for explaining the design, data pipeline, models, and presentation logic.": "用于解释研究设计、数据管线、模型和展示逻辑的学术材料。",
  "Paper PDF": "论文 PDF",
  "Full academic research paper": "完整学术研究论文",
  "Word report": "Word 报告",
  "Editable DOCX research report": "可编辑 DOCX 研究报告",
  "Slide deck": "演示文稿",
  "Presentation-ready PPTX": "可直接展示的 PPTX",
  "Workbook": "工作簿",
  "Data tables and analysis sheets": "数据表和分析表",
  "Intro video": "介绍视频",
  "Research overview video": "研究概览视频",
  "Full package": "完整包",
  "All final deliverables": "所有最终交付文件",
  "Questions people usually ask before taking the test.": "测试前常见问题。",
  "Is this a psychological diagnosis?": "这是心理诊断吗？",
  "No. The website is an educational research instrument. It estimates a decision-profile index and should not be used as clinical or mental-health diagnosis.": "不是。这个网站是教育研究工具，用来估计决策画像指数，不应作为临床或心理健康诊断。",
  "How long does the test take?": "测试需要多久？",
  "Most participants can finish in about three minutes. The survey combines short social-signal questions, loneliness and connection items, and brief decision scenarios.": "大多数参与者约 3 分钟可以完成。问卷包含社交信号问题、孤独感和连接感题项，以及简短决策情境。",
  "Is my response anonymous?": "我的回答是匿名的吗？",
  "The form does not ask for a name. Live submissions are stored on this server for research demonstration and CSV export, while synthetic pilot data remain clearly separated.": "表单不会询问姓名。实时提交会保存在本服务器用于研究展示和 CSV 导出，并与模拟试点数据明确分开。",
  "Can I retake the test?": "我可以重新测试吗？",
  "Yes. Retaking creates a new score. Use “Score without saving” if you want to see a profile without adding another live submission to the local database.": "可以。重新测试会生成新的分数。如果只想查看画像而不写入数据库，可以使用“仅评分不保存”。",
  "What population is the study designed for?": "这项研究面向什么人群？",
  "The primary target group is late adolescents and emerging adults, especially students and young adults in digitally mediated school or college communities.": "主要目标人群是青少年后期和新兴成年人，尤其是处在数字化学校或大学社群中的学生和年轻成人。",
  "Why does the study measure social media behavior?": "为什么测量社交媒体行为？",
  "What does the Risk Decision Index mean?": "风险决策指数是什么意思？",
  "Are synthetic and live data mixed together?": "模拟数据和实时数据会混在一起吗？",
  "Can this be used for a school research presentation?": "可以用于学校研究展示吗？",
  "Project contact": "项目联系",
  "Project lead": "项目负责人",
  "Project type": "项目类型",
  "Behavioral research prototype / class-ready lab product": "行为研究原型 / 可课堂展示的实验室产品",
  "Data note": "数据说明",
  "This public prototype is for educational research presentation; avoid submitting sensitive personal information.": "这个公开原型用于教育研究展示，请避免提交敏感个人信息。",
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
  applyStaticLanguage();
  if (appState.summary) renderCharts(appState.summary);
  if (window.lucide) window.lucide.createIcons();
  applyRoute();
}

function applyStaticLanguage() {
  const walker = document.createTreeWalker(
    document.body,
    NodeFilter.SHOW_TEXT,
    {
      acceptNode(node) {
        const parent = node.parentElement;
        if (!parent) return NodeFilter.FILTER_REJECT;
        if (parent.closest("script, style, canvas, [data-i18n], #likertGrid, #choiceTasks, #responsePreview tbody, #sourceList")) {
          return NodeFilter.FILTER_REJECT;
        }
        return node.nodeValue.trim() ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT;
      },
    },
  );
  const nodes = [];
  while (walker.nextNode()) nodes.push(walker.currentNode);
  nodes.forEach((node) => {
    if (!staticTextDefaults.has(node)) staticTextDefaults.set(node, node.nodeValue);
    const original = staticTextDefaults.get(node);
    if (appState.language === "en") {
      node.nodeValue = original;
      return;
    }
    const key = original.trim().replace(/\s+/g, " ");
    const translated = zhStaticCopy[key];
    if (!translated) {
      node.nodeValue = original;
      return;
    }
    const leading = original.match(/^\s*/)?.[0] ?? "";
    const trailing = original.match(/\s*$/)?.[0] ?? "";
    node.nodeValue = `${leading}${translated}${trailing}`;
  });
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

function initAmbientCanvas() {
  const canvas = document.querySelector("#ambientCanvas");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const pointer = { x: 0.5, y: 0.25, active: false };
  let particles = [];

  function resize() {
    const ratio = window.devicePixelRatio || 1;
    const width = window.innerWidth;
    const height = window.innerHeight;
    canvas.width = Math.max(1, Math.floor(width * ratio));
    canvas.height = Math.max(1, Math.floor(height * ratio));
    canvas.style.width = `${width}px`;
    canvas.style.height = `${height}px`;
    ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
    const count = Math.max(58, Math.min(120, Math.floor((width * height) / 18000)));
    particles = Array.from({ length: count }, (_, index) => ({
      x: Math.random() * width,
      y: Math.random() * height,
      vx: (Math.random() - 0.5) * (0.18 + (index % 5) * 0.02),
      vy: (Math.random() - 0.5) * (0.18 + (index % 7) * 0.018),
      r: 1.3 + Math.random() * 2.4,
      hue: index % 4,
      phase: Math.random() * Math.PI * 2,
    }));
    draw(0);
  }

  function colorFor(particle, alpha) {
    const colors = [
      `rgba(39, 100, 255, ${alpha})`,
      `rgba(15, 186, 167, ${alpha})`,
      `rgba(42, 189, 245, ${alpha})`,
      `rgba(244, 162, 26, ${alpha})`,
    ];
    return colors[particle.hue];
  }

  function draw(time = 0) {
    const width = canvas.clientWidth;
    const height = canvas.clientHeight;
    ctx.clearRect(0, 0, width, height);
    ctx.lineWidth = 1;

    const sweep = reduceMotion ? width * 0.55 : ((time / 9000) % 1) * width * 1.45 - width * 0.22;
    ctx.save();
    ctx.globalAlpha = 0.42;
    ctx.lineWidth = 1.2;
    for (let i = -2; i < 5; i += 1) {
      const x = sweep + i * 92;
      const gradient = ctx.createLinearGradient(x - 160, 0, x + 220, height);
      gradient.addColorStop(0, "rgba(39, 100, 255, 0)");
      gradient.addColorStop(0.5, "rgba(42, 189, 245, 0.28)");
      gradient.addColorStop(1, "rgba(15, 186, 167, 0)");
      ctx.strokeStyle = gradient;
      ctx.beginPath();
      ctx.moveTo(x - 180, 0);
      ctx.lineTo(x + 220, height);
      ctx.stroke();
    }
    ctx.restore();

    particles.forEach((particle, i) => {
      if (!reduceMotion) {
        particle.x += particle.vx;
        particle.y += particle.vy;
        const drift = Math.sin(time / 1800 + particle.phase) * 0.12;
        particle.x += drift;
        if (particle.x < -20) particle.x = width + 20;
        if (particle.x > width + 20) particle.x = -20;
        if (particle.y < -20) particle.y = height + 20;
        if (particle.y > height + 20) particle.y = -20;
      }

      for (let j = i + 1; j < particles.length; j += 1) {
        const other = particles[j];
        const dx = particle.x - other.x;
        const dy = particle.y - other.y;
        const distance = Math.hypot(dx, dy);
        if (distance > 150) continue;
        const alpha = (1 - distance / 150) * 0.26;
        ctx.beginPath();
        ctx.moveTo(particle.x, particle.y);
        ctx.lineTo(other.x, other.y);
        ctx.strokeStyle = colorFor(particle, alpha);
        ctx.stroke();
      }

      if (pointer.active) {
        const px = pointer.x * width;
        const py = pointer.y * height;
        const distance = Math.hypot(particle.x - px, particle.y - py);
        if (distance < 180) {
          ctx.beginPath();
          ctx.moveTo(particle.x, particle.y);
          ctx.lineTo(px, py);
          ctx.strokeStyle = `rgba(39, 100, 255, ${(1 - distance / 180) * 0.28})`;
          ctx.stroke();
        }
      }

      ctx.beginPath();
      ctx.arc(particle.x, particle.y, particle.r, 0, Math.PI * 2);
      ctx.fillStyle = colorFor(particle, 0.58);
      ctx.fill();
    });

    if (!reduceMotion) requestAnimationFrame(draw);
  }

  window.addEventListener("resize", resize, { passive: true });
  window.addEventListener("pointermove", (event) => {
    pointer.x = event.clientX / window.innerWidth;
    pointer.y = event.clientY / window.innerHeight;
    pointer.active = true;
  }, { passive: true });
  window.addEventListener("pointerleave", () => {
    pointer.active = false;
  });
  resize();
}

function initPointerSpotlight() {
  const selectors = [
    ".news-strip a",
    ".overview-grid article",
    ".pulse-grid article",
    ".work-grid article",
    ".workflow-preview div",
    ".launch-card",
    ".download-card",
    ".download-group",
    ".source-list article",
    ".faq-list details",
  ].join(",");
  document.querySelectorAll(selectors).forEach((element) => {
    element.addEventListener("pointermove", (event) => {
      const rect = element.getBoundingClientRect();
      const x = ((event.clientX - rect.left) / rect.width) * 100;
      const y = ((event.clientY - rect.top) / rect.height) * 100;
      element.style.setProperty("--mx", `${x}%`);
      element.style.setProperty("--my", `${y}%`);
    }, { passive: true });
  });
}

function initSignalCanvas() {
  const canvas = document.querySelector("#signalCanvas");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const nodes = [
    { x: 0.16, y: 0.62, color: "#fb7185", label: "L" },
    { x: 0.34, y: 0.28, color: "#93c5fd", label: "S" },
    { x: 0.56, y: 0.56, color: "#f9d56e", label: "R" },
    { x: 0.78, y: 0.28, color: "#67e8f9", label: "C" },
    { x: 0.84, y: 0.66, color: "#86efac", label: "I" },
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

    ctx.save();
    ctx.translate(width * 0.55, height * 0.5);
    ctx.strokeStyle = "rgba(125, 211, 252, 0.12)";
    ctx.lineWidth = 1;
    for (let i = 0; i < 4; i += 1) {
      const w = width * (0.28 + i * 0.16);
      const h = height * (0.2 + i * 0.11);
      ctx.beginPath();
      ctx.ellipse(0, 0, w, h, -0.08, 0, Math.PI * 2);
      ctx.stroke();
    }
    ctx.restore();

    links.forEach(([from, to], idx) => {
      const a = nodes[from];
      const b = nodes[to];
      const ax = a.x * width;
      const ay = a.y * height;
      const bx = b.x * width;
      const by = b.y * height;
      const progress = reduceMotion ? 0.65 : (Math.sin(time / 720 + idx) + 1) / 2;
      const gradient = ctx.createLinearGradient(ax, ay, bx, by);
      gradient.addColorStop(0, "rgba(251, 113, 133, 0.22)");
      gradient.addColorStop(0.48, "rgba(103, 232, 249, 0.62)");
      gradient.addColorStop(1, "rgba(249, 213, 110, 0.26)");
      ctx.beginPath();
      ctx.moveTo(ax, ay);
      ctx.lineTo(bx, by);
      ctx.strokeStyle = gradient;
      ctx.lineWidth = 2.4;
      ctx.shadowColor = "rgba(103, 232, 249, 0.24)";
      ctx.shadowBlur = 10;
      ctx.stroke();
      ctx.shadowBlur = 0;
      ctx.beginPath();
      ctx.arc(ax + (bx - ax) * progress, ay + (by - ay) * progress, 4.6, 0, Math.PI * 2);
      ctx.fillStyle = idx % 2 === 0 ? "#fb7185" : "#67e8f9";
      ctx.shadowColor = ctx.fillStyle;
      ctx.shadowBlur = 16;
      ctx.fill();
      ctx.shadowBlur = 0;
    });

    nodes.forEach((node, idx) => {
      const x = node.x * width;
      const y = node.y * height;
      const radius = 19 + (idx % 2 === 0 ? pulse * 4 : (1 - pulse) * 3);
      ctx.beginPath();
      ctx.arc(x, y, radius + 11, 0, Math.PI * 2);
      ctx.fillStyle = `${node.color}24`;
      ctx.fill();
      ctx.beginPath();
      ctx.arc(x, y, radius, 0, Math.PI * 2);
      ctx.shadowColor = node.color;
      ctx.shadowBlur = 18;
      ctx.fillStyle = node.color;
      ctx.fill();
      ctx.shadowBlur = 0;
      ctx.lineWidth = 2;
      ctx.strokeStyle = "rgba(255, 255, 255, 0.72)";
      ctx.stroke();
      ctx.fillStyle = "#FFFFFF";
      ctx.font = "800 14px Manrope, Inter, sans-serif";
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
    ".section-heading, .overview-grid article, .work-grid article, .workflow-preview div, .agent-grid article, .method-timeline, .chart-card, .model-interpretation, .model-table-wrap, fieldset, .form-actions, .share-panel, .table-shell, .source-list article, .download-group",
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
  initAmbientCanvas();
  initPointerSpotlight();
  initSignalCanvas();
  initReveal();
  applyRoute();
}

boot().catch((error) => {
  console.error(error);
  document.body.insertAdjacentHTML("afterbegin", `<pre style="padding:16px;background:#fee;color:#900">${error.message}</pre>`);
});
