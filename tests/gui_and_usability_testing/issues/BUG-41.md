## Title
[Minor] /profile khi chưa đăng nhập là ngõ cụt

## Description
Chỉ hiển thị text "Vui lòng đăng nhập" (Profile.jsx:109), không link/redirect.

## Steps to Reproduce
1. Đăng xuất, truy cập `/profile`.

## Expected Result
Có link "Đăng nhập" hoặc tự redirect.

## Actual Result
- (GUI-IA03-13) /profile khi chưa đăng nhập chỉ hiển thị text trần "Vui lòng đăng nhập", không có link tới trang đăng nhập và không tự redirect — ngõ cụt điều hướng.

## Environment
Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)
GUI-IA03-13

## Requirement
Heuristic (dead-end navigation)

## Severity
Minor — Chỉ có text, không có đường tới đăng nhập.

## Screenshot
![GUI-IA03-13](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965750/eshop-hw03/gui-checklist/GUI-IA03-13.png)