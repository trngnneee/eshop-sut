## Title
[Minor] Ảnh sản phẩm có alt rỗng

## Description
Ảnh card dùng `alt=""` (Home.jsx:81-85).

## Steps to Reproduce
1. Mở `/`, kiểm tra thuộc tính alt của ảnh card (DevTools).

## Expected Result
Ảnh có alt = tên sản phẩm, không rỗng.

## Actual Result
- (GUI-IA04-07) Ảnh sản phẩm trên trang chủ có alt="" (rỗng) — thiếu văn bản thay thế mô tả.

## Environment
Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)
GUI-IA04-07

## Requirement
FR-24 (image alt-text)

## Severity
Minor — Screen reader không mô tả được ảnh (FR-24).

## Screenshot
![GUI-IA04-07](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965763/eshop-hw03/gui-checklist/GUI-IA04-07.png)