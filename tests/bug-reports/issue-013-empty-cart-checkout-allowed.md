# Bug Report #13 — Ready for GitHub Issue

**Title:** [BUG][Checkout] Cho phép thanh toán khi giỏ hàng trống / lặp đơn rỗng

**Found by Test Case:** TC-CHECKOUT-028  
**Requirement:** FR-08  
**Severity / Priority:** Major / P1  
**Environment:** Windows 11 · Chromium (Playwright) · `http://localhost:5173`  
**Reported by:** QA / Playwright automation  
**Date:** 2026-06-29

**Classification:** Type: Functional | Severity: Major | Priority: P1

## Description

Sau khi thanh toán thành công lần đầu, người dùng có thể quay lại `/checkout` và **xác nhận thanh toán lần hai** dù giỏ hàng không còn sản phẩm. Hệ thống hiển thị "Thanh toán thành công!" và tạo thêm đơn hàng mới (thường với `total_amount` từ trường có thể sửa, ví dụ `0`).

## Steps to Reproduce

1. Đăng nhập `test@eshop.com`.
2. Mở `/checkout` và bấm "Xác Nhận Thanh Toán" (có thể không cần sản phẩm trong giỏ).
3. Sau thông báo thành công, mở lại `/checkout`.
4. Bấm "Xác Nhận Thanh Toán" lần nữa.

## Expected Result

- Không cho phép đặt hàng khi giỏ trống.
- Nút thanh toán bị ẩn/disabled hoặc chuyển hướng khỏi trang checkout.

## Actual Result

Lần thanh toán thứ hai vẫn thành công (`isOrderSuccessful()` = true).

## Evidence

- Playwright TC-CHECKOUT-028: `Second checkout with empty cart must fail` — nhận `true`
- Screenshot: `test-results/checkout-FR-08-·-Checkout--5e73d-out-blocked-when-cart-empty-chromium/test-failed-1.png`
- `Checkout.jsx`: không kiểm tra `cart.length` trước khi gọi API

## Suggested Labels

`type: bug`, `module: checkout`, `severity: major`, `priority: P1`, `status: new`, `found-by: test-case`, `requirement: FR-08`
