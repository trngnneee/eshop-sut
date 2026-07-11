# Bug Report #5 — Ready for GitHub Issue

**Title:** [BUG][Forgot Password] Step Indicator not displayed

**Found by Test Case:** TC-FORGOT-019, TC-GUI-008; **Mobile:** TC-MFORGOT-019  
**Requirement:** FR-03, FR-22  
**Severity / Priority:** Minor / P2  
**Environment:** Windows 11 · Chromium · `http://localhost:5173`  
**Reported by:** QA / Playwright automation  
**Date:** 2026-06-29

**Classification:** Type: UI/UX | Severity: Minor | Priority: P2

## Description

Trang Quên mật khẩu không hiển thị chỉ báo bước (Step Indicator) như "Bước 1 / 2" hoặc "Bước 2 / 2" theo FR-03 và **FR-22** (*"Các form có từ 2 bước trở lên phải có Step Indicator rõ ràng"*).

## Steps to Reproduce

1. Truy cập `/forgot-password`.
2. Quan sát phần header/form Bước 1.
3. Gửi email hợp lệ, chuyển sang Bước 2 và quan sát lại.

## Expected Result

UI hiển thị Step Indicator phản ánh bước hiện tại (ví dụ "Bước 1 / 2", sau đó "Bước 2 / 2").

## Actual Result

Không có phần tử chỉ báo bước trong DOM; chỉ có tiêu đề "Quên Mật Khẩu".

## Evidence

- Playwright: `Step 1 must show Step Indicator (FR-03)` — `test-results/.../test-failed-1.png`

## Suggested Labels

`type: bug`, `module: forgot`, `severity: minor`, `priority: P2`, `status: new`, `found-by: test-case`, `technique: EP`
