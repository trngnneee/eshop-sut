# Bug Report #24 — Ready for GitHub Issue

**Title:** [BUG][Mobile Forgot Password] OTP is 4 digits, not 6

**Found by Test Case:** TC-MFORGOT-SUP-001, TC-MFORGOT-006–008, TC-MFORGOT-027–029, TC-MFORGOT-028  
**Requirement:** FR-22 (≡ FR-03)  
**Severity / Priority:** Major / P1  
**Environment:** Windows 11 · Mobile App (Expo Web) `http://localhost:8081` · Backend API `http://localhost:3000`  
**Reported by:** QA / black-box testing (manual + Playwright)  
**Date:** 2026-06-29

**Classification:** Type: Functional | Severity: Major | Priority: P1

## Description

Đặc tả FR-03/FR-22 yêu cầu OTP **6 chữ số ngẫu nhiên**. Khi kiểm thử black-box qua API và UI Mobile, OTP chỉ có **4 chữ số** và nhãn trường OTP trên Bước 2 ghi **"Mã OTP (4 số)"** thay vì 6 số.

## Steps to Reproduce

1. Gọi `POST http://localhost:3000/api/forgot-password` với body `{"email":"test@eshop.com"}`.
2. Đọc giá trị `resetToken` trong response JSON.
3. Mở Mobile App → Quên mật khẩu → hoàn thành Bước 1 → quan sát nhãn trường OTP ở Bước 2.

## Expected Result

- `resetToken` là chuỗi **6 chữ số** (ví dụ `482917`).
- Nhãn UI mô tả OTP **6 số** (ví dụ *"Mã OTP (6 số)"*).

## Actual Result

- `resetToken` trả về **4 chữ số** (ví dụ `5439`, độ dài = 4).
- Nhãn trên Mobile Bước 2 hiển thị **"Mã OTP (4 số)"**.

## Evidence

- Playwright `TC-MFORGOT-SUP-001`: `resetToken` length 4, label contains *"4 số"*.
- Manual test `TC-MFORGOT-SUP-001`: token `"5439"`, `labelBad` = true.

## Suggested Labels

`type: bug`, `module: mobile`, `module: forgot`, `severity: major`, `priority: P1`, `found-by: test-case`, `technique: BVA`, `testing: black-box`
