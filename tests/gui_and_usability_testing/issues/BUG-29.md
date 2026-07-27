## Title
[Minor] Quên mật khẩu 2 bước thiếu Step Indicator

## Description
Luồng 2 bước không có chỉ dẫn bước (ForgotPassword.jsx:46-98).

## Steps to Reproduce
1. Đi qua bước 1 → bước 2, tìm chỉ dẫn bước.

## Expected Result
Hiển thị "Bước 1/2", "Bước 2/2" hoặc tương đương.

## Actual Result
- (GUI-IA02-05) Luồng Quên mật khẩu 2 bước không có Step Indicator ở cả bước 1 lẫn bước 2 (không có chỉ dẫn "Bước 1/2", "Bước 2/2").

## Environment
Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)
GUI-IA02-05

## Requirement
FR-22 (step indicator)

## Severity
Minor — Người dùng không biết đang ở bước nào.

## Screenshot
![GUI-IA02-05](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965716/eshop-hw03/gui-checklist/GUI-IA02-05.png)