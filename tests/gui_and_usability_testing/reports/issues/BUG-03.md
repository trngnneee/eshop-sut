## Title
[Major] Ô mật khẩu trang Đăng nhập dùng type=text (không che ký tự)

## Description
Ô Mật khẩu ở form Đăng nhập dùng `type="text"` (Login.jsx:39-45) nên ký tự hiển thị rõ.

## Steps to Reproduce
1. Mở `/login`.
2. Gõ vào ô Mật khẩu.
3. Quan sát ký tự hiển thị.

## Expected Result
Ký tự mật khẩu hiển thị dạng chấm tròn (`type="password"`).

## Actual Result
- (GUI-IA02-03) Ô Mật khẩu trên form Đăng nhập có type="text" → ký tự mật khẩu hiển thị rõ, không được che.

## Environment
Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)
GUI-IA02-03

## Requirement
FR-22 (password masking)

## Severity
Major — Mật khẩu hiển thị rõ trên màn hình — rủi ro lộ thông tin đăng nhập.

## Screenshot
![GUI-IA02-03](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965713/eshop-hw03/gui-checklist/GUI-IA02-03.png)