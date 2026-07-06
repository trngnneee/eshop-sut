# FR09-U-TC01: Từ chối mã khi user đã dùng hết số lượt cho phép

## Requirement ID

FR-09

## Module / Test type / Technique

Coupon Application / Functional / Decision Table

## Preconditions

- User đã đăng nhập bằng JWT hợp lệ.
- Coupon `SAVE10` tồn tại, còn hạn, đang hoạt động, `max_uses_per_user = 1`.
- Bảng `coupon_usage` đã có 1 bản ghi sử dụng `SAVE10` của user hiện tại.
- Giỏ hàng có tổng tiền `500000`.

## Test data

| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Actor | user |
| Endpoint | POST /api/apply-coupon |
| Coupon code | SAVE10 |
| Total amount | 500000 |
| Token | JWT hợp lệ |
| User usage | 1 / 1 |

## Test steps

1. Đăng nhập bằng tài khoản user đã từng dùng coupon `SAVE10`.
2. Chuẩn bị giỏ hàng có tổng tiền `500000`.
3. Gửi request `POST /api/apply-coupon` với body `{"code":"SAVE10","total_amount":500000,"user_id":<user_id>}`.
4. Kiểm tra response lỗi giới hạn số lượt sử dụng.

## Expected result

- Hệ thống trả về HTTP 400 hoặc lỗi nghiệp vụ phù hợp.
- Response thông báo user đã sử dụng mã này đủ số lần cho phép.
- Không áp dụng bất kỳ giảm giá nào cho đơn hàng.

## Status / Related bugs

Passed / None
