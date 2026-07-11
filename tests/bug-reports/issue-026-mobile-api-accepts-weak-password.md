# Bug Report #26 — Ready for GitHub Issue

**Title:** [BUG][Mobile Forgot Password] Backend accepts weak password on reset

**Found by Test Case:** TC-MFORGOT-SUP-003  
**Requirement:** FR-22, FR-01  
**Severity / Priority:** Major / P2  
**Environment:** Backend API `http://localhost:3000` (tested from Mobile FR-22 suite)  
**Reported by:** QA / black-box API testing  
**Date:** 2026-06-29

**Classification:** Type: Security | Severity: Major | Priority: P2

## Description

Theo FR-01, mật khẩu mới phải đáp ứng quy tắc độ mạnh (tối thiểu 8 ký tự, hoa/thường/số/ký tự đặc biệt). Khi reset qua API (giao diện ngoài mà Mobile App gọi), backend **chấp nhận mật khẩu yếu** `weakpass` nếu OTP đúng — không có validation phía server.

## Steps to Reproduce

1. Gọi `POST /api/forgot-password` với `{"email":"test@eshop.com"}` → lấy `resetToken`.
2. Gọi `POST /api/reset-password` với:
   ```json
   {"email":"test@eshop.com","resetToken":"<OTP>","newPassword":"weakpass"}
   ```
3. Quan sát HTTP status và response body.

## Expected Result

API trả **4xx** (từ chối); mật khẩu tài khoản **không** đổi.

## Actual Result

API trả **200 OK**; mật khẩu được cập nhật thành `weakpass` dù không đáp ứng FR-01.

## Evidence

- Playwright `TC-MFORGOT-SUP-003`: `response.ok()` = true for `newPassword: "weakpass"`.
- Manual test: HTTP status **200** for weak password reset.

## Suggested Labels

`type: bug`, `module: mobile`, `module: forgot`, `severity: major`, `priority: P2`, `found-by: test-case`, `technique: supplementary`, `testing: black-box`
