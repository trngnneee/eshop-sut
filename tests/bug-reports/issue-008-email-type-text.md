# Bug Report #8 — Ready for GitHub Issue

**Title:** [BUG][Forgot Password] Email input uses type text not email

**Found by Test Case:** TC-FORGOT-003, TC-FORGOT-SUP-003  
**Requirement:** FR-22, FR-03  
**Severity / Priority:** Minor / P2  
**Environment:** Windows 11 · Chromium · `http://localhost:5173`  
**Reported by:** QA / Playwright automation  
**Date:** 2026-06-29

**Classification:** Type: Validation | Severity: Minor | Priority: P2

## Description

Trường Email ở Bước 1 dùng `type="text"` thay vì `type="email"` theo FR-22, làm giảm kiểm tra HTML5 cho định dạng email.

## Steps to Reproduce

1. Mở `/forgot-password`.
2. Inspect input Email.
3. Nhập `notanemail` (không có `@`) và submit.

## Expected Result

`type="email"`; trình duyệt chặn hoặc cảnh báo format không hợp lệ.

## Actual Result

`ForgotPassword.jsx:51` — `type="text"`; email sai format vẫn có thể gửi request API.

## Evidence

- Playwright TC-FORGOT-007 (automation): expects `type="email"` — Received `text`.

## Suggested Labels

`type: bug`, `module: forgot`, `severity: minor`, `priority: P2`, `status: new`, `found-by: test-case`, `technique: EP`
