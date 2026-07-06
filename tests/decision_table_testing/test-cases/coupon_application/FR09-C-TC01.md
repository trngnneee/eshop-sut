# FR09-C-TC01: Từ chối mã giảm giá không tồn tại hoặc không hoạt động

## Requirement ID

FR-09

## Module / Test type / Technique

Coupon Application / Functional / Decision Table

## Preconditions

- User đã đăng nhập bằng JWT hợp lệ.
- Mã `NOTFOUND` không tồn tại trong CSDL hoặc mã thử nghiệm tương đương đang có `is_active = 0`.
- Giỏ hàng có tổng tiền đủ lớn để không bị lỗi ngưỡng đơn hàng che lấp.

## Test data

| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Actor | user |
| Endpoint | POST /api/apply-coupon |
| Coupon code | NOTFOUND |
| Total amount | 500000 |
| Token | JWT hợp lệ |

## Test steps

1. Đăng nhập bằng tài khoản user hợp lệ.
2. Chuẩn bị giỏ hàng có tổng tiền `500000`.
3. Gửi request `POST /api/apply-coupon` với body `{"code":"NOTFOUND","total_amount":500000,"user_id":<user_id>}`.
4. Kiểm tra response lỗi mã giảm giá.

## Expected result

- Hệ thống trả về HTTP 404 hoặc lỗi nghiệp vụ phù hợp.
- Response thông báo mã giảm giá không tồn tại hoặc đã bị vô hiệu hóa.
- Không áp dụng bất kỳ giảm giá nào cho đơn hàng.

## Status / Related bugs

Passed / None
