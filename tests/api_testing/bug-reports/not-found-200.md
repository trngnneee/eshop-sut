---
name: Bug Report
about: Mẫu báo cáo lỗi khi thực hiện test case thất bại
title: '[BUG][API-1] GET id không tồn tại trả `200 {}` thay vì `404`'
labels: ['type: bug', 'status: new', 'found-by: test-case']
assignees: ''
---

## Found by Test Case

TC-P1-006, TC-P1-007, TC-P1-065

## Requirement liên quan

FR-06

## Severity / Priority

Major / P1

## Environment

- **OS**: macOS (Darwin 24.5.0)
- **Browser**: Không dùng browser — kiểm thử API bằng Postman 11.x + Newman (newman-reporter-htmlextra)
- **URL**: http://localhost:3000
- **Build/Commit**: eshop-sut @ `0601698` (Node/Express + SQLite; `database.js` DROP+reseed mỗi lần `node server.js`)

## Steps to reproduce

1. `curl -i http://localhost:3000/api/products/99999`
2. `curl -i http://localhost:3000/api/products/6` (biên trên+1)

## Expected result

`404 Not Found` + body `{error: string}`.

## Actual result

`200 OK` + body `{}` (object rỗng) — client không phân biệt 'không tồn tại' với 'thành công'.

**Root cause:** `server.js:161` — `if (!row) return res.status(200).json({});`.

**Fix gợi ý:** `if (!row) return res.status(404).json({ error: 'Product not found' });`

## Evidence

TC-P1-007 assert `pm.response.code === 404` FAIL (nhận 200).

Run tổng: **Postman Runner 905 tests → 629 pass / 276 fail**; **Newman 893 assertions / 327 failed** (các fail là bằng chứng bug, không phải lỗi test).

- `tests/api_testing/newman/report.html` (htmlextra — lọc theo TC-ID ở cột Failed)
- `tests/api_testing/newman/screenshots/postman-run-result.png`
- `tests/api_testing/newman/screenshots/newman-terminal-localhost.png` (chứng minh host `localhost:3000`)
- `tests/api_testing/newman/screenshots/newman-htmlextra-summary.png`
