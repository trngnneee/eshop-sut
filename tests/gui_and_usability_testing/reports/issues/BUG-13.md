## Title
[Major] Không có route guard cho /checkout

## Description
Truy cập thẳng `/checkout` khi giỏ trống và chưa đăng nhập vẫn hiển thị form (tổng 0 ₫), không redirect.

## Steps to Reproduce
1. Đăng xuất, giỏ trống.
2. Truy cập thẳng `localhost:5173/checkout`.

## Expected Result
Giỏ trống → về giỏ hàng; chưa login → về đăng nhập.

## Actual Result
- (GUI-IA03-12) Vào thẳng /checkout khi giỏ trống & chưa đăng nhập vẫn hiển thị form thanh toán (tổng 0 ₫), không bị redirect — thiếu route guard.

## Environment
Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)
GUI-IA03-12

## Requirement
Heuristic (route guarding)

## Severity
Major — Vào thẳng thanh toán khi giỏ trống/chưa đăng nhập — luồng nghiệp vụ sai.

## Screenshot
![GUI-IA03-12](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965749/eshop-hw03/gui-checklist/GUI-IA03-12.png)