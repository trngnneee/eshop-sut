// IA-03 "Điều hướng (Navigation)" — 15 checklist items re-executed per platform.
//
// Navigation is the most engine-sensitive aspect of this SUT: it is a React SPA
// (react-router `BrowserRouter`) whose wizard step, cart and order-success flags
// live in component state only, so every history action (Back / Forward) is a
// bfcache + state-restoration question that Blink, Gecko and WebKit answer
// differently. Every check therefore records the URL *and* the visible heading
// before and after each history action into `metrics`.

/* ------------------------------------------------------------------ helpers */

/** innerText of the first match; never hangs on a missing element. */
async function textOf(locator, timeout = 1500) {
  try {
    return (await locator.first().innerText({ timeout })).trim();
  } catch {
    return '';
  }
}

/** Everything a human uses to answer "where am I": URL + route + heading + copy. */
async function where(page, label = '') {
  const url = page.url();
  let route = url;
  try {
    const u = new URL(url);
    route = u.pathname + u.search;
  } catch { /* about:blank */ }
  const heading = await textOf(page.locator('main h1, main h2').first());
  const mainText = (await textOf(page.locator('main'), 2500)).replace(/\s+/g, ' ').slice(0, 220);
  return { label, url, route, heading, mainText };
}

/**
 * Real browser history action. Same-document (pushState) entries resolve with
 * `null`, and WebKit is markedly slower to re-render React after `popstate`,
 * hence a bounded timeout + explicit settle instead of `waitForNavigation`.
 */
async function history(page, dir, settle = 1200) {
  let error = null;
  try {
    if (dir === 'back') await page.goBack({ timeout: 8000 });
    else await page.goForward({ timeout: 8000 });
  } catch (e) {
    error = String(e.message).split('\n')[0].slice(0, 120);
  }
  await page.waitForTimeout(settle);
  return error;
}

/** Header nav links plus every computed style that could express "active". */
async function navLinks(page) {
  return page.$$eval('header nav a', (els) => els.map((el) => {
    const cs = getComputedStyle(el);
    return {
      text: (el.innerText || '').trim(),
      href: el.getAttribute('href'),
      ariaCurrent: el.getAttribute('aria-current'),
      className: el.className,
      color: cs.color,
      fontWeight: cs.fontWeight,
      textDecorationLine: cs.textDecorationLine,
      backgroundColor: cs.backgroundColor,
      borderBottom: `${cs.borderBottomWidth} ${cs.borderBottomStyle}`,
    };
  }));
}

const styleSig = (l) => [l.color, l.fontWeight, l.textDecorationLine, l.backgroundColor, l.borderBottom].join('|');

/** Controls inside <main> only — the header logo must not count as "a way back". */
async function mainLinks(page) {
  return page.$$eval('main a, main button', (els) => els.map((el) => ({
    tag: el.tagName.toLowerCase(),
    text: (el.innerText || '').trim().slice(0, 60),
    href: el.getAttribute('href'),
  })));
}

/** Breadcrumb detection: semantic markers first, then the "Trang chủ >" idiom. */
async function breadcrumbOf(page) {
  return page.evaluate(() => {
    const main = document.querySelector('main');
    if (!main) return { count: 0, sample: '', mainHead: '' };
    const cand = Array.from(main.querySelectorAll('nav, ol, [aria-label], [class*="crumb"]'));
    const hits = cand.filter((e) => {
      const meta = `${e.className || ''} ${e.getAttribute('aria-label') || ''}`;
      const txt = (e.innerText || '').replace(/\s+/g, ' ');
      return /crumb/i.test(meta) || /(Trang chủ|Home)\s*[›>»/]/.test(txt);
    });
    const txt = (main.innerText || '').replace(/\s+/g, ' ');
    const idiom = /(Trang chủ|Home)\s*[›>»/]/.test(txt);
    return {
      count: hits.length + (idiom ? 1 : 0),
      sample: hits.length ? (hits[0].innerText || '').replace(/\s+/g, ' ').slice(0, 80) : '',
      mainHead: txt.slice(0, 80),
    };
  });
}

const CART_LINK = 'header nav a[href="/cart"]';
const CONFIRM_BTN = 'main button:has-text("Xác Nhận Thanh Toán")';

/** Log in by filling the form already on screen (keeps the React cart alive). */
async function loginInPlace(ctx) {
  const inputs = ctx.page.locator('form input');
  await inputs.nth(0).fill(ctx.USER.email);
  await inputs.nth(1).fill(ctx.USER.password);
  await ctx.page.locator('form button[type="submit"]').first().click();
  await ctx.page.waitForTimeout(1500);
}

