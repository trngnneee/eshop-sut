// Deterministic 3x3 (or filtered) matrix runner: executes each FEATURE x BROWSER cell as its
// own `playwright test` invocation (so each cell gets its own labeled HTML report under
// reports/<feature>/<browser>/), tolerates individual cell failures so every report still gets
// produced, then prints + persists a manifest summarizing all cells.
//
// Usage:
//   node scripts/run-matrix.js                       # all features x all browsers
//   node scripts/run-matrix.js --feature=login        # one feature x all browsers
//   node scripts/run-matrix.js --browser=chromium      # all features x one browser

const { spawnSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const ALL_FEATURES = ['login', 'cart', 'dashboard'];
const ALL_BROWSERS = ['chromium', 'firefox', 'webkit'];

function parseArgs() {
  const args = process.argv.slice(2);
  const get = (flag) => {
    const hit = args.find((a) => a.startsWith(`--${flag}=`));
    return hit ? hit.split('=')[1] : undefined;
  };
  return {
    feature: get('feature'),
    browser: get('browser'),
  };
}

function runCell(feature, browser) {
  const reportDir = `reports/${feature}/${browser}`;
  console.log(`\n=== Running FEATURE=${feature} BROWSER=${browser} (project=${browser}) ===`);

  const result = spawnSync('npx', ['playwright', 'test', `--project=${browser}`], {
    cwd: path.join(__dirname, '..'),
    env: { ...process.env, FEATURE: feature, BROWSER: browser },
    stdio: 'inherit',
    shell: true,
  });

  // Label the report regardless of pass/fail so every cell's evidence is traceable.
  spawnSync('node', ['scripts/inject-student-id.js', feature, browser], {
    cwd: path.join(__dirname, '..'),
    stdio: 'inherit',
    shell: true,
  });

  return {
    feature,
    browser,
    exitCode: result.status === null ? 1 : result.status,
    reportPath: `${reportDir}/index.html`,
  };
}

function main() {
  const { feature, browser } = parseArgs();
  const features = feature ? [feature] : ALL_FEATURES;
  const browsers = browser ? [browser] : ALL_BROWSERS;

  const manifest = [];
  for (const f of features) {
    for (const b of browsers) {
      manifest.push(runCell(f, b));
    }
  }

  console.log('\n=== Run manifest ===');
  console.table(
    manifest.map((m) => ({
      feature: m.feature,
      browser: m.browser,
      status: m.exitCode === 0 ? 'PASSED' : 'FAILED',
      report: m.reportPath,
    })),
  );

  const manifestPath = path.join(__dirname, '../reports/run-manifest.json');
  fs.mkdirSync(path.dirname(manifestPath), { recursive: true });
  fs.writeFileSync(
    manifestPath,
    JSON.stringify({ generatedAt: new Date().toISOString(), studentId: '23127207', manifest }, null, 2),
  );
  console.log(`\nManifest written to ${path.relative(process.cwd(), manifestPath)}`);

  const anyFailed = manifest.some((m) => m.exitCode !== 0);
  process.exit(anyFailed ? 1 : 0);
}

main();
