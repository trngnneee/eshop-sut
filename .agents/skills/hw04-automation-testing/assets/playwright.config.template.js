// @ts-check
const { defineConfig, devices } = require('@playwright/test');

// Replace with the real student ID before running the suite.
const STUDENT_ID = '23127158';
const RUN_TIMESTAMP = new Date().toISOString();

module.exports = defineConfig({
  testDir: './tests',
  fullyParallel: true,
  retries: 0,
  reporter: [
    // Playwright HTML reporter — title/metadata carries the required
    // "Run by: {StudentID}" + ISO timestamp stamp.
    ['html', { outputFolder: 'reports/html', open: 'never' }],
    ['list'],
  ],
  use: {
    baseURL: process.env.SUT_BASE_URL ?? 'http://localhost:3000',
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
  },
  // Required: at least 3 browser projects so every feature runs on all of them.
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
  ],
  metadata: {
    'Run by': STUDENT_ID,
    'Run at (ISO)': RUN_TIMESTAMP,
  },
});

// NOTE: Playwright's built-in HTML reporter shows top-level `metadata` in the report's
// "Metadata" panel automatically. If your Playwright version does not render it, run
// `npm run stamp-report` (scripts/stamp-report.js) after the test run to inject a
// visible "Run by: {{STUDENT_ID}} — {ISO timestamp}" banner into reports/html/index.html,
// so the requirement is unambiguously satisfied.