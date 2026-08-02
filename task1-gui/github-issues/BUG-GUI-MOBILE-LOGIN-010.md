# Kiểm tra Touch Target Size của nút Sign In trên màn hình cảm ứng Mobile.

**Local ID:** `BUG-GUI-MOBILE-LOGIN-010`
**Status:** `PENDING_EXTERNAL_ACTION`
**Severity:** `Medium`
**Reporter:** Đặng Đăng Khoa (23127207)
**Environment:** Google Chrome 150.0.7871.187 / Windows 10.0.26200

## Steps

1. Start EShop and open `Screen Login`.
2. Execute `GUI-MOBILE-LOGIN-010`: Kiểm tra Touch Target Size của nút Sign In trên màn hình cảm ứng Mobile.
3. Observe the UI and request/dialog state.

## Expected

Kích thước vùng bấm đạt tối thiểu 44x44 dp theo tiêu chuẩn Mobile Accessibility.

## Actual

Sign In touch target bounding box={"x":24,"y":320,"width":342,"height":39} CSS px.

## Evidence

![BUG-GUI-MOBILE-LOGIN-010](https://raw.githubusercontent.com/trngnneee/eshop-sut/HW3-Khoa/task1-gui/evidence/executed-chrome/034-mobile-login-baseline.png)

Local file: `evidence/executed-chrome/034-mobile-login-baseline.png`

## Duplicate-search disposition

PENDING_EXTERNAL_ACTION
