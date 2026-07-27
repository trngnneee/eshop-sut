## Title
[Minor] Lỗi form đăng nhập đặt DƯỚI nút submit (ngược FR-22)

## Description
Lỗi đăng nhập render dưới nút submit (Login.jsx:66); Quên MK/Hồ sơ còn dùng alert().

## Steps to Reproduce
1. Mở `/login`, nhập sai và submit, quan sát vị trí lỗi so với nút.

## Expected Result
Lỗi hiển thị trong trang, phía TRÊN nút submit.

## Actual Result
- (GUI-IA02-04) Thông báo lỗi đăng nhập nằm DƯỚI nút submit (errY=517, btnY=425) — ngược yêu cầu FR-22 (lỗi phải phía TRÊN nút submit). Quên MK/Hồ sơ còn dùng alert() native.

## Environment
Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)
GUI-IA02-04

## Requirement
FR-22 (message placement)

## Severity
Minor — Vi phạm quy tắc đặt lỗi phía trên nút submit.

## Screenshot
![GUI-IA02-04](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965714/eshop-hw03/gui-checklist/GUI-IA02-04.png)