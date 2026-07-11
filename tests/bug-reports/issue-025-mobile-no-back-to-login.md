# Bug Report #25 — Ready for GitHub Issue

**Title:** [BUG][Mobile Forgot Password] No control to return to login screen

**Found by Test Case:** TC-MFORGOT-020  
**Requirement:** FR-22 (≡ FR-03)  
**Severity / Priority:** Minor / P2  
**Environment:** Windows 11 · Mobile App (Expo Web) `http://localhost:8081`  
**Reported by:** QA / black-box testing (Playwright)  
**Date:** 2026-06-29

**Classification:** Type: UI/UX | Severity: Minor | Priority: P2

## Description

FR-03/FR-22 yêu cầu nút/link **Quay lại đăng nhập** trong luồng Quên mật khẩu. Trên Mobile App, Bước 1 không có cách quay về màn hình Đăng nhập; Bước 2 chỉ có **← Quay lại** đưa về Bước 1, không về Đăng nhập.

## Steps to Reproduce

1. Mở Mobile App → **Đăng nhập** → **Quên mật khẩu?** (Bước 1).
2. Tìm nút/link *"Quay lại đăng nhập"* trên màn hình.
3. Hoàn thành Bước 1 → ở Bước 2 bấm **← Quay lại** → quan sát màn hình hiện tại.

## Expected Result

- Bước 1 (và/hoặc Bước 2) có nút **Quay lại đăng nhập**.
- Bấm nút đó đưa người dùng về màn hình **Đăng nhập**.

## Actual Result

- Bước 1: không có nút/link *"Quay lại đăng nhập"*.
- Bước 2: nút **← Quay lại** chỉ quay về Bước 1 (form nhập email), không về màn hình Đăng nhập.

## Evidence

- Playwright `TC-MFORGOT-020`: assertion *'"Quay lại đăng nhập" required on Step 1'* failed — control not visible on screen.

## Suggested Labels

`type: bug`, `module: mobile`, `module: forgot`, `severity: minor`, `priority: P2`, `found-by: test-case`, `technique: EP`, `testing: black-box`
