# Bug Report #23 — Ready for GitHub Issue

**Title:** [BUG][Mobile Forgot Password] Step Indicator not displayed

**Found by Test Case:** TC-MFORGOT-019  
**Requirement:** FR-22 (≡ FR-03)  
**Severity / Priority:** Minor / P2  
**Environment:** Windows 11 · Mobile App (Expo Web) `http://localhost:8081`  
**Reported by:** QA / black-box testing (Playwright)  
**Date:** 2026-06-29

**Classification:** Type: UI/UX | Severity: Minor | Priority: P2

## Description

Màn hình Quên mật khẩu Mobile không hiển thị chỉ báo bước (Step Indicator) như *"Bước 1 / 2"* hoặc *"Bước 2 / 2"* theo FR-03/FR-22. Người dùng khó biết đang ở bước nào trong luồng hai bước.

## Steps to Reproduce

1. Mở Mobile App → **Đăng nhập** → **Quên mật khẩu?**.
2. Quan sát header/form ở Bước 1 — tìm text dạng *"Bước 1 / 2"*.
3. Nhập email hợp lệ → **Lấy mã OTP** → quan sát lại ở Bước 2.

## Expected Result

UI hiển thị Step Indicator phản ánh bước hiện tại (ví dụ *"Bước 1 / 2"*, sau đó *"Bước 2 / 2"*).

## Actual Result

Không có text hoặc thành phần UI nào hiển thị chỉ báo bước. Chỉ thấy tiêu đề *"Quên Mật Khẩu"* (hoặc tương đương) ở cả hai bước.

## Evidence

- Playwright `TC-MFORGOT-019`: assertion *"Step 1 must show indicator (FR-22)"* failed — no step indicator text found on screen.

## Suggested Labels

`type: bug`, `module: mobile`, `module: forgot`, `severity: minor`, `priority: P2`, `found-by: test-case`, `technique: EP`, `testing: black-box`
