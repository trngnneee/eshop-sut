---
name: Bug Report
about: Mẫu báo cáo lỗi khi thực hiện test case thất bại
title: '[BUG][API-3] PUT thiếu field làm NULL hóa các field không gửi (mất dữ liệu)'
labels: ['type: bug', 'status: new', 'found-by: test-case']
assignees: ''
---

## Found by Test Case

TC-P3-034, TC-P3-042

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

1. Tạo product hợp lệ (đủ 5 field)
2. `curl -X PUT http://localhost:3000/api/products/<id> -H 'Content-Type: application/json' -d '{"name":"Chỉ đổi tên"}'`
3. `GET /api/products/<id>` → `price/description/imageUrl/category_id` = null
4. Biến thể nặng: PUT body `{}` → null hóa TOÀN BỘ field

## Expected result

Chỉ đổi field được gửi (hoặc `400` nếu thiếu field bắt buộc); không mất dữ liệu.

## Actual result

`200`; các field KHÔNG gửi bị set `null`.

**Root cause:** `server.js:179-189` — `UPDATE products SET name=?,price=?,description=?,imageUrl=?,category_id=? WHERE id=?` với TẤT CẢ field; field thiếu = undefined → bind null.

**Fix gợi ý:** Chỉ update field có trong body (dynamic SET), hoặc bắt buộc gửi đủ field và trả 400 nếu thiếu.

## Evidence

TC-P3-034: hậu kiểm GET assert các field KHÔNG null — FAIL (đều null).

Run tổng: **Postman Runner 905 tests → 629 pass / 276 fail**; **Newman 893 assertions / 327 failed** (các fail là bằng chứng bug, không phải lỗi test).

- `tests/api_testing/newman/report.html` (htmlextra — lọc theo TC-ID ở cột Failed)
- `tests/api_testing/newman/screenshots/postman-run-result.png`
- `tests/api_testing/newman/screenshots/newman-terminal-localhost.png` (chứng minh host `localhost:3000`)
- `tests/api_testing/newman/screenshots/newman-htmlextra-summary.png`


**GitHub Issue:** [#454](https://github.com/trngnneee/eshop-sut/issues/454)

**Screenshot Issue:**

![Issue #454](screenshots/issue-454-put-null-fields.png)
