const fs = require('fs');
const path = require('path');

const matrixPath = path.join(__dirname, '../tests/test-summary/traceability-matrix.md');
const resultsPath = path.join(__dirname, '../tests/test-runs/mforgot-playwright-test-run.md');

const playwrightResults = {
  'TC-MFORGOT-SUP-001': { result: 'Fail', bugs: '#6' },
  'TC-MFORGOT-SUP-002': { result: 'Fail', bugs: '#20' },
  'TC-MFORGOT-SUP-003': { result: 'Fail', bugs: '#10' },
  'TC-MFORGOT-SUP-004': { result: 'Pass', bugs: 'None' },
  'TC-MFORGOT-SUP-005': { result: 'Fail', bugs: '#4' },
  'TC-MFORGOT-SUP-006': { result: 'Fail', bugs: '#21' },
  'TC-MFORGOT-SUP-007': { result: 'Fail', bugs: '#7' },
  'TC-MFORGOT-001': { result: 'Fail', bugs: '#4, #6, #20' },
  'TC-MFORGOT-004': { result: 'Pass', bugs: 'None' },
  'TC-MFORGOT-010': { result: 'Pass', bugs: 'None' },
  'TC-MFORGOT-019': { result: 'Fail', bugs: '#5' },
  'TC-MFORGOT-020': { result: 'Fail', bugs: '#9' },
  'TC-MFORGOT-028': { result: 'Fail', bugs: '#6, #7' },
  'TC-MFORGOT-031': { result: 'Fail', bugs: '#7' },
};

let matrix = fs.readFileSync(matrixPath, 'utf8');
for (const [tcId, { result, bugs }] of Object.entries(playwrightResults)) {
  const status = result === 'Pass' ? 'Done' : 'Open';
  const rowRe = new RegExp(
    `\\| FR-22 \\(Forgot Password Mobile\\) \\| \\[${tcId}\\][^\\n]+`,
    'g'
  );
  matrix = matrix.replace(
    rowRe,
    `| FR-22 (Forgot Password Mobile) | [${tcId}](../test-cases/forgot-mobile/${tcId}.md) | ${result} | ${bugs} | ${status} |`
  );
}
fs.writeFileSync(matrixPath, matrix);
console.log('Updated traceability for', Object.keys(playwrightResults).length, 'Playwright TCs');
