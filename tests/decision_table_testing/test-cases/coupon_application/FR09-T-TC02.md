# FR09-T-TC02: Từ chối mã khi tổng đơn hàng thấp hơn ngưỡng tối thiểu

## Requirement ID

FR-09

## Module / Test type / Technique

Coupon Application / Functional / Decision Table

## Preconditions

- User đã đăng nhập bằng JWT hợp lệ.
- Coupon `SAVE10` tồn tại, còn hạn, đang hoạt động và có `min_order_amount = 300000`.
- User chưa từng dùng coupon `SAVE10`.
- Giỏ hàng có tổng tiền thấp hơn ngưỡng tối thiểu.

## Test data

| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Actor | user |
| Endpoint | POST /api/apply-coupon |
| Coupon code | SAVE10 |
| Total amount | 299999 |
| Min order amount | 300000 |
| Token | JWT hợp lệ |
| User usage | 0 / 1 |

## Test steps

1. Đăng nhập bằng tài khoản user hợp lệ.
2. Chuẩn bị giỏ hàng có tổng tiền `299999`.
3. Gửi request `POST /api/apply-coupon` với body `{"code":"SAVE10","total_amount":299999,"user_id":<user_id>}`.
4. Kiểm tra response lỗi ngưỡng đơn hàng.

## Expected result

- Hệ thống trả về HTTP 400 hoặc lỗi nghiệp vụ phù hợp.
- Response thông báo đơn hàng chưa đủ giá trị tối thiểu để áp dụng mã.
- Không trả về `discount_amount`/`final_amount` thành công.

## Status / Related bugs

Passed / None
