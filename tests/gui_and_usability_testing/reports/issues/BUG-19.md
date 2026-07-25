## Title
[Major] Thiếu loading/error state khi tải dữ liệu

## Description
Home fetch không loading (Home.jsx:13-30); Chi tiết SP kẹt "Đang tải..." khi lỗi (ProductDetail.jsx:15-20); lỗi tải đơn bị nuốt thành "chưa có đơn" (Profile.jsx:26-29).

## Steps to Reproduce
1. Bật Network Slow 3G, mở `/`.
2. Tắt backend, mở `/product/1`.
3. Làm lỗi `/api/orders/my-orders`, mở `/profile`.

## Expected Result
Có spinner/skeleton khi chờ; lỗi có error state riêng, phân biệt với empty.

## Actual Result
- (GUI-IA04-08) Khi API bị làm chậm, trang chủ không hiển thị spinner/skeleton nào (số phần tử loading: 0) — người dùng thấy trang trống trong lúc chờ.
- (GUI-IA04-09) Khi API sản phẩm lỗi, trang kẹt ở "Đang tải..." (không có error state / nút thử lại) — chỉ log console, kẹt "Đang tải..." vô hạn.
- (GUI-IA04-16) Lỗi API tải đơn bị "nuốt" (catch → setOrders([])) nên hiển thị "Bạn chưa có đơn hàng nào" giống hệt trạng thái trống — không phân biệt lỗi với empty.

## Environment
Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)
GUI-IA04-08, GUI-IA04-09, GUI-IA04-16

## Requirement
Heuristic (loading/error state)

## Severity
Major — Trang trống hoặc kẹt "Đang tải...", lỗi API bị nhầm thành trạng thái trống.

## Screenshot
![GUI-IA04-08](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965764/eshop-hw03/gui-checklist/GUI-IA04-08.png) ![GUI-IA04-09](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965766/eshop-hw03/gui-checklist/GUI-IA04-09.png) ![GUI-IA04-16](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965777/eshop-hw03/gui-checklist/GUI-IA04-16.png)