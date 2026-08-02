# Kiểm tra thêm mới danh mục với tên rỗng.

**Local ID:** `BUG-GUI-ADMIN-CATEGORY-004`
**Status:** `PENDING_EXTERNAL_ACTION`
**Severity:** `High`
**Reporter:** Đặng Đăng Khoa (23127207)
**Environment:** Google Chrome 150.0.7871.187 / Windows 10.0.26200

## Steps

1. Start EShop and open `/ (Tab categories)`.
2. Execute `GUI-ADMIN-CATEGORY-004`: Kiểm tra thêm mới danh mục với tên rỗng.
3. Observe the UI and request/dialog state.

## Expected

Form có thuộc tính required ngăn chặn submit tên danh mục rỗng.

## Actual

required attribute='null'; empty POST observed=true; payload={"name":""}.

## Evidence

![BUG-GUI-ADMIN-CATEGORY-004](https://raw.githubusercontent.com/trngnneee/eshop-sut/HW3-Khoa/task1-gui/evidence/executed-chrome/026-admin-category-empty.png)

Local file: `evidence/executed-chrome/026-admin-category-empty.png`

## Duplicate-search disposition

PENDING_EXTERNAL_ACTION
