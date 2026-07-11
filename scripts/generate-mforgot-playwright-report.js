const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const results = JSON.parse(
  fs.readFileSync(path.join(ROOT, 'test-results/results.json'), 'utf8')
);

const bugMap = {
  'TC-MFORGOT-SUP-001': '#6',
  'TC-MFORGOT-SUP-002': '#20',
  'TC-MFORGOT-SUP-003': '#10',
  'TC-MFORGOT-SUP-004': 'None',
  'TC-MFORGOT-SUP-005': '#4',
  'TC-MFORGOT-SUP-006': '#21',
  'TC-MFORGOT-SUP-007': '#7',
  'TC-MFORGOT-001': '#4, #6, #20',
  'TC-MFORGOT-004': 'None',
  'TC-MFORGOT-010': 'None',
  'TC-MFORGOT-019': '#5',
  'TC-MFORGOT-020': '#9',
  'TC-MFORGOT-028': '#6, #7',
  'TC-MFORGOT-031': '#7',
};

function setTcStatus(tcId, result, bugs) {
  const file = path.join(ROOT, 'tests/test-cases/forgot-mobile', `${tcId}.md`);
  if (!fs.existsSync(file)) return;
  let c = fs.readFileSync(file, 'utf8');
  c = c.replace(/## Status \/ Related bugs\n.*/s, `## Status / Related bugs\n${result} / ${bugs}`);
  fs.writeFileSync(file, c);
}

const rows = [];
for (const suite of results.suites || []) {
  for (const sub of suite.suites || []) {
    for (const spec of sub.specs || []) {
      const title = spec.title || '';
      const m = title.match(/^(TC-MFORGOT-[A-Z0-9-]+)/);
      if (!m) continue;
      const tcId = m[1];
      const test = (spec.tests || [])[0];
      const result = test?.results?.[0];
      const status = result?.status === 'passed' ? 'Pass' : result?.status === 'skipped' ? 'Skip' : 'Fail';
      const bugs = bugMap[tcId] || (status === 'Pass' ? 'None' : 'TBD');
      setTcStatus(tcId, status, bugs);
      rows.push({ tcId, status, bugs, error: result?.error?.message?.split('\n')[0] });
    }
  }
}

const pass = rows.filter((r) => r.status === 'Pass').length;
const fail = rows.filter((r) => r.status === 'Fail').length;

const report = `# Test Run — FR-26 Mobile Forgot (Playwright Automation)

**Date:** ${new Date().toISOString().slice(0, 10)}  
**Command:** \`npm run test:mforgot\`  
**Project:** mobile-chromium · Expo Web \`http://localhost:8081\`

## Summary

| Metric | Count |
| :--- | ---: |
| Automated TC | ${rows.length} |
| Pass | ${pass} |
| Fail | ${fail} |

## Results

| Test Case | Result | Bug | Note |
| :--- | :--- | :--- | :--- |
${rows.map((r) => `| ${r.tcId} | ${r.status} | ${r.bugs} | ${(r.error || '').replace(/\|/g, '/').slice(0, 80)} |`).join('\n')}

## New bug reports

- [#20](issue-020-mobile-no-otp-demo.md) — Demo OTP not on Mobile screen
- [#21](issue-021-mobile-alert-not-inline.md) — Alert instead of inline error (FR-22)
`;

fs.writeFileSync(path.join(ROOT, 'tests/test-runs/mforgot-playwright-test-run.md'), report);
console.log(report);
console.log(`\nWrote tests/test-runs/mforgot-playwright-test-run.md (${pass} pass, ${fail} fail)`);
