// Task 3 runner — re-executes the Task 1 GUI checklist on every configured platform.
//
//   node run-audit.js                       # 3 required desktop platforms
//   node run-audit.js --platforms all       # + the 2 emulated mobile platforms
//   node run-audit.js --only GUI-IA01-07    # single item (comma-separated list ok)
//   node run-audit.js --shots all           # screenshot every item, not just failures
//
// Output:
//   ../results/raw/<platform>.json          machine-readable results
//   ../results/<platform>/screenshots/*.png overlay-stamped evidence

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { resolvePlatforms } from './lib/platforms.js';
import { createCtx, BASE, API } from './lib/ctx.js';
import { CHECKS } from './checks/index.js';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const RESULTS = path.resolve(HERE, '..', 'results');

function arg(name, fallback = null) {
  const i = process.argv.indexOf(`--${name}`);
  return i === -1 ? fallback : process.argv[i + 1];
}

const CHECK_TIMEOUT_MS = Number(arg('timeout', 60000));

function stamp() {
  const d = new Date();
  const p = (n) => String(n).padStart(2, '0');
  return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())} ${p(d.getHours())}:${p(d.getMinutes())}:${p(d.getSeconds())} (+07)`;
}

async function preflight() {
  for (const url of [BASE, `${API}/api/products`]) {
    const res = await fetch(url).catch((e) => ({ ok: false, err: e.message }));
    if (!res.ok) throw new Error(`SUT not reachable at ${url} (${res.err || res.status}). Start backend + frontend-web first.`);
  }
}

async function runPlatform(platform, checks, { shotMode }) {
  const runStamp = stamp();
  const browser = await platform.browserType.launch(platform.launch);
  platform.version = browser.version();

  const shotDir = path.join(RESULTS, platform.key, 'screenshots');
  const results = [];

  console.log(`\n=== ${platform.label} — ${platform.engine} ${platform.version} ===`);

  for (const item of checks) {
    const context = await browser.newContext({
      ...platform.contextOptions,
      ignoreHTTPSErrors: true,
    });
    const page = await context.newPage();
    const ctx = createCtx({ page, platform, item, runStamp, screenshotDir: shotDir });

    const started = Date.now();
    let outcome;
    try {
      outcome = await Promise.race([
        item.run(ctx),
        new Promise((_, rej) => setTimeout(() => rej(new Error(`check timeout after ${CHECK_TIMEOUT_MS}ms`)), CHECK_TIMEOUT_MS)),
      ]);
      if (!outcome || !outcome.status) throw new Error('check returned no status');
    } catch (err) {
      outcome = { status: 'ERROR', evidence: `Harness error: ${err.message}` };
    }

    const status = outcome.status;
    const wantShot = shotMode === 'all' || status === 'FAIL' || status === 'ERROR' || outcome.snap;
    if (wantShot && ctx.shots.length === 0) {
      try {
        await ctx.snap(status);
      } catch (e) {
        outcome.evidence += ` | screenshot failed: ${e.message}`;
      }
    }

    results.push({
      id: item.id,
      aspect: item.aspect,
      title: item.title,
      screens: item.screens,
      platformSensitive: Boolean(item.platformSensitive),
      task1Status: item.task1Status,
      status,
      evidence: outcome.evidence,
      metrics: outcome.metrics || null,
      screenshots: ctx.shots,
      durationMs: Date.now() - started,
    });

    const icon = { PASS: '✅', FAIL: '❌', BLOCKED: '⚠️', ERROR: '💥' }[status] || '·';
    console.log(`${icon} ${item.id.padEnd(13)} ${status.padEnd(7)} ${String(outcome.evidence || '').slice(0, 120)}`);

    await context.close();
  }

  await browser.close();

  const summary = ['PASS', 'FAIL', 'BLOCKED', 'ERROR'].reduce((acc, s) => {
    acc[s] = results.filter((r) => r.status === s).length;
    return acc;
  }, {});

  const payload = {
    platform: {
      key: platform.key,
      label: platform.label,
      engine: platform.engine,
      version: platform.version,
      os: platform.os,
      device: platform.device,
      viewport: platform.contextOptions.viewport || 'device preset',
      emulated: Boolean(platform.optional),
    },
    sut: { web: BASE, api: API },
    runStamp,
    summary,
    results,
  };

  fs.mkdirSync(path.join(RESULTS, 'raw'), { recursive: true });
  fs.writeFileSync(
    path.join(RESULTS, 'raw', `${platform.key}.json`),
    `${JSON.stringify(payload, null, 2)}\n`,
  );
  console.log(`--- ${platform.label}: ${JSON.stringify(summary)}`);
  return payload;
}

(async () => {
  await preflight();

  const only = arg('only');
  const checks = only
    ? CHECKS.filter((c) => only.split(',').some((k) => c.id.includes(k.trim())))
    : CHECKS;
  if (checks.length === 0) throw new Error(`No checks matched --only ${only}`);

  const platforms = resolvePlatforms((arg('platforms') || '').split(',').filter(Boolean));
  const shotMode = arg('shots', 'fail');

  console.log(`Running ${checks.length} checklist item(s) on ${platforms.length} platform(s).`);
  for (const p of platforms) {
    await runPlatform(p, checks, { shotMode });
  }
})();
