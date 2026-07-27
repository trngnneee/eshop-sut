import playwright from '../GUI testing/automation/node_modules/@playwright/test/index.js';

const { chromium } = playwright;
const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({
  viewport: { width: 390, height: 844 },
  screen: { width: 390, height: 844 },
  isMobile: true,
  hasTouch: true,
  deviceScaleFactor: 3,
  userAgent:
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1',
});
const page = await context.newPage();
page.setDefaultTimeout(30_000);

await page.goto('https://lumierecinema-testing-demo-ui.vercel.app/movies', {
  waitUntil: 'domcontentloaded',
  timeout: 60_000,
});
await page.waitForTimeout(10_000);

const title = page.getByText("Five Nights at Freddy's 2", { exact: true }).first();
const ancestry = await title.evaluate((node) => {
  const result = [];
  let current = node;
  for (let depth = 0; depth < 6 && current; depth += 1, current = current.parentElement) {
    const rect = current.getBoundingClientRect();
    result.push({
      depth,
      tag: current.tagName,
      className: current.className,
      opacity: getComputedStyle(current).opacity,
      pointerEvents: getComputedStyle(current).pointerEvents,
      rect: rect.toJSON(),
    });
  }
  return result;
});
console.log('BEFORE');
console.log(JSON.stringify(ancestry, null, 2));
await page.screenshot({ path: 'evidence/expert/12-mobile-movies-before-tap.png', fullPage: false });

const card = ancestry.find((item) => item.depth > 0 && String(item.className).includes('group')) || ancestry[2];
await page.touchscreen.tap(card.rect.x + card.rect.width / 2, card.rect.y + card.rect.height / 2);
await page.waitForTimeout(2_000);

console.log('AFTER_FIRST_TAP');
console.log(`URL=${page.url()}`);
console.log(
  JSON.stringify(
    await title.evaluate((node) => ({
      selfOpacity: getComputedStyle(node).opacity,
      parentOpacity: getComputedStyle(node.parentElement).opacity,
      visibleText: node.innerText,
    })),
    null,
    2,
  ),
);
await page.screenshot({ path: 'evidence/expert/13-mobile-movies-after-tap.png', fullPage: false });

await title.click({ force: true, noWaitAfter: true });
await page.waitForTimeout(5_000);
console.log('AFTER_TITLE_TAP');
console.log(`URL=${page.url()}`);

await browser.close();
