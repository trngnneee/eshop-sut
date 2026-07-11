const fs = require('fs');
const path = require('path');

const matrixPath = path.join(__dirname, '../tests/test-summary/traceability-matrix.md');
const resultsPath = path.join(__dirname, '../tests/test-runs/mforgot-manual-results.json');

let content = fs.readFileSync(matrixPath, 'utf8');
content = content.replace(/\\n/g, '\n');
const cut = content.indexOf('| FR-22');
const head = (cut >= 0 ? content.slice(0, cut) : content).trimEnd();

const results = JSON.parse(fs.readFileSync(resultsPath, 'utf8')).results;
const order = [];
for (let i = 1; i <= 44; i++) order.push(`TC-MFORGOT-${String(i).padStart(3, '0')}`);
for (let i = 1; i <= 7; i++) order.push(`TC-MFORGOT-SUP-${String(i).padStart(3, '0')}`);

const rows = order.map((id) => {
  const r = results[id];
  const bugs = r.bugs === 'None' ? 'None' : r.bugs;
  const status = r.result === 'Pass' ? 'Done' : 'Open';
  return `| FR-22 (Forgot Password Mobile) | [${id}](../test-cases/forgot-mobile/${id}.md) | ${r.result} | ${bugs} | ${status} |`;
});

fs.writeFileSync(matrixPath, `${head}\n${rows.join('\n')}\n`);
console.log(`Fixed matrix with ${rows.length} FR-22 rows`);
