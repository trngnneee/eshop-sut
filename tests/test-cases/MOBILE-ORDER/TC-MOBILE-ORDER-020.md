# Test Case Template


## Test Case ID

TC-MOBILE-ORDER-020


## Feature

Lịch sử đơn hàng trên phân hệ Mobile


## Requirement Reference

FR-10, FR-20


## Testing Technique

Domain Testing


## Test Objective

Kiểm tra lịch sử đơn hàng trên mobile chỉ hiển thị đơn hàng của user hiện tại, không hiển thị đơn hàng của người dùng khác. Theo FR-11, người dùng chỉ xem được đơn hàng của chính mình.


## Preconditions

- Hệ thống backend đang hoạt động.
- Có 2 tài khoản user: User A và User B.
- Cả 2 user đều đã đặt đơn hàng.
- User A đã đăng nhập trên mobile app.


## Test Data

| Parameter | Value |
|-|-|
| User đăng nhập | User A |
| Đơn hàng của User A | Có |
| Đơn hàng của User B | Có (nhưng không nên hiển thị) |


## Test Steps

1. Đăng nhập trên mobile bằng tài khoản User A.

2. Vào mục Lịch sử đơn hàng.

3. Kiểm tra danh sách đơn hàng hiển thị.

4. Ghi nhận số lượng và mã các đơn hàng hiển thị của User A.

5. Đăng xuất, đăng nhập bằng User B và kiểm tra danh sách đơn hàng hiển thị có khác biệt.


## Expected Result

- Danh sách đơn hàng CHỈ hiển thị đơn hàng của user hiện tại (User A).
- KHÔNG hiển thị bất kỳ đơn hàng nào của user khác (User B).
- Khi đăng nhập bằng User B, danh sách chỉ hiển thị đơn của User B, không lẫn đơn của User A.


## Actual Result

Không lẫn đơn hàng của user khác khi hiển thị danh sách đơn hàng cho user hiện tại.

## Status

PASSED


## Bug Reference
None