/* ------------------------------------------------------------------- checks */

export const IA03 = [
  {
    id: 'GUI-IA03-01',
    aspect: 'IA-03',
    screens: 'Tất cả 8 màn hình (Header)',
    title: 'Navbar highlight mục đang chọn (hiện chỉ hover:underline — App.jsx:22-37)',
    task1Status: 'Failed',
    platformSensitive: false,
    async run(ctx) {
      await ctx.goto('/cart');
      const links = await navLinks(ctx.page);
      const active = links.find((l) => l.href === '/cart');
      if (!active) {
        return { status: 'BLOCKED', evidence: `No header link to /cart found (nav links: ${links.map((l) => l.text).join(' | ') || 'none'})`, metrics: { links } };
      }
      const others = links.filter((l) => l !== active);
      const sameStyle = others.filter((l) => styleSig(l) === styleSig(active)).map((l) => l.text);
      const metrics = {
        route: '/cart',
        activeText: active.text,
        activeAriaCurrent: active.ariaCurrent,
        activeClass: active.className,
        activeStyleSig: styleSig(active),
        otherStyleSigs: others.map((l) => `${l.text}=${styleSig(l)}`),
        sameStyleAsActive: sameStyle,
      };
      const distinct = Boolean(active.ariaCurrent) || sameStyle.length === 0;
      return distinct
        ? { status: 'PASS', evidence: `At /cart the "Giỏ hàng" link is marked active (aria-current="${active.ariaCurrent}", style "${styleSig(active)}"), different from ${others.map((l) => l.text).join('/')}`, metrics }
        : { status: 'FAIL', evidence: `At /cart "${active.text}" has no active state — aria-current=${active.ariaCurrent}, class "${active.className}", computed style "${styleSig(active)}" identical to ${sameStyle.join('/')}`, metrics };
    },
  },

  {
    id: 'GUI-IA03-02',
    aspect: 'IA-03',
    screens: 'Tất cả 8 màn hình (Header)',
    title: 'Link "Giỏ hàng" có badge số lượng, cập nhật ngay khi thêm SP (hiện link trần — App.jsx:23)',
    task1Status: 'Failed',
    platformSensitive: false,
    async run(ctx) {
      await ctx.goto('/');
      const before = await textOf(ctx.page.locator(CART_LINK));
      const navBefore = (await textOf(ctx.page.locator('header nav'))).replace(/\s+/g, ' ');

      await ctx.addToCartFromHome(0, 1);
      await ctx.page.waitForTimeout(400);
      const after = await textOf(ctx.page.locator(CART_LINK));
      const navAfter = (await textOf(ctx.page.locator('header nav'))).replace(/\s+/g, ' ');
      const badgeNodes = await ctx.page.$$eval('header nav a[href="/cart"] *, header nav span, header nav sup', (els) => els
        .map((e) => (e.innerText || '').trim())
        .filter((t) => /^\(?\d+\)?$/.test(t)));

      // Prove the add really happened, so a missing badge is a badge bug.
      await ctx.page.locator(CART_LINK).click();
      await ctx.page.waitForTimeout(700);
      const rows = await ctx.page.locator('main table tbody tr').count();

      const metrics = { cartLinkBefore: before, cartLinkAfter: after, navBefore, navAfter, numericBadgeNodes: badgeNodes, cartRowsAfterAdd: rows };
      if (rows === 0) {
        return { status: 'BLOCKED', evidence: `Could not seed the cart on this platform (cart page shows ${rows} rows) — badge cannot be judged`, metrics };
      }
      const hasBadge = /\d/.test(after) || badgeNodes.length > 0;
      return hasBadge
        ? { status: 'PASS', evidence: `Cart link shows a quantity badge after adding 1 item: "${before}" → "${after}" (badge nodes ${JSON.stringify(badgeNodes)})`, metrics }
        : { status: 'FAIL', evidence: `Cart link text unchanged after adding 1 item (cart really holds ${rows} row): "${before}" → "${after}"; no numeric badge node in header nav ("${navAfter}")`, metrics };
    },
  },

  {
    id: 'GUI-IA03-03',
    aspect: 'IA-03',
    screens: 'Header (đã đăng nhập)',
    title: 'Nút đăng xuất nhãn chính xác "Đăng xuất" (hiện ghi "Thoát" — App.jsx:29)',
    task1Status: 'Failed',
    platformSensitive: false,
    async run(ctx) {
      const headerText = (await ctx.login()).replace(/\s+/g, ' ').trim();
      const buttons = await ctx.page.$$eval('header button', (els) => els.map((e) => (e.innerText || '').trim()));
      const metrics = { headerText, headerButtons: buttons };
      if (buttons.length === 0) {
        return { status: 'BLOCKED', evidence: `Login did not produce a logged-in header (header: "${headerText}") — logout label not observable`, metrics };
      }
      const label = buttons[0];
      return label === 'Đăng xuất'
        ? { status: 'PASS', evidence: `Logout button label is exactly "Đăng xuất" (header buttons: ${JSON.stringify(buttons)})`, metrics }
        : { status: 'FAIL', evidence: `Logout button label is "${label}", not "Đăng xuất" (header: "${headerText}")`, metrics };
    },
  },

  {
    id: 'GUI-IA03-04',
    aspect: 'IA-03',
    screens: 'Chi tiết SP, Giỏ hàng, Thanh toán',
    title: 'Có breadcrumb ở 3 trang con theo spec (hiện không có)',
    task1Status: 'Failed',
    platformSensitive: false,
    async run(ctx) {
      const seen = {};
      await ctx.goto('/product/1', { settle: 1200 });
      seen['/product/1'] = await breadcrumbOf(ctx.page);

      // /checkout is only reachable with a logged-in user + non-empty cart, and
      // the cart is React state, so walk there through the UI (no full reload).
      await ctx.login();
      await ctx.addToCartFromHome(0, 1);
      await ctx.page.locator(CART_LINK).click();
      await ctx.page.waitForTimeout(700);
      seen['/cart'] = await breadcrumbOf(ctx.page);

      await ctx.page.locator('main button:has-text("Tiến hành thanh toán")').click();
      await ctx.page.waitForTimeout(1000);
      const reached = new URL(ctx.page.url()).pathname;
      seen[reached] = await breadcrumbOf(ctx.page);

      const missing = Object.entries(seen).filter(([, v]) => v.count === 0).map(([k]) => k);
      const metrics = { breadcrumbs: seen, missing, reachedFromCart: reached };
      return missing.length === 0
        ? { status: 'PASS', evidence: `Breadcrumb present on all 3 sub-pages, e.g. /cart shows "${seen['/cart'].sample}"`, metrics }
        : { status: 'FAIL', evidence: `No breadcrumb on ${missing.join(', ')} — e.g. ${missing[0]} <main> starts with "${seen[missing[0]].mainHead}"`, metrics };
    },
  },

  {
    id: 'GUI-IA03-05',
    aspect: 'IA-03',
    screens: 'Toàn app',
    title: 'URL không tồn tại (/abc) hiển thị trang 404 thân thiện (không có route catch-all → trang trắng)',
    task1Status: 'Failed',
    platformSensitive: false,
    async run(ctx) {
      await ctx.goto('/abc', { settle: 1200 });
      const w = await where(ctx.page, 'after /abc');
      const links = await mainLinks(ctx.page);
      const homeLink = links.filter((l) => l.href === '/' || /trang chủ|home/i.test(l.text));
      const has404 = /404|không tìm thấy|not found|không tồn tại/i.test(w.mainText);
      const metrics = { ...w, mainTextLength: w.mainText.length, mainControls: links, homeLinkTexts: homeLink.map((l) => l.text), has404Wording: has404 };
      return has404 && homeLink.length > 0
        ? { status: 'PASS', evidence: `/abc renders a 404 page: "${w.mainText}" with a way home (${homeLink.map((l) => l.text).join('/')})`, metrics }
        : { status: 'FAIL', evidence: `/abc renders no 404 page — <main> text is "${w.mainText}" (${w.mainText.length} chars), ${links.length} control(s) in main, 404 wording present: ${has404}`, metrics };
    },
  },

  {
    id: 'GUI-IA03-06',
    aspect: 'IA-03',
    screens: 'Chi tiết SP',
    title: '/product/999 hiển thị thông báo thân thiện + đường quay về (hiện text kỹ thuật, không link)',
    task1Status: 'Failed',
    platformSensitive: false,
    async run(ctx) {
      await ctx.goto('/product/999', { settle: 1500 });
      const w = await where(ctx.page, 'after /product/999');
      const links = await mainLinks(ctx.page);
      const back = links.filter((l) => l.href === '/' || /trang chủ|home|quay lại|tiếp tục mua/i.test(l.text));
      const technical = /lỗi trắng trang|data rỗng|null|undefined|error/i.test(w.mainText);
      const metrics = { ...w, mainControls: links, backLinkTexts: back.map((l) => l.text), technicalWording: technical };
      return !technical && back.length > 0
        ? { status: 'PASS', evidence: `/product/999 shows a friendly message "${w.mainText}" plus a way back (${back.map((l) => l.text).join('/')})`, metrics }
        : { status: 'FAIL', evidence: `/product/999 shows "${w.mainText}" — technical wording: ${technical}, links back home inside main: ${back.length}`, metrics };
    },
  },

  {
    id: 'GUI-IA03-07',
    aspect: 'IA-03',
    screens: 'Đăng nhập',
    title: 'Link "Quên mật khẩu?" điều hướng SPA không reload trang (hiện dùng <a href> — Login.jsx:49-51)',
    task1Status: 'Failed',
    platformSensitive: false,
    async run(ctx) {
      const loads = [];
      const navs = [];
      ctx.page.on('load', () => loads.push(ctx.page.url()));
      ctx.page.on('framenavigated', (f) => {
        if (f === ctx.page.mainFrame()) navs.push(f.url());
      });

      await ctx.goto('/login');
      // A marker on window survives an SPA route change and dies on a reload.
      await ctx.page.evaluate(() => { window.__xpMarker = 'xp-alive'; });
      const loads0 = loads.length;
      const navs0 = navs.length;

      await ctx.page.locator('main a:has-text("Quên mật khẩu")').click();
      await ctx.page.waitForTimeout(1600);
      const navType = await ctx.page.evaluate(() => {
        try { return performance.getEntriesByType('navigation')[0]?.type || null; } catch { return null; }
      });
      const forgot = {
        route: new URL(ctx.page.url()).pathname,
        loadEvents: loads.length - loads0,
        frameNavigations: navs.length - navs0,
        markerSurvived: (await ctx.page.evaluate(() => window.__xpMarker || null)) === 'xp-alive',
        performanceNavigationType: navType,
      };

      // Control: a genuine react-router <Link> in the header must NOT reload.
      await ctx.page.evaluate(() => { window.__xpMarker = 'xp-alive'; });
      const loads1 = loads.length;
      const navs1 = navs.length;
      await ctx.page.locator(CART_LINK).click();
      await ctx.page.waitForTimeout(900);
      const control = {
        route: new URL(ctx.page.url()).pathname,
        loadEvents: loads.length - loads1,
        frameNavigations: navs.length - navs1,
        markerSurvived: (await ctx.page.evaluate(() => window.__xpMarker || null)) === 'xp-alive',
      };

      const metrics = { forgotPasswordLink: forgot, controlHeaderLink: control, totalLoadEvents: loads.length, totalFrameNavigations: navs.length };
      return forgot.markerSurvived && forgot.loadEvents === 0
        ? { status: 'PASS', evidence: `"Quên mật khẩu?" reached ${forgot.route} without a document reload (window marker survived, ${forgot.loadEvents} load event; control SPA link: ${control.loadEvents} load)`, metrics }
        : { status: 'FAIL', evidence: `"Quên mật khẩu?" did a FULL document reload to ${forgot.route}: window.__xpMarker lost (survived=${forgot.markerSurvived}), ${forgot.loadEvents} load event(s), ${forgot.frameNavigations} frame navigation(s), performance type "${forgot.performanceNavigationType}" — the control header <Link> to ${control.route} kept the marker (${control.loadEvents} load)`, metrics };
    },
  },

  {
    id: 'GUI-IA03-08',
    aspect: 'IA-03',
    screens: 'Thanh toán',
    title: 'Có link/nút quay lại Giỏ hàng trước khi xác nhận (hiện không có — Checkout.jsx:79-150)',
    task1Status: 'Failed',
    platformSensitive: false,
    async run(ctx) {
      await ctx.login();
      await ctx.addToCartFromHome(0, 1);
      await ctx.page.locator(CART_LINK).click();
      await ctx.page.waitForTimeout(700);
      await ctx.page.locator('main button:has-text("Tiến hành thanh toán")').click();
      await ctx.page.waitForTimeout(1000);

      const w = await where(ctx.page, 'checkout');
      if (!w.route.includes('/checkout')) {
        return { status: 'BLOCKED', evidence: `Could not reach /checkout with a seeded cart (landed on ${w.route}, heading "${w.heading}")`, metrics: { ...w, dialogs: ctx.dialogs } };
      }
      const links = await mainLinks(ctx.page);
      const backToCart = links.filter((l) => l.href === '/cart' || /giỏ hàng|quay lại giỏ/i.test(l.text));
      const metrics = { ...w, mainControls: links, backToCartCandidates: backToCart };
      return backToCart.length > 0
        ? { status: 'PASS', evidence: `Checkout offers a way back to the cart: ${JSON.stringify(backToCart)}`, metrics }
        : { status: 'FAIL', evidence: `Checkout ("${w.heading}") has no link/button back to the cart — the only main controls are ${JSON.stringify(links.map((l) => l.text))}`, metrics };
    },
  },

  {
    id: 'GUI-IA03-09',
    aspect: 'IA-03',
    screens: 'Giỏ hàng → Đăng nhập',
    title: 'Bị chặn checkout vì chưa login → đăng nhập xong quay lại giỏ/checkout (hiện luôn về / — Login.jsx:16)',
    task1Status: 'Failed',
    platformSensitive: false,
    async run(ctx) {
      await ctx.goto('/');
      await ctx.addToCartFromHome(0, 1);
      await ctx.page.locator(CART_LINK).click();
      await ctx.page.waitForTimeout(700);
      const atCart = await where(ctx.page, 'cart (guest)');

      await ctx.page.locator('main button:has-text("Tiến hành thanh toán")').click();
      await ctx.page.waitForTimeout(1400);
      const afterBlock = await where(ctx.page, 'after blocked checkout');
      const dialogs = ctx.dialogs.map((d) => `${d.type}: ${d.message}`);

      if (!afterBlock.route.includes('/login')) {
        return { status: 'BLOCKED', evidence: `Guest checkout did not route to /login (landed on ${afterBlock.route}) — the pre-login context cannot be judged. Dialogs: ${JSON.stringify(dialogs)}`, metrics: { atCart, afterBlock, dialogs } };
      }

      await loginInPlace(ctx);
      const afterLogin = await where(ctx.page, 'after login');
      const backErr = await history(ctx.page, 'back');
      const afterBack = await where(ctx.page, 'after goBack');

      // Did the cart survive the guest→login→home round trip? (SPA state only.)
      await ctx.page.locator(CART_LINK).click();
      await ctx.page.waitForTimeout(800);
      const cartRows = await ctx.page.locator('main table tbody tr').count();

      const metrics = { atCart, afterBlock, afterLogin, afterBack, goBackError: backErr, dialogs, cartRowsAfterLogin: cartRows };
      const returned = /\/cart|\/checkout/.test(afterLogin.route);
      return returned
        ? { status: 'PASS', evidence: `After logging in from the blocked checkout the user returns to ${afterLogin.route} ("${afterLogin.heading}"); cart still holds ${cartRows} row(s)`, metrics }
        : { status: 'FAIL', evidence: `Context lost: /cart → alert "${dialogs[0] || '—'}" → ${afterBlock.route}, then login lands on ${afterLogin.route} ("${afterLogin.heading}") instead of /cart|/checkout; goBack from there → ${afterBack.route} ("${afterBack.heading}"); cart still holds ${cartRows} row(s)`, metrics };
    },
  },

  {
    id: 'GUI-IA03-10',
    aspect: 'IA-03',
    screens: 'Thanh toán',
    title: 'Sau thanh toán thành công, Back trình duyệt không quay lại form có thể re-submit (Checkout.jsx:69-77)',
    task1Status: 'Passed',
    platformSensitive: true,
    async run(ctx) {
      await ctx.login();
      await ctx.addToCartFromHome(0, 1);
      await ctx.page.locator(CART_LINK).click();
      await ctx.page.waitForTimeout(700);
      await ctx.page.locator('main button:has-text("Tiến hành thanh toán")').click();
      await ctx.page.waitForTimeout(1000);
      if (!ctx.page.url().includes('/checkout')) {
        return { status: 'BLOCKED', evidence: `Could not reach /checkout to place an order (at ${new URL(ctx.page.url()).pathname}, dialogs ${JSON.stringify(ctx.dialogs)})`, metrics: { url: ctx.page.url(), dialogs: ctx.dialogs } };
      }
      await ctx.page.locator(CONFIRM_BTN).click();
      await ctx.page.waitForTimeout(2500);
      const success = await where(ctx.page, 'order success');
      if (!/thành công/i.test(success.mainText)) {
        return { status: 'BLOCKED', evidence: `Order did not complete, no success screen (heading "${success.heading}", dialogs ${JSON.stringify(ctx.dialogs)}) — Back behaviour not observable`, metrics: { success, dialogs: ctx.dialogs } };
      }

      const backErr = await history(ctx.page, 'back');
      const afterBack = await where(ctx.page, 'after goBack');
      const confirmAfterBack = await ctx.page.locator(CONFIRM_BTN).count();
      const confirmEnabled = confirmAfterBack > 0 ? await ctx.page.locator(CONFIRM_BTN).first().isEnabled() : false;

      // Forward is metrics-only: this is where engines diverge on restoring the
      // (state-only) `success` flag of the Checkout component.
      const fwdErr = await history(ctx.page, 'forward');
      const afterForward = await where(ctx.page, 'after goForward');
      const confirmAfterForward = await ctx.page.locator(CONFIRM_BTN).count();

      const metrics = {
        success,
        afterBack,
        afterForward,
        goBackError: backErr,
        goForwardError: fwdErr,
        confirmButtonsAfterBack: confirmAfterBack,
        confirmEnabledAfterBack: confirmEnabled,
        confirmButtonsAfterForward: confirmAfterForward,
        successFlagRestoredOnForward: /thành công/i.test(afterForward.mainText),
        dialogs: ctx.dialogs.map((d) => `${d.type}: ${d.message}`),
      };
      return confirmAfterBack === 0
        ? { status: 'PASS', evidence: `Back after "${success.heading}" lands on ${afterBack.route} ("${afterBack.heading}") with 0 re-submittable "Xác Nhận Thanh Toán" button; Forward → ${afterForward.route} ("${afterForward.heading}") shows ${confirmAfterForward}`, metrics }
        : { status: 'FAIL', evidence: `Back after a successful order returns to ${afterBack.route} ("${afterBack.heading}") with ${confirmAfterBack} re-submittable "Xác Nhận Thanh Toán" button (enabled=${confirmEnabled})`, metrics };
    },
  },

  {
    id: 'GUI-IA03-11',
    aspect: 'IA-03',
    screens: 'Quên mật khẩu',
    title: 'Ở bước 2 bấm Back trình duyệt: không mất tiến trình (step là state, không gắn URL — ForgotPassword.jsx:8)',
    task1Status: 'Failed',
    platformSensitive: true,
    async run(ctx) {
      // Enter the flow the way a user does: /login → "Quên mật khẩu?".
      await ctx.goto('/login');
      await ctx.page.locator('main a:has-text("Quên mật khẩu")').click();
      await ctx.page.waitForTimeout(1600);
      if (!ctx.page.url().includes('/forgot-password')) {
        return { status: 'BLOCKED', evidence: `Could not open /forgot-password from /login (at ${new URL(ctx.page.url()).pathname})`, metrics: { url: ctx.page.url() } };
      }
      await ctx.page.locator('main form input').first().fill(ctx.USER.email);
      await ctx.page.locator('main form button[type="submit"]').first().click();
      await ctx.page.waitForTimeout(1800);

      const stepOf = async () => {
        const inputs = await ctx.page.locator('main form input').count();
        const otpMessage = await textOf(ctx.page.locator('main .bg-green-100'), 1200);
        const resetButtons = await ctx.page.locator('main button:has-text("Đặt lại mật khẩu")').count();
        return { formInputs: inputs, otpMessage, resetButtons, step: resetButtons > 0 ? 2 : 1 };
      };
      const before = { ...(await where(ctx.page, 'step 2')), ...(await stepOf()) };
      if (before.step !== 2) {
        return { status: 'BLOCKED', evidence: `Never reached step 2 of the OTP flow (inputs=${before.formInputs}, message "${before.otpMessage}", dialogs ${JSON.stringify(ctx.dialogs)}) — Back behaviour not observable`, metrics: { before, dialogs: ctx.dialogs } };
      }

      const backErr = await history(ctx.page, 'back');
      const afterBack = { ...(await where(ctx.page, 'after goBack')), ...(await stepOf()) };
      const fwdErr = await history(ctx.page, 'forward');
      const afterForward = { ...(await where(ctx.page, 'after goForward')), ...(await stepOf()) };

      const metrics = {
        before,
        afterBack,
        afterForward,
        goBackError: backErr,
        goForwardError: fwdErr,
        otpPreservedOnBack: afterBack.otpMessage === before.otpMessage,
        otpRestoredOnForward: afterForward.otpMessage === before.otpMessage,
      };
      const stayed = afterBack.route.includes('/forgot-password');
      return stayed
        ? { status: 'PASS', evidence: `Back at step 2 stays on ${afterBack.route} at step ${afterBack.step} ("${afterBack.otpMessage || afterBack.heading}") — progress not lost`, metrics }
        : { status: 'FAIL', evidence: `Back at step 2 leaves the wizard entirely: ${before.route} step 2 ("${before.otpMessage}") → ${afterBack.route} ("${afterBack.heading}"); Forward returns to ${afterForward.route} at step ${afterForward.step}, OTP restored=${metrics.otpRestoredOnForward}`, metrics };
    },
  },

  {
    id: 'GUI-IA03-12',
    aspect: 'IA-03',
    screens: 'Thanh toán',
    title: 'Vào thẳng /checkout khi giỏ trống/chưa login bị chặn (hiện không guard — form hiện tổng 0 ₫)',
    task1Status: 'Failed',
    platformSensitive: false,
    async run(ctx) {
      // Fresh context + fresh document load ⇒ guest and empty cart by construction.
      await ctx.goto('/checkout', { settle: 1500 });
      const w = await where(ctx.page, 'direct /checkout');
      const confirmCount = await ctx.page.locator(CONFIRM_BTN).count();
      const confirmEnabled = confirmCount > 0 ? await ctx.page.locator(CONFIRM_BTN).first().isEnabled() : false;
      const totalInput = await ctx.page.locator('main input[type="number"]').first().inputValue().catch(() => null);
      const totalLine = await textOf(ctx.page.locator('main').getByText(/Tổng thanh toán/), 1200);
      const items = await ctx.page.locator('main ul li').count();
      const loggedIn = (await ctx.page.locator('header button').count()) > 0;
      const metrics = { ...w, confirmButtons: confirmCount, confirmEnabled, editableTotalValue: totalInput, totalLine, cartListItems: items, headerShowsLoggedIn: loggedIn, redirected: w.route !== '/checkout' };
      const guarded = w.route !== '/checkout' || confirmCount === 0;
      return guarded
        ? { status: 'PASS', evidence: `Direct /checkout as guest with an empty cart is guarded → ${w.route} ("${w.heading}"), ${confirmCount} confirm button`, metrics }
        : { status: 'FAIL', evidence: `Direct /checkout is not guarded: stays on ${w.route} showing "${w.heading}" with ${items} item(s), total input "${totalInput}", "${totalLine}" and an enabled=${confirmEnabled} "Xác Nhận Thanh Toán" button while logged out`, metrics };
    },
  },

  {
    id: 'GUI-IA03-13',
    aspect: 'IA-03',
    screens: 'Hồ sơ/ĐH',
    title: '/profile chưa login: thông báo kèm link tới đăng nhập (hiện text trần — Profile.jsx:109)',
    task1Status: 'Failed',
    platformSensitive: false,
    async run(ctx) {
      await ctx.goto('/profile', { settle: 1400 });
      const w = await where(ctx.page, 'guest /profile');
      const links = await mainLinks(ctx.page);
      const toLogin = links.filter((l) => l.href === '/login' || /đăng nhập/i.test(l.text));
      const metrics = { ...w, mainControls: links, loginLinksInMain: toLogin, redirected: w.route !== '/profile' };
      const ok = w.route.includes('/login') || toLogin.length > 0;
      return ok
        ? { status: 'PASS', evidence: `Guest /profile ${w.route.includes('/login') ? `redirects to ${w.route}` : `offers a login link ${JSON.stringify(toLogin)}`}`, metrics }
        : { status: 'FAIL', evidence: `Guest /profile stays on ${w.route} with bare text "${w.mainText}" — 0 login link/button inside main (main controls: ${JSON.stringify(links)})`, metrics };
    },
  },

  {
    id: 'GUI-IA03-14',
    aspect: 'IA-03',
    screens: 'Tất cả 8 màn hình',
    title: 'Logo "EShop" luôn về trang chủ từ mọi màn (App.jsx:21)',
    task1Status: 'Passed',
    platformSensitive: false,
    async run(ctx) {
      const routes = ['/login', '/register', '/forgot-password', '/profile', '/product/1', '/cart', '/checkout', '/abc'];
      const trips = [];
      for (const r of routes) {
        await ctx.goto(r, { settle: 500 });
        const logo = ctx.page.locator('header a[href="/"]').first();
        const logoText = await textOf(logo, 2500);
        let landed = null;
        let error = null;
        try {
          await logo.click({ timeout: 6000 });
          await ctx.page.waitForTimeout(500);
          landed = new URL(ctx.page.url()).pathname;
        } catch (e) {
          error = String(e.message).split('\n')[0].slice(0, 90);
        }
        trips.push({ from: r, logoText, landed, homeHeading: await textOf(ctx.page.locator('main h1').first(), 2000), error });
      }
      const bad = trips.filter((t) => t.landed !== '/');
      const metrics = { trips, screensTested: routes.length, failures: bad };
      return bad.length === 0
        ? { status: 'PASS', evidence: `Logo "${trips[0].logoText}" returns to "/" from all ${routes.length} screens (${routes.join(', ')}), each landing on "${trips[0].homeHeading}"`, metrics }
        : { status: 'FAIL', evidence: `Logo did not return home from ${bad.map((t) => `${t.from}→${t.landed || t.error}`).join(', ')}`, metrics };
    },
  },

  {
    id: 'GUI-IA03-15',
    aspect: 'IA-03',
    screens: 'Trang chủ, Lịch sử ĐH',
    title: 'Danh sách dài có phân trang/lazy-load hoặc không vỡ layout (render toàn bộ — Home.jsx:75, Profile.jsx:172-213)',
    task1Status: 'Passed',
    platformSensitive: true,
    async run(ctx) {
      const paginationOf = (page) => page.evaluate(() => {
        const main = document.querySelector('main');
        if (!main) return [];
        return Array.from(main.querySelectorAll('nav, button, a')).filter((e) => {
          const t = (e.innerText || '').trim();
          const meta = `${e.className || ''} ${e.getAttribute('aria-label') || ''}`;
          return /pagina|phân trang/i.test(meta) || /^(\d+|»|«|Tiếp|Trước|Next|Prev|Xem thêm|Tải thêm)$/i.test(t);
        }).map((e) => (e.innerText || '').trim() || e.getAttribute('aria-label'));
      });
      const overflowOf = (page) => page.evaluate(() => ({
        docScrollWidth: document.documentElement.scrollWidth,
        docClientWidth: document.documentElement.clientWidth,
        innerWidth: window.innerWidth,
        bodyScrollWidth: document.body.scrollWidth,
      }));

      await ctx.goto('/', { settle: 1200 });
      const cards = await ctx.page.locator('main .grid > div').count();
      const homeCounter = await textOf(ctx.page.locator('main h1').last(), 2000);
      const homePagination = await paginationOf(ctx.page);
      const homeOverflow = await overflowOf(ctx.page);
      const gridCols = await ctx.css('main .grid', 'gridTemplateColumns');

      await ctx.login();
      await ctx.goto('/profile', { settle: 1800 });
      const orderRows = await ctx.page.locator('main table tbody tr').count();
      const emptyOrders = await textOf(ctx.page.locator('main').getByText(/chưa có đơn hàng/i), 1200);
      const profilePagination = await paginationOf(ctx.page);
      const profileOverflow = await overflowOf(ctx.page);
      const table = await ctx.page.evaluate(() => {
        const el = document.querySelector('main table');
        if (!el) return null;
        const p = el.parentElement;
        return { tableScrollWidth: el.scrollWidth, parentClientWidth: p.clientWidth, parentScrollWidth: p.scrollWidth, parentOverflowX: getComputedStyle(p).overflowX };
      });

      const homeBroken = homeOverflow.docScrollWidth > homeOverflow.docClientWidth + 2;
      const profileBroken = profileOverflow.docScrollWidth > profileOverflow.docClientWidth + 2;
      const tableClipped = Boolean(table && table.tableScrollWidth > table.parentClientWidth + 2 && table.parentOverflowX === 'visible');
      const metrics = {
        viewport: ctx.page.viewportSize(),
        productCards: cards,
        homeCounter,
        gridTemplateColumns: gridCols,
        homePaginationControls: homePagination,
        homeOverflow,
        orderRows,
        emptyOrdersText: emptyOrders,
        profilePaginationControls: profilePagination,
        profileOverflow,
        orderTable: table,
        tableClipped,
        observationLimit: 'SUT seed exposes only 5 products; order-history length is whatever the shared seeded user currently has, so "very long list" could not be forced without mutating seed data',
      };
      if (homeBroken || profileBroken || tableClipped) {
        return {
          status: 'FAIL',
          evidence: `Layout breaks horizontally: home ${homeOverflow.docScrollWidth}px vs viewport ${homeOverflow.docClientWidth}px, profile ${profileOverflow.docScrollWidth}px vs ${profileOverflow.docClientWidth}px, order table ${table ? `${table.tableScrollWidth}px inside a ${table.parentClientWidth}px container (overflow-x: ${table.parentOverflowX})` : 'absent'}`,
          metrics,
        };
      }
      return {
        status: 'PASS',
        evidence: `No pagination/lazy-load control exists (home ${JSON.stringify(homePagination)}, profile ${JSON.stringify(profilePagination)}) but the layout holds: ${cards} product cards ("${homeCounter}") in grid "${gridCols}", no horizontal overflow (${homeOverflow.docScrollWidth}px ≤ ${homeOverflow.docClientWidth}px); order history ${orderRows} row(s)${table ? `, table ${table.tableScrollWidth}px in ${table.parentClientWidth}px` : ` ("${emptyOrders}")`}. Only the 5 seeded products could be observed`,
        metrics,
      };
    },
  },
];
