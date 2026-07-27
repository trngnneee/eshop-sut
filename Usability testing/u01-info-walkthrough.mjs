import playwright from '../GUI testing/automation/node_modules/@playwright/test/index.js';

const { chromium } = playwright;
const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
page.setDefaultTimeout(30_000);
page.on('response', (response) => {
  if (response.url().includes('back-end-lumierecinema')) {
    console.log(`[api:${response.status()}] ${response.request().method()} ${response.url()}`);
  }
});
page.on('console', (message) => {
  if (['error', 'warning'].includes(message.type())) console.log(`[console:${message.type()}] ${message.text()}`);
});
page.on('pageerror', (error) => console.log(`[pageerror] ${error.message}`));

await page.goto(
  'https://lumierecinema-testing-demo-ui.vercel.app/buy-ticket?movieId=6a50f3a363e917e045f2308d&branchId=6a50839d63cc73a21b16fcb6',
  { waitUntil: 'domcontentloaded', timeout: 60_000 },
);
const showtime = page.getByRole('button', { name: /20:00/ }).first();
await showtime.waitFor({ timeout: 60_000 });
await showtime.click({ noWaitAfter: true });
await page.waitForTimeout(8_000);
await page.getByText('SEATINGS', { exact: true }).first().click({ force: true, noWaitAfter: true });
await page.waitForTimeout(8_000);

const adultIncrease = page.getByRole('button', { name: 'Increase', exact: true }).first();
await adultIncrease.click();
await adultIncrease.click();
await page.locator('[title="Seat A1"]').click();
await page.locator('[title="Seat A2"]').click();
await page.getByText('SEATINGS', { exact: true }).first().click({ force: true, noWaitAfter: true });
await page.waitForTimeout(8_000);

await page.getByText('INFO', { exact: true }).first().click({ force: true, noWaitAfter: true });
await page.waitForTimeout(8_000);
await page.screenshot({ path: 'evidence/expert/11-ticket-info.png', fullPage: true });

console.log(`URL=${page.url()}`);
console.log((await page.locator('body').innerText()).slice(0, 20_000));
console.log('CONTROLS');
console.log(
  JSON.stringify(
    await page.locator('button, a, input, select, option, [role="button"], [role="option"]').evaluateAll((nodes) =>
      nodes.slice(0, 500).map((node, index) => ({
        index,
        tag: node.tagName,
        text: (node.innerText || node.getAttribute('aria-label') || node.getAttribute('placeholder') || '').trim(),
        ariaLabel: node.getAttribute('aria-label'),
        title: node.getAttribute('title'),
        type: node.getAttribute('type'),
        disabled: 'disabled' in node ? node.disabled : undefined,
      })),
    ),
    null,
    2,
  ),
);

await browser.close();
