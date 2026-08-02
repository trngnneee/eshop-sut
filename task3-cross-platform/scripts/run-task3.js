const { chromium, firefox, webkit, devices } = require("playwright");
const fs = require("fs");
const path = require("path");
const os = require("os");

const REPO_ROOT = path.resolve(__dirname, "..", "..");
const TASK_ROOT = path.resolve(__dirname, "..");
const EVIDENCE_ROOT = path.join(TASK_ROOT, "evidence");
const RESULTS_ROOT = path.join(TASK_ROOT, "results");
const WEB_URL = "http://localhost:5173";
const ADMIN_URL = "http://localhost:5174";
const MOBILE_URL = "http://localhost:8081";
const API_URL = "http://localhost:3000/api";

const STUDENT = {
  name: "Đặng Đăng Khoa",
  id: "23127207",
  email: "23127207@student.hcmus.edu.vn",
};

const PLATFORM_DEFINITIONS = {
  "chrome-windows": {
    label: "Google Chrome / Windows",
    eligible: true,
    launcher: chromium,
    launchOptions: { channel: "chrome", headless: true },
    device: "Desktop 1440×900",
    note: "Real locally installed Google Chrome on Windows.",
  },
  "firefox-windows": {
    label: "Firefox / Windows",
    eligible: true,
    launcher: firefox,
    launchOptions: { headless: true },
    device: "Desktop 1440×900",
    note: "Playwright-distributed Firefox browser binary running locally on Windows.",
  },
  "webkit-windows": {
    label: "Playwright WebKit / Windows",
    eligible: false,
    launcher: webkit,
    launchOptions: { headless: true },
    device: "Desktop 1440×900",
    note: "Supplemental WebKit-engine run only; this is not Apple Safari and is not counted as the required third platform.",
  },
  "android-chrome-emulation": {
    label: "Chromium Pixel 7 emulation / Windows host",
    eligible: false,
    launcher: chromium,
    launchOptions: { headless: true },
    device: "Emulated Pixel 7 viewport/touch/user-agent",
    contextOptions: { ...devices["Pixel 7"] },
    note: "Supplemental responsive emulation only; this is not a physical Android device or cloud Android Chrome session.",
  },
};

const requestedPlatforms = (() => {
  const argument = process.argv.find((item) => item.startsWith("--platforms="));
  if (!argument) return Object.keys(PLATFORM_DEFINITIONS);
  return argument
    .slice("--platforms=".length)
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
})();
const mobileOnly = process.argv.includes("--mobile-only");
const keyboardOnly = process.argv.includes("--keyboard-only");

const task1Checklist = fs.readFileSync(
  path.join(REPO_ROOT, "task1-gui", "GUI_Checklist_HW3.md"),
  "utf8",
);
const expectedIds = [...task1Checklist.matchAll(/^\|\s*(GUI-[A-Z0-9-]+)\s*\|/gm)].map(
  (match) => match[1],
);

fs.mkdirSync(EVIDENCE_ROOT, { recursive: true });
fs.mkdirSync(RESULTS_ROOT, { recursive: true });

const delay = (milliseconds) =>
  new Promise((resolve) => setTimeout(resolve, milliseconds));

async function api(pathname, options = {}) {
  const response = await fetch(`${API_URL}${pathname}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
  });
  const text = await response.text();
  let body = {};
  try {
    body = text ? JSON.parse(text) : {};
  } catch {
    body = { raw: text };
  }
  return { response, body };
}

async function createUser(email, password = "Task3Pass1!", name = "Task3 Synthetic User") {
  const { response, body } = await api("/register", {
    method: "POST",
    body: JSON.stringify({ name, email, password }),
  });
  if (!response.ok) throw new Error(`Synthetic user setup failed: ${response.status}`);
  return body.id;
}

async function getAdminToken() {
  const { response, body } = await api("/login", {
    method: "POST",
    body: JSON.stringify({ email: "admin@eshop.com", password: "Admin123!" }),
  });
  if (!response.ok || !body.token) throw new Error("Admin token setup failed.");
  return body.token;
}

async function cleanupUser(id, token) {
  if (!id) return;
  await api(`/admin/users/${id}`, {
    method: "DELETE",
    headers: { Authorization: `Bearer ${token}` },
  });
}

async function createCategory(name, token) {
  const { response, body } = await api("/categories", {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` },
    body: JSON.stringify({ name }),
  });
  if (!response.ok) throw new Error(`Synthetic category setup failed: ${response.status}`);
  return body.id;
}

async function cleanupCategory(id, token) {
  if (!id) return;
  await api(`/categories/${id}`, {
    method: "DELETE",
    headers: { Authorization: `Bearer ${token}` },
  });
}

async function createProduct(categoryId, suffix) {
  const { response, body } = await api("/products", {
    method: "POST",
    body: JSON.stringify({
      name: `TASK3_SYNTHETIC_PRODUCT_${suffix}`,
      price: 1000,
      description: "Synthetic Task 3 cleanup-safe product",
      imageUrl: "https://placehold.co/40",
      category_id: categoryId,
    }),
  });
  if (!response.ok) throw new Error(`Synthetic product setup failed: ${response.status}`);
  return body.id;
}

async function cleanupProduct(id) {
  if (!id) return;
  await api(`/products/${id}`, { method: "DELETE" });
}

function makeRunState(platformId, definition, browserVersion) {
  const platformDir = path.join(EVIDENCE_ROOT, platformId);
  fs.mkdirSync(platformDir, { recursive: true });
  return {
    platformId,
    definition,
    browserVersion,
    platformDir,
    sequence: 0,
    results: [],
    console: [],
    pageErrors: [],
    runErrors: [],
    createdUserIds: new Set(),
    createdCategoryIds: new Set(),
    createdProductIds: new Set(),
  };
}

function attachDiagnostics(page, state, scope) {
  page.on("console", (message) => {
    state.console.push({
      scope,
      type: message.type(),
      text: message.text().slice(0, 1000),
    });
  });
  page.on("pageerror", (error) => {
    state.pageErrors.push({ scope, message: error.message.slice(0, 1000) });
  });
}

async function addEvidenceOverlay(page, state, evidenceId, ids, observation) {
  const payload = {
    evidenceId,
    student: `${STUDENT.name} | ${STUDENT.id} | ${STUDENT.email}`,
    platform: `${state.definition.label} ${state.browserVersion}`,
    os: `Windows host ${os.release()}`,
    device: state.definition.device,
    url: page.url(),
    ids: ids.join(", "),
    observation,
    capturedAt: new Date().toISOString(),
  };
  await page.evaluate((data) => {
    document.getElementById("task3-evidence-overlay")?.remove();
    const overlay = document.createElement("aside");
    overlay.id = "task3-evidence-overlay";
    overlay.setAttribute("data-task3-overlay", "true");
    overlay.style.cssText = [
      "position:fixed",
      "left:8px",
      "right:8px",
      "bottom:8px",
      "z-index:2147483647",
      "background:rgba(9,18,35,.95)",
      "color:#fff",
      "border:2px solid #22d3ee",
      "border-radius:8px",
      "padding:8px 10px",
      "font:12px/1.35 Consolas,monospace",
      "box-shadow:0 2px 12px rgba(0,0,0,.45)",
      "white-space:normal",
      "overflow-wrap:anywhere",
    ].join(";");
    const rows = [
      `<b>${data.evidenceId}</b> — ${data.student}`,
      `<b>Platform:</b> ${data.platform} | <b>OS/device:</b> ${data.os}; ${data.device}`,
      `<b>SUT URL:</b> ${data.url}`,
      `<b>Checklist:</b> ${data.ids}`,
      `<b>Observed:</b> ${data.observation}`,
      `<b>Captured:</b> ${data.capturedAt}`,
    ];
    overlay.innerHTML = rows.map((row) => `<div>${row}</div>`).join("");
    document.body.appendChild(overlay);
  }, payload);
}

