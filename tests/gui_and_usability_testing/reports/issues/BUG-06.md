## Title
[Major] Heading trang Đăng nhập ghi sai thành "Đăng Ký"

## Description
Trang `/login` hiển thị heading "Đăng Ký" (Login.jsx:24) sai với chức năng.

## Steps to Reproduce
1. Mở `/login`.
2. Đọc heading đầu form.

## Expected Result
Heading là "Đăng Nhập".

## Actual Result
- (GUI-IA01-11) Heading trang /login là "Đăng Ký" — sai chức năng (ghi "Đăng Ký" trên trang Đăng nhập).

## Environment
Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)
GUI-IA01-11

## Requirement
FR-21 (tiêu đề trang)

## Severity
Major — Gây nhầm lẫn chức năng trang.

## Screenshot
![GUI-IA01-11](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965701/eshop-hw03/gui-checklist/GUI-IA01-11.png)