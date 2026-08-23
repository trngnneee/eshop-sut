---
name: Bug Report
about: Mẫu báo cáo lỗi khi thực hiện test case thất bại
title: '[BUG][API-3] Body rỗng `{}` tạo record toàn `null`'
labels: ['type: bug', 'status: new', 'found-by: test-case']
assignees: ''
---

## Found by Test Case

TC-P3-031, TC-P3-046

## Requirement liên quan

FR-15

## Severity / Priority

Major / P1

## Environment

- **OS**: macOS (Darwin 24.5.0)
- **Browser**: Không dùng browser — kiểm thử API bằng Postman 11.x + Newman (newman-reporter-htmlextra)
- **URL**: http://localhost:3000
- **Build/Commit**: eshop-sut @ `0601698` (Node/Express + SQLite; `database.js` DROP+reseed mỗi lần `node server.js`)

## Steps to reproduce

1. `curl -X POST http://localhost:3000/api/products -H 'Content-Type: application/json' -d '{}'`
2. `GET /api/products` → xuất hiện record `{name:null, price:null, ...}`

## Expected result

`400` — thiếu mọi field bắt buộc.

## Actual result

`200` created; record toàn `null` lọt vào bảng.

**Root cause:** `server.js:167-177` — không kiểm field bắt buộc trước INSERT.

**Fix gợi ý:** Validate required fields trước INSERT.

## Evidence

TC-P3-031 assert 400 FAIL (nhận 200).

Run tổng: **Postman Runner 905 tests → 629 pass / 276 fail**; **Newman 893 assertions / 327 failed** (các fail là bằng chứng bug, không phải lỗi test).

- `tests/api_testing/newman/report.html` (htmlextra — lọc theo TC-ID ở cột Failed)
- `tests/api_testing/newman/screenshots/postman-run-result.png`
- `tests/api_testing/newman/screenshots/newman-terminal-localhost.png` (chứng minh host `localhost:3000`)
- `tests/api_testing/newman/screenshots/newman-htmlextra-summary.png`