async function captureAndRecord(page, state, slug, assessments, observation) {
  state.sequence += 1;
  const number = String(state.sequence).padStart(3, "0");
  const evidenceId = `T3-${state.platformId.toUpperCase()}-${number}`;
  const fileName = `${number}-${slug}.png`;
  const absolutePath = path.join(state.platformDir, fileName);
  const ids = assessments.map((item) => item.id);
  await addEvidenceOverlay(page, state, evidenceId, ids, observation);
  await page.screenshot({ path: absolutePath, fullPage: false, animations: "disabled" });
  await page.evaluate(() => document.getElementById("task3-evidence-overlay")?.remove());
  const relativeEvidence = path
    .relative(TASK_ROOT, absolutePath)
    .split(path.sep)
    .join("/");
  for (const assessment of assessments) {
    state.results.push({
      participant_id: "N/A_TECHNICAL_TEST",
      platform_id: state.platformId,
      platform_label: state.definition.label,
      eligible_platform: state.definition.eligible ? "YES" : "NO",
      checklist_id: assessment.id,
      execution_mode: assessment.mode || "LIVE_LOCAL_SUT",
      status: assessment.status,
      actual_result: assessment.actual,
      evidence_id: evidenceId,
      evidence_path: relativeEvidence,
      captured_at: new Date().toISOString(),
    });
  }
  return relativeEvidence;
}

async function safeScenario(state, label, callback) {
  try {
    await callback();
  } catch (error) {
    state.runErrors.push({ label, message: error.stack || error.message });
  }
}

async function fillWebLogin(page, email, password) {
  const inputs = page.locator("form input");
  await inputs.nth(0).fill(email);
  await inputs.nth(1).fill(password);
}

async function fillRegister(page, { name, email, password, confirmPassword = password }) {
  await page.locator("#register-name").fill(name);
  await page.locator("#register-email").fill(email);
  await page.locator("#register-password").fill(password);
  await page.locator("#register-confirm-password").fill(confirmPassword);
}

async function loginAdmin(page) {
  await page.goto(ADMIN_URL, { waitUntil: "networkidle" });
  const inputs = page.locator("form input");
  await inputs.nth(0).fill("admin@eshop.com");
  await inputs.nth(1).fill("Admin123!");
  await page.locator("form button").click();
  await page.getByText("EShop Admin", { exact: true }).waitFor({ timeout: 10000 });
}

async function openCategories(page) {
  await page.locator("li").filter({ hasText: /Danh/ }).first().click();
  await page.locator("table").waitFor({ timeout: 10000 });
}

async function executeWebLogin(page, state, adminToken, suffix) {
  await safeScenario(state, "web-login-baseline", async () => {
    await page.setViewportSize({ width: 1440, height: 900 });
    await page.goto(`${WEB_URL}/login`, { waitUntil: "networkidle" });
    const heading = (await page.locator("h2").innerText()).trim();
    const labels = await page.locator("form label").allInnerTexts();
    const inputs = page.locator("form input");
    const emailType = await inputs.nth(0).getAttribute("type");
    const passwordType = await inputs.nth(1).getAttribute("type");
    const buttonText = (await page.locator("form button").innerText()).trim();
    await captureAndRecord(
      page,
      state,
      "web-login-baseline",
      [
        { id: "GUI-WEB-LOGIN-001", status: heading === "Đăng Nhập" ? "Pass" : "Fail", actual: `Heading is '${heading}'.` },
        { id: "GUI-WEB-LOGIN-002", status: labels[0] === "Email" && emailType === "email" ? "Pass" : "Fail", actual: `First label '${labels[0]}', input type '${emailType}'.` },
        { id: "GUI-WEB-LOGIN-003", status: passwordType === "password" ? "Pass" : "Fail", actual: `Password input type is '${passwordType}'.` },
        { id: "GUI-WEB-LOGIN-009", status: buttonText === "Đăng nhập" ? "Pass" : "Fail", actual: `Submit button text is '${buttonText}'.` },
      ],
      `heading=${heading}; labels=${labels.join("/")}; input types=${emailType}/${passwordType}; button=${buttonText}`,
    );
  });

  await safeScenario(state, "web-login-required-validation", async () => {
    await page.goto(`${WEB_URL}/login`, { waitUntil: "networkidle" });
    const inputs = page.locator("form input");
    await inputs.nth(1).fill("AnyPass1!");
    await page.locator("form button").click();
    const emailValidation = await inputs.nth(0).evaluate((element) => ({
      valid: element.checkValidity(),
      message: element.validationMessage,
    }));
    await inputs.nth(0).fill("nobody@example.test");
    await inputs.nth(1).fill("");
    await page.locator("form button").click();
    const passwordValidation = await inputs.nth(1).evaluate((element) => ({
      valid: element.checkValidity(),
      message: element.validationMessage,
    }));
    await captureAndRecord(
      page,
      state,
      "web-login-required-validation",
      [
        { id: "GUI-WEB-LOGIN-004", status: !emailValidation.valid && Boolean(emailValidation.message) ? "Pass" : "Fail", actual: `Empty email validity=${emailValidation.valid}; message='${emailValidation.message}'.` },
        { id: "GUI-WEB-LOGIN-005", status: !passwordValidation.valid && Boolean(passwordValidation.message) ? "Pass" : "Fail", actual: `Empty password validity=${passwordValidation.valid}; message='${passwordValidation.message}'.` },
      ],
      `Native required validation: email='${emailValidation.message}'; password='${passwordValidation.message}'`,
    );
  });

  await safeScenario(state, "web-login-invalid-feedback", async () => {
    await page.goto(`${WEB_URL}/login`, { waitUntil: "networkidle" });
    await fillWebLogin(page, `missing-${suffix}@example.test`, "WrongPass1!");
    await page.locator("form button").click();
    const feedback = page.locator(".bg-red-100");
    await feedback.waitFor({ timeout: 10000 });
    const text = (await feedback.innerText()).trim();
    await captureAndRecord(
      page,
      state,
      "web-login-invalid-feedback",
      [{ id: "GUI-WEB-LOGIN-006", status: text.length > 0 ? "Pass" : "Fail", actual: `Inline red feedback shown: '${text}'.` }],
      `Invalid-login inline feedback: ${text}`,
    );
  });

  await safeScenario(state, "web-login-forgot-navigation", async () => {
    await page.goto(`${WEB_URL}/login`, { waitUntil: "networkidle" });
    await page.evaluate(() => { window.__task3SpaMarker = "preserve-on-spa-navigation"; });
    await page.locator('a[href="/forgot-password"]').click();
    await page.waitForURL("**/forgot-password");
    const marker = await page.evaluate(() => window.__task3SpaMarker || null);
    await captureAndRecord(
      page,
      state,
      "web-login-forgot-navigation",
      [{ id: "GUI-WEB-LOGIN-007", status: marker ? "Pass" : "Fail", actual: `Reached /forgot-password; SPA marker ${marker ? "preserved" : "lost due to full document navigation"}.` }],
      `Forgot-password navigation reached ${page.url()}; SPA marker=${marker || "LOST"}`,
    );
  });

  await safeScenario(state, "web-login-register-navigation", async () => {
    await page.goto(`${WEB_URL}/login`, { waitUntil: "networkidle" });
    await page.evaluate(() => { window.__task3SpaMarker = "preserve-on-spa-navigation"; });
    await page.locator("main").locator('a[href="/register"]').click();
    await page.waitForURL("**/register");
    const marker = await page.evaluate(() => window.__task3SpaMarker || null);
    await captureAndRecord(
      page,
      state,
      "web-login-register-navigation",
      [{ id: "GUI-WEB-LOGIN-008", status: marker ? "Pass" : "Fail", actual: `Reached /register; SPA marker ${marker ? "preserved" : "lost"}.` }],
      `Registration navigation reached ${page.url()}; SPA marker=${marker || "LOST"}`,
    );
  });

  await safeScenario(state, "web-login-lockout-feedback", async () => {
    const email = `task3-lock-${suffix}@example.test`;
    const userId = await createUser(email);
    state.createdUserIds.add(userId);
    await page.goto(`${WEB_URL}/login`, { waitUntil: "networkidle" });
    const attempts = [];
    for (let attempt = 1; attempt <= 3; attempt += 1) {
      await fillWebLogin(page, email, "WrongPass1!");
      const responsePromise = page.waitForResponse((response) =>
        response.url().endsWith("/api/login") && response.request().method() === "POST",
      );
      await page.locator("form button").click();
      const response = await responsePromise;
      attempts.push(response.status());
      await page.locator(".bg-red-100").waitFor({ timeout: 10000 });
    }
    const feedback = (await page.locator(".bg-red-100").innerText()).trim();
    const distinguishesLockout = /khóa|lock|thời gian|minute|second/i.test(feedback);
    await captureAndRecord(
      page,
      state,
      "web-login-lockout-feedback",
      [{ id: "GUI-WEB-LOGIN-010", status: distinguishesLockout ? "Pass" : "Fail", actual: `Three wrong attempts returned HTTP ${attempts.join("/")}; UI still says '${feedback}'.` }],
      `Wrong-login HTTP sequence ${attempts.join("/")}; lockout-specific UI=${distinguishesLockout}`,
    );
    await cleanupUser(userId, adminToken);
    state.createdUserIds.delete(userId);
  });

  await safeScenario(state, "web-login-keyboard", async () => {
    await page.goto(`${WEB_URL}/login`, { waitUntil: "networkidle" });
    await page.evaluate(() => document.activeElement?.blur());
    await page.keyboard.press("Tab");
    const firstFocus = await page.evaluate(() => {
      const active = document.activeElement;
      return `${active?.tagName || "NONE"}:${active?.textContent?.trim() || active?.getAttribute("name") || ""}:tabindex=${active?.getAttribute("tabindex")}`;
    });
    const naturalOrder = firstFocus.startsWith("INPUT:");
    await captureAndRecord(
      page,
      state,
      "web-login-keyboard-focus",
      [{ id: "GUI-WEB-LOGIN-011", status: naturalOrder ? "Pass" : "Fail", actual: `First Tab target is ${firstFocus}.` }],
      `Keyboard first Tab target: ${firstFocus}`,
    );
  });

  await safeScenario(state, "web-login-responsive-320", async () => {
    await page.setViewportSize({ width: 320, height: 844 });
    await page.goto(`${WEB_URL}/login`, { waitUntil: "networkidle" });
    const metrics = await page.evaluate(() => ({
      innerWidth: window.innerWidth,
      scrollWidth: document.documentElement.scrollWidth,
      formRight: document.querySelector("form")?.getBoundingClientRect().right || 0,
    }));
    const fits = metrics.scrollWidth <= metrics.innerWidth && metrics.formRight <= metrics.innerWidth;
    await captureAndRecord(
      page,
      state,
      "web-login-responsive-320",
      [{ id: "GUI-WEB-LOGIN-012", status: fits ? "Pass" : "Fail", actual: `viewport=${metrics.innerWidth}, document scrollWidth=${metrics.scrollWidth}, form right=${metrics.formRight.toFixed(1)}.` }],
      `320px responsive metrics: ${JSON.stringify(metrics)}`,
    );
    await page.setViewportSize({ width: 1440, height: 900 });
  });

  await safeScenario(state, "web-login-trim", async () => {
    const email = `task3-trim-${suffix}@example.test`;
    const userId = await createUser(email);
    state.createdUserIds.add(userId);
    await page.goto(`${WEB_URL}/login`, { waitUntil: "networkidle" });
    await fillWebLogin(page, `  ${email}  `, "Task3Pass1!");
    await page.locator("form button").click();
    await page.waitForTimeout(600);
    const succeeded = new URL(page.url()).pathname === "/";
    const feedback = await page.locator(".bg-red-100").allInnerTexts();
    await captureAndRecord(
      page,
      state,
      "web-login-trim",
      [{ id: "GUI-WEB-LOGIN-013", status: succeeded ? "Pass" : "Fail", actual: succeeded ? "Whitespace was trimmed and login succeeded." : `Whitespace remained significant; login failed with '${feedback.join(" ")}'.` }],
      `Leading/trailing email whitespace login success=${succeeded}`,
    );
    await cleanupUser(userId, adminToken);
    state.createdUserIds.delete(userId);
  });
}

