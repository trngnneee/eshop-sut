# Bug Report #15 — Ready for GitHub Issue

**Title:** [BUG][Admin Product] Web Admin product CRUD UI not implemented (FR-15)

**Found by Test Case:** TC-PRODUCT-001 … TC-PRODUCT-032, TC-PRODUCT-SUP-002, TC-PRODUCT-SUP-005 … TC-PRODUCT-SUP-011  
**Requirement:** FR-15, FR-12  
**Severity / Priority:** Critical / P1  
**Environment:** Windows 11 · Chromium (Playwright) · `http://localhost:5173` · `http://localhost:3000`  
**Reported by:** QA / Playwright automation (`npm run test:fr15`)  
**Date:** 2026-06-29

**Classification:** Type: Functional | Severity: Critical | Priority: P1

## Description

FR-15 yêu cầu Admin **Thêm / Xem / Sửa / Xóa** sản phẩm qua phân hệ Web Admin (`http://localhost:5174` theo README). Trong repo hiện tại:

- `frontend-web/src/App.jsx` không có route `/admin/products` (chỉ có route người dùng: `/`, `/login`, `/cart`, …).
- Không có thư mục `web-admin` / `frontend-admin` trong workspace.
- Truy cập `/admin/products` trên `frontend-web` không render form quản lý sản phẩm — toàn bộ test UI CRUD không thể thực thi.

## Steps to Reproduce

1. Khởi động backend và `frontend-web` (`npm run dev` tại port 5173).
2. Đăng nhập admin (hoặc dùng API token).
3. Mở `http://localhost:5173/admin/products`.
4. Tìm form Thêm/Sửa sản phẩm và bảng danh sách.

## Expected Result

- Phân hệ Web Admin có màn hình Quản lý Sản phẩm với CRUD đầy đủ.
- Route được bảo vệ: user thường không truy cập được (FR-12).

## Actual Result

- Không có route hay component quản lý sản phẩm trong `frontend-web`.
- URL `/admin/products` không có UI tương ứng; automation timeout khi chờ form admin.

## Evidence

- Playwright: 32 EP/BVA tests + 7 SUP UI tests fail (không tìm thấy admin product page).
- `frontend-web/src/App.jsx` lines 50–59 — không có `/admin/products`.
- README §1: Web Admin `http://localhost:5174` — component chưa có trong repo.
- `test-results/admin-product-FR-15-*/error-context.md`

## Suggested Labels

`type: bug`, `module: admin-product`, `severity: critical`, `priority: P1`, `status: new`, `found-by: test-case`, `requirement: FR-15`
