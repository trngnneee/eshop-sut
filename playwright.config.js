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
      use: { ...devices['Desktop Chrome'] },
    },
  ],

  // Uncomment if you want Playwright to start the SUT automatically:
  // webServer: {
  //   command: 'bash run_servers.sh',
  //   url: 'http://localhost:5173',
  //   reuseExistingServer: true,
  //   timeout: 60_000,
  // },
});
