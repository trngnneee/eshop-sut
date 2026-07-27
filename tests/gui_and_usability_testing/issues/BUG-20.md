## Title
[Major] Giỏ hàng không được reset sau khi thanh toán thành công

## Description
`clearCart` được import nhưng không bao giờ gọi (Checkout.jsx:9,62).

## Steps to Reproduce
1. Thêm SP, đăng nhập, hoàn tất thanh toán.
2. Mở lại `/cart`.

## Expected Result
Giỏ trống sau khi đặt hàng thành công.

## Actual Result
- (GUI-IA04-15) Sau thanh toán thành công, giỏ hàng vẫn còn 1 sản phẩm cũ (clearCart không được gọi) — trạng thái giỏ không được reset.

## Environment
Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)
GUI-IA04-15

## Requirement
Heuristic (state consistency)

## Severity
Major — Giỏ còn hàng cũ sau khi đặt, dễ đặt trùng.

## Screenshot
![GUI-IA04-15](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965775/eshop-hw03/gui-checklist/GUI-IA04-15.png)