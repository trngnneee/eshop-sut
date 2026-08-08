const fs = require('fs');
const path = require('path');

const studentId = process.env.STUDENT_ID || '23127158';
const studentName = process.env.STUDENT_NAME || 'Nguyen Thanh Gia Bao';
const reportPath = process.argv[2] || 'reports/html/index.html';

if (!fs.existsSync(reportPath)) {
  console.error(`Report not found at ${reportPath}. Run the test suite first.`);
  process.exit(1);
}

let html = fs.readFileSync(reportPath, 'utf8');
const banner = `<div id="hw04-run-stamp" style="position:fixed;top:0;left:0;right:0;` +
  `z-index:9999;background:#111;color:#fff;padding:6px 12px;font:13px monospace;">` +
  `Run by: ${studentId} — ${studentName}</div>`;

if (!html.includes('id="hw04-run-stamp"')) {
  html = html.replace('<body>', `<body>${banner}`);
  fs.writeFileSync(reportPath, html, 'utf8');
  console.log(`Stamped ${reportPath} with "Run by: ${studentId} — ${studentName}"`);
} else {
  console.log('Report already stamped.');
}