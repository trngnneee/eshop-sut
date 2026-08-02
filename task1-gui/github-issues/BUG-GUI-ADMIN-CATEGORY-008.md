# Kiểm tra báo lỗi khi xóa danh mục đang có sản phẩm.

**Local ID:** `BUG-GUI-ADMIN-CATEGORY-008`
**Status:** `PENDING_EXTERNAL_ACTION`
**Severity:** `High`
**Reporter:** Đặng Đăng Khoa (23127207)
**Environment:** Google Chrome 150.0.7871.187 / Windows 10.0.26200

## Steps

1. Start EShop and open `/ (Tab categories)`.
2. Execute `GUI-ADMIN-CATEGORY-008`: Kiểm tra báo lỗi khi xóa danh mục đang có sản phẩm.
3. Observe the UI and request/dialog state.

## Expected

Không xóa category đang được product tham chiếu; UI hiển thị lỗi và category vẫn còn.

## Actual

Category referenced by synthetic product remained=false; error dialog=NONE. Backend allowed deletion=true.

## Evidence

![BUG-GUI-ADMIN-CATEGORY-008](https://raw.githubusercontent.com/trngnneee/eshop-sut/HW3-Khoa/task1-gui/evidence/executed-chrome/028-admin-category-delete-in-use.png)

Local file: `evidence/executed-chrome/028-admin-category-delete-in-use.png`

## Duplicate-search disposition

PENDING_EXTERNAL_ACTION
