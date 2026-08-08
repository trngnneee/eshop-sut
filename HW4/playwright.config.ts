import { defineConfig, devices } from '@playwright/test';

const STUDENT_ID = '23127207';

// FEATURE selects which spec file(s) run and which app (web :5173 vs admin :5174) is under test.
// BROWSER only names which report sub-folder the HTML output goes into; the actual browser
// engine used is controlled by Playwright's --project flag (chromium/firefox/webkit).
const FEATURE = process.env.FEATURE || 'login';
const BROWSER = process.env.BROWSER || 'chromium';

type FeatureConfig = {
  baseURL: string;
  testMatch: RegExp;
  label: string;
};

const FEATURE_CONFIG: Record<string, FeatureConfig> = {
  login: {
    baseURL: 'http://localhost:5173',
    testMatch: /login.*\.spec\.ts/,
    label: 'FR-02 Login & Lockout',
  },
  cart: {
    baseURL: 'http://localhost:5173',
    testMatch: /cart.*\.spec\.ts/,
    label: 'FR-07 Shopping Cart',
  },
  dashboard: {
    baseURL: 'http://localhost:5174',
    testMatch: /dashboard.*\.spec\.ts/,
    label: 'FR-13 Admin Dashboard',
  },
};

const cfg = FEATURE_CONFIG[FEATURE];
if (!cfg) {
  throw new Error(
    `Unknown FEATURE="${FEATURE}". Expected one of: ${Object.keys(FEATURE_CONFIG).join(', ')}`,
  );
}

const reportFolder = `reports/${FEATURE}/${BROWSER}`;

export default defineConfig({
  testDir: './tests',
  testMatch: cfg.testMatch,
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
        pageTitle: `Run by: ${STUDENT_ID} | ${cfg.label} | ${BROWSER}`,
      },
    ],
    ['list'],
  ],
  use: {
    baseURL: cfg.baseURL,
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
