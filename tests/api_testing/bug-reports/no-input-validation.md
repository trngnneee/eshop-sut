---
name: Bug Report
about: Mẫu báo cáo lỗi khi thực hiện test case thất bại
title: '[BUG][API-3] POST/PUT không validate input theo FR-15 (name rỗng / price ≤0 / category không tồn tại)'
labels: ['type: bug', 'status: new', 'found-by: test-case']
assignees: ''
---

## Found by Test Case

TC-P3-004, 005, 008, 009, 011, 012, 013, 014, 015, 016, 021, 022, 023, 024, 025, 030, 036, 037, 038, 068, 076; DD-2

## Requirement liên quan

FR-15

## Severity / Priority

Critical / P0

## Environment

- **OS**: macOS (Darwin 24.5.0)
- **Browser**: Không dùng browser — kiểm thử API bằng Postman 11.x + Newman (newman-reporter-htmlextra)
- **URL**: http://localhost:3000
- **Build/Commit**: eshop-sut @ `0601698` (Node/Express + SQLite; `database.js` DROP+reseed mỗi lần `node server.js`)

## Steps to reproduce

1. `curl -X POST .../api/products -d '{"name":"","price":-500,"category_id":9999}'` → `200` created
2. `curl -X POST .../api/products -d '{"name":"x","price":1000}'` (thiếu category_id) → `200`
3. Chạy DD-2 với `products.csv`: 5 dòng vi phạm đều trả 200

## Expected result

`400` + `{error}` cho mọi input vi phạm: `name` bắt buộc ≤255, `price` bắt buộc >0, `category_id` phải tồn tại.

## Actual result

`200` created/updated cho MỌI input — không có tầng validation.

**Root cause:** `server.js:167-177` (POST) và `:179-189` (PUT) đưa thẳng `req.body` vào INSERT/UPDATE; DB không có FOREIGN KEY.

**Fix gợi ý:** Thêm validation (name non-empty ≤255, price integer >0, category_id tồn tại) ⇒ 400; bật FK.

## Evidence

TC-P3-030 (tổ hợp lỗi) assert 400 FAIL (nhận 200). DD-2 report-dd2.html: 5/6 dòng đỏ.

Run tổng: **Postman Runner 905 tests → 629 pass / 276 fail**; **Newman 893 assertions / 327 failed** (các fail là bằng chứng bug, không phải lỗi test).

- `tests/api_testing/newman/report.html` (htmlextra — lọc theo TC-ID ở cột Failed)
- `tests/api_testing/newman/screenshots/postman-run-result.png`
- `tests/api_testing/newman/screenshots/newman-terminal-localhost.png` (chứng minh host `localhost:3000`)
- `tests/api_testing/newman/screenshots/newman-htmlextra-summary.png`
