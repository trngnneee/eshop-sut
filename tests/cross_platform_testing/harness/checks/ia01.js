// IA-01 "Giao diện chung (General UI)" — 16 checklist items + GUI-GAP-03.
//
// Every check observes the live app (DOM text, computed style, real Tab
// presses, real viewport resizes) and returns PASS / FAIL / BLOCKED on what it
// sees on the current engine. The Task 1 (manual, Chrome) verdict is carried in
// `task1Status` purely for the comparison matrix — it is never used to decide
// the outcome here.

/* ------------------------------------------------------------------ helpers */

/** The 8 screens in scope of the checklist ("Tất cả 8 màn hình"). */
const SCREENS = [
  { route: '/', name: 'Trang chủ' },
  { route: '/login', name: 'Đăng nhập' },
  { route: '/register', name: 'Đăng ký' },
  { route: '/forgot-password', name: 'Quên mật khẩu' },
  { route: '/product/1', name: 'Chi tiết SP' },
  { route: '/cart', name: 'Giỏ hàng' },
  { route: '/checkout', name: 'Thanh toán' },
  { route: '/profile', name: 'Hồ sơ / Lịch sử ĐH' },
];

/** The 6 screens of GUI-IA01-10. */
const H1_ROUTES = ['/login', '/register', '/forgot-password', '/cart', '/checkout', '/profile'];

/** The 5 forms of GUI-IA01-13. */
const FORM_ROUTES = ['/login', '/register', '/forgot-password', '/checkout', '/profile'];

/**
 * English UI words that FR-21 forbids on a Vietnamese UI. Standard technical
 * terms the checklist explicitly allows (Email, OTP), the brand (EShop) and
 * product names (data, not static UI text) are deliberately absent.
 */
const EN_LEXICON = [
  'username', 'user name', 'password', 'sign in', 'sign up', 'sign out', 'log in', 'log out',
  'login', 'logout', 'register', 'submit', 'search', 'cart', 'checkout', 'account', 'name',
  'first name', 'last name', 'address', 'phone number', 'confirm', 'cancel', 'back', 'next',
  'previous', 'continue', 'apply', 'quantity', 'price', 'total', 'subtotal', 'order', 'orders',
  'order history', 'profile', 'forgot password', 'reset password', 'reset', 'send', 'save',
  'update', 'edit', 'delete', 'remove', 'add to cart', 'buy now', 'home', 'view details',
  'shipping', 'payment', 'coupon', 'discount', 'loading', 'error', 'success', 'required',
  'welcome', 'quantity', 'sold out',
];

/** Word-boundary (unicode-aware) search so Vietnamese words never false-positive. */
function englishHits(text) {
  const out = [];
  for (const w of EN_LEXICON) {
    const re = new RegExp(`(^|[^\\p{L}])${w.replace(/ /g, '\\s+')}($|[^\\p{L}])`, 'iu');
    if (re.test(text)) out.push(w);
  }
  return out;
}

/** Collect every static UI string (label / button / heading / th / placeholder) of the current screen. */
function scanStaticText(page) {
  return page.evaluate(() => {
    const out = [];
    const push = (s) => {
      const t = String(s || '').replace(/\s+/g, ' ').trim();
      if (t && !out.includes(t)) out.push(t.slice(0, 80));
    };
    for (const el of document.querySelectorAll('label, button, h1, h2, h3, h4, th, legend, option, a[href]')) {
      push(el.innerText);
    }
    for (const el of document.querySelectorAll('[placeholder]')) push(el.getAttribute('placeholder'));
    return out;
  });
}

const norm = (v) => String(v == null ? '' : v).replace(/\s+/g, '');

/** Computed background-color of the first button whose text contains `text`. */
function buttonStyle(page, text) {
  return page.evaluate((needle) => {
    const b = [...document.querySelectorAll('button, a[href]')].find((x) => (x.innerText || '').includes(needle));
    if (!b) return null;
    const cs = getComputedStyle(b);
    const r = b.getBoundingClientRect();
    return {
      text: b.innerText.replace(/\s+/g, ' ').trim(),
      backgroundColor: cs.backgroundColor,
      color: cs.color,
      borderStyle: `${cs.borderTopWidth} ${cs.borderTopStyle} ${cs.borderTopColor}`,
      fontWeight: cs.fontWeight,
      opacity: cs.opacity,
      width: Math.round(r.width),
      disabled: Boolean(b.disabled),
    };
  }, text);
}

/** The blue actually used elsewhere in the app (header = bg-blue-600). */
async function referenceBlue(ctx) {
  const header = await ctx.css('header', 'backgroundColor');
  return header || 'rgb(37, 99, 235)';
}

/** Drive /forgot-password to step 2 (OTP + new password + the two buttons). */
async function gotoForgotStep2(ctx) {
  await ctx.goto('/forgot-password', { settle: 800 });
  await ctx.page.locator('form input').first().fill(ctx.USER.email);
  await ctx.page.getByRole('button', { name: 'Lấy mã OTP' }).click();
  try {
    await ctx.page.getByRole('button', { name: 'Đặt lại mật khẩu' }).waitFor({ timeout: 10000 });
    return true;
  } catch {
    return false;
  }
}

/** Seed the cart and reach /cart through client-side navigation (cart is React state only). */
async function gotoCartWithItem(ctx) {
  await ctx.goto('/', { settle: 900 });
  await ctx.addToCartFromHome(0, 1);
  await ctx.page.locator('header a[href="/cart"]').click();
  try {
    await ctx.page.getByRole('button', { name: 'Tiến hành thanh toán' }).waitFor({ timeout: 10000 });
    return true;
  } catch {
    return false;
  }
}

/** Per-viewport measurement helper; tolerates emulated-mobile contexts that refuse a resize. */
async function withViewport(ctx, width, height = 800) {
  const before = ctx.page.viewportSize();
  try {
    await ctx.page.setViewportSize({ width, height });
    await ctx.page.waitForTimeout(150);
    return { requested: width, applied: (ctx.page.viewportSize() || {}).width, resized: true };
  } catch (e) {
    return {
      requested: width,
      applied: (before || {}).width || null,
      resized: false,
      reason: e.message.slice(0, 120),
    };
  }
}

