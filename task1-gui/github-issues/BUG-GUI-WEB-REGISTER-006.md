# Kiểm tra đăng ký với Email đã tồn tại trong database.

**Local ID:** `BUG-GUI-WEB-REGISTER-006`
**Status:** `EXISTING_ISSUE_REUSED`
**Severity:** `High`
**Reporter:** Đặng Đăng Khoa (23127207)
**Environment:** Google Chrome 150.0.7871.187 / Windows 10.0.26200

## Steps

1. Start EShop and open `/register`.
2. Execute `GUI-WEB-REGISTER-006`: Kiểm tra đăng ký với Email đã tồn tại trong database.
3. Observe the UI and request/dialog state.

## Expected

Hiển thị thông báo lỗi từ backend 'User already exists' hoặc 'Email đã được sử dụng'.

## Actual

Second registration for the same email returned HTTP 200 and navigated as success.

## Evidence

![BUG-GUI-WEB-REGISTER-006](https://raw.githubusercontent.com/trngnneee/eshop-sut/HW3-Khoa/task1-gui/evidence/executed-chrome/013-web-register-duplicate.png)

Local file: `evidence/executed-chrome/013-web-register-duplicate.png`

## Duplicate-search disposition

https://github.com/trngnneee/eshop-sut/issues/117
