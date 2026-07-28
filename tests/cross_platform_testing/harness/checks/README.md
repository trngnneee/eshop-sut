# Check module contract

One exported object per item of the Task 1 checklist
(`../../gui_and_usability_testing/checklist-final.md`). The runner executes every
check once per platform in a **fresh browser context** (empty cart, empty
localStorage, no captured dialogs).

```js
export const IA01 = [
  {
    id: 'GUI-IA01-06',                 // exact checklist ID
    aspect: 'IA-01',                   // IA-01 | IA-02 | IA-03 | IA-04
    screens: 'Trang chủ',              // as in checklist-final.md
    title: 'Giá trên card dùng ký hiệu ₫ (hiện "VND")',
    task1Status: 'Failed',             // result recorded in Task 1 (Chrome, manual)
    platformSensitive: false,          // true if the outcome can legitimately differ per engine
    async run(ctx) {
      await ctx.goto('/');
      const price = await ctx.page.locator('.grid p.text-red-500').first().innerText();
      return price.includes('₫')
        ? { status: 'PASS', evidence: `Card price uses ₫: "${price}"` }
        : { status: 'FAIL', evidence: `Card price still uses VND: "${price}"`, metrics: { price } };
    },
  },
];
```

## Return value

| field | meaning |
|---|---|
| `status` | `PASS` \| `FAIL` \| `BLOCKED` (cannot be judged on this platform) |
| `evidence` | one line, **must quote the observed value** (text, computed style, count…) so a human can re-verify |
| `metrics` | optional object of raw values — this is what makes cross-platform divergence detectable |
| `snap` | optional `true` to force a screenshot even on PASS |

`ERROR` is produced by the runner when a check throws — never return it yourself.

## Rules

1. **Observe, never assume.** A check must read the live DOM / computed style /
   behaviour. Do not hard-code the Task 1 verdict.
2. **Put every platform-visible raw value into `metrics`.** The matrix builder
   diffs `metrics` across platforms; that diff is the actual Task 3 finding
   (e.g. `thousandsSeparator: "," | "."`, `validationMessage` per engine).
3. **No `expect()`** — this is a plain Node script, not Playwright Test. Return a status.
4. **Never use `page.on('dialog')`** — `ctx` already captures + auto-accepts them
   into `ctx.dialogs` (`[{type, message}]`). Read that array.
5. **Engine-safe selectors.** Prefer `getByRole` / text selectors / structural CSS.
   Avoid Chromium-only APIs (`CDPSession`, `page.emulateMedia({forcedColors})` is fine,
   `element.checkVisibility()` is not available in older WebKit).
6. **Self-clean.** A check may register users, place orders, etc. Use unique
   e-mails (`xp-${Date.now()}@t.local`) so re-runs on the next platform still work.
7. **Budget.** ≤ 60 s per check (runner timeout). Prefer explicit waits over long sleeps.
8. `BLOCKED` is legitimate: e.g. a keyboard-only check on the emulated mobile
   platforms, or `alert()` behaviour that a platform genuinely cannot express.
   Explain why in `evidence`.

## ctx API

| member | description |
|---|---|
| `ctx.page` | Playwright `Page` |
| `ctx.goto(route, {settle})` | navigate to `BASE + route`, waits for React to settle (default 700 ms) |
| `ctx.login(email?, pw?)` | logs in via the real UI, returns header text (`test@eshop.com` / `Test1234!`) |
| `ctx.addToCartFromHome(index=0, times=1)` | seeds the cart from the Home cards |
| `ctx.css(selector, prop)` / `ctx.cssOf(locator, prop)` | computed style |
| `ctx.snap(status, label?)` | overlay-stamped screenshot (runner already shoots every FAIL) |
| `ctx.dialogs` | native `alert/confirm/prompt` captured so far |
| `ctx.consoleErrors` | console errors captured so far |
| `ctx.platform` | `{key, label, engine, version, os, device}` |
| `ctx.BASE` / `ctx.API` | `http://localhost:5173` / `http://localhost:3000` |
| `ctx.USER` | seeded user `{email, password, name}` |

## SUT facts (seed data, re-created on every backend start)

* users: `admin@eshop.com` / `Admin123!` (admin), `test@eshop.com` / `Test1234!` (user)
* products id 1..5 — 1 `iPhone 15 Pro Max` 30000000, 2 `Samsung Galaxy S24 Ultra` 28000000,
  3 `MacBook Pro M3` 45000000, 4 `Tai nghe AirPods Pro 2` 6000000, 5 `Bàn phím cơ Keychron Q1` 4000000
* coupons: `SAVE10` (10 %, min 300 k), `BIGBUY` (−50 k, min 500 k), `VIP100` (−100 k, min 300 k, 2 uses), `EXPIRED`
* routes: `/`, `/login`, `/register`, `/forgot-password`, `/profile`, `/product/:id`, `/cart`, `/checkout`
* the cart lives in React state only (`CartContext`), the token in `localStorage`
