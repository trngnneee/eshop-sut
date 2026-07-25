## Title
[Major] Giỏ hàng mất toàn bộ khi refresh trang

## Description
Giỏ chỉ nằm trong React state (CartContext.jsx:6), không lưu localStorage (trong khi token thì có).

## Steps to Reproduce
1. Thêm SP vào giỏ.
2. Nhấn F5.
3. Mở `/cart`.

## Expected Result
Giỏ giữ nguyên sản phẩm sau reload.

## Actual Result
- (GUI-GAP-01) Thêm SP vào giỏ rồi F5 (reload) → giỏ trống (0 dòng). Giỏ chỉ nằm trong React state, không lưu localStorage (trong khi token thì có).

## Environment
Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)
GUI-GAP-01

## Requirement
Heuristic (state persistence)

## Severity
Major — Reload là mất giỏ — trải nghiệm mua sắm gãy.

## Screenshot
![GUI-GAP-01](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965680/eshop-hw03/gui-checklist/GUI-GAP-01.png)