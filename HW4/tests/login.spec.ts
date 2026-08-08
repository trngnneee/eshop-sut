import { test, expect, type Page } from '@playwright/test';
import * as fs from 'fs';
import * as path from 'path';
import { ensureFreshAccount, apiLogin, API_BASE_URL } from './utils/api';
import { getUserState, forceLockedUntil, deleteUserByEmail } from './utils/db';

const STUDENT_ID = '23127207';
const HOME_URL = 'http://localhost:5173/';

// ---------------------------------------------------------------------------------
// Data models + runtime validation (Section: "Make the scripts data-driven")
// ---------------------------------------------------------------------------------
interface SimpleLoginCase {
  caseId: string;
  category: string;
  description: string;
  bugRef?: string;
  accountMode: 'shared-existing' | 'fresh' | 'nonexistent';
  registerEmail?: string;
  registerPassword?: string;
  email: string;
  password: string;
  expectedOutcome: 'success' | 'error';
  expectedErrorContains?: string;
}

interface UiCase {
  caseId: string;
  category: string;
  description: string;
  bugRef?: string;
  check: string;
  email?: string;
  password?: string;
}

interface LockoutCase {
  caseId: string;
  category: string;
  description: string;
  bugRef?: string;
  action: string;
  wrongAttempts?: number;
  expectedAttempts?: number;
  expectedLocked?: boolean;
  expectedFinalOutcome?: 'success' | 'blocked';
  expectedMaxLockDurationMs?: number;
  expectedAttemptsAfterSuccess?: number;
  firstWrongAttempts?: number;
  expectedAttemptsAfterSecondWrong?: number;
  concurrentAttempts?: number;
  extraWrongAttemptsWhileLocked?: number;
  newPassword?: string;
}

function loadJsonArray<T extends { caseId: string }>(fileName: string, minCount: number): T[] {
  const filePath = path.join(__dirname, '../test-data', fileName);
  if (!fs.existsSync(filePath)) {
    throw new Error(`Test data file not found: ${filePath}`);
  }
  const parsed = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
  if (!Array.isArray(parsed)) {
    throw new Error(`${fileName} must contain a JSON array of test cases`);
  }
  if (parsed.length < minCount) {
    throw new Error(`${fileName} must contain at least ${minCount} cases, found ${parsed.length}`);
  }
  const seen = new Set<string>();
  for (const row of parsed) {
    if (!row || typeof row.caseId !== 'string' || row.caseId.length === 0) {
      throw new Error(`${fileName}: every case must have a non-empty caseId`);
    }
    if (seen.has(row.caseId)) {
      throw new Error(`${fileName}: duplicate caseId "${row.caseId}"`);
    }
    seen.add(row.caseId);
  }
  return parsed as T[];
}

const simpleCases = loadJsonArray<SimpleLoginCase>('login-cases.json', 12);
const uiCases = loadJsonArray<UiCase>('login-ui-cases.json', 1);
const lockoutCases = loadJsonArray<LockoutCase>('login-lockout-cases.json', 1);

// ---------------------------------------------------------------------------------
// Page helpers (the SUT's Login.jsx has no <label for>, so inputs are located via
// their surrounding field container text — see docs/system-analysis.md)
// ---------------------------------------------------------------------------------
async function fillLoginForm(page: Page, email: string, password: string) {
  await page.locator('div').filter({ hasText: /^Username$/ }).locator('input').fill(email);
  await page.locator('div').filter({ hasText: /^Mật khẩu$/ }).locator('input').fill(password);
}

async function submitLogin(page: Page) {
  await page.getByRole('button', { name: /Sign In|Đăng nhập/ }).click();
}

// ---------------------------------------------------------------------------------
// Shape A — single login attempt, fresh/shared/nonexistent account (31 cases)
// ---------------------------------------------------------------------------------
test.describe('FR-02 Login form submission (data-driven)', () => {
  for (const c of simpleCases) {
    test(`${c.caseId}: ${c.description}`, async ({ page, request }, testInfo) => {
      testInfo.annotations.push({ type: 'Run by', description: STUDENT_ID });
      if (c.bugRef) testInfo.annotations.push({ type: 'Bug ref', description: c.bugRef });

      if (c.accountMode === 'fresh') {
        await deleteUserByEmail(c.registerEmail!).catch(() => undefined);
        await ensureFreshAccount(request, c.registerEmail!, c.registerPassword!);
      }

      let dialogAppeared = false;
      page.on('dialog', async (dialog) => {
        dialogAppeared = true;
        await dialog.dismiss();
      });

      await page.goto('/login');
      await fillLoginForm(page, c.email, c.password);
      await submitLogin(page);

      if (c.expectedOutcome === 'success') {
        // Assertion pattern 1: URL navigation
        await expect(page).toHaveURL(HOME_URL);
        // Assertion pattern 2: element visibility
        await expect(page.getByRole('button', { name: 'Thoát' })).toBeVisible();
      } else {
        // Assertion pattern 1 (negated): stays on the login page
        await expect(page).toHaveURL(/\/login/);
        if (c.expectedErrorContains) {
          // Assertion pattern 3: text content
          await expect(page.getByText(c.expectedErrorContains, { exact: false })).toBeVisible();
        }
      }

      if (c.caseId === 'TC-LOGIN-016') {
        // Security oracle for the XSS case: no JS dialog must ever fire.
        expect(dialogAppeared).toBe(false);
      }
    });
  }
});

