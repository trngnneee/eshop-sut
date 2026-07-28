// Per-check execution context handed to every checklist check.
//
// One check == one item of the Task 1 GUI checklist (`checklist-final.md`).
// Every check gets a *fresh browser context* so that cart state, localStorage
// token and captured dialogs never leak between items — the same isolation a
// human tester gets by re-opening the app.

import fs from 'node:fs';
import path from 'node:path';
import { stampOverlay, removeOverlay } from './overlay.js';

export const BASE = process.env.SUT_WEB || 'http://localhost:5173';
export const API = process.env.SUT_API || 'http://localhost:3000';
export const USER = { email: 'test@eshop.com', password: 'Test1234!', name: 'Test User' };

export function createCtx({ page, platform, item, runStamp, screenshotDir }) {
  const dialogs = [];
  const consoleErrors = [];
  const shots = [];

  page.on('dialog', async (d) => {
    dialogs.push({ type: d.type(), message: d.message() });
    await d.accept().catch(() => {});
  });
  page.on('console', (m) => {
    if (m.type() === 'error') consoleErrors.push(m.text().slice(0, 300));
  });

  const ctx = {
    page,
    platform,
    item,
    BASE,
    API,
    USER,
    dialogs,
    consoleErrors,
    shots,

    /** Navigate to a SUT route and let React settle. */
    async goto(route = '/', { settle = 700 } = {}) {
      const url = route.startsWith('http') ? route : BASE + route;
      await page.goto(url, { waitUntil: 'domcontentloaded' });
      await page.waitForTimeout(settle);
      return page;
    },

    /** Log in through the real UI (Login.jsx: 2 text inputs + submit button). */
    async login(email = USER.email, password = USER.password) {
      await ctx.goto('/login');
      const inputs = page.locator('form input');
      await inputs.nth(0).fill(email);
      await inputs.nth(1).fill(password);
      await page.locator('form button[type="submit"], form button').first().click();
      await page.waitForTimeout(1200);
      return page.locator('header').innerText().catch(() => '');
    },

    /** Seed the cart through the UI from the Home page ("Thêm vào giỏ" cards). */
    async addToCartFromHome(index = 0, times = 1) {
      if (!page.url().startsWith(BASE + '/') || !/\/$/.test(new URL(page.url()).pathname)) {
        await ctx.goto('/');
      }
      const btns = page.getByRole('button', { name: 'Thêm vào giỏ', exact: true });
      await btns.first().waitFor({ timeout: 10000 });
      for (let i = 0; i < times; i += 1) {
        await btns.nth(index).click();
        await page.waitForTimeout(150);
      }
    },

    /** Computed style value of the first match. */
    async css(selector, prop) {
      return page.evaluate(
        ([sel, p]) => {
          const el = document.querySelector(sel);
          return el ? getComputedStyle(el)[p] : null;
        },
        [selector, prop],
      );
    },

    /** Computed style of a Playwright locator. */
    async cssOf(locator, prop) {
      return locator.evaluate((el, p) => getComputedStyle(el)[p], prop);
    },

    /** Overlay-stamped screenshot. Returns the repo-relative path. */
    async snap(status = 'FAIL', label = '') {
      const name = label ? `${item.id}--${label}.png` : `${item.id}.png`;
      const file = path.join(screenshotDir, name);
      fs.mkdirSync(screenshotDir, { recursive: true });
      await stampOverlay(page, {
        platformLabel: platform.label,
        engine: platform.engine,
        version: platform.version,
        os: platform.os,
        device: platform.device,
        itemId: item.id,
        status,
        timestamp: runStamp,
      });
      await page.waitForTimeout(120);
      await page.screenshot({ path: file, fullPage: false });
      await removeOverlay(page);
      shots.push(name);
      return name;
    },
  };

  return ctx;
}
