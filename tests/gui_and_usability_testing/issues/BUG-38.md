## Title
[Minor] Trang thanh toán thiếu đường quay lại Giỏ hàng

## Description
Không có link/nút quay lại giỏ (Checkout.jsx:79-150).

## Steps to Reproduce
1. Mở `/checkout`, tìm nút quay lại giỏ.

## Expected Result
Có link/nút quay lại giỏ hàng không mất dữ liệu.

## Actual Result
- (GUI-IA03-08) Trang thanh toán không có link/nút quay lại Giỏ hàng trước khi xác nhận — người dùng bị cụt đường về để sửa giỏ.

## Environment
Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)
GUI-IA03-08

## Requirement
Heuristic (back/continue links)

## Severity
Minor — Người dùng cụt đường về để sửa giỏ.

## Screenshot
![GUI-IA03-08](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965744/eshop-hw03/gui-checklist/GUI-IA03-08.png)