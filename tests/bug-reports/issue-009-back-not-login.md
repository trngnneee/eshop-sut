# Bug Report #9 — Ready for GitHub Issue

**Title:** [BUG][Forgot Password] Back control does not return to login

**Found by Test Case:** TC-FORGOT-020  
**Requirement:** FR-03  
**Severity / Priority:** Minor / P2  
**Environment:** Windows 11 · Chromium · `http://localhost:5173`  
**Reported by:** QA / manual + spec review  
**Date:** 2026-06-29

**Classification:** Type: UI/UX | Severity: Minor | Priority: P2

## Description

FR-03 yêu cầu nút **Quay lại đăng nhập**. Bước 1 không có link đăng nhập; Bước 2 chỉ có nút "← Quay lại" gọi `setStep(1)` thay vì điều hướng `/login`.

## Steps to Reproduce

1. Mở `/forgot-password` (Bước 1) — tìm "Quay lại đăng nhập".
2. Hoàn thành Bước 1, ở Bước 2 bấm "← Quay lại".
3. Quan sát URL.

## Expected Result

Nút/link "Quay lại đăng nhập" có ở flow; bấm sẽ về `/login`.

## Actual Result

- Bước 1: không có nút quay lại đăng nhập.
- Bước 2: `onClick={() => setStep(1)}` — quay Bước 1, URL vẫn `/forgot-password`.

## Evidence

- `ForgotPassword.jsx:94-96`

## Suggested Labels

`type: bug`, `module: forgot`, `severity: minor`, `priority: P2`, `status: new`, `found-by: test-case`, `technique: EP`
