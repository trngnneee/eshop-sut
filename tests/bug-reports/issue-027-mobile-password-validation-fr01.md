# Bug Report #27 — Ready for GitHub Issue

**Title:** [BUG][Mobile Forgot Password] Password validation does not match FR-01

**Found by Test Case:** TC-MFORGOT-SUP-007, TC-MFORGOT-009, TC-MFORGOT-011–016, TC-MFORGOT-028–044 (password-related)  
**Requirement:** FR-22, FR-01  
**Severity / Priority:** Major / P1  
**Environment:** Windows 11 · Mobile App (Expo Web) `http://localhost:8081`  
**Reported by:** QA / black-box testing (manual + Playwright)  
**Date:** 2026-06-29

**Classification:** Type: Validation | Severity: Major | Priority: P1

## Description

Validation mật khẩu mới ở Bước 2 Mobile không khớp FR-01. Black-box testing ghi nhận hai hành vi sai:

1. **Chấp nhận mật khẩu không hợp lệ:** `Test1234+` (ký tự `+` không thuộc tập `@$!%*?&`) được chấp nhận và reset thành công.
2. **Từ chối mật khẩu hợp lệ:** `Abc@1234` (8 ký tự, đủ hoa/thường/số/ký tự `@`) bị từ chối với thông báo mật khẩu yếu.

## Steps to Reproduce

**Case A — invalid password accepted**

1. Hoàn thành Bước 1 với `test@eshop.com`, lấy OTP hợp lệ.
2. Bước 2: nhập OTP + mật khẩu `Test1234+` → **Đặt lại mật khẩu**.
3. Quan sát kết quả (thông báo thành công / chuyển màn hình).

**Case B — valid password rejected**

1. Lặp lại Bước 1–2 với mật khẩu `Abc@1234`.
2. Quan sát thông báo lỗi và việc reset có hoàn tất hay không.

## Expected Result

- Case A: hệ thống **từ chối** `Test1234+` (ký tự đặc biệt ngoài whitelist FR-01).
- Case B: hệ thống **chấp nhận** `Abc@1234` và đặt lại mật khẩu thành công.

## Actual Result

- Case A: popup/dialog **thành công** — mật khẩu `Test1234+` được chấp nhận.
- Case B: popup/dialog **lỗi** *"Mật khẩu quá yếu…"* — mật khẩu `Abc@1234` bị từ chối dù đáp ứng FR-01.

## Evidence

- Manual `TC-MFORGOT-SUP-007`: `clientAcceptsPlus` = true.
- Manual / Playwright `TC-MFORGOT-031`: valid 8-char password `Abc@1234` not accepted.
- Playwright `TC-MFORGOT-SUP-007`: success dialog shown for `Test1234+`.

## Suggested Labels

`type: bug`, `module: mobile`, `module: forgot`, `severity: major`, `priority: P1`, `found-by: test-case`, `technique: supplementary`, `testing: black-box`
