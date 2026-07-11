# Bug Report #17 — Ready for GitHub Issue

**Title:** [BUG][Admin Product] API accepts invalid product data (no server-side validation)

**Found by Test Case:** TC-PRODUCT-SUP-001, TC-PRODUCT-SUP-007  
**Requirement:** FR-15  
**Severity / Priority:** Major / P1  
**Environment:** API `http://localhost:3000` · Playwright `npm run test:fr15`  
**Reported by:** QA / Playwright automation  
**Date:** 2026-06-29

**Classification:** Type: Validation | Severity: Major | Priority: P1

## Description

FR-15 quy định: Tên bắt buộc (max 255 ký tự), Giá bắt buộc **> 0**, Danh mục bắt buộc từ danh sách hợp lệ. Handler `POST /api/products` insert trực tiếp vào SQLite mà không validate, cho phép bypass mọi kiểm tra phía client.

## Steps to Reproduce

1. `POST /api/products` với `category_id: 99999` (không tồn tại).
2. `POST /api/products` với `name` dài **256** ký tự, `price: 100000`, `category_id` hợp lệ.
3. `POST /api/products` với `name: "Valid"`, `price: 0`, `category_id` hợp lệ.

## Expected Result

Mỗi request trả về **4xx**; không tạo/cập nhật bản ghi.

## Actual Result

- `category_id: 99999` → **200 OK**, sản phẩm được tạo (`res.ok === true`).
- Tên 256 ký tự → **200 OK** (`resName.ok === true`).
- Giá `0` → dự kiến cũng được chấp nhận (test dừng ở assertion tên 256).

## Evidence

- `backend/server.js` lines 167–176 — INSERT không kiểm tra độ dài tên, giá > 0, hay `category_id` tồn tại.
- Playwright TC-PRODUCT-SUP-001: `Expected: false Received: true` tại `admin-product.spec.js:357`.
- Playwright TC-PRODUCT-SUP-007: `API must reject 256-char name` tại `admin-product.spec.js:409`.

## Suggested Labels

`type: bug`, `module: admin-product`, `severity: major`, `priority: P1`, `status: new`, `found-by: test-case`, `requirement: FR-15`
