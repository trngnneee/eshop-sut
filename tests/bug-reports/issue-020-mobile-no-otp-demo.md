# Bug Report #20 — Ready for GitHub Issue

**Title:** [BUG][Mobile Forgot Password] Demo does not display OTP on screen

**Found by Test Case:** TC-MFORGOT-SUP-002, TC-MFORGOT-001  
**Requirement:** FR-22 (≡ FR-03)  
**Severity / Priority:** Major / P1  
**Environment:** Windows 11 · Mobile App (Expo Web) `http://localhost:8081` · Backend API `http://localhost:3000`  
**Reported by:** QA / black-box testing (manual + Playwright)  
**Date:** 2026-06-29

**Classification:** Type: Functional | Severity: Major | Priority: P1

## Description

Theo FR-03/FR-22, môi trường demo phải **hiển thị trực tiếp mã OTP** trên màn hình sau Bước 1 để người dùng có thể hoàn tất Bước 2 mà không cần truy cập email. Trên Mobile App, sau khi yêu cầu OTP thành công, màn hình chỉ hiện thông báo chung — **không có mã OTP 6 chữ số** — khiến luồng demo bị chặn.

## Steps to Reproduce

1. Mở Mobile App → màn hình **Đăng nhập** → bấm **Quên mật khẩu?**.
2. Nhập email đã đăng ký `test@eshop.com` → bấm **Lấy mã OTP**.
3. Chờ chuyển sang Bước 2 và quan sát vùng thông báo phía trên form.

## Expected Result

Sau Bước 1, màn hình hiển thị message dạng **"Mã OTP của bạn là: 123456"** (6 chữ số), cho phép người dùng copy/nhập OTP vào Bước 2.

## Actual Result

Màn hình hiển thị message chung: *"Nếu email tồn tại trong hệ thống, mã OTP đã được gửi đến email của bạn"*. Không có dòng nào chứa mã OTP 6 chữ số.

## Evidence

- Playwright `TC-MFORGOT-SUP-002`: expected message matching `Mã OTP của bạn là: <6 digits>`, received generic email-sent message only.
- Manual test run `mforgot-manual-test-run.md`: `demoShowsOtp` = not visible on screen.

## Suggested Labels

`type: bug`, `module: mobile`, `module: forgot`, `severity: major`, `priority: P1`, `found-by: test-case`, `technique: supplementary`, `testing: black-box`
