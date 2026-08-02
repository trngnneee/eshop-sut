# Kiểm tra popup xác nhận trước khi Xóa danh mục.

**Local ID:** `BUG-GUI-ADMIN-CATEGORY-006`
**Status:** `PENDING_EXTERNAL_ACTION`
**Severity:** `High`
**Reporter:** Đặng Đăng Khoa (23127207)
**Environment:** Google Chrome 150.0.7871.187 / Windows 10.0.26200

## Steps

1. Start EShop and open `/ (Tab categories)`.
2. Execute `GUI-ADMIN-CATEGORY-006`: Kiểm tra popup xác nhận trước khi Xóa danh mục.
3. Observe the UI and request/dialog state.

## Expected

Bấm nút 'Xóa' hiển thị modal xác nhận 'Bạn có chắc chắn muốn xóa danh mục này?'.

## Actual

Delete confirmation dialog observed=false.

## Evidence

![BUG-GUI-ADMIN-CATEGORY-006](https://raw.githubusercontent.com/trngnneee/eshop-sut/HW3-Khoa/task1-gui/evidence/executed-chrome/027-admin-category-delete.png)

Local file: `evidence/executed-chrome/027-admin-category-delete.png`

## Duplicate-search disposition

PENDING_EXTERNAL_ACTION
