## Title
[Minor] Tên sản phẩm bị cắt (truncate) không có tooltip xem đầy đủ

## Description
Class `truncate` (Home.jsx:86) cắt tên nhưng không có thuộc tính `title`.

## Steps to Reproduce
1. Seed sản phẩm tên dài, mở `/`, rê chuột lên tên.

## Expected Result
Có tooltip/title hiển thị tên đầy đủ.

## Actual Result
- (GUI-IA01-16) Tên sản phẩm dùng class "truncate" để cắt gọn nhưng KHÔNG có thuộc tính title/tooltip → không có cách xem đầy đủ tên khi bị cắt.

## Environment
Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)
GUI-IA01-16

## Requirement
Heuristic (text overflow)

## Severity
Minor — Không xem được tên đầy đủ khi bị cắt.

## Screenshot
![GUI-IA01-16](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965707/eshop-hw03/gui-checklist/GUI-IA01-16.png)