// playwright.config.js
const { defineConfig, devices } = require('@playwright/test');

module.exports = defineConfig({
  testDir: './tests/e2e',
  timeout: 30_000,
  expect: { timeout: 5_000 },
  fullyParallel: false,        // run sequentially — SUT has shared state (SQLite)
  retries: 0,
  workers: 1,
  reporter: [
    ['list'],
    ['html', { outputFolder: 'playwright-report', open: 'never' }],
    ['json', { outputFile: 'test-results/results.json' }],
  ],

  use: {
    baseURL: 'http://localhost:5173',   // frontend-web
    headless: true,
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    trace: 'retain-on-failure',
    locale: 'vi-VN',
  },

  projects: [
    {
      name: 'chromium',
      testIgnore: '**/forgot-password-mobile.spec.js',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'mobile-chromium',
      testMatch: '**/forgot-password-mobile.spec.js',
      use: {
        ...devices['Desktop Chrome'],
        baseURL: process.env.MOBILE_URL || 'http://localhost:8081',
      },
    },
  ],

  webServer: process.env.SKIP_MOBILE_SERVER
    ? undefined
    : {
        command: 'npx expo start --web --port 8081',
        cwd: './frontend-mobile',
        url: 'http://localhost:8081',
        reuseExistingServer: true,
        timeout: 120_000,
      },

  // Uncomment if you want Playwright to start the SUT automatically:
  // webServer: {
  //   command: 'bash run_servers.sh',
  //   url: 'http://localhost:5173',
  //   reuseExistingServer: true,
  //   timeout: 60_000,
  // },
});
