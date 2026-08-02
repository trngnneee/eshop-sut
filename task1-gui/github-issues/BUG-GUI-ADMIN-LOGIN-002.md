# Kiểm tra thẻ label liên kết với ô Email và Password.

**Local ID:** `BUG-GUI-ADMIN-LOGIN-002`
**Status:** `PENDING_EXTERNAL_ACTION`
**Severity:** `Medium`
**Reporter:** Đặng Đăng Khoa (23127207)
**Environment:** Google Chrome 150.0.7871.187 / Windows 10.0.26200

## Steps

1. Start EShop and open `/ (Unauth)`.
2. Execute `GUI-ADMIN-LOGIN-002`: Kiểm tra thẻ label liên kết với ô Email và Password.
3. Observe the UI and request/dialog state.

## Expected

Mỗi ô input đều có thẻ <label> liên kết tương ứng.

## Actual

Admin login form contains 0 label elements for two inputs.

## Evidence

![BUG-GUI-ADMIN-LOGIN-002](https://raw.githubusercontent.com/trngnneee/eshop-sut/HW3-Khoa/task1-gui/evidence/executed-chrome/018-admin-login-baseline.png)

Local file: `evidence/executed-chrome/018-admin-login-baseline.png`

## Duplicate-search disposition

PENDING_EXTERNAL_ACTION
