import { test, expect } from '@playwright/test';
import * as fs from 'fs';
import * as path from 'path';

interface LoginData {
  testCaseId: string;
  description: string;
  email: string;
  password: string;
  expectedUrl: string;
  expectedVisibleText: string;
  expectedUserGreeting: string;
}

function loadAndValidateLoginData(filePath: string): LoginData {
  if (!fs.existsSync(filePath)) {
    throw new Error(`Test data file not found at path: ${filePath}`);
  }
  
  const rawData = fs.readFileSync(filePath, 'utf-8');
  const data = JSON.parse(rawData);

  if (
    !data ||
    typeof data.testCaseId !== 'string' ||
    typeof data.description !== 'string' ||
    typeof data.email !== 'string' ||
    typeof data.password !== 'string' ||
    typeof data.expectedUrl !== 'string' ||
    typeof data.expectedVisibleText !== 'string' ||
    typeof data.expectedUserGreeting !== 'string'
  ) {
    throw new Error('Invalid test data structure in login-data.json');
  }

  return data as LoginData;
}

const loginDataPath = path.join(__dirname, '../test-data/login-data.json');
const loginData = loadAndValidateLoginData(loginDataPath);

test('TC-LOGIN-001: Login successfully with valid credentials', async ({ page }, testInfo) => {
  testInfo.annotations.push({
    type: 'Run by',
    description: '23127207',
  });

  // Step 1: Navigate to the login page
  await page.goto('/login');

  // Step 2: Fill email (Username field container)
  await page.locator('div').filter({ hasText: /^Username$/ }).locator('input').fill(loginData.email);

  // Step 3: Fill password (Mật khẩu field container)
  await page.locator('div').filter({ hasText: /^Mật khẩu$/ }).locator('input').fill(loginData.password);

  // Step 4: Click the login button (Sign In)
  await page.getByRole('button', { name: 'Sign In' }).click();

  // Step 5: Assertions - Verify successful login with 3 distinct patterns
  // Pattern 1: URL verification using toHaveURL()
  await expect(page).toHaveURL(loginData.expectedUrl);

  // Pattern 2: UI element visibility verification using toBeVisible()
  await expect(page.getByRole('button', { name: loginData.expectedVisibleText })).toBeVisible();

  // Pattern 3: User greeting text verification using toContainText()
  await expect(page.getByRole('link', { name: new RegExp(loginData.expectedUserGreeting, 'i') })).toContainText('Test User');
});
