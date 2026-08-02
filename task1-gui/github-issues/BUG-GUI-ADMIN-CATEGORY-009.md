# Kiểm tra giao diện khi danh sách danh mục rỗng.

**Local ID:** `BUG-GUI-ADMIN-CATEGORY-009`
**Status:** `PENDING_EXTERNAL_ACTION`
**Severity:** `Low`
**Reporter:** Đặng Đăng Khoa (23127207)
**Environment:** Google Chrome 150.0.7871.187 / Windows 10.0.26200

## Steps

1. Start EShop and open `/ (Tab categories)`.
2. Execute `GUI-ADMIN-CATEGORY-009`: Kiểm tra giao diện khi danh sách danh mục rỗng.
3. Observe the UI and request/dialog state.

## Expected

Hiển thị thông báo hoặc minh họa 'Chưa có danh mục nào'.

## Actual

Mocked empty category response rendered rows=0; empty-state message count=0.

## Evidence

![BUG-GUI-ADMIN-CATEGORY-009](https://raw.githubusercontent.com/trngnneee/eshop-sut/HW3-Khoa/task1-gui/evidence/executed-chrome/029-admin-category-empty-state.png)

Local file: `evidence/executed-chrome/029-admin-category-empty-state.png`

## Duplicate-search disposition

PENDING_EXTERNAL_ACTION
