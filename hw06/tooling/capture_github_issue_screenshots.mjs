import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { chromium } from 'playwright';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const manifestPath = path.join(root, 'report', 'github-issues.json');
const outputDir = path.join(root, 'evidence', 'screenshots', 'github-issues');
const manifest = JSON.parse(await fs.readFile(manifestPath, 'utf8'));
await fs.mkdir(outputDir, { recursive: true });

const browser = await chromium.launch({ headless: true });
try {
  for (let index = 0; index < manifest.length; index += 1) {
    const issue = manifest[index];
    const context = await browser.newContext({ viewport: { width: 1600, height: 1200 }, locale: 'en-US' });
    const page = await context.newPage();
    try {
      await page.goto(issue.url, { waitUntil: 'domcontentloaded', timeout: 45000 });
      await page.getByRole('heading', { level: 1 }).first().waitFor({ state: 'visible', timeout: 30000 });
      const filename = `bug-${String(index + 1).padStart(2, '0')}-${issue.bug_id}-issue.png`;
      await page.screenshot({ path: path.join(outputDir, filename), fullPage: true });
      console.log(`${issue.bug_id} -> ${filename}`);
    } finally {
      await context.close();
    }
  }
} finally {
  await browser.close();
}
