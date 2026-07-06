# FR09-C-TC02: Từ chối request áp dụng mã khi code rỗng

## Requirement ID

FR-09

## Module / Test type / Technique

Coupon Application / Functional / Decision Table

## Preconditions

- User đã đăng nhập bằng JWT hợp lệ.
- Giỏ hàng có tổng tiền đủ lớn để áp dụng coupon hợp lệ.

## Test data

| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Actor | user |
| Endpoint | POST /api/apply-coupon |
| Coupon code | `""` |
| Total amount | 500000 |
| Token | JWT hợp lệ |

## Test steps

1. Đăng nhập bằng tài khoản user hợp lệ.
2. Chuẩn bị giỏ hàng có tổng tiền `500000`.
3. Gửi request `POST /api/apply-coupon` với body `{"code":"","total_amount":500000,"user_id":<user_id>}`.
4. Kiểm tra response lỗi nhập mã.

## Expected result

- Hệ thống trả về HTTP 400 hoặc lỗi validate phù hợp.
- Response thông báo người dùng cần nhập mã giảm giá.
- Không áp dụng bất kỳ giảm giá nào cho đơn hàng.

## Status / Related bugs

Passed / None
