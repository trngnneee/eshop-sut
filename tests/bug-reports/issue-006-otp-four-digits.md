# Bug Report #6 — Ready for GitHub Issue

**Title:** [BUG][Forgot Password] OTP is 4 digits not 6

**Found by Test Case:** TC-FORGOT-007, TC-FORGOT-008, TC-FORGOT-SUP-001  
**Requirement:** FR-03  
**Severity / Priority:** Major / P1  
**Environment:** Windows 11 · Chromium · API `http://localhost:3000`  
**Reported by:** QA / Playwright automation  
**Date:** 2026-06-29

**Classification:** Type: Functional | Severity: Major | Priority: P1

## Description

Đặc tả FR-03 yêu cầu OTP **6 chữ số ngẫu nhiên**. Backend sinh token 4 chữ số (`1000–9999`) và UI ghi nhãn "Mã OTP (4 số)".

## Steps to Reproduce

1. `POST /api/forgot-password` với `{"email":"test@eshop.com"}`.
2. Đọc `resetToken` trong response.
3. Mở Bước 2 trên UI và đọc nhãn trường OTP.

## Expected Result

- `resetToken` dài 6 chữ số (`^\d{6}$`).
- Label UI mô tả OTP 6 số.

## Actual Result

- `server.js:72`: `Math.floor(1000 + Math.random() * 9000)` → 4 chữ số.
- `ForgotPassword.jsx:70`: label "Mã OTP (4 số)".

## Evidence

- Playwright TC-FORGOT-008: `OTP must be exactly 6 digits` — Received length 4.

## Suggested Labels

`type: bug`, `module: forgot`, `severity: major`, `priority: P1`, `status: new`, `found-by: test-case`, `technique: BVA`