async function executeWebKeyboardOnly(page, state) {
  await page.goto(`${WEB_URL}/login`, { waitUntil: "networkidle" });
  await page.evaluate(() => document.activeElement?.blur());
  const sequence = [];
  for (let index = 0; index < 8; index += 1) {
    await page.keyboard.press("Tab");
    sequence.push(
      await page.evaluate(() => {
        const active = document.activeElement;
        return {
          tag: active?.tagName || "NONE",
          text: (active?.textContent || active?.getAttribute("placeholder") || "").trim(),
          type: active?.getAttribute("type"),
          tabindex: active?.getAttribute("tabindex"),
          outline: getComputedStyle(active).outlineStyle,
        };
      }),
    );
  }
  const firstInputIndex = sequence.findIndex((item) => item.tag === "INPUT");
  const positiveButtonIndex = sequence.findIndex((item) => item.tag === "BUTTON" && item.tabindex === "1");
  const positiveSubmitPrecedesInputs = positiveButtonIndex >= 0 && firstInputIndex >= 0 && positiveButtonIndex < firstInputIndex;
  const naturalOrder = !positiveSubmitPrecedesInputs;
  const summary = sequence.map((item) => `${item.tag}:${item.text || item.type || ""}[${item.tabindex || "auto"}]`).join(" > ");
  await captureAndRecord(
    page,
    state,
    "web-login-keyboard-focus",
    [{ id: "GUI-WEB-LOGIN-011", status: naturalOrder ? "Pass" : "Fail", actual: `First eight Tab targets: ${summary}. Positive-tabindex submit precedes inputs=${positiveSubmitPrecedesInputs}.` }],
    `Fresh no-focus Tab sequence: ${summary}`,
  );
}

