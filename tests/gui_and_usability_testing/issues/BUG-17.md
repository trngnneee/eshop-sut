## Title
[Major] Click "Thêm vào giỏ hàng" lần đầu bị bỏ qua

## Description
Biến `clickCount` nuốt lần bấm đầu tiên (ProductDetail.jsx:22-32); phải bấm lần 2 mới có tác dụng.

## Steps to Reproduce
1. Mở `/product/1`.
2. Bấm "Thêm vào giỏ hàng" đúng 1 lần.
3. Mở giỏ kiểm tra.

## Expected Result
Bấm 1 lần → sản phẩm vào giỏ ngay + hiện "Đã thêm".

## Actual Result
- (GUI-IA04-02) Click "Thêm vào giỏ hàng" lần đầu bị "nuốt" (clickCount): không có feedback "Đã thêm" và giỏ vẫn trống (0 dòng) — mất 1 lần thao tác.

## Environment
Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)
GUI-IA04-02

## Requirement
FR-24 (add-to-cart feedback)

## Severity
Major — Mất thao tác người dùng; sản phẩm không vào giỏ ở lần bấm đầu.

## Screenshot
![GUI-IA04-02](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965754/eshop-hw03/gui-checklist/GUI-IA04-02.png)