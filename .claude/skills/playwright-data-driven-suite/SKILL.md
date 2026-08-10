---
name: playwright-data-driven-suite
description: Generate and maintain a data-driven, multi-browser Playwright test suite for one EShop feature (FR-XX). Use when asked to automate a feature, add test cases, or extend the HW04-style automation workflow to a new feature. Produces a JSON data file, Page Object, spec file, runs on 3 browsers, and triages failures into spec-violation bug reports.
---

# Playwright Data-Driven Suite (EShop SUT)

Quy trình chuẩn để automate một feature FR-XX của EShop theo đúng conventions của
`tests/automation_testing/` (đã dùng cho FR-02, FR-09, FR-14 trong HW04).
Làm TUẦN TỰ từng bước — không sinh toàn bộ trong một lượt.

## Bước 1 — Đọc spec và source thật (không đoán)

1. Đọc section FR-XX trong `README.md` (SRS) — liệt kê từng behavior + điều kiện biên.
2. Đọc component React thật (`frontend-web/src/` hoặc `frontend-admin/src/`) và endpoint
   backend liên quan trong `backend/server.js` + seed data trong `backend/database.js`.
3. Ghi lại: selectors khả dụng (role/placeholder/cấu trúc — labels của SUT KHÔNG có
   `htmlFor`, đừng dùng `getByLabel`), trạng thái server-side mà test sẽ chạm vào
   (counter, usage, rows...), và các điểm code lệch spec (ứng viên bug).

## Bước 2 — Thiết kế ≥12 test case

- Đủ 3 loại: positive / negative / edge (đặc biệt là boundary — spec dùng `>=` thì phải
  có case bằng đúng ngưỡng).
- Viết **expected theo SRS**, không theo hành vi hiện tại của SUT — fail lộ bug là kết
  quả mong đợi.
- Mỗi TC một dòng dữ liệu, đặt ID `FRXX-TCyy`.

## Bước 3 — Data file (bắt buộc data-driven)

- Toàn bộ TC vào `tests/automation_testing/data/frXX-<slug>.json` — spec KHÔNG được
  hardcode dữ liệu.
- Dùng token `{{UNIQUE}}` / `{{LONG255}}` cho dữ liệu cần duy nhất giữa các browser run.

## Bước 4 — Page Object + spec

- Page Object vào `pages/`, kế thừa style hiện có (locator theo role/placeholder/cấu trúc,
  method chờ response thay vì `waitForTimeout`).
- Spec vào `tests/frXX-<slug>.spec.ts`: chỉ là vòng lặp `for (const tc of data.cases)`
  dispatch theo `outcome`/`action`.
- Dùng ≥3 assertion pattern (URL, visibility/state, text, attribute/value, count,
  API response status, soft) — pattern API status là bắt buộc khi UI chỉ hiện thông báo chung.

## Bước 5 — Cô lập trạng thái (backend SQLite dùng chung!)

- Kịch bản làm bẩn state (lockout, usage limit...) → đăng ký user MỚI qua
  `utils/api.ts` cho từng test, không dùng tài khoản chung.
- Test tạo dữ liệu (category, product...) → snapshot trước test, xóa phần phát sinh
  trong `afterEach`.
- Giữ `workers: 1` — 3 browser đánh vào cùng một backend.

## Bước 6 — Chạy 3 browsers + report

```bash
REPORT_DIR=reports/frXX-<slug> npx playwright test frXX-<slug>.spec.ts
```

- Report phải mang "Run by: 23127438" + ISO timestamp (đã cấu hình sẵn trong
  `playwright.config.ts`; override MSSV bằng env `STUDENT_ID`).
- Verify bằng cách decode `report.json` nhúng trong `index.html` nếu cần bằng chứng.

## Bước 7 — Triage fail → bug report

- Một fail chỉ là bug khi: (1) tái hiện **nhất quán trên cả 3 browser**, và (2) truy được
  về một câu cụ thể trong SRS mà SUT vi phạm (kèm vị trí code sai).
- Bug thật → ghi vào `REPORT.md` + tạo GitHub issue theo template
  `.github/ISSUE_TEMPLATE/bug_report.md` (Found by TC / Requirement / Severity /
  Environment / Steps / Expected / Actual / Evidence), label
  `type: bug`, `status: new`, `found-by: test-case`.
- Screenshot: copy vào `bugs/screenshots/` tên `bug-XX-<slug>.png`, upload Cloudinary
  bằng `scripts/upload-screenshots-cloudinary.mjs` (credentials qua env, không hardcode).
- Fail do script sai → sửa script, ghi vào section review của `REPORT.md` (AI sai gì,
  vì sao, sửa thế nào) — mỗi fix đáng kể là một commit riêng đụng file `.spec.ts`.

## Bước 8 — Cập nhật hồ sơ nộp bài

- Cập nhật bảng TC + bug trong `REPORT.md`, AI Audit Report trong `ai_declaration/`
  (một dòng cho artifact mới, prompt verbatim), và export lại `git_log.txt`.
