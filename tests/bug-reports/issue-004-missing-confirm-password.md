# Bug Report #4 — Ready for GitHub Issue

**Title:** [BUG][Forgot Password] Step 2 missing confirm-password field

**Found by Test Case:** TC-FORGOT-001, TC-FORGOT-017, TC-FORGOT-018  
**Requirement:** FR-03  
**Severity / Priority:** Major / P1  
**Environment:** Windows 11 · Chromium (Playwright 1.44) · `http://localhost:5173` · branch `tram`  
**Reported by:** QA / Playwright automation  
**Date:** 2026-06-29

**Classification:** Type: UI/UX | Severity: Major | Priority: P1

## Description

Bước 2 đặt lại mật khẩu chỉ có trường **Mật khẩu mới**; thiếu hoàn toàn trường **Xác nhận mật khẩu mới** bắt buộc theo FR-03. Người dùng không thể xác nhận mật khẩu và hệ thống không kiểm tra hai trường khớp nhau.

## Steps to Reproduce

1. Mở `/forgot-password`.
2. Nhập email đã đăng ký `test@eshop.com` → Lấy mã OTP.
3. Quan sát form Bước 2.

## Expected Result

Form hiển thị OTP, Mật khẩu mới, **và Xác nhận mật khẩu mới**; từ chối khi hai mật khẩu không khớp.

## Actual Result

Chỉ có OTP và Mật khẩu mới (`ForgotPassword.jsx` lines 69–88). Không có input xác nhận.

## Evidence

- `test-results/forgot-password-FR-03-*-with-new-password-succeeds-chromium/test-failed-1.png`
- Playwright: `Step 2 must include confirm-password field (FR-03)`

## Suggested Labels

`type: bug`, `module: forgot`, `severity: major`, `priority: P1`, `status: new`, `found-by: test-case`, `technique: EP`, `needs-screenshot`
