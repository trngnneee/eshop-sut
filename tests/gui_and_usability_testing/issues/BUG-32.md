## Title
[Minor] Đăng ký thiếu field "Xác nhận mật khẩu"

## Description
Form không có field xác nhận mật khẩu (Register.jsx:35-81).

## Steps to Reproduce
1. Mở `/register`, tìm field xác nhận mật khẩu.

## Expected Result
Có field xác nhận và kiểm tra khớp.

## Actual Result
- (GUI-IA02-13) Form đăng ký KHÔNG có field "Xác nhận mật khẩu" — thiếu cơ chế kiểm tra khớp mật khẩu.

## Environment
Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)
GUI-IA02-13

## Requirement
Heuristic (confirmation field)

## Severity
Minor — Không phát hiện lỗi gõ mật khẩu.

## Screenshot
![GUI-IA02-13](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965728/eshop-hw03/gui-checklist/GUI-IA02-13.png)