# Bug Report #16 — Ready for GitHub Issue

**Title:** [BUG][Admin Product] Product CRUD API lacks authentication and admin role check

**Found by Test Case:** TC-PRODUCT-SUP-003, TC-PRODUCT-SUP-004  
**Requirement:** FR-12, SEC-02, SEC-03  
**Severity / Priority:** Critical / P1  
**Environment:** API `http://localhost:3000` · Playwright `npm run test:fr15`  
**Reported by:** QA / Playwright automation  
**Date:** 2026-06-29

**Classification:** Type: Security | Severity: Critical | Priority: P1

## Description

FR-12 quy định `POST/PUT/DELETE /api/products` phải yêu cầu JWT hợp lệ **và** `role = 'admin'`. Hiện tại các endpoint này không dùng middleware `authenticateToken`, cho phép bất kỳ client nào tạo/sửa/xóa sản phẩm.

## Steps to Reproduce

1. **Không gửi JWT:** `POST http://localhost:3000/api/products` với body `{ "name": "Hack", "price": 1, "category_id": 1 }`.
2. **Gửi JWT user thường:** Đăng nhập `test@eshop.com`, lấy token, gọi cùng endpoint với header `Authorization: Bearer <token>`.

## Expected Result

- Không JWT → **401 Unauthorized**.
- JWT user (`role !== 'admin'`) → **403 Forbidden**.

## Actual Result

- Cả hai trường hợp đều trả về **200 OK** và tạo sản phẩm `"Hack"` trong database.
- Playwright: `Expected: 401 Received: 200` (SUP-003); `Expected: 403 Received: 200` (SUP-004).

## Evidence

- `backend/server.js` lines 167–196 — `POST/PUT/DELETE /api/products` không có `authenticateToken` (so sánh với `POST /api/categories` và `POST /api/admin/import-products` có middleware).
- Playwright TC-PRODUCT-SUP-003, TC-PRODUCT-SUP-004 — `admin-product.spec.js:372`, `:381`.
- Sản phẩm `"Hack"` xuất hiện trên trang chủ sau khi gọi API không xác thực.

## Suggested Labels

`type: bug`, `module: admin-product`, `severity: critical`, `priority: P1`, `status: new`, `found-by: test-case`, `requirement: FR-12`, `security`
