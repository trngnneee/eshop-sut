// Builds the human-readable Task 3 deliverables from results/raw/*.json:
//
//   ../results-matrix.md   — 66 checklist items × N platforms, Pass/Fail/Blocked
//   ../divergences.md      — every item whose STATUS or observed VALUES differ per platform
//
//   node scripts/build-matrix.js

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '..', '..');
const RAW = path.join(ROOT, 'results', 'raw');

const ICON = { PASS: '✅ Pass', FAIL: '❌ Fail', BLOCKED: '⚠️ Blocked', ERROR: '💥 Error' };

const files = fs
  .readdirSync(RAW)
  .filter((f) => f.endsWith('.json'))
  .sort();
if (files.length === 0) throw new Error(`No result files in ${RAW} — run \`node run-audit.js\` first.`);

const runs = files.map((f) => JSON.parse(fs.readFileSync(path.join(RAW, f), 'utf8')));
const byId = new Map();
for (const run of runs) {
  for (const r of run.results) {
    if (!byId.has(r.id)) byId.set(r.id, { meta: r, per: {} });
    byId.get(r.id).per[run.platform.key] = r;
  }
}

const platforms = runs.map((r) => r.platform);
const short = (k) => k.split('-')[0]; // P1 / P2 / P3 …

/* ------------------------------------------------------------------ matrix */

const lines = [];
lines.push('# Task 3 — Ma trận thực thi checklist trên nhiều platform');
lines.push('');
lines.push('> Sinh tự động bởi `harness/scripts/build-matrix.js` từ `results/raw/*.json`. Không sửa tay.');
lines.push('');
lines.push('## Platform đã chạy');
lines.push('');
lines.push('| # | Platform | Engine + version | OS | Device / viewport | Locale engine | Thời điểm chạy |');
lines.push('|---|---|---|---|---|---|---|');
for (const [i, p] of platforms.entries()) {
  const run = runs[i];
  const loc =
    run.results.find((r) => r.metrics && (r.metrics.resolvedLocale || r.metrics.navigatorLanguage))?.metrics || {};
  const vp = typeof p.viewport === 'object' ? `${p.viewport.width}×${p.viewport.height}` : p.viewport;
  lines.push(
    `| ${short(p.key)} | ${p.label}${p.emulated ? ' _(emulated)_' : ''} | ${p.engine} ${p.version} | ${p.os} | ${p.device} · ${vp} | ${loc.resolvedLocale || loc.navigatorLanguage || '—'} | ${run.runStamp} |`,
  );
}
lines.push('');
// Cột "Platform" là vai trò theo đề (Chrome / Firefox / Safari), không phải tên bundle
// đã chạy. Nói rõ ngay dưới bảng để ảnh bằng chứng (menu bar hiện "Playwright") không
// bị đọc là gán nhãn sai — chi tiết ở platform-matrix.md §4.
lines.push(
  '> **Cột "Platform" là vai trò theo đề, không phải tên bundle đã chạy.** Ba engine đều là browser build do Playwright quản lý, chạy headed trên máy thật: ' +
    'P1 = *Google Chrome for Testing* (Blink, vai trò "Chrome") · P2 = Firefox bundle `Nightly.app` (Gecko, vai trò "Firefox") · ' +
    'P3 = **WebKit build của Playwright, KHÔNG phải `Safari.app`** (cùng engine `AppleWebKit/605.1.15` — `Version/26.5` — nên cùng lớp render/JS/CSS/validation với Safari, nhưng vỏ ứng dụng là `Playwright.app`, ' +
    'vì vậy menu bar macOS trong ảnh cửa sổ hiện "Playwright"). Khai báo đầy đủ: [platform-matrix.md](platform-matrix.md) §4.',
);
lines.push('');

lines.push('## Tổng hợp theo platform');
lines.push('');
lines.push(`| Platform | Pass | Fail | Blocked | Error | Tổng |`);
lines.push('|---|---|---|---|---|---|');
for (const run of runs) {
  const s = run.summary;
  lines.push(
    `| ${short(run.platform.key)} — ${run.platform.label} | ${s.PASS} | ${s.FAIL} | ${s.BLOCKED} | ${s.ERROR} | ${run.results.length} |`,
  );
}
lines.push('');

