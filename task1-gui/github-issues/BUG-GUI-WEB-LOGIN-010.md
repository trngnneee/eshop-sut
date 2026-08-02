# Kiểm tra phản hồi sau đúng ba lần đăng nhập sai liên tiếp.

**Local ID:** `BUG-GUI-WEB-LOGIN-010`
**Status:** `EXISTING_ISSUE_REUSED`
**Severity:** `High`
**Reporter:** Đặng Đăng Khoa (23127207)
**Environment:** Google Chrome 150.0.7871.187 / Windows 10.0.26200

## Steps

1. Start EShop and open `/login`.
2. Execute `GUI-WEB-LOGIN-010`: Kiểm tra phản hồi sau đúng ba lần đăng nhập sai liên tiếp.
3. Observe the UI and request/dialog state.

## Expected

Sau lần sai thứ ba, backend khóa 30 giây và UI hiển thị trạng thái khóa phù hợp mà không lộ chi tiết tài khoản.

## Actual

Three wrong attempts returned HTTP 401/401/403; UI still says 'Đăng nhập thất bại. Vui lòng kiểm tra lại.'.

## Evidence

![BUG-GUI-WEB-LOGIN-010](https://raw.githubusercontent.com/trngnneee/eshop-sut/HW3-Khoa/task1-gui/evidence/executed-chrome/006-web-login-lockout-feedback.png)

Local file: `evidence/executed-chrome/006-web-login-lockout-feedback.png`

## Duplicate-search disposition

https://github.com/trngnneee/eshop-sut/issues/238
