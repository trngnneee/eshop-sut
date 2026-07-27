import { defineConfig, devices } from '@playwright/test';

const STUDENT_ID = '23127207';
const targetBrowser = process.env.BROWSER || 'chromium';
const reportFolder = `reports/${targetBrowser}`;

export default defineConfig({
  testDir: './tests',
  timeout: 30000,
  expect: {
    timeout: 5000,
  },
  fullyParallel: false,
  forbidOnly: !!process.env.CI,
  retries: 0,
  workers: 1,
  reporter: [
    [
      'html',
      {
        outputFolder: reportFolder,
        open: 'never',
        pageTitle: `Run by: ${STUDENT_ID} | EShop Login Test Report (${targetBrowser})`,
      },
    ],
    ['list'],
  ],
  use: {
    baseURL: 'http://localhost:5173',
    trace: 'on',
    screenshot: 'on',
    video: 'on',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
  ],
});
