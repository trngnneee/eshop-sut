## Title
[Minor] Giỏ hàng không gộp sản phẩm trùng

## Description
`addToCart` luôn push entry mới (CartContext.jsx:8-10).

## Steps to Reproduce
1. Thêm cùng 1 SP 2 lần, mở `/cart`.

## Expected Result
Gộp thành 1 dòng với số lượng cộng dồn.

## Actual Result
- (GUI-GAP-02) Thêm cùng 1 sản phẩm 2 lần tạo 2 dòng riêng trong giỏ thay vì gộp thành 1 dòng số lượng 2 (addToCart luôn push entry mới).

## Environment
Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)
GUI-GAP-02

## Requirement
Heuristic (cart merge)

## Severity
Minor — Thêm cùng SP nhiều lần tạo nhiều dòng, khó quản lý số lượng.

## Screenshot
![GUI-GAP-02](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965681/eshop-hw03/gui-checklist/GUI-GAP-02.png)