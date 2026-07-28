// IA-02 "Biểu mẫu (Forms)" — 15 checklist items (GUI-IA02-01..14 + GUI-GAP-04).
//
// Every check drives the real forms of the SUT and reports what the *engine under
// test* actually does. The interesting cross-platform signal for this aspect is
// native HTML5 constraint validation: `validationMessage` wording/localisation,
// `validity.*` flags, how `input[type=number]` reacts to letters, and how a
// disabled input behaves on focus. All of that is dumped into `metrics`.

const norm = (s) => (s || '').replace(/\s+/g, ' ').trim();
const uniqEmail = () => `xp-${Date.now()}-${Math.floor(Math.random() * 10000)}@t.local`;
// Password that satisfies Register.jsx' flawed regex (it *requires* a whitespace).
const REGEX_OK_PW = 'Abc defg1';
// The password the on-screen hint promises should work (upper/lower/digit/special).
const HINT_PW = 'Abcdef1!';

/**
 * Tag every form control inside `scope` with `data-xp="<index>"` and return a
 * DOM descriptor per control (label text, type, constraint attributes, …).
 */
async function scan(page, scope = 'form') {
  const sel = `${scope} input, ${scope} textarea, ${scope} select`;
  await page.waitForSelector(sel, { timeout: 15000 });
  return page.evaluate((s) => {
    const nm = (t) => (t || '').replace(/\s+/g, ' ').trim();
    const els = Array.from(document.querySelectorAll(s));
    return els.map((el, i) => {
      el.setAttribute('data-xp', String(i));
      let lab = null;
      if (el.id) lab = document.querySelector(`label[for="${el.id}"]`);
      if (!lab) lab = el.closest('label');
      if (!lab && el.parentElement) lab = el.parentElement.querySelector('label');
      if (!lab && el.parentElement && el.parentElement.parentElement) {
        lab = el.parentElement.parentElement.querySelector('label');
      }
      const text = nm(lab && lab.textContent);
      return {
        idx: i,
        label: text,
        tag: el.tagName.toLowerCase(),
        type: el.getAttribute('type'),
        required: el.required,
        ariaRequired: el.getAttribute('aria-required'),
        id: el.id || null,
        name: el.getAttribute('name') || null,
        labelFor: lab ? lab.getAttribute('for') : null,
        starOnLabel: /\*/.test(text),
        placeholder: el.getAttribute('placeholder') || null,
        maxlengthAttr: el.getAttribute('maxlength'),
        patternAttr: el.getAttribute('pattern'),
        minAttr: el.getAttribute('min'),
        maxAttr: el.getAttribute('max'),
        stepAttr: el.getAttribute('step'),
        inputmodeAttr: el.getAttribute('inputmode'),
        disabled: el.disabled,
        readOnly: el.readOnly,
      };
    });
  }, sel);
}

const find = (fields, re, fallbackIdx = null) =>
  fields.find((f) => re.test(f.label)) ||
  (fallbackIdx !== null && fields[fallbackIdx] ? fields[fallbackIdx] : null);

const at = (page, field) => page.locator(`[data-xp="${field.idx}"]`);

/** Live constraint-validation state of one tagged control. */
async function validity(page, field) {
  return page.evaluate((i) => {
    const el = document.querySelector(`[data-xp="${i}"]`);
    if (!el) return null;
    const v = el.validity;
    return {
      value: el.value,
      valueLength: el.value.length,
      validationMessage: el.validationMessage,
      willValidate: el.willValidate,
      valid: v.valid,
      valueMissing: v.valueMissing,
      typeMismatch: v.typeMismatch,
      patternMismatch: v.patternMismatch,
      tooLong: v.tooLong,
      tooShort: v.tooShort,
      rangeUnderflow: v.rangeUnderflow,
      rangeOverflow: v.rangeOverflow,
      stepMismatch: v.stepMismatch,
      badInput: v.badInput,
      formValid: el.form ? el.form.checkValidity() : null,
      maxLengthProp: el.maxLength,
    };
  }, field.idx);
}

/** First in-page error banner (Login/Register use `bg-red-100`). */
async function pageError(page) {
  const box = page.locator('div[class*="bg-red-100"]');
  if ((await box.count()) === 0) return null;
  const first = box.first();
  const text = norm(await first.innerText().catch(() => ''));
  if (!text) return null;
  const bb = await first.boundingBox().catch(() => null);
  return { text, y: bb ? Math.round(bb.y) : null };
}

async function submitButton(page) {
  const typed = page.locator('form button[type="submit"]');
  if (await typed.count()) return typed.first();
  return page.locator('form button').first();
}

async function submitY(page) {
  const btn = await submitButton(page);
  const bb = await btn.boundingBox().catch(() => null);
  return bb ? Math.round(bb.y) : null;
}

const bodyText = async (page) => norm(await page.locator('body').innerText().catch(() => ''));

async function engineLocale(page) {
  return page.evaluate(() => ({
    navigatorLanguage: navigator.language,
    navigatorLanguages: (navigator.languages || []).join(','),
    documentLang: document.documentElement.lang || '(empty)',
  }));
}

/** Vietnamese-looking message? (diacritics or well-known VN validation words) */
const isVietnamese = (s) =>
  /[àáảãạăằắẳẵặâầấẩẫậđèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵ]/i.test(s || '') ||
  /(vui lòng|bắt buộc|hãy nhập|không được để trống)/i.test(s || '');

/** Log in, then open /profile and wait for the profile form to render. */
async function openProfile(ctx) {
  await ctx.login();
  await ctx.goto('/profile', { settle: 200 });
  await ctx.page.waitForSelector('form input', { timeout: 20000 });
  await ctx.page.waitForTimeout(400);
}

/** Log in, seed the cart, then walk Home → Cart → Checkout client-side. */
async function openCheckout(ctx) {
  await ctx.login();
  await ctx.addToCartFromHome(0, 1);
  await ctx.page.getByRole('link', { name: 'Giỏ hàng', exact: true }).click();
  const pay = ctx.page.getByRole('button', { name: /Tiến hành thanh toán/ });
  await pay.waitFor({ timeout: 15000 });
  await pay.click();
  await ctx.page.waitForSelector('input[type="number"]', { timeout: 15000 });
  await ctx.page.waitForTimeout(300);
}

