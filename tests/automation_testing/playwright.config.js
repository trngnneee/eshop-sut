// @ts-check
const { defineConfig, devices } = require('@playwright/test');

const STUDENT_ID = '23127438';
const STUDENT_NAME = 'Đặng Trường Nguyên';

module.exports = defineConfig({
  testDir: './e2e',
  fullyParallel: false,
  retries: 0,
  reporter: [
    [
      'html',
      {
        open: 'never',
        title: `EShop Automation — FR-04 Profile — Run by: ${STUDENT_ID} — ${STUDENT_NAME}`,
      },
    ],
    ['list'],
  ],
  metadata: {
    'Run by': `${STUDENT_ID} — ${STUDENT_NAME}`,
    'Timestamp (ISO)': new Date().toISOString(),
    'SUT': 'EShop — Frontend Web (http://localhost:5173)',
  },
  use: {
    baseURL: 'http://localhost:5173',
    screenshot: 'only-on-failure',
    trace: 'retain-on-failure',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
  ],
  webServer: [
    {
      command: 'node server.js',
      cwd: '../backend',
      port: 3000,
      reuseExistingServer: true,
      timeout: 30_000,
    },
    {
      command: 'npm run dev',
      cwd: '../frontend-web',
      port: 5173,
      reuseExistingServer: true,
      timeout: 60_000,
    },
  ],
});
