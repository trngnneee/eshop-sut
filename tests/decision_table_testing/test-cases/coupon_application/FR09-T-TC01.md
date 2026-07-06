# FR09-T-TC01: Chấp nhận mã percent khi tổng đơn hàng bằng đúng ngưỡng tối thiểu

## Requirement ID

FR-09

## Module / Test type / Technique

Coupon Application / Functional / Decision Table / Pairwise

## Preconditions

- User đã đăng nhập bằng JWT hợp lệ.
- Coupon `SAVE10` tồn tại, còn hạn, đang hoạt động và có `min_order_amount = 300000`.
- User chưa từng dùng coupon `SAVE10`.
- Giỏ hàng có tổng tiền đúng bằng `300000`.

## Test data

| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Actor | user |
| Endpoint | POST /api/apply-coupon |
| Coupon code | SAVE10 |
| Coupon type | percent |
| Total amount | 300000 |
| Min order amount | 300000 |
| Token | JWT hợp lệ |
| User usage | 0 / 1 |

## Test steps

1. Đăng nhập bằng tài khoản user hợp lệ.
2. Chuẩn bị giỏ hàng có tổng tiền `300000`.
3. Gửi request `POST /api/apply-coupon` với body `{"code":"SAVE10","total_amount":300000,"user_id":<user_id>}`.
4. Kiểm tra response tại điều kiện biên `total_amount = min_order_amount`.

## Expected result

- Hệ thống chấp nhận mã vì FR-09 quy định tổng đơn hàng `>= min_order_amount`.
- `discount_amount = 30000`.
- `final_amount = 270000`.
- Response có thông báo áp dụng mã giảm giá thành công.

## Status / Related bugs

Failed / BUG-FR09-T-01 - Hệ thống từ chối đơn hàng bằng đúng ngưỡng tối thiểu
