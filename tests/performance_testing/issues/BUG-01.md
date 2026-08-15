---
name: Bug Report
about: Mẫu báo cáo lỗi khi thực hiện test case thất bại
title: '[BUG][Auth] Account lockout sai spec FR-02: 2 lần sai đã khóa, khóa 180s thay vì 30s'
labels: ['type: bug', 'status: new', 'found-by: test-case', 'severity: major']
assignees: ''
---

## Found by Test Case

PERF-LOAD-01 / PERF-STRESS-01 / PERF-SPIKE-01 (bước xử lý lockout) — xác nhận bằng probe riêng `evidence/lockout_probe.md`.

## Requirement liên quan

FR-02 (Login and account lockout)

## Severity / Priority

Major / P1

## Environment

- **OS**: macOS 15.5 (Darwin 24.5.0), Apple M4
- **Browser**: N/A — Backend REST API (curl / JMeter 5.6.3)
- **URL**: http://localhost:3000/api/login
- **Build/Commit**: eshop-sut (HW05 SUT) · `backend/server.js` dòng 46–64

## Steps to reproduce

1. Chọn 1 user sạch (`login_attempts=0`), ví dụ `nguyen_probe@eshop.com`.
2. Gọi login SAI mật khẩu lần 1: `curl -X POST http://localhost:3000/api/login -H "Content-Type: application/json" -d '{"email":"nguyen_probe@eshop.com","password":"WRONG"}'` → 401 (attempts 0→2).
3. Gọi login SAI lần 2 → 401 (attempts 2→4 ≥ 3 ⇒ đặt `locked_until = now + 180000`).
4. Gọi login ĐÚNG mật khẩu `Test1234!` → nhận **HTTP 403** "Tài khoản đã bị khóa".

## Expected result

Theo spec FR-02: khóa sau **≥ 3** lần sai, thời gian khóa **~30 giây**.

## Actual result

- Chỉ **2 lần** sai đã bị khóa (mỗi lần sai `login_attempts += 2`, ngưỡng khóa `>= 3` — `server.js:54,56`).
- Thời gian khóa = `Date.now() + 180000` = **180 giây**, gấp 6× spec (`server.js:57`).
- Login đúng trong thời gian khóa trả 403.

## Evidence

`evidence/lockout_probe.md` (log curl 2 lần sai → login đúng nhận 403 + trạng thái DB `locked_until`).
![BUG-01](https://res.cloudinary.com/dnqinxiwo/image/upload/v1786794394/eshop-hw05/perf-bugs/BUG-01.png)
