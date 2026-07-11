# Bug Report #22 — Ready for GitHub Issue

**Title:** [BUG][Mobile Forgot Password] Step 2 missing confirm-password field

**Found by Test Case:** TC-MFORGOT-SUP-005, TC-MFORGOT-001, TC-MFORGOT-017, TC-MFORGOT-018, TC-MFORGOT-036, TC-MFORGOT-041, TC-MFORGOT-044  
**Requirement:** FR-22 (≡ FR-03)  
**Severity / Priority:** Major / P1  
**Environment:** Windows 11 · Mobile App (Expo Web) `http://localhost:8081`  
**Reported by:** QA / black-box testing (manual + Playwright)  
**Date:** 2026-06-29

**Classification:** Type: UI/UX | Severity: Major | Priority: P1

## Description

Bước 2 đặt lại mật khẩu trên Mobile App chỉ có trường **Mật khẩu mới**; thiếu hoàn toàn trường **Xác nhận mật khẩu mới** bắt buộc theo FR-03/FR-22. Người dùng không thể xác nhận mật khẩu và hệ thống không kiểm tra hai giá trị có khớp nhau.

## Steps to Reproduce

1. Mở Mobile App → **Đăng nhập** → **Quên mật khẩu?**.
2. Nhập `test@eshop.com` → bấm **Lấy mã OTP**.
3. Ở Bước 2, liệt kê tất cả trường nhập và nhãn hiển thị trên form.

## Expected Result

Form Bước 2 gồm: **Mã OTP**, **Mật khẩu mới**, và **Xác nhận mật khẩu mới**. Hệ thống từ chối khi hai mật khẩu không khớp.

## Actual Result

Form chỉ có **Mã OTP** và **Mật khẩu mới**. Không có trường hoặc nhãn *"Xác nhận mật khẩu"* / *"Confirm password"* trên màn hình.

## Evidence

- Playwright `TC-MFORGOT-SUP-005`: `hasConfirmPasswordField()` = false.
- Manual test: `hasConfirmLabel` = false; only one secure-text password field observed.

## Suggested Labels

`type: bug`, `module: mobile`, `module: forgot`, `severity: major`, `priority: P1`, `found-by: test-case`, `technique: supplementary`, `testing: black-box`
