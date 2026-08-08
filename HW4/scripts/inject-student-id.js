// Post-processes a Playwright HTML report to make it satisfy the HW04 anti-cheat rule
// (Section 11): every report must visibly show "Run by: <StudentID>" together with an
// ISO timestamp. Run this once per feature/browser cell right after `playwright test`.
//
// Usage:
//   node scripts/inject-student-id.js <feature> <browser>
//   node scripts/inject-student-id.js            (no args: scans every reports/**/index.html)

const fs = require('fs');
const path = require('path');

const STUDENT_ID = '23127207';
const REPORTS_ROOT = path.join(__dirname, '../reports');

function findReportIndexFiles(root) {
  const results = [];
  if (!fs.existsSync(root)) return results;
  for (const entry of fs.readdirSync(root, { withFileTypes: true })) {
    const full = path.join(root, entry.name);
    if (entry.isDirectory()) {
      results.push(...findReportIndexFiles(full));
    } else if (entry.isFile() && entry.name === 'index.html' && full.includes(`${path.sep}data${path.sep}`) === false) {
      results.push(full);
    }
  }
  return results;
}

function labelFromPath(indexPath) {
  // .../reports/<feature>/<browser>/index.html
  const rel = path.relative(REPORTS_ROOT, indexPath);
  const parts = rel.split(path.sep);
  const feature = parts.length >= 2 ? parts[0] : 'unknown-feature';
  const browser = parts.length >= 2 ? parts[1] : 'unknown-browser';
  return { feature, browser };
}

function injectInto(indexPath) {
  const { feature, browser } = labelFromPath(indexPath);
  const timestamp = new Date().toISOString();
  const bannerText = `Run by: ${STUDENT_ID} | Feature: ${feature} | Browser: ${browser} | ${timestamp}`;

  let content = fs.readFileSync(indexPath, 'utf-8');

  // Always refresh the <title> so the timestamp/browser reflect the latest run.
  content = content.replace(
    /<title>[^<]*<\/title>/,
    `<title>Run by: ${STUDENT_ID} | ${feature} (${browser}) | ${timestamp}</title>`,
  );

  // Strip any banner injected by a previous run, then insert a fresh one.
  content = content.replace(
    /<div class="student-id-banner">.*?<\/div>/s,
    '',
  );

  if (!content.includes('.student-id-banner {')) {
    content = content.replace(
      '</head>',
      `<style>
          .student-id-banner {
            background-color: #0f172a;
            color: #38bdf8;
            padding: 12px;
            font-family: system-ui, -apple-system, sans-serif;
            font-size: 15px;
            font-weight: 700;
            text-align: center;
            border-bottom: 2px solid #0284c7;
          }
        </style></head>`,
    );
  }

  content = content.replace(
    '<div id="root">',
    `<div class="student-id-banner">${bannerText}</div><div id="root">`,
  );

  fs.writeFileSync(indexPath, content, 'utf-8');
  console.log(`Injected "Run by: ${STUDENT_ID}" + timestamp into ${path.relative(process.cwd(), indexPath)}`);
}

function main() {
  const [, , featureArg, browserArg] = process.argv;

  let targets;
  if (featureArg && browserArg) {
    targets = [path.join(REPORTS_ROOT, featureArg, browserArg, 'index.html')].filter(fs.existsSync);
    if (targets.length === 0) {
      console.warn(`No report found at reports/${featureArg}/${browserArg}/index.html — skipping.`);
    }
  } else {
    targets = findReportIndexFiles(REPORTS_ROOT);
  }

  if (targets.length === 0) {
    console.warn('No Playwright HTML reports found to label.');
    return;
  }

  targets.forEach(injectInto);
}

main();
