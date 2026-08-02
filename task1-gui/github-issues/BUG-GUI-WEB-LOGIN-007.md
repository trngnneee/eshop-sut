# Kiểm tra link Quên mật khẩu.

**Local ID:** `BUG-GUI-WEB-LOGIN-007`
**Status:** `EXISTING_ISSUE_REUSED`
**Severity:** `Low`
**Reporter:** Đặng Đăng Khoa (23127207)
**Environment:** Google Chrome 150.0.7871.187 / Windows 10.0.26200

## Steps

1. Start EShop and open `/login`.
2. Execute `GUI-WEB-LOGIN-007`: Kiểm tra link Quên mật khẩu.
3. Observe the UI and request/dialog state.

## Expected

Bấm vào link 'Quên mật khẩu?' chuyển hướng mượt mà SPA không reload trang.

## Actual

Reached /forgot-password; SPA marker lost due to full document navigation.

## Evidence

![BUG-GUI-WEB-LOGIN-007](https://raw.githubusercontent.com/trngnneee/eshop-sut/HW3-Khoa/task1-gui/evidence/executed-chrome/004-web-login-forgot-navigation.png)

Local file: `evidence/executed-chrome/004-web-login-forgot-navigation.png`

## Duplicate-search disposition

https://github.com/trngnneee/eshop-sut/issues/230
