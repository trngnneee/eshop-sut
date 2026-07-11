# Bug Report #12 — Ready for GitHub Issue

**Title:** [BUG][Checkout API] Backend lưu `total_amount` do client gửi, không tự tính lại

**Found by Test Case:** TC-CHECKOUT-015, TC-CHECKOUT-016, TC-CHECKOUT-018, TC-CHECKOUT-026, TC-CHECKOUT-029, TC-CHECKOUT-031, TC-CHECKOUT-038, TC-CHECKOUT-039, TC-CHECKOUT-042, TC-CHECKOUT-043, TC-CHECKOUT-SUP-003, TC-CHECKOUT-SUP-004  
**Requirement:** FR-08  
**Severity / Priority:** Critical / P0  
**Environment:** Windows 11 · Chromium (Playwright) · Backend `http://localhost:3000`  
**Reported by:** QA / Playwright automation  
**Date:** 2026-06-29

**Classification:** Type: Security / Functional | Severity: Critical | Priority: P0

## Description

API `POST /api/checkout` ghi trực tiếp `total_amount` từ `req.body` vào CSDL mà **không** tính lại từ giỏ hàng/sản phẩm. Vi phạm FR-08: *"Backend phải tự tính lại tổng tiền; không chấp nhận giá trị `total_amount` do client gửi lên"*.

## Steps to Reproduce

1. Đăng nhập và lấy JWT hợp lệ.
2. Gửi `POST /api/checkout` với sản phẩm có tổng thực tế 30.000.000 ₫ nhưng `total_amount: 1` (hoặc `0`, `-1`, `cartTotal-1`, `cartTotal+1`, `"abc"`).
3. Gọi `GET /api/orders/my-orders` và đọc `total_amount` đơn vừa tạo.

## Expected Result

- Backend tính lại tổng từ dữ liệu giỏ/sản phẩm thực tế, **hoặc**
- Từ chối yêu cầu khi `total_amount` client gửi không khớp tổng thực tế.

## Actual Result

Đơn hàng lưu đúng giá trị `total_amount` do client gửi (ví dụ `1`, `0`, `-1`, `29999999`, `28000000`). API cũng bỏ qua trường `items` trong body.

## Evidence

- Playwright: `Backend must not persist tampered total_amount=…`
- `backend/server.js` lines 297–308: `INSERT INTO orders … total_amount` từ `req.body` trực tiếp
- UI path: TC-CHECKOUT-026 — sửa tổng trên UI thành `1`, đơn lưu `total_amount = 1`

## Suggested Labels

`type: bug`, `module: checkout`, `severity: critical`, `priority: P0`, `status: new`, `found-by: test-case`, `requirement: FR-08`, `security`
