## Title
[Minor] Input số lượng không có ràng buộc min

## Description
Input số lượng không có `min` (ProductDetail.jsx:57-62), nhập được `-1`.

## Steps to Reproduce
1. Mở `/product/1`, đặt số lượng `-1` rồi thêm vào giỏ.

## Expected Result
Số lượng <1 bị chặn/chuẩn hoá về 1.

## Actual Result
- (GUI-IA02-09) Input số lượng không có ràng buộc min (min=null); nhập được giá trị "-1" (<1) — cho phép số lượng vô lý.

## Environment
Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)
GUI-IA02-09

## Requirement
FR-22 (format constraints: quantity)

## Severity
Minor — Cho phép số lượng ≤0 hoặc vô lý vào giỏ.

## Screenshot
![GUI-IA02-09](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965724/eshop-hw03/gui-checklist/GUI-IA02-09.png)