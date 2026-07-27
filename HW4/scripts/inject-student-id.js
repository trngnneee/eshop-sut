const fs = require('fs');
const path = require('path');

const studentId = '23127207';
const reports = ['chromium', 'firefox', 'webkit'];

reports.forEach((browser) => {
  const indexPath = path.join(__dirname, `../reports/${browser}/index.html`);
  if (fs.existsSync(indexPath)) {
    let content = fs.readFileSync(indexPath, 'utf-8');
    
    // Update document title
    content = content.replace(
      '<title>Playwright Test Report</title>',
      `<title>Run by: ${studentId} | Playwright Test Report (${browser})</title>`
    );

    // Inject visible banner if not present
    if (!content.includes(`Run by: ${studentId}`)) {
      content = content.replace(
        '</head>',
        `<style>
          .student-id-banner {
            background-color: #0f172a;
            color: #38bdf8;
            padding: 12px;
            font-family: system-ui, -apple-system, sans-serif;
            font-size: 16px;
            font-weight: 700;
            text-align: center;
            border-bottom: 2px solid #0284c7;
          }
        </style></head>`
      ).replace(
        '<div id="root">',
        `<div class="student-id-banner">Run by: ${studentId} | Browser: ${browser}</div><div id="root">`
      );
    }
    
    fs.writeFileSync(indexPath, content, 'utf-8');
    console.log(`Successfully verified and injected Student ID into ${browser} index.html`);
  }
});
