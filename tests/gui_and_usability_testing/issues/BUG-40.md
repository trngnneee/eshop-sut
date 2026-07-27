## Title
[Minor] Back ở bước 2 Quên mật khẩu làm mất tiến trình

## Description
Bước là state không gắn URL (ForgotPassword.jsx:8) → Back rời trang.

## Steps to Reproduce
1. Vào bước 2, bấm Back của trình duyệt.

## Expected Result
Back quay về bước 1 hoặc giữ tiến trình.

## Actual Result
- (GUI-IA03-11) Ở bước 2, bấm Back trình duyệt rời hẳn trang Quên mật khẩu (URL: "about:blank") — step là state không gắn URL nên mất toàn bộ tiến trình OTP.

## Environment
Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)
GUI-IA03-11

## Requirement
Heuristic (browser back-button)

## Severity
Minor — Bấm Back rời hẳn trang, mất OTP đã lấy.

## Screenshot
![GUI-IA03-11](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965747/eshop-hw03/gui-checklist/GUI-IA03-11.png)