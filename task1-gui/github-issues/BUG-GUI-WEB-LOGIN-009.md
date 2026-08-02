# Kiểm tra nhãn và giao diện nút Đăng nhập.

**Local ID:** `BUG-GUI-WEB-LOGIN-009`
**Status:** `EXISTING_ISSUE_REUSED`
**Severity:** `Medium`
**Reporter:** Đặng Đăng Khoa (23127207)
**Environment:** Google Chrome 150.0.7871.187 / Windows 10.0.26200

## Steps

1. Start EShop and open `/login`.
2. Execute `GUI-WEB-LOGIN-009`: Kiểm tra nhãn và giao diện nút Đăng nhập.
3. Observe the UI and request/dialog state.

## Expected

Nút đăng nhập có nhãn tiếng Việt 'Đăng nhập', tabIndex mặc định.

## Actual

Submit button text is 'Sign In'.

## Evidence

![BUG-GUI-WEB-LOGIN-009](https://raw.githubusercontent.com/trngnneee/eshop-sut/HW3-Khoa/task1-gui/evidence/executed-chrome/001-web-login-baseline.png)

Local file: `evidence/executed-chrome/001-web-login-baseline.png`

## Duplicate-search disposition

https://github.com/trngnneee/eshop-sut/issues/198
