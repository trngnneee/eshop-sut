## Title
[Minor] Đơn vị tiền "VND" không nhất quán với ký hiệu ₫

## Description
Card trang chủ hiển thị "30,000,000 VND" (Home.jsx:87-89) trong khi các màn khác dùng ₫.

## Steps to Reproduce
1. Mở `/`, quan sát đơn vị tiền trên card.

## Expected Result
Dùng ký hiệu ₫ thống nhất toàn app.

## Actual Result
- (GUI-IA01-06) Giá trên card trang chủ hiển thị "30,000,000 VND" dùng "VND", trong khi các màn khác dùng ký hiệu ₫ — không nhất quán.

## Environment
Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)
GUI-IA01-06

## Requirement
FR-21 (đơn vị tiền)

## Severity
Minor — Không nhất quán đơn vị tiền theo FR-21.

## Screenshot
![GUI-IA01-06](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965695/eshop-hw03/gui-checklist/GUI-IA01-06.png)