// per aspect × platform
const aspects = [...new Set([...byId.values()].map((v) => v.meta.aspect))].sort();
lines.push('## Tổng hợp theo Interface Aspect');
lines.push('');
lines.push(`| Aspect | ${platforms.map((p) => `${short(p.key)} P/F/B`).join(' | ')} |`);
lines.push(`|---|${platforms.map(() => '---').join('|')}|`);
for (const a of aspects) {
  const cells = platforms.map((p) => {
    const rows = [...byId.values()].filter((v) => v.meta.aspect === a).map((v) => v.per[p.key]);
    const c = (s) => rows.filter((r) => r && r.status === s).length;
    return `${c('PASS')} / ${c('FAIL')} / ${c('BLOCKED') + c('ERROR')}`;
  });
  lines.push(`| ${a} | ${cells.join(' | ')} |`);
}
lines.push('');

/* --------------------------------------------------------------- divergence */

// Metrics that legitimately differ between two runs of the same platform: the
// throwaway account a check registered, the random OTP the SUT printed, ids and
// timings. A difference in these is NOT a platform difference, and reporting it as
// one would inflate the findings.
const NOISE_KEY = /account|email|otp|token|timestamp|orderid|orderrows|elapsed|duration|ms$/i;

function metricsDiff(entry) {
  const keys = new Set();
  for (const p of platforms) {
    const m = entry.per[p.key]?.metrics;
    if (m && typeof m === 'object') Object.keys(m).forEach((k) => keys.add(k));
  }
  const diffs = [];
  for (const k of keys) {
    const vals = platforms.map((p) => {
      const m = entry.per[p.key]?.metrics || {};
      return JSON.stringify(m[k]);
    });
    if (new Set(vals).size > 1) diffs.push({ key: k, vals });
  }
  return diffs;
}

const statusDiverged = [];
const valueDiverged = [];
const noiseOnly = [];
for (const [id, entry] of byId) {
  const statuses = platforms.map((p) => entry.per[p.key]?.status || '—');
  const all = metricsDiff(entry);
  const diffs = all.filter((d) => !NOISE_KEY.test(d.key));
  const noise = all.filter((d) => NOISE_KEY.test(d.key));
  if (new Set(statuses).size > 1) statusDiverged.push({ id, entry, statuses, diffs, noise });
  else if (diffs.length) valueDiverged.push({ id, entry, statuses, diffs, noise });
  else if (noise.length) noiseOnly.push({ id, entry, noise });
}

/* ------------------------------------------------------------- main table */

lines.push('## Ma trận chi tiết (66 item × platform)');
lines.push('');
lines.push(
  `| ID | Aspect | Task 1 (Chrome, thủ công) | ${platforms.map((p) => short(p.key)).join(' | ')} | Khác biệt giữa platform |`,
);
lines.push(`|---|---|---|${platforms.map(() => '---').join('|')}|---|`);

const order = [...byId.keys()].sort();
for (const id of order) {
  const entry = byId.get(id);
  const statuses = platforms.map((p) => ICON[entry.per[p.key]?.status] || '—');
  const sDiv = new Set(platforms.map((p) => entry.per[p.key]?.status)).size > 1;
  const vDiv = metricsDiff(entry).some((d) => !NOISE_KEY.test(d.key));
  const flag = sDiv ? '🔴 kết quả khác nhau' : vDiv ? '🟡 giá trị hiển thị khác nhau' : '—';
  lines.push(
    `| [${id}](results/raw/) | ${entry.meta.aspect} | ${entry.meta.task1Status} | ${statuses.join(' | ')} | ${flag} |`,
  );
}
lines.push('');
lines.push(
  `**Item có kết quả khác nhau giữa các platform: ${statusDiverged.length}** · **item cùng kết quả nhưng giá trị hiển thị khác nhau: ${valueDiverged.length}** · xem [divergences.md](divergences.md).`,
);
lines.push('');

lines.push('## Đối chiếu với Task 1');
lines.push('');
lines.push('| ID | Task 1 | ' + platforms.map((p) => short(p.key)).join(' | ') + ' | Ghi chú |');
lines.push(`|---|---|${platforms.map(() => '---').join('|')}|---|`);
let regressions = 0;
for (const id of order) {
  const entry = byId.get(id);
  const t1 = entry.meta.task1Status === 'Passed' ? 'PASS' : 'FAIL';
  const mine = platforms.map((p) => entry.per[p.key]?.status);
  if (mine.every((m) => m === t1)) continue;
  regressions += 1;
  lines.push(
    `| ${id} | ${entry.meta.task1Status} | ${mine.map((m) => ICON[m] || '—').join(' | ')} | ${entry.meta.title.slice(0, 90)} |`,
  );
}
lines.push('');
lines.push(`Tổng số item mà kết quả tự động khác kết luận Task 1 trên ít nhất 1 platform: **${regressions}**.`);
lines.push('');

