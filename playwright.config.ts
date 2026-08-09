import { defineConfig, devices } from '@playwright/test';

/**
 * HW04 - Automation Testing Configuration
 * Student: Phan Quốc Thịnh
 * Student ID: 23127486
 * Class: 23KTPM3
 */
export default defineConfig({
  testDir: './tests',
  timeout: 30_000,
  expect: {
    timeout: 5_000,
  },
  fullyParallel: false,
  workers: 1,
  retries: 0,
  reporter: [
    ['html', {
      outputFolder: 'playwright-report',
      open: 'never',
    }],
    ['list'],
    ['json', { outputFile: 'test-results/test-results.json' }],
  ],
  use: {
    baseURL: 'http://localhost:5173',
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  metadata: {
    'Run by': '23127486',
    'Student Name': 'Phan Quốc Thịnh',
    'Class': '23KTPM3',
    'Assignment': 'HW04 - Automation Testing',
    'Timestamp': new Date().toISOString(),
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
      use: { ...devices['Desktop WebKit'] },
    },
  ],
  webServer: [
    {
      command: 'node backend/server.js',
      port: 3000,
      reuseExistingServer: true,
      stdout: 'pipe',
      stderr: 'pipe',
    },
    {
      command: 'npm.cmd --prefix frontend-web run dev',
      port: 5173,
      reuseExistingServer: true,
      stdout: 'pipe',
      stderr: 'pipe',
    },
    {
      command: 'npm.cmd --prefix frontend-admin run dev',
      port: 5174,
      reuseExistingServer: true,
      stdout: 'pipe',
      stderr: 'pipe',
    },
  ],
});