/** Elements whose box sticks out past the layout viewport — evidence for "tràn ngang". */
function overflowingElements(page) {
  return page.evaluate(() => {
    const limit = document.documentElement.clientWidth;
    const out = [];
    for (const el of document.querySelectorAll('body *')) {
      const r = el.getBoundingClientRect();
      if (r.width > 0 && r.right > limit + 1) {
        out.push(`${el.tagName.toLowerCase()}.${String(el.className || '').split(/\s+/).slice(0, 2).join('.')} right=${Math.round(r.right)}`);
      }
      if (out.length >= 4) break;
    }
    return out;
  });
}

/**
 * Press Tab through one form and record the real focus sequence.
 * Links are recorded but excluded from the ordering verdict: WebKit/Safari does
 * not put <a> in the default Tab sequence, which would otherwise mask the bug.
 */
async function tabProbe(ctx, route) {
  await ctx.goto(route, { settle: 900 });
  const cands = await ctx.page.evaluate(() => {
    const scope = document.querySelector('form') || document.querySelector('main');
    if (!scope) return null;
    const visible = (el) => {
      const r = el.getBoundingClientRect();
      return r.width > 0 && r.height > 0;
    };
    const controls = [...scope.querySelectorAll('input, textarea, select, button')]
      .filter((el) => !el.disabled && visible(el));
    controls.forEach((el, i) => el.setAttribute('data-xp-idx', String(i)));
    const links = [...scope.querySelectorAll('a[href]')].filter(visible).length;
    return {
      links,
      controls: controls.map((el, i) => {
        const lab = el.closest('div') ? el.closest('div').querySelector('label') : null;
        return {
          idx: i,
          tag: el.tagName.toLowerCase(),
          type: (el.type || '').toLowerCase(),
          tabindex: el.getAttribute('tabindex'),
          label: (el.innerText || (lab && lab.innerText) || el.placeholder || '').replace(/\s+/g, ' ').trim().slice(0, 28),
        };
      }),
    };
  });
  if (!cands || cands.controls.length === 0) return null;

  const raw = [];
  const observed = [];
  const seen = new Set();
  let wrapped = false;
  const presses = Math.min(cands.controls.length + 6, 16);
  for (let i = 0; i < presses; i += 1) {
    await ctx.page.keyboard.press('Tab');
    const cur = await ctx.page.evaluate(() => {
      const a = document.activeElement;
      if (!a) return { tag: 'none', idx: null };
      return {
        tag: a.tagName.toLowerCase(),
        type: (a.type || '').toLowerCase(),
        idx: a.getAttribute ? a.getAttribute('data-xp-idx') : null,
        label: (a.innerText || a.placeholder || '').replace(/\s+/g, ' ').trim().slice(0, 22),
      };
    });
    raw.push(
      cur.idx == null
        ? `(outside:${cur.tag}${cur.label ? ' ' + cur.label : ''})`
        : `#${cur.idx}:${cur.tag}${cur.type ? '[' + cur.type + ']' : ''}`,
    );
    if (cur.idx != null) {
      const n = Number(cur.idx);
      if (seen.has(n)) { wrapped = true; break; }
      seen.add(n);
      observed.push(n);
    }
  }

  const ascending = observed.every((v, i) => i === 0 || v > observed[i - 1]);
  const unreachable = cands.controls.filter((c) => !seen.has(c.idx));
  return { route, controls: cands.controls, links: cands.links, raw, observed, ascending, unreachable, wrapped };
}

/* ------------------------------------------------------------------- checks */