async function executeWebRegister(page, state, adminToken, suffix) {
  await safeScenario(state, "web-register-baseline", async () => {
    await page.setViewportSize({ width: 1440, height: 900 });
    await page.goto(`${WEB_URL}/register`, { waitUntil: "networkidle" });
    const heading = (await page.locator("h1").innerText()).trim();
    const emailType = await page.locator("#register-email").getAttribute("type");
    const helper = (await page.locator("#register-password-help").innerText()).trim();
    const button = page.locator('button[type="submit"]');
    const buttonText = (await button.innerText()).trim();
    const background = await button.evaluate((element) => getComputedStyle(element).backgroundColor);
    const blue = /rgb\((?:37, 99, 235|29, 78, 216)\)/.test(background);
    await captureAndRecord(
      page,
      state,
      "web-register-baseline",
      [
        { id: "GUI-WEB-REGISTER-001", status: heading === "Đăng Ký Tài Khoản" ? "Pass" : "Fail", actual: `Heading is '${heading}'.` },
        { id: "GUI-WEB-REGISTER-002", status: emailType === "email" ? "Pass" : "Fail", actual: `Email input type is '${emailType}'.` },
        { id: "GUI-WEB-REGISTER-003", status: /8/.test(helper) && /@\$!%\*\?&/.test(helper) ? "Pass" : "Fail", actual: `Password helper text is '${helper}'.` },
        { id: "GUI-WEB-REGISTER-008", status: blue ? "Pass" : "Fail", actual: `Register button '${buttonText}' computed background ${background}.` },
      ],
      `heading=${heading}; email type=${emailType}; button background=${background}; helper=${helper}`,
    );
  });

  await safeScenario(state, "web-register-special-character", async () => {
    const email = `task3-special-${suffix}@example.test`;
    await page.goto(`${WEB_URL}/register`, { waitUntil: "networkidle" });
    const responsePromise = page.waitForResponse((response) =>
      response.url().endsWith("/api/register") && response.request().method() === "POST",
    );
    await fillRegister(page, { name: "Task3 Special Character", email, password: "Password123!" });
    await page.locator('button[type="submit"]').click();
    const response = await responsePromise;
    const body = await response.json();
    if (body.id) state.createdUserIds.add(body.id);
    await page.waitForURL("**/login");
    const passed = response.status() === 200 && new URL(page.url()).pathname === "/login";
    await captureAndRecord(
      page,
      state,
      "web-register-special-character",
      [{ id: "GUI-WEB-REGISTER-004", status: passed ? "Pass" : "Fail", actual: `Password123! produced HTTP ${response.status()} and final route ${page.url()}.` }],
      `Allowed special-character registration: HTTP ${response.status()}, final URL ${page.url()}`,
    );
  });

  await safeScenario(state, "web-register-weak-feedback", async () => {
    await page.goto(`${WEB_URL}/register`, { waitUntil: "networkidle" });
    await fillRegister(page, { name: "Task3 Weak", email: `task3-weak-${suffix}@example.test`, password: "weakpass" });
    await page.locator('button[type="submit"]').click();
    const alert = page.locator('[role="alert"]');
    await alert.waitFor({ timeout: 5000 });
    const text = (await alert.innerText()).trim();
    await captureAndRecord(
      page,
      state,
      "web-register-weak-feedback",
      [{ id: "GUI-WEB-REGISTER-005", status: /8|hoa|thường|số|special|đặc biệt/i.test(text) ? "Pass" : "Fail", actual: `Weak-password feedback shown: '${text}'.` }],
      `Weak-password feedback: ${text}`,
    );
  });

  await safeScenario(state, "web-register-duplicate", async () => {
    const email = `task3-duplicate-${suffix}@example.test`;
    const firstId = await createUser(email);
    state.createdUserIds.add(firstId);
    await page.goto(`${WEB_URL}/register`, { waitUntil: "networkidle" });
    const responsePromise = page.waitForResponse((response) =>
      response.url().endsWith("/api/register") && response.request().method() === "POST",
    );
    await fillRegister(page, { name: "Task3 Duplicate", email, password: "Password123!" });
    await page.locator('button[type="submit"]').click();
    const response = await responsePromise;
    const body = await response.json();
    if (body.id) state.createdUserIds.add(body.id);
    const rejected = response.status() >= 400;
    await captureAndRecord(
      page,
      state,
      "web-register-duplicate",
      [{ id: "GUI-WEB-REGISTER-006", status: rejected ? "Pass" : "Fail", actual: `Second registration for the same email returned HTTP ${response.status()} and ${rejected ? "showed an error" : "navigated as success"}.` }],
      `Duplicate-email registration HTTP ${response.status()}; rejected=${rejected}`,
    );
  });

  await safeScenario(state, "web-register-login-navigation", async () => {
    await page.goto(`${WEB_URL}/register`, { waitUntil: "networkidle" });
    await page.evaluate(() => { window.__task3SpaMarker = "preserve-on-spa-navigation"; });
    await page.locator("main").locator('a[href="/login"]').click();
    await page.waitForURL("**/login");
    const marker = await page.evaluate(() => window.__task3SpaMarker || null);
    await captureAndRecord(
      page,
      state,
      "web-register-login-navigation",
      [{ id: "GUI-WEB-REGISTER-007", status: marker ? "Pass" : "Fail", actual: `Reached /login; SPA marker ${marker ? "preserved" : "lost"}.` }],
      `Login navigation reached ${page.url()}; SPA marker=${marker || "LOST"}`,
    );
  });

  await safeScenario(state, "web-register-required", async () => {
    await page.goto(`${WEB_URL}/register`, { waitUntil: "networkidle" });
    await page.locator("#register-email").fill(`task3-required-${suffix}@example.test`);
    await page.locator("#register-password").fill("Password123!");
    await page.locator("#register-confirm-password").fill("Password123!");
    await page.locator('button[type="submit"]').click();
    const nameValidation = await page.locator("#register-name").evaluate((element) => ({ valid: element.checkValidity(), message: element.validationMessage }));
    await page.locator("#register-name").fill("Task3 Required");
    await page.locator("#register-email").fill("");
    await page.locator('button[type="submit"]').click();
    const emailValidation = await page.locator("#register-email").evaluate((element) => ({ valid: element.checkValidity(), message: element.validationMessage }));
    await captureAndRecord(
      page,
      state,
      "web-register-required",
      [
        { id: "GUI-WEB-REGISTER-009", status: !nameValidation.valid && Boolean(nameValidation.message) ? "Pass" : "Fail", actual: `Empty name validity=${nameValidation.valid}; message='${nameValidation.message}'.` },
        { id: "GUI-WEB-REGISTER-010", status: !emailValidation.valid && Boolean(emailValidation.message) ? "Pass" : "Fail", actual: `Empty email validity=${emailValidation.valid}; message='${emailValidation.message}'.` },
      ],
      `Required validation messages: name='${nameValidation.message}'; email='${emailValidation.message}'`,
    );
  });

  await safeScenario(state, "web-register-xss", async () => {
    const email = `task3-xss-${suffix}@example.test`;
    let dialogObserved = false;
    const xssDialogHandler = async (dialog) => {
      dialogObserved = true;
      await dialog.dismiss();
    };
    page.once("dialog", xssDialogHandler);
    await page.goto(`${WEB_URL}/register`, { waitUntil: "networkidle" });
    const responsePromise = page.waitForResponse((response) => response.url().endsWith("/api/register"));
    await fillRegister(page, { name: '<img src=x onerror=alert("xss")>', email, password: "Password123!" });
    await page.locator('button[type="submit"]').click();
    const response = await responsePromise;
    const body = await response.json();
    if (body.id) state.createdUserIds.add(body.id);
    await page.waitForTimeout(300);
    page.off("dialog", xssDialogHandler);
    await captureAndRecord(
      page,
      state,
      "web-register-xss",
      [{ id: "GUI-WEB-REGISTER-011", status: !dialogObserved ? "Pass" : "Fail", actual: `Payload submitted as text; script dialog observed=${dialogObserved}.` }],
      `XSS payload dialog executed=${dialogObserved}; React did not render supplied name on this transition screen`,
    );
  });

  await safeScenario(state, "web-register-network-error", async () => {
    await page.goto(`${WEB_URL}/register`, { waitUntil: "networkidle" });
    await page.route("**/api/register", (route) => route.abort("connectionrefused"));
    await fillRegister(page, { name: "Task3 Network", email: `task3-network-${suffix}@example.test`, password: "Password123!" });
    await page.locator('button[type="submit"]').click();
    const alert = page.locator('[role="alert"]');
    await alert.waitFor({ timeout: 5000 });
    const text = (await alert.innerText()).trim();
    await captureAndRecord(
      page,
      state,
      "web-register-network-error",
      [{ id: "GUI-WEB-REGISTER-012", status: text.length > 0 ? "Pass" : "Fail", mode: "MOCKED_NETWORK_FAILURE", actual: `Aborted register request produced visible feedback '${text}'.` }],
      `Mocked connection refusal produced UI feedback: ${text}`,
    );
    await page.unroute("**/api/register");
  });
}

