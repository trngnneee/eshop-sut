# Kiểm tra thông báo khi tài khoản user thường đăng nhập vào Admin.

**Local ID:** `BUG-GUI-ADMIN-LOGIN-004`
**Status:** `PENDING_EXTERNAL_ACTION`
**Severity:** `Medium`
**Reporter:** Đặng Đăng Khoa (23127207)
**Environment:** Google Chrome 150.0.7871.187 / Windows 10.0.26200

## Steps

1. Start EShop and open `/ (Unauth)`.
2. Execute `GUI-ADMIN-LOGIN-004`: Kiểm tra thông báo khi tài khoản user thường đăng nhập vào Admin.
3. Observe the UI and request/dialog state.

## Expected

Hiển thị thông báo lỗi phân quyền rõ ràng trên giao diện.

## Actual

Non-admin login produced native dialog 'Bạn không phải là admin!'; inline feedback count=0.

## Evidence

![BUG-GUI-ADMIN-LOGIN-004](https://raw.githubusercontent.com/trngnneee/eshop-sut/HW3-Khoa/task1-gui/evidence/executed-chrome/020-admin-login-nonadmin-dialog.png)

Local file: `evidence/executed-chrome/020-admin-login-nonadmin-dialog.png`

## Duplicate-search disposition

PENDING_EXTERNAL_ACTION