export const IA01 = [
  {
    id: 'GUI-IA01-01',
    aspect: 'IA-01',
    screens: 'Đăng nhập',
    title: 'Nhãn field và nút trên form đăng nhập hiển thị bằng tiếng Việt (hiện "Username", "Sign In")',
    task1Status: 'Failed',
    platformSensitive: false,
    async run(ctx) {
      await ctx.goto('/login', { settle: 800 });
      const observed = await ctx.page.evaluate(() => ({
        labels: [...document.querySelectorAll('form label')].map((l) => l.innerText.trim()),
        submit: (document.querySelector('form button[type="submit"]') || { innerText: '' }).innerText.trim(),
        heading: (document.querySelector('main h1, main h2, main h3') || { innerText: '' }).innerText.trim(),
        links: [...document.querySelectorAll('form a')].map((a) => a.innerText.trim()),
      }));
      const strings = [...observed.labels, observed.submit, ...observed.links];
      const flagged = strings
        .map((s) => ({ text: s, hits: englishHits(s) }))
        .filter((f) => f.hits.length > 0);
      const metrics = {
        labels: observed.labels,
        submitLabel: observed.submit,
        formLinks: observed.links,
        englishStrings: flagged.map((f) => f.text),
        englishTerms: flagged.map((f) => f.hits.join('/')),
      };
      return flagged.length === 0
        ? {
          status: 'PASS',
          evidence: `Login form is fully Vietnamese: labels ${JSON.stringify(observed.labels)}, submit "${observed.submit}"`,
          metrics,
        }
        : {
          status: 'FAIL',
          evidence: `English UI text on /login: ${flagged.map((f) => `"${f.text}"`).join(', ')} (labels ${JSON.stringify(observed.labels)}, submit "${observed.submit}")`,
          metrics,
        };
    },
  },

  {
    id: 'GUI-IA01-02',
    aspect: 'IA-01',
    screens: 'Tất cả 8 màn hình',
    title: '100% text UI tĩnh bằng tiếng Việt trên toàn bộ 8 màn hình (trừ thuật ngữ chuẩn Email, OTP)',
    task1Status: 'Failed',
    platformSensitive: false,
    async run(ctx) {
      await ctx.login(); // needed so /profile renders the real screen, not "Vui lòng đăng nhập"

      const perScreen = {};
      const flaggedByScreen = {};

      // /cart only shows its table headings when it holds an item -> seed it via the SPA first.
      const cartSeeded = await gotoCartWithItem(ctx);
      if (cartSeeded) {
        const strings = await scanStaticText(ctx.page);
        perScreen['/cart (có sản phẩm)'] = strings.length;
        const hits = strings.map((s) => ({ s, h: englishHits(s) })).filter((x) => x.h.length);
        if (hits.length) flaggedByScreen['/cart (có sản phẩm)'] = hits.map((x) => x.s);
      }

      for (const s of SCREENS) {
        await ctx.goto(s.route, { settle: 900 });
        const strings = await scanStaticText(ctx.page);
        perScreen[s.route] = strings.length;
        const hits = strings.map((x) => ({ s: x, h: englishHits(x) })).filter((x) => x.h.length);
        if (hits.length) flaggedByScreen[s.route] = hits.map((x) => `${x.s} [${x.h.join('/')}]`);
      }

      const metrics = {
        screensScanned: Object.keys(perScreen).length,
        stringsPerScreen: perScreen,
        englishByScreen: flaggedByScreen,
        cartSeeded,
        allowedTerms: 'Email, OTP, EShop, VND, ₫, tên sản phẩm',
      };
      const bad = Object.entries(flaggedByScreen);
      return bad.length === 0
        ? {
          status: 'PASS',
          evidence: `Scanned ${Object.keys(perScreen).length} screens / ${Object.values(perScreen).reduce((a, b) => a + b, 0)} static strings — no English outside Email/OTP`,
          metrics,
        }
        : {
          status: 'FAIL',
          evidence: `English static text on ${bad.length} screen(s): ${bad.map(([r, v]) => `${r} → ${v.join(', ')}`).join(' | ')}`,
          metrics,
        };
    },
  },

  {
    id: 'GUI-IA01-03',
    aspect: 'IA-01',
    screens: 'Đăng ký',
    title: 'Nút submit "Đăng Ký" dùng màu hành động tích cực (hiện nền đỏ bg-red-500)',
    task1Status: 'Failed',
    platformSensitive: false,
    async run(ctx) {
      await ctx.goto('/register', { settle: 800 });
      const blue = await referenceBlue(ctx);
      const btn = await buttonStyle(ctx.page, 'Đăng Ký');
      if (!btn) return { status: 'BLOCKED', evidence: 'Submit button "Đăng Ký" not found on /register', metrics: { blue } };
      const metrics = {
        registerButtonText: btn.text,
        registerButtonBg: btn.backgroundColor,
        referenceBlue: blue,
        tailwindBlue600: 'rgb(37, 99, 235)',
        matchesReferenceBlue: norm(btn.backgroundColor) === norm(blue),
      };
      return metrics.matchesReferenceBlue
        ? {
          status: 'PASS',
          evidence: `"${btn.text}" background ${btn.backgroundColor} == app blue ${blue}`,
          metrics,
        }
        : {
          status: 'FAIL',
          evidence: `"${btn.text}" background is ${btn.backgroundColor} instead of the app's blue ${blue} (red = danger/cancel per FR-21)`,
          metrics,
        };
    },
  },

  {
    id: 'GUI-IA01-04',
    aspect: 'IA-01',
    screens: 'Chi tiết SP, Giỏ hàng, Thanh toán, Quên MK',
    title: 'Các nút hành động tích cực dùng màu xanh dương thống nhất (hiện xanh lá / cam)',
    task1Status: 'Failed',
    platformSensitive: false,
    async run(ctx) {
      await ctx.goto('/', { settle: 700 });
      const blue = await referenceBlue(ctx);
      const observed = {};

      await ctx.goto('/product/1', { settle: 1000 });
      await ctx.page.getByRole('button', { name: /Thêm vào giỏ hàng/ }).waitFor({ timeout: 15000 });
      observed['Thêm vào giỏ hàng (/product/1)'] = await buttonStyle(ctx.page, 'Thêm vào giỏ hàng');

      const cartOk = await gotoCartWithItem(ctx);
      observed['Tiến hành thanh toán (/cart)'] = cartOk ? await buttonStyle(ctx.page, 'Tiến hành thanh toán') : null;

      await ctx.goto('/checkout', { settle: 900 });
      observed['Xác Nhận Thanh Toán (/checkout)'] = await buttonStyle(ctx.page, 'Xác Nhận Thanh Toán');
      observed['Áp dụng (/checkout)'] = await buttonStyle(ctx.page, 'Áp dụng');

      const fpOk = await gotoForgotStep2(ctx);
      observed['Đặt lại mật khẩu (/forgot-password b2)'] = fpOk ? await buttonStyle(ctx.page, 'Đặt lại mật khẩu') : null;

      const backgrounds = {};
      const missing = [];
      const offSpec = [];
      for (const [label, st] of Object.entries(observed)) {
        if (!st) { missing.push(label); backgrounds[label] = null; continue; }
        backgrounds[label] = st.backgroundColor;
        if (norm(st.backgroundColor) !== norm(blue)) offSpec.push(`${label} = ${st.backgroundColor}`);
      }
      const metrics = {
        referenceBlue: blue,
        backgrounds,
        offSpecButtons: offSpec,
        unavailable: missing,
        dialogs: ctx.dialogs.map((d) => d.message),
      };
      if (offSpec.length === 0 && missing.length > 0) {
        return { status: 'BLOCKED', evidence: `Could not reach ${missing.join(', ')} on this platform; the buttons that were reachable all matched ${blue}`, metrics };
      }
      return offSpec.length === 0
        ? { status: 'PASS', evidence: `All ${Object.keys(backgrounds).length} positive-action buttons use the app blue ${blue}`, metrics }
        : {
          status: 'FAIL',
          evidence: `${offSpec.length}/${Object.keys(backgrounds).length} positive-action buttons are not the app blue ${blue}: ${offSpec.join('; ')}`,
          metrics,
        };
    },
  },

  {
    id: 'GUI-IA01-05',
    aspect: 'IA-01',
    screens: 'Quên mật khẩu',
    title: 'Nút phụ "← Quay lại" phân biệt thị giác với nút chính "Đặt lại mật khẩu" (hiện cùng bg-green-600, full-width)',
    task1Status: 'Failed',
    platformSensitive: false,
    async run(ctx) {
      const ok = await gotoForgotStep2(ctx);
      if (!ok) {
        return {
          status: 'BLOCKED',
          evidence: `Could not reach step 2 of /forgot-password (dialogs: ${JSON.stringify(ctx.dialogs.map((d) => d.message))})`,
          metrics: { dialogs: ctx.dialogs },
        };
      }
      const primary = await buttonStyle(ctx.page, 'Đặt lại mật khẩu');
      const secondary = await buttonStyle(ctx.page, 'Quay lại');
      if (!primary || !secondary) {
        return { status: 'BLOCKED', evidence: 'One of the two step-2 buttons was not rendered', metrics: { primary, secondary } };
      }
      const diffs = [];
      if (norm(primary.backgroundColor) !== norm(secondary.backgroundColor)) diffs.push('background-color');
      if (norm(primary.borderStyle) !== norm(secondary.borderStyle)) diffs.push('border');
      if (norm(primary.color) !== norm(secondary.color)) diffs.push('color');
      if (norm(primary.fontWeight) !== norm(secondary.fontWeight)) diffs.push('font-weight');
      if (Math.abs(primary.width - secondary.width) > 4) diffs.push('width');
      const metrics = {
        primaryText: primary.text,
        primaryBg: primary.backgroundColor,
        primaryBorder: primary.borderStyle,
        primaryWidth: primary.width,
        secondaryText: secondary.text,
        secondaryBg: secondary.backgroundColor,
        secondaryBorder: secondary.borderStyle,
        secondaryWidth: secondary.width,
        differingProperties: diffs,
      };
      return diffs.length > 0
        ? {
          status: 'PASS',
          evidence: `Secondary "${secondary.text}" differs from primary "${primary.text}" in ${diffs.join(', ')} (bg ${secondary.backgroundColor} vs ${primary.backgroundColor})`,
          metrics,
        }
        : {
          status: 'FAIL',
          evidence: `"${primary.text}" and "${secondary.text}" are visually identical: both bg ${primary.backgroundColor}, border "${primary.borderStyle}", ${primary.width}px wide — no secondary styling`,
          metrics,
        };
    },
  },

  {
    id: 'GUI-IA01-06',
    aspect: 'IA-01',
    screens: 'Trang chủ',
    title: 'Giá trên card sản phẩm dùng ký hiệu ₫ (Home hiện dùng "VND")',
    task1Status: 'Failed',
    platformSensitive: false,
    async run(ctx) {
      await ctx.goto('/');
      const locator = ctx.page.locator('.grid p.text-red-500').first();
      await locator.waitFor({ timeout: 15000 });
      const price = (await locator.innerText()).trim();
      const detail = await (async () => {
        await ctx.goto('/product/1', { settle: 900 });
        const p = ctx.page.locator('p.text-2xl').first();
        await p.waitFor({ timeout: 15000 });
        return (await p.innerText()).trim();
      })();
      const metrics = { homeCardPrice: price, productDetailPrice: detail, homeUsesDong: price.includes('₫'), homeUsesVND: /VND/.test(price) };
      return price.includes('₫')
        ? { status: 'PASS', evidence: `Card price uses ₫: "${price}" (detail "${detail}")`, metrics }
        : { status: 'FAIL', evidence: `Card price still uses "VND": "${price}" while Chi tiết SP uses ₫: "${detail}"`, metrics };
    },
  },

  {
    id: 'GUI-IA01-07',
    aspect: 'IA-01',
    screens: 'Trang chủ, Chi tiết SP, Giỏ hàng, Thanh toán, Lịch sử ĐH',
    title: 'Phân cách hàng nghìn nhất quán (toLocaleString() không tham số → phụ thuộc locale engine)',
    task1Status: 'Passed',
    platformSensitive: true,
    async run(ctx) {
      const sep = (s) => (String(s).match(/\d([.,\s  ])\d/) || [null, '?'])[1];

      await ctx.goto('/');
      const homeLoc = ctx.page.locator('.grid p.text-red-500').first();
      await homeLoc.waitFor({ timeout: 15000 });
      const home = (await homeLoc.innerText()).trim();

      await ctx.goto('/product/1', { settle: 900 });
      const detailLoc = ctx.page.locator('p.text-2xl').first();
      await detailLoc.waitFor({ timeout: 15000 });
      const detail = (await detailLoc.innerText()).trim();

      let cart = null;
      if (await gotoCartWithItem(ctx)) {
        cart = (await ctx.page.locator('table tbody td').nth(1).innerText()).trim();
      }

      const engine = await ctx.page.evaluate(() => ({
        navigatorLanguage: navigator.language,
        navigatorLanguages: (navigator.languages || []).join(','),
        resolvedLocale: Intl.NumberFormat().resolvedOptions().locale,
        defaultFormat: (30000000).toLocaleString(),
        viVNFormat: (30000000).toLocaleString('vi-VN'),
      }));

      const screens = { '/': home, '/product/1': detail, ...(cart ? { '/cart': cart } : {}) };
      const seps = Object.fromEntries(Object.entries(screens).map(([k, v]) => [k, sep(v)]));
      const distinct = [...new Set(Object.values(seps))];
      const metrics = {
        prices: screens,
        separatorPerScreen: seps,
        distinctSeparators: distinct,
        ...engine,
        localePinnedByApp: engine.defaultFormat === engine.viVNFormat && engine.resolvedLocale.startsWith('vi'),
      };
      return distinct.length === 1
        ? {
          status: 'PASS',
          evidence: `One separator "${distinct[0]}" on all ${Object.keys(screens).length} screens (${Object.values(screens).map((v) => `"${v}"`).join(', ')}); engine locale ${engine.resolvedLocale}, toLocaleString() unparameterised → value is engine/locale dependent`,
          metrics,
        }
        : {
          status: 'FAIL',
          evidence: `Separator differs between screens: ${Object.entries(seps).map(([k, v]) => `${k}="${v}"`).join(', ')}`,
          metrics,
        };
    },
  },

  {
    id: 'GUI-IA01-08',
    aspect: 'IA-01',
    screens: 'Chi tiết SP',
    title: 'Giá luôn render là số có định dạng kể cả khi backend trả price sai kiểu (không bao giờ "NaN ₫")',
    task1Status: 'Passed',
    platformSensitive: false,
    async run(ctx) {
      // 1. baseline with the real seed data
      await ctx.goto('/product/1', { settle: 900 });
      const priceLoc = ctx.page.locator('p.text-2xl').first();
      await priceLoc.waitFor({ timeout: 15000 });
      const validPrice = (await priceLoc.innerText()).trim();

      // 2. same screen, backend returning a non-numeric price (ProductDetail does Number(product.price))
      const badPrice = 'ba mươi triệu';
      await ctx.page.route('**/api/products/1', async (route) => {
        await route.fulfill({
          status: 200,
          contentType: 'application/json',
          headers: { 'Access-Control-Allow-Origin': '*' },
          body: JSON.stringify({
            id: 1,
            name: 'iPhone 15 Pro Max',
            price: badPrice,
            description: 'Fixture: price sai kiểu (GUI-IA01-08)',
            imageUrl: '/assets/hero.png',
          }),
        });
      });
      await ctx.goto('/product/1', { settle: 1200 });
      let rendered = null;
      try {
        await ctx.page.locator('p.text-2xl').first().waitFor({ timeout: 10000 });
        rendered = (await ctx.page.locator('p.text-2xl').first().innerText()).trim();
      } catch {
        rendered = (await ctx.page.locator('main').innerText()).replace(/\s+/g, ' ').trim().slice(0, 120);
      }
      const bodyText = (await ctx.page.locator('main').innerText()).replace(/\s+/g, ' ').trim();

      const metrics = {
        validPrice,
        stubbedApiPrice: badPrice,
        renderedPriceWithBadType: rendered,
        containsNaN: /NaN/.test(bodyText),
        screenText: bodyText.slice(0, 160),
      };
      return metrics.containsNaN
        ? {
          status: 'FAIL',
          evidence: `With price="${badPrice}" from /api/products/1 the screen renders "${rendered}" — "NaN ₫" reaches the user (valid data renders "${validPrice}")`,
          metrics,
        }
        : {
          status: 'PASS',
          evidence: `Bad price type is handled: renders "${rendered}" (no "NaN"); valid data renders "${validPrice}"`,
          metrics,
        };
    },
  },

  {
    id: 'GUI-IA01-09',
    aspect: 'IA-01',
    screens: 'Trang chủ',
    title: 'Trang chủ có đúng 1 thẻ h1 (hiện 2: tiêu đề + dòng đếm sản phẩm)',
    task1Status: 'Failed',
    platformSensitive: false,
    async run(ctx) {
      await ctx.goto('/');
      await ctx.page.locator('.grid h2').first().waitFor({ timeout: 15000 });
      const h = await ctx.page.evaluate(() => ({
        count: document.querySelectorAll('h1').length,
        texts: [...document.querySelectorAll('h1')].map((x) => x.innerText.replace(/\s+/g, ' ').trim()),
        h2Count: document.querySelectorAll('h2').length,
      }));
      const metrics = { h1Count: h.count, h1Texts: h.texts, h2Count: h.h2Count };
      return h.count === 1
        ? { status: 'PASS', evidence: `Exactly 1 <h1> on "/": ${JSON.stringify(h.texts)}`, metrics }
        : { status: 'FAIL', evidence: `"/" has ${h.count} <h1> elements: ${JSON.stringify(h.texts)} — expected exactly 1`, metrics };
    },
  },

  {
    id: 'GUI-IA01-10',
    aspect: 'IA-01',
    screens: 'Đăng nhập, Đăng ký, Quên MK, Giỏ hàng, Thanh toán, Hồ sơ/ĐH',
    title: 'Mỗi trang có đúng 1 h1 mô tả nội dung (6 trang này chỉ có h2)',
    task1Status: 'Failed',
    platformSensitive: false,
    async run(ctx) {
      await ctx.login(); // so /profile renders the real screen
      const h1Count = {};
      const h1Texts = {};
      const h2Texts = {};
      for (const route of H1_ROUTES) {
        await ctx.goto(route, { settle: 900 });
        const v = await ctx.page.evaluate(() => ({
          n: document.querySelectorAll('h1').length,
          h1: [...document.querySelectorAll('h1')].map((x) => x.innerText.replace(/\s+/g, ' ').trim()),
          h2: [...document.querySelectorAll('main h2')].map((x) => x.innerText.replace(/\s+/g, ' ').trim()),
        }));
        h1Count[route] = v.n;
        h1Texts[route] = v.h1;
        h2Texts[route] = v.h2;
      }
      const bad = Object.entries(h1Count).filter(([, n]) => n !== 1);
      const metrics = { h1CountByRoute: h1Count, h1TextsByRoute: h1Texts, h2TextsByRoute: h2Texts };
      return bad.length === 0
        ? { status: 'PASS', evidence: `All 6 routes have exactly 1 <h1>: ${JSON.stringify(h1Texts)}`, metrics }
        : {
          status: 'FAIL',
          evidence: `${bad.length}/6 routes do not have exactly 1 <h1> — counts ${JSON.stringify(h1Count)}; they only carry <h2> (e.g. /login → ${JSON.stringify(h2Texts['/login'])})`,
          metrics,
        };
    },
  },

  {
    id: 'GUI-IA01-11',
    aspect: 'IA-01',
    screens: 'Đăng nhập',
    title: 'Heading mô tả đúng chức năng trang (trang /login hiện ghi "Đăng Ký")',
    task1Status: 'Failed',
    platformSensitive: false,
    async run(ctx) {
      await ctx.goto('/login', { settle: 800 });
      const v = await ctx.page.evaluate(() => {
        const h = document.querySelector('main h1, main h2, main h3');
        return {
          heading: h ? h.innerText.replace(/\s+/g, ' ').trim() : null,
          tag: h ? h.tagName.toLowerCase() : null,
          submit: (document.querySelector('form button[type="submit"]') || { innerText: '' }).innerText.trim(),
        };
      });
      const canon = String(v.heading || '').toLowerCase();
      const ok = canon.includes('đăng nhập');
      const metrics = { heading: v.heading, headingTag: v.tag, submitLabel: v.submit, route: '/login' };
      return ok
        ? { status: 'PASS', evidence: `/login heading is <${v.tag}> "${v.heading}"`, metrics }
        : { status: 'FAIL', evidence: `/login heading is <${v.tag}> "${v.heading}" — does not describe the login page (expected "Đăng Nhập"); submit button reads "${v.submit}"`, metrics };
    },
  },

  {
    id: 'GUI-IA01-12',
    aspect: 'IA-01',
    screens: 'Tất cả 8 màn hình',
    title: 'Title tab trình duyệt mô tả trang và đổi theo trang (hiện cố định "frontend-web")',
    task1Status: 'Failed',
    platformSensitive: false,
    async run(ctx) {
      const titles = {};
      for (const s of SCREENS) {
        await ctx.goto(s.route, { settle: 700 });
        titles[s.route] = await ctx.page.title();
      }
      const distinct = [...new Set(Object.values(titles))];
      const metrics = { titleByRoute: titles, distinctTitles: distinct, distinctCount: distinct.length, screens: SCREENS.length };
      return distinct.length > 1
        ? { status: 'PASS', evidence: `document.title changes per screen (${distinct.length} distinct values): ${JSON.stringify(titles)}`, metrics }
        : {
          status: 'FAIL',
          evidence: `document.title is the same "${distinct[0]}" on all ${SCREENS.length} screens — it never describes the page`,
          metrics,
        };
    },
  },

  {
    id: 'GUI-IA01-13',
    aspect: 'IA-01',
    screens: 'Đăng nhập, Đăng ký, Quên MK, Thanh toán, Hồ sơ',
    title: 'Tab order mọi form đi trên-xuống, submit cuối (Đăng nhập có tabIndex={1} trên nút → focus nút TRƯỚC input)',
    task1Status: 'Failed',
    platformSensitive: true,
    async run(ctx) {
      await ctx.login(); // /profile needs a session
      const forms = {};
      const sequences = {};
      const orderViolations = [];
      const unreachableByRoute = {};
      let nativeButtonFocused = false;
      let anyProbe = false;

      for (const route of FORM_ROUTES) {
        const p = await tabProbe(ctx, route);
        if (!p) { forms[route] = 'no focusable control found'; continue; }
        anyProbe = true;
        sequences[route] = p.raw.join(' → ');
        forms[route] = {
          controls: p.controls.map((c) => `#${c.idx} ${c.tag}${c.type ? '[' + c.type + ']' : ''}${c.tabindex ? ' tabindex=' + c.tabindex : ''} "${c.label}"`),
          domOrder: p.controls.map((c) => c.idx),
          focusOrder: p.observed,
          linksInForm: p.links,
        };
        if (!p.ascending) {
          const first = p.controls.find((c) => c.idx === p.observed[0]);
          orderViolations.push(`${route}: focus order ${JSON.stringify(p.observed)} vs DOM order ${JSON.stringify(p.controls.map((c) => c.idx))} — first focused is #${p.observed[0]} ${first ? `${first.tag}[${first.type}] "${first.label}"${first.tabindex ? ` tabindex=${first.tabindex}` : ''}` : ''}`);
        }
        if (p.unreachable.length) {
          unreachableByRoute[route] = p.unreachable.map((c) => `#${c.idx} ${c.tag}${c.type ? '[' + c.type + ']' : ''} "${c.label}"`);
        }
        for (const idx of p.observed) {
          const c = p.controls.find((x) => x.idx === idx);
          if (c && c.tag === 'button' && !c.tabindex) nativeButtonFocused = true;
        }
      }

      const metrics = {
        forms,
        rawFocusSequence: sequences,
        orderViolations,
        unreachableControls: unreachableByRoute,
        nativeButtonsInTabOrder: nativeButtonFocused,
        note: 'links are excluded from the verdict because WebKit/Safari keeps <a> out of the default Tab sequence',
      };

      if (!anyProbe) {
        return { status: 'BLOCKED', evidence: 'No form control could be probed on this platform', metrics };
      }
      if (orderViolations.length) {
        return { status: 'FAIL', evidence: `Tab order broken on ${orderViolations.length}/${FORM_ROUTES.length} form(s) — ${orderViolations[0]}`, metrics };
      }
      const missing = Object.keys(unreachableByRoute);
      if (missing.length && !nativeButtonFocused) {
        return {
          status: 'BLOCKED',
          evidence: `This engine keeps <button> out of the default Tab sequence (no plain button ever received focus), so "submit last" cannot be judged; unreachable on ${missing.join(', ')}: ${JSON.stringify(unreachableByRoute)}`,
          metrics,
        };
      }
      if (missing.length) {
        return { status: 'FAIL', evidence: `Some form controls are never reached by Tab: ${JSON.stringify(unreachableByRoute)}`, metrics };
      }
      return {
        status: 'PASS',
        evidence: `Tab follows DOM/visual order with submit last on all ${FORM_ROUTES.length} forms (e.g. /login ${sequences['/login']})`,
        metrics,
      };
    },
  },

  {
    id: 'GUI-IA01-14',
    aspect: 'IA-01',
    screens: 'Chi tiết SP',
    title: 'Viewport ≤640px: nút "Thêm vào giỏ hàng" hiển thị đầy đủ (class bug-mobile-hidden áp margin-right:-100px)',
    task1Status: 'Failed',
    platformSensitive: true,
    async run(ctx) {
      const vp = await withViewport(ctx, 375, 812);
      await ctx.goto('/product/1', { settle: 1000 });
      await ctx.page.getByRole('button', { name: /Thêm vào giỏ hàng/ }).waitFor({ timeout: 15000 });

      const m = await ctx.page.evaluate(() => {
        const b = [...document.querySelectorAll('button')].find((x) => (x.innerText || '').includes('Thêm vào giỏ hàng'));
        if (!b) return null;
        const cs = getComputedStyle(b);
        const r = b.getBoundingClientRect();
        const parent = b.parentElement.getBoundingClientRect();
        const cx = Math.round(r.left + r.width / 2);
        const cy = Math.round(r.top + r.height / 2);
        const hitCentre = document.elementFromPoint(cx, cy);
        const hitRight = document.elementFromPoint(Math.round(r.right - 3), cy);
        return {
          text: b.innerText.trim(),
          marginRight: cs.marginRight,
          marginLeft: cs.marginLeft,
          alignSelf: cs.alignSelf,
          classes: b.className,
          rect: { left: Math.round(r.left), right: Math.round(r.right), width: Math.round(r.width) },
          parentRect: { left: Math.round(parent.left), right: Math.round(parent.right) },
          layoutWidthReserved: Math.round(r.width + parseFloat(cs.marginRight || '0') + parseFloat(cs.marginLeft || '0')),
          viewportWidth: document.documentElement.clientWidth,
          documentScrollWidth: document.documentElement.scrollWidth,
          hitCentreIsButton: Boolean(hitCentre && hitCentre.closest('button') === b),
          hitRightEdgeIsButton: Boolean(hitRight && hitRight.closest('button') === b),
          mediaQuery640: window.matchMedia('(max-width: 640px)').matches,
        };
      });
      if (!m) return { status: 'BLOCKED', evidence: 'Button "Thêm vào giỏ hàng" not found on /product/1', metrics: { viewport: vp } };

      const marginRightPx = parseFloat(m.marginRight) || 0;
      const problems = [];
      if (marginRightPx < 0) problems.push(`computed margin-right ${m.marginRight} — the ${m.rect.width}px button only reserves ${m.layoutWidthReserved}px of layout space`);
      if (m.rect.right > m.parentRect.right + 1) problems.push(`button right ${m.rect.right}px overflows its container right ${m.parentRect.right}px`);
      if (m.rect.right > m.viewportWidth + 1) problems.push(`button right ${m.rect.right}px is outside the ${m.viewportWidth}px viewport`);
      if (m.documentScrollWidth > m.viewportWidth + 1) problems.push(`page scrolls horizontally (scrollWidth ${m.documentScrollWidth} > clientWidth ${m.viewportWidth})`);
      if (!m.hitCentreIsButton || !m.hitRightEdgeIsButton) problems.push('button is not hit-testable over its whole width');

      const metrics = { viewport: vp, ...m };
      return problems.length === 0
        ? {
          status: 'PASS',
          evidence: `At ${m.viewportWidth}px the button "${m.text}" is intact: rect ${m.rect.left}–${m.rect.right}px inside container ${m.parentRect.left}–${m.parentRect.right}px, margin-right ${m.marginRight}, hit-test OK`,
          metrics,
        }
        : {
          status: 'FAIL',
          evidence: `At ${m.viewportWidth}px (max-width:640px active=${m.mediaQuery640}) button "${m.text}": ${problems.join('; ')}`,
          metrics,
        };
    },
  },

  {
    id: 'GUI-IA01-15',
    aspect: 'IA-01',
    screens: 'Trang chủ',
    title: 'Grid sản phẩm 1/2/3 cột theo breakpoint, không horizontal scroll ở 375/768/1280px',
    task1Status: 'Passed',
    platformSensitive: true,
    async run(ctx) {
      const expected = { 375: 1, 768: 2, 1280: 3 };
      const columns = {};
      const gridTemplate = {};
      const overflow = {};
      const overflowingBy = {};
      const media = {};
      const viewports = {};

      for (const w of [375, 768, 1280]) {
        viewports[w] = await withViewport(ctx, w, 800);
        await ctx.goto('/', { settle: 900 });
        await ctx.page.locator('.grid h2').first().waitFor({ timeout: 15000 });
        const v = await ctx.page.evaluate(() => {
          const grid = document.querySelector('.grid');
          const cs = grid ? getComputedStyle(grid) : null;
          return {
            template: cs ? cs.gridTemplateColumns : null,
            cols: cs ? cs.gridTemplateColumns.trim().split(/\s+/).length : 0,
            clientWidth: document.documentElement.clientWidth,
            innerWidth: window.innerWidth,
            scrollWidth: document.documentElement.scrollWidth,
            bodyScrollWidth: document.body.scrollWidth,
            sm: window.matchMedia('(min-width: 640px)').matches,
            md: window.matchMedia('(min-width: 768px)').matches,
          };
        });
        columns[w] = v.cols;
        gridTemplate[w] = v.template;
        media[w] = { clientWidth: v.clientWidth, innerWidth: v.innerWidth, sm640: v.sm, md768: v.md };
        overflow[w] = v.scrollWidth > v.clientWidth + 1;
        if (overflow[w]) {
          overflowingBy[w] = `${v.scrollWidth - v.clientWidth}px (scrollWidth ${v.scrollWidth} vs clientWidth ${v.clientWidth}) from ${JSON.stringify(await overflowingElements(ctx.page))}`;
        }
      }

      const wrongCols = Object.entries(expected).filter(([w, n]) => columns[w] !== n);
      const scrolls = Object.entries(overflow).filter(([, bad]) => bad).map(([w]) => w);
      const metrics = {
        expectedColumns: expected,
        columnsByViewport: columns,
        gridTemplateByViewport: gridTemplate,
        horizontalOverflowByViewport: overflow,
        overflowDetail: overflowingBy,
        mediaByViewport: media,
        viewportResize: viewports,
      };
      const problems = [];
      if (wrongCols.length) problems.push(`columns ${wrongCols.map(([w, n]) => `${w}px → ${columns[w]} (expected ${n})`).join(', ')}`);
      if (scrolls.length) problems.push(`horizontal scroll at ${scrolls.map((w) => `${w}px: ${overflowingBy[w]}`).join(' | ')}`);
      return problems.length === 0
        ? { status: 'PASS', evidence: `Grid is ${columns[375]}/${columns[768]}/${columns[1280]} columns at 375/768/1280px with no horizontal scroll`, metrics }
        : { status: 'FAIL', evidence: `Observed ${columns[375]}/${columns[768]}/${columns[1280]} columns at 375/768/1280px — ${problems.join('; ')}`, metrics };
    },
  },

  {
    id: 'GUI-IA01-16',
    aspect: 'IA-01',
    screens: 'Trang chủ',
    title: 'Tên sản phẩm dài bị truncate vẫn xem được đầy đủ, không phá layout',
    task1Status: 'Failed',
    platformSensitive: true,
    async run(ctx) {
      const LONG = 'Tai nghe không dây chống ồn chủ động bản đặc biệt phiên bản giới hạn 2026 màu xanh dương';
      await ctx.page.route('**/api/products?**', async (route) => {
        let list = [];
        try {
          const res = await route.fetch();
          const json = await res.json();
          if (Array.isArray(json)) list = json;
        } catch { /* fall through to the synthetic fixture */ }
        const base = list[0] || { id: 1, price: 30000000, description: 'fixture', imageUrl: '/assets/hero.png' };
        list = [{ ...base, id: 9901, name: LONG }, ...list];
        await route.fulfill({
          status: 200,
          contentType: 'application/json',
          headers: { 'Access-Control-Allow-Origin': '*' },
          body: JSON.stringify(list),
        });
      });

      const perViewport = {};
      for (const w of [1280, 375]) {
        const vp = await withViewport(ctx, w, 800);
        await ctx.goto('/', { settle: 1000 });
        await ctx.page.locator('.grid h2').first().waitFor({ timeout: 15000 });
        const v = await ctx.page.evaluate(() => {
          const h = document.querySelector('.grid h2');
          if (!h) return null;
          const cs = getComputedStyle(h);
          const card = h.closest('div');
          const grid = document.querySelector('.grid');
          const hr = h.getBoundingClientRect();
          const cr = card.getBoundingClientRect();
          const gr = grid.getBoundingClientRect();
          return {
            renderedText: h.innerText.replace(/\s+/g, ' ').trim(),
            fullTextLength: h.textContent.trim().length,
            scrollWidth: h.scrollWidth,
            clientWidth: h.clientWidth,
            truncated: h.scrollWidth > h.clientWidth + 1,
            textOverflow: cs.textOverflow,
            whiteSpace: cs.whiteSpace,
            overflow: cs.overflow,
            titleAttr: h.getAttribute('title'),
            ariaLabel: h.getAttribute('aria-label'),
            cardTitleAttr: card.getAttribute('title'),
            nameOverflowsCard: hr.right > cr.right + 1,
            cardOverflowsGrid: cr.right > gr.right + 1,
            cardWidth: Math.round(cr.width),
            documentScrollWidth: document.documentElement.scrollWidth,
            viewportWidth: document.documentElement.clientWidth,
          };
        });
        perViewport[w] = { viewport: vp, ...(v || { missing: true }) };
      }

      const at375 = perViewport[375];
      const at1280 = perViewport[1280];
      const anyTruncated = [at375, at1280].some((x) => x && x.truncated);
      const tooltip = [at375, at1280].some((x) => x && (x.titleAttr || x.ariaLabel || x.cardTitleAttr));
      const layoutBroken = [at375, at1280].some((x) => x && (x.nameOverflowsCard || x.cardOverflowsGrid));

      const metrics = {
        fixtureName: LONG,
        fixtureNameLength: LONG.length,
        byViewport: perViewport,
        truncated: anyTruncated,
        hasTooltip: tooltip,
        layoutBroken,
      };
      const problems = [];
      if (anyTruncated && !tooltip) problems.push(`name is clipped (scrollWidth ${at1280 && at1280.scrollWidth}px vs clientWidth ${at1280 && at1280.clientWidth}px, text-overflow "${at1280 && at1280.textOverflow}") but carries no title/aria-label — the full name cannot be read`);
      if (layoutBroken) problems.push('the long name pushes past its card/grid box');
      return problems.length === 0
        ? {
          status: 'PASS',
          evidence: `Long name (${LONG.length} chars) renders as "${at1280 && at1280.renderedText}" — truncated=${anyTruncated}, tooltip=${tooltip}, layout intact`,
          metrics,
        }
        : { status: 'FAIL', evidence: `Long product name (${LONG.length} chars): ${problems.join('; ')}`, metrics };
    },
  },

  {
    id: 'GUI-GAP-03',
    aspect: 'IA-01',
    screens: 'Toàn app',
    title: 'Thẻ <html> khai báo đúng ngôn ngữ nội dung (hiện lang="en" trong khi UI tiếng Việt)',
    task1Status: 'Failed',
    platformSensitive: false,
    async run(ctx) {
      const langByRoute = {};
      for (const route of ['/', '/login', '/product/1']) {
        await ctx.goto(route, { settle: 700 });
        langByRoute[route] = await ctx.page.evaluate(() => ({
          lang: document.documentElement.getAttribute('lang'),
          computedLang: document.documentElement.lang,
          dir: document.documentElement.getAttribute('dir'),
        }));
      }
      const lang = langByRoute['/'].lang;
      const uiIsVietnamese = await ctx.page.evaluate(() => /[ăâđêôơưàáảãạ]/i.test(document.body.innerText));
      const metrics = {
        htmlLang: lang,
        langByRoute,
        uiTextIsVietnamese: uiIsVietnamese,
        navigatorLanguage: await ctx.page.evaluate(() => navigator.language),
      };
      return String(lang || '').toLowerCase().startsWith('vi')
        ? { status: 'PASS', evidence: `<html lang="${lang}"> matches the Vietnamese UI`, metrics }
        : {
          status: 'FAIL',
          evidence: `<html lang="${lang}"> on every route while the UI text is Vietnamese (WCAG 3.1.1) — expected lang="vi"`,
          metrics,
        };
    },
  },
];