async function executeAdminLogin(page, state, adminToken, suffix) {
  await safeScenario(state, "admin-login-baseline", async () => {
    await page.goto(ADMIN_URL, { waitUntil: "networkidle" });
    await page.evaluate(() => localStorage.removeItem("adminToken"));
    await page.reload({ waitUntil: "networkidle" });
    const heading = (await page.locator("h2").innerText()).trim();
    const labels = await page.locator("form label").count();
    const inputs = page.locator("form input");
    const passwordType = await inputs.nth(1).getAttribute("type");
    const dashboardVisible = await page.getByText("EShop Admin", { exact: true }).count();
    await captureAndRecord(
      page,
      state,
      "admin-login-baseline",
      [
        { id: "GUI-ADMIN-LOGIN-001", status: heading === "Admin Login" ? "Pass" : "Fail", actual: `Admin heading is '${heading}'.` },
        { id: "GUI-ADMIN-LOGIN-002", status: labels >= 2 ? "Pass" : "Fail", actual: `Admin login form contains ${labels} label elements for two inputs.` },
        { id: "GUI-ADMIN-LOGIN-008", status: passwordType === "password" ? "Pass" : "Fail", actual: `Admin password input type is '${passwordType}'.` },
        { id: "GUI-ADMIN-LOGIN-009", status: dashboardVisible === 0 ? "Pass" : "Fail", actual: `Without token, protected dashboard visible count=${dashboardVisible}; login form remains visible.` },
      ],
      `heading=${heading}; labels=${labels}; password type=${passwordType}; protected dashboard visible=${dashboardVisible}`,
    );
  });

  await safeScenario(state, "admin-login-invalid-dialog", async () => {
    await page.goto(ADMIN_URL, { waitUntil: "networkidle" });
    await page.evaluate(() => localStorage.removeItem("adminToken"));
    await page.reload({ waitUntil: "networkidle" });
    const inputs = page.locator("form input");
    await inputs.nth(0).fill("admin@eshop.com");
    await inputs.nth(1).fill("WrongPass1!");
    const dialogPromise = page.waitForEvent("dialog");
    const clickPromise = page.locator("form button").click();
    const dialog = await dialogPromise;
    const message = dialog.message();
    if (!dialog.handled) await dialog.dismiss();
    await clickPromise;
    const inlineFeedback = await page.locator('[role="alert"], .bg-red-100').count();
    await captureAndRecord(
      page,
      state,
      "admin-login-invalid-dialog",
      [{ id: "GUI-ADMIN-LOGIN-003", status: inlineFeedback > 0 ? "Pass" : "Fail", actual: `Native browser dialog captured with '${message}'; inline feedback count=${inlineFeedback}.` }],
      `Automation captured native alert('${message}'); no inline error banner was present`,
    );
  });

  await safeScenario(state, "admin-login-nonadmin-dialog", async () => {
    const email = `task3-nonadmin-${suffix}@example.test`;
    const userId = await createUser(email);
    state.createdUserIds.add(userId);
    await page.goto(ADMIN_URL, { waitUntil: "networkidle" });
    await page.evaluate(() => localStorage.removeItem("adminToken"));
    await page.reload({ waitUntil: "networkidle" });
    const inputs = page.locator("form input");
    await inputs.nth(0).fill(email);
    await inputs.nth(1).fill("Task3Pass1!");
    const dialogPromise = page.waitForEvent("dialog");
    const clickPromise = page.locator("form button").click();
    const dialog = await dialogPromise;
    const message = dialog.message();
    if (!dialog.handled) await dialog.dismiss();
    await clickPromise;
    const inlineFeedback = await page.locator('[role="alert"], .bg-red-100').count();
    await captureAndRecord(
      page,
      state,
      "admin-login-nonadmin-dialog",
      [{ id: "GUI-ADMIN-LOGIN-004", status: inlineFeedback > 0 ? "Pass" : "Fail", actual: `Non-admin login produced native dialog '${message}'; inline feedback count=${inlineFeedback}.` }],
      `Automation captured non-admin native alert('${message}'); no inline authorization banner was present`,
    );
    await cleanupUser(userId, adminToken);
    state.createdUserIds.delete(userId);
  });

  await safeScenario(state, "admin-login-success", async () => {
    await loginAdmin(page);
    const dashboard = await page.getByText("Dashboard", { exact: true }).count();
    const tokenPresent = await page.evaluate(() => Boolean(localStorage.getItem("adminToken")));
    await captureAndRecord(
      page,
      state,
      "admin-login-success",
      [{ id: "GUI-ADMIN-LOGIN-005", status: dashboard > 0 && tokenPresent ? "Pass" : "Fail", actual: `Dashboard visible=${dashboard > 0}; admin token stored=${tokenPresent}.` }],
      `Successful admin login: dashboard visible=${dashboard > 0}; token stored=${tokenPresent}`,
    );
  });

  await safeScenario(state, "admin-refresh-persistence", async () => {
    await page.reload({ waitUntil: "networkidle" });
    const dashboard = await page.getByText("EShop Admin", { exact: true }).count();
    const tokenPresent = await page.evaluate(() => Boolean(localStorage.getItem("adminToken")));
    await captureAndRecord(
      page,
      state,
      "admin-refresh-persistence",
      [{ id: "GUI-ADMIN-LOGIN-006", status: dashboard > 0 && tokenPresent ? "Pass" : "Fail", actual: `After reload, admin shell visible=${dashboard > 0}; token present=${tokenPresent}.` }],
      `F5/reload persistence: admin shell=${dashboard > 0}; token=${tokenPresent}`,
    );
  });

  await safeScenario(state, "admin-logout", async () => {
    await page.locator("li").filter({ hasText: /xuất/i }).last().click();
    const loginVisible = await page.getByText("Admin Login", { exact: true }).count();
    const tokenPresent = await page.evaluate(() => Boolean(localStorage.getItem("adminToken")));
    await captureAndRecord(
      page,
      state,
      "admin-logout",
      [{ id: "GUI-ADMIN-LOGIN-007", status: loginVisible > 0 && !tokenPresent ? "Pass" : "Fail", actual: `After logout, login form visible=${loginVisible > 0}; token present=${tokenPresent}.` }],
      `Admin logout: login form=${loginVisible > 0}; token remaining=${tokenPresent}`,
    );
  });
}