/** Drive /forgot-password step 1 with a known e-mail and land on step 2. */
async function forgotToStep2(ctx, email) {
  await ctx.goto('/forgot-password');
  let fields = await scan(ctx.page);
  await at(ctx.page, fields[0]).fill(email);
  const btn = await submitButton(ctx.page);
  await btn.click();
  await ctx.page.waitForSelector('div[class*="bg-green-100"]', { timeout: 15000 });
  await ctx.page.waitForTimeout(300);
  fields = await scan(ctx.page);
  const otpMessage = norm(await ctx.page.locator('div[class*="bg-green-100"]').first().innerText());
  return { fields, otpMessage };
}

/** Select-all + real keystrokes (works on input[type=number] where fill() throws). */
async function retype(page, field, text) {
  const loc = at(page, field);
  await loc.click({ timeout: 5000 }).catch(() => {});
  await loc.evaluate((el) => {
    el.focus();
    if (typeof el.select === 'function') el.select();
  });
  await page.keyboard.press('Backspace');
  if (text) await page.keyboard.type(text, { delay: 20 });
  await page.waitForTimeout(200);
}

export const IA02 = [
  {
    id: 'GUI-IA02-01',
    aspect: 'IA-02',
    screens: 'Đăng ký, Đăng nhập, Quên MK, Hồ sơ',
    title: 'Mọi field required hiển thị dấu "*" cạnh nhãn',
    task1Status: 'Failed',
    platformSensitive: false,
    async run(ctx) {
      const brief = (f) => ({ label: f.label, required: f.required, ariaRequired: f.ariaRequired, star: f.starOnLabel });
      const perForm = {};
      for (const route of ['/register', '/login', '/forgot-password']) {
        await ctx.goto(route);
        perForm[route] = (await scan(ctx.page)).map(brief);
      }
      await openProfile(ctx);
      perForm['/profile'] = (await scan(ctx.page)).map(brief);

      const required = [];
      const missing = [];
      for (const [route, fs] of Object.entries(perForm)) {
        for (const f of fs) {
          if (!f.required) continue;
          required.push(`${route}:"${f.label}"`);
          if (!f.star) missing.push(`${route}:"${f.label}"`);
        }
      }
      const metrics = { perForm, requiredCount: required.length, missingStar: missing };
      return missing.length === 0
        ? { status: 'PASS', evidence: `All ${required.length} required fields carry "*" on their label`, metrics }
        : {
            status: 'FAIL',
            evidence: `${missing.length}/${required.length} required fields have no "*" on the label: ${missing.join(', ')}`,
            metrics,
          };
    },
  },

  {
    id: 'GUI-IA02-02',
    aspect: 'IA-02',
    screens: 'Đăng ký, Đăng nhập, Quên MK',
    title: 'Field Email dùng type="email" và chặn định dạng sai ("abc")',
    task1Status: 'Failed',
    platformSensitive: true,
    async run(ctx) {
      const forms = {
        '/register': { emailRe: /email/i, others: [[/họ tên/i, 'XP Tester'], [/mật khẩu/i, 'abc']] },
        '/login': { emailRe: /email|username/i, others: [[/mật khẩu/i, 'wrong-pw-xp']] },
        '/forgot-password': { emailRe: /email/i, others: [] },
      };
      const perForm = {};
      for (const [route, cfg] of Object.entries(forms)) {
        await ctx.goto(route);
        const fields = await scan(ctx.page);
        const email = find(fields, cfg.emailRe, 0);
        for (const [re, value] of cfg.others) {
          const f = fields.find((x) => re.test(x.label) && x.idx !== email.idx);
          if (f) await at(ctx.page, f).fill(value);
        }
        await at(ctx.page, email).fill('abc');
        const state = await validity(ctx.page, email);
        const dialogsBefore = ctx.dialogs.length;
        const urlBefore = ctx.page.url();
        const btn = await submitButton(ctx.page);
        await btn.click();
        await ctx.page.waitForTimeout(1800);
        const err = await pageError(ctx.page);
        const newDialogs = ctx.dialogs.slice(dialogsBefore).map((d) => d.message);
        const stepChanged = (await ctx.page.locator('div[class*="bg-green-100"]').count()) > 0;
        const urlChanged = ctx.page.url() !== urlBefore;
        const appReacted = Boolean(err) || newDialogs.length > 0 || stepChanged || urlChanged;
        perForm[route] = {
          label: email.label,
          typeAttr: email.type,
          validationMessage: state ? state.validationMessage : null,
          typeMismatch: state ? state.typeMismatch : null,
          formValidWithAbc: state ? state.formValid : null,
          willValidate: state ? state.willValidate : null,
          appReacted,
          appReaction: err
            ? `in-page: ${err.text}`
            : newDialogs.length
              ? `alert(): ${newDialogs.join(' | ')}`
              : stepChanged
                ? 'advanced to step 2'
                : urlChanged
                  ? `navigated to ${ctx.page.url()}`
                  : 'none — engine blocked the submit',
        };
      }
      const metrics = { perForm, ...(await engineLocale(ctx.page)) };
      const types = Object.fromEntries(Object.entries(perForm).map(([k, v]) => [k, v.typeAttr]));
      const wrongType = Object.entries(perForm).filter(([, v]) => v.typeAttr !== 'email');
      const notBlocked = Object.entries(perForm).filter(([, v]) => v.appReacted);
      if (wrongType.length === 0 && notBlocked.length === 0) {
        return { status: 'PASS', evidence: `All 3 e-mail fields are type="email" and "abc" was blocked by the engine`, metrics };
      }
      return {
        status: 'FAIL',
        evidence:
          `Email input type = ${JSON.stringify(types)}; validationMessage for "abc" = ${JSON.stringify(Object.fromEntries(Object.entries(perForm).map(([k, v]) => [k, v.validationMessage])))}; ` +
          `handler still ran on ${notBlocked.map(([k, v]) => `${k} → ${v.appReaction}`).join(' ; ') || 'none'}`,
        metrics,
      };
    },
  },

  {
    id: 'GUI-IA02-03',
    aspect: 'IA-02',
    screens: 'Đăng nhập',
    title: 'Field Mật khẩu che ký tự khi gõ',
    task1Status: 'Failed',
    platformSensitive: true,
    async run(ctx) {
      await ctx.goto('/login');
      const fields = await scan(ctx.page);
      const pw = find(fields, /mật khẩu|password/i, 1);
      const loc = at(ctx.page, pw);
      const style = await loc.evaluate((el) => {
        const cs = getComputedStyle(el);
        return {
          webkitTextSecurity: cs.webkitTextSecurity || cs.getPropertyValue('-webkit-text-security') || 'none',
          fontFamily: cs.fontFamily,
          fontSize: cs.fontSize,
          letterSpacing: cs.letterSpacing,
        };
      });
      // Behavioural probe: a masked field renders every char as the same bullet,
      // so 60×"i" and 60×"W" occupy exactly the same width. A text field does not.
      const widths = {};
      for (const ch of ['i', 'W']) {
        await loc.fill(ch.repeat(60));
        await ctx.page.waitForTimeout(150);
        widths[ch] = await loc.evaluate((el) => ({ scrollWidth: el.scrollWidth, clientWidth: el.clientWidth }));
      }
      const glyphsRendered = widths.i.scrollWidth !== widths.W.scrollWidth;
      const masked = !glyphsRendered && (pw.type === 'password' || style.webkitTextSecurity !== 'none');
      const metrics = {
        label: pw.label,
        typeAttr: pw.type,
        ...style,
        widthOf60i: widths.i.scrollWidth,
        widthOf60W: widths.W.scrollWidth,
        clientWidth: widths.i.clientWidth,
        glyphsRendered,
      };
      return masked
        ? {
            status: 'PASS',
            evidence: `Login password field type="${pw.type}", -webkit-text-security="${style.webkitTextSecurity}"; 60×i and 60×W render the same width (${widths.i.scrollWidth}px) → characters masked`,
            metrics,
          }
        : {
            status: 'FAIL',
            evidence: `Login password field type="${pw.type}" renders real glyphs: 60×i = ${widths.i.scrollWidth}px vs 60×W = ${widths.W.scrollWidth}px (a masked field is equal) → password visible on screen`,
            metrics,
          };
    },
  },

  {
    id: 'GUI-IA02-04',
    aspect: 'IA-02',
    screens: 'Đăng nhập, Đăng ký, Quên MK, Hồ sơ',
    title: 'Lỗi form hiển thị trong trang, phía TRÊN nút submit (không alert native)',
    task1Status: 'Failed',
    platformSensitive: false,
    async run(ctx) {
      const perForm = {};
      const record = async (route, dialogsBefore) => {
        const err = await pageError(ctx.page);
        const dialogs = ctx.dialogs.slice(dialogsBefore).map((d) => d.message);
        const btnY = await submitY(ctx.page);
        perForm[route] = {
          mechanism: dialogs.length ? 'native alert()' : err ? 'in-page' : 'no error shown',
          errorText: dialogs.length ? dialogs.join(' | ') : err ? err.text : null,
          errorY: err ? err.y : null,
          submitY: btnY,
          aboveSubmit: err && err.y !== null && btnY !== null ? err.y < btnY : false,
        };
      };

      // 1) /login — wrong password
      await ctx.goto('/login');
      let fields = await scan(ctx.page);
      await at(ctx.page, find(fields, /email|username/i, 0)).fill(ctx.USER.email);
      await at(ctx.page, find(fields, /mật khẩu/i, 1)).fill('definitely-wrong-xp');
      let dbefore = ctx.dialogs.length;
      await (await submitButton(ctx.page)).click();
      await ctx.page.waitForTimeout(2000);
      await record('/login', dbefore);

      // 2) /register — password rejected by the app-level regex
      await ctx.goto('/register');
      fields = await scan(ctx.page);
      await at(ctx.page, find(fields, /họ tên/i, 0)).fill('XP Tester');
      await at(ctx.page, find(fields, /email/i, 1)).fill(uniqEmail());
      await at(ctx.page, find(fields, /mật khẩu/i, 2)).fill('abc');
      dbefore = ctx.dialogs.length;
      await (await submitButton(ctx.page)).click();
      await ctx.page.waitForTimeout(1400);
      await record('/register', dbefore);

      // 3) /forgot-password — unknown e-mail
      await ctx.goto('/forgot-password');
      fields = await scan(ctx.page);
      await at(ctx.page, fields[0]).fill(`nobody-${Date.now()}@t.local`);
      dbefore = ctx.dialogs.length;
      await (await submitButton(ctx.page)).click();
      await ctx.page.waitForTimeout(2200);
      await record('/forgot-password', dbefore);

      // 4) /profile — invalid phone
      await openProfile(ctx);
      fields = await scan(ctx.page);
      const phone = find(fields, /số điện thoại/i);
      if (phone) await at(ctx.page, phone).fill('abc');
      dbefore = ctx.dialogs.length;
      await (await submitButton(ctx.page)).click();
      await ctx.page.waitForTimeout(2000);
      await record('/profile', dbefore);

      const bad = Object.entries(perForm).filter(([, v]) => v.mechanism !== 'in-page' || v.aboveSubmit !== true);
      const metrics = { perForm };
      return bad.length === 0
        ? { status: 'PASS', evidence: 'All 4 forms render in-page errors positioned above the submit button', metrics }
        : {
            status: 'FAIL',
            evidence: bad
              .map(([route, v]) =>
                v.mechanism === 'native alert()'
                  ? `${route} uses native alert() ("${v.errorText}")`
                  : v.mechanism === 'in-page'
                    ? `${route} in-page error is BELOW the submit button (errY=${v.errorY}, btnY=${v.submitY}): "${v.errorText}"`
                    : `${route}: ${v.mechanism}`)
              .join(' ; '),
            metrics,
          };
    },
  },

  {
    id: 'GUI-IA02-05',
    aspect: 'IA-02',
    screens: 'Quên mật khẩu',
    title: 'Luồng 2 bước có Step Indicator rõ ràng ("Bước 1/2", "Bước 2/2")',
    task1Status: 'Failed',
    platformSensitive: false,
    async run(ctx) {
      const indicator = (t) => /bước\s*\d|step\s*\d|\b\d\s*\/\s*2\b/i.test(t);
      const stepper = () =>
        ctx.page.evaluate(() => ({
          ariaCurrent: document.querySelectorAll('[aria-current]').length,
          olLists: document.querySelectorAll('ol').length,
          progress: document.querySelectorAll('progress, [role="progressbar"]').length,
        }));

      await ctx.goto('/forgot-password');
      const step1Text = await bodyText(ctx.page);
      const step1Stepper = await stepper();
      const heading = norm(await ctx.page.locator('h2').first().innerText().catch(() => ''));

      const { otpMessage } = await forgotToStep2(ctx, ctx.USER.email);
      const step2Text = await bodyText(ctx.page);
      const step2Stepper = await stepper();

      const metrics = {
        heading,
        step1Indicator: indicator(step1Text),
        step2Indicator: indicator(step2Text),
        step1Text: step1Text.slice(0, 300),
        step2Text: step2Text.slice(0, 300),
        step2OtpMessage: otpMessage,
        step1Stepper,
        step2Stepper,
      };
      return metrics.step1Indicator && metrics.step2Indicator
        ? { status: 'PASS', evidence: `Step indicator present on both steps (step 2 shows "${step2Text.slice(0, 90)}")`, metrics }
        : {
            status: 'FAIL',
            evidence: `No step indicator: step 1 body "${step1Text.slice(0, 70)}" and step 2 body "${step2Text.slice(0, 70)}" contain no "Bước n/2"; [aria-current]=${step1Stepper.ariaCurrent}/${step2Stepper.ariaCurrent}, <ol>=${step1Stepper.olLists}/${step2Stepper.olLists}`,
            metrics,
          };
    },
  },

  {
    id: 'GUI-IA02-06',
    aspect: 'IA-02',
    screens: 'Hồ sơ',
    title: 'Field SĐT chấp nhận số VN 10 số bắt đầu bằng 0',
    task1Status: 'Failed',
    platformSensitive: false,
    async run(ctx) {
      await openProfile(ctx);
      const fields = await scan(ctx.page);
      const phone = find(fields, /số điện thoại/i);
      if (!phone) {
        return {
          status: 'BLOCKED',
          evidence: 'No "Số điện thoại" field found on /profile',
          metrics: { labels: fields.map((f) => f.label) },
        };
      }
      const results = {};
      for (const value of ['0912345678', 'abc', '123']) {
        await at(ctx.page, phone).fill(value);
        const state = await validity(ctx.page, phone);
        const dbefore = ctx.dialogs.length;
        await (await submitButton(ctx.page)).click();
        await ctx.page.waitForTimeout(1800);
        const dialogs = ctx.dialogs.slice(dbefore).map((d) => d.message);
        const err = await pageError(ctx.page);
        const feedback = dialogs.join(' | ') || (err ? err.text : '(no feedback)');
        results[value] = {
          nativeValidationMessage: state ? state.validationMessage : null,
          nativePatternMismatch: state ? state.patternMismatch : null,
          via: dialogs.length ? 'native alert()' : err ? 'in-page' : 'none',
          feedback,
          accepted: /thành công/i.test(feedback),
        };
      }
      const metrics = {
        typeAttr: phone.type,
        patternAttr: phone.patternAttr,
        placeholder: phone.placeholder,
        appRegex: '/^[1-9][0-9]{8,9}$/ (Profile.jsx:44)',
        results,
      };
      const validOk = results['0912345678'].accepted;
      const invalidBlocked = !results.abc.accepted && !results['123'].accepted;
      return validOk && invalidBlocked
        ? {
            status: 'PASS',
            evidence: `"0912345678" accepted → "${results['0912345678'].feedback}"; "abc" → "${results.abc.feedback}", "123" → "${results['123'].feedback}"`,
            metrics,
          }
        : {
            status: 'FAIL',
            evidence: `Valid VN number "0912345678" rejected → "${results['0912345678'].feedback}" although the placeholder promises "${phone.placeholder}"; "abc" → "${results.abc.feedback}", "123" → "${results['123'].feedback}"`,
            metrics,
          };
    },
  },

  {
    id: 'GUI-IA02-07',
    aspect: 'IA-02',
    screens: 'Đăng ký, Quên MK',
    title: 'Validate mật khẩu khớp hint — "Abcdef1!" phải được chấp nhận',
    task1Status: 'Failed',
    platformSensitive: false,
    async run(ctx) {
      const registerWith = async (email, password) => {
        await ctx.goto('/register');
        const fields = await scan(ctx.page);
        await at(ctx.page, find(fields, /họ tên/i, 0)).fill('XP Tester');
        await at(ctx.page, find(fields, /email/i, 1)).fill(email);
        await at(ctx.page, find(fields, /mật khẩu/i, 2)).fill(password);
        const hint = norm(await ctx.page.locator('form p').first().innerText().catch(() => ''));
        await (await submitButton(ctx.page)).click();
        await ctx.page.waitForTimeout(2000);
        const err = await pageError(ctx.page);
        const path = new URL(ctx.page.url()).pathname;
        return { hint, error: err ? err.text : null, path, accepted: !err && path === '/login' };
      };

      // (a) the password the on-screen hint promises
      const hintTry = await registerWith(uniqEmail(), HINT_PW);
      // (b) a throwaway account whose password satisfies the *actual* regex, so
      //     the Quên-MK probe below can never touch the seeded fixture user.
      const throwaway = uniqEmail();
      const regexTry = await registerWith(throwaway, REGEX_OK_PW);

      // (c) /forgot-password step 2 with the hint password
      const forgot = { accepted: null, feedback: null, otpUsed: null };
      if (regexTry.accepted) {
        const { fields: f2, otpMessage } = await forgotToStep2(ctx, throwaway);
        const code = (otpMessage.match(/(\d{3,})/) || [, ''])[1];
        forgot.otpUsed = code;
        await at(ctx.page, find(f2, /otp/i, 0)).fill(code);
        await at(ctx.page, find(f2, /mật khẩu mới/i, 1)).fill(HINT_PW);
        const dbefore = ctx.dialogs.length;
        await (await submitButton(ctx.page)).click();
        await ctx.page.waitForTimeout(2000);
        const dialogs = ctx.dialogs.slice(dbefore).map((d) => d.message);
        const err = await pageError(ctx.page);
        forgot.feedback = dialogs.join(' | ') || (err ? err.text : '(no feedback)');
        forgot.accepted = /thành công/i.test(forgot.feedback);
      }

      const metrics = {
        appRegex: '/^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*\\s)[A-Za-z\\d\\s]{8,}$/ (Register.jsx:16, ForgotPassword.jsx:27)',
        hintText: hintTry.hint,
        registerWithHintPassword: { password: HINT_PW, ...hintTry },
        registerWithWhitespacePassword: { password: REGEX_OK_PW, email: throwaway, ...regexTry },
        forgotPasswordWithHintPassword: { password: HINT_PW, ...forgot },
      };
      return hintTry.accepted && forgot.accepted !== false
        ? {
            status: 'PASS',
            evidence: `"${HINT_PW}" accepted on /register (→ ${hintTry.path}) and on /forgot-password ("${forgot.feedback}")`,
            metrics,
          }
        : {
            status: 'FAIL',
            evidence: `Hint says "${hintTry.hint}" but "${HINT_PW}" is rejected on /register: "${hintTry.error}"; on /forgot-password: "${forgot.feedback}". A password containing a SPACE ("${REGEX_OK_PW}") is accepted (${regexTry.accepted}) → the regex demands whitespace and bans special characters`,
            metrics,
          };
    },
  },

  {
    id: 'GUI-IA02-08',
    aspect: 'IA-02',
    screens: 'Quên mật khẩu',
    title: 'Field OTP giới hạn đúng 4 chữ số như nhãn',
    task1Status: 'Failed',
    platformSensitive: true,
    async run(ctx) {
      const { fields } = await forgotToStep2(ctx, ctx.USER.email);
      const otp = find(fields, /otp/i, 0);
      if (!otp) {
        return { status: 'BLOCKED', evidence: 'OTP field not reachable on step 2', metrics: { labels: fields.map((f) => f.label) } };
      }
      await retype(ctx.page, otp, '123456abcd');
      const typed = await validity(ctx.page, otp);
      // Submit with a password that passes the app regex so the request really
      // reaches the API. The OTP is deliberately wrong → nothing gets reset.
      const pw = find(fields, /mật khẩu mới/i, 1);
      if (pw) await at(ctx.page, pw).fill(REGEX_OK_PW);
      const dbefore = ctx.dialogs.length;
      await (await submitButton(ctx.page)).click();
      await ctx.page.waitForTimeout(2200);
      const dialogs = ctx.dialogs.slice(dbefore).map((d) => d.message);

      const metrics = {
        label: otp.label,
        typeAttr: otp.type,
        maxlengthAttr: otp.maxlengthAttr,
        maxLengthProp: typed ? typed.maxLengthProp : null,
        patternAttr: otp.patternAttr,
        inputmodeAttr: otp.inputmodeAttr,
        keystrokes: '123456abcd',
        acceptedValue: typed ? typed.value : null,
        acceptedLength: typed ? typed.valueLength : null,
        validationMessage: typed ? typed.validationMessage : null,
        patternMismatch: typed ? typed.patternMismatch : null,
        tooLong: typed ? typed.tooLong : null,
        formValid: typed ? typed.formValid : null,
        submitFeedback: dialogs.join(' | ') || '(no dialog — submit blocked by the engine)',
      };
      const limited = typed && typed.valueLength <= 4 && /^\d*$/.test(typed.value);
      return limited
        ? {
            status: 'PASS',
            evidence: `OTP field kept only "${typed.value}" (${typed.valueLength} digits) out of "123456abcd"; maxlength=${otp.maxlengthAttr}, pattern=${otp.patternAttr}`,
            metrics,
          }
        : {
            status: 'FAIL',
            evidence: `Label says "${otp.label}" but the field kept "${typed.value}" (length ${typed.valueLength}, letters included); maxlength=${otp.maxlengthAttr}, pattern=${otp.patternAttr}, validationMessage="${typed.validationMessage}" → value reached the API: "${metrics.submitFeedback}"`,
            metrics,
          };
    },
  },

  {
    id: 'GUI-IA02-09',
    aspect: 'IA-02',
    screens: 'Chi tiết SP',
    title: 'Input Số lượng có ràng buộc min/max, không cho giá trị vô lý',
    task1Status: 'Failed',
    platformSensitive: true,
    async run(ctx) {
      await ctx.goto('/product/1');
      await ctx.page.waitForSelector('input[type="number"]', { timeout: 15000 });
      const fields = await scan(ctx.page, 'main');
      const qty = find(fields, /số lượng/i, 0);
      const attrs = { type: qty.type, min: qty.minAttr, max: qty.maxAttr, step: qty.stepAttr, required: qty.required };

      const probes = {};
      for (const keystrokes of ['-1', 'abc', '']) {
        await retype(ctx.page, qty, keystrokes);
        const v = await validity(ctx.page, qty);
        probes[keystrokes === '' ? '(cleared)' : keystrokes] = {
          keystrokes,
          valueAfter: v ? v.value : null,
          validationMessage: v ? v.validationMessage : null,
          badInput: v ? v.badInput : null,
          rangeUnderflow: v ? v.rangeUnderflow : null,
          valueMissing: v ? v.valueMissing : null,
          valid: v ? v.valid : null,
        };
      }

      // Push the nonsense quantity all the way into the cart (2 clicks — the
      // first click on ProductDetail.jsx is swallowed by a known SUT bug).
      await retype(ctx.page, qty, '-1');
      const addBtn = ctx.page.getByRole('button', { name: /Thêm vào giỏ hàng/ });
      await addBtn.click();
      await ctx.page.waitForTimeout(400);
      await addBtn.click();
      await ctx.page.waitForTimeout(600);
      await ctx.page.getByRole('link', { name: 'Giỏ hàng', exact: true }).click();
      await ctx.page.waitForTimeout(1000);
      const rows = await ctx.page.locator('tbody tr').count();
      const cartQty = rows ? norm(await ctx.page.locator('tbody tr').first().locator('td').nth(2).innerText()) : null;
      const cartLine = rows
        ? norm(await ctx.page.locator('tbody tr').first().innerText())
        : (await bodyText(ctx.page)).slice(0, 140);

      const metrics = { attrs, probes, cartRows: rows, cartQuantityCell: cartQty, cartLine };
      const constrained = attrs.min !== null && Number(attrs.min) >= 1;
      const cartSane = rows === 0 || (cartQty !== null && Number(cartQty) >= 1);
      return constrained && cartSane
        ? {
            status: 'PASS',
            evidence: `Quantity input min="${attrs.min}" max="${attrs.max}"; cart shows quantity "${cartQty}"`,
            metrics,
          }
        : {
            status: 'FAIL',
            evidence: `Quantity input has min=${attrs.min}, max=${attrs.max} (no lower bound); typing "-1" leaves value "${probes['-1'].valueAfter}" (rangeUnderflow=${probes['-1'].rangeUnderflow}, validationMessage="${probes['-1'].validationMessage}"), typing "abc" leaves "${probes.abc.valueAfter}" (badInput=${probes.abc.badInput}); cart accepted quantity "${cartQty}" — row "${cartLine}"`,
            metrics,
          };
    },
  },

  {
    id: 'GUI-IA02-10',
    aspect: 'IA-02',
    screens: 'Thanh toán',
    title: 'Tổng tiền thanh toán là giá trị chỉ đọc, không sửa được',
    task1Status: 'Failed',
    platformSensitive: false,
    async run(ctx) {
      const posted = [];
      ctx.page.on('request', (req) => {
        if (req.url().includes('/api/checkout')) {
          posted.push({ method: req.method(), body: (req.postData() || '').slice(0, 300) });
        }
      });

      await openCheckout(ctx);
      const total = ctx.page.locator('input[type="number"]').first();
      const shape = await total.evaluate((el) => ({
        tag: el.tagName.toLowerCase(),
        type: el.getAttribute('type'),
        readOnly: el.readOnly,
        disabled: el.disabled,
        ariaReadonly: el.getAttribute('aria-readonly'),
        value: el.value,
      }));

      let typeError = null;
      try {
        await total.click({ timeout: 5000 });
        await total.evaluate((el) => {
          el.focus();
          el.select();
        });
        // Type over the selection (no Backspace first: clearing a controlled
        // number input makes React write back "0" and the digits get appended).
        await ctx.page.keyboard.type('1000', { delay: 40 });
        await ctx.page.waitForTimeout(400);
      } catch (e) {
        typeError = e.message.split('\n')[0].slice(0, 120);
      }
      const afterTyping = await total.inputValue();
      const summaryLine = norm(await ctx.page.locator('span[class*="font-bold"]').last().innerText().catch(() => ''));

      await ctx.page.getByRole('button', { name: /Xác Nhận Thanh Toán/ }).click();
      await ctx.page.waitForTimeout(3000);
      const banner = norm(await ctx.page.locator('h2').first().innerText().catch(() => ''));

      const metrics = {
        totalField: shape,
        valueAfterTyping1000: afterTyping,
        typeError,
        summaryLine,
        checkoutRequests: posted,
        resultBanner: banner,
        dialogs: ctx.dialogs.map((d) => d.message),
      };
      const editable = shape.tag === 'input' && !shape.readOnly && !shape.disabled && afterTyping === '1000';
      const tampered = posted.some((p) => /"total_amount":\s*1000(\D|$)/.test(p.body));
      return !editable && !tampered
        ? {
            status: 'PASS',
            evidence: `Total is not user-editable (tag=${shape.tag}, type=${shape.type}, readOnly=${shape.readOnly}, disabled=${shape.disabled}); POST body: ${posted.map((p) => p.body).join(' ') || '(none)'}`,
            metrics,
          }
        : {
            status: 'FAIL',
            evidence: `"Tổng tiền thanh toán" is an editable <input type="${shape.type}"> (readOnly=${shape.readOnly}, disabled=${shape.disabled}): value ${shape.value} → "${afterTyping}", summary "${summaryLine}", and POST /api/checkout carried ${posted.map((p) => p.body).join(' ') || '(no request captured)'}`,
            metrics,
          };
    },
  },

  {
    id: 'GUI-IA02-11',
    aspect: 'IA-02',
    screens: 'Thanh toán',
    title: 'Mã giảm giá chuẩn hoá hoa/thường ("save10" xử lý như "SAVE10")',
    task1Status: 'Passed',
    platformSensitive: false,
    async run(ctx) {
      await openCheckout(ctx);
      const coupon = ctx.page.locator('input[placeholder*="giảm giá"]').first();
      const apply = ctx.page.getByRole('button', { name: 'Áp dụng', exact: true });
      const textTransform = await ctx.cssOf(coupon, 'textTransform');

      const attempt = async (code) => {
        await coupon.fill('');
        await ctx.page.waitForTimeout(200);
        await coupon.fill(code);
        await ctx.page.waitForTimeout(200);
        await apply.click();
        await ctx.page.waitForTimeout(2200);
        const ok = ctx.page.locator('div[class*="text-green-700"]');
        const bad = ctx.page.locator('p[class*="text-red-600"]');
        const success = (await ok.count()) > 0 ? norm(await ok.first().innerText()) : null;
        const error = (await bad.count()) > 0 ? norm(await bad.first().innerText()) : null;
        return { typedValue: await coupon.inputValue(), success, error, applied: Boolean(success) };
      };

      const lower = await attempt('save10');
      const upper = await attempt('SAVE10');
      const metrics = {
        cssTextTransform: textTransform,
        codeSentToApi: 'couponCode.trim().toUpperCase() (Checkout.jsx:30)',
        lowerCase: lower,
        upperCase: upper,
      };
      const same =
        lower.applied === upper.applied &&
        norm(lower.success || lower.error || '') === norm(upper.success || upper.error || '');
      return same && lower.applied
        ? {
            status: 'PASS',
            evidence: `"save10" and "SAVE10" behave identically → "${norm((lower.success || '').split('\n')[0])}"; the input is rendered with text-transform: ${textTransform} while its value stays "${lower.typedValue}"`,
            metrics,
          }
        : {
            status: 'FAIL',
            evidence: `Case handling differs — "save10" → ${lower.applied ? `applied "${lower.success}"` : `error "${lower.error}"`} vs "SAVE10" → ${upper.applied ? `applied "${upper.success}"` : `error "${upper.error}"`}`,
            metrics,
          };
    },
  },

  {
    id: 'GUI-IA02-12',
    aspect: 'IA-02',
    screens: 'Hồ sơ',
    title: 'Field Email hồ sơ disabled rõ ràng (nhãn "(Không đổi)", nền xám)',
    task1Status: 'Passed',
    platformSensitive: false,
    async run(ctx) {
      await openProfile(ctx);
      const fields = await scan(ctx.page);
      const email = find(fields, /email/i, 0);
      const loc = at(ctx.page, email);
      const before = await loc.inputValue();
      const style = await loc.evaluate((el) => {
        const cs = getComputedStyle(el);
        return {
          backgroundColor: cs.backgroundColor,
          color: cs.color,
          opacity: cs.opacity,
          cursor: cs.cursor,
          pointerEvents: cs.pointerEvents,
        };
      });
      let clickError = null;
      try {
        await loc.click({ timeout: 2500, force: true });
      } catch (e) {
        clickError = e.message.split('\n')[0].slice(0, 90);
      }
      const focusable = await loc.evaluate((el) => {
        el.focus();
        return document.activeElement === el;
      });
      await ctx.page.keyboard.type('hacked@evil.local', { delay: 10 }).catch(() => {});
      await ctx.page.waitForTimeout(250);
      const after = await loc.inputValue();

      const metrics = {
        label: email.label,
        disabledProp: email.disabled,
        readOnlyProp: email.readOnly,
        valueBefore: before,
        valueAfterTyping: after,
        focusable,
        clickError,
        ...style,
      };
      const labelOk = /\(Không đổi\)/i.test(email.label);
      return email.disabled && before === after && labelOk
        ? {
            status: 'PASS',
            evidence: `Email field disabled=${email.disabled}, label "${email.label}", background ${style.backgroundColor}; typing left the value at "${after}" (focusable=${focusable})`,
            metrics,
          }
        : {
            status: 'FAIL',
            evidence: `Email field disabled=${email.disabled}, label "${email.label}", value "${before}" → "${after}", background ${style.backgroundColor}`,
            metrics,
          };
    },
  },

  {
    id: 'GUI-IA02-13',
    aspect: 'IA-02',
    screens: 'Đăng ký',
    title: 'Form đăng ký có field "Xác nhận mật khẩu" và kiểm tra khớp',
    task1Status: 'Failed',
    platformSensitive: false,
    async run(ctx) {
      await ctx.goto('/register');
      const fields = await scan(ctx.page);
      const labels = fields.map((f) => `${f.label} [${f.tag}${f.type ? `:${f.type}` : ''}]`);
      const confirm = fields.find((f) => /xác nhận|nhập lại|confirm|repeat/i.test(f.label));
      const passwordFields = fields.filter((f) => f.type === 'password');
      const metrics = {
        fields: labels,
        passwordFieldCount: passwordFields.length,
        confirmFieldFound: Boolean(confirm),
      };

      if (!confirm) {
        return {
          status: 'FAIL',
          evidence: `No "Xác nhận mật khẩu" field on /register — the form only has: ${labels.join(', ')} (${passwordFields.length} password input)`,
          metrics,
        };
      }
      await at(ctx.page, find(fields, /họ tên/i, 0)).fill('XP Tester');
      await at(ctx.page, find(fields, /email/i, 1)).fill(uniqEmail());
      const pw = fields.find((f) => f.type === 'password' && f.idx !== confirm.idx) || fields[2];
      await at(ctx.page, pw).fill(REGEX_OK_PW);
      await at(ctx.page, confirm).fill(`${REGEX_OK_PW}X`);
      const dbefore = ctx.dialogs.length;
      await (await submitButton(ctx.page)).click();
      await ctx.page.waitForTimeout(2000);
      const err = await pageError(ctx.page);
      const dialogs = ctx.dialogs.slice(dbefore).map((d) => d.message);
      metrics.mismatchFeedback = err ? err.text : dialogs.join(' | ') || null;
      metrics.errorY = err ? err.y : null;
      metrics.submitY = await submitY(ctx.page);
      metrics.pathAfterSubmit = new URL(ctx.page.url()).pathname;
      const blocked = Boolean(metrics.mismatchFeedback) && metrics.pathAfterSubmit !== '/login';
      return blocked
        ? {
            status: 'PASS',
            evidence: `Confirm field "${confirm.label}" present; mismatch rejected with "${metrics.mismatchFeedback}" (errY=${metrics.errorY}, btnY=${metrics.submitY})`,
            metrics,
          }
        : {
            status: 'FAIL',
            evidence: `Confirm field "${confirm.label}" present but a mismatch was accepted (path ${metrics.pathAfterSubmit}, feedback: ${metrics.mismatchFeedback})`,
            metrics,
          };
    },
  },

  {
    id: 'GUI-IA02-14',
    aspect: 'IA-02',
    screens: 'Đăng ký, Đăng nhập, Quên MK',
    title: 'Thông báo "bắt buộc nhập" nhất quán tiếng Việt (hiện dùng tooltip native)',
    task1Status: 'Failed',
    platformSensitive: true,
    async run(ctx) {
      const perForm = {};
      for (const route of ['/register', '/login', '/forgot-password']) {
        await ctx.goto(route);
        const fields = await scan(ctx.page);
        const firstRequired = fields.find((f) => f.required) || fields[0];
        const dbefore = ctx.dialogs.length;
        const urlBefore = ctx.page.url();
        await (await submitButton(ctx.page)).click(); // every field left empty
        await ctx.page.waitForTimeout(1400);
        const state = await validity(ctx.page, firstRequired);
        const err = await pageError(ctx.page);
        const dialogs = ctx.dialogs.slice(dbefore).map((d) => d.message);
        const focusAfterSubmit = await ctx.page.evaluate(() => {
          const el = document.activeElement;
          if (!el || el === document.body) return 'body (nothing focused)';
          return `${el.tagName.toLowerCase()}${el.getAttribute('data-xp') !== null ? `[data-xp=${el.getAttribute('data-xp')}]` : ''}`;
        });
        perForm[route] = {
          field: firstRequired.label,
          requiredAttr: firstRequired.required,
          validationMessage: state ? state.validationMessage : null,
          valueMissing: state ? state.valueMissing : null,
          willValidate: state ? state.willValidate : null,
          formValid: state ? state.formValid : null,
          mechanism: dialogs.length
            ? 'native alert()'
            : err
              ? 'in-page banner'
              : 'native constraint-validation bubble',
          inPageError: err ? err.text : null,
          appDialogs: dialogs,
          submitBlocked: ctx.page.url() === urlBefore && !err && dialogs.length === 0,
          focusAfterSubmit,
          isVietnamese: isVietnamese(state ? state.validationMessage : ''),
        };
      }
      const metrics = { perForm, ...(await engineLocale(ctx.page)) };
      const nonVi = Object.entries(perForm).filter(([, v]) => !v.isVietnamese);
      return nonVi.length === 0
        ? {
            status: 'PASS',
            evidence: `Required messages are Vietnamese on all 3 forms: ${Object.values(perForm).map((v) => `"${v.validationMessage}"`).join(', ')}`,
            metrics,
          }
        : {
            status: 'FAIL',
            evidence: `Required feedback is the engine's own bubble, not Vietnamese app text: ${nonVi
              .map(([r, v]) => `${r} "${v.field}" → "${v.validationMessage}"`)
              .join(' ; ')} (navigator.language=${metrics.navigatorLanguage}, <html lang>=${metrics.documentLang})`,
            metrics,
          };
    },
  },

  {
    id: 'GUI-GAP-04',
    aspect: 'IA-02',
    screens: 'Đăng nhập, Đăng ký, Quên MK, Hồ sơ',
    title: 'Mọi label gắn với input qua htmlFor/id — click nhãn focus vào ô nhập',
    task1Status: 'Failed',
    platformSensitive: false,
    async run(ctx) {
      const perForm = {};
      const inspect = async (route) => {
        const fields = await scan(ctx.page);
        const labelInfo = await ctx.page.evaluate(() =>
          Array.from(document.querySelectorAll('form label')).map((l) => ({
            text: (l.textContent || '').replace(/\s+/g, ' ').trim(),
            htmlFor: l.getAttribute('for'),
            wrapsControl: Boolean(l.querySelector('input, textarea, select')),
          })));
        const labels = ctx.page.locator('form label');
        const clicks = [];
        const n = Math.min(await labels.count(), 4);
        for (let i = 0; i < n; i += 1) {
          await ctx.page.evaluate(() => document.activeElement && document.activeElement.blur());
          await labels.nth(i).click({ timeout: 4000 }).catch(() => {});
          await ctx.page.waitForTimeout(150);
          const focusAfterClick = await ctx.page.evaluate(() => {
            const el = document.activeElement;
            if (!el || el === document.body) return 'body (nothing focused)';
            return `${el.tagName.toLowerCase()}${el.getAttribute('data-xp') !== null ? `[data-xp=${el.getAttribute('data-xp')}]` : ''}`;
          });
          clicks.push({ label: labelInfo[i] ? labelInfo[i].text : `#${i}`, focusAfterClick });
        }
        perForm[route] = {
          labelCount: labelInfo.length,
          labelsWithFor: labelInfo.filter((l) => l.htmlFor).length,
          labelsWrappingControl: labelInfo.filter((l) => l.wrapsControl).length,
          controlCount: fields.length,
          controlsWithId: fields.filter((f) => f.id).length,
          labels: labelInfo,
          clicks,
        };
      };

      for (const route of ['/login', '/register', '/forgot-password']) {
        await ctx.goto(route);
        await inspect(route);
      }
      await openProfile(ctx);
      await inspect('/profile');

      const totals = Object.values(perForm).reduce(
        (a, v) => ({
          labels: a.labels + v.labelCount,
          withFor: a.withFor + v.labelsWithFor,
          wrapping: a.wrapping + v.labelsWrappingControl,
          ids: a.ids + v.controlsWithId,
          controls: a.controls + v.controlCount,
          focusHits: a.focusHits + v.clicks.filter((c) => /data-xp=/.test(c.focusAfterClick)).length,
          clicks: a.clicks + v.clicks.length,
        }),
        { labels: 0, withFor: 0, wrapping: 0, ids: 0, controls: 0, focusHits: 0, clicks: 0 },
      );
      const metrics = { perForm, totals };
      const sample = perForm['/login'].clicks[1] || perForm['/login'].clicks[0];
      return totals.withFor === totals.labels && totals.focusHits === totals.clicks
        ? {
            status: 'PASS',
            evidence: `All ${totals.labels} labels use htmlFor and every label click focused its control (${totals.focusHits}/${totals.clicks})`,
            metrics,
          }
        : {
            status: 'FAIL',
            evidence: `${totals.withFor}/${totals.labels} labels have htmlFor and ${totals.wrapping} wrap their control (${totals.ids}/${totals.controls} controls have an id); clicking a label focused the input only ${totals.focusHits}/${totals.clicks} times — e.g. /login "${sample ? sample.label : ''}" → ${sample ? sample.focusAfterClick : 'n/a'}`,
            metrics,
          };
    },
  },
];
