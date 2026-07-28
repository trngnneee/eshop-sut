// Evidence overlay.
//
// HW03 §6 Task 3 requires every cross-platform screenshot to show the
// browser / OS / device name next to the SUT's localhost URL, and to overlay the
// student's e-mail. Playwright's page.screenshot() captures the viewport only
// (no browser chrome), so the harness stamps that information into the page
// itself right before the shot and removes it afterwards.

export const STUDENT = {
  id: '23127438',
  name: 'Đặng Trường Nguyên',
  email: 'dtnguyen23@clc.fitus.edu.vn',
};

const OVERLAY_ID = '__hw03_xp_overlay__';

export async function stampOverlay(page, meta) {
  await page.evaluate(
    ({ id, meta, student }) => {
      document.getElementById(id)?.remove();

      const bar = document.createElement('div');
      bar.id = id;
      bar.style.cssText = [
        'position:fixed', 'top:0', 'left:0', 'right:0', 'z-index:2147483647',
        'font:12px/1.45 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif',
        'background:#111827', 'color:#f9fafb', 'padding:6px 10px',
        'box-shadow:0 2px 6px rgba(0,0,0,.45)', 'pointer-events:none',
      ].join(';');

      const row = (label, value, strong) =>
        `<span style="opacity:.6">${label}</span> ` +
        `<span style="${strong ? 'font-weight:700;color:#fbbf24' : 'color:#e5e7eb'}">${value}</span>`;

      bar.innerHTML = [
        row('PLATFORM', `${meta.platformLabel} · ${meta.engine} ${meta.version}`, true),
        row('OS', meta.os),
        row('DEVICE', meta.device),
        row('VIEWPORT', `${window.innerWidth}×${window.innerHeight} @${window.devicePixelRatio}x`),
        row('LOCALE', `${navigator.language} / ${Intl.DateTimeFormat().resolvedOptions().locale}`),
      ].join(' &nbsp;|&nbsp; ') +
        '<br>' +
        [
          row('SUT URL', location.href, true),
          row('CHECKLIST ITEM', meta.itemId, true),
          row('RESULT', meta.status),
          row('RUN', meta.timestamp),
        ].join(' &nbsp;|&nbsp; ') +
        '<br>' +
        [
          row('STUDENT', `${student.id} — ${student.name}`),
          row('EMAIL', student.email, true),
          row('HW', 'HW03-AI · Task 3 Cross-Browser / Cross-Platform'),
        ].join(' &nbsp;|&nbsp; ');

      document.documentElement.appendChild(bar);
      // Push the page down by the bar height so the stamp never hides the SUT's
      // own header (needed for the IA-03 navigation items).
      document.body.dataset.hw03PrevPadTop = document.body.style.paddingTop || '';
      document.body.style.paddingTop = `${bar.getBoundingClientRect().height}px`;
      window.scrollTo(0, 0);
    },
    { id: OVERLAY_ID, meta, student: STUDENT },
  );
}

export async function removeOverlay(page) {
  await page
    .evaluate((id) => {
      document.getElementById(id)?.remove();
      if (document.body?.dataset.hw03PrevPadTop !== undefined) {
        document.body.style.paddingTop = document.body.dataset.hw03PrevPadTop;
        delete document.body.dataset.hw03PrevPadTop;
      }
    }, OVERLAY_ID)
    .catch(() => {});
}