async function executeAdminCategories(context, page, state, adminToken, suffix) {
  await safeScenario(state, "admin-category-baseline", async () => {
    await loginAdmin(page);
    await openCategories(page);
    const heading = (await page.locator("h2").innerText()).trim();
    const headers = await page.locator("table thead th").allInnerTexts();
    const input = page.locator('input[placeholder*="danh"]');
    const placeholder = await input.getAttribute("placeholder");
    const addButton = page.locator("form button");
    const addText = (await addButton.innerText()).trim();
    const editButtons = await page.locator("tbody button").filter({ hasText: /Sửa|Edit/i }).count();
    await captureAndRecord(
      page,
      state,
      "admin-category-baseline",
      [
        { id: "GUI-ADMIN-CATEGORY-001", status: /Danh/.test(heading) && headers.length >= 3 ? "Pass" : "Fail", actual: `Heading '${heading}'; headers '${headers.join(" / ")}'.` },
        { id: "GUI-ADMIN-CATEGORY-002", status: Boolean(placeholder) && addText.length > 0 ? "Pass" : "Fail", actual: `Input placeholder '${placeholder}'; add button '${addText}'.` },
        { id: "GUI-ADMIN-CATEGORY-005", status: editButtons > 0 ? "Pass" : "Fail", actual: `Edit-button count across category rows=${editButtons}.` },
      ],
      `Category baseline: heading=${heading}; headers=${headers.join("/")}; edit buttons=${editButtons}`,
    );
  });

  await safeScenario(state, "admin-category-add", async () => {
    const name = `TASK3_ADD_${suffix}`;
    const responsePromise = page.waitForResponse((response) =>
      response.url().endsWith("/api/categories") && response.request().method() === "POST",
    );
    const input = page.locator('input[placeholder*="danh"]');
    await input.fill(name);
    await page.locator("form button").click();
    const response = await responsePromise;
    const body = await response.json();
    if (body.id) state.createdCategoryIds.add(body.id);
    await page.getByText(name, { exact: true }).waitFor({ timeout: 10000 });
    const reset = (await input.inputValue()) === "";
    await captureAndRecord(
      page,
      state,
      "admin-category-add",
      [{ id: "GUI-ADMIN-CATEGORY-003", status: response.ok() && reset ? "Pass" : "Fail", actual: `Create HTTP ${response.status()}; row visible; input reset=${reset}.` }],
      `Synthetic category ${name} created with HTTP ${response.status()}; input reset=${reset}`,
    );
  });

  await safeScenario(state, "admin-category-empty", async () => {
    let postedBody = null;
    await page.route("**/api/categories", async (route) => {
      if (route.request().method() === "POST") {
        postedBody = route.request().postDataJSON();
        await route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ message: "mocked", id: 999001 }) });
      } else {
        await route.continue();
      }
    });
    const input = page.locator('input[placeholder*="danh"]');
    await input.fill("");
    await page.locator("form button").click();
    await page.waitForTimeout(300);
    const required = await input.getAttribute("required");
    await captureAndRecord(
      page,
      state,
      "admin-category-empty",
      [{ id: "GUI-ADMIN-CATEGORY-004", status: postedBody === null ? "Pass" : "Fail", mode: "MOCKED_WRITE_PREVENTION", actual: `required attribute='${required}'; empty POST observed=${postedBody !== null}; payload=${JSON.stringify(postedBody)}.` }],
      `Empty-submit request intercepted to prevent database mutation; POST observed=${postedBody !== null}; required=${required}`,
    );
    await page.unroute("**/api/categories");
  });

  await safeScenario(state, "admin-category-delete", async () => {
    const name = `TASK3_DELETE_${suffix}`;
    const categoryId = await createCategory(name, adminToken);
    state.createdCategoryIds.add(categoryId);
    await page.reload({ waitUntil: "networkidle" });
    await openCategories(page);
    const row = page.locator("tbody tr").filter({ hasText: name });
    let dialogObserved = false;
    page.once("dialog", async (dialog) => {
      dialogObserved = true;
      await dialog.dismiss();
    });
    await row.locator("button").click();
    await row.waitFor({ state: "detached", timeout: 10000 });
    await captureAndRecord(
      page,
      state,
      "admin-category-delete",
      [
        { id: "GUI-ADMIN-CATEGORY-006", status: dialogObserved ? "Pass" : "Fail", actual: `Delete confirmation dialog observed=${dialogObserved}.` },
        { id: "GUI-ADMIN-CATEGORY-007", status: true ? "Pass" : "Fail", actual: `Synthetic empty category '${name}' disappeared after delete.` },
      ],
      `Synthetic category deleted; confirmation dialog observed=${dialogObserved}`,
    );
    state.createdCategoryIds.delete(categoryId);
  });

  await safeScenario(state, "admin-category-delete-with-product", async () => {
    const categoryName = `TASK3_IN_USE_${suffix}`;
    const categoryId = await createCategory(categoryName, adminToken);
    state.createdCategoryIds.add(categoryId);
    const productId = await createProduct(categoryId, suffix);
    state.createdProductIds.add(productId);
    await page.reload({ waitUntil: "networkidle" });
    await openCategories(page);
    const row = page.locator("tbody tr").filter({ hasText: categoryName });
    let dialogMessage = null;
    page.once("dialog", async (dialog) => {
      dialogMessage = dialog.message();
      await dialog.dismiss();
    });
    await row.locator("button").click();
    await page.waitForTimeout(500);
    const stillPresent = await page.locator("tbody tr").filter({ hasText: categoryName }).count();
    await captureAndRecord(
      page,
      state,
      "admin-category-delete-in-use",
      [{ id: "GUI-ADMIN-CATEGORY-008", status: stillPresent > 0 && Boolean(dialogMessage) ? "Pass" : "Fail", actual: `Category referenced by synthetic product remained=${stillPresent > 0}; error dialog=${dialogMessage || "NONE"}. Backend allowed deletion=${stillPresent === 0}.` }],
      `In-use synthetic category remained=${stillPresent > 0}; error feedback=${dialogMessage || "NONE"}`,
    );
    await cleanupProduct(productId);
    state.createdProductIds.delete(productId);
    await cleanupCategory(categoryId, adminToken);
    state.createdCategoryIds.delete(categoryId);
  });

  await safeScenario(state, "admin-category-empty-state", async () => {
    const emptyPage = await context.newPage();
    attachDiagnostics(emptyPage, state, "admin-empty-state");
    await emptyPage.route("**/api/categories", async (route) => {
      if (route.request().method() === "GET") {
        await route.fulfill({ status: 200, contentType: "application/json", body: "[]" });
      } else {
        await route.continue();
      }
    });
    await emptyPage.goto(ADMIN_URL, { waitUntil: "domcontentloaded" });
    await emptyPage.evaluate((token) => localStorage.setItem("adminToken", token), adminToken);
    await emptyPage.reload({ waitUntil: "networkidle" });
    await openCategories(emptyPage);
    const rows = await emptyPage.locator("tbody tr").count();
    const messageCount = await emptyPage.getByText(/Chưa có|No categor/i).count();
    await captureAndRecord(
      emptyPage,
      state,
      "admin-category-empty-state",
      [{ id: "GUI-ADMIN-CATEGORY-009", status: messageCount > 0 ? "Pass" : "Fail", mode: "MOCKED_EMPTY_API_STATE", actual: `Mocked empty category response rendered rows=${rows}; empty-state message count=${messageCount}.` }],
      `Mocked GET /categories=[]; rows=${rows}; empty-state message=${messageCount > 0}`,
    );
    await emptyPage.close();
  });

  await safeScenario(state, "admin-category-loading", async () => {
    const loadingPage = await context.newPage();
    attachDiagnostics(loadingPage, state, "admin-loading-state");
    await loadingPage.route("**/api/categories", async (route) => {
      if (route.request().method() === "GET") {
        await delay(2500);
        await route.fulfill({ status: 200, contentType: "application/json", body: "[]" });
      } else {
        await route.continue();
      }
    });
    await loadingPage.goto(ADMIN_URL, { waitUntil: "domcontentloaded" });
    await loadingPage.evaluate((token) => localStorage.setItem("adminToken", token), adminToken);
    await loadingPage.reload({ waitUntil: "domcontentloaded" });
    await loadingPage.locator("li").filter({ hasText: /Danh/ }).first().click();
    await loadingPage.waitForTimeout(400);
    const loadingCount = await loadingPage.getByText(/loading|đang tải/i).count();
    await captureAndRecord(
      loadingPage,
      state,
      "admin-category-loading",
      [{ id: "GUI-ADMIN-CATEGORY-010", status: loadingCount > 0 ? "Pass" : "Fail", mode: "MOCKED_SLOW_API", actual: `During a 2.5-second category delay, loading indicator count=${loadingCount}.` }],
      `Mocked 2.5s GET /categories delay; loading indicator visible=${loadingCount > 0}`,
    );
    await loadingPage.close();
  });

  await safeScenario(state, "admin-category-duplicate", async () => {
    const name = `TASK3_DUP_CATEGORY_${suffix}`;
    const firstId = await createCategory(name, adminToken);
    state.createdCategoryIds.add(firstId);
    await page.reload({ waitUntil: "networkidle" });
    await openCategories(page);
    const responsePromise = page.waitForResponse((response) => response.url().endsWith("/api/categories") && response.request().method() === "POST");
    await page.locator('input[placeholder*="danh"]').fill(name);
    await page.locator("form button").click();
    const response = await responsePromise;
    const body = await response.json();
    if (body.id) state.createdCategoryIds.add(body.id);
    const duplicates = await page.getByText(name, { exact: true }).count();
    await captureAndRecord(
      page,
      state,
      "admin-category-duplicate",
      [{ id: "GUI-ADMIN-CATEGORY-011", status: response.status() >= 400 ? "Pass" : "Fail", actual: `Duplicate category POST returned HTTP ${response.status()}; visible duplicate row count=${duplicates}.` }],
      `Duplicate category HTTP ${response.status()}; rows with same name=${duplicates}`,
    );
  });

  await safeScenario(state, "admin-category-long-name", async () => {
    const name = `TASK3_LONG_${suffix}_` + "L".repeat(260);
    const categoryId = await createCategory(name, adminToken);
    state.createdCategoryIds.add(categoryId);
    await page.reload({ waitUntil: "networkidle" });
    await openCategories(page);
    const row = page.locator("tbody tr").filter({ hasText: `TASK3_LONG_${suffix}_` });
    const metrics = await row.evaluate((element) => ({
      rowWidth: element.getBoundingClientRect().width,
      viewport: window.innerWidth,
      documentScrollWidth: document.documentElement.scrollWidth,
      whiteSpace: getComputedStyle(element.querySelectorAll("td")[1]).whiteSpace,
    }));
    const noOverflow = metrics.documentScrollWidth <= metrics.viewport;
    await captureAndRecord(
      page,
      state,
      "admin-category-long-name",
      [{ id: "GUI-ADMIN-CATEGORY-012", status: noOverflow ? "Pass" : "Fail", actual: `260+ character row: document scrollWidth=${metrics.documentScrollWidth}, viewport=${metrics.viewport}, white-space=${metrics.whiteSpace}.` }],
      `Long-name layout metrics: ${JSON.stringify(metrics)}`,
    );
  });

  await safeScenario(state, "admin-category-double-submit", async () => {
    let postCount = 0;
    await page.route("**/api/categories", async (route) => {
      if (route.request().method() === "POST") {
        postCount += 1;
        await delay(700);
        await route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ message: "mocked", id: 999100 + postCount }) });
      } else {
        await route.continue();
      }
    });
    const input = page.locator('input[placeholder*="danh"]');
    const button = page.locator("form button");
    await input.fill(`TASK3_DOUBLE_${suffix}`);
    await button.click({ clickCount: 2, delay: 20 });
    await page.waitForTimeout(1100);
    const disabled = await button.isDisabled();
    await captureAndRecord(
      page,
      state,
      "admin-category-double-submit",
      [{ id: "GUI-ADMIN-CATEGORY-013", status: postCount === 1 ? "Pass" : "Fail", mode: "MOCKED_SLOW_WRITE", actual: `Rapid double click generated ${postCount} POST request(s); button disabled after completion=${disabled}.` }],
      `Mocked 700ms POST delay; double-click request count=${postCount}; disabled=${disabled}`,
    );
    await page.unroute("**/api/categories");
  });
}

const mobileText = {
  login: /(Đăng nhập|ÄÄƒng nháº­p)/i,
  loginHeading: /(Đăng Nhập|ÄÄƒng Nháº­p)/i,
  back: /(Quay Lại|Quay Láº¡i)/i,
  registerNow: /(Đăng ký ngay|ÄÄƒng kÃ½ ngay)/i,
  forgot: /(Quên mật khẩu|QuÃªn máº­t kháº©u)/i,
  registerHeading: /(Đăng Ký Tài Khoản|ÄÄƒng KÃ½ TÃ i Khoáº£n)/i,
  forgotHeading: /(Quên Mật Khẩu|QuÃªn Máº­t Kháº©u)/i,
};

