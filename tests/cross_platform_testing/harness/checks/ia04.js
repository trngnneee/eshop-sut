// IA-04 — Phản hồi & Trạng thái (Feedback & State): 17 checklist items + 2 GAP items.
//
// Every check observes the live app and derives its own verdict. Native
// alert()/confirm() are captured by ctx (ctx.dialogs) — no check registers its
// own dialog handler.

// ---------------------------------------------------------------- helpers ----

const XSS1 = '<img src=x onerror="window.__xss1=1">'; // search echo
const XSS2 = '<img src=x onerror="window.__xss2=1">'; // header "Chào, {name}"
const XSS3 = '<img src=x onerror="window.__xss3=1">'; // shipping address

/** Unique throwaway credentials — never touches the seeded test@eshop.com. */
function throwaway(name = 'XP Probe') {
  const tag = `${Date.now()}-${Math.random().toString(36).slice(2, 6)}`;
  return { email: `xp-${tag}@t.local`, password: 'Test1234!', name };
}

/** Register a throwaway user through the public API (fixture setup, not the observation). */
async function apiRegister(ctx, name = 'XP Probe') {
  const who = throwaway(name);
  const res = await ctx.page.request.post(`${ctx.API}/api/register`, {
    data: { name: who.name, email: who.email, password: who.password },
  });
  if (!res.ok()) throw new Error(`register failed: HTTP ${res.status()}`);
  return who;
}

/** Register + log in through the real login UI. Returns the credentials. */
async function freshLogin(ctx, name = 'XP Probe') {
  const who = await apiRegister(ctx, name);
  await ctx.login(who.email, who.password);
  return who;
}

/** Create one pending order for the logged-in user (fixture for order-history checks). */
async function apiCreateOrder(ctx, total = 1234000) {
  const token = await ctx.page.evaluate(() => localStorage.getItem('token'));
  const res = await ctx.page.request.post(`${ctx.API}/api/checkout`, {
    data: { items: [], total_amount: total, shipping_address: 'XP harness' },
    headers: { Authorization: `Bearer ${token}` },
  });
  return { status: res.status(), body: (await res.text()).slice(0, 160) };
}

/** In-app (SPA) navigation — keeps the React-only cart alive, unlike page.goto. */
async function clickHeader(ctx, href, wait = 800) {
  await ctx.page.locator(`header a[href="${href}"]`).first().click();
  await ctx.page.waitForTimeout(wait);
}

async function textOf(locator, fallback = '') {
  try {
    if ((await locator.count()) === 0) return fallback;
    return (await locator.first().innerText()).trim().replace(/\s+/g, ' ');
  } catch {
    return fallback;
  }
}

async function mainText(ctx, max = 400) {
  const t = await ctx.page.evaluate(() => (document.querySelector('main') || document.body).innerText);
  return t.trim().replace(/\s+/g, ' ').slice(0, max);
}

/** Cart table rows as {name, price, qty, total} — engine-neutral structural read. */
async function cartRows(ctx) {
  return ctx.page.evaluate(() =>
    Array.from(document.querySelectorAll('table tbody tr')).map((tr) => {
      const c = Array.from(tr.querySelectorAll('td')).map((td) => td.innerText.trim());
      return { name: c[0] || '', price: c[1] || '', qty: c[2] || '', total: c[3] || '' };
    }),
  );
}

/** Feedback affordances a user would actually notice. */
async function feedbackProbe(ctx) {
  return ctx.page.evaluate(() => {
    const main = document.querySelector('main') || document.body;
    return {
      header: (document.querySelector('header') || document.body).innerText.replace(/\s+/g, ' ').trim(),
      body: main.innerText.replace(/\s+/g, ' ').trim(),
      liveRegions: document.querySelectorAll('[role="alert"],[role="status"],[aria-live],.toast,.snackbar,.notification').length,
      modals: document.querySelectorAll('[role="dialog"],[role="alertdialog"],dialog,.modal').length,
      spinners: document.querySelectorAll('.animate-spin,.animate-pulse,[aria-busy="true"],[role="progressbar"],.spinner,.skeleton').length,
      icons: main.querySelectorAll('img,svg').length,
    };
  });
}

/** Orders panel of /profile (text + icon/CTA counts). */
async function ordersPanel(ctx) {
  return ctx.page.evaluate(() => {
    const heading = Array.from(document.querySelectorAll('main h2')).find((h) => /Lịch sử đơn hàng/.test(h.innerText));
    const panel = heading && heading.parentElement ? heading.parentElement : document.body;
    return {
      text: panel.innerText.replace(/\s+/g, ' ').trim().slice(0, 220),
      icons: panel.querySelectorAll('img,svg').length,
      ctas: panel.querySelectorAll('a,button').length,
      rows: panel.querySelectorAll('table tbody tr').length,
    };
  });
}

/** Signed integer from a rendered money string ("-270,000,000 ₫" → -270000000). */
function moneyOf(s) {
  if (!s) return null;
  const m = String(s).match(/-?\d[\d.,  \s]*/);
  if (!m) return null;
  const neg = m[0].trim().startsWith('-');
  const digits = m[0].replace(/\D/g, '');
  if (!digits) return null;
  return (neg ? -1 : 1) * Number(digits);
}

// ---------------------------------------------------------------- checks -----

