# Bug Report #7 — Ready for GitHub Issue

**Title:** [BUG][Forgot Password] Password regex rejects valid special chars

**Found by Test Case:** TC-FORGOT-001, TC-FORGOT-009; **Mobile:** TC-MFORGOT-SUP-007, TC-MFORGOT-028, TC-MFORGOT-031  
**Requirement:** FR-03, FR-22, FR-01  
**Severity / Priority:** Major / P1  
**Environment:** Windows 11 · Chromium · `http://localhost:5173`  
**Reported by:** QA / Playwright automation  
**Date:** 2026-06-29

**Classification:** Type: Validation | Severity: Major | Priority: P1

## Description

Client-side validation dùng regex sai: yêu cầu **khoảng trắng** `(?=.*\s)` thay vì ký tự đặc biệt FR-01 (`@$!%*?&`). Mật khẩu hợp lệ như `NewPass1!` hoặc `Abc@1234` bị từ chối; reset không hoàn tất.

## Steps to Reproduce

1. Hoàn thành Bước 1 với `test@eshop.com`, lấy OTP hiển thị.
2. Nhập OTP đúng và mật khẩu mới `NewPass1!`.
3. Bấm "Đặt lại mật khẩu".

## Expected Result

Mật khẩu đạt FR-01 được chấp nhận; chuyển về `/login` sau thành công.

## Actual Result

Alert: `Mật khẩu quá yếu! Phải dài tối thiểu 8 ký tự, gồm chữ hoa, chữ thường, số và KÝ TỰ ĐẶC BIỆT.` — dù mật khẩu có `@` và đủ điều kiện FR-01.

## Evidence

- `ForgotPassword.jsx:27` — flawed regex
- Playwright: reset does not redirect to `/login`

## Suggested Labels

`type: bug`, `module: forgot`, `severity: major`, `priority: P1`, `status: new`, `found-by: test-case`, `technique: EP`