// ---------------------------------------------------------------------------------
// Shape B — UI/UX/accessibility standards (7 cases)
// ---------------------------------------------------------------------------------
test.describe('FR-02 Login UI standards', () => {
  for (const c of uiCases) {
    test(`${c.caseId}: ${c.description}`, async ({ page }, testInfo) => {
      testInfo.annotations.push({ type: 'Run by', description: STUDENT_ID });
      if (c.bugRef) testInfo.annotations.push({ type: 'Bug ref', description: c.bugRef });

      await page.goto('/login');

      switch (c.check) {
        case 'form-standards': {
          await expect(page.getByRole('heading')).toHaveText(/Đăng Nhập|Đăng nhập/i);
          await expect(page.getByText('Email', { exact: false })).toBeVisible();
          const pwInput = page.locator('div').filter({ hasText: /^Mật khẩu$/ }).locator('input');
          await expect(pwInput).toHaveAttribute('type', 'password');
          await expect(page.getByRole('button', { name: 'Đăng nhập' })).toBeVisible();
          break;
        }
        case 'loading-state': {
          await fillLoginForm(page, c.email!, c.password!);
          const button = page.getByRole('button', { name: /Sign In|Đăng nhập/ });
          await button.click();
          await expect(button).toBeDisabled();
          break;
        }
        case 'password-toggle': {
          const toggle = page.getByRole('button', { name: /hiện mật khẩu|show password|toggle password/i });
          await expect(toggle).toBeVisible();
          break;
        }
        case 'route-guard': {
          await fillLoginForm(page, c.email!, c.password!);
          await submitLogin(page);
          await expect(page).toHaveURL(HOME_URL);
          await page.goto('/login');
          await expect(page).not.toHaveURL(/\/login/);
          break;
        }
        case 'no-credentials-in-url': {
          await fillLoginForm(page, c.email!, c.password!);
          await submitLogin(page);
          await expect(page).not.toHaveURL(new RegExp(c.password!.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')));
          break;
        }
        case 'tab-order': {
          const emailInput = page.locator('div').filter({ hasText: /^Username$/ }).locator('input');
          await page.keyboard.press('Tab');
          await expect(emailInput).toBeFocused();
          break;
        }
        case 'autofill-attributes': {
          const emailInput = page.locator('div').filter({ hasText: /^Username$/ }).locator('input');
          await expect(emailInput).toHaveAttribute('autocomplete', 'username');
          break;
        }
        case 'offline-submit': {
          await fillLoginForm(page, c.email!, c.password!);
          await page.context().setOffline(true);
          await submitLogin(page);
          await page.waitForTimeout(1000);
          await expect(page.locator('body')).toBeVisible();
          await page.context().setOffline(false);
          break;
        }
        default:
          throw new Error(`Unknown UI check "${c.check}" for ${c.caseId}`);
      }
    });
  }
});

// ---------------------------------------------------------------------------------
// Shape C — account lockout state machine (12 cases)
// Uses the API for the repeated wrong-password setup steps (fast + deterministic) and
// a direct DB fixture to simulate "the lock window has elapsed" instead of sleeping for
// the real ~3 minutes; the decisive outcome of each case is still checked exactly the
// way a user would see it (through the login form, or through admin-visible state).
// ---------------------------------------------------------------------------------
test.describe('FR-02 Account lockout behavior', () => {
  for (const c of lockoutCases) {
    test(`${c.caseId}: ${c.description}`, async ({ page, request }, testInfo) => {
      testInfo.annotations.push({ type: 'Run by', description: STUDENT_ID });
      if (c.bugRef) testInfo.annotations.push({ type: 'Bug ref', description: c.bugRef });

      const email = `lockout-${c.caseId.toLowerCase()}@eshop.com`;
      const correctPassword = 'ValidPassword1!';
      const wrongPassword = 'WrongPassword1!';

      await deleteUserByEmail(email).catch(() => undefined);
      await ensureFreshAccount(request, email, correctPassword);

      const doWrongAttempts = async (n: number) => {
        for (let i = 0; i < n; i++) {
          await apiLogin(request, email, wrongPassword);
        }
      };

      switch (c.action) {
        case 'wrong-then-check-attempts': {
          await doWrongAttempts(c.wrongAttempts!);
          const state = await getUserState(email);
          expect(state?.login_attempts).toBe(c.expectedAttempts);
          break;
        }
        case 'wrong-then-check-locked': {
          await doWrongAttempts(c.wrongAttempts!);
          const state = await getUserState(email);
          const isLocked = !!state?.locked_until && new Date(state.locked_until) > new Date();
          expect(isLocked).toBe(c.expectedLocked);
          break;
        }
        case 'wrong-then-correct-login': {
          await doWrongAttempts(c.wrongAttempts!);
          await page.goto('/login');
          await fillLoginForm(page, email, correctPassword);
          await submitLogin(page);
          if (c.expectedFinalOutcome === 'success') {
            await expect(page).toHaveURL(HOME_URL);
          } else {
            await expect(page).toHaveURL(/\/login/);
          }
          break;
        }
        case 'lock-duration-check': {
          const beforeMs = Date.now();
          await doWrongAttempts(c.wrongAttempts!);
          const state = await getUserState(email);
          expect(state?.locked_until).toBeTruthy();
          const durationMs = new Date(state!.locked_until as string).getTime() - beforeMs;
          expect(durationMs).toBeLessThanOrEqual(c.expectedMaxLockDurationMs!);
          break;
        }
        case 'auto-unlock-after-expiry': {
          await doWrongAttempts(c.wrongAttempts!);
          await forceLockedUntil(email, new Date(Date.now() - 1000).toISOString());
          await page.goto('/login');
          await fillLoginForm(page, email, correctPassword);
          await submitLogin(page);
          await expect(page).toHaveURL(HOME_URL);
          break;
        }
        case 'reset-on-success': {
          await doWrongAttempts(c.wrongAttempts!);
          await page.goto('/login');
          await fillLoginForm(page, email, correctPassword);
          await submitLogin(page);
          await expect(page).toHaveURL(HOME_URL);
          const state = await getUserState(email);
          expect(state?.login_attempts).toBe(c.expectedAttemptsAfterSuccess);
          break;
        }
        case 'interleaved-reset-check': {
          await doWrongAttempts(c.firstWrongAttempts!);
          await apiLogin(request, email, correctPassword);
          await doWrongAttempts(1);
          const state = await getUserState(email);
          expect(state?.login_attempts).toBe(c.expectedAttemptsAfterSecondWrong);
          break;
        }
        case 'concurrent-wrong-attempts': {
          await Promise.all(
            Array.from({ length: c.concurrentAttempts! }, () => apiLogin(request, email, wrongPassword)),
          );
          const state = await getUserState(email);
          expect(state?.login_attempts).toBeGreaterThanOrEqual(c.concurrentAttempts!);
          break;
        }
        case 'while-locked-no-growth': {
          await doWrongAttempts(c.wrongAttempts!);
          const afterLock = await getUserState(email);
          await doWrongAttempts(c.extraWrongAttemptsWhileLocked!);
          const afterExtra = await getUserState(email);
          expect(afterExtra?.login_attempts).toBe(afterLock?.login_attempts);
          break;
        }
        case 'correct-login-while-locked': {
          await doWrongAttempts(c.wrongAttempts!);
          await page.goto('/login');
          await fillLoginForm(page, email, correctPassword);
          await submitLogin(page);
          await expect(page).toHaveURL(/\/login/);
          break;
        }
        case 'reset-password-unlock': {
          await doWrongAttempts(c.wrongAttempts!);
          const forgotRes = await request.post(`${API_BASE_URL}/api/forgot-password`, { data: { email } });
          const { resetToken } = await forgotRes.json();
          await request.post(`${API_BASE_URL}/api/reset-password`, {
            data: { email, resetToken, newPassword: c.newPassword },
          });
          await page.goto('/login');
          await fillLoginForm(page, email, c.newPassword!);
          await submitLogin(page);
          await expect(page).toHaveURL(HOME_URL);
          break;
        }
        default:
          throw new Error(`Unknown lockout action "${c.action}" for ${c.caseId}`);
      }
    });
  }
});