fs.writeFileSync(path.join(ROOT, 'results-matrix.md'), `${lines.join('\n')}\n`);

/* ------------------------------------------------------------ divergences */

const d = [];
d.push('# Task 3 — Khác biệt giữa các platform');
d.push('');
d.push('> Sinh tự động từ `results/raw/*.json`. Mỗi mục dưới đây là bằng chứng cho thấy cùng một item checklist cho ra kết quả hoặc giá trị hiển thị **khác nhau** giữa các engine — đây chính là nội dung của Task 3.');
d.push('');
d.push('## A. Khác biệt về KẾT QUẢ Pass/Fail (nghiêm trọng nhất)');
d.push('');
if (statusDiverged.length === 0) d.push('_Không có item nào đổi kết quả Pass/Fail giữa các platform._');
for (const { id, entry, statuses, diffs } of statusDiverged) {
  d.push(`### ${id} — ${entry.meta.title}`);
  d.push('');
  d.push(`* Aspect: ${entry.meta.aspect} · Screen(s): ${entry.meta.screens} · Task 1: ${entry.meta.task1Status}`);
  d.push('');
  d.push('| Platform | Kết quả | Quan sát |');
  d.push('|---|---|---|');
  for (const [i, p] of platforms.entries()) {
    const r = entry.per[p.key];
    d.push(`| ${short(p.key)} ${p.label} | ${ICON[statuses[i]] || '—'} | ${(r?.evidence || '—').replace(/\|/g, '\\|')} |`);
  }
  d.push('');
  if (diffs.length) {
    d.push('Giá trị thô khác nhau:');
    d.push('');
    d.push(`| metric | ${platforms.map((p) => short(p.key)).join(' | ')} |`);
    d.push(`|---|${platforms.map(() => '---').join('|')}|`);
    for (const { key, vals } of diffs) {
      d.push(`| \`${key}\` | ${vals.map((v) => `\`${String(v).slice(0, 160).replace(/\|/g, '\\|')}\``).join(' | ')} |`);
    }
    d.push('');
  }
  const shots = platforms
    .map((p) => (entry.per[p.key]?.screenshots || []).map((s) => `[${short(p.key)}](results/${p.key}/screenshots/${s})`))
    .flat();
  if (shots.length) d.push(`Screenshot: ${shots.join(' · ')}`);
  d.push('');
}

d.push('## B. Cùng kết quả nhưng GIÁ TRỊ HIỂN THỊ khác nhau');
d.push('');
if (valueDiverged.length === 0) d.push('_Không có._');
for (const { id, entry, diffs } of valueDiverged) {
  d.push(`### ${id} — ${entry.meta.title}`);
  d.push('');
  d.push(`| metric | ${platforms.map((p) => short(p.key)).join(' | ')} |`);
  d.push(`|---|${platforms.map(() => '---').join('|')}|`);
  for (const { key, vals } of diffs) {
    d.push(`| \`${key}\` | ${vals.map((v) => `\`${String(v).slice(0, 160).replace(/\|/g, '\\|')}\``).join(' | ')} |`);
  }
  d.push('');
}

d.push('## C. Khác biệt CHỈ do dữ liệu của lần chạy — KHÔNG phải khác biệt platform');
d.push('');
d.push('Liệt kê để minh bạch: các item dưới đây có giá trị `metrics` khác nhau, nhưng mọi khoá khác nhau đều là dữ liệu sinh theo từng lần chạy (email throwaway do check tự đăng ký, mã OTP ngẫu nhiên của SUT, id đơn hàng, thời gian). Chạy lại 2 lần trên **cùng một** engine cũng cho giá trị khác nhau, nên đây không phải phát hiện cross-platform.');
d.push('');
if (noiseOnly.length === 0) d.push('_Không có._');
else {
  d.push('| ID | Khoá chỉ khác do dữ liệu chạy |');
  d.push('|---|---|');
  for (const { id, noise } of noiseOnly) d.push(`| ${id} | ${noise.map((n) => `\`${n.key}\``).join(', ')} |`);
}
d.push('');

fs.writeFileSync(path.join(ROOT, 'divergences.md'), `${d.join('\n')}\n`);

console.log(
  `Wrote results-matrix.md (${byId.size} items × ${platforms.length} platforms) and divergences.md ` +
    `(${statusDiverged.length} status divergences, ${valueDiverged.length} engine-value divergences, ` +
    `${noiseOnly.length} run-data-only differences).`,
);
