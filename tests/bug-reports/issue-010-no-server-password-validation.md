# Bug Report #10 — Ready for GitHub Issue

**Title:** [BUG][Forgot Password] API accepts weak passwords on reset

**Found by Test Case:** TC-FORGOT-SUP-002  
**Requirement:** FR-03, FR-01  
**Severity / Priority:** Major / P2  
**Environment:** API `http://localhost:3000`  
**Reported by:** QA / gap analysis supplementary TC  
**Date:** 2026-06-29

**Classification:** Type: Security | Severity: Major | Priority: P2

## Description

`POST /api/reset-password` cập nhật mật khẩu trực tiếp không kiểm tra độ mạnh theo FR-01, cho phép bypass validation client nếu gọi API trực tiếp.

## Steps to Reproduce

1. Lấy OTP hợp lệ cho `test@eshop.com`.
2. `POST /api/reset-password` với `newPassword: "weakpass"`.

## Expected Result

API 4xx; mật khẩu không đổi.

## Actual Result

`server.js:87-97` — UPDATE password không validate; chấp nhận bất kỳ chuỗi nào khi OTP đúng.

## Evidence

- Code review `backend/server.js`
- TC-FORGOT-SUP-002 (Not Run — expected Fail)

## Suggested Labels

`type: bug`, `module: forgot`, `severity: major`, `priority: P2`, `status: new`, `found-by: test-case`, `technique: EP`
