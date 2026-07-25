## Title
[Minor] Đăng ký thành công không có thông báo xác nhận

## Description
Đăng ký thành công navigate thẳng `/login` không message (Register.jsx:25).

## Steps to Reproduce
1. Đăng ký hợp lệ, quan sát có thông báo trước khi sang login.

## Expected Result
Có toast/message "Đăng ký thành công, mời đăng nhập".

## Actual Result
- (GUI-IA04-17) Đăng ký thành công điều hướng thẳng sang /login không có thông báo xác nhận ("Đăng ký thành công, mời đăng nhập").

## Environment
Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)
GUI-IA04-17

## Requirement
Heuristic (action feedback)

## Severity
Minor — Chuyển trang đột ngột, người dùng không chắc đã thành công.

## Screenshot
![GUI-IA04-17](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965779/eshop-hw03/gui-checklist/GUI-IA04-17.png)