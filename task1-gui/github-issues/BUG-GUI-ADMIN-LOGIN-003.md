# Kiểm tra thông báo khi nhập sai mật khẩu Admin.

**Local ID:** `BUG-GUI-ADMIN-LOGIN-003`
**Status:** `PENDING_EXTERNAL_ACTION`
**Severity:** `Medium`
**Reporter:** Đặng Đăng Khoa (23127207)
**Environment:** Google Chrome 150.0.7871.187 / Windows 10.0.26200

## Steps

1. Start EShop and open `/ (Unauth)`.
2. Execute `GUI-ADMIN-LOGIN-003`: Kiểm tra thông báo khi nhập sai mật khẩu Admin.
3. Observe the UI and request/dialog state.

## Expected

Hiển thị thông báo lỗi dạng inline banner bên trong form admin.

## Actual

Native browser dialog captured with 'Đăng nhập thất bại'; inline feedback count=0.

## Evidence

![BUG-GUI-ADMIN-LOGIN-003](https://raw.githubusercontent.com/trngnneee/eshop-sut/HW3-Khoa/task1-gui/evidence/executed-chrome/019-admin-login-invalid-dialog.png)

Local file: `evidence/executed-chrome/019-admin-login-invalid-dialog.png`

## Duplicate-search disposition

PENDING_EXTERNAL_ACTION
