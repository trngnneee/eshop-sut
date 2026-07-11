# Bug Report #11 — Ready for GitHub Issue

**Title:** [BUG][Checkout] Tổng tiền thanh toán cho phép chỉnh sửa trực tiếp trên UI

**Found by Test Case:** TC-CHECKOUT-004  
**Requirement:** FR-08  
**Severity / Priority:** Major / P1  
**Environment:** Windows 11 · Chromium (Playwright) · `http://localhost:5173` · `http://localhost:3000`  
**Reported by:** QA / Playwright automation  
**Date:** 2026-06-29

**Classification:** Type: Functional | Severity: Major | Priority: P1

## Description

Trang Thanh toán hiển thị trường `input[type="number"]` cho **Tổng tiền thanh toán**, cho phép người dùng tự ý thay đổi giá trị. Vi phạm FR-08: *"Tổng tiền thanh toán được tính tự động từ giỏ hàng và **không cho phép người dùng chỉnh sửa trực tiếp**"*.

## Steps to Reproduce

1. Đăng nhập `test@eshop.com` / `Test1234!`.
2. Thêm sản phẩm vào giỏ và mở `/checkout`.
3. Quan sát trường "Tổng tiền thanh toán (VND)".
4. Thử nhập giá trị khác (ví dụ `1`).

## Expected Result

Tổng tiền hiển thị dạng read-only/text; người dùng không thể sửa trên UI.

## Actual Result

`Checkout.jsx` dùng `editableTotal` state và `<input type="number">` có `onChange` — người dùng sửa được tổng tiền.

## Evidence

- Playwright: `Total must not be user-editable` — `isTotalEditable()` trả về `true`
- `frontend-web/src/pages/Checkout.jsx` lines 15, 92–103
- Screenshot: `test-results/checkout-FR-08-·-Checkout--*Total-amount-not-editable*/test-failed-1.png`

## Suggested Labels

`type: bug`, `module: checkout`, `severity: major`, `priority: P1`, `status: new`, `found-by: test-case`, `requirement: FR-08`