async function proxyMobileApi(context) {
  await context.route("http://192.168.10.13:3000/api/**", async (route) => {
    const request = route.request();
    const target = request.url().replace("http://192.168.10.13:3000/api", API_URL);
    try {
      const response = await fetch(target, {
        method: request.method(),
        headers: { "Content-Type": (await request.headerValue("content-type")) || "application/json" },
        body: ["GET", "HEAD"].includes(request.method()) ? undefined : request.postData(),
      });
      await route.fulfill({
        status: response.status,
        headers: { "Content-Type": response.headers.get("content-type") || "application/json" },
        body: Buffer.from(await response.arrayBuffer()),
      });
    } catch (error) {
      await route.abort("connectionfailed");
    }
  });
}

async function openMobileLogin(page) {
  await page.goto(MOBILE_URL, { waitUntil: "domcontentloaded", timeout: 30000 });
  await page.waitForTimeout(2500);
  const loginTarget = page.getByText(mobileText.login, { exact: true }).first();
  await loginTarget.waitFor({ timeout: 20000 });
  await loginTarget.click();
  await page.getByText(mobileText.loginHeading, { exact: true }).first().waitFor({ timeout: 10000 });
}

async function executeMobileLogin(browser, state, adminToken, suffix) {
  const context = await browser.newContext({
    viewport: { width: 390, height: 844 },
    deviceScaleFactor: 2,
    isMobile: true,
    hasTouch: true,
    ...(state.definition.contextOptions || {}),
  });
  await proxyMobileApi(context);
  const page = await context.newPage();
  attachDiagnostics(page, state, "mobile-login");

  await safeScenario(state, "mobile-login-baseline", async () => {
    await openMobileLogin(page);
    const bodyText = await page.locator("body").innerText();
    const headingVisible = mobileText.loginHeading.test(bodyText);
    const usernameLabel = /Username/.test(bodyText);
    const emailLabel = /(^|\n)Email(\n|$)/m.test(bodyText);
    const inputs = page.locator("input");
    const passwordType = await inputs.nth(1).getAttribute("type");
    const signIn = page.getByText("Sign In", { exact: true });
    const buttonBox = await signIn.locator("..").boundingBox();
    const touchTargetPass = Boolean(buttonBox && buttonBox.width >= 44 && buttonBox.height >= 44);
    await captureAndRecord(
      page,
      state,
      "mobile-login-baseline",
      [
        { id: "GUI-MOBILE-LOGIN-001", status: headingVisible ? "Pass" : "Fail", actual: `Login heading visible=${headingVisible}. Runtime is Expo Web, not Expo Go.` },
        { id: "GUI-MOBILE-LOGIN-002", status: emailLabel && !usernameLabel ? "Pass" : "Fail", actual: `Visible Username label=${usernameLabel}; standalone Email label=${emailLabel}.` },
        { id: "GUI-MOBILE-LOGIN-003", status: passwordType === "password" ? "Pass" : "Fail", actual: `Rendered password input type is '${passwordType}'.` },
        { id: "GUI-MOBILE-LOGIN-004", status: (await signIn.innerText()).trim() === "Đăng nhập" ? "Pass" : "Fail", actual: `Rendered submit label is '${(await signIn.innerText()).trim()}'.` },
        { id: "GUI-MOBILE-LOGIN-010", status: touchTargetPass ? "Pass" : "Fail", actual: `Sign In touch target bounding box=${JSON.stringify(buttonBox)} CSS px.` },
      ],
      `Expo Web mobile login: heading=${headingVisible}; Username label=${usernameLabel}; password type=${passwordType}; Sign In box=${JSON.stringify(buttonBox)}`,
    );
  });

  await safeScenario(state, "mobile-login-invalid-feedback", async () => {
    const inputs = page.locator("input");
    await inputs.nth(0).fill(`missing-mobile-${suffix}@example.test`);
    await inputs.nth(1).fill("WrongPass1!");
    await page.getByText("Sign In", { exact: true }).click();
    await page.waitForTimeout(800);
    const bodyText = await page.locator("body").innerText();
    const feedbackVisible = /thất bại|kiểm tra lại|failed/i.test(bodyText);
    await captureAndRecord(
      page,
      state,
      "mobile-login-invalid-feedback",
      [{ id: "GUI-MOBILE-LOGIN-005", status: feedbackVisible ? "Pass" : "Fail", actual: `Invalid-login feedback visible=${feedbackVisible}.` }],
      `Proxied live backend invalid login; feedback visible=${feedbackVisible}`,
    );
  });

  await safeScenario(state, "mobile-login-back", async () => {
    await page.getByText(mobileText.back, { exact: true }).click();
    await page.waitForTimeout(300);
    const homeLogin = await page.getByText(mobileText.login, { exact: true }).count();
    await captureAndRecord(
      page,
      state,
      "mobile-login-back",
      [{ id: "GUI-MOBILE-LOGIN-006", status: homeLogin > 0 ? "Pass" : "Fail", actual: `After Quay Lại, home login control count=${homeLogin}.` }],
      `Mobile back navigation returned to home=${homeLogin > 0}`,
    );
  });

  await safeScenario(state, "mobile-register-navigation", async () => {
    await openMobileLogin(page);
    await page.getByText(mobileText.registerNow).click();
    await page.waitForTimeout(300);
    const heading = await page.getByText(mobileText.registerHeading, { exact: true }).count();
    await captureAndRecord(
      page,
      state,
      "mobile-register-navigation",
      [{ id: "GUI-MOBILE-LOGIN-007", status: heading > 0 ? "Pass" : "Fail", actual: `Registration heading visible after navigation=${heading > 0}.` }],
      `Mobile registration navigation success=${heading > 0}`,
    );
  });

  await safeScenario(state, "mobile-forgot-navigation", async () => {
    await openMobileLogin(page);
    await page.getByText(mobileText.forgot).click();
    await page.waitForTimeout(300);
    const heading = await page.getByText(mobileText.forgotHeading, { exact: true }).count();
    await captureAndRecord(
      page,
      state,
      "mobile-forgot-navigation",
      [{ id: "GUI-MOBILE-LOGIN-008", status: heading > 0 ? "Pass" : "Fail", actual: `Forgot-password heading visible after navigation=${heading > 0}.` }],
      `Mobile forgot-password navigation success=${heading > 0}`,
    );
  });

  await safeScenario(state, "mobile-login-success", async () => {
    const email = `task3-mobile-${suffix}@example.test`;
    const displayName = `Task3 Mobile ${suffix}`;
    const userId = await createUser(email, "Task3Pass1!", displayName);
    state.createdUserIds.add(userId);
    await openMobileLogin(page);
    const inputs = page.locator("input");
    await inputs.nth(0).fill(email);
    await inputs.nth(1).fill("Task3Pass1!");
    await page.getByText("Sign In", { exact: true }).click();
    await page.waitForTimeout(1000);
    const bodyText = await page.locator("body").innerText();
    const updated = bodyText.includes(displayName);
    await captureAndRecord(
      page,
      state,
      "mobile-login-success",
      [{ id: "GUI-MOBILE-LOGIN-009", status: updated ? "Pass" : "Fail", actual: `After live proxied login, header contains synthetic display name=${updated}.` }],
      `Mobile login through local API proxy; header updated with synthetic name=${updated}`,
    );
    await cleanupUser(userId, adminToken);
    state.createdUserIds.delete(userId);
  });

  await safeScenario(state, "mobile-soft-keyboard", async () => {
    await openMobileLogin(page);
    await page.locator("input").first().focus();
    const before = await page.evaluate(() => ({ width: window.innerWidth, height: window.innerHeight, visualHeight: window.visualViewport?.height || null }));
    await page.waitForTimeout(300);
    const after = await page.evaluate(() => ({ width: window.innerWidth, height: window.innerHeight, visualHeight: window.visualViewport?.height || null }));
    await captureAndRecord(
      page,
      state,
      "mobile-soft-keyboard-not-observable",
      [{ id: "GUI-MOBILE-LOGIN-011", status: "Not Observable", mode: "EXPO_WEB_DESKTOP_BROWSER", actual: `Desktop/headless Expo Web cannot display a real mobile soft keyboard. Before=${JSON.stringify(before)}, after=${JSON.stringify(after)}.` }],
      `Soft keyboard cannot be evidenced in Expo Web/headless browser; viewport before=${JSON.stringify(before)} after=${JSON.stringify(after)}`,
    );
  });

  await context.close();
}