export const IA04 = [
  {
    id: 'GUI-IA04-01',
    aspect: 'IA-04',
    screens: 'Trang chủ',
    title: '"Thêm vào giỏ" trên card có phản hồi trực quan ngay (toast/badge)',
    task1Status: 'Failed',
    platformSensitive: false,
    async run(ctx) {
      await ctx.goto('/');
      const btn = ctx.page.getByRole('button', { name: 'Thêm vào giỏ', exact: true }).first();
      await btn.waitFor({ timeout: 15000 });
      const before = await feedbackProbe(ctx);
      await btn.click();
      await ctx.page.waitForTimeout(900);
      const after = await feedbackProbe(ctx);
      const label = (await btn.innerText()).trim();

      const metrics = {
        headerBefore: before.header,
        headerAfter: after.header,
        mainTextChanged: before.body !== after.body,
        liveRegionsAfter: after.liveRegions,
        modalsAfter: after.modals,
        buttonLabelAfter: label,
        dialogCount: ctx.dialogs.length,
      };
      const anyFeedback = metrics.mainTextChanged || after.liveRegions > 0 || after.modals > 0
        || before.header !== after.header || label !== 'Thêm vào giỏ' || ctx.dialogs.length > 0;

      return anyFeedback
        ? { status: 'PASS', evidence: `Click produced feedback — header "${after.header}", ${after.liveRegions} live region(s), button "${label}"`, metrics }
        : {
            status: 'FAIL',
            evidence: `No visual feedback after click: header unchanged ("${after.header}"), 0 toast/live-region, button still "${label}", main text identical`,
            metrics,
          };
    },
  },

  {
    id: 'GUI-IA04-02',
    aspect: 'IA-04',
    screens: 'Chi tiết SP',
    title: 'MỖI click "Thêm vào giỏ hàng" đều thêm SP + feedback từ lần đầu (click đầu bị nuốt)',
    task1Status: 'Failed',
    platformSensitive: false,
    async run(ctx) {
      await ctx.goto('/product/1');
      const btn = ctx.page.locator('button:has-text("Thêm vào giỏ")').first();
      await btn.waitFor({ timeout: 15000 });
      const labelBefore = (await btn.innerText()).trim();
      await btn.click();
      await ctx.page.waitForTimeout(800);
      const labelAfter = (await btn.innerText()).trim();

      await clickHeader(ctx, '/cart');
      const rows = await cartRows(ctx);
      const cartText = await mainText(ctx, 160);

      const metrics = { labelBefore, labelAfter, cartRowCount: rows.length, rows, cartText };
      return rows.length >= 1 && labelAfter === 'Đã thêm'
        ? { status: 'PASS', evidence: `One click → cart has ${rows.length} row(s) and the button showed "${labelAfter}"`, metrics }
        : {
            status: 'FAIL',
            evidence: `First click swallowed: button "${labelBefore}" → "${labelAfter}", cart rows = ${rows.length} ("${cartText}")`,
            metrics,
          };
    },
  },

  {
    id: 'GUI-IA04-03',
    aspect: 'IA-04',
    screens: 'Giỏ hàng',
    title: '"Xóa" item có dialog xác nhận (hiện xoá ngay)',
    task1Status: 'Failed',
    platformSensitive: true,
    async run(ctx) {
      await ctx.goto('/');
      await ctx.addToCartFromHome(0, 1);
      await clickHeader(ctx, '/cart');
      const rowsBefore = await cartRows(ctx);
      if (rowsBefore.length === 0) {
        return { status: 'BLOCKED', evidence: 'Could not seed the cart from Home — no row to delete', metrics: { rowsBefore: 0 } };
      }
      const dialogsBefore = ctx.dialogs.length;
      await ctx.page.locator('button:has-text("Xóa")').first().click();
      await ctx.page.waitForTimeout(800);
      const probe = await feedbackProbe(ctx);
      const rowsAfter = await cartRows(ctx);
      const newDialogs = ctx.dialogs.slice(dialogsBefore);

      const metrics = {
        rowsBefore: rowsBefore.length,
        rowsAfter: rowsAfter.length,
        newDialogs,
        confirmDialogs: newDialogs.filter((d) => d.type === 'confirm').length,
        inPageModals: probe.modals,
        cartTextAfter: probe.body.slice(0, 160),
      };
      return metrics.confirmDialogs > 0 || probe.modals > 0
        ? { status: 'PASS', evidence: `Delete guarded: ${metrics.confirmDialogs} confirm() + ${probe.modals} in-page dialog(s)`, metrics }
        : {
            status: 'FAIL',
            evidence: `"Xóa" removed the item immediately (rows ${rowsBefore.length}→${rowsAfter.length}) with 0 confirm() and 0 in-page dialog`,
            metrics,
          };
    },
  },

  {
    id: 'GUI-IA04-04',
    aspect: 'IA-04',
    screens: 'Lịch sử ĐH',
    title: '"Hủy đơn" có dialog xác nhận trước hành động không hoàn tác',
    task1Status: 'Failed',
    platformSensitive: true,
    async run(ctx) {
      const who = await freshLogin(ctx, 'XP Cancel');
      const order = await apiCreateOrder(ctx, 999000);
      await ctx.goto('/profile', { settle: 1500 });
      const cancelBtn = ctx.page.locator('button:has-text("Hủy đơn")').first();
      if ((await cancelBtn.count()) === 0) {
        return {
          status: 'BLOCKED',
          evidence: `No "Hủy đơn" button on /profile — order fixture HTTP ${order.status}: ${order.body}`,
          metrics: { account: who.email, order, profileText: await mainText(ctx, 220) },
        };
      }
      const statusBefore = await textOf(ctx.page.locator('table tbody tr td:nth-child(4)'));
      const dialogsBefore = ctx.dialogs.length;
      await cancelBtn.click();
      await ctx.page.waitForTimeout(300);
      const probe = await feedbackProbe(ctx);
      await ctx.page.waitForTimeout(1500);
      const statusAfter = await textOf(ctx.page.locator('table tbody tr td:nth-child(4)'));
      const newDialogs = ctx.dialogs.slice(dialogsBefore);

      const metrics = {
        account: who.email,
        statusBefore,
        statusAfter,
        newDialogs,
        confirmDialogs: newDialogs.filter((d) => d.type === 'confirm').length,
        inPageModals: probe.modals,
      };
      return metrics.confirmDialogs > 0 || probe.modals > 0
        ? { status: 'PASS', evidence: `Cancel guarded by ${metrics.confirmDialogs} confirm() / ${probe.modals} in-page dialog; status "${statusBefore}"→"${statusAfter}"`, metrics }
        : {
            status: 'FAIL',
            evidence: `"Hủy đơn" cancelled immediately ("${statusBefore}"→"${statusAfter}") with 0 confirm(); only post-hoc dialog(s): ${JSON.stringify(newDialogs)}`,
            metrics,
          };
    },
  },

  {
    id: 'GUI-IA04-05',
    aspect: 'IA-04',
    screens: 'Giỏ hàng, Lịch sử ĐH',
    title: 'Empty state có icon/hình + message thân thiện + CTA (hiện text trần)',
    task1Status: 'Failed',
    platformSensitive: false,
    async run(ctx) {
      await ctx.goto('/cart');
      const cart = await feedbackProbe(ctx);
      const cartCtas = await ctx.page.locator('main a, main button').count();

      const who = await freshLogin(ctx, 'XP Empty');
      await ctx.goto('/profile', { settle: 1500 });
      const orders = await ordersPanel(ctx);

      const metrics = {
        account: who.email,
        cartEmptyText: cart.body.slice(0, 200),
        cartIcons: cart.icons,
        cartCtas,
        ordersEmptyText: orders.text,
        ordersIcons: orders.icons,
        ordersCtas: orders.ctas,
        ordersRows: orders.rows,
      };
      return cart.icons > 0 && orders.icons > 0
        ? { status: 'PASS', evidence: `Both empty states illustrated (cart ${cart.icons} icon(s), orders ${orders.icons} icon(s))`, metrics }
        : {
            status: 'FAIL',
            evidence: `Plain-text empty states: cart "${metrics.cartEmptyText}" with ${cart.icons} icon/illustration; order history "${orders.text}" with ${orders.icons} icon and ${orders.ctas} CTA`,
            metrics,
          };
    },
  },

  {
    id: 'GUI-IA04-06',
    aspect: 'IA-04',
    screens: 'Trang chủ',
    title: 'Tìm kiếm 0 kết quả có empty state ("Không tìm thấy..." + icon)',
    task1Status: 'Failed',
    platformSensitive: false,
    async run(ctx) {
      await ctx.goto('/');
      const term = 'zzzzzzzz';
      await ctx.page.locator('form input[type="text"]').first().fill(term);
      await ctx.page.getByRole('button', { name: 'Tìm', exact: true }).click();
      await ctx.page.waitForTimeout(1500);

      const observed = await ctx.page.evaluate(() => {
        const main = document.querySelector('main') || document.body;
        return {
          cards: document.querySelectorAll('.grid > div').length,
          text: main.innerText.replace(/\s+/g, ' ').trim(),
          icons: main.querySelectorAll('img,svg').length,
        };
      });
      const hasEmptyMsg = /không tìm thấy|không có sản phẩm|no results|0 sản phẩm/i.test(observed.text);
      const metrics = { searchTerm: term, cardCount: observed.cards, iconCount: observed.icons, mainText: observed.text.slice(0, 240), hasEmptyStateMessage: hasEmptyMsg };

      if (observed.cards > 0) {
        return { status: 'BLOCKED', evidence: `Search "${term}" still returned ${observed.cards} card(s) — the 0-result state cannot be judged`, metrics };
      }
      return hasEmptyMsg
        ? { status: 'PASS', evidence: `0 results shows an empty state: "${metrics.mainText}"`, metrics }
        : { status: 'FAIL', evidence: `0 results renders no empty state — main content is only "${metrics.mainText}" (${observed.cards} cards, ${observed.icons} icons)`, metrics };
    },
  },

  {
    id: 'GUI-IA04-07',
    aspect: 'IA-04',
    screens: 'Trang chủ',
    title: 'Ảnh sản phẩm trên card có alt mô tả (hiện alt="")',
    task1Status: 'Failed',
    platformSensitive: false,
    async run(ctx) {
      await ctx.goto('/');
      await ctx.page.locator('.grid img').first().waitFor({ timeout: 15000 });
      const data = await ctx.page.evaluate(() => ({
        alts: Array.from(document.querySelectorAll('.grid img')).map((i) => i.getAttribute('alt')),
        names: Array.from(document.querySelectorAll('.grid h2')).map((h) => h.innerText.trim()),
      }));
      await ctx.goto('/product/1');
      const detailAlt = await ctx.page.locator('img').first().getAttribute('alt').catch(() => null);

      const empty = data.alts.filter((a) => !a || !a.trim()).length;
      const metrics = { cardAlts: data.alts, cardNames: data.names, emptyAltCount: empty, imgCount: data.alts.length, detailAlt };
      return empty === 0
        ? { status: 'PASS', evidence: `All ${data.alts.length} card images carry alt text, e.g. "${data.alts[0]}"`, metrics }
        : {
            status: 'FAIL',
            evidence: `${empty}/${data.alts.length} Home card images have alt="${data.alts[0]}" (empty) although the visible name is "${data.names[0]}"; product detail alt="${detailAlt}"`,
            metrics,
          };
    },
  },

  {
    id: 'GUI-IA04-08',
    aspect: 'IA-04',
    screens: 'Trang chủ, Lịch sử ĐH, Chi tiết SP',
    title: 'Thao tác tải dữ liệu có loading indicator (spinner/skeleton) khi mạng chậm',
    task1Status: 'Failed',
    platformSensitive: true,
    async run(ctx) {
      const DELAY = 2500;
      await ctx.page.route('**/api/products*', async (route) => {
        await new Promise((r) => setTimeout(r, DELAY));
        await route.continue().catch(() => {});
      });
      await ctx.page.route('**/api/products/1', async (route) => {
        await new Promise((r) => setTimeout(r, DELAY));
        await route.continue().catch(() => {});
      });

      await ctx.goto('/', { settle: 700 });
      const homeLoading = await feedbackProbe(ctx);
      const homeCardsDuringLoad = await ctx.page.locator('.grid > div').count();
      await ctx.page.waitForTimeout(DELAY + 900);
      const homeCardsAfter = await ctx.page.locator('.grid > div').count();

      await ctx.goto('/product/1', { settle: 700 });
      const detailLoading = await feedbackProbe(ctx);
      await ctx.page.unroute('**/api/products*').catch(() => {});
      await ctx.page.unroute('**/api/products/1').catch(() => {});

      const metrics = {
        artificialDelayMs: DELAY,
        homeSpinnersDuringLoad: homeLoading.spinners,
        homeTextDuringLoad: homeLoading.body.slice(0, 160),
        homeCardsDuringLoad,
        homeCardsAfterDelay: homeCardsAfter,
        detailSpinnersDuringLoad: detailLoading.spinners,
        detailTextDuringLoad: detailLoading.body.slice(0, 160),
      };
      if (homeCardsDuringLoad > 0 && homeCardsDuringLoad === homeCardsAfter) {
        return { status: 'BLOCKED', evidence: `Route delay ineffective on this engine — ${homeCardsDuringLoad} cards already rendered inside the delay window`, metrics };
      }
      return homeLoading.spinners > 0 && detailLoading.spinners > 0
        ? { status: 'PASS', evidence: `Loading indicators present (home ${homeLoading.spinners}, detail ${detailLoading.spinners} spinner/skeleton elements)`, metrics }
        : {
            status: 'FAIL',
            evidence: `With a ${DELAY} ms API delay Home shows ${homeLoading.spinners} spinner/skeleton (main text "${metrics.homeTextDuringLoad}"), product detail ${detailLoading.spinners} spinner (bare text "${metrics.detailTextDuringLoad}")`,
            metrics,
          };
    },
  },

  {
    id: 'GUI-IA04-09',
    aspect: 'IA-04',
    screens: 'Chi tiết SP',
    title: 'API lỗi → error state, không kẹt "Đang tải..." vô hạn',
    task1Status: 'Failed',
    platformSensitive: true,
    async run(ctx) {
      await ctx.page.route('**/api/products/1', async (route) => {
        await route.fulfill({ status: 500, contentType: 'application/json', body: '{"error":"XP forced failure"}' }).catch(() => {});
      });
      await ctx.goto('/product/1', { settle: 2500 });
      const text = await mainText(ctx, 240);
      const actions = await ctx.page.evaluate(() =>
        Array.from(document.querySelectorAll('main button, main a')).map((b) => b.innerText.trim()).filter(Boolean),
      );
      await ctx.page.unroute('**/api/products/1').catch(() => {});

      const stuck = /Đang tải/i.test(text);
      const hasError = /lỗi|error|thử lại|không tải được|xảy ra/i.test(text);
      const metrics = { mainText: text, stuckOnLoadingText: stuck, hasErrorMessage: hasError, actionElements: actions, consoleErrorCount: ctx.consoleErrors.length, consoleErrorSample: ctx.consoleErrors.slice(0, 2) };
      return hasError && !stuck
        ? { status: 'PASS', evidence: `API 500 → error state rendered: "${text}" (actions ${JSON.stringify(actions)})`, metrics }
        : {
            status: 'FAIL',
            evidence: `API 500 leaves the page at "${text}" — no error message / retry action (actions ${JSON.stringify(actions)}); failure only visible as ${ctx.consoleErrors.length} console error(s)`,
            metrics,
          };
    },
  },

  {
    id: 'GUI-IA04-10',
    aspect: 'IA-04',
    screens: 'Quên MK, Hồ sơ, Giỏ hàng, Thanh toán',
    title: 'Feedback thành công/lỗi API dùng UI trong trang nhất quán, không alert() native',
    task1Status: 'Failed',
    platformSensitive: true,
    async run(ctx) {
      // 1) Cart → "Tiến hành thanh toán" while logged out (Cart.jsx:13 alert)
      await ctx.goto('/');
      await ctx.addToCartFromHome(0, 1);
      await clickHeader(ctx, '/cart');
      await ctx.page.locator('button:has-text("Tiến hành thanh toán")').first().click();
      await ctx.page.waitForTimeout(1000);
      const afterCartStep = ctx.dialogs.length;

      // 2) Profile update success feedback (Profile.jsx:61 alert)
      const who = await freshLogin(ctx, 'XP Alert');
      await ctx.goto('/profile', { settle: 1200 });
      await ctx.page.locator('form input').nth(2).fill('912345678');
      await ctx.page.locator('form button[type="submit"]').first().click();
      await ctx.page.waitForTimeout(1800);

      const probe = await feedbackProbe(ctx);
      const alerts = ctx.dialogs.filter((d) => d.type === 'alert');
      const metrics = {
        account: who.email,
        dialogs: ctx.dialogs,
        alertCount: alerts.length,
        alertsAfterCartStep: afterCartStep,
        alertMessages: alerts.map((d) => d.message),
        inPageFeedbackRegions: probe.liveRegions,
        profileTextAfterSave: probe.body.slice(0, 200),
      };
      return alerts.length === 0
        ? { status: 'PASS', evidence: `No native alert() captured; ${probe.liveRegions} in-page feedback region(s) instead`, metrics }
        : {
            status: 'FAIL',
            evidence: `${alerts.length} native alert() surfaced on this engine: ${alerts.map((d) => `"${d.message}"`).join(' | ')} — and 0 in-page toast/live region`,
            metrics,
          };
    },
  },

  {
    id: 'GUI-IA04-11',
    aspect: 'IA-04',
    screens: 'Đăng nhập',
    title: 'Sau 3 lần sai, UI báo rõ tài khoản bị khoá (kèm thời gian), khác message sai mật khẩu',
    task1Status: 'Failed',
    platformSensitive: false,
    async run(ctx) {
      const who = await apiRegister(ctx, 'XP Lockout'); // throwaway → never locks test@eshop.com
      await ctx.goto('/login');
      const inputs = ctx.page.locator('form input');
      const err = ctx.page.locator('div.bg-red-100');
      const messages = [];

      for (let i = 1; i <= 3; i += 1) {
        await inputs.nth(0).fill(who.email);
        await inputs.nth(1).fill(`WrongPw${i}`);
        await ctx.page.locator('form button[type="submit"]').first().click();
        await ctx.page.waitForTimeout(1000);
        messages.push(await textOf(err, '(no message)'));
      }

      // 4th attempt with the CORRECT password — the account is locked by now.
      await inputs.nth(0).fill(who.email);
      await inputs.nth(1).fill(who.password);
      await ctx.page.locator('form button[type="submit"]').first().click();
      await ctx.page.waitForTimeout(1300);
      const uiAfterLock = await textOf(err, '(no message)');
      const pathAfter = new URL(ctx.page.url()).pathname;

      const apiRes = await ctx.page.request.post(`${ctx.API}/api/login`, { data: { email: who.email, password: who.password } });
      const apiBody = (await apiRes.text()).slice(0, 200);

      const metrics = {
        account: who.email,
        uiMessagePerWrongAttempt: messages,
        uiMessageAfterLock: uiAfterLock,
        pathAfterCorrectPassword: pathAfter,
        backendStatus: apiRes.status(),
        backendBody: apiBody,
        mentionsLock: /khóa|khoá|lock/i.test(uiAfterLock),
        mentionsTime: /\d+\s*(giây|s|phút|minute|second)/i.test(uiAfterLock),
      };
      if (apiRes.status() !== 403) {
        return { status: 'BLOCKED', evidence: `Backend did not report a locked account (HTTP ${apiRes.status()}: ${apiBody}) — lockout state not reproducible here`, metrics };
      }
      return metrics.mentionsLock && uiAfterLock !== messages[0]
        ? { status: 'PASS', evidence: `Locked state has its own message: "${uiAfterLock}" (unlock time mentioned: ${metrics.mentionsTime})`, metrics }
        : {
            status: 'FAIL',
            evidence: `Backend answers 403 ${apiBody} but the UI shows the same generic text as a plain wrong password: "${uiAfterLock}" (attempts: ${JSON.stringify(messages)}) — no lock reason, no unlock time`,
            metrics,
          };
    },
  },

  {
    id: 'GUI-IA04-12',
    aspect: 'IA-04',
    screens: 'Thanh toán',
    title: 'Feedback coupon đủ 2 nhánh (hợp lệ → message + tiết kiệm + thành tiền; sai → lỗi đỏ) và số tiền tính đúng',
    task1Status: 'Passed',
    platformSensitive: true,
    async run(ctx) {
      const who = await freshLogin(ctx, 'XP Coupon'); // fresh account → per-user coupon limit never hit
      await ctx.goto('/');
      await ctx.addToCartFromHome(0, 1);
      await clickHeader(ctx, '/cart');
      await ctx.page.locator('button:has-text("Tiến hành thanh toán")').first().click();
      await ctx.page.waitForTimeout(1300);
      if (!/\/checkout$/.test(new URL(ctx.page.url()).pathname)) {
        return { status: 'BLOCKED', evidence: `Could not reach /checkout (still at ${ctx.page.url()})`, metrics: { account: who.email, url: ctx.page.url() } };
      }

      const totalRaw = await ctx.page.locator('input[type="number"]').first().inputValue();
      const total = Number(totalRaw);

      // valid branch — SAVE10 = 10 %, min 300 k
      const couponInput = ctx.page.locator('input[placeholder="Nhập mã giảm giá..."]');
      await couponInput.fill('SAVE10');
      await ctx.page.locator('button:has-text("Áp dụng")').first().click();
      await ctx.page.waitForTimeout(1600);
      const successBlock = await textOf(ctx.page.locator('div.text-green-700'), '(none)');
      const grandTotalLine = await textOf(ctx.page.locator('span.font-bold.text-xl'), '(none)');
      const savedText = (successBlock.match(/Tiết kiệm:\s*(.*?)₫/) || [null, ''])[1].trim();
      const finalText = (successBlock.match(/Thành tiền:\s*(.*?)₫/) || [null, ''])[1].trim();
      const saved = moneyOf(savedText);
      const finalAmount = moneyOf(finalText);
      const expectedSaved = Math.floor(total * 0.1);
      const expectedFinal = total - expectedSaved;

      // invalid branch
      await couponInput.fill('NOPEXP999');
      await ctx.page.locator('button:has-text("Áp dụng")').first().click();
      await ctx.page.waitForTimeout(1600);
      const errLoc = ctx.page.locator('p.text-red-600');
      const errorText = await textOf(errLoc, '(none)');
      const errorColor = (await errLoc.count()) > 0 ? await ctx.cssOf(errLoc.first(), 'color') : null;

      const metrics = {
        account: who.email,
        cartTotalInput: totalRaw,
        successBlockText: successBlock,
        savedRendered: savedText,
        finalRendered: finalText,
        savedParsed: saved,
        finalParsed: finalAmount,
        expectedSaved,
        expectedFinal,
        grandTotalLine,
        invalidCouponError: errorText,
        invalidCouponColor: errorColor,
        thousandsSeparator: (savedText.match(/\d([.,  \s])\d/) || [null, '(none)'])[1],
      };
      const validBranchOk = /Áp dụng thành công/i.test(successBlock) && saved !== null && finalAmount !== null;
      const invalidBranchOk = errorText !== '(none)' && /không tồn tại|không thể|hết hạn|giới hạn/i.test(errorText);
      const mathOk = saved === expectedSaved && finalAmount === expectedFinal;

      if (validBranchOk && invalidBranchOk && mathOk) {
        return { status: 'PASS', evidence: `SAVE10 on ${total}: "Tiết kiệm ${savedText} ₫ / Thành tiền ${finalText} ₫" = 10 % correct; invalid code → "${errorText}" (${errorColor})`, metrics };
      }
      const why = [];
      if (!validBranchOk) why.push(`valid branch incomplete ("${successBlock}")`);
      if (!invalidBranchOk) why.push(`invalid-code branch message "${errorText}"`);
      if (!mathOk) why.push(`amounts wrong: SAVE10 (10 %) on ${total} renders "Tiết kiệm ${savedText} ₫ / Thành tiền ${finalText} ₫" (grand total line "${grandTotalLine}") instead of ${expectedSaved} / ${expectedFinal}`);
      return { status: 'FAIL', evidence: why.join('; '), metrics };
    },
  },

  {
    id: 'GUI-IA04-13',
    aspect: 'IA-04',
    screens: 'Trang chủ, Header, Hồ sơ',
    title: 'Text người dùng nhập render an toàn tại 3 điểm (search echo, "Chào, {name}", địa chỉ giao hàng)',
    task1Status: 'Failed',
    platformSensitive: true,
    async run(ctx) {
      // point 2 — header "Chào, {name}" of a throwaway account whose name is the payload
      const who = await freshLogin(ctx, XSS2);

      // point 1 — search echo on Home (we are on '/' after login: no reload, flags survive)
      await ctx.page.locator('form input[type="text"]').first().fill(XSS1);
      await ctx.page.getByRole('button', { name: 'Tìm', exact: true }).click();
      await ctx.page.waitForTimeout(1600);

      const stage1 = await ctx.page.evaluate(() => {
        // smallest div that still contains the search-echo line (avoids matching the page wrapper)
        const echo = Array.from(document.querySelectorAll('main div'))
          .filter((d) => /Kết quả tìm kiếm/.test(d.textContent))
          .sort((a, b) => a.textContent.length - b.textContent.length)[0];
        const headerLink = document.querySelector('header a[href="/profile"]');
        return {
          xss1: Boolean(window.__xss1),
          xss2: Boolean(window.__xss2),
          headerHtml: headerLink ? headerLink.innerHTML.slice(0, 200) : '(no profile link)',
          headerText: (document.querySelector('header') || document.body).innerText.replace(/\s+/g, ' ').trim().slice(0, 120),
          headerImgs: document.querySelectorAll('header img').length,
          echoHtml: echo ? echo.innerHTML.slice(0, 220) : '(no echo line)',
          echoImgs: echo ? echo.querySelectorAll('img').length : 0,
        };
      });

      // point 3 — shipping address, saved then re-rendered after a full reload
      await clickHeader(ctx, '/profile', 1300);
      await ctx.page.locator('form input').nth(2).fill('912345678');
      await ctx.page.locator('form textarea').first().fill(XSS3);
      await ctx.page.locator('form button[type="submit"]').first().click();
      await ctx.page.waitForTimeout(1600);
      await ctx.goto('/profile', { settle: 2000 });
      const stage2 = await ctx.page.evaluate(() => ({
        xss3: Boolean(window.__xss3),
        xss2AfterReload: Boolean(window.__xss2),
        addressValue: (document.querySelector('form textarea') || { value: '' }).value.slice(0, 140),
        mainImgs: (document.querySelector('main') || document.body).querySelectorAll('img').length,
      }));

      const points = {
        searchEcho: { executed: stage1.xss1, injectedImgs: stage1.echoImgs, renderedHtml: stage1.echoHtml },
        headerName: { executed: stage1.xss2 || stage2.xss2AfterReload, injectedImgs: stage1.headerImgs, renderedHtml: stage1.headerHtml, headerText: stage1.headerText },
        shippingAddress: { executed: stage2.xss3, injectedImgs: stage2.mainImgs, storedValue: stage2.addressValue },
      };
      const names = Object.keys(points);
      const vulnerable = names.filter((k) => points[k].executed || points[k].injectedImgs > 0);
      const metrics = { account: who.email, payloadSearch: XSS1, payloadName: XSS2, payloadAddress: XSS3, points, vulnerablePoints: vulnerable };

      return vulnerable.length === 0
        ? { status: 'PASS', evidence: `All 3 points render as plain text — header "${stage1.headerText}", address stored as "${stage2.addressValue}", no payload executed`, metrics }
        : {
            status: 'FAIL',
            evidence: `HTML/JS executed at ${vulnerable.length}/3 point(s): ${vulnerable.join(', ')} — search echo html "${stage1.echoHtml}", header html "${stage1.headerHtml}"; safe: ${names.filter((n) => !vulnerable.includes(n)).join(', ') || 'none'}`,
            metrics,
          };
    },
  },

  {
    id: 'GUI-IA04-14',
    aspect: 'IA-04',
    screens: 'Trang chủ',
    title: 'Lỗi backend hiển thị thân thiện, không lộ SQL/stack (search `\'` → raw "Database Error")',
    task1Status: 'Failed',
    platformSensitive: false,
    async run(ctx) {
      await ctx.goto('/');
      await ctx.page.locator('form input[type="text"]').first().fill("'");
      await ctx.page.getByRole('button', { name: 'Tìm', exact: true }).click();
      await ctx.page.waitForTimeout(1800);

      const observed = await ctx.page.evaluate(() => {
        const block = document.querySelector('main div.bg-red-100');
        const main = document.querySelector('main') || document.body;
        return {
          blockPresent: Boolean(block),
          blockText: (block ? block.innerText : main.innerText).replace(/\s+/g, ' ').trim().slice(0, 400),
          blockHtml: block ? block.innerHTML.slice(0, 300) : '',
          headings: Array.from((block || main).querySelectorAll('h1,h2,h3')).map((h) => h.innerText.trim()),
        };
      });
      const leaks = ['Database Error', 'SQLITE_ERROR', 'SQL', 'syntax error'].filter((k) => new RegExp(k, 'i').test(observed.blockText));
      const metrics = { searchTerm: "'", ...observed, technicalKeywords: leaks };

      return leaks.length === 0
        ? { status: 'PASS', evidence: `Backend failure shown as a friendly message: "${observed.blockText}"`, metrics }
        : {
            status: 'FAIL',
            evidence: `Raw backend error rendered as HTML — heading(s) ${JSON.stringify(observed.headings)}, text "${observed.blockText}" (leaked: ${leaks.join(', ')})`,
            metrics,
          };
    },
  },

  {
    id: 'GUI-IA04-15',
    aspect: 'IA-04',
    screens: 'Thanh toán, Giỏ hàng',
    title: 'Sau thanh toán thành công giỏ hàng được reset (clearCart không bao giờ được gọi)',
    task1Status: 'Failed',
    platformSensitive: false,
    async run(ctx) {
      const who = await freshLogin(ctx, 'XP Reset');
      await ctx.goto('/');
      await ctx.addToCartFromHome(0, 1);
      await clickHeader(ctx, '/cart');
      const rowsBefore = await cartRows(ctx);
      await ctx.page.locator('button:has-text("Tiến hành thanh toán")').first().click();
      await ctx.page.waitForTimeout(1300);
      await ctx.page.locator('button:has-text("Xác Nhận Thanh Toán")').first().click();
      await ctx.page.waitForTimeout(2200);
      const successText = await mainText(ctx, 160);
      if (!/thành công/i.test(successText)) {
        return {
          status: 'BLOCKED',
          evidence: `Checkout did not succeed — page shows "${successText}"; dialogs ${JSON.stringify(ctx.dialogs)}`,
          metrics: { account: who.email, successText, dialogs: ctx.dialogs, rowsBefore: rowsBefore.length },
        };
      }
      await clickHeader(ctx, '/cart', 1000);
      const rowsAfter = await cartRows(ctx);
      const cartText = await mainText(ctx, 200);

      const metrics = { account: who.email, successText, rowsBefore: rowsBefore.length, rowsAfter: rowsAfter.length, rowsAfterDetail: rowsAfter, cartTextAfterOrder: cartText };
      return rowsAfter.length === 0
        ? { status: 'PASS', evidence: `Cart reset after the order (${rowsBefore.length}→0 rows): "${cartText}"`, metrics }
        : {
            status: 'FAIL',
            evidence: `Cart still holds ${rowsAfter.length} row(s) after "${successText}": ${rowsAfter.map((r) => `${r.name} x${r.qty}`).join(', ')}`,
            metrics,
          };
    },
  },

  {
    id: 'GUI-IA04-16',
    aspect: 'IA-04',
    screens: 'Lịch sử ĐH',
    title: 'Lỗi API tải đơn hiển thị khác empty state (lỗi bị nuốt → hiện "chưa có đơn")',
    task1Status: 'Failed',
    platformSensitive: true,
    async run(ctx) {
      const who = await freshLogin(ctx, 'XP OrderErr');
      await ctx.goto('/profile', { settle: 1500 });
      const trueEmpty = await ordersPanel(ctx);

      const order = await apiCreateOrder(ctx, 777000);
      await ctx.goto('/profile', { settle: 1800 });
      const withApiOk = await ordersPanel(ctx);

      await ctx.page.route('**/api/orders/my-orders*', async (route) => {
        await route.fulfill({ status: 500, contentType: 'application/json', body: '{"error":"XP forced failure"}' }).catch(() => {});
      });
      await ctx.goto('/profile', { settle: 2200 });
      const withApiError = await ordersPanel(ctx);
      await ctx.page.unroute('**/api/orders/my-orders*').catch(() => {});

      const metrics = {
        account: who.email,
        orderFixture: order,
        trueEmptyStateText: trueEmpty.text,
        rowsWithApiOk: withApiOk.rows,
        textWithApiError: withApiError.text,
        rowsWithApiError: withApiError.rows,
        identicalToEmptyState: withApiError.text === trueEmpty.text,
        consoleErrorSample: ctx.consoleErrors.slice(0, 2),
      };
      if (withApiOk.rows === 0) {
        return { status: 'BLOCKED', evidence: `Order fixture not visible on /profile (checkout HTTP ${order.status}) — error vs empty cannot be compared`, metrics };
      }
      const distinguishable = !metrics.identicalToEmptyState && /lỗi|error|thử lại|không tải/i.test(withApiError.text);
      return distinguishable
        ? { status: 'PASS', evidence: `API 500 renders a distinct error message: "${withApiError.text}" (true empty state is "${trueEmpty.text}")`, metrics }
        : {
            status: 'FAIL',
            evidence: `Account HAS ${withApiOk.rows} order(s), yet with /api/orders/my-orders → 500 the panel shows "${withApiError.text}" — identical to the true empty state "${trueEmpty.text}"`,
            metrics,
          };
    },
  },

  {
    id: 'GUI-IA04-17',
    aspect: 'IA-04',
    screens: 'Đăng ký',
    title: 'Đăng ký thành công có thông báo xác nhận (hiện navigate thẳng /login)',
    task1Status: 'Failed',
    platformSensitive: false,
    async run(ctx) {
      const who = throwaway('XP Register');
      const pw = 'Abcd 1234'; // satisfies Register.jsx's flawed regex (it requires whitespace)
      await ctx.goto('/register');
      const inputs = ctx.page.locator('form input');
      await inputs.nth(0).fill(who.name);
      await inputs.nth(1).fill(who.email);
      await inputs.nth(2).fill(pw);
      await ctx.page.locator('form button[type="submit"]').first().click();

      // poll for a flash message during and after the redirect
      let successMsg = '';
      const paths = [];
      let liveRegions = 0;
      for (let i = 0; i < 16 && !successMsg; i += 1) {
        await ctx.page.waitForTimeout(150);
        const snap = await ctx.page.evaluate(() => ({
          path: location.pathname,
          text: (document.body.innerText || '').replace(/\s+/g, ' ').trim().slice(0, 300),
          live: document.querySelectorAll('[role="alert"],[role="status"],[aria-live],.toast').length,
        })).catch(() => null);
        if (!snap) continue;
        paths.push(snap.path);
        liveRegions = Math.max(liveRegions, snap.live);
        if (/đăng ký thành công|registered successfully|mời đăng nhập/i.test(snap.text)) successMsg = snap.text;
      }
      await ctx.page.waitForTimeout(600);
      const finalPath = new URL(ctx.page.url()).pathname;
      const finalText = await ctx.page.evaluate(() => (document.body.innerText || '').replace(/\s+/g, ' ').trim().slice(0, 300));
      const probe = await ctx.page.request.post(`${ctx.API}/api/login`, { data: { email: who.email, password: pw } });

      const metrics = {
        account: who.email,
        pathsObserved: [...new Set(paths)],
        finalPath,
        finalPageText: finalText,
        successMessage: successMsg || null,
        liveRegionsSeen: liveRegions,
        dialogs: ctx.dialogs,
        loginProbeStatus: probe.status(),
      };
      if (probe.status() !== 200) {
        return { status: 'BLOCKED', evidence: `Registration itself failed (login probe HTTP ${probe.status()}), page text "${finalText.slice(0, 140)}"`, metrics };
      }
      return successMsg
        ? { status: 'PASS', evidence: `Confirmation shown: "${successMsg.slice(0, 120)}"`, metrics }
        : {
            status: 'FAIL',
            evidence: `Registration succeeded (login probe 200) but no confirmation: went straight to "${finalPath}" (paths ${JSON.stringify(metrics.pathsObserved)}), page text "${finalText.slice(0, 140)}", 0 dialogs, ${liveRegions} live region(s)`,
            metrics,
          };
    },
  },

  {
    id: 'GUI-GAP-01',
    aspect: 'IA-04',
    screens: 'Giỏ hàng (toàn app)',
    title: 'Giỏ hàng được giữ lại sau khi refresh (F5) — hiện chỉ nằm trong React state',
    task1Status: 'Failed',
    platformSensitive: false,
    async run(ctx) {
      await ctx.goto('/');
      await ctx.addToCartFromHome(0, 1);
      await clickHeader(ctx, '/cart');
      const rowsBefore = await cartRows(ctx);
      if (rowsBefore.length === 0) {
        return { status: 'BLOCKED', evidence: 'Cart could not be seeded before the reload', metrics: { rowsBefore: 0 } };
      }
      const store = await ctx.page.evaluate(() => ({ local: Object.keys(localStorage), session: Object.keys(sessionStorage) }));
      await ctx.page.reload({ waitUntil: 'domcontentloaded' });
      await ctx.page.waitForTimeout(1300);
      const rowsAfter = await cartRows(ctx);
      const cartText = await mainText(ctx, 200);

      const metrics = {
        rowsBefore: rowsBefore.length,
        rowsAfterReload: rowsAfter.length,
        cartTextAfterReload: cartText,
        localStorageKeys: store.local,
        sessionStorageKeys: store.session,
        pathAfterReload: new URL(ctx.page.url()).pathname,
      };
      return rowsAfter.length === rowsBefore.length
        ? { status: 'PASS', evidence: `Cart survived F5: ${rowsBefore.length}→${rowsAfter.length} row(s), storage keys ${JSON.stringify(store.local)}`, metrics }
        : {
            status: 'FAIL',
            evidence: `Cart lost on reload: ${rowsBefore.length}→${rowsAfter.length} row(s), page shows "${cartText}"; persisted keys ${JSON.stringify(store.local)} contain no cart entry`,
            metrics,
          };
    },
  },

  {
    id: 'GUI-GAP-02',
    aspect: 'IA-04',
    screens: 'Trang chủ, Giỏ hàng',
    title: 'Thêm cùng 1 SP nhiều lần → gộp 1 dòng, số lượng cộng dồn (hiện append dòng riêng)',
    task1Status: 'Failed',
    platformSensitive: false,
    async run(ctx) {
      await ctx.goto('/');
      const firstName = (await ctx.page.locator('.grid h2').first().innerText()).trim();
      await ctx.addToCartFromHome(0, 2);
      await clickHeader(ctx, '/cart');
      const rows = await cartRows(ctx);
      const totalRendered = await textOf(ctx.page.locator('span.text-red-600'), '(none)');

      const metrics = {
        productAdded: firstName,
        clicks: 2,
        rowCount: rows.length,
        rows,
        rowsWithSameProduct: rows.filter((r) => r.name === firstName).length,
        quantities: rows.map((r) => r.qty),
        cartTotalRendered: totalRendered,
      };
      return rows.length === 1 && Number(rows[0].qty) === 2
        ? { status: 'PASS', evidence: `2 clicks merged into 1 row with quantity ${rows[0].qty} ("${firstName}"), total ${totalRendered}`, metrics }
        : {
            status: 'FAIL',
            evidence: `2 clicks on "${firstName}" produced ${rows.length} row(s) with quantities ${JSON.stringify(metrics.quantities)} instead of 1 row × 2; total ${totalRendered}`,
            metrics,
          };
    },
  },
];
