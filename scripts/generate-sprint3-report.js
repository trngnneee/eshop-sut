const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const results = JSON.parse(
  fs.readFileSync(path.join(ROOT, 'test-results/results.json'), 'utf8')
);

const meta = {
  '001': { bugs: '#4, #7', note: 'Thiếu confirm-password; regex client từ chối `NewPass1!`.' },
  '002': { bugs: 'None', note: 'Timeout — automation không phát hiện phản hồi lỗi email rỗng.' },
  '003': { bugs: '#8', note: 'type=text; không chặn format email (timeout).' },
  '004': { bugs: 'None', note: 'Timeout — không phát hiện lỗi email chưa đăng ký.' },
  '005': { bugs: 'None', note: 'Timeout — OTP rỗng không có phản hồi lỗi rõ.' },
  '006': { bugs: '#6', note: 'Timeout — OTP chứa chữ cái không bị từ chối rõ.' },
  '007': { bugs: '#6', note: 'Timeout — OTP 5 số không bị từ chối rõ.' },
  '008': { bugs: '#6', note: 'Timeout — OTP 7 số không bị từ chối (spec yêu cầu 6).' },
  '009': { bugs: '#7', note: 'Timeout — OTP sai không hiển thị lỗi rõ.' },
  '010': { bugs: 'None', note: 'API từ chối OTP cross-email — đúng spec.' },
  '011': { bugs: '#4, #7', note: 'Timeout — mật khẩu rỗng; thiếu confirm field.' },
  '012': { bugs: '#7', note: 'Timeout — MK 7 ký tự không báo lỗi FR-01.' },
  '013': { bugs: '#7', note: 'Timeout — thiếu chữ hoa.' },
  '014': { bugs: '#7', note: 'Timeout — thiếu chữ thường.' },
  '015': { bugs: '#7', note: 'Timeout — thiếu chữ số.' },
  '016': { bugs: '#7', note: 'Regex yêu cầu space thay vì ký tự đặc biệt.' },
  '017': { bugs: '#4', note: 'Không có trường xác nhận mật khẩu.' },
  '018': { bugs: '#4', note: 'Không kiểm tra khớp mật khẩu.' },
  '019': { bugs: '#5', note: 'Không có Step Indicator.' },
  '020': { bugs: '#9', note: '"Quay lại" không về `/login`.' },
  '021': { bugs: 'None', note: 'Timeout — email 4 ký tự không báo lỗi độ dài.' },
  '022': { bugs: 'None', note: 'Email 5 ký tự — không báo lỗi độ dài (đúng BVA min).' },
  '023': { bugs: 'None', note: 'Email 6 ký tự — không báo lỗi độ dài (đúng BVA min+).' },
  '024': { bugs: 'None', note: 'Email 99 ký tự — không báo lỗi độ dài (đúng BVA max−).' },
  '025': { bugs: 'None', note: 'Email 100 ký tự — không báo lỗi độ dài (đúng BVA max).' },
  '026': { bugs: 'None', note: 'Timeout — email 101 ký tự không báo lỗi độ dài.' },
  '027': { bugs: '#6', note: 'Timeout — OTP BVA 5 số không bị từ chối.' },
  '028': { bugs: '#7', note: 'Reset MK 6 ký tự không redirect `/login`.' },
  '029': { bugs: '#6', note: 'Timeout — OTP BVA 7 số không bị từ chối.' },
  '030': { bugs: '#7', note: 'Timeout — MK 7 ký tự BVA không báo lỗi.' },
  '031': { bugs: '#7', note: 'Reset MK 8 ký tự (min) không thành công.' },
  '032': { bugs: '#7', note: 'Reset MK 9 ký tự (min+) không thành công.' },
  '033': { bugs: '#7', note: 'Reset MK 49 ký tự (max−) không thành công.' },
  '034': { bugs: '#7', note: 'Reset MK 50 ký tự (max) không thành công.' },
  '035': { bugs: '#7', note: 'Timeout — MK 51 ký tự không báo lỗi.' },
  '036': { bugs: '#4', note: 'Timeout — thiếu trường confirm; MK 7 ký tự.' },
  '037': { bugs: '#7', note: 'Reset confirm 8 ký tự không thành công.' },
  '038': { bugs: '#7', note: 'Reset confirm 9 ký tự không thành công.' },
  '039': { bugs: '#7', note: 'Reset confirm 49 ký tự không thành công.' },
  '040': { bugs: '#7', note: 'Reset confirm 50 ký tự không thành công.' },
  '041': { bugs: '#4', note: 'Timeout — confirm 51 ký tự; thiếu trường confirm.' },
  '042': { bugs: '#7', note: 'Cross-boundary min (MK 8 + confirm 8) — reset fail.' },
  '043': { bugs: '#7', note: 'Cross-boundary max (MK 50 + confirm 50) — reset fail.' },
  '044': { bugs: '#4', note: 'Timeout — confirm min− mismatch; thiếu trường confirm.' },
};

const rows = [];