async function cleanupState(state, adminToken) {
  for (const productId of [...state.createdProductIds]) {
    await cleanupProduct(productId).catch(() => {});
  }
  for (const categoryId of [...state.createdCategoryIds]) {
    await cleanupCategory(categoryId, adminToken).catch(() => {});
  }
  for (const userId of [...state.createdUserIds]) {
    await cleanupUser(userId, adminToken).catch(() => {});
  }
}

async function executePlatform(platformId) {
  const definition = PLATFORM_DEFINITIONS[platformId];
  if (!definition) throw new Error(`Unknown platform '${platformId}'.`);
  const browser = await definition.launcher.launch(definition.launchOptions);
  const state = makeRunState(platformId, definition, browser.version());
  const context = await browser.newContext({
    viewport: { width: 1440, height: 900 },
    ...(definition.contextOptions || {}),
  });
  const page = await context.newPage();
  attachDiagnostics(page, state, "desktop-web-admin");
  let adminToken = null;
  const suffix = `${platformId.replace(/[^a-z0-9]/g, "-")}-${Date.now()}`;

  try {
    adminToken = await getAdminToken();
    if (keyboardOnly) {
      const existingPath = path.join(RESULTS_ROOT, `${platformId}.json`);
      if (!fs.existsSync(existingPath)) {
        throw new Error(`Cannot run --keyboard-only without existing result: ${existingPath}`);
      }
      const existing = JSON.parse(fs.readFileSync(existingPath, "utf8"));
      const retained = existing.results.filter((item) => item.checklist_id !== "GUI-WEB-LOGIN-011");
      state.results.push(...retained);
      state.console.push(...(existing.console || []));
      state.pageErrors.push(...(existing.page_errors || []));
      state.sequence = 6;
      await executeWebKeyboardOnly(page, state);
    } else if (mobileOnly) {
      const existingPath = path.join(RESULTS_ROOT, `${platformId}.json`);
      if (!fs.existsSync(existingPath)) {
        throw new Error(`Cannot run --mobile-only without existing result: ${existingPath}`);
      }
      const existing = JSON.parse(fs.readFileSync(existingPath, "utf8"));
      const retained = existing.results.filter((item) => !item.checklist_id.startsWith("GUI-MOBILE-"));
      state.results.push(...retained);
      state.console.push(...(existing.console || []).filter((item) => item.scope !== "mobile-login"));
      state.pageErrors.push(...(existing.page_errors || []).filter((item) => item.scope !== "mobile-login"));
      state.sequence = Math.max(
        0,
        ...retained.map((item) => Number(path.basename(item.evidence_path).split("-")[0]) || 0),
      );
    } else {
      await executeWebLogin(page, state, adminToken, suffix);
      await executeWebRegister(page, state, adminToken, suffix);
      await executeAdminLogin(page, state, adminToken, suffix);
      await executeAdminCategories(context, page, state, adminToken, suffix);
    }
    if (!keyboardOnly) await executeMobileLogin(browser, state, adminToken, suffix);
  } finally {
    if (adminToken) await cleanupState(state, adminToken);
    await context.close().catch(() => {});
    await browser.close().catch(() => {});
  }

  const resultIds = state.results.map((item) => item.checklist_id);
  const missingIds = expectedIds.filter((id) => !resultIds.includes(id));
  const duplicateIds = resultIds.filter((id, index) => resultIds.indexOf(id) !== index);
  const unexpectedIds = resultIds.filter((id) => !expectedIds.includes(id));
  const summary = {
    platform_id: platformId,
    platform_label: definition.label,
    browser_version: state.browserVersion,
    os_host: `Windows ${os.release()}`,
    device: definition.device,
    eligible_for_hw03_required_three: definition.eligible,
    platform_note: definition.note,
    expected_checklist_items: expectedIds.length,
    executed_result_rows: state.results.length,
    pass: state.results.filter((item) => item.status === "Pass").length,
    fail: state.results.filter((item) => item.status === "Fail").length,
    not_observable: state.results.filter((item) => item.status === "Not Observable").length,
    evidence_files: new Set(state.results.map((item) => item.evidence_path)).size,
    missing_ids: missingIds,
    duplicate_ids: [...new Set(duplicateIds)],
    unexpected_ids: [...new Set(unexpectedIds)],
    scenario_errors: state.runErrors,
  };

  fs.writeFileSync(
    path.join(RESULTS_ROOT, `${platformId}.json`),
    JSON.stringify({ summary, results: state.results, console: state.console, page_errors: state.pageErrors }, null, 2),
    "utf8",
  );
  return { summary, results: state.results };
}

function toCsv(rows) {
  if (!rows.length) return "";
  const headers = Object.keys(rows[0]);
  const escape = (value) => {
    const text = value === null || value === undefined ? "" : String(value);
    return /[",\r\n]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
  };
  return [headers.join(","), ...rows.map((row) => headers.map((header) => escape(row[header])).join(","))].join("\n") + "\n";
}

async function main() {
  const runs = [];
  for (const platformId of requestedPlatforms) {
    process.stdout.write(`Running Task 3 on ${platformId}...\n`);
    try {
      const run = await executePlatform(platformId);
      runs.push(run);
      process.stdout.write(
        `Finished ${platformId}: ${run.summary.executed_result_rows}/${run.summary.expected_checklist_items} rows, ` +
          `${run.summary.evidence_files} screenshots, ${run.summary.scenario_errors.length} scenario errors.\n`,
      );
    } catch (error) {
      runs.push({
        summary: {
          platform_id: platformId,
          platform_label: PLATFORM_DEFINITIONS[platformId]?.label || platformId,
          eligible_for_hw03_required_three: Boolean(PLATFORM_DEFINITIONS[platformId]?.eligible),
          fatal_error: error.stack || error.message,
        },
        results: [],
      });
      process.stderr.write(`Fatal ${platformId}: ${error.stack || error.message}\n`);
    }
  }

  const existingFiles = fs
    .readdirSync(RESULTS_ROOT)
    .filter((file) => file.endsWith(".json") && file !== "run-summary.json");
  for (const file of existingFiles) {
    const platformId = path.basename(file, ".json");
    if (runs.some((run) => run.summary.platform_id === platformId)) continue;
    try {
      const existing = JSON.parse(fs.readFileSync(path.join(RESULTS_ROOT, file), "utf8"));
      if (existing.summary && Array.isArray(existing.results)) {
        runs.push({ summary: existing.summary, results: existing.results });
      }
    } catch (error) {
      process.stderr.write(`Skipped unreadable prior result ${file}: ${error.message}\n`);
    }
  }

  runs.sort((left, right) => left.summary.platform_id.localeCompare(right.summary.platform_id));
  const allResults = runs.flatMap((run) => run.results);
  fs.writeFileSync(path.join(RESULTS_ROOT, "Task3_Cross_Platform_Results.csv"), toCsv(allResults), "utf8");
  fs.writeFileSync(
    path.join(RESULTS_ROOT, "run-summary.json"),
    JSON.stringify(
      {
        generated_at: new Date().toISOString(),
        student: STUDENT,
        requirement: "Chrome + Firefox + Safari or Android Chrome; at least three real/cloud/physical platforms",
        eligible_successful_platforms: runs.filter(
          (run) => run.summary.eligible_for_hw03_required_three && run.summary.executed_result_rows === expectedIds.length,
        ).length,
        required_eligible_platforms: 3,
        task3_status: runs.filter(
          (run) => run.summary.eligible_for_hw03_required_three && run.summary.executed_result_rows === expectedIds.length,
        ).length >= 3
          ? "COMPLETE"
          : "BLOCKED_THIRD_REQUIRED_PLATFORM",
        platforms: runs.map((run) => run.summary),
      },
      null,
      2,
    ),
    "utf8",
  );

  const fatalCount = runs.filter((run) => run.summary.fatal_error).length;
  process.stdout.write(`Task 3 runner complete: ${allResults.length} result rows; fatal platforms=${fatalCount}.\n`);
  process.exitCode = fatalCount > 0 ? 2 : 0;
}

main().catch((error) => {
  console.error(error);
  process.exit(2);
});
