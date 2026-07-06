# FR09-E-TC01: Từ chối mã giảm giá đã hết hạn

## Requirement ID

FR-09

## Module / Test type / Technique

Coupon Application / Functional / Decision Table

## Preconditions

- User đã đăng nhập bằng JWT hợp lệ.
- Coupon `EXPIRED` tồn tại, `is_active = 1`, `type = percent`, `discount_value = 20`, `min_order_amount = 100000`, `expired_at = 2020-01-01`.
- User chưa từng dùng coupon `EXPIRED`.
- Giỏ hàng có tổng tiền vượt ngưỡng tối thiểu.

## Test data

| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Actor | user |
| Endpoint | POST /api/apply-coupon |
| Coupon code | EXPIRED |
| Coupon type | percent |
| Total amount | 150000 |
| Expired at | 2020-01-01 |
| Token | JWT hợp lệ |
| User usage | 0 / 1 |

## Test steps

1. Đăng nhập bằng tài khoản user hợp lệ.
2. Chuẩn bị giỏ hàng có tổng tiền `150000`.
3. Gửi request `POST /api/apply-coupon` với body `{"code":"EXPIRED","total_amount":150000,"user_id":<user_id>}`.
4. Kiểm tra response lỗi hết hạn.

## Expected result

- Hệ thống trả về HTTP 400 hoặc lỗi nghiệp vụ phù hợp.
- Response thông báo mã giảm giá đã hết hạn.
- Không áp dụng bất kỳ giảm giá nào cho đơn hàng.

## Status / Related bugs

Passed / None
