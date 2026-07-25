## Title
[Major] tabindex=1 trên nút Đăng nhập phá thứ tự Tab

## Description
Nút submit form Đăng nhập có `tabIndex={1}` (Login.jsx:56) nên được focus trước các input.

## Steps to Reproduce
1. Mở `/login`.
2. Nhấn Tab liên tục từ đầu trang, ghi lại thứ tự focus.

## Expected Result
Tab đi lần lượt các ô nhập rồi mới tới nút submit.

## Actual Result
- (GUI-IA01-13) Nút submit form Đăng nhập có tabindex="1" → được focus TRƯỚC các ô input, phá thứ tự Tab tự nhiên.

## Environment
Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)
GUI-IA01-13

## Requirement
FR-21 (tab order)

## Severity
Major — Bàn phím focus vào nút submit trước các ô nhập — cản trở thao tác keyboard/accessibility.

## Screenshot
![GUI-IA01-13](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965704/eshop-hw03/gui-checklist/GUI-IA01-13.png)