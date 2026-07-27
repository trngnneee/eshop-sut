## Title
[Minor] Navbar không highlight trang đang chọn

## Description
Link navbar chỉ có `hover:underline`, không có active state (App.jsx:22-37).

## Steps to Reproduce
1. Điều hướng tới `/cart`, quan sát link "Giỏ hàng".

## Expected Result
Link trang hiện tại có style active.

## Actual Result
- (GUI-IA03-01) Ở /cart, link "Giỏ hàng" trên navbar chỉ có class "hover:underline" (chỉ hover:underline), không có active-state (aria-current/đậm/đổi màu) để chỉ mục đang chọn.

## Environment
Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)
GUI-IA03-01

## Requirement
FR-23 (active highlight)

## Severity
Minor — Người dùng không biết đang ở mục nào.

## Screenshot
![GUI-IA03-01](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965731/eshop-hw03/gui-checklist/GUI-IA03-01.png)