---
name: Bug Report
about: Mẫu báo cáo lỗi khi thực hiện test case thất bại
title: '[BUG][API-2/API-3] Secret JWT hardcode → forge token, mạo danh + nâng quyền'
labels: ['type: bug', 'status: new', 'found-by: test-case']
assignees: ''
---

## Found by Test Case

TC-O2-032, TC-O2-033, TC-O2-034; TC-P3-051

## Requirement liên quan

SEC-02 / SEC-03

## Severity / Priority

Critical / P0

## Environment

- **OS**: macOS (Darwin 24.5.0)
- **Browser**: Không dùng browser — kiểm thử API bằng Postman 11.x + Newman (newman-reporter-htmlextra)
- **URL**: http://localhost:3000
- **Build/Commit**: eshop-sut @ `0601698` (Node/Express + SQLite; `database.js` DROP+reseed mỗi lần `node server.js`)

## Steps to reproduce

1. Trong `eshop-sut/backend/`: `node -e 'console.log(require("jsonwebtoken").sign({id:1,role:"user"},"super_secret_key_that_should_not_be_here"))'`
2. Dùng token đó: `PUT /api/orders/<đơn của user id=1>/cancel` → `200` (hủy được đơn người khác)
3. Forge `{id:2,role:"admin"}` tương tự → verify PASS

## Expected result

`401`/`403` — token giả phải bị từ chối (secret nằm ngoài source, có `exp`).

## Actual result

`200` — chữ ký hợp lệ (secret lộ) ⇒ `jwt.verify` PASS ⇒ mạo danh id bất kỳ, hủy đơn của mọi user.

**Root cause:** `server.js:9` — `const SECRET_KEY = "super_secret_key_that_should_not_be_here";` hardcode trong repo public. `server.js:51` sign không có `exp`.

**Fix gợi ý:** Đưa secret ra biến môi trường (không commit), rotate secret, thêm `expiresIn`; cân nhắc kiểm `role` từ DB.

## Evidence

TC-O2-032 assert status != 200 FAIL (nhận 200) khi dán `{{forgedVictim}}`. TC-O2-034 hậu kiểm đơn bị canceled.

> Cần dán forged token vào environment (`forgedVictim`/`forgedAdminRole`) trước khi chạy — xem mô tả request.

Run tổng: **Postman Runner 905 tests → 629 pass / 276 fail**; **Newman 893 assertions / 327 failed** (các fail là bằng chứng bug, không phải lỗi test).

- `tests/api_testing/newman/report.html` (htmlextra — lọc theo TC-ID ở cột Failed)
- `tests/api_testing/newman/screenshots/postman-run-result.png`
- `tests/api_testing/newman/screenshots/newman-terminal-localhost.png` (chứng minh host `localhost:3000`)
- `tests/api_testing/newman/screenshots/newman-htmlextra-summary.png`
