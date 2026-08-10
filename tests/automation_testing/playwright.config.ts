import { defineConfig, devices } from '@playwright/test';

// Anti-cheat: report phải hiển thị "Run by: {StudentID}" + ISO timestamp.
const STUDENT_ID = process.env.STUDENT_ID || '23127438';
const RUN_AT = new Date().toISOString();

export default defineConfig({
  testDir: './tests',
  // Backend SQLite dùng chung cho mọi browser (lockout counter, coupon usage, categories)
  // → chạy tuần tự để các kịch bản stateful không phá nhau.
  fullyParallel: false,
  workers: 1,
  timeout: 60_000,
  expect: { timeout: 7_000 },
  reporter: [
    [
      'html',
      {
        outputFolder: process.env.REPORT_DIR || 'reports/all',
        open: 'never',
        title: `Run by: ${STUDENT_ID} — ${RUN_AT}`,
      },
    ],
    ['list'],
  ],
  metadata: {
    'Run by': STUDENT_ID,
    'Run at (ISO)': RUN_AT,
    SUT: 'EShop — FR-02 Login/Lockout, FR-09 Coupon, FR-14 Category CRUD',
  },
  use: {
    baseURL: 'http://localhost:5173',
    locale: 'en-US', // cố định locale để assert số tiền định dạng toLocaleString()
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
      cwd: '../../backend',
      port: 3000,
      reuseExistingServer: true,
    },
    {
      // gọi thẳng vite (npm .bin bị copy thay vì symlink trên máy này → hỏng relative import)
      command: 'node node_modules/vite/bin/vite.js',
      cwd: '../../frontend-web',
      port: 5173,
      reuseExistingServer: true,
    },
    {
      command: 'node node_modules/vite/bin/vite.js',
      cwd: '../../frontend-admin',
      port: 5174,
      reuseExistingServer: true,
    },
  ],
});
