// @ts-check
const path = require('path');
const { defineConfig, devices } = require('@playwright/test');

const studentId = process.env.STUDENT_ID || '23127271';
const featureName = process.env.FEATURE_NAME || 'adhoc';
// Default must NOT be fr03 — bare `npx playwright test` must not overwrite Feature A reports.
const featureSlug = process.env.FEATURE_SLUG || 'adhoc';
const browserName = process.env.BROWSER_PROJECT || 'chromium';
const isoTimestamp = process.env.RUN_TIMESTAMP || new Date().toISOString();

const reportDir =
  process.env.PLAYWRIGHT_HTML_OUTPUT_DIR ||
  process.env.HTML_REPORT_DIR ||
  path.join('reports', 'html', featureSlug, browserName);

const reportTitle =
  process.env.PLAYWRIGHT_HTML_TITLE ||
  `Run by: ${studentId} | ${featureName} | ${browserName} | ${isoTimestamp}`;

const baseURL = process.env.BASE_URL || 'http://localhost:5173';

/** @type {import('@playwright/test').PlaywrightTestConfig} */
module.exports = defineConfig({
  testDir: './tests',
  fullyParallel: false,
  forbidOnly: !!process.env.CI,
  retries: 0,
  workers: 1,
  timeout: 60_000,
  expect: { timeout: 15_000 },
  reporter: [
    ['list'],
    [
      'html',
      {
        open: 'never',
        outputFolder: reportDir,
        title: reportTitle,
      },
    ],
  ],
  use: {
    baseURL,
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'off',
  },
  outputDir: path.join('test-results', featureSlug, browserName),
  metadata: {
    runBy: `Run by: ${studentId}`,
    studentId,
    feature: featureName,
    browser: browserName,
    timestamp: isoTimestamp,
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
  ],
});
