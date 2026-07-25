## Title
[Minor] Nút phụ "← Quay lại" trùng style nút chính

## Description
Nút "Đặt lại mật khẩu" và "← Quay lại" cùng nền xanh lá, full-width (ForgotPassword.jsx:91-96).

## Steps to Reproduce
1. Vào bước 2 của `/forgot-password`.
2. Quan sát 2 nút.

## Expected Result
Nút phụ có style thứ cấp, phân biệt rõ với nút submit.

## Actual Result
- (GUI-IA01-05) Nút chính "Đặt lại mật khẩu" (rgb(22, 163, 74)) và nút phụ "← Quay lại" (rgb(22, 163, 74)) cùng nền xanh lá, full-width — không phân biệt được thị giác.

## Environment
Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)
GUI-IA01-05

## Requirement
Heuristic (visual hierarchy)

## Severity
Minor — Dễ bấm nhầm nút hành động chính.

## Screenshot
![GUI-IA01-05](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965693/eshop-hw03/gui-checklist/GUI-IA01-05.png)