# Kiểm tra chỉ báo Loading khi đang tải dữ liệu danh mục.

**Local ID:** `BUG-GUI-ADMIN-CATEGORY-010`
**Status:** `PENDING_EXTERNAL_ACTION`
**Severity:** `Medium`
**Reporter:** Đặng Đăng Khoa (23127207)
**Environment:** Google Chrome 150.0.7871.187 / Windows 10.0.26200

## Steps

1. Start EShop and open `/ (Tab categories)`.
2. Execute `GUI-ADMIN-CATEGORY-010`: Kiểm tra chỉ báo Loading khi đang tải dữ liệu danh mục.
3. Observe the UI and request/dialog state.

## Expected

Hiển thị spinner hoặc skeleton loading khi fetch API.

## Actual

During a 2.5-second category delay, loading indicator count=0.

## Evidence

![BUG-GUI-ADMIN-CATEGORY-010](https://raw.githubusercontent.com/trngnneee/eshop-sut/HW3-Khoa/task1-gui/evidence/executed-chrome/030-admin-category-loading.png)

Local file: `evidence/executed-chrome/030-admin-category-loading.png`

## Duplicate-search disposition

PENDING_EXTERNAL_ACTION
