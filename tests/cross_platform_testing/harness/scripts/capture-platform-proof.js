// Platform-proof screenshots.
//
// run-audit.js produces *viewport* screenshots (Playwright cannot capture browser
// chrome). HW03 §6 also wants the browser / OS / device name next to the SUT's
// localhost URL, so this script captures the **whole OS window** of each real
// browser — macOS menu bar (browser app name) + the browser's own address bar
// showing http://localhost:5173/... — with the student-e-mail overlay stamped
// inside the page.
//
//   node scripts/capture-platform-proof.js                 # 3 desktop platforms
//   node scripts/capture-platform-proof.js --platforms P1-chromium-macos
//
// Output: ../results/<platform>/platform-proof/<screen>.png

import fs from 'node:fs';
import path from 'node:path';
import { execSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { resolvePlatforms } from '../lib/platforms.js';
import { stampOverlay } from '../lib/overlay.js';
import { BASE, USER } from '../lib/ctx.js';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const RESULTS = path.resolve(HERE, '..', '..', 'results');

const SCREENS = [
  { slug: '01-home', route: '/', note: 'Trang chủ — danh sách sản phẩm' },
  { slug: '02-login', route: '/login', note: 'Đăng nhập' },
  { slug: '03-product-detail', route: '/product/1', note: 'Chi tiết sản phẩm' },
  { slug: '04-cart', route: '/cart', note: 'Giỏ hàng (đã thêm 1 SP)', seedCart: true },
  { slug: '05-checkout', route: '/checkout', note: 'Thanh toán (đã đăng nhập, giỏ có SP)', login: true, seedCart: true },
  { slug: '06-not-found', route: '/abc', note: 'URL không tồn tại' },
];

function arg(name, fallback = null) {
  const i = process.argv.indexOf(`--${name}`);
  return i === -1 ? fallback : process.argv[i + 1];
}

function stamp() {
  const d = new Date();
  const p = (n) => String(n).padStart(2, '0');
  return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())} ${p(d.getHours())}:${p(d.getMinutes())}:${p(d.getSeconds())} (+07)`;
}

/**
 * The .app bundle that owns the browser window.
 * Chromium/Firefox: the executable lives inside the bundle. WebKit: the executable
 * is `pw_run.sh`, and the bundle (`Playwright.app`) is its sibling.
 */
function bundleOf(executablePath) {
  const i = executablePath.indexOf('.app');
  if (i !== -1) return executablePath.slice(0, i + 4);
  const dir = path.dirname(executablePath);
  const app = fs.readdirSync(dir).find((f) => f.endsWith('.app'));
  return app ? path.join(dir, app) : null;
}

/** Name macOS shows in the menu bar for that bundle. */
const appNameOf = (bundle) => (bundle ? path.basename(bundle, '.app') : null);

/** Name of the app currently owning the menu bar — no Accessibility permission needed. */
function frontAppName() {
  try {
    const asn = execSync('lsappinfo front').toString().trim();
    const info = execSync(`lsappinfo info -only name ${asn}`).toString();
    return (info.match(/"LSDisplayName"="([^"]*)"/) || [])[1] || info.trim();
  } catch {
    return null;
  }
}

/**
 * Raise the browser window and REFUSE to capture until macOS confirms that this
 * browser really owns the menu bar. A screen-region capture is a picture of
 * whatever is in front: without this check a foreign window (or another app's
 * content) can silently end up in the evidence set.
 */
async function focusOrThrow(page, bundle, label) {
  const want = appNameOf(bundle);
  for (let attempt = 1; attempt <= 6; attempt += 1) {
    await page.bringToFront().catch(() => {});
    if (bundle) {
      try {
        execSync(`osascript -e 'tell application "${bundle}" to activate'`, { stdio: 'ignore' });
      } catch { /* fall through to the verification below */ }
    }
    await page.waitForTimeout(700);
    const front = frontAppName();
    if (want && front && front.toLowerCase().includes(want.toLowerCase())) return front;
    if (attempt === 6)
      throw new Error(
        `refusing to capture ${label}: front app is "${front}", expected "${want}" — the browser window is not in front`,
      );
  }
  return null;
}

(async () => {
  const platforms = resolvePlatforms((arg('platforms') || '').split(',').filter(Boolean));
  const runStamp = stamp();

  for (const platform of platforms) {
    const browser = await platform.browserType.launch(platform.launch);
    platform.version = browser.version();
    const bundle = bundleOf(platform.browserType.executablePath());
    const outDir = path.join(RESULTS, platform.key, 'platform-proof');
    fs.mkdirSync(outDir, { recursive: true });

    const context = await browser.newContext(platform.contextOptions);
    const page = await context.newPage();
    console.log(`\n=== ${platform.label} — ${platform.engine} ${platform.version} (${bundle}) ===`);

    for (const screen of SCREENS) {
      if (screen.login) {
        await page.goto(`${BASE}/login`, { waitUntil: 'domcontentloaded' });
        await page.waitForTimeout(600);
        const inputs = page.locator('form input');
        await inputs.nth(0).fill(USER.email);
        await inputs.nth(1).fill(USER.password);
        await page.locator('form button').first().click();
        await page.waitForTimeout(1200);
      }
      if (screen.seedCart) {
        await page.goto(BASE, { waitUntil: 'domcontentloaded' });
        await page.waitForTimeout(800);
        await page.getByRole('button', { name: 'Thêm vào giỏ', exact: true }).first().click();
        await page.waitForTimeout(300);
        // SPA navigation only — a full reload would wipe the React-state cart.
        await page.getByRole('link', { name: 'Giỏ hàng' }).click();
        await page.waitForTimeout(600);
        if (screen.route === '/checkout') {
          await page.getByRole('button', { name: /Tiến hành thanh toán/ }).click();
          await page.waitForTimeout(900);
        }
      } else {
        await page.goto(BASE + screen.route, { waitUntil: 'domcontentloaded' });
        await page.waitForTimeout(900);
      }

      await stampOverlay(page, {
        platformLabel: platform.label,
        engine: platform.engine,
        version: platform.version,
        os: platform.os,
        device: platform.device,
        itemId: `PLATFORM-PROOF ${screen.slug} — ${screen.note}`,
        status: 'EVIDENCE',
        timestamp: runStamp,
      });

      const front = await focusOrThrow(page, bundle, `${platform.key}/${screen.slug}`);
      await page.waitForTimeout(400);

      const geo = await page.evaluate(() => ({
        sx: window.screenX,
        sy: window.screenY,
        ow: window.outerWidth,
        oh: window.outerHeight,
      }));
      // Exact window rectangle, extended up to y=0 so the macOS menu bar (which
      // carries the browser's app name) is included — and not one pixel wider, so
      // nothing behind the window can leak into the evidence.
      const x = Math.max(0, geo.sx);
      const w = geo.ow;
      const h = geo.sy + geo.oh;
      const file = path.join(outDir, `${screen.slug}.png`);
      execSync(`screencapture -x -R${x},0,${w},${h} "${file}"`);
      console.log(
        `  ${screen.slug} → ${path.relative(RESULTS, file)} (window ${geo.ow}×${geo.oh} @ ${geo.sx},${geo.sy}, front app "${front}")`,
      );
    }

    await context.close();
    await browser.close();
  }
})();
