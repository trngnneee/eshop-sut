---
name: Bug Report
about: Mẫu báo cáo lỗi khi thực hiện test case thất bại
title: '[BUG][API-2] Đọc đơn hàng của bất kỳ ai KHÔNG cần token (IDOR read)'
labels: ['type: bug', 'status: new', 'found-by: test-case']
assignees: ''
---

## Found by Test Case

TC-O2-058, TC-O2-034

## Requirement liên quan

SEC-02 / FR-10

## Severity / Priority

Critical / P0

## Environment

- **OS**: macOS (Darwin 24.5.0)
- **Browser**: Không dùng browser — kiểm thử API bằng Postman 11.x + Newman (newman-reporter-htmlextra)
- **URL**: http://localhost:3000
- **Build/Commit**: eshop-sut @ `0601698` (Node/Express + SQLite; `database.js` DROP+reseed mỗi lần `node server.js`)

## Steps to reproduce

1. `curl -i http://localhost:3000/api/orders/1` (KHÔNG gửi Authorization)

## Expected result

`401`/`403` — endpoint đơn hàng phải yêu cầu auth.

## Actual result

`200` + lộ `user_id`, `total_amount`, `shipping_address` của đơn bất kỳ ⇒ IDOR đọc mọi đơn.

**Root cause:** `server.js:344` — `app.get('/api/orders/:id', (req,res)=>{...})` thiếu `authenticateToken` (khác `/api/orders/:id/cancel` và `/api/orders/my-orders` đều có).

**Fix gợi ý:** Gắn `authenticateToken` + kiểm ownership (`WHERE id=? AND user_id=?`).

## Evidence

TC-O2-058 assert 401/403 FAIL (nhận 200, body chứa shipping_address).

Run tổng: **Postman Runner 905 tests → 629 pass / 276 fail**; **Newman 893 assertions / 327 failed** (các fail là bằng chứng bug, không phải lỗi test).

- `tests/api_testing/newman/report.html` (htmlextra — lọc theo TC-ID ở cột Failed)
- `tests/api_testing/newman/screenshots/postman-run-result.png`
- `tests/api_testing/newman/screenshots/newman-terminal-localhost.png` (chứng minh host `localhost:3000`)
- `tests/api_testing/newman/screenshots/newman-htmlextra-summary.png`
