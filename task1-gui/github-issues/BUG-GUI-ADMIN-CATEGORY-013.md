# Kiểm tra ngăn chặn Double Submit khi nhấp liên tục nút Thêm mới.

**Local ID:** `BUG-GUI-ADMIN-CATEGORY-013`
**Status:** `PENDING_EXTERNAL_ACTION`
**Severity:** `Medium`
**Reporter:** Đặng Đăng Khoa (23127207)
**Environment:** Google Chrome 150.0.7871.187 / Windows 10.0.26200

## Steps

1. Start EShop and open `/ (Tab categories)`.
2. Execute `GUI-ADMIN-CATEGORY-013`: Kiểm tra ngăn chặn Double Submit khi nhấp liên tục nút Thêm mới.
3. Observe the UI and request/dialog state.

## Expected

Nút Thêm mới tự động disable trong thời gian chờ gửi request.

## Actual

Rapid double click generated 2 POST request(s); button disabled after completion=false.

## Evidence

![BUG-GUI-ADMIN-CATEGORY-013](https://raw.githubusercontent.com/trngnneee/eshop-sut/HW3-Khoa/task1-gui/evidence/executed-chrome/033-admin-category-double-submit.png)

Local file: `evidence/executed-chrome/033-admin-category-double-submit.png`

## Duplicate-search disposition

PENDING_EXTERNAL_ACTION
