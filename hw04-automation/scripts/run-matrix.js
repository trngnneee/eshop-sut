/**
 * Runs each selected feature × browser cell separately so every cell gets its
 * own HTML report with a visible "Run by: {StudentID}" title.
 *
 * Evidence isolation rules:
 * - Reports live under reports/html/<feature-slug>/<browser>/ — never shared.
 * - Per-feature manifests: reports/run-manifest-<slug>.json
 * - Combined manifest merges cells and does not drop other features.
 * - Feature directories with EVIDENCE-LOCK.json are skipped unless FORCE_OVERWRITE=1.
 * - Prefer: npm run test:matrix:fr08  (Feature B only; leaves FR-03 untouched)
 */
const { spawnSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const STUDENT_ID = process.env.STUDENT_ID || '23127271';
const ROOT = path.resolve(__dirname, '..');
const FORCE_OVERWRITE = process.env.FORCE_OVERWRITE === '1';

/** @type {{ slug: string, name: string, grep: string, letter: string }[]} */
const ALL_FEATURES = [
  {
    slug: 'fr03-forgot-password',
    name: 'FR-03 Forgot Password',
    grep: 'FR-03',
    letter: 'A',
  },
  {
    slug: 'fr08-checkout',
    name: 'FR-08 Checkout',
    grep: 'FR-08',
    letter: 'B',
  },
  {
    slug: 'fr15-admin-product',
    name: 'FR-15 Admin Product CRUD',
    grep: 'FR-15',
    letter: 'C',
  },
];

const BROWSERS = ['chromium', 'firefox', 'webkit'];

/**
 * FEATURE_FILTER examples (env or CLI arg):
 *   fr08 | fr08-checkout | B | feature-b
 *   fr03,fr08
 *   all
 * CLI: node scripts/run-matrix.js fr08
 */
function resolveFeatures() {
  const raw = (
    process.env.FEATURE_FILTER ||
    process.argv.slice(2).join(',') ||
    ''
  )
    .trim()
    .toLowerCase();
  const implemented = ALL_FEATURES.filter((f) => {
    const specHint =
      f.slug === 'fr03-forgot-password'
        ? 'fr03-forgot-password.spec.js'
        : f.slug === 'fr08-checkout'
          ? 'fr08-checkout.spec.js'
          : 'fr15-admin-product.spec.js';
    return fs.existsSync(path.join(ROOT, 'tests', specHint));
  });

  if (!raw || raw === 'all') {
    return implemented;
  }

  const tokens = raw.split(/[,+\s]+/).filter(Boolean);
  const selected = ALL_FEATURES.filter((f) =>
    tokens.some(
      (t) =>
        t === f.slug ||
        t === f.slug.split('-')[0] ||
        t === f.letter.toLowerCase() ||
        t === `feature-${f.letter.toLowerCase()}` ||
        t === f.grep.toLowerCase(),
    ),
  );

  if (selected.length === 0) {
    throw new Error(
      `FEATURE_FILTER="${raw}" matched no features. Use fr03, fr08, fr15, A, B, C, or all.`,
    );
  }
  return selected;
}

function isFrozen(absReportDir) {
  return fs.existsSync(path.join(absReportDir, 'EVIDENCE-LOCK.json'));
}

function stampReportLabel(indexHtmlPath, reportTitle) {
  if (!fs.existsSync(indexHtmlPath)) return false;
  let html = fs.readFileSync(indexHtmlPath, 'utf8');
  const label = `Run by: ${STUDENT_ID}`;

  html = html.replace(
    /<title>[^<]*<\/title>/i,
    `<title>${reportTitle}</title>`,
  );

  const banner = [
    `<header id="hw04-run-by" data-student-id="${STUDENT_ID}" style="font-family:system-ui,sans-serif;padding:12px 16px;background:#0b3d2e;color:#f5fff9;border-bottom:3px solid #2ecc71;">`,
    `<strong>${label}</strong>`,
    `<span style="opacity:.9"> &nbsp;|&nbsp; ${reportTitle.replace(`${label} | `, '')}</span>`,
    `</header>`,
  ].join('');

  if (html.includes('id="hw04-run-by"')) {
    html = html.replace(/<header id="hw04-run-by"[\s\S]*?<\/header>/, banner);
  } else if (/<body[^>]*>/i.test(html)) {
    html = html.replace(/<body([^>]*)>/i, `<body$1>${banner}`);
  } else {
    html = `${banner}\n${html}`;
  }

  if (!html.includes('name="run-by"')) {
    html = html.replace(
      /<head>/i,
      `<head>\n    <meta name="run-by" content="${label}">\n    <meta name="student-id" content="${STUDENT_ID}">`,
    );
  }

  fs.writeFileSync(indexHtmlPath, html, 'utf8');
  return fs.readFileSync(indexHtmlPath, 'utf8').includes(label);
}

function runCell(feature, browser) {
  const timestamp = new Date().toISOString();
  const reportDir = path.join('reports', 'html', feature.slug, browser);
  const absReportDir = path.join(ROOT, reportDir);
  const reportTitle = `Run by: ${STUDENT_ID} | ${feature.name} | ${browser} | ${timestamp}`;

  if (isFrozen(absReportDir) && !FORCE_OVERWRITE) {
    console.log(
      `\n=== SKIP frozen evidence: ${feature.name} @ ${browser} ===`,
    );
    console.log(`Lock: ${path.join(reportDir, 'EVIDENCE-LOCK.json')}`);
    console.log('Set FORCE_OVERWRITE=1 only if you intentionally re-run Feature A.');
    return {
      feature: feature.slug,
      featureName: feature.name,
      browser,
      exitCode: 0,
      reportPath: reportDir,
      indexHtml: fs.existsSync(path.join(absReportDir, 'index.html'))
        ? path.join(absReportDir, 'index.html')
        : null,
      labelFound: true,
      timestamp,
      reportTitle: `FROZEN | ${feature.name} | ${browser}`,
      skippedFrozen: true,
    };
  }

  fs.mkdirSync(absReportDir, { recursive: true });

  const args = [
    'playwright',
    'test',
    '--project',
    browser,
    '--grep',
    feature.grep,
  ];

  const env = {
    ...process.env,
    STUDENT_ID,
    FEATURE_NAME: feature.name,
    FEATURE_SLUG: feature.slug,
    BROWSER_PROJECT: browser,
    RUN_TIMESTAMP: timestamp,
    HTML_REPORT_DIR: reportDir,
    PLAYWRIGHT_HTML_OUTPUT_DIR: reportDir,
    PLAYWRIGHT_HTML_TITLE: reportTitle,
    PLAYWRIGHT_HTML_OPEN: 'never',
  };

  console.log(`\n=== ${feature.name} @ ${browser} ===`);
  console.log(`Report: ${reportDir}`);
  console.log(`Title: ${reportTitle}`);

  const result = spawnSync('npx', args, {
    cwd: ROOT,
    env,
    encoding: 'utf8',
    shell: true,
    stdio: 'inherit',
  });

  const indexHtml = path.join(absReportDir, 'index.html');
  const labelFound = stampReportLabel(indexHtml, reportTitle);

  return {
    feature: feature.slug,
    featureName: feature.name,
    browser,
    exitCode: result.status ?? 1,
    reportPath: reportDir,
    indexHtml: fs.existsSync(indexHtml) ? indexHtml : null,
    labelFound,
    timestamp,
    reportTitle,
    skippedFrozen: false,
  };
}

function readJsonSafe(filePath) {
  if (!fs.existsSync(filePath)) return null;
  try {
    return JSON.parse(fs.readFileSync(filePath, 'utf8'));
  } catch {
    return null;
  }
}

function writeFeatureManifest(featureSlug, cells) {
  const featureManifest = {
    studentId: STUDENT_ID,
    runBy: `Run by: ${STUDENT_ID}`,
    feature: featureSlug,
    generatedAt: new Date().toISOString(),
    cells,
    summary: {
      total: cells.length,
      passed: cells.filter((r) => r.exitCode === 0 && !r.skippedFrozen).length,
      failed: cells.filter((r) => r.exitCode !== 0).length,
      skippedFrozen: cells.filter((r) => r.skippedFrozen).length,
      labelsOk: cells.filter((r) => r.labelFound).length,
    },
  };
  const featurePath = path.join(
    ROOT,
    'reports',
    `run-manifest-${featureSlug}.json`,
  );
  fs.mkdirSync(path.dirname(featurePath), { recursive: true });
  fs.writeFileSync(featurePath, JSON.stringify(featureManifest, null, 2), 'utf8');
  return featurePath;
}

/**
 * Merge per-feature manifests into combined run-manifest.json without dropping
 * cells from features that were not part of this invocation.
 */
function mergeCombinedManifest(updatedBySlug) {
  const combinedPath = path.join(ROOT, 'reports', 'run-manifest.json');
  const existing = readJsonSafe(combinedPath);
  /** @type {Map<string, any>} */
  const byKey = new Map();

  if (existing?.cells) {
    for (const cell of existing.cells) {
      byKey.set(`${cell.feature}::${cell.browser}`, cell);
    }
  }

  for (const [slug, cells] of Object.entries(updatedBySlug)) {
    for (const cell of cells) {
      // Do not replace a prior real run with a skippedFrozen placeholder
      const key = `${cell.feature}::${cell.browser}`;
      const prev = byKey.get(key);
      if (cell.skippedFrozen && prev && !prev.skippedFrozen) {
        continue;
      }
      byKey.set(key, cell);
    }
    void slug;
  }

  const cells = [...byKey.values()].sort((a, b) =>
    `${a.feature}-${a.browser}`.localeCompare(`${b.feature}-${b.browser}`),
  );

  const manifest = {
    studentId: STUDENT_ID,
    runBy: `Run by: ${STUDENT_ID}`,
    generatedAt: new Date().toISOString(),
    cells,
    summary: {
      total: cells.length,
      passed: cells.filter((r) => r.exitCode === 0 && !r.skippedFrozen).length,
      failed: cells.filter((r) => r.exitCode !== 0).length,
      skippedFrozen: cells.filter((r) => r.skippedFrozen).length,
      labelsOk: cells.filter((r) => r.labelFound).length,
    },
  };

  fs.writeFileSync(combinedPath, JSON.stringify(manifest, null, 2), 'utf8');
  return combinedPath;
}

function main() {
  const features = resolveFeatures();
  /** @type {Record<string, ReturnType<typeof runCell>[]>} */
  const updatedBySlug = {};
  /** @type {ReturnType<typeof runCell>[]} */
  const results = [];

  console.log(
    `Matrix features: ${features.map((f) => f.slug).join(', ') || '(none)'}`,
  );
  console.log(`FORCE_OVERWRITE=${FORCE_OVERWRITE ? '1' : '0'}`);

  for (const feature of features) {
    updatedBySlug[feature.slug] = [];
    for (const browser of BROWSERS) {
      const cell = runCell(feature, browser);
      updatedBySlug[feature.slug].push(cell);
      results.push(cell);
    }
    const featureManifestPath = writeFeatureManifest(
      feature.slug,
      updatedBySlug[feature.slug],
    );
    console.log(`Feature manifest: ${featureManifestPath}`);
  }

  const combinedPath = mergeCombinedManifest(updatedBySlug);

  console.log('\n========== MATRIX SUMMARY ==========');
  for (const r of results) {
    const status = r.skippedFrozen
      ? 'FROZEN'
      : r.exitCode === 0
        ? 'PASS'
        : 'FAIL';
    const label = r.labelFound ? 'label OK' : 'label MISSING';
    console.log(
      `${status} | ${r.feature} | ${r.browser} | ${label} | ${r.reportPath}`,
    );
  }
  console.log(`Combined manifest: ${combinedPath}`);
  console.log(
    `This run cells: ${results.length} · Combined cells kept across features in ${combinedPath}`,
  );

  const failed =
    results.some((r) => r.exitCode !== 0 && !r.skippedFrozen) ||
    results.some((r) => !r.labelFound && !r.skippedFrozen);
  process.exit(failed ? 1 : 0);
}

main();
