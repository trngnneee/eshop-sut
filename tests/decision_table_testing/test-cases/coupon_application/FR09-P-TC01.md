# FR09-P-TC01: Áp dụng mã percent khi tất cả điều kiện hợp lệ

## Requirement ID

FR-09

## Module / Test type / Technique

Coupon Application / Functional / Decision Table / Pairwise

## Preconditions

- User đã đăng nhập bằng JWT hợp lệ.
- Coupon `SAVE10` tồn tại, `is_active = 1`, `type = percent`, `discount_value = 10`, `min_order_amount = 300000`, `expired_at = 2099-12-31`, `max_uses_per_user = 1`.
- User chưa từng dùng coupon `SAVE10`.
- Giỏ hàng có tổng tiền `500000`.

## Test data

| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Actor | user |
| Endpoint | POST /api/apply-coupon |
| Coupon code | SAVE10 |
| Coupon type | percent |
| Total amount | 500000 |
| Token | JWT hợp lệ |
| User usage | 0 / 1 |

## Test steps

1. Đăng nhập bằng tài khoản user hợp lệ.
2. Chuẩn bị giỏ hàng có tổng tiền `500000`.
3. Gửi request `POST /api/apply-coupon` với body `{"code":"SAVE10","total_amount":500000,"user_id":<user_id>}`.
4. Kiểm tra response tính giảm giá và tổng tiền sau giảm.

## Expected result

- Hệ thống trả về HTTP 200 hoặc response thành công phù hợp.
- `discount_amount = 50000`.
- `final_amount = 450000`.
- Response có thông báo áp dụng mã giảm giá thành công.

## Status / Related bugs

Failed / BUG-FR09-P-01 - Công thức giảm giá percent tính sai `discount_amount`
