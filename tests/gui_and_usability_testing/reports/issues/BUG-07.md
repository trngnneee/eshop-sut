## Title
[Major] Nút hành động tích cực không dùng màu xanh dương theo spec

## Description
Nút "Đăng Ký" nền đỏ (Register.jsx:71-76); các nút tích cực khác (thêm giỏ/thanh toán xanh lá, áp mã cam) — không nút nào dùng xanh dương như spec.

## Steps to Reproduce
1. Mở lần lượt Đăng ký, Chi tiết SP, Giỏ hàng, Thanh toán.
2. Quan sát màu nền các nút hành động tích cực.

## Expected Result
Tất cả nút hành động tích cực đồng nhất màu xanh dương.

## Actual Result
- (GUI-IA01-03) Nút "Đăng Ký" có màu nền rgb(239, 68, 68) (đỏ, bg-red-500) — dùng màu cảnh báo cho hành động tích cực thay vì xanh dương.
- (GUI-IA01-04) Nút "Thêm vào giỏ hàng" (Chi tiết SP) màu rgb(22, 163, 74) — xanh lá, không phải xanh dương. Các nút tích cực khác (thanh toán xanh lá, áp mã cam) cũng lệch spec.

## Environment
Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)
GUI-IA01-03, GUI-IA01-04

## Requirement
FR-21 (nhất quán màu sắc)

## Severity
Major — Vi phạm quy tắc màu FR-21 trên nhiều nút mua hàng/đăng ký.

## Screenshot
![GUI-IA01-03](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965690/eshop-hw03/gui-checklist/GUI-IA01-03.png) ![GUI-IA01-04](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965691/eshop-hw03/gui-checklist/GUI-IA01-04.png)