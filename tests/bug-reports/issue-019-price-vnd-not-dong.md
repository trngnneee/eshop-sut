# Bug Report #19 — Ready for GitHub Issue

**Title:** [BUG][Product] Price displayed as VND instead of ₫ (FR-21)

**Found by Test Case:** TC-PRODUCT-SUP-011  
**Requirement:** FR-05, FR-21  
**Severity / Priority:** Minor / P2  
**Environment:** `http://localhost:5173` · Playwright `npm run test:fr15`  
**Reported by:** QA / spec review + automation design  
**Date:** 2026-06-29

**Classification:** Type: UI/UX | Severity: Minor | Priority: P2

## Description

FR-05 và FR-21 yêu cầu giá hiển thị đơn vị **₫** với phân cách hàng nghìn. Trang chủ (và danh sách sản phẩm) dùng hậu tố **VND** thay vì ký hiệu ₫.

## Steps to Reproduce

1. Mở trang chủ `http://localhost:5173/`.
2. Quan sát giá sản phẩm (ví dụ `199.000` hoặc `30.000.000`).
3. TC-PRODUCT-SUP-011: sau khi có admin list UI, kiểm tra cột giá trong bảng sản phẩm.

## Expected Result

Giá hiển thị dạng `199.000 ₫` (ký hiệu ₫, phân cách hàng nghìn).

## Actual Result

`Home.jsx:87-88` — `{Number(p.price).toLocaleString()} VND` (ví dụ `30.000.000 VND`).

## Evidence

- `frontend-web/src/pages/Home.jsx` line 88
- TC-PRODUCT-SUP-011 expects `listShowsCurrencySymbol()` → ký hiệu ₫
- Automation blocked by #15, #18; định dạng sai xác nhận qua code review trang chủ

## Suggested Labels

`type: bug`, `module: product`, `severity: minor`, `priority: P2`, `status: new`, `found-by: test-case`, `requirement: FR-21`
