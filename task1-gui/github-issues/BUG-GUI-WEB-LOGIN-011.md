# Kiểm tra thứ tự Tab (Keyboard Navigation) và Visible Focus.

**Local ID:** `BUG-GUI-WEB-LOGIN-011`
**Status:** `EXISTING_ISSUE_REUSED`
**Severity:** `Medium`
**Reporter:** Đặng Đăng Khoa (23127207)
**Environment:** Google Chrome 150.0.7871.187 / Windows 10.0.26200

## Steps

1. Start EShop and open `/login`.
2. Execute `GUI-WEB-LOGIN-011`: Kiểm tra thứ tự Tab (Keyboard Navigation) và Visible Focus.
3. Observe the UI and request/dialog state.

## Expected

Ấn phím Tab di chuyển tuần tự qua các input và button có viền focus rõ ràng.

## Actual

First eight Tab targets: BUTTON:Sign In[1] > A:EShop[auto] > A:Giỏ hàng[auto] > A:Đăng nhập[auto] > A:Đăng ký[auto] > INPUT:text[auto] > INPUT:text[auto] > A:Quên mật khẩu?[auto]. Positive-tabindex submit precedes inputs=true.

## Evidence

![BUG-GUI-WEB-LOGIN-011](https://raw.githubusercontent.com/trngnneee/eshop-sut/HW3-Khoa/task1-gui/evidence/executed-chrome/007-web-login-keyboard-focus.png)

Local file: `evidence/executed-chrome/007-web-login-keyboard-focus.png`

## Duplicate-search disposition

https://github.com/trngnneee/eshop-sut/issues/201
