// One-off helper: renders a verbatim Playwright failure block as a terminal-style PNG,
// used as GitHub Issue evidence for API-level bugs that have no browser page to
// screenshot (pure HTTP request/response assertions). Not part of the test suite itself.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const entries = JSON.parse(fs.readFileSync(process.argv[2], 'utf-8'));

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1000, height: 10 } });
  for (const { file, title, body } of entries) {
    const html = `
      <html><body style="margin:0;background:#0f172a;font-family:'Cascadia Code',Consolas,monospace;">
        <div style="padding:20px 24px;color:#e2e8f0;">
          <div style="color:#38bdf8;font-weight:700;font-size:15px;margin-bottom:10px;">${title}</div>
          <pre style="white-space:pre-wrap;font-size:13px;line-height:1.5;margin:0;color:#e2e8f0;">${body
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')}</pre>
        </div>
      </body></html>`;
    await page.setContent(html);
    const height = await page.evaluate(() => document.body.scrollHeight);
    await page.setViewportSize({ width: 1000, height: Math.min(height + 10, 4000) });
    await page.screenshot({ path: file, fullPage: true });
    console.log('wrote', file);
  }
  await browser.close();
})();
