# Bug Report #21 — Ready for GitHub Issue

**Title:** [BUG][Mobile Forgot Password] Validation error shown in popup dialog instead of inline (FR-22)

**Found by Test Case:** TC-MFORGOT-SUP-006  
**Requirement:** FR-22  
**Severity / Priority:** Minor / P2  
**Environment:** Windows 11 · Mobile App (Expo Web) `http://localhost:8081`  
**Reported by:** QA / black-box testing (manual + Playwright)  
**Date:** 2026-06-29

**Classification:** Type: UI/UX | Severity: Minor | Priority: P2

## Description

FR-22 yêu cầu thông báo lỗi validation hiển thị **trên** nút submit (inline), không dùng popup che màn hình. Trên Mobile Quên mật khẩu, khi nhập dữ liệu không hợp lệ (ví dụ mật khẩu yếu), hệ thống hiện **hộp thoại popup** thay vì dòng lỗi cố định trên form — khác với pattern inline trên các màn hình Đăng nhập/Đăng ký Mobile.

## Steps to Reproduce

1. Mở Mobile App → **Đăng nhập** → **Quên mật khẩu?**.
2. Hoàn thành Bước 1 với `test@eshop.com`, lấy OTP hợp lệ (qua API hoặc demo).
3. Ở Bước 2, nhập OTP đúng và mật khẩu yếu `weakpass` → bấm **Đặt lại mật khẩu**.
4. Quan sát vị trí và kiểu thông báo lỗi.

## Expected Result

Thông báo lỗi (ví dụ *"Mật khẩu quá yếu…"*) xuất hiện **inline** trên form, phía **trên** nút **Đặt lại mật khẩu**, không che toàn màn hình.

## Actual Result

Hệ thống hiện **popup dialog** (tiêu đề *"Lỗi"*, nội dung mô tả mật khẩu yếu). Người dùng phải bấm OK để đóng dialog. Không có dòng lỗi inline trên form.

## Evidence

- Manual test `TC-MFORGOT-SUP-006`: validation error delivered via popup dialog, not inline text on form.
- Playwright `TC-MFORGOT-SUP-006`: inline error count = 0; dialog message captured instead.

## Suggested Labels

`type: bug`, `module: mobile`, `module: forgot`, `severity: minor`, `priority: P2`, `found-by: test-case`, `technique: supplementary`, `testing: black-box`
