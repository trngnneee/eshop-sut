# FR09-T-TC03: Chấp nhận mã fixed khi tổng đơn hàng bằng đúng ngưỡng tối thiểu

## Requirement ID

FR-09

## Module / Test type / Technique

Coupon Application / Functional / Decision Table / Pairwise

## Preconditions

- User đã đăng nhập bằng JWT hợp lệ.
- Coupon `BIGBUY` tồn tại, `is_active = 1`, `type = fixed`, `discount_value = 50000`, `min_order_amount = 500000`, `expired_at = 2099-12-31`, `max_uses_per_user = 1`.
- User chưa từng dùng coupon `BIGBUY`.
- Giỏ hàng có tổng tiền đúng bằng `500000`.

## Test data

| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Actor | user |
| Endpoint | POST /api/apply-coupon |
| Coupon code | BIGBUY |
| Coupon type | fixed |
| Total amount | 500000 |
| Min order amount | 500000 |
| Token | JWT hợp lệ |
| User usage | 0 / 1 |

## Test steps

1. Đăng nhập bằng tài khoản user hợp lệ.
2. Chuẩn bị giỏ hàng có tổng tiền `500000`.
3. Gửi request `POST /api/apply-coupon` với body `{"code":"BIGBUY","total_amount":500000,"user_id":<user_id>}`.
4. Kiểm tra response tại điều kiện biên `total_amount = min_order_amount` cho mã fixed.

## Expected result

- Hệ thống chấp nhận mã vì FR-09 quy định tổng đơn hàng `>= min_order_amount`.
- `discount_amount = 50000`.
- `final_amount = 450000`.
- Response có thông báo áp dụng mã giảm giá thành công.

## Status / Related bugs

Failed / BUG-FR09-T-01 - Hệ thống từ chối đơn hàng bằng đúng ngưỡng tối thiểu
