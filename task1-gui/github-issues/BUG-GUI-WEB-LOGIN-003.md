# Kiểm tra ẩn/hiển thị ký tự trường Mật khẩu.

**Local ID:** `BUG-GUI-WEB-LOGIN-003`
**Status:** `EXISTING_ISSUE_REUSED`
**Severity:** `Critical`
**Reporter:** Đặng Đăng Khoa (23127207)
**Environment:** Google Chrome 150.0.7871.187 / Windows 10.0.26200

## Steps

1. Start EShop and open `/login`.
2. Execute `GUI-WEB-LOGIN-003`: Kiểm tra ẩn/hiển thị ký tự trường Mật khẩu.
3. Observe the UI and request/dialog state.

## Expected

Ký tự mật khẩu khi nhập vào bị ẩn dạng dấu chấm (type='password').

## Actual

Password input type is 'text'.

## Evidence

![BUG-GUI-WEB-LOGIN-003](https://raw.githubusercontent.com/trngnneee/eshop-sut/HW3-Khoa/task1-gui/evidence/executed-chrome/001-web-login-baseline.png)

Local file: `evidence/executed-chrome/001-web-login-baseline.png`

## Duplicate-search disposition

https://github.com/trngnneee/eshop-sut/issues/37
