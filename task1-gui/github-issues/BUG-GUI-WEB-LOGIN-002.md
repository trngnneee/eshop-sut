# Kiểm tra nhãn label và type của trường Email.

**Local ID:** `BUG-GUI-WEB-LOGIN-002`
**Status:** `EXISTING_ISSUE_REUSED`
**Severity:** `Medium`
**Reporter:** Đặng Đăng Khoa (23127207)
**Environment:** Google Chrome 150.0.7871.187 / Windows 10.0.26200

## Steps

1. Start EShop and open `/login`.
2. Execute `GUI-WEB-LOGIN-002`: Kiểm tra nhãn label và type của trường Email.
3. Observe the UI and request/dialog state.

## Expected

Nhãn hiển thị 'Email', input có type='email'.

## Actual

First label 'Username', input type 'text'.

## Evidence

![BUG-GUI-WEB-LOGIN-002](https://raw.githubusercontent.com/trngnneee/eshop-sut/HW3-Khoa/task1-gui/evidence/executed-chrome/001-web-login-baseline.png)

Local file: `evidence/executed-chrome/001-web-login-baseline.png`

## Duplicate-search disposition

https://github.com/trngnneee/eshop-sut/issues/203