function walkSuites(suites) {
  for (const suite of suites || []) {
    for (const spec of suite.specs || []) {
      const m = spec.title.match(/TC-FORGOT-(\d+)/);
      if (!m) continue;
      const num = m[1].padStart(3, '0');
      const id = `TC-FORGOT-${num}`;
      const n = parseInt(m[1], 10);
      const raw = spec.tests?.[0]?.results?.[0]?.status;
      const result = raw === 'passed' ? 'Pass' : 'Fail';
      rows.push({ n, id, num, result, raw });
    }
    walkSuites(suite.suites);
  }
}

walkSuites(results.suites);
rows.sort((a, b) => a.n - b.n);

const pass = rows.filter((r) => r.result === 'Pass').length;
const fail = rows.filter((r) => r.result === 'Fail').length;
const rate = Math.round((pass / rows.length) * 100);

const tableRows = rows
  .map((r) => {
    const m = meta[r.num];
    return `| [${r.id}](../test-cases/forgot/${r.id}.md) | Forgot Password | Playwright | ${r.result} | ${m.bugs} | ${m.note} |`;
  })
  .join('\n');

const report = `# Test Run - Sprint 3 (FR-03 Forgot Password)

**Ngày thực hiện**: 29/06/2026  
**Người thực hiện**: Playwright E2E (aligned spec)  
**Môi trường thử nghiệm**: Frontend \`http://localhost:5173\` · Backend \`http://localhost:3000\` · Chromium · Playwright 1.61  
**Nguồn kết quả**: \`test-results/results.json\` — \`npx playwright test tests/e2e/forgot-password.spec.js\` (44 tests)  
**Gap analysis**: [gap-analysis-FR-03.md](../test-summary/gap-analysis-FR-03.md)

## Tổng kết

| Chỉ số | Giá trị |
| :--- | :--- |
| Markdown TC (DT + BVA) | 44 |
| Supplementary TC | 4 |
| Pass | ${pass} |
| Fail | ${fail} |
| Pass rate | ${rate}% |

> **Ghi chú:** Spec E2E đã đồng bộ ID với markdown TC 001–044 (GAP-06 đã khắc phục). Nhiều case Fail do timeout 30s — SUT không hiển thị thông báo lỗi mà automation chờ.

## Kết quả chi tiết

| Test Case ID | Module | Tester | Result | Related Bug | Note |
| :--- | :--- | :--- | :--- | :--- | :--- |
${tableRows}
| [TC-FORGOT-SUP-001](../test-cases/forgot/TC-FORGOT-SUP-001.md) | Forgot Password | — | Not Run | #6 | Gap remediation — OTP 6 digits. |
| [TC-FORGOT-SUP-002](../test-cases/forgot/TC-FORGOT-SUP-002.md) | Forgot Password | — | Not Run | #10 | Gap remediation — server password validation. |
| [TC-FORGOT-SUP-003](../test-cases/forgot/TC-FORGOT-SUP-003.md) | Forgot Password | — | Not Run | #8 | Gap remediation — FR-22 email type. |
| [TC-FORGOT-SUP-004](../test-cases/forgot/TC-FORGOT-SUP-004.md) | Forgot Password | — | Not Run | None | Gap remediation — OTP one-time use. |

## Phân loại lỗi automation

| Mẫu lỗi | Số TC | Mô tả |
| :--- | :--- | :--- |
| Timeout (30s) | 24 | Invalid input không có phản hồi lỗi UI/API rõ ràng |
| Assertion fail | 15 | Thiếu UI (#4, #5, #9), reset không redirect (#7), OTP cross-email pass (#10) |
| Pass | 5 | TC-010, 022, 023, 024, 025 |

## Bug reports (paste vào GitHub Issues)

| Issue | Title | Found by (this run) |
| :--- | :--- | :--- |
| #4 | Missing confirm-password field | TC-FORGOT-001, 017, 018, 036, 041, 044 |
| #5 | Missing Step Indicator | TC-FORGOT-019 |
| #6 | OTP 4 digits not 6 | TC-FORGOT-006–008, 027, 029, SUP-001 |
| #7 | Wrong password regex | TC-FORGOT-001, 009, 011–016, 028, 030–035, 037–043 |
| #8 | Email type text not email | TC-FORGOT-003, SUP-003 |
| #9 | Back button not to login | TC-FORGOT-020 |
| #10 | No server password validation | TC-FORGOT-SUP-002 |

Chi tiết: \`tests/bug-reports/issue-004\` … \`issue-010.md\`  
Artifacts: \`test-results/\` (screenshots, traces, video)
`;

fs.writeFileSync(
  path.join(ROOT, 'tests/test-runs/sprint-3-test-run.md'),
  report,
  'utf8'
);

const tcDir = path.join(ROOT, 'tests/test-cases/forgot');
for (const r of rows) {
  const file = path.join(tcDir, `${r.id}.md`);
  if (!fs.existsSync(file)) continue;
  const m = meta[r.num];
  let content = fs.readFileSync(file, 'utf8');
  content = content.replace(
    /## Status \/ Related bugs\r?\n.+/,
    `## Status / Related bugs\n${r.result} / ${m.bugs}`
  );
  fs.writeFileSync(file, content, 'utf8');
}

console.log(`Report written. Updated ${rows.length} TC files. Pass: ${pass}, Fail: ${fail}`);
