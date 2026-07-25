## Title
[Major] Hành động phá huỷ (Xóa giỏ, Hủy đơn) không có dialog xác nhận

## Description
Bấm "Xóa" (Cart.jsx:50-55) và "Hủy đơn" (Profile.jsx:200-208) thực hiện ngay, không hỏi xác nhận.

## Steps to Reproduce
1. Mở `/cart` có hàng, bấm "Xóa".
2. Mở `/profile`, bấm "Hủy đơn" một đơn chưa giao.

## Expected Result
Có dialog xác nhận trước khi xoá/huỷ; chọn Hủy → giữ nguyên.

## Actual Result
- (GUI-IA04-03) Bấm "Xóa" item xoá ngay (dòng giỏ 1→0) không có dialog xác nhận — thao tác phá huỷ không có bước chặn.
- (GUI-IA04-04) Bấm "Hủy đơn" huỷ ngay, không có dialog xác nhận trước hành động không hoàn tác (chỉ có alert "Hủy đơn thành công" sau khi đã huỷ).

## Environment
Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)
GUI-IA04-03, GUI-IA04-04

## Requirement
FR-24 (confirmation dialog)

## Severity
Major — Dễ mất dữ liệu do bấm nhầm, không hoàn tác được.

## Screenshot
![GUI-IA04-03](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965756/eshop-hw03/gui-checklist/GUI-IA04-03.png) ![GUI-IA04-04](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965757/eshop-hw03/gui-checklist/GUI-IA04-04.png)