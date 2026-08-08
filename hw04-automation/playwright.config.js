// @ts-check
const { defineConfig, devices } = require("@playwright/test");

// Replace with the real student ID before running the suite.
const STUDENT_ID = "23127158";
const RUN_TIMESTAMP = new Date().toISOString();

module.exports = defineConfig({
  testDir: "./tests",
  fullyParallel: true,
  retries: 0,
  reporter: [
    ["html", { outputFolder: "reports/html", open: "never" }],
    ["list"],
  ],
  use: {
    baseURL: process.env.SUT_BASE_URL ?? "http://localhost:5173",
    trace: "retain-on-failure",
    screenshot: "only-on-failure",
  },
  projects: [
    { name: "chromium", use: { ...devices["Desktop Chrome"] } },
    { name: "firefox", use: { ...devices["Desktop Firefox"] } },
    { name: "webkit", use: { ...devices["Desktop Safari"] } },
  ],
  metadata: {
    "Run by": STUDENT_ID,
    "Run at (ISO)": RUN_TIMESTAMP,
  },
});

// Playwright HTML reporter should show top-level metadata in the report.
// If not, run `npm run stamp-report` after tests to inject a visible banner.
