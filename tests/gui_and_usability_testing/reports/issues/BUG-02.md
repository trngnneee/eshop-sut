## Title
[Blocker] Tổng tiền thanh toán là input sửa được và gửi thẳng lên API

## Description
Ô "Tổng tiền thanh toán" là `input type=number` sửa được (Checkout.jsx:94-103); giá trị sửa tay được gửi thẳng vào `POST /api/checkout` (dòng 44-48) không kiểm tra lại phía server.

## Steps to Reproduce
1. Thêm sản phẩm vào giỏ, đăng nhập, mở `/checkout`.
2. Sửa ô "Tổng tiền thanh toán" thành `1000`.
3. Bấm "Xác Nhận Thanh Toán", xem payload ở Network tab.

## Expected Result
Tổng tiền là giá trị chỉ đọc; số tiền gửi lên server không thể bị sửa từ UI.

## Actual Result
- (GUI-IA02-10) Ô "Tổng tiền thanh toán" là input number sửa được: đổi thành "1000" thành công → số tiền do người dùng nhập được gửi thẳng lên API /api/checkout (lỗi nghiêm trọng).

## Environment
Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)
GUI-IA02-10

## Requirement
Heuristic (input constraint)

## Severity
Blocker — Người dùng tự đặt số tiền phải trả → thất thoát doanh thu, lỗi nghiệp vụ nghiêm trọng.

## Screenshot
![GUI-IA02-10](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965726/eshop-hw03/gui-checklist/GUI-IA02-10.png)