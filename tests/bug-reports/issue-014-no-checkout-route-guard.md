# Bug Report #14 — Ready for GitHub Issue

**Title:** [BUG][Checkout] Trang `/checkout` không yêu cầu đăng nhập (thiếu route guard)

**Found by Test Case:** TC-CHECKOUT-019 (thiết kế); liên quan FR-08 Rule 1  
**Requirement:** FR-08  
**Severity / Priority:** Major / P1  
**Environment:** Windows 11 · Chromium · `http://localhost:5173`  
**Reported by:** QA / Code review + test design  
**Date:** 2026-06-29

**Classification:** Type: Security / Functional | Severity: Major | Priority: P1

## Description

FR-08 yêu cầu chỉ người dùng **đã đăng nhập** mới tiến hành thanh toán. Hiện tại `App.jsx` mount route `/checkout` **không có** bảo vệ phiên đăng nhập; chỉ `Cart.jsx` kiểm tra `user` khi bấm "Tiến hành thanh toán". Người dùng có thể truy cập trực tiếp `/checkout` khi chưa đăng nhập.

## Steps to Reproduce

1. Xóa token / không đăng nhập.
2. Truy cập trực tiếp `http://localhost:5173/checkout`.
3. Quan sát trang vẫn tải (không chuyển `/login`).

## Expected Result

Chưa đăng nhập → chuyển hướng `/login` hoặc chặn thao tác xác nhận đơn hàng.

## Actual Result

Route `/checkout` public trong `App.jsx` (line 58). `Checkout.jsx` vẫn render form và cho phép gọi API (token rỗng nếu chưa login).

## Evidence

- `frontend-web/src/App.jsx` — `<Route path="/checkout" element={<Checkout />} />` không bọc auth
- So sánh: `Cart.jsx` lines 11–17 mới kiểm tra `user` trước khi `navigate('/checkout')`
- TC-CHECKOUT-019: automation chưa xác nhận do lỗi `logout()` trên `about:blank` — cần chạy lại sau sửa helper

## Suggested Labels

`type: bug`, `module: checkout`, `severity: major`, `priority: P1`, `status: new`, `found-by: test-case`, `requirement: FR-08`
