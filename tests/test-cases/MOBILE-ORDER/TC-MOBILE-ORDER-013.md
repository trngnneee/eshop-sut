# Test Case Template


## Test Case ID

TC-MOBILE-ORDER-013


## Feature

Hủy đơn hàng trên phân hệ Mobile — Phân quyền


## Requirement Reference

FR-10, FR-20


## Testing Technique

Domain Testing


## Test Objective

Kiểm tra User chưa đăng nhập không thể truy cập mục Lịch sử đơn hàng và không thể hủy đơn hàng trên mobile.


## Preconditions

- Hệ thống backend đang hoạt động.
- User CHƯA đăng nhập trên mobile app (hoặc đã đăng xuất).


## Test Data

| Parameter | Value |
|-|-|
| Trạng thái xác thực | Chưa đăng nhập |
| Hành động | Cố truy cập Lịch sử đơn hàng |


## Test Steps

1. Mở ứng dụng mobile mà KHÔNG đăng nhập.

2. Thử truy cập mục Lịch sử đơn hàng từ thanh điều hướng hoặc menu.

3. Quan sát phản hồi của giao diện.


## Expected Result

- Giao diện mobile không cho phép truy cập Lịch sử đơn hàng khi chưa đăng nhập.
- Ứng dụng chuyển hướng User tới màn hình Đăng nhập hoặc hiển thị thông báo yêu cầu đăng nhập.
- User không thể nhìn thấy hoặc thao tác bất kỳ đơn hàng nào.


## Actual Result



## Status

NOT EXECUTED


## Bug Reference

